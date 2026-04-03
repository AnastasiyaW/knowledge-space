---
title: Tokenization
category: concepts
tags: [llm-agents, tokenization, bpe, wordpiece, sentencepiece, context-window]
---

# Tokenization

Tokenization converts raw text into sequences of integer token IDs that transformer models can process. The choice of tokenizer affects vocabulary size, sequence length, multilingual capability, and API cost.

## Key Facts
- A token is roughly 4 characters or 0.75 words in English
- Non-English text (Russian, Chinese, Japanese) uses 2-4x more tokens per word - meaning higher API costs
- Each LLM family has its own tokenizer - tokens from GPT differ from Llama's
- Modern subword tokenizers virtually eliminate out-of-vocabulary (OOV) issues
- Context window = maximum tokens the model processes (input + output combined)

## Tokenization Algorithms

### BPE (Byte Pair Encoding)
Iteratively merges the most frequent character/subword pairs. Simple frequency heuristic.

**Used in**: GPT family, RoBERTa, BART

```python
from tokenizers import Tokenizer, models, pre_tokenizers, trainers

tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
trainer = trainers.BpeTrainer(vocab_size=1000)
tokenizer.train_from_iterator(corpus, trainer)
print(tokenizer.encode("Hello world").tokens)
```

### WordPiece
Optimizes corpus likelihood rather than simple frequency. Uses `##` prefix for continuation subwords ("playing" -> "play" + "##ing").

**Used in**: BERT

### SentencePiece
Treats spaces as characters (`_` symbol). Language-agnostic - works on raw text without pre-tokenization. Supports BPE and Unigram modes.

**Used in**: T5, mBART, LLaMA

```python
import sentencepiece as spm
spm.SentencePieceTrainer.Train(
    '--input=corpus.txt --model_prefix=tok_sp --vocab_size=1000'
)
sp = spm.SentencePieceProcessor(model_file='tok_sp.model')
```

## Special Tokens

| Token | Purpose | BERT | GPT | T5 |
|-------|---------|------|-----|-----|
| [CLS] / \<s\> | Classification aggregate | Yes | No | \<s\> |
| [SEP] / \</s\> | Sentence separator | Yes | `\n\n` | \</s\> |
| [PAD] | Batch padding | Yes | \<eos\> | \<pad\> |
| [MASK] | Masked language modeling | Yes | No | \<extra_id_N\> |
| \<unk\> | Unknown token | Yes | No (BPE covers all) | Yes |

Multimodal markers: `<image>`, `<video>`, `<speech>` used in Flamingo, LLaVA, Kosmos-1.

## Token Counting

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")
tokens = enc.encode("Hello world")
print(len(tokens))  # exact token count

# Cost estimation
input_tokens = len(enc.encode(prompt))
cost = input_tokens * 2.50 / 1_000_000  # GPT-4o input price
```

## Context Windows

| Model | Context Window |
|-------|---------------|
| BERT | 512 tokens |
| GPT-4 | 8K / 128K tokens |
| Claude 3 | 200K tokens |
| Gemini 1.5 Pro | 1M tokens (up to 2M preview) |
| Llama 3 | 8K (extended variants) |
| Mistral Large | 128K tokens |

### Extending Effective Context
- **Truncation**: cut left/right context for local tasks
- **Sliding window + aggregation**: process in windows, merge results
- **Map-reduce summarization**: summarize chunks, merge summaries
- **RAG**: index corpus, inject only relevant fragments
- **KV-cache reuse**: cache static instructions separately from variable content

## Gotchas
- Token boundaries don't align with word boundaries - LLMs struggle with character-level tasks like string reversal
- Same text tokenizes differently across models - always count with the specific model's tokenizer
- Code and JSON are often more token-expensive than prose
- System prompt, function schemas, and chat history all count toward context window
- Output token limits are separate from context window (typically 4K-16K per response)
- "Lost in the middle" problem: information in the middle of long contexts is less likely to be attended to

## See Also
- [[transformer-architecture]] - How transformers process token sequences
- [[embeddings]] - Converting tokens to vector representations
- [[llm-api-integration]] - Token counting for API cost management
- [[model-optimization]] - Quantization reduces per-token compute
