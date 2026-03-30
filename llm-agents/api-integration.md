---
title: LLM API Integration
category: llm-agents/infrastructure
tags: [api, openai-api, anthropic-api, rest-api, sdk, authentication, rate-limits]
---

# LLM API Integration

## Key Facts

- LLM APIs provide programmatic access to frontier models (GPT, Claude, Gemini) via HTTP/SDK
- Two separate worlds: **web UI** (ChatGPT, claude.ai - subscription) and **API** (pay-per-token, programmatic)
- API pricing: per 1M tokens. GPT-4o-mini: ~$0.15 input / $0.60 output. GPT-4o: ~$2.50 / $10.00
- Authentication: API keys stored in `.env` files, never committed to source control
- Standard response path: `response.choices[0].message.content` (OpenAI format)
- Rate limits: requests/min and tokens/min. Varies by tier/plan. Implement exponential backoff
- OpenAI's message format (system/user/assistant roles) became the de facto standard across providers

## Patterns

```python
# .env file setup (NEVER commit to git)
# OPENAI_API_KEY=sk-proj-...
# ANTHROPIC_API_KEY=sk-ant-...

from dotenv import load_dotenv
import os
load_dotenv()  # loads .env file
api_key = os.getenv("OPENAI_API_KEY")
```

```python
# OpenAI Python SDK
from openai import OpenAI
client = OpenAI()  # reads OPENAI_API_KEY from env

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,     # 0=deterministic, 1=creative
    max_tokens=1000,     # max output tokens
    stream=True          # streaming response
)

# Streaming
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

```python
# Anthropic Python SDK
import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content[0].text)
```

```python
# Rate limit handling with retry
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def call_llm(messages):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
```

## Gotchas

- **API key security**: never hardcode keys. Use `.env` files + `python-dotenv`. Add `.env` to `.gitignore`
- **Hyphens vs dashes**: copy-pasting API keys through Mac Notes can replace hyphens with em-dashes, breaking the key
- **Minimum deposit**: OpenAI requires ~$5 minimum prepaid balance. Keep auto-recharge OFF
- **Streaming vs non-streaming**: streaming is better UX but harder to parse. Non-streaming waits for full response
- **Token counting matters**: long system prompts + chat history accumulate. Monitor with `usage` in response
- **Model naming**: model IDs change (e.g., `gpt-4o-mini-2024-07-18`). Use aliases when possible
- **Timeout handling**: long generations can timeout. Set appropriate timeout values in HTTP clients

## See Also

- [[function-calling]] - extending API calls with tool use
- [[prompt-engineering]] - designing effective API prompts
- [[tokenization]] - understanding token-based pricing
- [[model-selection]] - choosing the right API/model
- https://platform.openai.com/docs/api-reference - OpenAI API reference
- https://docs.anthropic.com/en/api - Anthropic API reference
- https://ai.google.dev/docs - Google Gemini API docs
