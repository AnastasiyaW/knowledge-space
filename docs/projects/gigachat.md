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

<!-- live-update:cd02f99a435cccd5a8a06019d9c27913457ba19b147bb1462586019eee372044 -->
## 2026-11-26 — Sber launches GigaChat 4 with 708B MoE architecture and 1M context window

Sber released GigaChat 4, a hybrid Mixture-of-Experts model with 708 billion parameters. It comes with an on-premise 37B dense variant and a 1-million-token context window through sparse attention. It has two modes, Instant and Reasoning, and native Model Context Protocol tooling for agents.

## 2026-11-26 — Sber introduces Kandinsky 6.5 with KandiShop identity preservation and 2K video

Sber updated its image and video generation with Kandinsky 6.5. It adds KandiShop, which keeps a face the same across generations. It also adds 10-second 2K video with keyframe control over transitions, and composition of characters and objects from several sources.

### Usage and practices

- Open the GigaChat web interface, or register for Sber AI Studio developer API credentials. [Source](https://giga.chat/)
- Select the GigaChat 4 checkpoint and set the mode: Instant for quick queries, Reasoning for complex multi-step tasks. [Source](https://giga.chat/)
- Connect external tools, file repositories or agent harnesses through Model Context Protocol (MCP) endpoints, so the model can run multi-step tasks on its own. [Source](https://giga.chat/)
- Call the Kandinsky 6.5 endpoints for multimodal generation. Give reference portraits for KandiShop identity preservation, or initial and terminal keyframes for video clips. [Source](https://giga.chat/)
- Use Reasoning mode for code synthesis, large-document analysis and multi-hop data extraction. Keep Instant mode for dialogue where latency matters. [Source](https://giga.chat/)
- Deploy the 37B on-premise GigaChat 4 variant in air-gapped enterprise environments that need strict data residency and perimeter security. [Source](https://giga.chat/)
- For Kandinsky 6.5 Video, provide clear reference keyframes and distinct character source images, so the scene stays continuous across transitions. [Source](https://giga.chat/)

### Additional evidence

- 2026-11-26: Sber described GigaChat 4 as a hybrid Mixture-of-Experts model with 708 billion total parameters and 41 billion active. A 37 billion parameter dense variant is meant for on-premise deployment. Sparse attention gives a native 1-million-token context window. Native Model Context Protocol (MCP) integrations support long-running autonomous tasks with tools. Instant and Reasoning modes sit in one unified checkpoint. [Source](https://giga.chat/)
- 2026-11-26: Kandinsky 6.5 includes the KandiShop identity preservation system, built with the AIRI Institute, which keeps exact facial features across generations. Video now runs up to 10 seconds at 2K resolution, with control over start and end keyframes. Characters and assets can be composed from distinct reference images. [Source](https://giga.chat/)

### Superseded guidance (retained for history)

- 2026-11-26: GigaChat 3.5 is the primary flagship model for complex enterprise tasks. [Source](https://giga.chat/)
- 2026-11-26: Kandinsky video generations are limited to short lower-resolution clips, with no multi-character blending and no keyframe constraints. [Source](https://giga.chat/)

### Limits and open questions

- Direct article links from Russian tech press (Habr, Forbes Russia, IXBT) could not be confirmed.
- Pricing tiers, API token limits and open-source weight repositories for the GigaChat 4 37B weights (for example on Hugging Face or Gitverse) are not confirmed with direct public paths.
- Independent benchmarks and accuracy comparisons against other frontier models are still pending, until the model is used in practice.

<!-- Retained base: 24e47c487718c6d5e8a3eb5e549a30b2eafa082d; article blob: f255efec0ef879346797ceb0d7028417945922c7 -->
