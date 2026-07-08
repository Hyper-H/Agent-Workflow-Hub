# Events And Eval

`events.jsonl` is append-only local sidecar telemetry for workflow evaluation. It is not a chat transcript, benchmark trace, or token accounting source.

V3.9 adds `load-handoff` events with fields such as:

```json
{
  "event": "load-handoff",
  "taskId": "...",
  "threadRole": "...",
  "loadMode": "section",
  "section": "validation",
  "reasonCode": "validation-needed",
  "reasonNotePresent": false,
  "handoffAvailable": true,
  "contentReturned": true,
  "contentChars": 820,
  "resolvedBy": "query",
  "scanScope": "sidecar-handoff-load"
}
```

The event must not include handoff content, long logs, model reasoning, diffs, chat transcripts, or exact token claims.

`eval-report` aggregates:

- `load-handoff` count.
- compact / section / full counts.
- full load rate.
- reason distribution.
- section distribution.
- grouped thread roles.
- compact-insufficient count.

These are workflow proxy metrics. They help dogfood whether Agent Workflow Hub improves recoverability and auditability; they do not prove correctness or exact token savings.
