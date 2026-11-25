---
title: Qwen3.6-34B-80L-Fable-5-Heretic
category: projects
date: 2026-06-29
tags: [project, qwen3-6-34b-80l-fable-5-heretic]
aliases: ["Qwen3.6-34B-80L-Fable-5-Heretic"]
---

# Qwen3.6-34B-80L-Fable-5-Heretic

**Development line:** `project:qwen3-6-34b-80l-fable-5-heretic` · thread `qwen3-6-34b-80l-fable-5-heretic`  
**Last event:** 2026-06-29 · 1 dated since 2026-06-29 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Qwen3.6-34B-80L-Fable-5-Heretic is a BF16 derivative of Qwen3.6-27B for self-hosting with Transformers or vLLM.

- 80 layers, ~34B parameters, and context claimed up to 256K.
- QLoRA training on 4 665 Fable-5 agentic CoT traces.
- MTP weights in the repository for speculative decoding.

## Development line

- **2026-06-29 — Qwen3.6-34B-80L-Fable-5-Heretic model page recorded on Hugging Face.** A Qwen3.6-27B derivative expanded from 64 to 80 layers, claiming ~34B parameters, BF16 weights, 4 665 QLoRA traces, and 15 MTP weights. We found no independent dated confirmation of publication on 2026-06-29.

## What changed

2026-06-29 — We recorded the link to hiebo/Qwen3.6-34B-80L-Fable-5-Heretic. The model card details this step: the Qwen3.6-27B derivative expands from 64 to 80 layers, claiming ~34B parameters, BF16 weights, 4 665 QLoRA traces, and 15 MTP weights. We found no independent dated confirmation of publication on 2026-06-29.

After 2026-06-29 — We found no verified dated changes to the model. Mirrors on Hugging Face redistribute the same artifacts rather than a new version.

## How to use this

From 2026-06-29, locate the Qwen3.6-34B-80L-Fable-5-Heretic entry on Hugging Face and verify the model card, files, licensing, provenance, and compatibility before adopting it.

1. Load the exact ID `hiebo/Qwen3.6-34B-80L-Fable-5-Heretic` through Transformers with `device_map="auto"` and test a short prompt before loading the full context.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
2. Serve with the vLLM command from the model card using BF16 and an explicit `--max-model-len`. Start with a lower limit until you measure KV-cache and GPU memory.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>

## Best practices

- Do not carry over base model settings automatically: the custom derivative changes the layer count and adds MTP weights, so verify loader, tokenizer, and generation pipeline compatibility with a local smoke test first.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- Treat the claimed 78% acceptance rate and 2× throughput as a model card hypothesis; measure acceptance, latency, and quality on your own task suite.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- The base Qwen model recommends a large generation limit for complex tasks; treat that as an experimental setting, not proof of derivative quality.
  — <https://huggingface.co/Qwen/Qwen3.6-27B>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The model card is an author claim from a personal repository; we found no independent evaluations, reproducible training runs, or verified speedups.
- Primary sources omit exact publication and update dates, so we cannot confirm the release occurred on 2026-06-29.
- The schema lacks `event_findings` and `new_events` fields; we recorded relevant findings in `what_changed` and `unknowns`.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic | hiebo/Qwen3.6-34B-80L-Fable-5-Heretic — model card | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.6-27B | Qwen/Qwen3.6-27B — official model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-6-34b-80l-fable-5-heretic`, thread `qwen3-6-34b-80l-fable-5-heretic`, 1 dated events 2026-06-29 → 2026-06-29.
- **Practical note:** From 2026-06-29, practitioners can locate the Qwen3.6-34B-80L-Fable-5-Heretic Hugging Face entry and should verify the model card, files, licensing, provenance, and compatibility before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.