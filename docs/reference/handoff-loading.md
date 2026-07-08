# Handoff Loading Reference

`load-handoff` loads saved sidecar/handoff state for a new thread.

```text
load-handoff
  --worktree <path>
  [--project-id <id>]
  [--base-branch <branch>]
  [--query <natural-language phrase>]
  [--task-id <task id>]
  [--mode compact|section|full]
  [--section meta|receipt|objective|facts|inferences|unknowns|safety|done|not-done|blocker|touched-areas|key-files|next-step|validation|risks|thread-summary]
  [--reason resume|validation-needed|decision-trace|route-mismatch|stale-head|compact-insufficient|debug|user-asked|other]
  [--reason-note <short note>]
  [--language zh-CN|en]
```

Defaults:

```text
--mode compact
--reason resume
```

Resolution priority:

```text
--task-id > --query > current worktree
```

Rules:

- Query resolution reuses deterministic task routing.
- Ambiguous queries return candidates and no content.
- Compact mode does not return full Markdown.
- Section mode returns only the requested `##` section.
- Full mode returns the whole handoff only when explicitly requested.
- Events record mode, section, reason, role, and content size. They do not record handoff content.
