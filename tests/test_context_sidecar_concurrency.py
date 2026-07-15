from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import multiprocessing
import os
from pathlib import Path
import sys
import tempfile
import time
import traceback
import unittest
from unittest import mock


PROJECT_ID = "concurrent-update-test"
WORKER_COUNT = 4


def load_sidecar_module(script_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load sidecar module: {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def alias_worker(
    script_path_text: str,
    worktree_text: str,
    home_text: str,
    active_tasks_path_text: str,
    ready_marker_text: str,
    result_path_text: str,
    worker_index: int,
) -> None:
    script_path = Path(script_path_text)
    active_tasks_path = Path(active_tasks_path_text).resolve()
    ready_marker = Path(ready_marker_text)
    result_path = Path(result_path_text)
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        os.environ["HOME"] = home_text
        os.environ["USERPROFILE"] = home_text
        module = load_sidecar_module(script_path, f"context_sidecar_worker_{os.getpid()}_{worker_index}")
        module.FILE_LOCK_TIMEOUT_SECONDS = 60
        original_file_lock = module.file_lock
        reported_ready = False

        @contextlib.contextmanager
        def reporting_file_lock(path: Path):
            nonlocal reported_ready
            if not reported_ready and Path(path).resolve() == active_tasks_path:
                ready_marker.write_text("ready\n", encoding="utf-8")
                reported_ready = True
            with original_file_lock(path):
                yield

        module.file_lock = reporting_file_lock
        argv = [
            str(script_path),
            "alias-task",
            "--worktree",
            worktree_text,
            "--project-id",
            PROJECT_ID,
            "--task-id",
            f"task-{worker_index}",
            "--alias",
            f"alias-{worker_index}",
        ]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exit_code = module.main()
        result_path.write_text(
            json.dumps(
                {"exitCode": exit_code, "stdout": stdout.getvalue(), "stderr": stderr.getvalue()},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        if exit_code != 0:
            raise RuntimeError(f"worker returned {exit_code}")
    except BaseException:
        result_path.write_text(
            json.dumps(
                {"exitCode": 1, "stdout": stdout.getvalue(), "stderr": stderr.getvalue(), "traceback": traceback.format_exc()},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        raise


class ConcurrentSidecarUpdateTests(unittest.TestCase):
    repo_root = Path(__file__).resolve().parents[1]
    script_paths = [
        repo_root / "skills" / "agent-workflow-hub" / "scripts" / "context_sidecar.py",
        repo_root / "skills" / "context-handoff" / "scripts" / "context_sidecar.py",
    ]

    def test_parallel_cli_updates_preserve_all_tasks(self) -> None:
        for script_path in self.script_paths:
            with self.subTest(script=str(script_path.relative_to(self.repo_root))):
                self.run_parallel_alias_updates(script_path)

    def run_parallel_alias_updates(self, script_path: Path) -> None:
        with tempfile.TemporaryDirectory() as temp_dir_text:
            temp_dir = Path(temp_dir_text)
            home = temp_dir / "home"
            home.mkdir()
            with mock.patch.dict(os.environ, {"HOME": str(home), "USERPROFILE": str(home)}):
                module = load_sidecar_module(script_path, f"context_sidecar_setup_{time.time_ns()}")
                manager = module.SidecarManager(self.repo_root, project_id_override=PROJECT_ID)
                manager.ensure_layout()
                manager.sidecar_config()
                tasks = [
                    {
                        "taskId": f"task-{index}",
                        "status": "active",
                        "branch": f"test-branch-{index}",
                        "worktreePath": str(self.repo_root),
                        "aliases": [],
                    }
                    for index in range(WORKER_COUNT)
                ]
                module.write_json(
                    manager.active_tasks_path,
                    {"version": module.SIDECAR_VERSION, "projectId": PROJECT_ID, "tasks": tasks},
                )
                manager.load_active_tasks_with_project_state()

            active_tasks_path = manager.active_tasks_path
            project_state_path = manager.project_state_path
            active_lock_path = module.lock_path_for(active_tasks_path)
            active_lock_path.write_text("test gate\n", encoding="utf-8")

            ready_dir = temp_dir / "ready"
            result_dir = temp_dir / "results"
            ready_dir.mkdir()
            result_dir.mkdir()
            context = multiprocessing.get_context("spawn")
            processes = []
            for index in range(WORKER_COUNT):
                process = context.Process(
                    target=alias_worker,
                    args=(
                        str(script_path),
                        str(self.repo_root),
                        str(home),
                        str(active_tasks_path),
                        str(ready_dir / f"{index}.ready"),
                        str(result_dir / f"{index}.json"),
                        index,
                    ),
                )
                process.start()
                processes.append(process)

            try:
                deadline = time.monotonic() + 20
                while time.monotonic() < deadline:
                    if len(list(ready_dir.glob("*.ready"))) == WORKER_COUNT:
                        break
                    time.sleep(0.05)
                else:
                    self.fail(f"workers did not all reach the active-task lock; results: {self.worker_results(result_dir)}")

                active_lock_path.unlink()
                for process in processes:
                    process.join(30)
                alive = [process.pid for process in processes if process.is_alive()]
                self.assertFalse(alive, f"workers did not exit: {alive}")
                self.assertEqual(
                    [process.exitcode for process in processes],
                    [0] * WORKER_COUNT,
                    self.worker_results(result_dir),
                )
            finally:
                if active_lock_path.exists():
                    active_lock_path.unlink()
                for process in processes:
                    if process.is_alive():
                        process.terminate()
                    process.join(5)

            active_payload = json.loads(active_tasks_path.read_text(encoding="utf-8"))
            tasks_by_id = {task["taskId"]: task for task in active_payload["tasks"]}
            self.assertEqual(set(tasks_by_id), {f"task-{index}" for index in range(WORKER_COUNT)})
            for index in range(WORKER_COUNT):
                self.assertEqual(tasks_by_id[f"task-{index}"]["aliases"], [f"alias-{index}"])

            project_state = json.loads(project_state_path.read_text(encoding="utf-8"))
            state_tasks_by_id = {task["taskId"]: task for task in project_state["activeTasks"]}
            self.assertEqual(project_state["activeTaskCount"], WORKER_COUNT)
            self.assertEqual(set(state_tasks_by_id), set(tasks_by_id))
            for index in range(WORKER_COUNT):
                self.assertEqual(state_tasks_by_id[f"task-{index}"]["aliases"], [f"alias-{index}"])
            self.assertFalse(active_lock_path.exists())

    @staticmethod
    def worker_results(result_dir: Path) -> str:
        results = {}
        for path in sorted(result_dir.glob("*.json")):
            results[path.name] = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(results, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    unittest.main()
