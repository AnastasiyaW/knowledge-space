---
title: "Agent Orchestration"
description: "Coordinate model calls, tools, handoffs, approvals, retries, and evidence through explicit task state rather than a framework-specific agent loop."
tags: [llm-agents, orchestration, workflows, multi-agent, state-machine, approvals, observability]
---

# Agent Orchestration (September 2026)

Version context: orchestration frameworks, SDKs, protocol versions, storage backends, and model tool semantics change quickly. Design the task state, authorization boundary, and terminal evidence first; select a framework only after those contracts are clear.

Agent orchestration is the controlled execution of a task across model calls, deterministic code, tools, agents, people, and durable state. It is not a synonym for "let several agents chat." The orchestrator owns the task lifecycle and proves whether a requested effect happened.

## Define the Durable Task Contract

```json
{
  "task_id": "publish-research-044",
  "schema_version": "agent-task/v1",
  "objective": "prepare a cited draft for review",
  "input_refs": ["artifact:source-manifest-44"],
  "owner": "editorial-platform",
  "state": "PENDING",
  "tool_policy_revision": "tools@9",
  "approval_policy_revision": "review@4",
  "idempotency_key": "publish-research-044:v1",
  "attempt": 0
}
```

The task record is application-owned. It holds only references to controlled data and persists across worker restarts, browser disconnects, and agent handoffs.

## Model States and Receipts Separately

Use non-terminal states to express work in progress and mutually exclusive terminal states for the task result. The legal transitions must include an approval decision, expiry, and cancellation:

```text
PENDING -> RUNNING -> COMPLETED | FAILED
RUNNING -> NEEDS_APPROVAL
NEEDS_APPROVAL + bound approved receipt -> RUNNING
NEEDS_APPROVAL + denied or expired receipt -> CANCELLED
any non-terminal state -> CANCELLED

verification status: PENDING | VERIFIED | REJECTED
```

Every transition has a receipt. A terminal receipt contains the output reference, validator result, external-effect receipt if any, retry classification, and configuration revisions. The task resumes from `NEEDS_APPROVAL` only when the approval receipt is bound to the exact task, effect, arguments digest, actor, scope, expiry, and idempotency key. Verification status is a review of immutable terminal evidence: `REJECTED` does not pretend that an already completed external effect never happened, and `VERIFIED` does not authorize a new effect.

## Separate Deterministic Control from Model Judgment

Use deterministic code for:

- authorization, tenant scope, budgets, rate limits, and data classification;
- schema parsing, business invariants, idempotency, and retries;
- state transitions, timers, cancellation, and external-effect reconciliation;
- approval routing and audit records.

Use a model where interpretation, planning alternatives, summarization, or bounded selection is actually required. Frameworks such as LangGraph support workflows that combine deterministic and model-driven steps, durable execution, and human-in-the-loop points. [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)

## Roles Are Not Permissions

A router may choose a reviewed configuration. A researcher may create a claim set. An executor may request a tool. A reviewer may issue a verdict. None of those labels grants access to data or external effects.

For each role, define:

| Role | May do | Must not decide alone | Required receipt |
|---|---|---|---|
| Router | choose an approved path | access beyond task scope | route and configuration revision |
| Worker | perform bounded model/tool work | publish or deploy by default | output, tool, and terminal receipts |
| Reviewer | evaluate explicit criteria | alter candidate evidence | verdict and findings reference |
| Approver | authorize a defined effect | rewrite the task implicitly | identity, scope, and decision |

This prevents a handoff from becoming an authority escalation.

## Tools, Handoffs, and Protocol Boundaries

A model tool call invokes a capability exposed to the current agent. A handoff delegates a bounded task to another worker or specialist. Both need a schema, identity, deadline, and durable result record.

MCP describes a host-client-server protocol for agent-to-tool context exchange, while A2A covers collaboration between independent agents. Use neither protocol as a replacement for application authorization or task receipts. [MCP architecture](https://modelcontextprotocol.io/specification/latest/architecture) and [A2A Protocol](https://a2a-protocol.org/latest/)

The OpenAI Agents SDK is one current example of an agent runtime with tools, handoffs, guardrails, human-in-the-loop, and tracing. Its primitives can inform a design but should not become a provider-neutral task schema. [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)

## Retry, Cancellation, and Side Effects

Retry only an action proven safe to retry. Create an idempotency key before an effectful tool call and preserve it through queue, agent, and tool boundaries.

```text
timeout or lost response
  -> reconcile external receipt
  -> retry only if absence of effect is established
  -> otherwise mark for review
```

Cancellation is a state transition with a reconciliation step, not merely a request to stop generating text. A cancelled task must say whether a tool call was not started, was stopped, or completed before cancellation arrived.

## Select a Runtime by Contract

| Requirement | Capability to require |
|---|---|
| Long-running work | durable state, resume, timeout, and reconciliation |
| Sensitive action | approval checkpoint, policy enforcement, idempotency |
| Multiple specialists | typed handoff, result schema, ownership and deadline |
| Concurrent workers | queue lease, deduplication, backpressure, dead-letter path |
| Auditability | trace, state-transition receipts, redaction, evaluator version |
| Portability | internal task contract isolated from framework SDK objects |

A small application-owned state machine is often sufficient. Add a graph runtime, agent SDK, or multi-agent protocol only when its capability closes a measured requirement.

## Gotchas

- **A conversation is not orchestration state.** Chat history does not prove who owns a task or whether an effect completed. **Fix:** persist a task record and terminal receipts.
- **Handoffs can multiply authority.** A delegated instruction may expose tools or data the sender did not control. **Fix:** authorize independently at the receiver and at every tool boundary.
- **Retries can duplicate real-world actions.** A timeout does not prove an API call failed. **Fix:** reconcile by idempotency key before retrying.
- **Human review after an effect is too late.** A reviewer cannot reverse an already published or paid action. **Fix:** place approval before the irreversible boundary.
- **Framework state is not automatically portable.** SDK object layouts and persistence semantics change. **Fix:** store a small application-owned contract outside the framework.
- **Throughput is not completion.** A busy queue can hide failed tasks without terminal evidence. **Fix:** alert on missing or stale terminal receipts.

## Sources

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [A2A Protocol](https://a2a-protocol.org/latest/)

## See Also

- [[multi-agent-messaging]]
- [[multi-session-coordination]]
- [[agent-design-patterns]]
- [[agent-evaluation]]
- [[agent-observability-dashboards]]
- [[agent-security]]
