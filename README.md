# context-handoff

[中文](./README.zh-CN.md) | English

`context-handoff` is a lightweight workflow for reducing context rebuild cost across multi-worktree, multi-thread feature development with stable repo docs, a local sidecar state layer, and intake/handoff skills.

## What It Solves

- New threads repeatedly re-scan the same repository.
- Parallel worktrees and agent threads lose track of current task status.
- Feature or PR handoff is noisy, inconsistent, and expensive.

## Core Idea

Split project context into three layers:

- `docs/agent/`
  Stable repository facts that belong in version control.
- local sidecar
  Dynamic task state that should stay off feature PRs.
- `worktree-intake` / `worktree-handoff`
  Natural-language skill entry points for restoring and saving current task context.

## How You Actually Use It

The intended primary interface is conversation, not manual shell commands.

In practice, usage should look like this:

- `Take over this worktree and tell me where we are.`
- `Continue this feature and recover the current context.`
- `Before I open a PR, sync the current state and write a handoff.`
- `End this round, save the next step, and prepare handoff for another agent.`
- `This task is done, archive the current task state.`

The skills should handle sidecar synchronization in the background. The Python tool is the implementation layer behind the skills, and also serves as a fallback for testing or debugging.

## Repository Layout

```text
docs/
  agent/
    project-map.md
    conventions.md
    common-commands.md
skills/
  worktree-intake/
  worktree-handoff/
tools/
  worktree-context-reuse-v1/
    context_sidecar.py
    templates/
specs/
  multi-worktree-thread-handoff-v1.md
worktree-context-reuse-v1-usage.md
```

## Local Sidecar Layout

By default the tool writes local state to:

```text
%USERPROFILE%\.codex\projects\<project-id>\
  active-tasks.json
  handoffs\
  archive\
  events.jsonl
```

This state is local-only and should not be committed to feature PRs.

## Conversation-First Quick Start

1. Copy or adapt the stable repo docs in `docs/agent/`.
2. Install or copy the two skills into your local Codex skill directory.
3. In a real git worktree, start by speaking to the agent:
   - `Use $worktree-intake to recover the current worktree context and tell me the next step.`
4. Before ending a work session, ask the agent to persist state:
   - `Use $worktree-handoff to save the current worktree status and prepare the next agent handoff.`
5. When the task is done, ask the agent to archive the current task.

## Skill Prompts

Once installed locally, use prompts like:

- `Use $worktree-intake to recover the current worktree context and tell me the next step.`
- `Use $worktree-handoff to save the current worktree status and prepare the next agent handoff.`

Natural-language variants should also work well, for example:

- `Take over this worktree and recover the current context.`
- `Continue this branch and tell me the next step.`
- `Sync the current feature state before I submit the PR.`
- `End this round and leave a clean handoff for the next agent.`
- `Archive the current task, we are done here.`

## Low-Level CLI

The repository also includes a Python CLI for testing, debugging, and non-skill integrations:

```powershell
python tools\worktree-context-reuse-v1\context_sidecar.py init
python tools\worktree-context-reuse-v1\context_sidecar.py snapshot
python tools\worktree-context-reuse-v1\context_sidecar.py intake
python tools\worktree-context-reuse-v1\context_sidecar.py handoff ...
python tools\worktree-context-reuse-v1\context_sidecar.py archive
```

## Validation Status

This repository includes a working v1 implementation that has been validated in:

- a non-git fallback workspace
- a temporary real git repo smoke test for:
  - `snapshot`
  - `handoff`
  - `intake`
  - `archive`

## Notes

- This project intentionally avoids custom MCP in v1.
- The current design prioritizes personal workflow first, then later sharing or evaluation.
- `events.jsonl` is a lightweight evaluation trace, not a full research benchmark.
