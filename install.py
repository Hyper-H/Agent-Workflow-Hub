#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_NAMES = ["agent-workflow-hub", "context-handoff"]


def default_codex_home() -> Path:
    return Path.home() / ".codex"


def copy_skill(skill_name: str, source: Path, destination: Path, dry_run: bool) -> None:
    if not source.exists():
        raise SystemExit(f"skill source not found: {source}")
    if not (source / "SKILL.md").exists():
        raise SystemExit(f"skill source is missing SKILL.md: {source}")

    print(f"Installing {skill_name} skill")
    print(f"Source: {source}")
    print(f"Target: {destination}")
    if dry_run:
        print("Dry run only; no files were changed.")
        print("")
        return

    if destination.exists():
        print("Existing installation found; replacing it with the bundled skill package.")
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )

    print("")
    print(f"Installed {skill_name} successfully.")
    print("")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install the Agent Workflow Hub and context-handoff Codex skill packages.")
    parser.add_argument(
        "--codex-home",
        default=str(default_codex_home()),
        help="Codex home directory. Defaults to ~/.codex.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be installed without changing files.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(__file__).resolve().parent
    codex_home = Path(args.codex_home).expanduser().resolve()
    for skill_name in SKILL_NAMES:
        source = repo_root / "skills" / skill_name
        destination = codex_home / "skills" / skill_name
        copy_skill(skill_name, source, destination, args.dry_run)
    if not args.dry_run:
        print("Installed successfully.")
        print("Restart or refresh Codex if the skill list does not update immediately.")
        print("GitHub CLI is optional; run `Use $agent-workflow-hub to run doctor for this project.` to check readiness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
