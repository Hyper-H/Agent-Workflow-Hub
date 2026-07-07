# Direct Plan To Execution

Direct plan-to-execution remains the primary workflow.

A discussion or research thread should give the user a complete execution prompt and plan. The user can paste that prompt into a Primary Execution Thread, where implementation, validation, handoff, and PR work happen.

Agent Workflow Hub records the workflow state around that work. It does not replace the user's ability to carry a complete plan into an execution thread.

Use this path when:

- The user has a concrete implementation plan.
- The next thread is expected to modify code.
- The plan itself is the most important context.
- The execution thread can start from the pasted prompt without needing old chat history.

Recommended ending for discussion/research/hub plans:

```text
Execution target recommendation: open a new Primary Execution Thread.
```

or:

```text
Execution target recommendation: continue the existing execution thread.
```

or:

```text
Execution target recommendation: ask before choosing.
```

Do not read full handoffs only to produce this recommendation. Use the visible plan, compact sidecar state, and current user intent.
