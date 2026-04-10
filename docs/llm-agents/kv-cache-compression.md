---
title: KV Cache Compression
category: techniques
tags: [llm-agents, kv-cache, quantization, inference, memory-optimization, long-context, turboquant, triattention, kvpress, lopace]
---

# KV Cache Compression

Reducing KV cache memory during LLM inference to enable longer contexts and more concurrent requests on the same GPU. The key-value cache grows linearly with sequence length and batch size, often becoming the memory bottleneck before model weights do.

## Key Facts

- KV cache for a 70B model at 128K context can exceed 40GB - more than the weights themselves
- 3-bit KV cache quantization achieves ~5-6x memory reduction with 99.5% attention fidelity
- Random rotation + scalar quantization is the simplest effective approach - implementations appeared within hours of the paper
- Weight quantization and KV cache quantization are orthogonal - combine them for maximum savings
- The benefit scales with context length: minimal at 4K, significant at 32K+, transformative at 128K+

## Why KV Cache Is the Bottleneck

During autoregressive generation, the model stores key and value tensors for every past token in every layer:

```
KV cache size = 2 * num_layers * num_heads * head_dim * seq_len * batch_size * bytes_per_element

Example (Llama 70B, FP16, single sequence):
= 2 * 80 * 64 * 128 * 128000 * 1 * 2 bytes
= ~42 GB
```

Model weights (Q4_K_M quantized) take ~40GB. The KV cache alone matches or exceeds weight memory at long contexts.

## TurboQuant: Rotation + Scalar Quantization

Core algorithm with no model retraining:

1. **Random rotation** - multiply K and V vectors by a random orthogonal matrix. This spreads outlier magnitudes evenly across dimensions, making all channels quantization-friendly
2. **Scalar quantization** - map rotated values to a small lookup table (3-4 bits per element)
3. **Optional error correction** - QJL (Quantized Johnson-Lindenstrauss) reduces approximation error in attention scores

```bash
# llama.cpp with KV cache quantization (fork)
./llama-server -m model.gguf \
  --cache-type-k turbo3 \
  --cache-type-v turbo3

# Standard llama.cpp (when merged)
./llama-server -m model.gguf \
  --cache-type-k q4_0 \
  --cache-type-v q4_0
```

## Memory Savings by Configuration

| Config | Weights | KV Cache | Total (128K ctx) | Quality |
|--------|---------|----------|-------------------|---------|
| FP16 + FP16 cache | 140 GB | 42 GB | 182 GB | Baseline |
| Q4_K_M + FP16 cache | 40 GB | 42 GB | 82 GB | ~99.9% |
| Q4_K_M + Q8 cache | 40 GB | 21 GB | 61 GB | ~99.8% |
| Q4_K_M + turbo3 cache | 40 GB | 7 GB | 47 GB | ~99.5% |
| Q4_K_M + turbo2 cache | 40 GB | 5 GB | 45 GB | ~98.5% |

## Implementation Landscape (2026)

| Project | Status | Platform |
|---------|--------|----------|
| llama.cpp fork (TheTom) | Working, 18/18 tests pass | CPU |
| llama.cpp mainline | Feature request, merge expected | CPU/GPU |
| vLLM | Feature request open | GPU (CUDA) |
| Standalone Triton kernels | Working | GPU (CUDA) |
| Apple Silicon variant | 4.6x compression, q8_0 speed parity | Metal |
| PyTorch reference | Educational implementation | Any |

## When to Use

**High value:**

- Long-context inference (64K+ tokens) where KV cache dominates memory
- Multi-user serving where batch size multiplies cache memory
- Running large models on limited VRAM (single GPU for 70B)

**Low value:**

- Short prompts (<4K tokens) - cache is small anyway
- Batch size 1 with short context - weight quantization matters more
- Training - KV cache is recomputed per step, not stored

## Quality Considerations

Base weight quantization affects how well KV cache quantization works:

```
Higher quality weights + aggressive cache quant = good
  Q8_0 weights + turbo3 cache → minimal degradation

Lower quality weights + aggressive cache quant = compounding errors
  Q4_K_M weights + turbo2 cache → noticeable on complex reasoning
```

**Validation approach:**

```bash
# Needle-in-haystack test across context lengths
python eval_needle.py \
  --model model.gguf \
  --cache-type turbo3 \
  --context-lengths 4096 16384 65536 131072 \
  --num-needles 100

# Compare perplexity
./llama-perplexity -m model.gguf \
  --cache-type-k turbo3 --cache-type-v turbo3 \
  -f wiki_test.txt
```

## Combining with Other Optimizations

KV cache compression stacks with other inference techniques:

| Technique | Target | Combines? |
|-----------|--------|-----------|
| Weight quantization (GGUF, AWQ, GPTQ) | Model weights | Yes - orthogonal |
| KV cache quantization | Attention cache | This article |
| Flash Attention | Attention compute | Yes - reduces compute, this reduces memory |
| Sliding window attention | Context structure | Yes - reduces cache entries, this reduces per-entry size |
| Speculative decoding | Generation speed | Yes - no conflict |
| PagedAttention (vLLM) | Memory fragmentation | Yes - paged allocation + smaller pages |

## TriAttention - Pre-RoPE Importance Scoring (2026)

10.7x KV memory reduction with zero accuracy loss on reasoning tasks. Exploits the discovery that pre-RoPE Q/K vectors concentrate around fixed centers across heads.

### Architecture

1. **Trigonometric Series Scoring (S_trig)** - estimates key importance via Q/K centers + positional distance
2. **Norm-Based Scoring (S_norm)** - complementary signal for low-concentration heads
3. **Adaptive Weighting** - auto-balances using Mean Resultant Length (R) metric

```text
Performance:
  AIME25: 32.9% (vs R-KV 17.5%, SnapKV similar budget) at 10.7x compression
  MATH 500: 6.3x speedup (1405 vs 223 tokens/sec)
  RULER retrieval: 66.1 (vs SnapKV 55.6)

Deployment: vLLM plugin (auto-discovery, no code changes)
Validated on: Qwen3-8B, DeepSeek-R1-Distill-Llama-8B, GPT-OSS-20B, GLM-4.7-Flash (MLA)
```

Why it beats prior methods: H2O, SnapKV, R-KV use "limited observation windows" - only recent queries maintain representative orientations. TriAttention operates in pre-RoPE space where vectors are stable, providing intrinsic importance signals independent of position.

## KVPress Toolkit (NVIDIA, 2026)

Framework for benchmarking and deploying KV compression strategies. Not a standalone method - wraps multiple approaches for comparison.

```text
Methods: KnormPress, SnapKVPress, ObservedAttention, SinkPress, TurboQuant
Integration: HuggingFace transformers native
Use case: Benchmark different strategies on your specific model/task
```

## CompLLM - Segment-Based Soft Compression

Divides context into segments, compresses each independently. Results: 2x compression yields 4x TTFT speedup, 50% KV cache reduction. Practical for long-context Q&A where full attention is unnecessary.

## LoPace - Lossless Prompt Compression for Storage

Lossless compression for prompt caching and storage (not inference-time):

```text
Methods: Zstandard + BPE tokenization + binary packing + hybrid
Compression: 4.89x average (range 1.22-19.09x), 72.2% space savings
Reconstruction: 100% lossless
Use case: Prompt caching, template storage, prompt libraries
NOT for: Runtime KV cache reduction
```

## Gotchas

- **QJL correction can hurt through standard attention paths** - the second-stage error correction from the paper assumes a specific attention implementation. Through standard scaled dot-product attention, QJL correction empirically worsens quality. Use the `_mse` variant that optimizes mean squared error directly instead
- **`turbo3` is not equivalent to `q3_0`** - the rotation step before quantization is critical. Standard 3-bit quantization without rotation produces much worse results because outlier channels dominate the error. The rotation spreads information evenly across dimensions first
- **Benchmark at YOUR context length** - a model that passes perplexity tests at 4K may fail needle-in-haystack at 128K with aggressive cache quantization. Always test at the actual context length you plan to serve
- **MemPalace AAAK debunked** - claimed 30x lossless compression via abbreviation dialect, but token counting was wrong (len(text)//3 instead of proper tokenizer). AAAK actually increases tokens at small scales. LongMemEval regressed from 96.6% to 84.2%. The valid finding: raw verbatim storage + smart retrieval beats LLM extraction
- **TriAttention requires pre-RoPE access** - the method operates on Q/K vectors before rotary position embedding is applied. Inference frameworks that fuse RoPE into the attention kernel may need modification

## See Also

- [[model-optimization]] - weight quantization, distillation, pruning
- [[token-optimization]] - reducing token count to reduce cache size
- [[production-patterns]] - serving infrastructure for LLM inference
- [[transformer-architecture]] - attention mechanism that generates KV cache
- [[Diffusion Inference Acceleration]] - TriAttention applied to diffusion models
