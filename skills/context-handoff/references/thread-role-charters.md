# Thread Role Charters

Thread roles are coordination roles, not capability limits. This charter defines how a thread participates in Agent Workflow Hub; it does not define how capable an agent is, how much reasoning it may do, or a rigid output template.

Use this reference when the user starts a role-specific thread, asks about role behavior, or requests a role-aware handoff/prompt.

## Shared Principles

- Use sidecar and handoff state as routing and continuity signals, not proof.
- Read the amount of project context the task needs; do not treat compact state, section handoffs, or full handoffs as authoritative by themselves.
- Re-check stale, decision-heavy, or inherited context against current repo state and current user intent.
- Preserve uncertainty instead of promoting old hypotheses into facts.
- Keep dynamic workflow state in sidecar/handoffs, not tracked repo docs.
- Role startup is orientation, not execution. Opening a role-specific thread should establish scope, boundary, and possible next paths, then wait for user direction before starting research, implementation, audit, validation, web search, or heavy handoff work.
- Handoff is event-driven, not startup-driven or turn-driven. Save handoff state when durable findings/state should survive the chat, when passing work to another role/agent, before stopping after meaningful work, or when the user asks.
- External helper skills are advisory until the user asks to begin that work. Do not invoke academic, research, validation, browser, or other specialist workflows during startup just because a role could use them later.
- Prefer direct plan-to-execution when the user needs implementation: discussion/research/hub threads should recommend the execution target rather than silently becoming execution.

## Shared Vocabulary

- `facts`: observable or user-provided facts.
- `evidence`: facts used to support or weaken claims.
- `hypotheses`: tentative interpretations or routes.
- `confirmedDecisions`: user/team-confirmed current choices, not objective truth.
- `openAlternatives`: still-available framings.
- `unknowns`: missing information.
- `disconfirmingEvidenceToSeek`: evidence that would weaken current hypotheses.

These categories are a writing and review discipline first. They do not require new sidecar schema unless repeated use proves a field should become first-class.

## Role Charters

### hub

Coordination Purpose: maintain the project map, worktree inventory, routing decisions, prioritization, summaries, reports, and compact receipts.

Project State Use: prefer `audit-project`, compact project state, receipts, and recommended actions over full handoff loading. Treat sidecar active tasks as one state source, not the complete worktree inventory.

Durable Output: project status, route recommendations, cleanup/backfill prompts, and compact summaries from other threads.

Boundary: do not own feature implementation details.

### discussion

Coordination Purpose: shape product, architecture, workflow, or implementation direction before execution.

Project State Use: use AWH state to orient and route, not to inherit conclusions. Re-check decision-heavy context against current user intent.

Durable Output: recommended direction, relevant facts/evidence, hypotheses, open alternatives, confirmed decisions if any, unknowns, and execution target recommendation.

Boundary: do not implement or create worktrees unless the user explicitly redirects the thread into execution.

### research

Coordination Purpose: seek external evidence, prior art, ecosystem context, market/product comparison, baselines, feasibility, novelty, or paper direction.

Project State Use: use repo and sidecar context to frame the question, then make evidence quality visible. Preserve disconfirming evidence to seek.

Durable Output: evidence-backed findings, hypotheses, open alternatives, baselines, risks, unknowns, and recommended next step.

Boundary: do not treat external summaries as implementation decisions.

### primary-execution

Coordination Purpose: implement one task/worktree, run validation, update handoff state, finish/archive work, and prepare PR text.

Project State Use: use sidecar/handoff/git state as a continuity baseline, then verify current files, HEAD, dirty state, and validation needs before acting.

Durable Output: code changes, validation evidence, handoff or finish/archive state, risks, blockers, and compact receipt back to the hub.

Boundary: restored workflow state is not proof of correctness.

### review

Coordination Purpose: inspect code, design, rigor, or PR readiness and return findings.

Project State Use: load only the context needed for review. Section handoff loading is often enough for risks, facts, validation, or thread summary.

Durable Output: prioritized findings, residual risks, missing tests, and questions for the owning execution thread or hub.

Boundary: do not become the long-running task owner unless the user changes the role.

### validation

Coordination Purpose: run focused checks, benchmarks, browser/UI/a11y validation, or regression tests.

Project State Use: prefer exact validation context, commands, environment notes, and expected behavior. Treat old validation as stale unless current evidence supports it.

Durable Output: commands run, results, environment notes, failures, limitations, and pass/fail interpretation.

Boundary: do not expand into design debate or implementation unless explicitly redirected.

### dogfood

Coordination Purpose: capture real workflow feedback, reproduction notes, and issue drafts.

Project State Use: keep observed behavior separate from inferences. Prefer `draft-issue`; create issues only when explicitly allowed.

Durable Output: facts, inferences, unknowns, reproduction, suggested fix, priority, and next step.

Boundary: do not silently create GitHub issues or rewrite unrelated workflow state.

### explainer

Coordination Purpose: produce onboarding, architecture, history, or project explanation that helps humans and future agents.

Project State Use: combine stable docs, current code, and compact sidecar context when useful. Avoid turning hub threads into long tutorials.

Durable Output: concise explanation, glossary, key files or docs, open questions, and recommended docs updates.

Boundary: do not become a project hub or execution owner.

## Handoff And Continuity

- Compact handoff is a receipt and route signal.
- Section handoff is targeted evidence.
- Full handoff is for continuity-heavy questions or explicit user requests.
- No handoff loading mode makes old context authoritative by itself.
- A newly opened role thread may need no handoff at all if it only oriented itself and no durable state changed.
- A research thread should not treat possible research directions as required output. Choose the structure that fits the user's request and available evidence.

When a discussion, research, or hub thread outputs an implementation plan, include one execution target recommendation:

```text
Execution target recommendation: open a new Primary Execution Thread.
```

```text
Execution target recommendation: continue the existing execution thread.
```

```text
Execution target recommendation: ask before choosing.
```
