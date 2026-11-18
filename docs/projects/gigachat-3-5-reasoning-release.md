---
title: "GigaChat"
category: "projects"
date: 2026-09-14
tags: ["gigachat", "gigachat-3-5-reasoning-release", "gigachat-development", "project"]
aliases: ["GigaChat", "GigaChat 2"]
---

# GigaChat

**Development line:** project:gigachat-3-5-reasoning-release · thread gigachat-development  
**Last event:** 2026-09-14 · 2 dated since 2026-09-14 · **Researched:** 2026-11-18 · confidence: high

## What it is

GigaChat 3.5 Reasoning is Sber's open-weights reasoning model. It is built for developers and companies that need multi-stage problem solving they can check.

- Chain-of-thought planning: works through a task step by step.
- Code synthesis, mathematical deduction and auditing contracts for discrepancies.
- Mixture of experts: 432B parameters in total, 28B active per token.
- Hybrid attention: multi-head latent attention mixed with GatedDeltaNet layers.
- Context: 256K tokens, scaled with YaRN.

The 432B weights need multi-GPU servers running vLLM or SGLang. Under the MIT license, it is an open alternative to DeepSeek and OpenAI reasoning models that spends fewer tokens.

## Development line

- **2026-09-14 — GigaChat 3.5 Reasoning released with a reasoning mode and better benchmark scores.** Sber calls it a flagship model. Reasoning mode breaks a complex task into stages and checks the intermediate results. On average it uses 37% fewer tokens than DeepSeek V4 Flash Preview. Scores went up on IFBench, Natural Plan and Live Code Bench v6. The model is out under the MIT license on Hugging Face and GitVerse.
- **2026-09-14 — more detail from the same day.**
  - Architecture: mixture of experts with 432B total parameters, 28B active per token. Multi-Head Latent Attention \(MLA\) is interleaved with GatedDeltaNet linear attention every fourth layer. Context scales to 256K tokens with YaRN. (2026-09-14) — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>
  - The open weights ship with native configurations for vLLM and SGLang. The release confirms training with online reinforcement learning for multi-stage verification. The full weights are on GitVerse under the MIT license. (2026-09-14) — <https://gitverse.ru/GigaTeam/gigachat3.5-reasoning>

## What changed

GigaChat 3.5 Reasoning is a dedicated thinking variant of the GigaChat 3.5 architecture. The line moved from plain conversational generation to online reinforcement learning with an explicit reasoning mode. Multi-head latent attention and linear delta-rule layers keep long-context reasoning intact while cutting the tokens spent on inference.

## How to use this

1. Download the open weights from the Hugging Face repository ai-sage/GigaChat3.5-432B-A28B-Reasoning, or clone the repository from GitVerse.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>
2. Run the model on an inference engine that handles hybrid MLA and MoE, such as vLLM or SGLang, across multi-GPU servers.
  — <https://gitverse.ru/GigaTeam/gigachat3.5-reasoning>
3. Turn reasoning mode on for multi-stage analytical tasks. The model then writes out its chain-of-thought steps before the final answer.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>

## Best practices

- Plan for multi-node GPU clusters with enough total VRAM for the 432B MoE weights. If full BF16 does not fit in memory, use FP8 quantization.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>
- Turn on YaRN context extension up to 256K tokens for large document collections, legal contracts or multi-file repositories.
  — <https://gitverse.ru/GigaTeam/gigachat3.5-reasoning>
- Send multi-step logical deductions, mathematical proofs and program verification to reasoning mode. Keep simple generation on standard models so it does not burn tokens.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>

## Superseded by this

- Earlier GigaChat models had no open-weights reasoning architecture that checks its own intermediate steps. Multi-step tasks needed external prompt scaffolding.
  — <https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning>

## Still unknown

- Community views on Reddit and Habr are left out: we could not confirm those threads down to their permanent links.
- Commercial managed API pricing and rate limits on Cloud.ru are not documented in the official open-weights repositories.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning | ai-sage/GigaChat3.5-432B-A28B-Reasoning · Hugging Face | 2026-11-18 |
| https://gitverse.ru/GigaTeam/gigachat3.5-reasoning | GigaTeam / gigachat3.5-reasoning · GitVerse | 2026-11-18 |

## Agent brief {#agent-brief}

- **Subject:** project:gigachat-3-5-reasoning-release, thread gigachat-development, 2 dated events 2026-09-14 → 2026-09-14.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
