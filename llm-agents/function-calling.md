---
title: Function Calling
category: llm-agents/tools
tags: [function-calling, tool-use, api-integration, openai-functions, agent-tools]
---

# Function Calling

## Key Facts

- Function calling lets LLMs invoke external tools (APIs, calculators, databases, code interpreters) to overcome their limitations
- LLMs are bad at: math, real-time data, file I/O, API calls, executing code. Function calling fills these gaps
- The LLM decides **which function to call** and **what arguments to pass** based on the conversation context
- The LLM does NOT execute the function - it returns a structured request, your code executes it, then feeds the result back
- Karpathy's framing: LLM = operating system, functions = peripheral devices (browser, calculator, disk, other models)
- Supported by: OpenAI, Anthropic (tool_use), Google Gemini, Mistral, Llama 3+ (via Ollama/vLLM)
- Foundation for [[agent-architectures]] - agents are LLMs + tools + reasoning loops

## Patterns

```python
# OpenAI function calling
from openai import OpenAI
client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto"  # "auto", "none", "required", or specific function
)

# Check if model wants to call a function
if response.choices[0].message.tool_calls:
    call = response.choices[0].message.tool_calls[0]
    # call.function.name == "get_weather"
    # call.function.arguments == '{"location": "Tokyo", "unit": "celsius"}'

    # Execute the function yourself
    result = get_weather(**json.loads(call.function.arguments))

    # Feed result back to the model
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "content": json.dumps(result)
    })
    final = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
```

```python
# Anthropic Claude tool use
import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "Weather in Tokyo?"}]
)
# response.content may contain tool_use blocks
```

## Gotchas

- **LLM does NOT execute functions**: it only generates the call signature. Your code must execute and return results
- **Hallucinated arguments**: LLM may invent plausible but incorrect function arguments. Validate all inputs
- **Tool description quality**: vague descriptions = wrong tool selection. Be specific about when/why to use each tool
- **Cost multiplier**: function calling requires at least 2 API calls (plan + result integration), often more in loops
- **Parallel tool calls**: GPT-4o+ can request multiple tool calls in one response. Handle all of them
- **Security**: never let LLMs call destructive functions without human approval (delete, send email, execute code)
- **Token overhead**: tool schemas count toward input tokens. Many tools = expensive context

## See Also

- [[agent-architectures]] - agents built on top of function calling
- [[api-integration]] - connecting to external APIs
- [[structured-output]] - constraining LLM output format
- [[langchain]] - framework abstracting tool integration
- https://platform.openai.com/docs/guides/function-calling - OpenAI function calling docs
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use - Anthropic tool use docs
