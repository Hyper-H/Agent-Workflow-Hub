# CLI Actions Reference

The CLI is the implementation layer behind `$agent-workflow-hub` and the compatible `$context-handoff` entrypoint. Users normally interact with the skill conversationally.

Common actions:

- `doctor`: readiness check.
- `setup`: create local sidecar layout.
- `start-feature`: create/update a sidecar task.
- `attach-thread`: attach thread role/label/purpose metadata.
- `orient-thread`: orient a new role-specific thread without writing by default.
- `resolve-task`: route a natural-language task phrase.
- `resume-feature`: resume the current worktree.
- `resume-query`: route a natural-language query, then resume.
- `handoff`: save task state, full handoff Markdown, compact receipt, continue phrase, changed files, freshness status, validation evidence, safety rules, and rollback notes.
- `load-handoff`: load compact, section, or explicit full handoff content.
- `audit-context`: audit one worktree.
- `audit-project`: audit project hub/worktree inventory.
- `visualize-project`: generate project map reports.
- `weekly-report`: project progress report.
- `eval-report`: workflow effectiveness proxy metrics.
- `finish-feature`: archive/finish a task and optionally prepare PR text.

Machine JSON keys, action names, event names, and status enums remain English.
