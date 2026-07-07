# Review And Validation Workflow

Review and validation threads often need only part of a handoff.

Use section loading instead of full loading when possible:

```text
load-handoff --query "<task>" --mode section --section validation --reason validation-needed
```

Useful sections:

- `validation`: commands, results, notes, and validation time.
- `risks`: recorded risks.
- `facts`: objective facts.
- `inferences`: agent conclusions that need checking.
- `unknowns`: known gaps.
- `next-step`: suggested next action.
- `thread-summary`: short semantic recap.

Review and validation outputs should report findings back to the owning execution thread or Project Hub. They should not silently mutate code unless the user explicitly changes the thread into an implementation thread.
