---
name: context-handoff
description: Conversation-first project and feature lifecycle state for Codex worktrees using the local context sidecar CLI.
---

# Context Handoff

Use this skill when the user wants to start, resume, hand off, finish, inspect, or report on feature work for the current repository. Keep normal interaction conversational. The Python sidecar CLI is the implementation layer, not the primary user experience.

## Implementation Layer

Resolve the sidecar CLI before running an action. Do not ask the user to paste the CLI path during normal use.

CLI resolution order:

1. If `CONTEXT_HANDOFF_CLI` is set, use that absolute path.
2. If the current repository contains `tools/worktree-context-reuse-v1/context_sidecar.py`, use that path.
3. If `%USERPROFILE%\Documents\context-handoff\tools\worktree-context-reuse-v1\context_sidecar.py` exists, use that path as the local installed development copy.
4. If none of the above exists, explain that the sidecar CLI is not installed and ask the user to install or clone `context-handoff`.

When using a CLI outside the current repository, pass the current worktree explicitly:

```powershell
python <resolved-context-sidecar.py> <action> --worktree <current-worktree>
```

When using the current repository's bundled CLI, running from the repository root is also valid:

```powershell
python tools\worktree-context-reuse-v1\context_sidecar.py <action>
```

The sidecar stays local at:

```text
%USERPROFILE%\.codex\projects\<project-id>\
```

Do not write dynamic task state into tracked repo docs. Do not require MCP for this V2 workflow.

## Actions

- `start-feature`: Create or update the active task for the current branch/worktree. Use when the user starts a new feature or says what this branch is for.
- `resume-feature`: Recover compact task state, latest handoff availability, stable docs, git status, and next-step hints. Use when taking over or continuing a branch.
- `handoff`: Save incomplete work, next step, blockers, touched areas, validation notes, and a concise thread summary.
- `finish-feature`: Finish and archive the active task. Create a PR only if the user explicitly asks and GitHub CLI is already installed and authenticated.
- `project-status`: Return compact project state for a project hub thread or planning discussion.
- `weekly-report`: Generate a human-facing Markdown report under the sidecar `reports/` directory and reply with a short notification, not the full report by default.
- `setup`: Safely create the local sidecar layout for this project.
- `doctor`: Report readiness without installing tools or changing global Codex/GitHub configuration.

## Routing Guide

- Before the first action in a project, resolve the CLI path with the rules above. Prefer `doctor` before `setup` when the project has not used the sidecar before.
- If the user says "start this feature", "track this branch", or gives a feature goal, run `start-feature` with `--goal` and optional `--next-step`.
- If the user says "take over", "resume", "where are we", or "continue this worktree", run `resume-feature`, then summarize only the useful context and next step.
- If the user is ending a session or passing work to another agent, run `handoff` with concrete done/not-done/validation fields.
- If the user says the task is done, run `finish-feature`. Add `--create-pr` only when the user explicitly requests PR creation.
- If the user asks from a project hub thread, use `project-status` for compact status and `weekly-report` for a human update.
- If setup is uncertain, run `doctor` first. Explain any missing optional tools without installing them.

## Backfill Guidance

When initializing an existing project, git history can provide objective facts such as branches, commits, touched files, and changed areas. Git history alone cannot reliably recover intent, design decisions, validation status, blockers, or what should happen next.

For a useful first sidecar state, combine:

- Git facts from `snapshot`, `start-feature`, and recent commits.
- Current thread or user-provided context for goal, current status, next step, blocker, and validation.
- Existing PR descriptions, issue text, or release notes when available.

If semantic context is missing, write a provisional task state and say what is missing rather than pretending the git history is enough.

## Compatibility

The existing `worktree-intake` and `worktree-handoff` skills remain valid compatibility entry points. Prefer this unified skill for V2 lifecycle work, but do not break established V1 prompts.

## Output Style

Return a short conversational summary:

- Current task and status.
- Latest useful next step.
- Handoff or report path when a file was written.
- PR URL when known, or generated PR title/body guidance when GitHub CLI is unavailable.

Avoid pasting long sidecar JSON or full weekly reports unless the user asks for detail.
