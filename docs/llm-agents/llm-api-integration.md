---
title: LLM API Integration
category: infrastructure
tags: [llm-agents, openai-api, anthropic-api, api-keys, streaming, chat-completions]
---

# LLM API Integration

Practical guide to integrating with LLM provider APIs. Covers authentication, message structure, key parameters, streaming, and cost management across OpenAI, Anthropic, and other providers.

## Key Facts
- API keys must NEVER be hardcoded - use environment variables and `.env` files
- LLMs are stateless - each API call is independent, client sends full conversation history
- Token-based pricing: input tokens (cheaper) + output tokens (more expensive)
- Streaming improves perceived latency by sending response chunks as they're generated
- If a key is exposed, revoke immediately and generate a new one

## API Key Management

```python
# .env file (never commit to version control)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...

# Load in Python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

## OpenAI Chat Completions

### Basic Call
```python
from openai import OpenAI
client = OpenAI()  # reads OPENAI_API_KEY from env

completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is a black hole?"}
    ]
)
print(completion.choices[0].message.content)
```

### Message Roles
- **system**: defines model purpose, persona, constraints. Set once at start.
- **user**: human input (questions, tasks, content)
- **assistant**: model responses OR few-shot examples for guiding style

### Key Parameters

| Parameter | Values | Effect |
|-----------|--------|--------|
| `temperature` | 0-2 (default 1) | 0 = deterministic, 2 = very random. >1.5 produces nonsense |
| `max_tokens` | integer | Cap on completion tokens. Too low = truncated |
| `n` | integer (default 1) | Number of response variants |
| `seed` | integer | Pseudo-reproducibility (not guaranteed) |
| `stream` | bool | Stream response as chunks |

### Streaming
```python
completion = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    stream=True
)
for chunk in completion:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="")
```

### Few-Shot Example Pattern
```python
messages = [
    {"role": "system", "content": "Classify tweet sentiment."},
    {"role": "user", "content": "This movie is extraordinary."},
    {"role": "assistant", "content": "positive"},
    {"role": "user", "content": "This album is alright."},
    {"role": "assistant", "content": "neutral"},
    {"role": "user", "content": "This new song blew my mind."}
]
```

## Anthropic Messages API

```python
from anthropic import Anthropic
client = Anthropic()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "What is a black hole?"}]
)
print(message.content[0].text)
```

## Pricing Model

```
Cost = (input_tokens * input_price) + (output_tokens * output_price)

Example (GPT-4o):
  Input:  1000 tokens * $2.50/1M = $0.0025
  Output: 500 tokens  * $10.00/1M = $0.005
  Total: ~$0.0075 per request
  At 10,000 req/day: ~$75/day
```

**Token caching** (Anthropic, OpenAI): 25% premium to cache context, then ~10x cheaper for subsequent queries against same context. Transforms economics of repeated document analysis.

## LogProbs - Hallucination Detection

Request log probabilities per token to see model confidence:
- Color-code tokens by confidence: red = uncertain, green = confident
- When model hallucinated, first tokens often show high uncertainty
- When model blindly trusted wrong input, it was confidently wrong
- Development debugging tool, not for end users

## Conversation History Management

```python
# Must send full history each time (stateless API)
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "First question"},
    {"role": "assistant", "content": "First answer"},
    {"role": "user", "content": "Follow-up"}
]
# Track token count, trim when approaching limit
```

## Gotchas
- Temperature 0 is not truly deterministic - small variations can occur
- max_tokens too low silently truncates responses without error
- Streaming responses require different parsing (delta.content vs message.content)
- API rate limits vary by tier - implement exponential backoff
- Model names change over time (GPT-4 -> GPT-4o -> GPT-4o-mini) - check current docs
- Hidden token costs: system prompts and function schemas count as input tokens

## See Also
- [[prompt-engineering]] - Crafting effective messages
- [[function-calling]] - Tool use via API
- [[tokenization]] - Understanding token counts and costs
- [[llmops]] - Monitoring API usage in production
- [[frontier-models]] - Which model to use for which API
