---
title: Qwythos-27B-v1
category: projects
date: 2026-08-03
tags: [project, qwythos, qwythos-27b-v1, qwythos-27b-v1-release]
aliases: ["Qwythos-27B-v1"]
---

# Qwythos-27B-v1

**Development line:** `project:qwythos-27b-v1` · thread `qwythos-27b-v1-release`  
**Last event:** 2026-08-03 · 1 dated since 2026-08-03 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Qwythos-27B-v1 is an open-weight bf16 checkpoint on Qwen3.5-27B for developers who need a local model with function calling and image input.

- Context window: provides 1,048,576 tokens through YaRN 4.0.
- Vision tower and native multi-token prediction: preserved from the base architecture.
- Post-training pipeline: full SFT → DPO → ESFT as v1 before RL.

The native window is 262,144 tokens; the 1M configuration degrades short-context quality.

The checkpoint fits self-hosted agent and tool workflows, but the vision tower was not fine-tuned and sensitive deployments require external review.

## Development line

- **2026-08-03 — Qwythos-27B-v1 linked on Hugging Face.** Third parties uploaded FancieF/Qwythos-27B-v1-MLX-VLM-4bit, FancieF/Qwythos-27B-v1-MLX-VLM-bf16 and a separate MTP draft; this is not a new official checkpoint.

## What changed

2026-07-29 — Empero released Qwythos-27B-v1 and an official GGUF set: a 27B full-parameter model on Qwen3.5-27B under Apache-2.0, with 1M context, vision and MTP. 2026-08-03 — Third-party MLX ports of the base Qwythos-27B-v1 appeared: FancieF/Qwythos-27B-v1-MLX-VLM-4bit, FancieF/Qwythos-27B-v1-MLX-VLM-bf16 and a separate MTP draft; this is not a new official checkpoint.

## How to use this

From 2026-08-03, practitioners should use the linked Hugging Face model page as the recorded reference for Qwythos-27B-v1 and verify its model-card details and availability there before use.

1. For local deployment on a 24 GB GPU, start with official GGUF Q4_K_M; add `mmproj-Qwythos-27B-F16.gguf` for image input.
  — <https://empero.org/writing/qwythos-27b-the-long-awaited-27b>
2. For Transformers, load `empero-ai/Qwythos-27B-v1` via `AutoModelForImageTextToText` and use the built-in chat template.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
3. For OpenAI-compatible serving, run vLLM or SGLang; near 1M context, vLLM requires `VLLM_ALLOW_LONG_MAX_MODEL_LEN=1` and explicit `--max-model-len`.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
4. For function calling, pass definitions in `tools=[...]` to the built-in chat template and handle standard tool call blocks.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>

## Best practices

- For agentic and tool use, start with temperature 0.6, top_p 0.95, top_k 20, repetition_penalty 1.05 and a budget of at least 16,384 new tokens.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
- If 1M context is not needed, lower the YaRN factor to 2.0 for about 512k or revert to native 262k configuration for better short-context quality.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>
- For K-quants, pick official GGUF: it keeps the sensitive Gated-DeltaNet state path at Q8_0 or higher instead of quantizing it with the remaining weights.
  — <https://empero.org/writing/qwythos-27b-the-long-awaited-27b>
- Do not serve the uncensored checkpoint to users without application-level policy, review and access controls.
  — <https://huggingface.co/empero-ai/Qwythos-27B-v1>

## Superseded by this

- 2026-08-03: treating this date as the release of base Qwythos-27B-v1 is obsolete; the primary announcement was 2026-07-29, while 3 August refers to third-party MLX conversions.

## Still unknown

- The official model card describes v1 and plans for RL-v2, but primary sources do not confirm that Qwythos-27B-v2 was released by 2026-09-05.
- The 3 August list confirms third-party MLX conversions, but gives no independent evaluation of quality, compatibility or preserved capabilities of the original model.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/empero-ai/Qwythos-27B-v1 | empero-ai/Qwythos-27B-v1 · Hugging Face | 2026-09-05 |
| https://huggingface.co/models?other=base_model%3Aquantized%3Aempero-ai%2FQwythos-27B-v1 | Quantized Models for empero-ai/Qwythos-27B-v1 – Hugging Face | 2026-09-05 |
| https://empero.org/writing/qwythos-27b-the-long-awaited-27b | Qwythos-27B-v1: the long-awaited 27B — Empero | 2026-09-05 |
| https://huggingface.co/models?other=qwythos | Models – Hugging Face | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwythos-27b-v1`, thread `qwythos-27b-v1-release`, 1 dated events 2026-08-03 → 2026-08-03.
- **Practical note:** From 2026-08-03, practitioners should use the linked Hugging Face model page as the recorded reference for Qwythos-27B-v1 and verify its model-card details and availability there before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
