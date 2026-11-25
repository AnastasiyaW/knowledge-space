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

<!-- live-update:99eff90331534eb7a05520b7b681c68ed9e5d422263284b1f910bf0cb25525d6 -->
## 2026-09-11 — GigaChat 3.5 Reasoning open weights released under MIT

GigaChat 3.5 Reasoning is an open-weight reasoning checkpoint under the MIT license. The training used online reinforcement learning and specialized expert models.

## 2026-09-11 — GigaChat 3.5 Reasoning checkpoint published for self-hosting

The GigaChat3.5-432B-A28B-Reasoning checkpoint is out for self-hosting. It has 432B total parameters, 28B active parameters, and a 262K-token context limit. Documented serving paths cover SGLang and vLLM.

### Usage and practices

- Choose the FP8 checkpoint for inference, and the BF16 variant for fine-tuning or custom quantization. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)
- Install the SGLang or vLLM revision named in the model card so the launch path picks up GigaChat 3.5 support from the upstream pull requests. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)
- Launch on the documented eight-H100 setup with tensor and expert parallelism, and enable the GigaChat reasoning and tool-call parsers. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)
- Call the OpenAI-compatible chat-completions endpoint. Read the parsed reasoning field separately from the final content when the reasoning parser is on. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)
- Serve from the FP8 weights and tune or quantize from the separate BF16 weights. Do not use the inference checkpoint for fine-tuning. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)
- Turn on the documented reasoning and tool-call parsers so hidden reasoning and the final answer land in separate response fields. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)
- Treat published benchmark comparisons as vendor measurements. The model card documents benchmark-specific judges, corrected scoring, and agent timeouts. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)

### What practitioners say

- One practitioner advises self-hosting on rented compute or a dedicated server instead of home GPUs. The released checkpoint handles text generation, not image inputs. (2026-09-14) [Source](https://blog.fillikam.com/guides/gigachat-3-5-reasoning-rassuzhdeniya/)

### Additional evidence

- 2026-09-11: Release notes identify this as the first GigaChat model trained for full reasoning with online RL. Six domain experts—STEM, code, code agent, general agent, dialogue and instruction following—are combined through on-policy distillation. The post reports an IFBench score of 77.00 versus 43.66 for GigaChat 3.5 Ultra Instruct. [Source](https://giga.chat/blog/en/posts/gigachat-3-5-reasoning)
- 2026-09-11: The checkpoint is named ai-sage/GigaChat3.5-432B-A28B-Reasoning. The model card lists MIT licensing, 432B total and 28B active parameters, a 262K-token context limit, FP8 inference weights, and a separate BF16 checkpoint for fine-tuning or custom quantization. [Source](https://huggingface.co/ai-sage/GigaChat3.5-432B-A28B-Reasoning)

### Subsequent developments

- 2026-07-06: GigaChat 3.5 Ultra established the 432B GigaChat 3.5 base family. It open-sourced the hybrid MLA-plus-GatedDeltaNet architecture that the Reasoning checkpoint builds on. [Source](https://giga.chat/blog/en/posts/gigachat-3-5)

### Limits and open questions

- The two reviewed entries share their title and sources. Public evidence supports one release announcement, not two separate product changes.
- No independent benchmark replication was found. Performance figures in the model card remain vendor-reported.
- The model card's SGLang and vLLM installation instructions point to named upstream pull requests. Verify upstream compatibility before deploying to production.

<!-- Retained base: b499a7b71aef3b3ef3cc25a3ac6fd5795b6ae5d4; article blob: fe3036a0b6f222b1b7ecf77ef59dffdd2d5b7033 -->
