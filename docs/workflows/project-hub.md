# Project Hub Workflow

Project Hub threads should prefer inventory and receipts over full handoff loading.

Use:

- `audit-project` for multi-worktree inventory.
- `project-status` for compact sidecar state.
- `visualize-project` for a human-facing project map.
- `weekly-report` for progress reporting.
- `eval-report` for tool/workflow effectiveness metrics.

Use `load-handoff` only as a follow-up tool when a compact receipt or recommended action is insufficient.

Hub threads should route work to execution, discussion, research, review, validation, or dogfood threads and request durable receipts back. They should not become the place where every implementation detail is pasted.
