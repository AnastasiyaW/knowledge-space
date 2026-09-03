---
title: "LLM API Integration"
description: "Build provider integrations around typed contracts, secure configuration, explicit state, retries, and observable release gates."
tags: [llm-agents, api, openai, anthropic, streaming, function-calling, llmops]
---

# LLM API Integration (September 2026)

Version context: model IDs, endpoints, response shapes, rate limits, retention options, tool semantics, and pricing change independently. Keep them in reviewed configuration and validate the exact provider contract at deployment time. This page uses no static price table or permanent model recommendation.

A production LLM integration is an application boundary, not a single SDK call. It needs typed inputs and outputs, identity and data controls, model configuration, timeouts, retry semantics, usage telemetry, and a way to reproduce or roll back a behavior change.

## Start with a Provider-Neutral Contract

Keep application logic independent from an SDK response object.

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    task_id: str
    model_key: str
    input_text: str
    max_output_tokens: int


@dataclass(frozen=True)
class LLMResult:
    text: str
    provider_request_id: str
    model_revision: str
    usage: dict[str, int]
    finish_state: str


class LLMProvider(Protocol):
    def complete(self, request: LLMRequest) -> LLMResult: ...
```

The adapter owns provider-specific request construction, streaming events, tool-call loops, errors, and usage extraction. The application owns authorization, business validation, idempotency, and user-visible policy.

## Secure Configuration

Use a secret manager, workload identity, or environment injection managed by the deployment system. Do not put API keys in source files, browser code, screenshots, documents, prompts, logs, or model-accessible tools.

Keep configuration separate from code:

```json
{
  "provider": "approved_provider",
  "model_key": "support_triage_v4",
  "model_id": "reviewed-at-deploy",
  "timeout_seconds": 45,
  "max_output_tokens": 300,
  "data_policy_revision": "policy@12",
  "tool_policy_revision": "tools@7"
}
```

A model key lets the application request a reviewed capability while deployment configuration maps it to a currently approved provider model. Record the resolved model revision in the result receipt.

## OpenAI Responses API

The current OpenAI Responses API accepts text, image, and file inputs, exposes status and usage data, and can return tool calls. Use the SDK convenience field for text only after checking terminal status.

```python
import os
from openai import OpenAI


def run_openai(prompt: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=os.environ["OPENAI_MODEL"],
        input=prompt,
        max_output_tokens=300,
    )
    if response.status != "completed":
        raise RuntimeError(f"response did not complete: {response.status}")
    return response.output_text
```

Do not hard-code a model name into a reusable article or application module. Restrict the environment variable to an approved allowlist in deployment configuration.

## Anthropic Messages API

The Messages API accepts a structured conversation and generates the next message. Keep the conversation state in an application-owned record when your product needs reproducibility, retention controls, or cross-provider portability.

```python
import os
import anthropic


def run_anthropic(prompt: str) -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=os.environ["ANTHROPIC_MODEL"],
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(
        block.text for block in message.content if block.type == "text"
    )
```

Provider response blocks can include more than visible text. Preserve the typed response until policy and tool handling are complete; do not assume the first content block is the only result.

## State Is a Product Decision

Different APIs offer different conversation and retention mechanisms. OpenAI Responses can link calls through a conversation or previous response identifier; the Anthropic Messages API can be used with an explicit message list. A generic adapter should not treat either behavior as a universal memory model.

For every request, record:

- application conversation or task ID;
- configuration and model revision;
- input/content policy classification;
- provider request/response identifiers;
- tool-call and approval decisions;
- terminal status, usage, and retry count;
- redacted trace reference and retention policy.

This gives an operator a reproducible task boundary without retaining more content than policy permits.

## Streaming Needs an Event Contract

Provider streams are event sequences, not simply text chunks. Route them through a parser that recognizes start, delta, tool-input, usage, error, completion, and cancellation events.

```text
stream event -> provider parser -> typed application event
             -> validation / UI update -> durable terminal receipt
```

Do not execute a tool from a partial JSON fragment. Accumulate and validate a complete tool input, authorize it on the server, run it with an idempotency key, then return a structured tool result. Some providers deliberately allow fine-grained tool streaming where JSON can be incomplete while it is arriving.

## Structured Output and Tool Calls

Use schemas at both boundaries:

1. Give the model a narrow output or tool schema.
2. Parse with a real JSON/schema validator.
3. Check business invariants, tenant scope, and authorization in application code.
4. Bind credentials to the action being performed, not to the model process broadly.
5. Return a typed error or correction request; never silently coerce an unsafe value.
6. Store a receipt that identifies the policy and schema revisions.

A valid JSON object is not automatically a valid business action.

## Retries, Idempotency, and Rate Limits

Retry only failures that are known safe to retry. Use bounded exponential backoff with jitter for transient network, capacity, or rate-limit failures according to the provider's current guidance. Do not repeat an external side effect merely because an LLM response is missing.

For an effectful workflow, create the idempotency key before the provider call and preserve it through tool execution:

```json
{
  "task_id": "invoice-summary-003",
  "idempotency_key": "task:invoice-summary-003:v1",
  "effect": "send_draft_only",
  "retry_budget": 3,
  "terminal_state": "pending"
}
```

Use a queue or background job for long-running requests. A browser connection closing is not proof that the underlying task has failed or succeeded.

## Observability and Cost Control

Track provider-reported usage, latency, status, errors, model revision, cache signals where available, tool-call count, and task outcome. Tie alerts to user-visible failures and approved budgets, not a hard-coded price copied from a past release.

Test each provider adapter with:

- an ordinary response and an incomplete/error response;
- a timeout and a bounded retry;
- structured-output violation;
- partial stream or partial tool input;
- duplicate delivery of the same task;
- cross-tenant or unauthorized tool request;
- a model/configuration switch with the release evaluation suite.

## Gotchas

- **SDK objects are provider-specific.** Directly leaking them into application code makes migration and testing fragile. **Fix:** normalize into a small internal result contract.
- **A conversation ID is not a data-retention policy.** Provider state and application state can have different retention semantics. **Fix:** define where history lives and what is deleted or redacted.
- **Partial stream data is not executable input.** Tool JSON can be incomplete or invalid while streaming. **Fix:** buffer, parse, validate, authorize, then execute.
- **Retries can duplicate side effects.** A timeout does not prove the first request failed. **Fix:** use idempotency keys and reconcile terminal state.
- **Static price examples decay quickly.** Costs depend on model, tier, cache behavior, and output. **Fix:** use provider-reported usage and current pricing at planning time.

## Sources

- [OpenAI Responses API reference](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [Anthropic Messages API reference](https://platform.claude.com/docs/en/api/messages/create)
- [Anthropic streaming messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Anthropic fine-grained tool streaming](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming)

## See Also

- [[prompt-engineering]]
- [[function-calling]]
- [[tokenization]]
- [[llmops]]
- [[frontier-models]]
- [[agent-security]]
