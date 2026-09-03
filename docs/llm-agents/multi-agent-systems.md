---
title: "Multi-Agent System Coordination"
description: "Coordinate multiple agents through task contracts, ownership, authority, state, and evidence boundaries; add agents only when a measured decomposition needs them."
tags: [llm-agents, multi-agent, orchestration, delegation, governance, evidence]
---

# Multi-Agent System Coordination

**Scope checked: 2026-09-04.** A multi-agent system is a workflow with more than one autonomous decision-maker or execution role. It is not automatically more capable than a single agent. Add a role only when the task has a clear decomposition, a distinct authority or tool boundary, and a way to evaluate the additional coordination cost.

## Start with the Work Contract

Every delegated task needs a record that survives messages and restarts.

```json
{
  "task_id": "docs-review-001",
  "input_revision": "immutable source revision",
  "owner": "named coordinator",
  "acceptance": ["named checks pass", "evidence is attached"],
  "authority": "read-only review",
  "allowed_tools": ["read", "search", "named test"],
  "side_effect_policy": "no external actions",
  "handoff": "structured findings with source references"
}
```

The contract prevents a specialist role from becoming a vague persona. It lets the coordinator distinguish a completed task from a message that merely sounds complete.

## Use the Simplest Coordination Shape

| Shape | Good fit | Main risk |
|---|---|---|
| single agent with deterministic tools | one coherent task and one authority boundary | unnecessary delegation hides responsibility |
| sequential pipeline | each artifact is the input to the next defined stage | an early error becomes uninspected downstream context |
| parallel investigation | independent sources, tests, or candidate designs | duplicate work and correlated assumptions |
| supervisor with bounded workers | several distinct task contracts require a final owner | supervisor becomes an untestable bottleneck |
| independent reviewer | material change needs a fresh assessment | reviewer is asked to approve without access to evidence |

Do not select a number of agents from a template. Measure whether the current bottleneck is missing evidence, insufficient tool access, or an actual need for independent review. A deterministic transform should remain code, even when an agent can describe it.

## Separate State by Concurrency Model

| State kind | Safe coordination pattern |
|---|---|
| immutable input or evidence | content digest and read-only references |
| append-only findings or receipts | one record per producer with stable identifiers |
| mutable task ownership | a lease or explicit single writer |
| shared artifact under edit | isolated worktree or branch plus reviewed merge |
| directed question | addressed message with sender, recipient, and response record |
| external side effect | idempotency key, named owner, and target receipt |

Avoid a single shared scratchpad that every agent can rewrite. It makes loss, conflict, and accidental instruction injection hard to attribute. If an agent needs a lock, record the resource, holder, heartbeat, expiry, and recovery check.

## Authority Does Not Flow Through a Handoff

A coordinator may ask an agent to investigate a production issue without granting it deployment rights. Tool permissions, data access, approval policy, and the target environment must be assigned per role. A forwarded message, summary, or agent confidence score cannot elevate authority.

Claude Code subagents are a concrete example of a system where delegated roles can be defined with scoped instructions and tool limits; consult the current product documentation for exact fields and precedence. [Create custom subagents](https://code.claude.com/docs/en/subagents)

For a system with external effects, use a release gate outside the debate loop:

1. the worker produces a candidate and evidence;
2. a verifier compares evidence to the acceptance contract;
3. a named owner provides any required approval;
4. the authorized executor performs the action with an idempotency key where applicable;
5. the workflow records the actual target receipt.

## Review and Aggregation

Parallel work should converge through evidence, not vote count. The coordinator can compare independently gathered sources, deterministic test results, and bounded trade-offs. It must be able to return “not proven” when no candidate meets the contract.

For security or safety concerns, retain the union of findings as triage and verify each finding before treating it as a defect or changing a target. NIST's generative-AI risk profile is a useful framing for maintaining risk and governance evidence across a system lifecycle. [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## Evaluate the Decomposition

A multi-agent workflow needs evaluation at two levels:

| Level | Question |
|---|---|
| role | does each worker produce the required artifact within its authority? |
| system | does the handoff preserve inputs, constraints, and evidence through completion? |
| operational | do retries, failures, locks, and side effects remain visible and recoverable? |
| comparative | does the team improve the task's acceptance result against a simpler baseline? |

Keep the simplest arrangement that meets the acceptance contract. More messages, roles, and model calls can increase latency, cost, and inconsistent state without adding new evidence.

## Common Failure Modes

- **Role theatre:** names such as “researcher” or “critic” replace a concrete input/output contract.
- **Shared mutable memory:** agents overwrite each other's state or treat notes as authority.
- **Delegated permission:** a handoff is mistaken for approval to use a secret or production target.
- **Consensus as proof:** several agents repeat the same unsupported claim.
- **Unbounded retries:** a failed worker relaunches without an attempt limit or recovery condition.
- **No integration proof:** each role passes locally, but the combined workflow lacks a target receipt.

## References

- [Create custom subagents](https://code.claude.com/docs/en/subagents)
- [NIST AI RMF: Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
