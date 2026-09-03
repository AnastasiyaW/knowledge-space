---
title: "Agent Deployment Patterns (September 2026)"
category: patterns
tags: [llm-agents, deployment, production, reliability, observability, rollout]
---

# Agent Deployment Patterns (September 2026)

Reviewed 2026-09-03. Deploy an agent as a versioned application workflow, not as a prompt attached to a model endpoint. A deployment must make its model configuration, tools, policies, state transitions, and evidence inspectable after a request has finished.

## Deployment Unit

| Part | Freeze and record | Why it matters |
|---|---|---|
| Application | Image or immutable source revision | Reproduces orchestration and validation behavior |
| Model | Provider, exact model/artifact identifier, decoding policy | Prevents accidental capability or cost drift |
| Prompt/config | Versioned template and runtime configuration | Makes output changes attributable |
| Tools | Manifest, scopes, timeouts, and approval policy | Keeps side effects bounded |
| Data | Retrieval corpus revision and access policy | Identifies what evidence the agent could read |
| Evaluation | Test set, rubric, and release threshold | Separates a new build from a verified build |

An image digest alone is insufficient when model aliases, prompts, tool definitions, or an index can change independently.

## Choose the Execution Lane

| Lane | Use when | Required contract |
|---|---|---|
| Synchronous request | A bounded answer is expected in the user interaction | Deadline, cancellation, response schema, and safe timeout message |
| Durable job | Work may outlive an HTTP request or involve several steps | Idempotency key, checkpoint, retry predicate, and terminal receipt |
| Approval hold | A tool can create a material external side effect | Named approver, immutable proposed action, expiry, and auditable decision |
| Scheduled batch | Inputs are known and processing can be delayed | Manifest, deduplication key, per-item state, and completion accounting |

Do not put long-running work behind a request handler merely because the first model call is quick. Persist state before invoking a retriable action.

## A Small Durable Work Item

```json
{
  "work_id": "news-2026-09-03-0042",
  "input_revision": "sha256:...",
  "agent_release": "2026-09-03.2",
  "state": "AWAITING_APPROVAL",
  "idempotency_key": "publish:news-2026-09-03-0042",
  "tool_manifest_revision": "tools-19",
  "checkpoint": "extract-complete",
  "evidence": ["source-17", "evaluation-run-82"]
}
```

`state` is application-owned. A model may propose a next action, but it must not directly set `SUCCEEDED`, approve itself, or erase the audit record.

## Failure and Retry Policy

Treat each error class differently:

1. **Invalid input or policy denial:** terminally reject with a user-safe reason; do not retry unchanged input.
2. **Provider/network transient:** retry only an idempotent operation within a bounded budget and retain the attempt record.
3. **Tool-side effect ambiguous:** reconcile using the idempotency key or provider receipt before any retry.
4. **Model output invalid:** run a deterministic repair/validation path or return a typed failure; do not silently reinterpret it as success.
5. **Process interruption:** resume from the last verified checkpoint, not from an inferred conversation transcript.

## Observability as a Release Requirement

One trace should let an operator answer: which release ran, what input/data revision it saw, what tools it requested, which actions were denied or approved, what retries occurred, and how the workflow reached its terminal state. Record opaque identifiers or redacted attributes rather than raw secrets and personal data.

GenAI semantic conventions provide a common vocabulary for model spans; they complement, rather than replace, business-level work-item and approval events. [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai)

## Rollout Contract

```text
candidate release
    -> deterministic and adversarial evaluation set
    -> isolated canary with trace + receipt inspection
    -> bounded rollout with rollback target
    -> production observation against explicit SLOs
```

Roll back the complete deployment unit. Switching only a model while retaining a changed tool policy or index revision makes the incident impossible to reconstruct.

## Gotchas

- **Issue: Calling an asynchronous agent endpoint "stateless."** The browser connection is stateless; the work is not. **Fix:** store a work item and checkpoint before any action that can be retried or resumed.
- **Issue: Retrying a side-effecting tool after a timeout.** The original request may have succeeded remotely. **Fix:** require a provider receipt or idempotency key before retrying.
- **Issue: Treating an LLM trace as an audit log.** Traces can omit policy decisions and must not store sensitive payloads blindly. **Fix:** emit separate structured events for authorization, approval, and terminal outcome.
- **Issue: Rolling forward a model alias without evaluation.** Alias movement can change output shape and tool behavior. **Fix:** pin the release identifier and re-run the release corpus before promotion.

## See Also

- [[production-patterns]]
- [[agent-observability-dashboards]]
- [[tool-use-patterns]]
- [[agent-evaluation]]

## Sources

- [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
