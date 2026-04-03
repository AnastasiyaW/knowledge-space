---
title: Function Calling and Tool Use
category: techniques
tags: [llm-agents, function-calling, tool-use, openai-tools, anthropic-tools, api]
---

# Function Calling and Tool Use

Function calling enables LLMs to output structured tool invocations instead of free text. The model does not execute functions - it generates a JSON object describing which function to call and with what arguments. Your code executes the function and feeds the result back.

## Key Facts
- Function calling is more reliable for structured output than asking for JSON in a prompt
- The model chooses tools based on their descriptions - description quality directly affects tool selection accuracy
- Models can request multiple tool calls in parallel in a single response
- Tool results are fed back as messages, creating a multi-turn tool-use conversation

## Patterns

### OpenAI Function Calling

**Define tools:**
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city. Use when user asks about weather, temperature, or rain.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g., 'Paris'"},
                    "units": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["city"]
            }
        }
    }
]
```

**Call with tools:**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = execute_function(name, args)
        # Feed result back
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })
    # Get final response with tool results
    final = client.chat.completions.create(
        model="gpt-4", messages=messages, tools=tools
    )
```

**tool_choice options:**

| Value | Behavior |
|-------|----------|
| `"auto"` | Model decides whether to call a function |
| `"none"` | Never call functions (text only) |
| `"required"` | Must call at least one function |
| `{"type": "function", "function": {"name": "..."}}` | Force specific function |

### Anthropic Tool Use

```python
response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }],
    messages=[{"role": "user", "content": "Weather in Paris?"}]
)

for block in response.content:
    if block.type == "tool_use":
        result = execute_function(block.name, block.input)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": block.id, "content": str(result)}]
        })
```

### LangChain Tools

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the company database for relevant records.

    Args:
        query: Search query string
        limit: Maximum number of results (default 10)
    """
    results = db.search(query, limit=limit)
    return json.dumps(results)
```

## Tool Description Best Practices

**Bad**: `"Does stuff with weather"`
**Good**: `"Get current weather conditions including temperature, humidity, and precipitation probability for a specific city. Use when the user asks about weather, temperature, or if they should bring rain gear."`

Include in parameter descriptions:
- What the parameter means
- Expected format/values
- Constraints (min/max, enum options)
- Default behavior if omitted

## Tool Calling Patterns

- **Sequential**: each tool result informs the next (search -> get ID -> query details)
- **Conditional**: model picks tool based on context (weather API vs finance API)
- **Parallel**: model requests multiple tools simultaneously for independent queries
- **Composition**: chain tools where each output feeds the next

## Validation

Before executing tool calls, validate:
- Function name exists in available tools
- Required parameters are present
- Parameter types are correct
- Values are within expected ranges
- No injection attacks in string parameters

## Gotchas
- Tool descriptions are the primary way the model decides which tool to use - invest time in writing clear, specific descriptions
- Models can generate malformed JSON arguments - always wrap `json.loads` in try/except
- Smaller/local models are less reliable at function calling than GPT-4 or Claude
- Each tool call round-trip costs tokens (request + response + tool result + final response)
- Long tool result strings consume context window - truncate verbose outputs

## See Also
- [[agent-fundamentals]] - How tools fit into the ReAct agent loop
- [[langchain-framework]] - LangChain tool abstractions
- [[llm-api-integration]] - API setup for tool-enabled calls
- [[agent-security]] - Validating tool calls for safety
