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

Qwen3.6-34B-80L-Fable-5-Heretic is a BF16 derivative of Qwen3.6-27B for teams that deploy models locally using Transformers or vLLM.

- 80 layers, ~34B parameters, context claimed up to 256K.
- Training claimed on 4 665 Fable-5 agentic CoT traces with QLoRA.
- MTP weights in the repository for speculative decoding.

## Development line

- **2026-06-29 — Qwen3.6-34B-80L-Fable-5-Heretic model page recorded on Hugging Face.** The Qwen3.6-27B derivative expands from 64 to 80 layers, claiming ~34B parameters, BF16 weights, 4 665 QLoRA traces, and 15 MTP weights. We found no independent dated confirmation for publication on 2026-06-29.

## What changed

2026-06-29 — We recorded the link to hiebo/Qwen3.6-34B-80L-Fable-5-Heretic. The model card details this step: the Qwen3.6-27B derivative expands from 64 to 80 layers, claiming ~34B parameters, BF16 weights, 4 665 QLoRA traces, and 15 MTP weights. We found no independent dated confirmation for publication on 2026-06-29.

После 2026-06-29 — We found no reliable dated changes for the model. Hugging Face hosts copies of the repository, but they distribute the existing artifacts rather than a new version.

## How to use this

From 2026-06-29, practitioners can locate the Qwen3.6-34B-80L-Fable-5-Heretic Hugging Face entry and should verify the model card, files, licensing, provenance, and compatibility before adopting it.

1. Load the exact ID `hiebo/Qwen3.6-34B-80L-Fable-5-Heretic` in Transformers with `device_map="auto"` and test a short prompt before loading full context.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
2. For serving, use the card's vLLM command with BF16 and an explicit `--max-model-len`; start with a lower limit if you have not measured KV-cache and GPU memory.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>

## Best practices

- Do not copy base model settings automatically: the custom derivative changes layer count and adds MTP weights, so verify loader, tokenizer, and generation pipeline compatibility on a local smoke test first.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- Treat the reported 78% acceptance rate and 2× throughput as a hypothesis from the model card; measure acceptance, latency, and quality on your own workload.
  — <https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic>
- For complex tasks, base Qwen recommends a large output limit; use this as a separate experimental setting rather than proof of the derivative's quality.
  — <https://huggingface.co/Qwen/Qwen3.6-27B>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The model card represents claims from the repository author; we found no independent evaluation results, reproducible training runs, or verified speedups.
- Primary verified pages omitted the release date and repository update timestamps, so we cannot confirm that the release occurred on 2026-06-29.
- Fields `event_findings` and `new_events` are absent from the required output schema; relevant findings appear in `what_changed` and `unknowns`.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/hiebo/Qwen3.6-34B-80L-Fable-5-Heretic | hiebo/Qwen3.6-34B-80L-Fable-5-Heretic — model card | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3.6-27B | Qwen/Qwen3.6-27B — official model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-6-34b-80l-fable-5-heretic`, thread `qwen3-6-34b-80l-fable-5-heretic`, 1 dated events 2026-06-29 → 2026-06-29.
- **Practical note:** From 2026-06-29, practitioners can locate the Qwen3.6-34B-80L-Fable-5-Heretic Hugging Face entry and should verify the model card, files, licensing, provenance, and compatibility before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.