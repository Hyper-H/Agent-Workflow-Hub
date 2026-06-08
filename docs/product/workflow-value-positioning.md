# Workflow Value Positioning

Agent Workflow Hub is an agent-native workflow state layer for multi-worktree, multi-thread, and multi-agent software development. It is not a memory patch for weak models, and it is not primarily a token-saving tool.

Its job is to make development workflow state explicit, inspectable, and portable across chats, worktrees, branches, and agents.

## Why This Still Matters As Agent Memory Improves

Native agent platforms will keep improving. Codex, Claude Code, Cursor, Windsurf, and similar tools are likely to cover more of the following over time:

- Reading and summarizing repository context.
- Remembering user preferences.
- Remembering recent thread history.
- Resuming simple work inside one conversation or one workspace.
- Reconstructing likely next steps from code, commits, and open files.

Those capabilities are valuable. Agent Workflow Hub should not compete with them as a second memory system.

The durable gap is workflow coordination. A stronger model can infer a lot, but multi-worktree development still benefits from a shared state protocol that says, explicitly:

- Which task is active.
- Which worktree and branch own that task.
- What is fact, inference, or unknown.
- What validation was run and when.
- What safety rules constrain the next agent.
- Whether the recorded handoff is stale relative to current Git state.
- Which project hub actions are recommended next.

## Product Contract Versus Benefits

The product contract is workflow state coordination:

- Stable project identity across worktrees.
- Local sidecar state outside the target repository.
- Handoff artifacts that separate facts, inferences, unknowns, validation, and safety rules.
- Project hub inventory from real Git worktrees plus sidecar active tasks.
- Stale detection from recorded HEAD and dirty fingerprints.
- Recommended actions and prompts for old execution threads or new execution threads.
- Natural-language routing from a human phrase to the right task/worktree.

Benefits include:

- Less repeated scanning.
- Lower context rebuild cost.
- Faster handoff between threads.
- Better dogfood feedback capture.
- More consistent weekly reports.

Those benefits matter, but they are not the core promise. If future agents become better at reading context cheaply, Agent Workflow Hub should still be useful because it records project workflow state explicitly.

## What Agent Workflow Hub Does Not Replace

Agent Workflow Hub does not replace:

- Code understanding.
- Tests or validation.
- PR review.
- Issue trackers.
- Project management tools.
- Human product judgment.
- The agent's own investigation strategy.
- Native model memory.

`resume-feature` and `resume-query` restore recorded workflow state. They do not prove the code is correct. They also do not prove the recorded state is sufficient; stale warnings, unknowns, and missing validation are first-class signals that the agent must re-check.

The sidecar is not a chat transcript database and not a model reasoning store. It should contain auditable project state, not hidden chain-of-thought or long logs.

## Core Concepts

### Workflow State Layer

A local protocol and set of artifacts that describe what is happening in the project workflow: tasks, worktrees, branches, handoffs, validation, safety rules, stale state, and recommended next actions.

### Project Hub

The coordination view for a repository or project. A project hub thread owns the project map, worktree inventory, routing decisions, and periodic summaries. It should not own every implementation detail.

### Primary Execution Thread

The thread that owns implementation for one active task/worktree. It updates sidecar state, performs validation, saves handoffs, finishes or archives work, and reports compact results back to the project hub.

### Sidecar

The local state directory under `%USERPROFILE%\.codex\projects\<project-id>\`. It stores config, active tasks, compact project state, handoffs, reports, archives, and events. It is intentionally outside the target repository.

### Audit Project

The project hub inventory action. It compares real `git worktree list` output with sidecar active tasks, reports missing or stale state, and produces recommended actions, execution-thread prompts, and cleanup prompts.

### Resume Query

The natural-language routing action. It maps a phrase such as `markerless clean` to a sidecar task/worktree using deterministic local matching, then performs sidecar-first resume when confidence is high.

## Where It Remains Useful

Agent Workflow Hub remains valuable in workflows where state must outlive a single chat or workspace:

- Multiple worktrees with related branches.
- Parallel execution threads.
- Hub threads that need inventory without owning implementation detail.
- Long-running branches where validation and handoff freshness matter.
- Team or multi-agent dogfood where issues and reports need consistent structure.
- Auditing whether a task has safety rules, validation, handoff, stale warnings, or cleanup prompts.
- Future UI surfaces that need stable machine-readable state.
- Future evals that compare workflow quality, not just answer quality.

## Future Direction

Future versions should keep the same boundary:

- Let native agents get better at context reading and reasoning.
- Keep Agent Workflow Hub focused on explicit workflow artifacts and local project state.
- Avoid storing chat transcripts or model reasoning.
- Keep dynamic state outside the target repository.
- Make project state easy to inspect manually and easy to consume by future UI/eval layers.

The long-term value is not that agents forget. It is that software development across worktrees, branches, and threads needs a shared workflow state layer that agents and humans can both trust.
