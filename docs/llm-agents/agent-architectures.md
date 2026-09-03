---
title: "Agent Architectures"
description: "Choose a bounded control-flow architecture for LLM agents: state, tools, handoffs, protocols, and evidence"
---

# Agent Architectures (September 2026)

Version context: reviewed against the MCP `latest` specification, A2A, and OpenAI Agents SDK documentation. Protocol revisions and SDK releases are dependencies; record the exact revision used by a deployed system.

An agent architecture is the deterministic control plane around probabilistic model calls. The architecture owns permissions, state transitions, retry limits, durable work, and evidence. The model proposes; the control plane decides what can happen next.

## Choose the Smallest Sufficient Shape

| Shape | Use when | Required controls |
|---|---|---|
| Single bounded action | One request, no side effect or one reversible tool action | Input validation, timeout, output validation |
| Explicit state machine | A task has stages, retries, approvals, or recovery | Transition table, budget, idempotency, terminal states |
| DAG | Independent tasks can run in parallel and have explicit joins | Dependency graph, join semantics, per-node receipts |
| Specialist handoff | Different authority or domain owns a task | Typed handoff contract, authorization, history filter |
| Remote agent boundary | Independent service owns execution | Protocol, authentication, task lifecycle, artifact contract |

Do not begin with a multi-agent graph. Add structure only when a simpler bounded flow cannot meet the required reliability, permission, or latency contract.

## Work Item Contract

A durable work item makes retries and recovery inspectable.

```json
{
  "task_id": "task_01J...",
  "state": "planned",
  "attempt": 0,
  "attempt_limit": 3,
  "idempotency_key": "sha256:...",
  "input_ref": "artifact://request/...",
  "policy_revision": "agent-policy-v4",
  "trace_ref": "trace_...",
  "terminal_receipt": null
}
```

Every transition has one owner and a reason. Unknown states fail closed.

## Minimal State Machine

```python
from dataclasses import dataclass, replace
from typing import Literal

State = Literal["planned", "running", "verified", "failed", "cancelled"]
ALLOWED: dict[State, set[State]] = {
    "planned": {"running", "cancelled"},
    "running": {"verified", "failed", "cancelled"},
    "verified": set(),
    "failed": set(),
    "cancelled": set(),
}


@dataclass(frozen=True)
class WorkItem:
    task_id: str
    state: State
    attempt: int
    attempt_limit: int


def transition(item: WorkItem, target: State) -> WorkItem:
    if target not in ALLOWED[item.state]:
        raise ValueError(f"invalid transition: {item.state} -> {target}")
    if target == "running" and item.attempt >= item.attempt_limit:
        raise RuntimeError("attempt budget exhausted")
    return replace(
        item,
        state=target,
        attempt=item.attempt + (target == "running"),
    )
```

Tool calls occur only in `running` after authorization and schema validation. `verified` requires an independently checkable receipt, not a model statement that work completed.

## Memory and Context

Separate four things:

- **Run state:** the durable work item and transition receipts.
- **Conversation context:** the minimum input needed for the next model turn.
- **Long-term memory:** scoped, versioned records with ownership and retention.
- **Knowledge corpus:** source documents retrieved with provenance.

A prompt summary cannot replace a durable state record. Conversely, the model should not receive all durable records by default; retrieve a least-privilege projection.

## Tool Boundary

Each tool needs a typed input schema, actor/tenant scope, authorization policy, timeout, idempotency rule, side-effect classification, and output receipt.

```text
model proposal -> schema validation -> policy decision -> tool execution
               -> receipt persistence -> verified state transition
```

Read-only tools and reversible actions can have different policy paths. Destructive, financial, external-message, or privilege-changing actions require an explicit approval boundary.

## Interoperability Boundaries

MCP and A2A solve different problems:

| Protocol | Boundary | Core unit | Do not assume |
|---|---|---|---|
| MCP | Host application to focused server | Resources, prompts, tools; negotiated capabilities | That a tool is authorized merely because it is advertised |
| A2A | Independent agent services | Agent Card, task, message, artifact | That a remote agent exposes its internal memory or tools |

MCP's host-client-server architecture keeps each server scope isolated. Its current `latest` protocol is stateless: every request carries declared protocol version and capabilities, and a client may use `server/discover` before other calls for server discovery. A2A provides a task lifecycle for opaque remote agents and uses an Agent Card for discovery and interaction requirements.

Use a protocol only when its boundary exists. An in-process function call does not become safer by wrapping it in a remote-agent protocol.

## Handoffs and Specialists

A specialist handoff must include:

1. destination identity and permitted capability;
2. typed reason and task reference;
3. authorized context projection, not full history by default;
4. responsibility for side effects and final response;
5. trace linkage and terminal receipt.

The OpenAI Agents SDK is one current implementation example: it supports tools, guardrails, handoffs, structured outputs, and tracing. Those SDK features do not replace application authorization or durable workflow state.

## Observability and Evaluation

Capture model calls, tool calls, handoffs, policy decisions, transition records, errors, and redacted input/output metadata. Correlate them with task ID, trace ID, policy revision, and deployment revision.

Evaluate architecture with replayable scenarios:

- permitted and denied tool invocation;
- retry after a transient failure;
- duplicate request with the same idempotency key;
- malformed tool result;
- handoff with overscoped history;
- timeout, cancellation, and terminal recovery.

## Gotchas

- **A loop without a budget is not an architecture.** It can repeat an unsuccessful action indefinitely. **Fix:** enforce iteration, time, cost, and retry limits in deterministic state.
- **A handoff is an authorization boundary.** Forwarding full conversation history can disclose data or grant unintended capability. **Fix:** pass a typed, least-privilege projection and authorize the receiving specialist.
- **Protocol discovery is not trust.** An advertised MCP tool or A2A Agent Card does not grant permission to use it. **Fix:** bind discovery to identity, explicit policy, and per-action authorization.
- **Tracing can contain sensitive content.** Generation and tool spans may record inputs and outputs. **Fix:** set redaction/retention policy before enabling telemetry and test it with representative data.

## Sources

- [Model Context Protocol latest architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Model Context Protocol latest server primitives](https://modelcontextprotocol.io/specification/latest/server)
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- [OpenAI Agents SDK: agents](https://openai.github.io/openai-agents-python/agents/)
- [OpenAI Agents SDK: tracing](https://openai.github.io/openai-agents-python/tracing/)

## See Also

- [[agent-design-patterns]]
- [[agent-memory]]
- [[function-calling]]
- [[tool-use-patterns]]
- [[multi-agent-systems]]
