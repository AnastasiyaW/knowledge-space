---
title: TimeLens2
category: projects
date: 2026-07-22
tags: [project, timelens2, timelens2-development]
aliases: ["TimeLens2"]
---

# TimeLens2

**Development line:** `project:timelens2` · thread `timelens2-development`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-05 · confidence: high

## What it is

TimeLens2 is an open Qwen3-VL-based model family for researchers and video-search builders. It converts a video plus text query into one or more evidence intervals.
Released sizes are 2B, 4B, and 8B. It handles short, long, repeated-event, question-form, and egocentric grounding. The 8B model reports 48.0 average mIoU across seven benchmarks. Local inference needs a compatible Transformers and video stack rather than a hosted inference provider.

## Development line

- **2026-07-22 — TimeLens2 public project resources were linked.** On 2026-07-22, the project linked its public project page, GitHub source repository, Hugging Face collection, and temporal-grounding Space. The initial links gave no specific version, model configuration, or feature claim.

## What changed

2026-07-22 — TimeLens2 launched as a generalist temporal-grounding release with a project page, Apache-2.0 code, TimeLens2-93K data, 2B/4B/8B checkpoints, and an 8B demo.
The paper, submitted 2026-07-19, frames the task as set-valued interval prediction. It reports Qwen3-VL backbone gains of 14.2 mIoU (2B), 13.0 (4B), and 18.1 (8B).
On 2026-07-27, matching 2B/4B/8B SFT checkpoints arrived for rollout generation and GRPO reproduction.

## How to use this

From 2026-07-22, start with the project page and repository for TimeLens2, and use the linked Hugging Face collection and Space for public assets and demos.

1. Install the inference dependencies, load `MCG-NJU/TimeLens2-8B` with Transformers, and provide a local video URI.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
2. Ask for all relevant spans in seconds and require a JSON array of `[start, end]` pairs; decode the generated response as the evidence set.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
3. For reproduction, download the required videos, run SFT, optionally regenerate rollouts from the matching `-SFT` checkpoint, then run GRPO and evaluation.
  — <https://github.com/MCG-NJU/TimeLens2>

## Best practices

- Request all matching spans instead of a single moment, and constrain the response format to timestamp pairs.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
- Use a separate rollout output root for every model, data, and seed combination so concurrent jobs with identical shard names do not overwrite outputs.
  — <https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md>
- Do not start GRPO until rollout merging succeeds and every training row has the expected eight responses.
  — <https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The 2026-07-22 release links an 8B Space, but the page exposes no operational limits or deployment configuration. The official 8B model card confirms it is not deployed by an inference provider, so the demo is not a supported hosted API.

## Sources

| source | title | read |
|---|---|---|
| https://mcg-nju.github.io/TimeLens2/ | TimeLens2 — Generalist Video Temporal Grounding with Multimodal LLMs | 2026-09-05 |
| https://github.com/MCG-NJU/TimeLens2 | MCG-NJU/TimeLens2 repository | 2026-09-05 |
| https://huggingface.co/collections/MCG-NJU/timelens2 | TimeLens2 collection | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/timelens2-8b-temporal-grounding | TimeLens2-8B temporal-grounding Space | 2026-09-05 |
| https://arxiv.org/abs/2607.17423 | TimeLens2: Generalist Video Temporal Grounding with Multimodal LLMs | 2026-09-05 |
| https://huggingface.co/MCG-NJU/TimeLens2-8B | MCG-NJU/TimeLens2-8B model card | 2026-09-05 |
| https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md | TimeLens2 Rollout and GRPO guide | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:timelens2`, thread `timelens2-development`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** From 2026-07-22, start from the project page and repository for TimeLens2, using the linked Hugging Face collection and Space as public asset and demo entry points; exact capabilities remain unverified.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
