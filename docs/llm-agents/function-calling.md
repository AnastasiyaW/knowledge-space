---
title: "Function Calling and Tool Use (September 2026)"
category: techniques
tags: [llm-agents, function-calling, tool-use, schemas, validation]
---

# Function Calling and Tool Use (September 2026)

Reviewed 2026-09-03. Function calling is a contract: a model emits a structured request, the application validates and executes it, and the result returns to the model or workflow. The model does not receive authority to execute an action merely by naming a function.

## The Contract

```text
user request
    -> model selects a declared tool
    -> application validates name, schema, policy, and approval
    -> application executes or rejects the call
    -> structured result becomes the next model/workflow input
```

| Field | Requirement |
|---|---|
| Tool name | Stable, unique, and allowlisted |
| Arguments | Typed schema with constraints and examples where ambiguity matters |
| Caller | Run ID, agent version, and tool-policy identity |
| Deadline | Bounded execution time and cancellation behavior |
| Result | Structured success or error envelope |
| Side effect | Explicit approval and idempotency key when material |

The same application-owned loop appears across provider APIs. Claude documents client tool calls as a model request followed by application execution and a tool result; Gemini documents the same responsibility for function execution. [Claude tool-use contract](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) [Gemini function calling](https://ai.google.dev/gemini-api/docs/function-calling)

## A Minimal Safe Dispatcher

This Python 3.11+ example keeps validation and authority outside the model response.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    payload: dict[str, Any]


def get_weather(city: str, units: str = "celsius") -> ToolResult:
    if units not in {"celsius", "fahrenheit"}:
        return ToolResult(False, {"error": "unsupported_units"})
    return ToolResult(True, {"city": city, "units": units, "temperature": 20})


TOOLS = {"get_weather": get_weather}


def dispatch(call: dict[str, Any]) -> ToolResult:
    name = call.get("name")
    arguments = call.get("arguments")
    if name not in TOOLS:
        return ToolResult(False, {"error": "tool_not_allowed"})
    if not isinstance(arguments, dict):
        return ToolResult(False, {"error": "invalid_arguments"})
    city = arguments.get("city")
    units = arguments.get("units", "celsius")
    if not isinstance(city, str) or not city:
        return ToolResult(False, {"error": "city_required"})
    if not isinstance(units, str):
        return ToolResult(False, {"error": "invalid_units"})
    return TOOLS[name](city=city, units=units)


if __name__ == "__main__":
    print(dispatch({"name": "get_weather", "arguments": {"city": "Paris"}}))
```

In production, replace the example result with a bounded service call and add authentication, audit logging, idempotency, and domain-specific schema validation.

## Tool Definition Rules

| Rule | Why |
|---|---|
| Describe when to use and when not to use a tool | Prevents overlapping descriptions from producing arbitrary selection |
| Keep schemas narrow | Makes validation, policy, and review feasible |
| Return machine-readable errors | Lets the model recover without parsing prose |
| Separate read from write tools | Allows different authorization policies |
| Bind tool access to a phase or task | Avoids exposing unused capabilities |
| Version a breaking schema change | Existing prompts and clients may rely on the old shape |

Use structured output for a final answer that must match a schema. Use function calling when the model needs an intermediate interaction with an application-owned capability. They solve different stages of a workflow.

## Execution Policy

```json
{
  "tool_policy_id": "research-readonly-v2",
  "allowed_tools": ["search_sources", "read_document"],
  "requires_approval": ["publish_article", "send_email"],
  "timeout_ms": 15000,
  "idempotency_scope": "run_id:tool_call_id"
}
```

Do not express this policy only in a system prompt. Enforce it in the dispatcher or gateway that performs the action.

## Parallel Calls and Retries

Parallel calls are safe only when the operations are independent and their result ordering is defined. A retry of an external write must reuse the idempotency key and reconcile any uncertain first attempt before sending another request.

## Gotchas

- **Issue: Calling a tool name supplied by the model without an allowlist.** A model response is untrusted input. **Fix:** resolve names through a server-side registry and reject unknown tools.
- **Issue: Treating schema validation as authorization.** Valid arguments can still request an impermissible action. **Fix:** evaluate identity, policy, approval, and budget separately from argument shape.
- **Issue: Returning free-text errors.** The next model turn may invent a recovery path. **Fix:** return stable error codes, retryability, and a safe next action.
- **Issue: Retrying writes after a timeout.** The original call may have succeeded. **Fix:** persist an idempotency key and query the external receipt first.

## See Also

- [[tool-use-patterns]]
- [[agent-orchestration]]
- [[agent-security]]
- [[llm-api-integration]]

## Sources

- [Claude: How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Claude: Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools)
- [Gemini API: Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [OpenAI Agents SDK: Tools](https://openai.github.io/openai-agents-js/guides/tools/)
