# context-handoff

[中文](./README.zh-CN.md) | English

`context-handoff` is a self-contained Codex skill for AI-assisted feature lifecycle state. It helps agents resume work across branches, worktrees, and threads without repeatedly rebuilding the same project context.

The normal interface is conversation:

```text
Use $context-handoff to resume this worktree.
```

The skill bundles its own Python sidecar CLI under `skills/context-handoff/scripts/`, so users do not need to know where the CLI lives.

## What It Solves

- New agent threads repeatedly scan the same repository.
- Feature branches, worktrees, and threads lose task status.
- Multi-worktree projects get split into unrelated local project IDs.
- Handoff, finish/archive, audit, and weekly reporting become inconsistent.
- Dynamic agent state leaks into repository docs or feature PRs.

## Install

Clone this repository, then run:

```powershell
python install.py
```

This copies the complete skill package to:

```text
%USERPROFILE%\.codex\skills\context-handoff\
```

Restart or refresh Codex if the skill list does not update immediately.

The installer only copies the skill package. It does not install GitHub CLI, authenticate accounts, or change global Codex configuration.

## Use

In any git project or worktree, ask Codex:

```text
Use $context-handoff to run doctor/setup for this project.
```

Then use natural prompts:

```text
Use $context-handoff to start this feature. Goal: improve the dashboard UI.
```

```text
Use $context-handoff to resume this worktree and tell me the immediate next step.
```

```text
Use $context-handoff to save a handoff before I stop today.
```

```text
Use $context-handoff to audit this context before another agent takes over.
```

```text
Use $context-handoff to draft a dogfood issue for this problem.
```

```text
Use $context-handoff to finish this feature and generate PR text.
```

## Sidecar State

Dynamic state is local-only and stays outside your repository:

```text
%USERPROFILE%\.codex\projects\<project-id>\
  config.json
  active-tasks.json
  project-state.json
  handoffs\
  archive\
  reports\
  events.jsonl
```

`project-state.json` is compact machine-readable status for agents. Handoffs and weekly reports are Markdown for humans. Stable repository facts can still live in tracked `docs/agent/` files.

Project identity is stable across multiple worktrees. Resolution order is:

- `--project-id`
- `CONTEXT_HANDOFF_PROJECT_ID`
- existing local sidecar `config.json`
- Git remote URL or common Git directory
- repository root name fallback

Base branch can be overridden with `--base-branch dev`; the value is persisted in local sidecar config and reused by later actions.

## Main Actions

- `doctor`: Check Python, Git, sidecar, and optional GitHub CLI readiness.
- `setup`: Create the local sidecar layout.
- `start-feature`: Track the current branch/worktree as an active task.
- `resume-feature`: Recover compact context, stale detection, and a `startThreadSummary`.
- `handoff`: Save incomplete work, next step, facts, inferences, unknowns, validation, and safety rules.
- `audit-context`: Report missing handoff, stale git state, missing validation, missing safety rules, dirty worktree, and backfill prompts.
- `finish-feature`: Archive the task and generate PR title/body; create a PR only when explicitly requested and GitHub CLI is ready.
- `project-status`: Summarize current project state for a project hub thread.
- `weekly-report`: Write a human-facing Markdown report under the sidecar `reports/` directory.
- `draft-issue`: Generate a dogfood/debug issue draft without requiring GitHub CLI.
- `create-issue`: Create a dogfood/debug issue only when explicitly requested, safe, authenticated, and not likely duplicated.
- `enable-dogfood-issue-mode` / `disable-dogfood-issue-mode`: Persist local sidecar permission for dogfood issue creation.

V1 `worktree-intake` and `worktree-handoff` have been merged into the unified `context-handoff` skill as `resume-feature` and `handoff`.

## Trustworthy Handoffs

Git history can recover objective facts such as branches, commits, and touched files. It cannot reliably recover intent, design decisions, blockers, validation status, or the correct next step.

V2.2 handoffs deliberately separate:

- `facts`: observed or user-provided facts.
- `inferences`: agent conclusions that should remain inspectable.
- `unknowns`: missing context that should not be guessed.
- `safetyRules`: first-class constraints for later agents.
- `validation`: command(s), result(s), notes, and validation time.

The sidecar also records `headSha`, `upstream`, `dirtyFiles`, and `dirtyFingerprint`. `resume-feature` and `audit-context` flag stale context when HEAD or dirty files differ from the recorded task snapshot.

## GitHub PR Behavior

GitHub CLI is optional. `finish-feature` always works without a PR URL. If `gh` is installed and authenticated, the skill can create a PR when the user explicitly asks. Otherwise it generates PR title/body text and records local completion state.

Any non-zero `gh auth status` result, traceback, `TypeError`, or exception-like output is treated as unauthenticated.

## Dogfood Issue Mode

Dogfood issue reporting is draft-only by default. Agents may generate a copyable issue draft with `draft-issue` without GitHub CLI. Issue bodies always separate:

- Facts
- Inferences
- Unknowns
- Reproduction
- Suggested Fix
- Priority

Automatic issue creation is allowed only when the user explicitly asks to create an issue or enables dogfood issue mode for the local sidecar project. Created issues get `agent-reported` and `needs-triage` labels. Before creating, the CLI checks `gh auth status`, searches similar open issues, and blocks creation when sensitive content, tokens, private paths, or oversized logs are detected. In blocked or unauthenticated cases it returns the title/body draft instead.

## Research Notes

`events.jsonl` records lightweight lifecycle events for future evaluation. It is not a full benchmark by itself. See [docs/research/context-handoff-v2-benchmark.md](./docs/research/context-handoff-v2-benchmark.md) for the planned comparison between no shared context, stable repo docs only, and sidecar + handoff.
