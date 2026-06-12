# Agent Workflow Hub

[中文](./README.zh-CN.md) | English

Agent-native development workflow layer for Codex worktrees. Agent Workflow Hub helps Codex coordinate project hubs, execution threads, worktrees, tasks, handoffs, validation, safety rules, and recommended actions through a local sidecar.

Agent Workflow Hub is a workflow state layer, not a replacement for native model memory or context windows. Even as Codex, Claude Code, Cursor, Windsurf, and other agents improve their built-in memory, multi-worktree development still benefits from an explicit, auditable protocol for what task is active, what was validated, what is stale, what is unknown, and which thread should act next. Reduced repeat scanning and lower context rebuild cost are benefits, not the product contract.

The normal interface is conversation:

```text
Use $agent-workflow-hub to resume this worktree.
```

The primary skill bundles its own Python sidecar CLI under `skills/agent-workflow-hub/scripts/`, so users do not need to know where the CLI lives. The compatibility skill under `skills/context-handoff/` uses the same CLI and sidecar data.


## Compatibility

`$agent-workflow-hub` is the default entrypoint from V2.7 onward. `$context-handoff` remains available as a legacy compatibility entrypoint and uses the same local sidecar data, CLI file name, and JSON schema. Existing state under `%USERPROFILE%\.codex\projects\<project-id>\` is not migrated.

## Positioning

### Why This Exists If Agents Already Have Memory/Context

Native agent memory is good at remembering preferences, recent conversations, and broad context. Agent Workflow Hub focuses on explicit project workflow state: task identity, worktree mapping, handoff facts, inferences, unknowns, validation, safety rules, stale detection, and hub-level recommended actions.

### What It Does Not Replace

It does not replace code understanding, tests, PR review, issue tracking, project management tools, or the agent's own investigation. `resume-feature` and `resume-query` restore recorded workflow state; they do not prove correctness.

### Where It Remains Useful As Agents Improve

It remains useful when work spans multiple worktrees, multiple execution threads, multiple agents, or long-running branches where state must be visible, inspectable, and independent of any one chat transcript. The sidecar is auditable project state, not a chat log or model reasoning store.

For the long-form product framing, see [docs/product/workflow-value-positioning.md](./docs/product/workflow-value-positioning.md).

## What It Solves

- New execution threads need explicit task/worktree routing.
- Feature branches, worktrees, and threads lose task status.
- Multi-worktree projects get split into unrelated local project IDs.
- Handoff, finish/archive, audit, and weekly reporting become inconsistent.
- Agents give inconsistent advice about when to use a hub, execution thread, side chat, subagent, or worktree.
- Dynamic agent state leaks into repository docs or feature PRs.

## Install

Clone this repository, then run:

```powershell
python install.py
```

This copies both complete skill packages to:

```text
%USERPROFILE%\.codex\skills\agent-workflow-hub\
%USERPROFILE%\.codex\skills\context-handoff\
```

Restart or refresh Codex if the skill list does not update immediately.

The installer only copies the skill packages. It does not install GitHub CLI, authenticate accounts, or change global Codex configuration.

## Use

In any git project or worktree, ask Codex:

```text
Use $agent-workflow-hub to run doctor/setup for this project.
```

Then use natural prompts:

```text
Use $agent-workflow-hub to start this feature. Goal: improve the dashboard UI.
```

```text
Use $agent-workflow-hub to resume this worktree and tell me the immediate next step.
```

```text
Use $agent-workflow-hub to continue markerless clean.
```

```text
Use $agent-workflow-hub to act as the markerless execution thread.
```

```text
Use $agent-workflow-hub to save a handoff before I stop today.
```

```text
Use $agent-workflow-hub to audit this context before another agent takes over.
```

```text
Use $agent-workflow-hub to audit this project hub across all worktrees.
```

```text
Use $agent-workflow-hub to draft a dogfood issue for this problem.
```

```text
Use $agent-workflow-hub to finish this feature and generate PR text.
```

```text
Use $agent-workflow-hub to generate this week's eval report.
```

## Multi-Thread Workflow Playbook

V2.5 treats threads as workflow roles and the sidecar as their shared state layer. This is documentation and agent guidance only: it does not add CLI actions, change the sidecar schema, or require UI/MCP support.

Default topology:

- One project has one Project Hub Thread for project-wide status, routing, worktree inventory, and periodic `audit-project` / `weekly-report` summaries.
- One active worktree/task has one Primary Execution Thread for implementation, validation, handoff, finish/archive, and PR text.
- Create a new worktree when the task needs an isolated branch, parallel implementation, or a different base. Reuse the existing worktree when continuing the same task or doing tiny scratch work.
- Repo-bound fuzzy tasks can start directly in an execution thread, plan there first, then implement.
- Product-direction fuzzy tasks stay in the hub or a short-lived Discussion Thread until they become actionable.
- Side chats are for short questions, scratch wording, and throwaway drafts; copy only durable decisions back to the hub or execution thread.
- Subagents are temporary helpers for review, investigation, comparison, or validation; they report findings back and do not own long-running tasks.
- Explainer Threads handle deep project explanation or onboarding so the hub does not become a tutorial transcript.
- Dogfood/QA Threads capture real-project test feedback, reproduction notes, and issue drafts.
- `sidecar`, `handoff`, and `audit-project` are the shared state layer between threads.

Routing guidance:

- Use or create the Project Hub Thread when the user asks "where are we across the project?", wants all worktrees, or needs task routing.
- Use or create a Primary Execution Thread when the user asks to build, fix, refactor, validate, or finish one branch/worktree task.
- Recommend a new worktree only when isolation, parallel work, or a separate branch/base is useful; otherwise continue in the current worktree.
- If the task is fuzzy but clearly belongs to one repo/worktree, open the execution thread and plan inside it.
- If the task is still about product direction, priority, or whether the idea should exist, keep it in the hub or a Discussion Thread.
- Use a side chat for small non-durable questions.
- Use a subagent for bounded research/review/validation with a narrow return-finding prompt.
- Use an Explainer Thread for architecture/history/onboarding explanations.
- Use a Dogfood/QA Thread for dogfood feedback and prefer `draft-issue` unless the user explicitly asks to create an issue.

State rules:

- The hub owns the map, inventory, routing decisions, and compact summaries; it should not own every implementation detail.
- Execution threads update sidecar with `start-feature`, `resume-feature`, `handoff`, `audit-context`, and `finish-feature` as appropriate.
- Results from discussion, side chat, explainer, dogfood, and subagent threads become durable only when copied into the hub, the relevant execution thread, or sidecar handoff/audit output.
- Never treat `project-status` as the full project inventory; use `audit-project` for hub-level status.

Recommended prompt templates:

New execution thread:

```text
You are the Primary Execution Thread for <project>/<task>. Repo/worktree: <path>. Use $agent-workflow-hub first: run resume-feature if a task already exists, otherwise start-feature with this goal: <goal>. Plan briefly inside this thread, then implement. Keep dynamic state in sidecar/handoffs, not tracked repo docs. Before stopping, run the relevant validation, audit-context if useful, and save a handoff with facts, inferences, unknowns, safety rules, validation, blockers, and next step.
```

Execution thread completion handoff:

```text
Task complete for <project>/<task>. Please update $agent-workflow-hub: run audit-context, then finish-feature or handoff as appropriate. Report back to the Project Hub with: branch, worktree, summary of changes, validation commands/results, PR URL or generated PR title/body, remaining risks, sidecar handoff/archive path, and whether the worktree is clean.
```

Dogfood feedback:

```text
This is a Dogfood/QA Thread for <project>. Feedback: <observed behavior>. Expected: <expected behavior>. Repo/worktree if known: <path>. Use $agent-workflow-hub to draft a dogfood issue. Keep Facts, Inferences, Unknowns, Reproduction, Suggested Fix, and Priority separate. Do not create a GitHub issue unless I explicitly ask or dogfood issue mode is enabled.
```

Project hub migration:

```text
You are the Project Hub Thread for <project>. Canonical repo/worktree: <path>. Use $agent-workflow-hub to run audit-project with the expected project id/base branch. Build the hub view from real git worktrees plus sidecar active tasks. Summarize active execution threads, missing sidecar coverage, stale handoffs, validation gaps, and concrete backfill prompts. Do not treat project-status as the full inventory.
```

Explainer thread:

```text
You are an Explainer Thread for <project>. Repo/worktree: <path>. Explain <topic> for onboarding. Use stable repo docs and current code. Keep the hub clean: produce a concise explanation, glossary, key files, and open questions, then tell the hub only the durable takeaways or docs that should be updated.
```

## Human-Facing Localization

Machine JSON keys, CLI action names, status enums, event names, paths, branch names, and Git output stay in English/original form. Human-facing Markdown and summary text can be English or Simplified Chinese.

Default output is English. For one command, agents can pass `--language zh-CN` or `--language en` to actions that produce human-readable text, including `handoff`, `resume-feature`, `audit-context`, `audit-project`, `weekly-report`, `draft-issue`, and `create-issue`.

To persist a local preference in sidecar config:

```text
Use $agent-workflow-hub to set human-facing output language to zh-CN.
```

This writes `preferredLanguage` only under `%USERPROFILE%\.codex\projects\<project-id>\config.json` and does not mutate the target repository.

## Natural-Language Routing

V2.8 adds deterministic task routing for project hubs and execution threads. When the user says something like `continue markerless clean`, `take over markerless`, `act as the markerless execution thread`, or Chinese phrases like `接手 markerless`, agents should use `resume-query --query "markerless"` or `resolve-task --query "markerless"` with a known project/worktree path.

Use `resume-feature` only when the user explicitly means the current Git worktree, such as `resume this worktree` or `继续当前 worktree`.

This routing layer is sidecar-first, git-aware, and scan-minimal. It restores the last recorded workflow state for the resolved task; it does not prove code correctness, replace tests, or replace PR review. Agents still choose their own investigation strategy and may use sidecar state, handoffs, Git facts, touched files, recent commits, PRs, issues, tests, or targeted search as needed.

Resolution uses local deterministic matching only: normalized strings, token overlap, and `difflib`. It does not use an LLM, embeddings, a vector database, UI, MCP, or any thread API.

Task aliases are supported:

- `start-feature --alias "markerless clean"` and `handoff --alias "markerless clean"` persist user-confirmed aliases on the task.
- `alias-task --alias "markerless clean"` adds an alias to the current or selected task.
- `alias-task --remove-alias "markerless clean"` removes an alias.
- Generated aliases from branch, task id, worktree name, goal, touched areas, and handoff summary participate in matching but are not persisted.

`resolve-task` returns short JSON with `resolved`, `confidence`, `taskId`, `branch`, `worktreePath`, `matchedFields`, `candidates`, and `disambiguationQuestion`. High-confidence matches can be resumed automatically by `resume-query`; low-confidence or close candidates return one question instead of guessing.

Project discovery records `canonicalRepoRoot`, `projectContainerRoots`, and `knownWorktreeRoots` in local sidecar config. This lets a hub thread route from a non-Git container directory to a known project when there is a single clear match. If multiple projects match, the CLI returns candidates and asks for disambiguation.

`start-feature` and `handoff` are guarded on non-Git paths. By default they refuse to create or update sidecar task state from a container directory and return guidance to use `resume-query` or a real worktree path. Use `--allow-non-git-worktree` only when the user explicitly wants to record a non-Git directory.

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
- `alias-task`: Add or remove human-friendly task aliases.
- `resolve-task`: Resolve a natural-language query to a sidecar task without resuming.
- `resume-feature`: Recover compact context, stale detection, and a `startThreadSummary`.
- `resume-query`: Resolve a natural-language query, then run sidecar-first resume on the matched worktree when confidence is high.
- `handoff`: Save incomplete work, next step, facts, inferences, unknowns, validation, and safety rules.
- `audit-context`: Report missing handoff, stale git state, missing validation, missing safety rules, dirty worktree, and backfill prompts.
- `audit-project`: Audit all Git worktrees for a project hub inventory, compare real worktrees with sidecar active tasks, and generate branch-level backfill prompts, recommended actions, execution-thread prompts, and cleanup prompts.
- `finish-feature`: Archive the task and generate PR title/body; create a PR only when explicitly requested and GitHub CLI is ready.
- `project-status`: Summarize compact sidecar project state. It is not the full Git worktree inventory.
- `weekly-report`: Write a human-facing Markdown report under the sidecar `reports/` directory.
- `eval-report`: Write lightweight workflow evaluation Markdown and JSON reports under `reports/`. This reports proxy workflow metrics, not exact token savings or proof of correctness.
- `visualize-project`: Write a Markdown + Mermaid project graph, companion JSON, and static HTML dashboard under `reports/`. Use when the user asks to visualize the project or show the project graph.
- `draft-issue`: Generate a dogfood/debug issue draft without requiring GitHub CLI.
- `create-issue`: Create a dogfood/debug issue only when explicitly requested, safe, authenticated, and not likely duplicated.
- `enable-dogfood-issue-mode` / `disable-dogfood-issue-mode`: Persist local sidecar permission for dogfood issue creation.
- `set-language`: Persist local sidecar language preference for human-facing output.
- `snapshot`: Print current worktree Git facts for lightweight backfill.

V1 `worktree-intake` and `worktree-handoff` have been merged into Agent Workflow Hub as `resume-feature` and `handoff`. The old `$context-handoff` entrypoint remains a compatibility alias.

## Project Hub Inventory

`project-status` reports sidecar-known active tasks. It does not enumerate every Git worktree. For project hub threads or multi-worktree status, use:

```text
Use $agent-workflow-hub to audit this project hub across all worktrees. Project id: my_project. Base branch: dev.
```

The skill runs `audit-project`, which uses `git worktree list --porcelain`, audits every worktree, and returns:

- Total Git worktrees versus sidecar active tasks.
- Tracked and untracked worktrees.
- Dirty, stale, missing handoff, missing validation, and missing safety-rule worktrees.
- Sidecar tasks whose recorded worktree no longer exists.
- Backfill prompts grouped by branch/worktree.
- Recommended actions with copyable old-thread and new execution-thread prompts.
- Cleanup prompts for sidecar tasks whose recorded worktree no longer exists.

Rows with `sidecarHit: false` use `taskStatus: "missing"` because no real sidecar task exists. They may include `provisionalTaskStatus` from the audit-only default task; `taskStatus` always reflects sidecar state.

If a requested project id is normalized, such as `paus_robot_lab_host` becoming `paus-robot-lab-host`, the output reports that canonicalization explicitly.

When an old execution thread exists, send it `oldThreadBackfillPrompt` first because it may have semantic context Git cannot recover. If no old execution thread exists, open a new Primary Execution Thread with `newExecutionThreadPrompt`. That thread must recover or initialize sidecar state, distinguish facts/inferences/unknowns, add validation/safety/nextStep, save a handoff, and report back to the Project Hub.

These prompts standardize the collaboration artifact; they do not micromanage the agent's investigation path. Agents may use sidecar state, handoff Markdown, Git facts, touched files, recent commits, PRs, issues, tests, or targeted search as needed.

## Project Visualization

When the user says `visualize project`, `show project graph`, `可视化项目`, `显示项目图`, `项目关系图`, or asks to see the global project map, use:

```text
Use $agent-workflow-hub to visualize this project.
```

The skill runs `visualize-project`, writes Markdown, JSON, and static HTML dashboard reports under the local sidecar `reports/` directory, and replies with the Mermaid graph, Legend, details table, needs-attention summary, and report paths instead of the full JSON by default. The HTML path is generated by default but is not opened automatically.

The default graph shows the main relationship chain `Project -> Task -> Worktree -> Thread Role`. The HTML dashboard keeps Project as page context, uses a route spotlight interaction for task/worktree/thread nodes, keeps dependencies and `th-project-hub` audit/routing outside the ownership graph, and puts risk/nextStep/validation/handoff in the detail panel instead of drawing them as graph nodes. Health is represented through text badges and visual classes. Archived tasks are hidden by default and summarized as `Archived hidden: N`; pass `--include-archive` only when archived context should be shown.

## Trustworthy Handoffs

Git history can recover objective facts such as branches, commits, and touched files. It cannot reliably recover intent, design decisions, blockers, validation status, or the correct next step.

`touchedFiles` means current Git dirty/touched files. It is one locator signal when context is thin, not an instruction to inspect touched files first or perform a full scan.

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

`events.jsonl` records lightweight lifecycle events for future evaluation. It is not a full benchmark by itself. See [docs/research/agent-workflow-hub-v2-benchmark.md](./docs/research/context-handoff-v2-benchmark.md) for the planned comparison between no shared context, stable repo docs only, and sidecar + handoff.

`weekly-report` is for project progress. `eval-report` is for Agent Workflow Hub effectiveness: usage counts, recovery health, routing health, coverage, and proxy efficiency metrics. It deliberately avoids exact token-saving claims.
