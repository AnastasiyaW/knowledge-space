---
title: Laguna S 2.1 — Laguna
category: projects
date: 2026-07-22
tags: [laguna, poolside-laguna-s-2-1, project]
aliases: ["Laguna S 2.1"]
---

# Laguna S 2.1 — Laguna

**Development line:** `project:poolside-laguna-s-2-1` · thread `laguna`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Laguna S 2.1 is Poolside's open-weight text-to-text Mixture-of-Experts coding model for teams building long-horizon software agents.

- 118B total parameters, about 8B active per token
- 1,048,576-token context, interleaved reasoning and tool use
- Hugging Face weights plus hosted and local serving paths

The BF16 checkpoint needs roughly 236 GB of weights and multiple GPUs; quantized artifacts change the hardware trade-off. We use it where long context, tool-call handling and self-hosting matter, but we validate the harness and the exact checkpoint before production.

## Development line

- **2026-07-22 — Poolside introduced Laguna S 2.1.** On 2026-07-22, Poolside introduced Laguna S 2.1 as a new step in the Laguna development line. The dated links associate the release with an announcement, a model-distribution page, quantized-model references, and listed chat and provider access routes. This matters because it identifies a distinct named version of the project.

## What changed

- **2026-07-21** — Laguna S 2.1 launched as an 118B-total, 8B-active MoE with a 1M-token context window and open weights.
- **2026-07-22** — An FP8 variant commit documented a spinquantless 256K configuration that it said fixes agentic looping; a second commit restored default thinking and preserved reasoning.
- **2026-07-28** — Poolside Desktop Assistant began pairing pool with Laguna S 2.1 by default; this is an integration, not a model checkpoint.
- **2026-08-01** — FP8 RC2 was promoted to main with a 1M configuration and a new-checkpoint note.
- **2026-08-02** — The INT4/BF16 hybrid release was promoted to main with a 1M configuration and a new-checkpoint note.

## How to use this

1. For a no-code trial, open Poolside Chat, confirm it displays Laguna S 2.1, and send a bounded coding task. Use its offered sign-up or login only if required. Do not submit material you cannot allow to be used for model improvement.
  — <https://chat.poolside.ai/>
2. For a hosted route, select the OpenRouter model ID poolside/laguna-s-2.1. It accepts tools and tool_choice, but does not enforce JSON response_format, so validate structured output in the client.
  — <https://openrouter.ai/poolside/laguna-s-2.1>
3. For standard self-hosting, use the official vLLM recipe for poolside/Laguna-S-2.1 with tensor parallelism, poolside_v1 tool and reasoning parsers, auto-tool choice and thinking enabled; then call its OpenAI-compatible chat endpoint.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
4. For a lower-memory local route, use the official Ollama command ollama run laguna-s-2.1 and choose a published quantization tag such as q4_K_M or q8_0 for the available machine.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
5. On macOS, install Poolside Desktop Assistant if a pool-based multi-agent workspace is wanted; its default pairing is pool with Laguna S 2.1.
  — <https://poolside.ai/blog/introducing-poolside-desktop-assistant>

## Best practices

- For agentic coding, keep enable_thinking on and preserve reasoning_content through assistant and tool turns; dropping prior thinking can stop later reasoning.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
- Use the serving integration's Laguna tool and reasoning parsers rather than generic defaults. The vLLM and TRT-LLM flag names differ, so copy the recipe for the chosen engine exactly.
  — <https://huggingface.co/poolside/Laguna-S-2.1>
- On the current FP8 checkpoint, retain the generation_config defaults, including top_k 20, rather than setting a separate temperature or top_p. Its card also warns that quality can degrade at long context.
  — <https://huggingface.co/poolside/Laguna-S-2.1-FP8>
- Treat the 22 GB 2080 Ti mixed-offload and DFlash configuration as one community testbed, then measure context length and throughput on the target hardware before adopting its settings.
  — <https://ai-muninn.com/zh-TW/blog/laguna-118b-moe-on-one-2080ti>

## Superseded by this

- Earlier poolside/Laguna-S-2.1-FP8 repository copies before the current FP8 artifact. Obsolete since 2026-08-01; the August card says the replacement is a new checkpoint with changed weights.
- Earlier poolside/Laguna-S-2.1-INT4 repository copies before the current INT4 artifact. Obsolete since 2026-08-02; the August card says the replacement is a new checkpoint with changed weights.

## Still unknown

- The retained source event is dated 2026-07-22, while Poolside dates the base-model launch 2026-07-21. Without the private source text, we cannot establish whether the source record was a delayed release post or a different same-subject item.
- No first-party Simplified-Chinese release or operating documentation was found in this pass. The dated Chinese source used here is Traditional Chinese community evidence and does not substitute for a zh-CN lane.
- No dated first-party source found in this pass says that the base poolside/Laguna-S-2.1 repository, rather than its FP8 and INT4 variants, was replaced after the July 21 launch.
- Poolside's benchmark figures are declared results under its stated harnesses and benchmark conditions; they are not independent production-performance proof.

## Sources

| source | title | read |
|---|---|---|
| https://poolside.ai/blog/introducing-laguna-s-2-1 | Introducing Laguna S 2.1 - Poolside | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1 | poolside/Laguna-S-2.1 - Hugging Face model card | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-FP8/commits/main | Commits - poolside/Laguna-S-2.1-FP8 | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-FP8 | poolside/Laguna-S-2.1-FP8 - Hugging Face model card | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-INT4/commits/main | Commits - poolside/Laguna-S-2.1-INT4 | 2026-09-06 |
| https://huggingface.co/poolside/Laguna-S-2.1-INT4 | poolside/Laguna-S-2.1-INT4 - Hugging Face model card | 2026-09-06 |
| https://poolside.ai/blog/introducing-poolside-desktop-assistant | Introducing Poolside Desktop Assistant, for macOS - Poolside | 2026-09-06 |
| https://openrouter.ai/poolside/laguna-s-2.1 | Laguna S 2.1 - API Pricing & Providers - OpenRouter | 2026-09-06 |
| https://chat.poolside.ai/ | Poolside Chat | 2026-09-06 |
| https://ai-muninn.com/zh-TW/blog/laguna-118b-moe-on-one-2080ti | [洋垃圾跑大模型 #2] 一張 22G 老卡跑 118B 的 coding 大模型:Poolside Laguna S 2.1 實戰 | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:poolside-laguna-s-2-1`, thread `laguna`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
