---
title: "GigaChat"
category: "projects"
date: 2026-09-13
tags: ["gigachat", "gigachat-development", "project"]
aliases: ["GigaChat", "GigaChat 2"]
---

# GigaChat

**Development line:** project:gigachat · thread gigachat-development  
**Last event:** 2026-09-13 · 2 dated since 2026-09-13 · **Researched:** 2026-11-18 · confidence: medium

## What it is

GigaChat is Sber's family of open-weights mixture-of-experts foundation language models. It is built for enterprise automation, mathematical reasoning and technical work in Russian. It is a sovereign enterprise alternative for organisations that need on-premises deployment and local domain alignment without depending on Western cloud APIs.

- **Reasoning:** handles complex multi-step problems.
- **Bilingual text:** generates Russian and English.
- **Code:** synthesises code.
- **Long context:** analyses long documents.
- **Speculative decoding:** multi-token prediction heads speed up generation.

432B parameters in total, 28B active per token. Deploying the full weights needs a lot of VRAM across several accelerators.

## Development line

- **2026-09-13 — GigaChat architecture and benchmark analysis.** An analysis compares the architecture with DeepSeek MLA and Kimi K3. Its benchmarks show GigaChat weaker than Qwen3.8-27B. It also compares the pricing with competitors.
- **2026-09-13 — Sergey Markov announced as GigaChat director at Norilsk Nickel conference.** On September 13, 2026, at a Norilsk Nickel conference, Sergey Markov presented himself as director of GigaChat and Kandinsky. The same report questions his authority. It notes that his education is in information systems and state management, not AI. It cites open data on his academic history at Orlovsky State Technical University.
- **2026-09-13 — other reporting on this date.**
  - The model repository lists the architecture: 432B total and 28B active parameters, 256 experts with 8 active and 1 shared per token. Layers mix Multi-head Latent Attention and GatedDeltaNet. There are 3 multi-token prediction heads, a 262K context window and the MIT license. (2026-09-13) — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>
  - The conference recording confirms the talk. Sergey Markov presented Sber's sovereign AI roadmap, enterprise integration strategies for GigaChat and Kandinsky, and industrial deployment initiatives at Norilsk Nickel. (2026-09-13) — <https://www.youtube.com/watch?v=wU5NzlUPDH0>

## What changed

- **Dense to sparse.** Dense large models gave way to a sparse mixture-of-experts design. Less compute goes to active parameters, and capacity stays the same.
- **Attention.** Standard multi-head attention was replaced by alternating multi-head latent attention and gated linear attention layers. This compresses key-value cache memory.
- **Generation.** Multi-token prediction heads were added to raise inference throughput through speculative decoding.
- **Distribution.** Beyond proprietary cloud endpoints, the weights are now open under a permissive license on public repositories. Executives also took the model to major domestic enterprise partners.

## How to use this

1. Deploy GigaChat3.5-432B-A28B-Reasoning on vLLM or SGLang. Use FP8 quantization and multi-GPU tensor parallelism with support for Multi-head Latent Attention (MLA) and GatedDeltaNet layers.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>
2. Set the runtime to use the native 262K token context window. Turn on the multi-token prediction heads for speculative decoding.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>

## Best practices

- Combine low-rank MLA key-value cache compression with the alternating linear attention layers, so long-context generation does not run out of memory.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>
- Provision a distributed enterprise cluster with enough total VRAM for the 432B parameter weights. Only 28B are routed per token, but all the weights still have to be hosted.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>

## Superseded by this

- Earlier dense GigaChat generations and monolithic Multi-Head Attention setups with uncompressed key-value caches. The hybrid MLA, GatedDeltaNet and 432B/28B MoE architecture replaces them.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>

## Still unknown

- Point-by-point benchmark tables against Qwen3.8-27B and Kimi K3. They could not be verified from primary sources, because the third-party forum links sit behind search redirects that would not resolve.
- Sergey Markov's education at Orlovsky State Technical University and the other biographical claims. Public repository metadata does not confirm them.
- How Sber's internal enterprise GigaChat API tier relates to the public open-weights ai-sage release. First-party documentation alone does not settle it.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning | ai-sage/GigaChat3.5-432B-A28B-Reasoning · Hugging Face | 2026-11-18 |
| https://www.youtube.com/watch?v=wU5NzlUPDH0 | Sergey Markov Presentation at Norilsk Nickel Conference | 2026-11-18 |

## Agent brief {#agent-brief}

- **Subject:** project:gigachat, thread gigachat-development, 2 dated events 2026-09-13 → 2026-09-13.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
