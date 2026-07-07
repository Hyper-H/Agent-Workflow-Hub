# Thread Continuity

Thread continuity is for later continuation, not for replacing a complete plan.

Use it when an old thread is too long, unavailable, noisy, or when a review/validation thread only needs a narrow slice of saved handoff state.

Default flow:

```text
resume-query --query "<continue phrase or task>"
load-handoff --query "<same phrase>" --mode compact
```

Escalate only when needed:

- `--mode section --section validation` for validation.
- `--mode section --section risks` for review risk checks.
- `--mode section --section thread-summary` for a short semantic recap.
- `--mode full` only when the user explicitly asks for the full handoff or compact/section output cannot answer the concrete question.

If the query is ambiguous, ask the returned disambiguation question once. Do not guess between close tasks.

If the task exists but no handoff file exists, say so and continue with `resume-feature`, `audit-context`, or targeted investigation.
