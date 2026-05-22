Read and execute below with ultrathink

## Goal Tracker Setup (REQUIRED FIRST STEP)

Before starting implementation, you MUST initialize the Goal Tracker:

1. Read @/c/Users/Administrator/Documents/context-handoff/.humanize/rlcr/2026-05-22_21-50-19/goal-tracker.md
2. If the "Ultimate Goal" section says "[To be extracted...]", extract a clear goal statement from the plan
3. If the "Acceptance Criteria" section says "[To be defined...]", define 3-7 specific, testable criteria
4. Populate the "Active Tasks" table with tasks from the plan, mapping each to an AC and filling Tag/Owner
5. Write the updated goal-tracker.md

**IMPORTANT**: The IMMUTABLE SECTION can only be modified in Round 0. After this round, it becomes read-only.

---

## Implementation Plan

For all tasks that need to be completed, please use the Task system (TaskCreate, TaskUpdate, TaskList) to track each item in order of importance.
You are strictly prohibited from only addressing the most important issues - you MUST create Tasks for ALL discovered issues and attempt to resolve each one.

## Task Tag Routing (MUST FOLLOW)

Each task must have one routing tag from the plan: `coding` or `analyze`.

- Tag `coding`: Claude executes the task directly.
- Tag `analyze`: Claude must execute via `/humanize:ask-codex`, then integrate Codex output.
- Keep Goal Tracker "Active Tasks" columns **Tag** and **Owner** aligned with execution (`coding -> claude`, `analyze -> codex`).
- If a task has no explicit tag, default to `coding` (Claude executes directly).

# Context Handoff V2 Lifecycle Plan

## Goal Description

Upgrade `context-handoff` from a v1 worktree handoff prototype into a shareable MVP for AI-assisted feature lifecycle state management.

The V2 product should let a user interact conversationally through one primary skill while the implementation persists compact project/task state in a local sidecar. The user should be able to start a feature, resume a feature, write an incomplete-work handoff, finish/archive a feature, inspect project status from a project hub thread, and generate weekly human-facing reports without committing dynamic state into the repository.

The implementation must keep MCP out of scope for V2. The sidecar schema and CLI should remain simple enough to be wrapped by MCP later, but V2 success is measured by a working skill + CLI + sidecar workflow.

## Acceptance Criteria

- AC-1: Unified conversation-first skill exists.
  - Positive Tests (expected to PASS):
    - A `skills/context-handoff/SKILL.md` file exists and documents the actions `start-feature`, `resume-feature`, `handoff`, `finish-feature`, `project-status`, `weekly-report`, `setup`, and `doctor`.
    - The skill tells the agent to use the sidecar CLI as the implementation layer and to keep normal usage conversational.
    - The existing `worktree-intake` and `worktree-handoff` skills remain usable for compatibility.
  - Negative Tests (expected to FAIL):
    - The V2 README tells users to primarily run raw Python commands during normal usage.
    - The new skill requires MCP to work.

- AC-2: Sidecar supports V2 project lifecycle state.
  - Positive Tests (expected to PASS):
    - The sidecar layout includes `active-tasks.json`, `project-state.json`, `handoffs/`, `archive/`, `reports/`, and `events.jsonl`.
    - `active-tasks.json` still tracks only active-like tasks.
    - `project-state.json` stores compact machine-readable project status for agents.
    - Weekly reports are Markdown files under the sidecar `reports/` directory and are not written into the repository.
  - Negative Tests (expected to FAIL):
    - Dynamic task state is written under repo-tracked docs.
    - Weekly report text is mixed into `project-state.json` as long narrative history.

- AC-3: CLI supports lifecycle actions.
  - Positive Tests (expected to PASS):
    - `context_sidecar.py start-feature` creates or updates a task record for the current branch/worktree.
    - `context_sidecar.py resume-feature` resolves the current task and returns compact JSON suitable for skill output.
    - `context_sidecar.py handoff` still updates the latest incomplete-work handoff.
    - `context_sidecar.py finish-feature` archives the task, removes it from active tasks, updates project state, and returns PR-related output.
    - `context_sidecar.py project-status` returns compact project status.
    - `context_sidecar.py weekly-report` writes a Markdown report into sidecar reports.
    - `context_sidecar.py doctor` reports environment readiness without mutating global system state.
  - Negative Tests (expected to FAIL):
    - `finish-feature` fails only because GitHub CLI is absent.
    - `doctor` silently installs GitHub CLI or modifies Codex configuration without explicit user consent.

- AC-4: PR creation follows the hybrid strategy.
  - Positive Tests (expected to PASS):
    - If `gh` is installed and authenticated, `finish-feature` can create a PR when explicitly requested.
    - If `gh` is absent or unauthenticated, `finish-feature` generates PR title/body text, updates sidecar state, and reports setup guidance instead of failing.
    - `prUrl` is recorded when known and left empty when unavailable.
  - Negative Tests (expected to FAIL):
    - The default finish flow silently installs `gh`.
    - The task cannot be finished or archived when no PR URL exists.

- AC-5: Project hub and weekly report behavior is documented and usable.
  - Positive Tests (expected to PASS):
    - README describes the `project hub thread` as a long-lived thread for project status, planning, and short weekly report notifications.
    - Weekly report output is human-facing Markdown in sidecar.
    - Automation setup instructions bind weekly report notifications to the current project hub thread.
    - The thread notification is short and does not paste the full report by default.
  - Negative Tests (expected to FAIL):
    - Weekly reports are positioned as the primary context input for agents.
    - Automation is required for manual `weekly-report` to work.

- AC-6: Telemetry and research scaffold exist without making the workflow heavy.
  - Positive Tests (expected to PASS):
    - `events.jsonl` records lifecycle events such as `start`, `resume`, `handoff`, `finish`, `project-status`, and `weekly-report`.
    - Events include objective fields such as timestamp, projectId, taskId when available, sidecar hit, handoff availability, scan scope, and duration where practical.
    - A research or benchmark note describes future comparisons among no shared context, stable repo docs only, and sidecar + handoff.
  - Negative Tests (expected to FAIL):
    - The normal workflow requires manual subjective scoring after every action.
    - Token measurement is treated as mandatory when no token API is available.

- AC-7: Documentation supports a shareable MVP.
  - Positive Tests (expected to PASS):
    - README and Chinese README explain the V2 positioning as a lightweight project/task state layer.
    - Documentation includes conversation-first examples for start, resume, finish, project status, and weekly report.
    - Documentation clearly says dynamic sidecar state stays local and out of feature PRs.
    - Setup/doctor guidance is understandable for another developer cloning the repo.
  - Negative Tests (expected to FAIL):
    - The docs present V2 as only a handoff template.
    - The docs imply users must use MCP in V2.

## Path Boundaries

### Upper Bound (Maximum Scope)

The implementation may add a new unified skill, expand the existing Python sidecar CLI, add sidecar schema helpers, add Markdown templates for weekly reports, add doctor/setup commands, update README files, and add lightweight research notes.

The implementation may support GitHub CLI detection and PR creation when explicitly requested and when `gh` is already installed and authenticated.

### Lower Bound (Minimum Scope)

The implementation must at least deliver the unified skill, V2 lifecycle CLI commands, sidecar `project-state.json`, sidecar `reports/*.md`, hybrid PR fallback behavior, project-status output, weekly-report generation, doctor checks, and updated README usage.

### Allowed Choices

- Can use Python standard library only unless there is a strong reason to add a dependency.
- Can keep the existing `tools/worktree-context-reuse-v1/context_sidecar.py` path for compatibility, even if it gains V2 commands.
- Can add templates or reference files under `skills/context-handoff/`.
- Can keep V1 skill directories and documentation as compatibility material.
- Cannot implement a custom MCP service in V2.
- Cannot write dynamic sidecar state into repo-tracked `docs/agent/`.
- Cannot silently install external tools or modify global Codex settings.
- Cannot make automation mandatory for core workflows.

## Dependencies and Sequence

### Milestones

1. Expand sidecar data model and CLI lifecycle commands.
   - Add sidecar paths for `project-state.json` and `reports/`.
   - Add lifecycle command handlers.
   - Preserve existing `init`, `snapshot`, `intake`, `handoff`, and `archive` behavior or provide compatibility aliases.
   - Add event logging for new lifecycle events.

2. Add project status and weekly report generation.
   - Implement compact project status JSON output.
   - Implement Markdown weekly report generation from sidecar state.
   - Keep reports in local sidecar only.

3. Add PR hybrid behavior.
   - Detect `gh`.
   - Detect authentication status when practical.
   - Create PR only when explicitly requested and possible.
   - Otherwise generate PR title/body and continue finish/archive flow.

4. Add setup and doctor support.
   - Implement non-mutating doctor checks.
   - Implement explicit setup guidance or safe initialization behavior.
   - Do not silently install external tools.

5. Add unified skill and update docs.
   - Add `skills/context-handoff/SKILL.md`.
   - Document action routing, fallback behavior, and output expectations.
   - Update English and Chinese README with conversation-first V2 usage.
   - Describe project hub thread and weekly report automation.

6. Validate and review.
   - Run Python CLI smoke tests in a temporary git repository.
   - Test missing `gh` fallback.
   - Test sidecar output does not enter the repository.
   - Run Codex review through the Humanize RLCR review phase.
   - After RLCR passes, run one independent final Codex review with `gpt-5.5` and `xhigh` reasoning against `main`.

## Implementation Notes

- Prefer small helper functions over adding a new framework.
- Keep sidecar JSON compact and deterministic.
- Keep long human-facing narrative in Markdown reports and handoffs, not in `project-state.json`.
- For action names, use hyphenated CLI subcommands and natural-language skill routing.
- If existing V1 files contain garbled Chinese text due encoding, avoid making that worse; use UTF-8 writes.
- Do not introduce implementation code comments that mention AC numbers or Humanize plan terminology.
- Use `gpt-5.5:high` for the Humanize RLCR loop. Do not run the entire loop at `xhigh`.
- Use `gpt-5.5:xhigh` only for the final independent review after RLCR has completed.

---

## BitLesson Selection (REQUIRED FOR EACH TASK)

Before executing each task or sub-task, you MUST:

1. Read @/c/Users/Administrator/Documents/context-handoff/.humanize/bitlesson.md
2. Run `bitlesson-selector` for each task/sub-task to select relevant lesson IDs
3. Follow the selected lesson IDs (or `NONE`) during implementation

Include a `## BitLesson Delta` section in your summary with:
- Action: none|add|update
- Lesson ID(s): NONE or comma-separated IDs
- Notes: what changed and why (required if action is add or update)

Reference: @/c/Users/Administrator/Documents/context-handoff/.humanize/bitlesson.md

---

## Goal Tracker Rules

Throughout your work, you MUST maintain the Goal Tracker:

1. **Before starting a task**: Mark it as "in_progress" in Active Tasks
   - Confirm Tag/Owner routing is correct before execution
2. **After completing a task**: Move it to "Completed and Verified" with evidence (but mark as "pending verification")
3. **If you discover the plan has errors**:
   - Do NOT silently change direction
   - Add entry to "Plan Evolution Log" with justification
   - Explain how the change still serves the Ultimate Goal
4. **If you need to defer a task**:
   - Move it to "Explicitly Deferred" section
   - Provide strong justification
   - Explain impact on Acceptance Criteria
5. **If you discover new issues**: Add to "Open Issues" table

---

Note: You MUST NOT try to exit `start-rlcr-loop` loop by lying or edit loop state file or try to execute `cancel-rlcr-loop`

After completing the work, please:
0. If you have access to the `code-simplifier` agent, use it to review and optimize the code you just wrote
1. Finalize @/c/Users/Administrator/Documents/context-handoff/.humanize/rlcr/2026-05-22_21-50-19/goal-tracker.md (this is Round 0, so you are initializing it - see "Goal Tracker Setup" above)
2. Commit your changes with a descriptive commit message
3. Write your work summary into @/c/Users/Administrator/Documents/context-handoff/.humanize/rlcr/2026-05-22_21-50-19/round-0-summary.md
