# Thread Role Charters

[中文](./thread-role-charters.zh-CN.md) | English

Thread role charters describe how Agent Workflow Hub threads coordinate. They are not capability limits for an agent.

## What This Is

A thread role is a coordination position in the AWH workflow. It helps an agent answer:

- What project state should I treat as orientation?
- What durable outcome should survive this thread?
- Where should I report results?
- When should I hand work to another role?

The charter does not tell an agent how smart it is, which reasoning strategy it must use, or how much context it is allowed to read.

## Why This Exists

AWH already has sidecar state, handoffs, project hub inventory, and natural-language routing. The missing piece is a small shared protocol for role-specific behavior.

Without a charter, agents can overfit to old handoffs, treat hypotheses as facts, let hub threads absorb implementation details, or turn review/validation threads into long-running owners. With an overly strict charter, agents may become less capable because the documentation acts like a second prompt. This design chooses the middle path: enough coordination semantics to keep the project coherent, without constraining agent judgment.

## Design Rationale

The charter is low-anchor by design:

- It defines workflow participation, not agent capability.
- It treats sidecar and handoff state as routing and continuity signals, not proof.
- It preserves uncertainty instead of promoting old hypotheses into facts.
- It keeps dynamic state in sidecar/handoffs, not tracked repo docs.
- It uses existing handoff fields first instead of adding schema fields before the practice is proven.

The agent-facing charter is English-only and lives inside the installed skill package. Human-facing docs are bilingual because users should be able to understand the workflow design and demos without reading implementation instructions.

## How Agents Use The Charter

Agent Workflow Hub is a skill-first workflow. The path is:

```text
User invokes $agent-workflow-hub
-> agent reads SKILL.md
-> SKILL.md points role-specific work to references/thread-role-charters.md
-> agent reads the compact English charter
-> agent runs orient-thread / resume-query / handoff as appropriate
```

The CLI does not automatically read the charter. The sidecar does not store charter content. The charter is guidance for the agent after it reads `SKILL.md`.

## Demo

User opens a project-level Discussion Thread:

```text
Use $agent-workflow-hub first. If only $context-handoff is available, use it as the compatible entrypoint.
You are a Discussion Thread for Agent Workflow Hub. threadRole: discussion. Scope: project-level.
Topic: Design a low-anchor Thread Role Charter system.
```

Agent behavior:

1. Read `SKILL.md`.
2. Read `references/thread-role-charters.md` because the user started a role-specific thread.
3. Run `orient-thread --role discussion --scope project-level --query "<topic>"`.
4. Treat related task matches as context, not as a confirmed feature binding.
5. Shape direction, alternatives, unknowns, and execution target recommendation.
6. Save a low-anchor handoff with facts, hypotheses, open alternatives, unknowns, risks, and next step when useful.

The important point is not that the agent follows a rigid template. The important point is that it does not inherit old project state as truth and does not silently become an execution thread.

## Role Overview

### hub

Coordination purpose: maintain the project map, worktree inventory, routing decisions, prioritization, summaries, reports, and compact receipts.

Project state use: prefer `audit-project`, project status, receipts, and recommended actions over full handoff loading. Treat sidecar active tasks as one state source, not the full worktree inventory.

Durable output: project status, route recommendations, cleanup/backfill prompts, and compact summaries from other threads.

Boundary: do not own feature implementation details.

### discussion

Coordination purpose: shape product, architecture, workflow, or implementation direction before execution.

Project state use: use AWH state to orient and route, not to inherit conclusions. Re-check decision-heavy context against current user intent.

Durable output: recommended direction, relevant facts/evidence, hypotheses, open alternatives, confirmed decisions if any, unknowns, and execution target recommendation.

Boundary: do not implement or create worktrees unless the user explicitly redirects the thread into execution.

### research

Coordination purpose: seek external evidence, prior art, ecosystem context, market/product comparison, baselines, feasibility, novelty, or paper direction.

Project state use: use repo and sidecar context to frame the question, then make evidence quality visible. Preserve disconfirming evidence to seek.

Durable output: evidence-backed findings, hypotheses, open alternatives, baselines, risks, unknowns, and recommended next step.

Boundary: do not treat external summaries as implementation decisions.

### primary-execution

Coordination purpose: implement one task/worktree, run validation, update handoff state, finish/archive work, and prepare PR text.

Project state use: use sidecar/handoff/git state as a continuity baseline, then verify current files, HEAD, dirty state, and validation needs before acting.

Durable output: code changes, validation evidence, handoff or finish/archive state, risks, blockers, and compact receipt back to the hub.

Boundary: do not rely on restored workflow state as proof of correctness.

### review

Coordination purpose: inspect code, design, rigor, or PR readiness and return findings.

Project state use: load only the context needed for the review. Section handoff loading is often enough for risks, facts, validation, or thread summary.

Durable output: prioritized findings, residual risks, missing tests, and questions for the owning execution thread or hub.

Boundary: do not become the long-running task owner unless the user changes the role.

### validation

Coordination purpose: run focused checks, benchmarks, browser/UI/a11y validation, or regression tests.

Project state use: prefer exact validation context, commands, environment notes, and expected behavior. Treat old validation as stale unless current evidence supports it.

Durable output: commands run, results, environment notes, failures, limitations, and pass/fail interpretation.

Boundary: do not expand into design debate or implementation unless explicitly redirected.

### dogfood

Coordination purpose: capture real workflow feedback, reproduction notes, and issue drafts.

Project state use: keep observed behavior separate from inferences. Prefer `draft-issue`; create issues only when explicitly allowed.

Durable output: facts, inferences, unknowns, reproduction, suggested fix, priority, and next step.

Boundary: do not silently create GitHub issues or rewrite unrelated workflow state.

### explainer

Coordination purpose: produce onboarding, architecture, history, or project explanation that helps humans and future agents.

Project state use: combine stable docs, current code, and compact sidecar context when useful. Avoid turning hub threads into long tutorials.

Durable output: concise explanation, glossary, key files or docs, open questions, and recommended docs updates.

Boundary: do not become a project hub or execution owner.

## Shared Vocabulary

- `facts`: observable or user-provided facts.
- `evidence`: facts used to support or weaken claims.
- `hypotheses`: tentative interpretations or routes.
- `confirmedDecisions`: user/team-confirmed current choices, not objective truth.
- `openAlternatives`: still-available framings.
- `unknowns`: missing information.
- `disconfirmingEvidenceToSeek`: evidence that would weaken current hypotheses.

These categories are a writing and review discipline first. They do not require new sidecar schema until repeated use proves a field should become first-class.

## Related Docs

- [Direct Plan To Execution](../workflows/direct-plan-to-execution.md)
- [Thread Continuity](../workflows/thread-continuity.md)
- [Project Hub Workflow](../workflows/project-hub.md)
- [Review And Validation](../workflows/review-validation.md)
- [Handoff Loading Reference](./handoff-loading.md)
