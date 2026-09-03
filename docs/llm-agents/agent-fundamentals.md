---
title: "Agent Fundamentals"
description: "Core contracts for LLM agents: model decisions, tools, state, policy, evidence, and controlled autonomy"
---

# Agent Fundamentals (September 2026)

Version context: an agent is a system, not a model capability. Record the model revision, prompt/tool policy, state schema, and evaluation suite with every deployed agent version.

An LLM agent combines model inference with a control plane that observes inputs, selects permitted actions, persists state, and returns evidence. A chatbot becomes an agent only when it can affect or inspect an environment through governed capabilities.

## Core Components

| Component | Responsibility | Must be deterministic? |
|---|---|---|
| Model | Propose language, structured output, or next action | No |
| Instructions | Define role, constraints, and output contract | Versioned |
| Tools | Read or act through typed interfaces | Yes at boundary |
| Policy layer | Authorize actions and enforce budgets | Yes |
| State store | Persist work items, receipts, and recovery data | Yes |
| Evaluator | Decide whether the terminal result meets acceptance | Yes / independently reviewed |
| Observability | Correlate model calls, tools, decisions, and errors | Yes |

The model is not the source of truth for permissions, facts, task completion, or side-effect status.

## Agent Lifecycle

```text
request -> validate identity and input -> create durable work item
        -> choose a permitted next action -> execute or refuse
        -> persist receipt -> verify terminal result -> respond
```

A work item should have a unique ID, actor/tenant scope, idempotency key, attempt budget, policy revision, trace reference, and terminal receipt. Replaying the same request must be safe or explicitly rejected.

## Tools

A tool is a typed capability with an owner, not just a natural-language description.

```json
{
  "name": "get_invoice",
  "input_schema": {"invoice_id": "string"},
  "side_effect": "read_only",
  "authorization": "billing.read",
  "timeout_ms": 3000,
  "idempotency": "not_applicable",
  "receipt_schema": "invoice-v2"
}
```

Validate model-proposed parameters on the server. A valid schema does not prove that a call is authorized; authorization must bind the actor, tenant, resource, action, and current policy.

## State and Memory

Separate these objects:

- **Conversation context:** minimum information for the next model turn.
- **Run state:** current workflow state, attempt count, and tool receipts.
- **Long-term memory:** scoped records with ownership, expiration, and write policy.
- **Knowledge corpus:** source material retrieved with provenance.

A context window is not a database. Do not store opaque facts in a prompt and call them durable memory.

## Agent Versus Workflow

| Question | Prefer workflow | Consider agent |
|---|---|---|
| Is the step order already known? | Yes | Only if an unknown decision remains |
| Are actions high-impact or irreversible? | Yes, with approvals | Only within a narrow policy boundary |
| Does new evidence change the next step? | Maybe not needed | Yes, with explicit stop/replan conditions |
| Can success be mechanically verified? | Yes | Required before production autonomy |
| Is latency/cost tightly bounded? | Usually | Only after evaluation proves value |

Start with a workflow, then introduce a model decision at the smallest point where it provides measured benefit.

## Basic Action Gateway

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RequestContext:
    actor_id: str
    tenant_id: str
    remaining_steps: int


def execute_read_only(
    context: RequestContext,
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    if context.remaining_steps <= 0:
        raise RuntimeError("step budget exhausted")
    if tool_name != "get_invoice":
        raise PermissionError("tool is not available in this stage")
    invoice_id = arguments.get("invoice_id")
    if not isinstance(invoice_id, str) or not invoice_id:
        raise ValueError("invoice_id must be a non-empty string")
    return {"receipt_type": "invoice_lookup", "invoice_id": invoice_id}
```

Production code adds actual identity verification, a repository call, audit persistence, deadline propagation, and policy lookup. The important invariant is that the model never bypasses this gateway.

## Autonomy Levels

Choose an explicit level per action:

1. propose only — human or application performs it;
2. execute read-only — system returns evidence;
3. execute reversible action — bounded retry and receipt;
4. execute external/irreversible action — explicit approval;
5. autonomous durable workflow — only after end-to-end evaluation and incident controls.

One agent may operate at different levels for different tools. Never grant the highest level globally because a low-risk task exists.

## Interoperability

MCP standardizes a host/client/server boundary for resources, prompts, and tools. A2A standardizes communication with an independent agent service through agent discovery, tasks, messages, and artifacts. Neither protocol replaces application identity, authorization, data governance, or task-level evidence.

Use protocols to define a real boundary, not to add ceremony to an in-process function.

## Observability and Evaluation

Record action proposals, policy decisions, tool call inputs/outputs with appropriate redaction, retry reason, timing, cost, and terminal verdict. Evals should cover normal requests, malformed input, denied actions, injection attempts, tool failure, duplicate submission, and recovery.

## Gotchas

- **More tools do not automatically mean more capability.** They increase ambiguity and attack surface. **Fix:** expose only the task-scoped allowlist.
- **A successful API response is not task completion.** It can contain partial, stale, or unauthorized data. **Fix:** define a separate acceptance check tied to the user outcome.
- **Context growth hides state loss.** Long transcript history becomes expensive and can omit critical facts. **Fix:** persist structured state and retrieve a minimal authorized projection.
- **A protocol is not a security boundary by itself.** MCP/A2A metadata advertises capabilities but cannot grant authority. **Fix:** enforce authorization at every local or remote action gateway.

## Sources

- [OpenAI Agents SDK: agents](https://openai.github.io/openai-agents-python/agents/)
- [Model Context Protocol latest architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [A2A Protocol specification](https://a2a-protocol.org/latest/specification/)
- [OpenAI API: function calling](https://developers.openai.com/api/docs/guides/function-calling)

## See Also

- [[agent-design-patterns]]
- [[agent-architectures]]
- [[agent-memory]]
- [[function-calling]]
- [[agent-security]]
