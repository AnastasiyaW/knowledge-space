---
title: "Ternary Bonsai 2.5: ternary-bonsai-model-line — Ternary Bonsai Model Line"
category: "projects"
date: 2026-11-26
tags: ["project", "ternary-bonsai-2-5", "ternary-bonsai-model-line"]
aliases: ["Ternary Bonsai 2.5: ternary-bonsai-model-line"]
---

# Ternary Bonsai 2.5: ternary-bonsai-model-line — Ternary Bonsai Model Line

Ternary Bonsai 2.5 is an open-weight 27B language and vision model that runs locally on consumer GPUs with 12 GB VRAM.

**Development line:** project:ternary-bonsai-2-5 · thread ternary-bonsai-model-line  
**Last event:** 2026-11-26 · 2 dated since 2026-11-26 · **Researched:** 2026-11-27 · confidence: medium

## What it is

Ternary Bonsai 2.5 is an open-weight 27B language and vision model. It is built for local agent work on a consumer graphics card, not a multi-GPU server. It is a local alternative to full-precision 27B models for people with tight hardware limits.

Abilities:

- Function calling: works over multiple turns.
- Tool use: calls tools inside agent workflows.
- Code generation: holds up over long-horizon tasks.
- Vision-language understanding: reads images together with text.
- Long context: processes up to 262K tokens.

The 27B weights are compressed to about 5.93 GB. The method is ternary quantization with values {-1, 0, +1} and blockwise Hadamard rotations. Stable inference needs at least 12 GB VRAM.

## Development line

- **2026-11-26 — PrismML releases Ternary Bonsai 2.5, a 27B model with ternary quantization.** PrismML's Ternary Bonsai 2.5 is a 27B model with ternary quantization. Its weights are reported at about 5.93 GB, so it can run on consumer GPUs with 12 GB VRAM. The source reports benchmark claims of near parity with Qwen3.8 27B FP16 on tool use, and discusses local agents and RAG.
- **2026-11-26 — PrismML releases Ternary Bonsai 2.5, a 27B model claimed to run on 12 GB VRAM.** A Habr article covers PrismML's Ternary Bonsai 2.5, a 27B model with ternary quantization at about 5.93 GB of weights. It reports benchmark parity with Qwen3.8 27B FP16 in tool use. It frames the model as a way to run local AI agents and RAG on 12 GB GPUs.
- **2026-11-26 — other reporting on this date.**
  - Technical analysis of the format: ternary weights {-1, 0, +1} with per-128 FP16 scaling factors (~1.71-1.76 bits per weight), plus orthogonal blockwise Hadamard rotation. The base is Qwen3.8-27B with 262K context and hybrid attention. (2026-11-26) — <https://habr.com/ru/articles/1112562/>
  - Deployment specifications: the 5.93 GB footprint runs locally through custom llama.cpp forks and Apple MLX. It keeps over 94% of FP16 benchmark scores in tool use and coding evaluations, within a 12 GB VRAM envelope. (2026-11-26) — <https://habr.com/ru/articles/1112562/>

## What changed

The architecture moved from standard low-bit integer quantization to ternary weights. This applies to all linear projections, embedding layers and output heads. A later refinement moved the base to a hybrid-attention model with long-context tool calls. It also added ternary execution kernels for local runtimes.

## How to use this

1. Download the Ternary Bonsai 2.5 27B quantized GGUF weights (~5.93 GB), or the MLX distribution, for your runtime.
  — <https://habr.com/ru/articles/1112562/>
2. Run inference with a llama.cpp fork that supports ternary hybrid attention kernels, or with MLX on Apple Silicon.
  — <https://habr.com/ru/articles/1112562/>
3. Reserve at least 8-12 GB of GPU VRAM or unified memory for the weights and runtime context, so agent tool use and RAG pipelines have room.
  — <https://habr.com/ru/articles/1112562/>

## Best practices

- Use ternary-specific inference kernels with Hadamard transformation support, so activations are not dequantized at extra cost.
  — <https://habr.com/ru/articles/1112562/>
- For long-context agent work up to 262K tokens, use hardware with at least 12 GB VRAM, so the KV cache fits.
  — <https://habr.com/ru/articles/1112562/>

## What practitioners say

- The 5.93 GB ternary weights let a 27B reasoning model with near-FP16 quality run locally on a consumer 12 GB GPU. Custom runtime forks are needed for the best kernel speed. (2026-11-26)
  — <https://habr.com/ru/articles/1112562/>

## Superseded by this

- Standard FP16 or INT4 27B deployments need 16 GB to 54 GB VRAM. For local agent use on a 12 GB consumer GPU, 1.58-bit ternary quantization replaces them.
  — <https://habr.com/ru/articles/1112562/>

## Still unknown

- The first-party pages on prismml.com, github.com and huggingface.co came back only as redirect tokens with no canonical URLs. We could not check those endpoints directly.
- The Qwen3.8 27B FP16 comparisons rest on community reporting and publisher release notes. No independent evaluation suite has replicated them.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/articles/1112562/ | PrismML releases Ternary Bonsai 2.5: 27B model with ternary quantization on 12 GB VRAM | 2026-11-27 |

## Agent brief {#agent-brief}

- **Subject:** project:ternary-bonsai-2-5, thread ternary-bonsai-model-line, 2 dated events 2026-11-26 → 2026-11-26.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
