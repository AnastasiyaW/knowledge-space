---
title: "Multi-Agent Messaging and Coordination"
description: "Choose the right boundary for agent-to-agent work, tool access, durable messages, receipts, and concurrent repository changes."
tags: [llm-agents, multi-agent, messaging, a2a, mcp, coordination, observability]
---

# Multi-Agent Messaging and Coordination (September 2026)

Version context: agent runtimes, IDE features, protocol revisions, and transport adapters evolve quickly. This page describes durable coordination contracts rather than claiming a particular client flag, plugin, broker, polling interval, or experimental feature is universal.

Communication is only one part of coordination. A reliable system distinguishes a message from a task state, an authority decision, a shared artifact, and an exclusive lock. Treating all of them as chat text makes duplicate execution and unverifiable completion likely.

## Choose the Correct Boundary

| Need | Appropriate primitive | What it does not prove |
|---|---|---|
| An agent needs a tool, API, or data resource | MCP client/server boundary | that another independent agent accepted a task |
| An agent delegates an objective to an independent agent | A2A or an application task protocol | that a side effect completed safely |
| Two local sessions share project knowledge | versioned artifact, handoff, or repository reference | exclusive ownership of a mutable resource |
| Exactly one worker may mutate a resource | lease or lock with external reconciliation | durable delivery of a message |
| A reviewer needs evidence | immutable receipt linked from the task | that a sender's description was correct |

The current A2A documentation describes A2A as agent-to-agent communication and MCP as agent-to-tool communication. They are complementary: an agent can use MCP tools while collaborating with another agent through A2A. [A2A Protocol](https://a2a-protocol.org/latest/)

MCP itself uses a host-client-server architecture. The host manages connections, policy, consent, and user authorization; an MCP server does not automatically grant a remote agent authority over a user's resources. [MCP architecture](https://modelcontextprotocol.io/specification/latest/architecture)

## A Durable Message Envelope

Use a typed envelope with an idempotency key, routing metadata, expiry, and references to controlled artifacts. Do not place credentials, unrestricted instructions, or raw private context into the envelope.

```json
{
  "schema_version": "agent-message/v1",
  "message_id": "msg_01...",
  "trace_id": "tr_01...",
  "idempotency_key": "research:source-set-44:v1",
  "sender": {"agent_id": "researcher@release-12", "role": "research"},
  "recipient": {"queue": "editorial-review", "role": "review"},
  "intent": "review_claim_set",
  "allowed_actions": ["read_artifact", "write_review_receipt"],
  "input_refs": ["artifact:claim-set-44"],
  "expires_at": "2026-09-04T12:00:00Z",
  "sent_at": "2026-09-03T12:00:00Z"
}
```

The receiver validates schema, identity, expiry, allowed actions, and artifact access before it accepts work. The sender never gets to grant permissions merely by writing them into a message.

## Model the Task Separately from Delivery

A transport acknowledgement means only that a message reached a transport. It is not evidence that the recipient read it, had authority, completed it, or produced a valid result.

Track task state and verification separately. A task has mutually exclusive terminal states; verification is a review of the terminal receipt, not another task transition.

```text
non-terminal task states: PENDING -> ACCEPTED -> RUNNING
terminal task state: COMPLETED | FAILED | CANCELLED
verification receipt: PENDING -> VERIFIED | REJECTED
```

Every task transition carries an appropriate receipt. A terminal task state requires a terminal receipt:

- **ACCEPTED:** receiver identity, accepted scope, deadline, and task revision;
- **COMPLETED:** output artifact reference, validation result, and no-side-effect or side-effect receipt;
- **FAILED:** classified error, retryability, preserved evidence, and next safe action;
- **CANCELLED:** actor, reason, and reconciliation outcome for any in-flight effect;
- **Verification receipt:** independent criteria version, reviewer identity, and verdict.

Cancellation may occur from any non-terminal state. When a message might lead to a payment, publication, deployment, or other external effect, the effect needs its own application-level authorization and idempotency key.

## Transport Choices

| Transport | Good fit | Contract to add yourself |
|---|---|---|
| Append-only files | local, auditable handoffs and asynchronous research | atomic write, schema validation, expiry, processed receipt |
| Queue or database | retries, backpressure, many workers | deduplication, lease, dead-letter policy, terminal task record |
| A2A endpoint | interoperable delegation between independent agent systems | application authorization, local work ledger, effect controls |
| Direct process call | bounded in-process subtask | timeout, cancellation, result validation, parent receipt |

Start with the smallest transport that preserves the needed evidence. A repository-backed artifact is often stronger than a real-time message for research, planning, or review because it gives every recipient the same versioned input.

## Treat Received Content as Untrusted Input

An agent message, retrieved file, tool result, or issue comment can contain instructions that conflict with the recipient's policy. A receiver should:

1. parse the envelope without executing its free text;
2. resolve artifact references through an access-controlled store;
3. apply its own task and authorization policy;
4. restrict tools to the declared and locally approved action set;
5. validate output against the task contract;
6. write a terminal receipt before notifying the sender.

This makes delegation a controlled interface rather than a prompt-injection tunnel.

## Coordinate Concurrent Repository Work

For code or documentation changes, assign one writer to a path or feature boundary. Use a dedicated branch and worktree per writer, then exchange only commit references, review artifacts, and scoped change requests. Git worktrees are designed to provide multiple working trees attached to one repository. [git-worktree](https://git-scm.com/docs/git-worktree)

A concise handoff should identify:

```text
objective + scope + base commit + branch + changed paths
+ verification commands + receipts + known gaps + owner
```

A shared chat transcript is not an integration artifact. It has no immutable base revision, no merge semantics, and no guarantee that a later reader sees the correct input.

## Observability

Give every message, task, and result a shared trace ID. Measure queue age, acceptance delay, execution duration, retries, schema failures, authorization denials, and verified terminal outcomes. Do not measure only message throughput: a fast queue that loses receipts is not a successful coordination system.

## Gotchas

- **Delivery is not completion.** A broker acknowledgement says nothing about the recipient's work. **Fix:** require an accepted state and a separate terminal receipt.
- **A lock is not a message queue.** It can exclude concurrent writers but cannot preserve a task description or result. **Fix:** keep locks, messages, and task records as separate primitives.
- **A sender cannot delegate authority it does not own.** A message's declared permissions are only a request. **Fix:** authorize independently at the receiver and at every effectful tool boundary.
- **Polling intervals are not reliability guarantees.** A process can be asleep, dead, or reading stale state. **Fix:** use durable state, expiry, and reconciliation rather than timing assumptions.
- **Full context dumps are an access-control failure.** They spread private material and make relevance harder to audit. **Fix:** send narrow artifact references with provenance and a policy-controlled reader.

## Sources

- [A2A Protocol](https://a2a-protocol.org/latest/)
- [Model Context Protocol architecture](https://modelcontextprotocol.io/specification/latest/architecture)
- [Git worktree documentation](https://git-scm.com/docs/git-worktree)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## See Also

- [[multi-session-coordination]]
- [[agent-orchestration]]
- [[agent-design-patterns]]
- [[agent-security]]
- [[agent-observability-dashboards]]
- [[llmops]]
