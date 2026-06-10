# Skill Maintenance

Canonical source repo:

```text
https://github.com/Hyper-H/Agent-Workflow-Hub.git
```

Installed skill paths:

```text
%USERPROFILE%\.codex\skills\agent-workflow-hub\
%USERPROFILE%\.codex\skills\context-handoff\
```

The installed skill directories are deployment copies. Do not treat them as the canonical source checkout and do not make lasting fixes there first.

## Update Protocol

1. Locate or clone the canonical source repo.
2. Check the source checkout with `git status --short --branch`.
3. Do not overwrite unrelated user changes. If the worktree is dirty, inspect the changed files and preserve user edits.
4. Make changes in the source checkout.
5. Validate:

```powershell
python -m py_compile skills\agent-workflow-hub\scripts\context_sidecar.py skills\context-handoff\scripts\context_sidecar.py install.py
python install.py --dry-run
git diff --check
```

6. Install from the source checkout:

```powershell
python install.py
```

7. Confirm both installed skill packages contain `SKILL.md`, `scripts\context_sidecar.py`, and `references\maintenance.md`.

## Repair Notes

- `$agent-workflow-hub` is the primary entrypoint.
- `$context-handoff` is the compatibility entrypoint and should stay behavior-compatible.
- Dynamic sidecar state belongs under `%USERPROFILE%\.codex\projects\<project-id>\`, not in the target repository.
- Historical bad sidecar records should be reported, not automatically deleted or rewritten.
