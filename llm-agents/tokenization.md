---
title: Tokenization
category: llm-agents/fundamentals
tags: [tokens, tokenizer, bpe, context-window, token-limits]
---

# Tokenization

## Key Facts

- Tokenization converts text into numerical tokens that LLMs process. LLMs see numbers, not words
- A token is roughly 4 characters or 0.75 words in English. 1500 words ~ 2048 tokens
- **BPE** (Byte Pair Encoding) is the dominant algorithm: learns frequent character sequences as single tokens
- Each LLM family has its own tokenizer. Tokens from GPT tokenizer differ from Llama's
- **Context window** = maximum tokens the model can process (input + output combined)
- Context window sizes: GPT-4o = 128K, Claude 3.5 = 200K, Gemini 1.5 = 2M, Llama 3.2 = 128K, small open-source = 4K-32K
- When context window is full, the model loses track of earlier conversation. This is the token limit
- API pricing is per-token: input tokens (cheaper) and output tokens (more expensive)

## Patterns

```python
# Count tokens with tiktoken (OpenAI)
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o-mini")
tokens = enc.encode("Hello, world!")
print(f"Token count: {len(tokens)}")  # 4
print(f"Token IDs: {tokens}")  # [9906, 11, 1917, 0]
print(f"Decoded: {enc.decode(tokens)}")

# Estimate cost
input_tokens = len(enc.encode(prompt))
# GPT-4o-mini: $0.15 per 1M input tokens
cost = input_tokens * 0.15 / 1_000_000
```

```python
# HuggingFace tokenizer
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tokens = tokenizer("Hello world", return_tensors="pt")
print(tokenizer.convert_ids_to_tokens(tokens["input_ids"][0]))
```

```python
# Check if text fits in context window
def fits_in_context(text: str, model: str = "gpt-4o-mini", max_tokens: int = 128000) -> bool:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text)) < max_tokens
```

## Gotchas

- **Token != word**: "indivisibility" = 5 tokens, not 1. Always count tokens, never words
- **Non-English text**: uses more tokens per word (Chinese: ~2 tokens per character)
- **Code tokens**: code is tokenized differently than prose. JSON/code is often more token-expensive
- **Context window != memory**: the model "forgets" nothing within the window, but has attention degradation for middle content
- **Hidden tokens**: system prompt, function schemas, and chat history all count toward the context window
- **Output token limits**: separate from context window. Max output is typically 4K-16K tokens per response
- **Tokenizer mismatch**: using wrong tokenizer to count tokens gives wrong estimates. Match tokenizer to model

## See Also

- [[prompt-engineering]] - designing efficient prompts within token budgets
- [[memory-and-context]] - strategies when context window isn't enough
- [[api-integration]] - token-based pricing models
- [[model-selection]] - context window as selection criterion
- https://platform.openai.com/tokenizer - OpenAI interactive tokenizer
- https://github.com/openai/tiktoken - tiktoken library
