---
name: context-handoff
description: Conversation-first project and feature lifecycle state for Codex worktrees using the local context sidecar CLI.
---

# Context Handoff

Use this skill when the user wants to start, resume, hand off, finish, inspect, or report on feature work for the current repository. Keep normal interaction conversational. The Python sidecar CLI is the implementation layer, not the primary user experience.

## Implementation Layer

Use the bundled sidecar CLI in this skill package. Do not ask the user to paste a CLI path during normal use.

Run actions through:

```powershell
python scripts\context_sidecar.py <action> --worktree <current-worktree>
```

If the current working directory is the installed skill directory, use the relative script path above. If running from another directory, resolve `scripts\context_sidecar.py` relative to this `SKILL.md` file and pass the user's current repository or worktree through `--worktree`.

The user should only need to say `Use $context-handoff ...`; CLI path resolution is the agent's responsibility.

The sidecar stays local at:

```text
%USERPROFILE%\.codex\projects\<project-id>\
```

Do not write dynamic task state into tracked repo docs. Do not require MCP for this workflow.

For multi-worktree projects, keep one stable project identity. The CLI resolves projectId in this order: `--project-id`, `CONTEXT_HANDOFF_PROJECT_ID`, existing local sidecar `config.json`, Git remote/common-dir, then repo root name fallback. Use `--project-id` only when the inferred identity would be wrong. Use `--base-branch dev` when the feature base branch is not the inferred default; it persists in sidecar config.

## Actions

- `start-feature`: Create or update the active task for the current branch/worktree. Use when the user starts a new feature or says what this branch is for.
- `resume-feature`: Recover compact task state, latest handoff availability, stable docs, git status, and next-step hints. Use when taking over or continuing a branch.
- `handoff`: Save incomplete work, next step, blockers, touched areas, facts, inferences, unknowns, validation commands/results/time, safety rules, and a concise thread summary.
- `audit-context`: Check whether the current context is trustworthy before handoff/resume. It reports missing handoff, stale HEAD/dirty files, missing validation, missing safety rules, dirty worktree, and backfill prompts.
- `finish-feature`: Finish and archive the active task. Create a PR only if the user explicitly asks and GitHub CLI is already installed and authenticated.
- `project-status`: Return compact project state for a project hub thread or planning discussion.
- `weekly-report`: Generate a human-facing Markdown report under the sidecar `reports/` directory and reply with a short notification, not the full report by default.
- `setup`: Safely create the local sidecar layout for this project.
- `doctor`: Report readiness without installing tools or changing global Codex/GitHub configuration.

## Routing Guide

- Before the first action in a project, run the bundled CLI with the current worktree path. Prefer `doctor` before `setup` when the project has not used the sidecar before.
- If the user says "start this feature", "track this branch", or gives a feature goal, run `start-feature` with `--goal` and optional `--next-step`.
- If the user says "take over", "resume", "where are we", or "continue this worktree", run `resume-feature`, then summarize only the useful context and next step.
- If the user asks to audit trustworthiness, run `audit-context` and summarize findings plus backfill prompts.
- If the user is ending a session or passing work to another agent, run `handoff` with concrete done/not-done fields and explicit `--fact`, `--inference`, `--unknown`, `--safety-rule`, `--validation-command`, `--validation-result`, and `--validation-at` values where known.
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

Handoffs must distinguish:

- Facts: observed git state, user-provided statements, exact validation results.
- Inferences: agent conclusions drawn from facts.
- Unknowns: missing context that should not be guessed.
- Safety rules: constraints for future agents, such as not deleting worktrees and not writing dynamic state into the target repo.

The sidecar records `headSha`, `upstream`, `dirtyFiles`, and `dirtyFingerprint`. Treat `resume-feature` stale output as a warning to re-check current files before trusting an older handoff.

## Output Style

Return a short conversational summary:

- Current task and status.
- Latest useful next step.
- Handoff or report path when a file was written.
- PR URL when known, or generated PR title/body guidance when GitHub CLI is unavailable.

Avoid pasting long sidecar JSON or full weekly reports unless the user asks for detail.
