---
title: "Agentic Systems Landscape (September 2026)"
description: "Protocol boundaries, runtime choices, and production control-plane patterns for agentic systems; reviewed 2026-09-03."
---

# Agentic Systems Landscape (September 2026)

Reviewed 2026-09-03. Treat an agent system as an application control plane around probabilistic model calls, not as a collection of autonomous personas. The durable units are contracts, state, permissions, evidence, and rollback boundaries.

## Protocol Boundaries

| Boundary | Use it for | Owns the lifecycle | Do not use it as |
|---|---|---|---|
| MCP | Connecting an application-hosted agent to tools, data, and context providers | The host application | A generic agent-to-agent workflow engine |
| A2A | Exchanging tasks and outcomes between separately operated agents | Each participating agent/service | A replacement for tool authorization or local function calls |
| Application API | Internal calls between components you deploy together | Your application | A public interoperability protocol without a compatibility contract |

MCP specifies a host-client-server architecture: the host creates clients, controls permissions, and manages lifecycle. [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

A2A is an interoperability protocol for communication between agents. It complements MCP rather than replacing it: an agent can use MCP to reach its tools and A2A to exchange work with another agent. [A2A specification](https://a2a-protocol.org/latest/)

## Runtime Choice

Choose the smallest runtime that exposes the control you need.

| Need | Suitable starting point | Required control |
|---|---|---|
| One bounded task with a few tools | One agent loop in application code | Tool schemas, deadlines, structured final output |
| A specialist helps a manager | Manager calls specialist as a tool | Manager remains the sole final-output authority |
| The user should continue with a specialist | Explicit handoff | Routing rule, user-visible ownership, context contract |
| Independent work items | Deterministic fan-out and fan-in | Idempotency key, concurrency cap, reducer |
| Long-running or restartable work | Durable workflow/state store | Checkpoints, lease, retry policy, terminal receipt |

The OpenAI Agents SDK documents two distinct composition patterns: specialists used as tools keep a manager in control, while handoffs transfer the active conversation to a specialist. Its guidance also distinguishes model-selected orchestration from code-selected orchestration. [Agent orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)

Managed runtimes can reduce infrastructure ownership, but they do not remove the need to define data access, approval, output validation, and incident handling. For example, Claude Managed Agents models an agent as a versioned configuration plus an environment and a session. [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/quickstart)

## Production Control Plane

An agent invocation should have one durable record. Store references to large inputs and outputs instead of copying them through every prompt.

```json
{
  "run_id": "run_01J...",
  "work_item_id": "news-2026-09-03-001",
  "parent_run_id": null,
  "attempt": 1,
  "input_ref": "s3://private-bucket/intake/001.json",
  "agent_version": "news-curator@2026-09-03",
  "tool_policy_id": "news-read-only-v3",
  "status": "running",
  "output_ref": null,
  "evidence": [],
  "idempotency_key": "news-2026-09-03-001:curate:v3"
}
```

### Required Invariants

- One component owns each mutable record. Workers may append evidence, but only the workflow controller changes the terminal status.
- A retry uses the same work item and a new attempt number. It never silently creates a second publication candidate.
- A tool call has an allowlisted capability, deadline, caller identity, and receipt. Unknown tool outcomes fail closed.
- A generated answer is not a receipt. A receipt identifies the input, agent/configuration version, tool results, validator result, and timestamp.
- Public publication is a separate state transition after review. Do not equate successful extraction with approval.

## Build Order

1. Implement a single-agent path with a typed input and typed output.
2. Add deterministic validation before adding another agent.
3. Add a separately scoped evaluator when a bad output is materially costly.
4. Add parallel workers only for independent, partitioned work items.
5. Add durable recovery only when the work can outlive one process.
6. Add cross-service A2A only when independently owned agents need a stable interoperability boundary.

This order keeps the failure surface observable. A multi-agent design is justified by a concrete need for independent work, separation of authority, or a different trust boundary—not by a role name.

## Model and Tool Routing

Route by the contract, not by a product label.

| Work class | Routing criterion | Example validator |
|---|---|---|
| Extraction | Schema is known | JSON schema and source-reference checks |
| Classification | Allowed labels are finite | Enum validation and confidence policy |
| Drafting | Human review is required | Editorial checklist and approval record |
| Code change | Repository state is authoritative | Targeted test plus diff review |
| External action | Side effect is material | Explicit approval and idempotency key |

Use a model-selected route only when the route itself is an open-ended reasoning task. Use application code when the route is a policy decision, an authorization boundary, or a budget limit.

## When Not to Add an Agent

Do not add a specialist merely to rename a prompt. Keep one agent when:

- the task is sequential and the same permissions apply throughout;
- the result has one deterministic validator;
- sharing full context is cheaper and safer than serializing it between agents;
- no independent reviewer or external trust boundary is needed.

Splitting work introduces context loss, extra cost, more traces to inspect, and another failure mode at every handoff.

## Gotchas

- **Issue: Treating MCP and A2A as interchangeable.** MCP authorization belongs to the host/tool boundary; A2A addresses communication between agents. **Fix:** document both boundaries separately and use the protocol that owns the relationship.
- **Issue: Letting a model decide a policy-controlled route.** A natural-language instruction is not an authorization system. **Fix:** keep budgets, publication approval, and destructive-action gates in deterministic application code.
- **Issue: Retrying with a new identity.** A timeout can leave an external side effect uncertain. **Fix:** persist an idempotency key and reconcile the prior attempt before resubmitting.
- **Issue: Counting a model response as completion.** A fluent response may omit required evidence. **Fix:** make the workflow terminate only after the validator records a PASS receipt.

## Limitations

Protocols make boundaries explicit; they do not make agents reliable, secure, or mutually trustworthy. Tool behavior, source quality, model non-determinism, and reviewer policy remain application responsibilities. Test the actual workflow with representative failures before increasing autonomy.

## See Also

- [[agent-orchestration]]
- [[managed-agents]]
- [[multi-agent-systems]]
- [[multi-session-coordination]]
- [[llmops]]

## Sources

- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [A2A Protocol](https://a2a-protocol.org/latest/)
- [OpenAI Agents SDK: Agent Orchestration](https://openai.github.io/openai-agents-js/guides/multi-agent/)
- [Claude Managed Agents Quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
