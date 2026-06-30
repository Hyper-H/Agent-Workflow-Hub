# V3.7.2 Dogfood Smoke Hygiene Design

## Summary

V3.7.2 adds a narrow dogfood/smoke hygiene workflow for Agent Workflow Hub.

The goal is to help the Project Hub identify stale dogfood or smoke-test sidecar records that were superseded by later passing validation, so old blockers do not keep polluting `audit-project`, `visualize-project`, and hub health summaries.

This version deliberately does not implement general sidecar cleanup. It only targets dogfood/smoke records and requires explicit confirmation before archiving anything.

## Problem

Dogfood exposed a real workflow failure mode:

- A dogfood thread tested V3.7.1 before the local source checkout and installed skill were updated.
- That pre-reinstall smoke failed and wrote blocker/handoff state into the local sidecar.
- After updating and reinstalling the skill, the same smoke passed.
- The old failed task state remained in active sidecar records and could still affect Project Hub health and visualization.

The code under test may be correct, but old dogfood records can make the project look unhealthy. The hub needs a safe way to recognize this pattern and suggest archival without erasing history.

## Goals

- Detect stale dogfood/smoke records that have later pass evidence.
- Explain why each record is considered stale.
- Recommend a precise archive command for each candidate.
- Archive only when the user explicitly confirms a specific `taskId`.
- Preserve handoff/archive history.
- Surface hygiene recommendations in hub-facing output.
- Keep dynamic state in the local sidecar, not the target repo.

## Non-Goals

- Do not build general task cleanup.
- Do not archive non-dogfood execution tasks.
- Do not bulk archive by default.
- Do not delete worktrees.
- Do not delete sidecar history.
- Do not migrate the sidecar schema.
- Do not implement UI, MCP, or thread API integration.
- Do not hide true active blockers by automatically lowering health.

## User Experience

The Project Hub or dogfood thread can run:

```text
Use $agent-workflow-hub to check stale dogfood smoke records.
```

The agent runs:

```text
hygiene-dogfood --worktree <repo> --project-id <projectId>
```

The default output is report-only. It lists candidate records, evidence, and suggested archive commands.

To archive one candidate:

```text
hygiene-dogfood --worktree <repo> --project-id <projectId> --confirm-archive --task-id <taskId>
```

The command archives only the named record if it still matches the dogfood/smoke candidate rules and still has pass evidence.

## CLI Interface

Add a new action:

```text
hygiene-dogfood
```

Supported arguments:

```text
--worktree <path>
--project-id <id>
--base-branch <branch>
--language en|zh-CN
--task-id <taskId>
--confirm-archive
```

Default behavior:

- Inspect active sidecar tasks.
- Inspect relevant handoff text when available.
- Return JSON with candidate records and recommended archive commands.
- Do not mutate sidecar state.

Confirmed behavior:

- Require both `--confirm-archive` and `--task-id`.
- Re-run candidate detection for the named task.
- Refuse archive if the task is not a dogfood/smoke hygiene candidate.
- Move the task from active state to archive using the same sidecar archival behavior as `finish-feature`, without touching Git worktrees.
- Preserve handoff paths and write an archive reason.

## Output Shape

Machine JSON keys stay English.

```json
{
  "projectId": "example",
  "sidecarRoot": "/home/user/.codex/projects/example",
  "checkedAt": "2026-06-30T00:00:00Z",
  "candidateRecords": [
    {
      "taskId": "dogfood-v371-role-model-consistency",
      "threadRole": "dogfood",
      "status": "blocked",
      "reason": "stale dogfood blocker superseded by later passing validation",
      "evidence": [
        "task or handoff mentions pre-reinstall failure",
        "later validation result contains PASS"
      ],
      "confidence": "high",
      "recommendedAction": "archive-stale-dogfood-record",
      "archiveCommand": "hygiene-dogfood --confirm-archive --task-id dogfood-v371-role-model-consistency"
    }
  ],
  "nonRecommendedRecords": [
    {
      "taskId": "dogfood-current-failure",
      "reason": "dogfood task still has failure signals but no later pass evidence"
    }
  ],
  "archived": [],
  "requiresConfirmation": true
}
```

When archiving succeeds, `archived` contains the archived task id, archive path, and reason.

## Candidate Detection

A task is a candidate only if all required groups match.

### Dogfood Or Smoke Scope

At least one of:

- `threadRole == "dogfood"`
- `taskId`, `goal`, `threadLabel`, `aliases`, `blocker`, `lastThreadSummary`, or handoff text contains dogfood/smoke terms:
  - `dogfood`
  - `smoke`
  - `pre-reinstall`
  - `stale environment`
  - `role model consistency`
  - `old checksum`
  - `installed skill stale`

### Old Failure Signal

At least one of:

- `status == "blocked"`
- `blocker` is non-empty and mentions failed/stale environment/version mismatch.
- Validation or handoff text mentions failure before reinstall/update.
- Handoff text includes old commit/checksum evidence.

### Later Pass Evidence

At least one of:

- Validation result contains `PASS`, `passed`, `resolved`, `install passed`, or `checksum match`.
- Handoff facts or summary state that the source was updated and installed source checksums match.
- Handoff/inference states that the previous failure was a stale environment issue and not a patch failure.
- A later handoff for the same task records successful smoke after the failed run.

If a record is dogfood/smoke and has failure signals but lacks later pass evidence, the command reports it under `nonRecommendedRecords` and does not suggest archive.

## Archive Semantics

Archival is not deletion.

The archive reason should be:

```text
stale dogfood/smoke record superseded by later passing validation
```

The archive artifact should preserve:

- Original `taskId`
- Previous status
- Previous blocker
- Previous validation
- Previous safety rules
- Handoff path if available
- Hygiene evidence
- Archive timestamp
- Archive action source: `hygiene-dogfood`

The active task should be removed from `active-tasks.json` only after the archive file is written successfully.

## Audit And Visualization Integration

This version lightly integrates with existing hub surfaces.

`audit-project` includes recommended actions for high-confidence stale dogfood records:

```json
{
  "recommendedActionType": "archive-stale-dogfood-record",
  "reason": "stale dogfood blocker superseded by later passing validation",
  "prompt": "Run hygiene-dogfood --confirm-archive --task-id ..."
}
```

`visualize-project` shows the recommendation in row details/action text when a task matches the candidate rules.

Health should not be automatically downgraded or hidden differently in V3.7.2. The goal is transparency and safe action, not automatic suppression.

## Localization

Support `--language en|zh-CN` for human-facing messages, reasons, and prompts.

JSON keys, task ids, status enums, action names, branches, paths, and commit/checksum values remain English/original.

## Skill Documentation

Update both skills:

- `skills/agent-workflow-hub/SKILL.md`
- `skills/context-handoff/SKILL.md`

Add guidance:

- When old dogfood blockers appear to be superseded by later passing smoke, run `hygiene-dogfood`.
- Default action is report-only.
- Archive requires explicit confirmation and a task id.
- Do not use this command for normal execution tasks.

Update README files with the same user-facing behavior:

- `README.md`
- `README.zh-CN.md`

## Safety Rules

- Never archive without `--confirm-archive --task-id`.
- Never archive non-candidate execution tasks.
- Never delete worktrees.
- Never delete archive or handoff files.
- Never write dynamic state into the target repo.
- Never infer pass evidence from absence of recent failures.
- Prefer false negatives over false positives.

## Test Plan

### CLI Smoke

- Create a temp repo and isolated project id.
- Create a dogfood task with old blocker text and a later passing validation/handoff.
- Run `hygiene-dogfood` without confirmation.
- Verify it recommends archive and does not mutate active tasks.
- Run with `--confirm-archive --task-id`.
- Verify active task is archived and no worktree is deleted.

### Negative Cases

- Non-dogfood execution task with blocker is not recommended.
- Dogfood task with current failure and no later pass evidence is not recommended.
- `--confirm-archive` without `--task-id` is rejected.
- `--confirm-archive --task-id` for a non-candidate is rejected.

### Hub Integration

- `audit-project` includes `archive-stale-dogfood-record` recommended action for matching candidates.
- `visualize-project` row/action detail includes the hygiene recommendation.
- Existing `audit-project` and `visualize-project` behavior remains compatible.

### Regression

- Existing lifecycle actions still work.
- Existing `finish-feature` archive behavior remains unchanged.
- Dynamic sidecar state remains under `~/.codex/projects/<project-id>/`.
- `python -m py_compile skills\agent-workflow-hub\scripts\context_sidecar.py skills\agent-workflow-hub\scripts\project_hub_dashboard.py skills\context-handoff\scripts\context_sidecar.py skills\context-handoff\scripts\project_hub_dashboard.py install.py`
- `python install.py --dry-run`
- `git diff --check`
- `python install.py`

## Open Decisions

- Whether to expose `hygiene-dogfood` recommendations in `project-status` is deferred. `audit-project` and `visualize-project` are enough for V3.7.2.
- Bulk archive is deferred. Single-task confirmation is safer.
- General sidecar hygiene is deferred to a later version after dogfood-specific behavior is proven.

## Follow-Up Candidates

- V3.8 Hub Action Workflow: turn hub recommendations into a more general action queue.
- General sidecar hygiene for stale execution tasks.
- Dashboard affordances for acknowledged stale records without changing sidecar schema.
