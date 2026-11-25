---
title: "Inkling 2 Mini: inkling-2-mini-release — Inkling 2 Mini Release"
category: "projects"
date: 2026-11-22
tags: ["inkling-2-mini", "inkling-2-mini-release", "project"]
aliases: ["Inkling 2 Mini: inkling-2-mini-release"]
---

# Inkling 2 Mini: inkling-2-mini-release — Inkling 2 Mini Release

Inkling 2 Mini is an open-weights multimodal model for local coding agents, an alternative to Qwen3.8-27B.

**Development line:** project:inkling-2-mini · thread inkling-2-mini-release  
**Last event:** 2026-11-22 · 2 dated since 2026-11-22 · **Researched:** 2026-11-24 · confidence: medium

## What it is

Inkling 2 Mini is an open-weights multimodal language model for local agentic software engineering and tool execution. It is an alternative to larger frontier models such as Qwen3.8-27B. It takes text and image input and produces text. It does tool use and multi-step reasoning, with a context window of up to one million tokens.

- 24 transformer layers, where 12 intermediate layers loop three times per token
- About 5.4 billion effective active parameters out of 26.4 billion total
- About twenty gigabytes of memory under low-bit quantization

It runs on a single desktop GPU or a thirty-two-gigabyte laptop. Full context is still limited by the unified memory available.

## Development line

- **2026-11-22 — Thinking Machines Lab releases open Inkling 2 Mini looped multimodal model.** On 2026-11-22, Thinking Machines Lab released Inkling 2 Mini, an open multimodal looped transformer under Apache 2.0 with about 26.4B total parameters (3.4B active). The authors report pruning from 384 to 128 experts per layer, healing on 1T distilled tokens, and RL post-training. They also report benchmark results (e.g., SWE-bench Verified 79.2%, DeepSWE v1.1 48.2%) and claim roughly 4x faster and 6x cheaper per task than Qwen3.8-27B.
- **2026-11-22 — Uncensored Inkling 2 Mini GGUF versions released.** Developers released three quantized GGUF versions (about 8.67 to 16.53 GB) of the 26.4B-parameter model, described as uncensored. Reported tests showed the refusal rate falling from 100% to 0% while keeping 98% of MMLU accuracy.
- **2026-11-22 — other reporting on this date.**
  - The release documentation describes 24 layers, with 12 intermediate layers looping three times per token and independent KV cache allocations. This extends context to one million tokens. The weights are packaged for local 20 GB deployment via vLLM and Ollama. (2026-11-22) — <https://huggingface.co/thinkingmachines/Inkling-2-Mini>
  - The quantization packages offer three GGUF weight configurations, from 8.67 GB to 16.53 GB, for llama.cpp. They alter the alignment layers to cut refusals to 0% and keep about 98% of baseline evaluation scores. (2026-11-22) — <https://huggingface.co/AtomicChat/Inkling-2-Mini-Uncensored-GGUF>

## What changed

Thinking Machines Lab pruned the experts from 384 to 128 per layer and used a looped transformer, with distillation and reinforcement learning post-training. The community then added quantized GGUF builds that remove refusals and keep benchmark task accuracy.

## How to use this

1. Load the weights from the thinkingmachines/Inkling-2-Mini repository. Use a supported engine such as vLLM for API serving or local orchestration.
  — <https://huggingface.co/thinkingmachines/Inkling-2-Mini>
2. On a workstation with limited VRAM, download the quantized GGUF files from AtomicChat/Inkling-2-Mini-Uncensored-GGUF. Run them in llama.cpp or a compatible desktop interface.
  — <https://huggingface.co/AtomicChat/Inkling-2-Mini-Uncensored-GGUF>

## Best practices

- Allow at least 20 GB of unified memory for quantized runs. Use a runtime that supports recurrent looped transformer layers, so deep reasoning cycles do not fail.
  — <https://huggingface.co/thinkingmachines/Inkling-2-Mini>
- Pick a quantization tier between 8.67 GB and 16.53 GB to fit the host memory. This trades decoding throughput against how much accuracy is kept.
  — <https://huggingface.co/AtomicChat/Inkling-2-Mini-Uncensored-GGUF>

## Superseded by this

- For local developer tasks, the pruned 128-expert recurrent transformer replaces dense unpruned 384-expert Mixture-of-Experts designs that have no recurrent layer looping.
  — <https://huggingface.co/thinkingmachines/Inkling-2-Mini>

## Still unknown

- Secondhand reports mention an announcement before the repository went up, but no canonical article could be verified. Community discussion threads and detailed independent benchmark logs could not be checked either.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/thinkingmachines/Inkling-2-Mini | thinkingmachines/Inkling-2-Mini · Hugging Face | 2026-11-24 |
| https://huggingface.co/AtomicChat/Inkling-2-Mini-Uncensored-GGUF | AtomicChat/Inkling-2-Mini-Uncensored-GGUF · Hugging Face | 2026-11-24 |

## Agent brief {#agent-brief}

- **Subject:** project:inkling-2-mini, thread inkling-2-mini-release, 2 dated events 2026-11-22 → 2026-11-22.
- **Practical note:** see the usage and practice sections above, including their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
