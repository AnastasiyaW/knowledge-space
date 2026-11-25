---
title: Qwopus3.5-9B-Coder
category: projects
date: 2026-05-18
tags: [project, qwopus3-5-9b-coder, qwopus3-5-9b-coder-gguf-distribution, qwopus3_5_9b_coder]
aliases: ["Qwopus3.5-9B-Coder"]
---

# Qwopus3.5-9B-Coder

**Development line:** `project:qwopus3-5-9b-coder` · thread `qwopus3-5-9b-coder-gguf-distribution`  
**Last event:** 2026-05-18 · 1 dated since 2026-05-18 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Qwopus3.5-9B-Coder is a 9B coding and tool-calling model from a single community author, distributed as GGUF files for local inference.

- What: supervised fine-tune (Unsloth) of Qwopus3.5-9B-v3.5, aimed at agentic coding, tool calling and reasoning.
- Users: local inference users on llama.cpp-style runtimes; the card's examples use llama.cpp.
- Files: Q3_K_M (4.62 GB) to Q8_0 (9.53 GB). Vision needs a separate mmproj.gguf in the same directory.
- Limits: "released purely as an experimental community version", "only for research and exploration use", and "has not undergone comprehensive general performance evaluation". The card warns of capability decay outside programming tasks. License: Apache-2.0.

As of 2026-11, the benchmarks on the card are the author's own or unattributed, so treat them as self-reported.

## Development line

- **2026-05-18 — Qwopus3.5-9B-Coder GGUF distribution recorded on Hugging Face.** On 2026-05-18, a Hugging Face repository appeared for a GGUF distribution of Qwopus3.5-9B-Coder. This artifact provides local inference for the project. The link alone does not confirm exact quantization, provenance, or an upstream release.

## What changed

- No dated version is verified. The model card (read 2026-11-21) gives file sizes and a training description but no release history.

## How to use this

1. Pick a quantization by memory. Q4_K_M (5.63 GB) is the middle option; Q8_0 (9.53 GB) is the largest listed.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>
2. For vision, place mmproj.gguf in the same directory as the main model.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>
3. Use temperature 1, which the card says follows Qwen3.5's official recommendation. For tool calls, match the prompt format and system prompt used in training.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>
4. Hide or parse the `<think>` output in front-end apps, as the card advises.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>
5. Beyond 32K context, use the YaRN scaling the card shows (ctx-size 131072, rope-scale 4, yarn-orig-ctx 32768). The author says long-context results vary by backend, quantization and hardware.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>

## Best practices

- Run your own coding and tool-call tests before adoption. The card's tool-calling numbers come from the author and one unnamed community tester.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>
- Keep the training prompt format. The card states that tool calling depends on it.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>
- Do not use it as a general-purpose model. The card warns that capability outside programming may decline.
  — <https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF>

## Superseded by this

- Nothing verified as obsolete. The card names Qwopus3.5-9B-v3.5 as its base; this page does not evaluate that base.

## Still unknown

- The base lineage is inconsistent within the card. The model tree lists Qwen3.5-9B ancestors, while the acknowledgements refer to a "Qwen3.6 base model".
- The SWE-bench Verified figure (53.89) has no named evaluator or harness.
- The GGUF repository's release date is not shown on the page read.
- Data quality of the "trace inversion" sets is not verified; the card says the reasoning chains are not checked against the source models.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF | Jackrong/Qwopus3.5-9B-Coder-GGUF — model card | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwopus3-5-9b-coder`, thread `qwopus3-5-9b-coder-gguf-distribution`, 1 dated events 2026-05-18 → 2026-05-18.
- **Practical note:** A 9B community coding/tool-calling GGUF, Apache-2.0, quantizations 4.62–9.53 GB. Use the card's prompt format and settings; benchmarks are self-reported, so run your own tests first.
- **Confidence:** medium. The card is verified; its benchmarks and base lineage are inconsistent or self-reported. Dated supersedes above are the authority for what is obsolete.
