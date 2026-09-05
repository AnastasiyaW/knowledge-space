---
title: Qwen3.8-Flash-Next — Qwen
category: projects
date: 2026-08-26
tags: [project, qwen, qwen3-8-flash-next]
aliases: ["Qwen3.8-Flash-Next"]
---

# Qwen3.8-Flash-Next — Qwen

**Development line:** `project:qwen3-8-flash-next` · thread `qwen`  
**Last event:** 2026-08-26 · 1 dated since 2026-08-26 · **Researched:** 2026-09-05 · confidence: high

## What it is

Qwen3.8-Flash-Next is an open multimodal MoE model for developers who need vision, text, coding, and agent workflows.

- Runtimes: runs across Transformers, vLLM, SGLang, TokenSpeed, and llama.cpp.
- Architecture: uses Gated DeltaNet, Qwen Sparse Attention, Gated Residual, and n-gram embeddings.

125B parameters in the base model, 51B parameters in n-gram embedding tables, 6B active parameters per token, and a 262 144 token context in the official serving example. The model fits open-weight experiments; Qwen Cloud positions managed Qwen3.8-Flash separately for production APIs.

## Development line

- **2026-08-26 — Qwen3.8-Flash-Next project resources were documented.** The release provides a multimodal MoE model and an early preview of the Qwen4 architecture.

## What changed

- 2026-08-26 — open weights released for Qwen3.8-Flash-Next, an open multimodal MoE model and early preview of the Qwen4 architecture.
- 2026-08-31 — technical report published with architecture ablations, efficiency evaluation, and training stability analysis.

## How to use this

As of 2026-08-26, verify Qwen3.8-Flash-Next through the linked source repository, model-hosting resources, and demo before selecting a checkpoint or deployment route.

1. For an image and text prototype, load `Qwen/Qwen3.8-Flash-Next` through the Transformers `image-text-to-text` pipeline or with `AutoProcessor` and `AutoModelForMultimodalLM`.
  — <https://huggingface.co/Qwen/Qwen3.8-Flash-Next>
2. For a self-hosted OpenAI-compatible API, run vLLM: the official example uses tensor parallelism 4, `--max-model-len 262144`, reasoning parser `qwen3`, and tool-call parser `qwen3_coder`.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
3. Use Qwen Cloud when we do not want to maintain open-weights infrastructure: managed Qwen3.8-Flash is compatible with OpenAI and Anthropic APIs.
  — <https://www.qwencloud.com/>

## Best practices

- Enable reasoning parser `qwen3` and tool-call parser `qwen3_coder` together for tool calls; the official recipe provides no serving instructions without both.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- On Apple Silicon, use mlx-vlm or prebuilt MLX quantizations; pick compatible GGUF weights for llama.cpp instead of the raw checkpoint.
  — <https://github.com/QwenLM/Qwen3.8-Flash-Next>
- Do not apply the 262K limit from the self-hosted example to the managed model: Qwen Cloud specifies 1M context for Qwen3.8-Flash separately.
  — <https://www.qwencloud.com/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- For the 2026-08-26 event: the official repository dates the release to 2026-08-26 and notes open weights for Qwen3.8-Flash-Next, a 125B parameter multimodal MoE model with 6B active parameters per token; source_date=2026-08-26; source_url=https://github.com/QwenLM/Qwen3.8-Flash-Next.
- New event: 2026-08-31 — the technical report evaluated 14 pre-training benchmarks: the model beats its 397B-A17B predecessor on eight and trails on the rest by no more than 2,6 points, using roughly a third of active parameters, a third of training tokens, and about one ninth of FLOPs; source_date=2026-08-31; source_url=https://arxiv.org/abs/2608.30320.
- The model card calls Qwen3.8-Flash a production release based on Flash-Next with 1M context and built-in tools, but gives no date for the transition; we cannot tie it to 2026-08-26 or record it as a dated supersedes.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/QwenLM/Qwen3.8-Flash-Next | QwenLM/Qwen3.8-Flash-Next | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.8-Flash-Next | Qwen/Qwen3.8-Flash-Next model card | 2026-09-05 |
| https://arxiv.org/abs/2608.30320 | On the Design of Qwen3.8-Next Architecture: Evaluation, Efficiency, and Training Stability | 2026-09-05 |
| https://www.qwencloud.com/ | QwenCloud — AI-Native Models, Tools & Apps Platform | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-8-flash-next`, thread `qwen`, 1 dated events 2026-08-26 → 2026-08-26.
- **Practical note:** As of 2026-08-26, practitioners should verify Qwen3.8-Flash-Next through its linked source repository, model-hosting resources, and demo before selecting a checkpoint or deployment route.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
