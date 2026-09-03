---
title: "Tool Use Patterns (September 2026)"
category: patterns
tags: [llm-agents, tool-use, function-calling, mcp, authorization, observability]
---

# Tool Use Patterns (September 2026)

Reviewed 2026-09-03. A tool is an application capability exposed to a model through a schema. Design it as an API with authorization, validation, timeouts, audit records, and explicit failure semantics—not as an extra paragraph in a prompt.

## Tool Manifest

```json
{
  "name": "search_sources",
  "version": "v2",
  "purpose": "Read approved public sources for a research run.",
  "input_schema": {"type": "object"},
  "access": "read_only",
  "timeout_ms": 15000,
  "idempotency": "not_required",
  "result_schema": "source-results/v1",
  "owner": "research-platform"
}
```

Every field above is application policy. A model can request the declared capability, but the gateway decides whether the call is allowed.

## Design Patterns

| Pattern | Use when | Required safeguard |
|---|---|---|
| Read-only search/retrieval | Model needs current or proprietary information | Source allowlist and citation/reference output |
| Scoped write | Model proposes an approved draft or record update | Approval state, idempotency, and audit receipt |
| Phase-specific toolset | Workflow stages need different capabilities | Controller selects the phase; model cannot widen it |
| Tool search | A large catalog would consume context | Discovery policy and explicit selected-tool review |
| MCP integration | Tools are provided by a separate server | Host-owned permissions and server trust review |

MCP uses a host-client-server architecture where the host controls client lifecycle and permissions. [MCP Architecture](https://modelcontextprotocol.io/specification)

## Result Envelope

Return an envelope that lets the next step distinguish a result from a failure without parsing prose.

```python
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ToolEnvelope:
    status: str
    data: dict[str, Any]
    error_code: str | None = None
    retryable: bool = False


def read_document(document_id: str) -> ToolEnvelope:
    if document_id != "allowed-001":
        return ToolEnvelope(
            status="error",
            data={},
            error_code="document_not_allowed",
            retryable=False,
        )
    return ToolEnvelope(status="ok", data={"document_id": document_id, "text": "..."})


if __name__ == "__main__":
    print(asdict(read_document("allowed-001")))
```

For side-effecting tools, include a caller/run identity and durable external receipt reference in addition to this envelope.

## Tool Selection

Descriptions should state:

- the user outcome the tool enables;
- the input format and valid ranges;
- what it returns;
- when it should not be used;
- whether it reads, writes, or triggers an external action.

Anthropic documents that tool definitions and accumulated tool results consume context, and recommends selecting a context-management method that matches the source of pressure. [Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)

## Failure and Recovery

| Failure | Safe behavior |
|---|---|
| Unknown tool | Reject without execution |
| Schema mismatch | Return a stable validation error |
| Permission denied | Return denial; do not suggest a bypass |
| Timeout on read | Mark retryable and bound retry budget |
| Timeout on write | Mark outcome unknown; reconcile receipt before retry |
| Partial external result | Preserve receipt/reference and hold for reconciliation |

## Gotchas

- **Issue: Giving every tool to every agent.** More tools create ambiguity, cost, and attack surface. **Fix:** expose the smallest task-specific allowlist.
- **Issue: Using one generic search or execute tool.** The model and operator cannot tell which policy applies. **Fix:** make purpose, authority, inputs, and outputs explicit.
- **Issue: Silently falling back after a failure.** A different tool or provider may change data handling or side effects. **Fix:** register each fallback with trigger, equivalent guarantee, and visible signal.
- **Issue: Treating an MCP server as inherently trusted.** Protocol interoperability does not validate a server behavior. **Fix:** review server identity, permissions, data flow, and tool schema before exposure.

## See Also

- [[function-calling]]
- [[agent-security]]
- [[agent-orchestration]]
- [[agent-observability-dashboards]]

## Sources

- [Model Context Protocol Architecture](https://modelcontextprotocol.io/specification)
- [Claude: Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Claude: Manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context)
- [OpenAI Agents SDK: Tools](https://openai.github.io/openai-agents-js/guides/tools/)
