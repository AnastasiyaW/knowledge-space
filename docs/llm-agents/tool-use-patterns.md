---
title: Tool Use Patterns
category: patterns
tags: [llm-agents, tool-use, function-calling, api, mcp, tool-design]
---

# Tool Use Patterns

How to design, expose, and manage tools for LLM agents. Tool quality directly determines agent reliability - vague tool descriptions and poor error handling cause most agent failures.

## Tool Definition Best Practices

### Clear, Specific Descriptions

```python
# BAD: vague, model has to guess
tools = [{
    "name": "search",
    "description": "Search for stuff",
    "parameters": {"query": {"type": "string"}}
}]

# GOOD: specific, with examples and constraints
tools = [{
    "name": "search_products",
    "description": "Search product catalog by name, category, or SKU. "
                   "Returns up to 10 matching products with price and availability. "
                   "Use for: finding specific items, checking stock, comparing prices. "
                   "Do NOT use for: order status, customer info, analytics.",
    "parameters": {
        "query": {
            "type": "string",
            "description": "Product name, category, or SKU code (e.g., 'wireless headphones', 'SKU-12345')"
        },
        "max_results": {
            "type": "integer",
            "description": "Maximum results to return (1-50, default 10)",
            "default": 10
        },
        "in_stock_only": {
            "type": "boolean",
            "description": "If true, only return items currently in stock",
            "default": False
        }
    }
}]
```

### Tool Result Formatting

Return structured, parseable results. Include error context.

```python
def execute_tool(name, params):
    try:
        result = tool_registry[name](**params)
        return {
            "status": "success",
            "data": result,
            "metadata": {"execution_time_ms": elapsed, "result_count": len(result)}
        }
    except ToolError as e:
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e),
            "suggestion": e.recovery_hint  # help agent recover
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": "unexpected",
            "message": f"Tool '{name}' failed: {str(e)}"
        }
```

## Tool Selection Patterns

### Toolkit Scoping

Don't give agent 50 tools at once. Scope by task phase:

```python
# Phase-based tool availability
TOOL_PHASES = {
    "research": ["web_search", "read_document", "query_database"],
    "analysis": ["run_python", "create_chart", "statistical_test"],
    "writing": ["write_document", "format_table", "spell_check"],
    "review": ["diff_compare", "validate_schema", "run_tests"],
}

def get_tools_for_phase(phase):
    return [tool_registry[t] for t in TOOL_PHASES[phase]]
```

### Fallback Chains

When primary tool fails, try alternatives:

```python
async def search_with_fallback(query):
    # Try primary source
    result = await web_search(query)
    if result.status == "success" and result.data:
        return result

    # Fallback to alternative
    result = await cached_search(query)
    if result.status == "success":
        return result

    # Final fallback
    return await knowledge_base_search(query)
```

### Confirmation for Destructive Actions

```python
DESTRUCTIVE_TOOLS = {"delete_file", "send_email", "execute_sql_write", "deploy"}

def should_confirm(tool_name, params):
    if tool_name in DESTRUCTIVE_TOOLS:
        return True
    if tool_name == "execute_sql" and not params.get("query", "").upper().startswith("SELECT"):
        return True
    return False
```

## MCP (Model Context Protocol)

Standard protocol for connecting LLMs to external tools and data sources:

```python
# MCP server exposes tools
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-tools")

@server.tool()
async def get_weather(city: str) -> list[TextContent]:
    """Get current weather for a city."""
    data = await fetch_weather_api(city)
    return [TextContent(type="text", text=f"Weather in {city}: {data['temp']}F, {data['condition']}")]

# MCP client consumes tools
from mcp.client import ClientSession

async with ClientSession(transport) as session:
    tools = await session.list_tools()
    result = await session.call_tool("get_weather", {"city": "Berlin"})
```

**MCP advantages**: standardized tool interface, tool discovery, transport-agnostic (stdio, HTTP, SSE), security boundaries between tool servers.

## Parallel Tool Execution

When tools are independent, run them concurrently:

```python
import asyncio

async def parallel_tool_calls(tool_calls):
    # Group independent calls
    independent = [tc for tc in tool_calls if not tc.depends_on]
    dependent = [tc for tc in tool_calls if tc.depends_on]

    # Execute independent calls in parallel
    results = {}
    parallel_results = await asyncio.gather(*[
        execute_tool(tc.name, tc.params) for tc in independent
    ])
    for tc, result in zip(independent, parallel_results):
        results[tc.id] = result

    # Execute dependent calls sequentially
    for tc in dependent:
        dep_results = {d: results[d] for d in tc.depends_on}
        results[tc.id] = await execute_tool(tc.name, {**tc.params, **dep_results})

    return results
```

## Rate Limiting and Cost Control

```python
import time
from collections import defaultdict

class ToolRateLimiter:
    def __init__(self):
        self.call_counts = defaultdict(int)
        self.cost_tracker = 0.0
        self.limits = {
            "web_search": {"max_calls": 20, "cost_per_call": 0.01},
            "run_code": {"max_calls": 50, "cost_per_call": 0.001},
            "send_email": {"max_calls": 5, "cost_per_call": 0.0},
        }

    def check(self, tool_name):
        limit = self.limits.get(tool_name, {"max_calls": 100, "cost_per_call": 0})
        if self.call_counts[tool_name] >= limit["max_calls"]:
            raise RateLimitError(f"{tool_name} limit reached ({limit['max_calls']} calls)")
        if self.cost_tracker > 1.0:  # $1 budget cap
            raise BudgetError("Tool execution budget exceeded")

    def record(self, tool_name):
        self.call_counts[tool_name] += 1
        self.cost_tracker += self.limits.get(tool_name, {}).get("cost_per_call", 0)
```

## Gotchas

- **Tool descriptions are prompt engineering**: the model decides which tool to call based solely on the description string. Ambiguous descriptions cause wrong tool selection. Include explicit "use for" / "do NOT use for" examples. Test with adversarial queries that might confuse similar tools
- **Large tool results overflow context**: a database query returning 10,000 rows or a web page with 50KB of text fills the context window. Always truncate/summarize tool results before returning to the agent. Set max_tokens on tool outputs and paginate large results
- **Missing error recovery causes agent death spirals**: agent calls tool, gets error, retries same call, gets same error, repeats until token limit. Tool errors must include recovery hints (different parameters, alternative tool, skip this step). Agent must track failed attempts

## See Also

- [[function-calling]]
- [[agent-design-patterns]]
- [[agent-architectures]]
- [[rag-pipeline]]
