---
title: Prompt Engineering
category: llm-agents/prompting
tags: [prompt-engineering, system-prompt, few-shot, chain-of-thought, prompting-techniques]
---

# Prompt Engineering

## Key Facts

- Prompt engineering is the practice of designing inputs to LLMs to get desired outputs without changing model weights
- Two core prompt types: **system prompt** (sets context, persona, constraints) and **user prompt** (the actual request)
- OpenAI message format (now industry standard): list of `{"role": "system"|"user"|"assistant", "content": "..."}`
- Key techniques ranked by complexity: zero-shot < few-shot < chain-of-thought < tree-of-thought < ReAct
- Better prompts on small models often outperform poor prompts on large models
- Prompt engineering is free (no training cost) vs [[fine-tuning]] which requires compute and data
- Works across all LLMs: OpenAI, Anthropic Claude, Google Gemini, open-source models via [[ollama-local-llms]]

## Patterns

```python
# Basic message structure (OpenAI format, adopted by most providers)
messages = [
    {"role": "system", "content": "You are a helpful assistant that responds in JSON."},
    {"role": "user", "content": "List 3 fruits with their colors."}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
```

```python
# Few-shot prompting - provide examples
messages = [
    {"role": "system", "content": "Classify customer feedback as positive, negative, or neutral."},
    {"role": "user", "content": "Great product, love it!"},
    {"role": "assistant", "content": "positive"},
    {"role": "user", "content": "Terrible experience, never again."},
    {"role": "assistant", "content": "negative"},
    {"role": "user", "content": "The package arrived on time."},  # actual query
]
```

```python
# Chain-of-thought prompting
system = """You are a math tutor. When solving problems:
1. State what information is given
2. Identify what we need to find
3. Show each step of your reasoning
4. State the final answer clearly

Think step by step."""
```

```python
# Role-based system prompt for RAG
system = """You are a customer support agent for ACME Corp.
Use ONLY the provided context to answer questions.
If the context doesn't contain the answer, say "I don't have that information."
Never make up product specifications or policies.

Context:
{retrieved_chunks}"""
```

## Gotchas

- **Prompt injection**: users can override system prompts with instructions like "ignore previous instructions". Always validate outputs
- **Temperature affects determinism**: temperature=0 for factual/deterministic, 0.7-1.0 for creative tasks
- **Order matters**: LLMs attend more to the beginning and end of prompts (recency and primacy bias)
- **Negative instructions fail**: "Don't mention X" often makes the model mention X. Use positive framing instead
- **Token cost**: long system prompts cost tokens on every request. Cache-friendly prefixes help (see KV context caching)
- **Model-specific**: prompts that work on GPT-4 may not work on Claude or Llama. Test across models
- **Structured output**: ask for JSON/markdown explicitly in the system prompt, or use [[structured-output]] features

## See Also

- [[function-calling]] - extending LLMs with tools via prompts
- [[rag-pipeline]] - injecting retrieved context into prompts
- [[agent-architectures]] - system prompts for autonomous agents
- [[structured-output]] - forcing specific output formats
- https://platform.openai.com/docs/guides/prompt-engineering - OpenAI prompt guide
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering - Anthropic prompt guide
- https://www.promptingguide.ai/ - comprehensive prompting techniques
