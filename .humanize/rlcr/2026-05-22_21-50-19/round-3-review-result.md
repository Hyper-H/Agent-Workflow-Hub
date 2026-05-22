- [P2] Avoid reusing prior branch task on start — C:\Users\Administrator\Documents\context-handoff\tools\worktree-context-reuse-v1\context_sidecar.py:753-755
  When a user reuses the same worktree by switching from branch A to branch B and runs `start-feature`, `find_task` falls back to a worktree match if there is no branch match. That means an existing active task for branch A is passed to `upsert_task`, which rewrites its branch/worktree fields to branch B and saves it, losing the original active task instead of creating a new task for the new branch. For `start-feature`, avoid the worktree fallback or treat it as a conflict.
2026-05-22T14:34:32.113774Z  WARN codex_state::runtime: failed to remove legacy logs db file C:\Users\Administrator\.codex\logs_2.sqlite: 另一个程序正在使用此文件，进程无法访问。 (os error 32)
2026-05-22T14:34:32.113824Z  WARN codex_state::runtime: failed to remove legacy logs db file C:\Users\Administrator\.codex\logs_2.sqlite-shm: 另一个程序正在使用此文件，进程无法访问。 (os error 32)
2026-05-22T14:34:32.113850Z  WARN codex_state::runtime: failed to remove legacy logs db file C:\Users\Administrator\.codex\logs_2.sqlite-wal: 另一个程序正在使用此文件，进程无法访问。 (os error 32)
2026-05-22T14:34:32.114783Z  WARN codex_state::runtime: failed to open state db at C:\Users\Administrator\.codex\state_5.sqlite: migration 23 was previously applied but is missing in the resolved migrations
2026-05-22T14:34:32.115455Z  WARN codex_state::runtime: failed to remove legacy logs db file C:\Users\Administrator\.codex\logs_2.sqlite: 另一个程序正在使用此文件，进程无法访问。 (os error 32)
2026-05-22T14:34:32.115532Z  WARN codex_state::runtime: failed to remove legacy logs db file C:\Users\Administrator\.codex\logs_2.sqlite-shm: 另一个程序正在使用此文件，进程无法访问。 (os error 32)
2026-05-22T14:34:32.115573Z  WARN codex_state::runtime: failed to remove legacy logs db file C:\Users\Administrator\.codex\logs_2.sqlite-wal: 另一个程序正在使用此文件，进程无法访问。 (os error 32)
2026-05-22T14:34:32.116512Z  WARN codex_state::runtime: failed to open state db at C:\Users\Administrator\.codex\state_5.sqlite: migration 23 was previously applied but is missing in the resolved migrations
2026-05-22T14:34:32.148333Z  WARN codex_rollout::list: state db discrepancy during find_thread_path_by_id_str_in_subdir: falling_back
The new lifecycle command can overwrite an unrelated active task when a worktree is reused across branches, causing loss of tracked state. This is a functional bug in the V2 task lifecycle behavior.

Review comment:

- [P2] Avoid reusing prior branch task on start — C:\Users\Administrator\Documents\context-handoff\tools\worktree-context-reuse-v1\context_sidecar.py:753-755
  When a user reuses the same worktree by switching from branch A to branch B and runs `start-feature`, `find_task` falls back to a worktree match if there is no branch match. That means an existing active task for branch A is passed to `upsert_task`, which rewrites its branch/worktree fields to branch B and saves it, losing the original active task instead of creating a new task for the new branch. For `start-feature`, avoid the worktree fallback or treat it as a conflict.
