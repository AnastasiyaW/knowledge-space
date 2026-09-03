---
title: "Agent Observability Dashboards"
description: "Trace contracts, dashboard views, and data-minimizing telemetry for tool-using and multi-agent systems; reviewed 2026-09-03."
---

# Agent Observability Dashboards

Reviewed 2026-09-03. An observability dashboard answers four operational questions: what work ran, which authority acted, which tools or models were involved, and what evidence makes the result trustworthy. It should not depend on a particular IDE hook or vendor event name.

## Start with a Trace Contract

Use one trace for one user-visible workflow or durable work item. Every model call, tool call, handoff, validator, and approval becomes a child span or event.

```json
{
  "schema_version": "agent-trace/v1",
  "timestamp": "2026-09-03T14:10:31.442Z",
  "trace_id": "tr_01J...",
  "span_id": "sp_01J...",
  "parent_span_id": "sp_01J-parent",
  "run_id": "run_01J...",
  "operation": "tool.fetch_source",
  "actor": { "kind": "agent", "id": "researcher@2026-09-03" },
  "outcome": "ok",
  "duration_ms": 184,
  "input_ref": "source:42",
  "output_ref": "artifact:claim-set-42",
  "tool": { "name": "fetch_source", "policy_id": "research-readonly-v2" },
  "attributes": { "attempt": 1, "environment": "production" }
}
```

Do not put secrets, raw user prompts, access tokens, or unrestricted tool output in the default event payload. Store a controlled reference or digest when replay requires it.

## Minimum Span Taxonomy

| Operation | Parent | Required fields | Success evidence |
|---|---|---|---|
| Workflow | None | run ID, objective, owner, terminal state | terminal receipt |
| Agent turn | Workflow | agent/config version, model, input/output references | validated output or error |
| Tool call | Agent turn | allowlist policy, tool name, arguments reference, deadline | tool receipt |
| Handoff | Agent turn | from/to owner, routing reason, context reference | accepted handoff |
| Validator | Workflow | criteria version, result, findings reference | pass/fail report |
| Approval | Workflow | reviewer identity, scope, decision | approval receipt |

The OpenTelemetry GenAI semantic-conventions project covers spans, metrics, and events for GenAI clients and MCP. Use its conventions where they match; keep application-specific fields namespaced and documented. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Emit a Structured Event

This dependency-free Python 3.11+ example writes one JSON event per line to standard output. A production collector can forward the same envelope to an OTLP endpoint, a queue, or a database.

```python
from __future__ import annotations

import json
from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4


def emit(operation: str, trace_id: str, started: float, outcome: str) -> None:
    event = {
        "schema_version": "agent-trace/v1",
        "timestamp": datetime.now(UTC).isoformat(),
        "trace_id": trace_id,
        "span_id": f"sp_{uuid4().hex}",
        "operation": operation,
        "outcome": outcome,
        "duration_ms": round((perf_counter() - started) * 1000, 2),
        "attributes": {"environment": "development"},
    }
    print(json.dumps(event, separators=(",", ":"), sort_keys=True))


def main() -> None:
    trace_id = f"tr_{uuid4().hex}"
    started = perf_counter()
    try:
        # Replace with a bounded model or tool invocation.
        result = "validated"
        emit("agent.generate_summary", trace_id, started, "ok")
        print(result)
    except Exception:
        emit("agent.generate_summary", trace_id, started, "error")
        raise


if __name__ == "__main__":
    main()
```

## Dashboard Views That Drive Decisions

| View | Primary question | Data needed |
|---|---|---|
| Run list | Which work is stuck, failed, or awaiting approval? | terminal state, owner, age, retry count |
| Trace tree | Where did time or authority move? | parent/child spans, duration, handoffs |
| Tool ledger | Which capability caused a failure or cost spike? | tool policy, tool outcome, arguments reference |
| Validator queue | Which candidates are safe to publish? | criteria version, verdict, evidence reference |
| Budget view | Which workflow exceeds its allocation? | model/tool units, cost attribution, concurrency |
| Incident view | Can this run be replayed or reconciled? | idempotency key, external receipt, error category |

Avoid vanity charts. A token chart without workflow identity cannot tell an operator which user task or production change it represents.

## Pipeline Design

```text
application / workflow controller
        |
        v
structured trace emitter
        |
        v
collector with schema validation and redaction
        |
        +--> durable event store
        |
        +--> OpenTelemetry-compatible backend
        |
        v
operator dashboard and alerts
```

The collector is a trust boundary. It validates event shape, assigns ingestion time, applies sampling/redaction, and rejects malformed payloads. Instrument at your own workflow and tool boundaries instead of assuming a third-party client emits every event your operations team needs.

The OpenAI Agents SDK exposes built-in tracing with trace, agent, turn, generation, function, guardrail, and handoff spans. An adapter can enrich those spans with your work-item and evidence references rather than replacing its trace hierarchy. [OpenAI Agents SDK tracing](https://openai.github.io/openai-agents-js/guides/tracing/)

## Sampling, Retention, and Privacy

| Data class | Default policy | Escalation |
|---|---|---|
| Identifiers and timing | Retain for operational window | Aggregate after the window |
| Prompt/output text | Do not retain by default | Opt-in, redacted, access-controlled capture |
| Tool arguments/results | Store references or allowlisted fields | Full capture only for approved debugging |
| Error payloads | Redact before storage | Time-limited secured incident record |

Set retention by purpose. Debug replay, product analytics, cost allocation, and audit evidence have different access and deletion requirements. Verify the actual storage behavior of the tracing backend you deploy; dashboard UI claims are not a data-retention policy.

## Alert Conditions

Alert on transitions that require action, not raw event volume:

- a run exceeds its deadline or budget;
- a side-effecting tool has an unknown outcome;
- validator failure rate changes after an agent/configuration release;
- an approval queue crosses its age target;
- a collector rejects events or loses its durable-store acknowledgement.

Every alert should link to a trace ID, owner, evidence reference, and runbook action.

## Gotchas

- **Issue: Logging raw prompts and tool results by default.** Telemetry becomes a secondary data leak and expensive replay store. **Fix:** log references, hashes, and allowlisted metadata; capture full payloads only under a documented, access-controlled policy.
- **Issue: Reusing one span ID across retries.** The dashboard cannot distinguish a new attempt from the original uncertain call. **Fix:** keep the trace and work-item identity, but create a new span and attempt number for every retry.
- **Issue: Treating a client library's events as the complete system trace.** Approval, queueing, and external receipts often happen outside the SDK. **Fix:** instrument workflow-controller boundaries and correlate vendor spans with the durable run ID.
- **Issue: Alerting on token count alone.** High volume can be legitimate; a silent side-effect timeout is more urgent. **Fix:** alert on violated policy, state, or service-level objectives.

## See Also

- [[llmops]]
- [[agent-orchestration]]
- [[multi-agent-systems]]
- [[multi-session-coordination]]

## Sources

- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- [OpenAI Agents SDK: Tracing](https://openai.github.io/openai-agents-js/guides/tracing/)
- [OpenAI Agents SDK: Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
