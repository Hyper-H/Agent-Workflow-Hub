# Worktree Context Reuse v1 Usage

## Installed Paths

- Shared tool:
  `tools/worktree-context-reuse-v1/context_sidecar.py`
- Skill:
  `skills/worktree-intake`
- Skill:
  `skills/worktree-handoff`

## Stable Repo Docs

This repository includes starter templates:

- `docs/agent/project-map.md`
- `docs/agent/conventions.md`
- `docs/agent/common-commands.md`

Fill these with stable, low-frequency repo facts. Do not put task progress or handoff state here.

## Conversation-First Usage

The intended primary interface is conversation through the two skills.

Typical prompts:

- `Use $worktree-intake to recover the current worktree context and tell me the next step.`
- `Use $worktree-handoff to save the current worktree status and prepare the next agent handoff.`
- `Take over this worktree and recover the current context.`
- `Sync the current feature state before I submit the PR.`
- `End this round and leave a clean handoff for the next agent.`
- `Archive the current task, we are done here.`

In the intended workflow, the skills call the sidecar tool in the background. You should not need to run the Python commands manually during normal usage.

## Low-Level Commands

Run from the target worktree directory:

```powershell
python tools\worktree-context-reuse-v1\context_sidecar.py init
python tools\worktree-context-reuse-v1\context_sidecar.py snapshot
python tools\worktree-context-reuse-v1\context_sidecar.py intake
```

Write a handoff manually:

```powershell
python tools\worktree-context-reuse-v1\context_sidecar.py handoff `
  --goal "current goal" `
  --status active `
  --next-step "next concrete step" `
  --thread-summary "2-4 sentence compressed summary"
```

Archive the current task manually after it is done:

```powershell
python tools\worktree-context-reuse-v1\context_sidecar.py archive
```

## Sidecar Location

By default the project sidecar is created at:

```text
%USERPROFILE%\.codex\projects\<project-id>\
```

## Validation Notes

- The shared tool works for `init`, `snapshot`, `intake`, `handoff`, and `archive`.
- The skill directories are structured for local Codex installation or reuse.
- A real temporary git repo smoke test passed for `snapshot -> handoff -> intake -> archive`.
- If git is installed but not discoverable, set `CODEX_GIT_EXE` to the absolute `git.exe` path.

## Known Working Git Path On The Author Machine

```text
D:\install\Git\cmd\git.exe
```
