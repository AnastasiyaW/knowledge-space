---
title: "Claude Managed Agents"
description: "A version-aware guide to Anthropic's managed agent harness: agent configuration, environments, sessions, events, permission policies, and data boundaries."
tags: [llm-agents, claude, managed-agents, sandboxes, permissions, orchestration]
---

# Claude Managed Agents

**Scope checked: 2026-09-03.** Claude Managed Agents is Anthropic's beta managed harness for long-running, asynchronous agent work. It provides the agent loop, environments, tool execution, persisted event history, and session lifecycle; the application still owns its business authorization, approval decisions, and release criteria. [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)

## What Is Managed

| Concept | Current meaning | Application responsibility |
|---|---|---|
| Agent | model, system prompt, tools, MCP servers, skills | version and review the configuration |
| Environment | Anthropic cloud sandbox or self-hosted sandbox configuration | select data-residency and network boundary |
| Session | running agent instance for a task | create, steer, interrupt, reconcile outcomes |
| Events | messages, tool results, status and progress records | consume the authoritative event stream |

Managed infrastructure reduces runtime assembly work. It does not make a tool call authorized, a result factually correct, or a publication safe to release.

## Lifecycle Contract

```text
versioned agent + reviewed environment
          -> create session
          -> send user event
          -> stream authoritative events
          -> approval / denial / interrupt as required
          -> reconcile external effects
          -> terminal receipt
```

The platform supports persisted session history and outputs, server-sent event streaming, and mid-execution steering or interruption. A UI preview is not the record: use persisted session events and an application receipt to decide whether a task really finished. [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## Minimum Configuration

Start from an explicit, least-privilege definition:

```yaml
name: Editorial Research Agent
model:
  id: claude-opus-5
system: Draft from approved public sources. Do not publish.
tools:
  - type: agent_toolset_20260401
    default_config:
      permission_policy:
        type: always_ask
```

The current API is beta and requires the `managed-agents-2026-04-01` beta header; supported SDKs add it automatically. Pin the SDK and test its current request shape before deploying. [Managed Agents quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)

## Permission Policy Is Not Access Control

Permission policies decide whether server-executed tools run immediately or pause for approval:

| Policy | Result |
|---|---|
| `always_allow` | enabled server tool executes without confirmation |
| `always_ask` | session pauses until the application returns allow or deny |

The pre-built agent toolset defaults to `always_allow`; MCP toolsets default to `always_ask`. Custom tools run in the application and therefore need their own authorization layer. Running sessions retain the tool configuration they were created with, so a policy change affects only later sessions unless the application explicitly handles migration. [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)

For a public-content workflow, use a narrow split:

| Stage | Capability | Default |
|---|---|---|
| Research | read approved sources, create structured notes | allowed |
| Draft | create revision proposal | allowed |
| Review | inspect sources and draft | allowed |
| Publish | create a public effect | deny until a concrete approval event |
| Recovery | inspect task and receipt | allowed, no new effect |

An approval UI must identify the exact tool call, arguments, target account, and expiry. “The agent was approved earlier” is not enough evidence for a new publication.

## Environment and Data Boundary

Choose a cloud sandbox only after documenting:

- network allowlist and egress policy;
- file, repository, and artifact mounts;
- which credentials are available to the session;
- data classification and retention;
- whether a self-hosted sandbox is required for residency or compliance;
- how uploaded files and session data will be deleted.

Managed Agents sessions are intentionally stateful. Anthropic documents that this feature is not eligible for Zero Data Retention or HIPAA BAA coverage at the current beta stage; assess that boundary before putting sensitive corpus or learner data in a session. [Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)

## Event Handling

Consume events as a state machine, not as chat text:

1. persist the session ID, task ID, expected inputs, and current policy revision;
2. send the task as a `user.message` event;
3. stream status, agent, and tool events;
4. when an `always_ask` action pauses, inspect the concrete request and send an allow or deny event;
5. on interruption, wait for the recorded idle transition;
6. reconcile any external effect before assigning a terminal state.

The platform's preview deltas are for display only; its buffered persisted event is the authoritative record. [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## When It Fits

Choose Managed Agents when the task benefits from a managed environment, multiple tool calls over minutes or hours, persisted sessions, or scheduled execution. Use the Messages API or a local harness when the application needs full control of the loop, environment, data path, and every tool executor.

## Gotchas

- **The agent toolset is permissive by default.** Its default is `always_allow`. **Fix:** configure `always_ask` or disable unnecessary tools before creating each production agent version.
- **An MCP approval is not application authorization.** A user can approve a tool yet lack authority for the business action. **Fix:** validate tenant, target, scope, and approval at the downstream executor.
- **A session going idle is not proof of success.** It can be waiting for confirmation, interrupted, or unable to reconcile a side effect. **Fix:** require a domain terminal receipt.
- **Stateful sessions retain more than a prompt.** History, sandbox state, and outputs are part of the data boundary. **Fix:** classify data, define retention, and verify deletion operations.
- **Beta surfaces evolve.** A copied quickstart may drift. **Fix:** pin dependencies, cite the current beta header, and run a controlled canary after changes.

## Sources

- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Claude Managed Agents quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
- [Permission policies](https://platform.claude.com/docs/en/managed-agents/permission-policies)
- [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming)

## See Also

- [[agent-orchestration]]
- [[agent-safety-alignment]]
- [[tool-use-patterns]]
- [[multi-agent-messaging]]
- [[llmops]]
