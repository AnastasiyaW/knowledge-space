---
title: Transformer Architecture
category: concepts
tags: [llm-agents, transformers, attention, deep-learning, architecture]
---

# Transformer Architecture

The transformer is the foundational architecture behind all modern LLMs. Introduced in 2017 ("Attention Is All You Need"), it replaced recurrent approaches with parallelizable self-attention, enabling massive scaling of model size and training data.

## Evolution: RNN -> LSTM -> Transformer

**RNN**: Processes tokens sequentially, maintaining hidden state. Suffers from vanishing/exploding gradients on long sequences. Cannot parallelize.

**LSTM**: Added gates (forget, input, output) to control information flow. Better at long-range dependencies but still sequential - cannot parallelize training.

**Transformer**: Fully parallelizable via attention mechanism. Processes all tokens simultaneously. Scales with compute and data. Foundation for GPT, BERT, Claude, Llama, and all modern LLMs.

## Core Architecture

### Encoder-Decoder Structure

The original transformer was designed for translation with both components:

- **Encoder**: processes input sequence, builds contextual representations
- **Decoder**: generates output sequence using encoder representations via cross-attention

Modern variants specialize:
- **Encoder-only** (BERT): bidirectional attention, best for classification, NER, embeddings
- **Decoder-only** (GPT, Claude, Llama): autoregressive (causal), best for text generation

### Self-Attention Mechanism

Each token attends to all other tokens to determine relevance.

**Query, Key, Value (Q, K, V):**
1. Each token produces three vectors: Query (what am I looking for?), Key (what do I contain?), Value (what information do I provide?)
2. Attention score = Q * K^T (relevance of each token)
3. Scale by sqrt(d_k) to prevent gradient issues in softmax
4. Softmax produces attention weights (sum to 1)
5. Weighted sum of Value vectors = output

**Formula**: `Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V`

**Intuition**: For "The cat sat on the mat", when processing "sat", the model gives high attention to "cat" (subject), medium to "mat" (location), low to "the" (article).

### Multi-Head Attention

Run H parallel attention "heads", each with separate Q, K, V weight matrices. Each head learns different relationship types (syntactic, semantic, positional). Outputs are concatenated and projected.

Typical head counts: 12 (BERT-base), 32 (GPT-3), 96 (large frontier models).

### Feed-Forward Network (FFN)

After attention, each token passes through a 2-layer network:

```text
FFN(x) = max(0, xW1 + b1)W2 + b2
```

- First layer expands dimension (typically 4x hidden size)
- ReLU/GELU activation
- Second layer projects back to hidden size
- This is where much of the model's "knowledge" is stored

### Residual Connections and Layer Normalization

- **Residual connections**: `output = LayerNorm(x + Sublayer(x))` - prevents vanishing gradients in deep networks
- **Layer normalization**: normalizes activations across feature dimension
- **Pre-norm** (normalize before sublayer) is more stable for deep models than post-norm

## BERT vs GPT

| Feature | BERT | GPT |
|---------|------|-----|
| Architecture | Encoder-only | Decoder-only |
| Attention | Bidirectional (full context) | Causal (sees only past tokens) |
| Training | Masked Language Model (predict masked tokens) | Autoregressive (predict next token) |
| Best for | Classification, NER, Q&A, embeddings | Text generation, chat, code |

## Positional Encoding

Transformers have no inherent sense of token order. Position information is injected via:

| Type | Mechanism | Models | Extrapolation |
|------|-----------|--------|---------------|
| **Sinusoidal** | Fixed sin/cos patterns | GPT-1, BERT, original Transformer | Poor beyond training length |
| **Learned** | Trainable position embeddings | GPT-2 | Limited to trained length |
| **RoPE** (Rotary) | Rotates embeddings by position-dependent angle | LLaMA, Mistral, GPT-4 | Good with NTK/YaRN extensions |
| **ALiBi** | Distance-based penalty on attention scores | Mistral variants | Good - works beyond training length |

## Attention Optimizations

- **FlashAttention**: GPU-friendly tiled computation. Same accuracy, 2-4x faster, much less memory. Breaks Q/K/V into tiles instead of computing full attention matrix.
- **MQA (Multi-Query Attention)**: One K/V pair shared across all heads. Saves memory and compute with slight expressiveness tradeoff.
- **GQA (Grouped-Query Attention)**: Heads divided into groups, each sharing K/V. Used in Llama 2 70B. Middle ground between MHA and MQA.
- **MoE (Mixture of Experts)**: Only activate subset of parameters per token. Mixtral uses 2 of 8 experts per token (47B total, ~13B active).

## Key Architectural Parameters

| Parameter | BERT-base | GPT-3 | Effect |
|-----------|-----------|-------|--------|
| Hidden size (d_model) | 768 | 4096 | Model capacity |
| Layers | 12 | 96 | Depth of reasoning |
| Attention heads | 12 | 96 | Attention pattern diversity |
| FFN inner dim | 3072 | 16384 | Knowledge storage |
| Vocab size | 30K | 50K | Language coverage |
| Max sequence | 512 | 2048+ | Context window |

## Gotchas
- Attention complexity is O(n^2) with sequence length - this is why context windows are expensive
- KV-cache memory grows as O(n * layers * d_model) per token during generation
- "Lost in the middle" problem: information in the middle of long prompts is less likely to be used than beginning/end
- Extending context beyond trained window risks quality degradation even with RoPE

## See Also
- [[tokenization]] - How text becomes tokens for the transformer
- [[embeddings]] - Vector representations from transformer layers
- [[model-optimization]] - Quantization, distillation, pruning of transformer models
- [[frontier-models]] - Comparison of transformer-based LLMs
