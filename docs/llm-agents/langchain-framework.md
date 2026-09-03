---
title: "LangChain Framework"
category: frameworks
tags: [llm-agents, langchain, agents, middleware, langgraph, observability]
description: "A version-aware guide to LangChain's current agent harness, provider integrations, middleware, state, and production boundaries."
---

# LangChain Framework

**Scope checked: 2026-09-03.** LangChain is now centred on `create_agent`: a configurable agent harness composed from a model, tools, a system prompt, and middleware. It is useful when an application needs that composition and provider portability; it is not required for a one-call model integration. [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)

## Choose the Right Layer

| Need | Prefer | Why |
|---|---|---|
| One model call or one stable tool call | Provider SDK | Smallest surface and clearest failure modes |
| Configurable tool-using harness | LangChain `create_agent` | Model, tools, prompt, and middleware are composed explicitly |
| Durable state machine, approvals, or mixed deterministic/agentic flow | LangGraph | Lower-level orchestration is designed for those control points |
| Traces, evaluation, and production diagnosis | LangSmith or equivalent | Observability is separate from the runtime contract |

Framework choice does not replace authorization, validation, or domain logic. Keep money movement, publication, access control, and irreversible effects in deterministic application code.

## Minimal Agent Contract

An agent is a model calling tools in a loop. A production harness needs an explicit contract for each layer:

| Layer | Declare | Verify |
|---|---|---|
| Model | provider, model identifier, timeout, retry policy | provider capability and error receipt |
| Tools | input schema, output schema, permission class, effect level | server-side validation and tool receipt |
| State | thread identity, checkpoint policy, retention | restore and cancellation test |
| Middleware | routing, guards, retries, context policy | deterministic test per policy |
| Observability | trace ID, model/tool versions, outcome | trace linked to terminal receipt |

Do not treat a provider-neutral interface as proof that all providers offer identical context windows, tool semantics, structured-output guarantees, or regional availability.

## Current Starting Point

```python
# pip install -U langchain "langchain[anthropic]"
from langchain.agents import create_agent
from langchain.tools import tool


@tool
def lookup_project(project_id: str) -> dict:
    """Return a public project record after server-side authorization."""
    return {"project_id": project_id, "status": "published"}


agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[lookup_project],
    system_prompt="Use tools only for public project records.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Show project happyin-space"}]}
)
```

The example intentionally keeps the tool small. The function must still authenticate the caller, validate the `project_id`, enforce scope, and return a structured error when the action is unavailable. The model should not receive a broad database credential merely because the tool is convenient.

## Middleware Is a Policy Boundary

Middleware can add routing, retry, tool policy, context management, and guardrails. Treat each addition as executable policy rather than decoration:

1. state the trigger and expected result;
2. name the owner of the policy and the version;
3. make the allow, deny, retry, and escalation paths observable;
4. test the policy with malformed input and unavailable dependencies;
5. keep a deterministic fallback only when it preserves the same safety guarantees.

For example, a retry wrapper may handle a transient model error. It must not silently replay a tool call that could publish, charge, delete, or send a message.

## State and Durable Work

LangChain agents are built on LangGraph, which provides durable execution, persistence, and human-in-the-loop support. That is useful for long-running work, but persistence changes the data contract: record what state is retained, who can restore it, and how an interrupted external effect is reconciled. [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)

Use a task record outside the model context:

```json
{
  "task_id": "research-044",
  "state": "awaiting_review",
  "input_revision": "source-set@2026-09-03",
  "allowed_actions": ["draft_article"],
  "approval_ref": null,
  "terminal_receipt": null
}
```

The runtime may summarize this record for the model, but the application remains the authority for transitions, approval, and the terminal receipt.

## Observability and Evaluation

Tracing can show prompts, tool calls, state transitions, latency, and errors. It does not prove that the output is correct. Pair traces with:

- a representative, versioned evaluation set;
- expected tool-call and refusal cases;
- quality measures tied to the task rather than token count;
- redaction and retention rules for prompts, tool inputs, and outputs;
- a review path for high-impact failures.

LangSmith documents tracing and evaluation for agents built with LangChain, LangGraph, and other frameworks. [LangSmith observability](https://docs.langchain.com/langsmith/observability)

## Gotchas

- **Old examples use deprecated chain and memory helpers.** They can still appear in search results. **Fix:** start from the current `create_agent` and provider-integration documentation, then pin the package versions you test.
- **A common model interface is not a common capability contract.** Providers differ in tool calling, limits, and error behavior. **Fix:** validate the selected model-provider pair in CI or a controlled canary.
- **Middleware can hide an effectful retry.** A model retry is not necessarily safe for an external action. **Fix:** put idempotency and reconciliation at the executor boundary.
- **Trace data can become a shadow data store.** Debug logs often contain prompts and tool outputs. **Fix:** classify, redact, restrict, and expire observability data.
- **State persistence is not a permission system.** Restoring a checkpoint must not restore expired authority. **Fix:** revalidate capabilities and approvals at effect time.

## Sources

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain agents](https://docs.langchain.com/oss/python/langchain/agents)
- [LangChain provider integrations](https://docs.langchain.com/oss/python/integrations/providers/overview)
- [LangSmith observability](https://docs.langchain.com/langsmith/observability)

## See Also

- [[langgraph]]
- [[agent-orchestration]]
- [[tool-use-patterns]]
- [[agent-safety-alignment]]
- [[llmops]]
