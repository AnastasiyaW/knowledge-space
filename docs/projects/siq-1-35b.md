---
title: SIQ-1-35B — Public model and demo
category: projects
date: 2026-06-17
tags: [project, public-model-and-demo, siq-1-35b, siq_1_35b]
aliases: ["SIQ-1-35B"]
---

# SIQ-1-35B — Public model and demo

**Development line:** `project:siq-1-35b` · thread `public-model-and-demo`  
**Last event:** 2026-06-17 · 1 dated since 2026-06-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

SIQ-1-35B — an Apache-2.0 finetune of Qwen/Qwen3.6-35B-A3B for local coding, reasoning, and tool use.

- Thinking and no-think chat modes
- BF16 and GGUF distributions
- Local OpenAI-compatible serving

## Development line

- **2026-06-17 — SIQ-1-35B public model and agent demo were linked.** On 2026-06-17, SIQ-1-35B was linked to a public Hugging Face model page and a Hermes-agent ZeroGPU Space. Autoresearch, parameter-golf, and benchmark repositories were linked alongside it. The links confirm the public files, but not the author's benchmark claims.

## What changed

2026-06-17 — The model card renamed SIQ-1-35B to “SIQ-1-tiny-35b”. It presents the model as a universal agent for autoresearch, coding, and reasoning. The update added benchmark charts, serving profiles, prompts, and a demo link, without a weight upload recorded that day.

## How to use this

From 2026-06-17, treat SIQ-1-35B as a public model with an agent demo. Verify capabilities and benchmark claims independently before relying on them.

1. Start with the Q4_K_M GGUF locally: `llama serve -hf AlexWortega/SIQ-1-35B:Q4_K_M`, then use its localhost OpenAI-compatible endpoint.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
2. For tool calls and thinking, use the documented llama.cpp profile with `--jinja`, GPU offload, and a 131072-token context split across four slots.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
3. For BF16 serving, use the documented SGLang configuration with tensor parallelism 2 plus the Qwen3 reasoning and tool-call parsers.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
4. Set `enable_thinking=true`, `Reasoning effort: high`, and temperature 0 for hard reasoning. Turn thinking off for direct replies.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
5. Before enabling MTP speculative decoding, fetch the current companion GGUF and confirm it loads with the selected trunk quantization.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B/commit/cb6f95ec76411517babbfa6a854f7f0425313ff4>

## Best practices

- Keep `--jinja` enabled for llama.cpp: the documented Qwen chat template carries the thinking and tool tags.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
- Report benchmark results with precision, prompt mode, and sampling settings; the card distinguishes Q4 co-measurement from its BF16 result.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B>
- Treat MTP as version-sensitive: the companion was corrected on 2026-06-23 after an incorrect draft layer, and users reported earlier load failures.
  — <https://huggingface.co/AlexWortega/SIQ-1-35B/discussions/2>
- Use a local runtime rather than the hosted ZeroGPU demo until it recovers; it returned a missing `libcuda.so.1` runtime error when read.
  — <https://huggingface.co/spaces/AlexWortega/hermes-agent-zerogpu>
- Do not present the card’s one-A6000, two-hour test as an official Parameter Golf leaderboard result; that project scopes leaderboard submissions to ten minutes on 8×H100.
  — <https://github.com/openai/parameter-golf>

## Superseded by this

- 2026-06-17 — The model is a `finetune`, not an adapter. The release history explicitly corrects this relationship.
- 2026-06-23 — Earlier vocab-only DFlash and wrong-layer MTP companions are obsolete; the repository replaced them with the Qwen3.6-35B-A3B MTP layer and updated tensor names.

## Still unknown

- Independent evaluations for SIQ claims are missing. Treat GPQA, autoresearch, coding, and BullshitBench figures as author-reported.
- SIQ-1-35B is the repository name while its 2026-06-17 card calls the same model SIQ-1-tiny-35b. Commit history shows no separate model identities.
- Karpathy autoresearch and OpenAI Parameter Golf use different training and evaluation setups. Sources show no direct training-data lineage to SIQ-1-35B.
- SIQ is tagged as text generation although its Qwen3.6 base is multimodal. The model card does not confirm vision input support.
- The hosted ZeroGPU failure is a hosted-runtime issue, not evidence that local GGUF or BF16 serving fails.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/AlexWortega/SIQ-1-35B | AlexWortega/SIQ-1-35B model card | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commits/d6a09a9f86bf21d60db5b575578a1df47d222adf/README.md | SIQ-1-35B README commit history | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commits/cb6f95ec76411517babbfa6a854f7f0425313ff4 | SIQ-1-35B repository commit history through the MTP correction | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/commit/cb6f95ec76411517babbfa6a854f7f0425313ff4 | Correct MTP layer from Qwen3.6-35B-A3B commit | 2026-09-05 |
| https://huggingface.co/AlexWortega/SIQ-1-35B/discussions/2 | SIQ-1-35B MTP loading discussion | 2026-09-05 |
| https://huggingface.co/spaces/AlexWortega/hermes-agent-zerogpu | Hermes · SIQ-1-35B ZeroGPU Space | 2026-09-05 |
| https://github.com/karpathy/autoresearch | karpathy/autoresearch | 2026-09-05 |
| https://github.com/openai/parameter-golf | openai/parameter-golf | 2026-09-05 |
| https://github.com/petergpt/bullshit-benchmark | BullshitBench v2 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:siq-1-35b`, thread `public-model-and-demo`, 1 dated events 2026-06-17 → 2026-06-17.
- **Practical note:** From 2026-06-17, treat SIQ-1-35B as having a linked public model artifact and agent-demo entry point, while independently verifying capabilities and benchmark claims before relying on them.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.