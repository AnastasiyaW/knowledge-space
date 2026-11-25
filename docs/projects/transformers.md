---
title: "Transformers: release-v5-20-0"
category: "projects"
date: 2026-07-16
tags: ["project", "release-v5-20-0", "transformers"]
aliases: ["Transformers: release-v5-20-0"]
---

# Transformers: release-v5-20-0

**Development line:** project:transformers · thread release-v5-20-0  
**Last event:** 2026-07-16 · 4 dated since 2026-07-03 · **Researched:** 2026-11-25 · confidence: high

## What it is

Transformers is Hugging Face’s Python library for loading pretrained models, running inference with pipelines and fine-tuning with Trainer.

It provides model, processor and task-level APIs for text, vision, audio and multimodal workloads.

Model availability and runtime requirements vary by architecture and release.

We use the stable package for production and test model-specific upgrades before deployment.

## Development line

- **2026-07-03 — Hugging Face Transformers Releases v5.13.0 with Support for Kimi, MiMo, Nemotron, Qwen3 ASR, and VideoPrism.** Hugging Face released Transformers v5.13.0, adding support for Kimi K2.5, 2.6, and 2.7, Xiaomi MiMo-V2-Flash, NVIDIA Nemotron 3.5 ASR / Nemotron ASR Streaming, Alibaba Qwen3 ASR and Forced Aligner, Zyphra ZAYA1-8B, and Google DeepMind VideoPrism.
  - v5.13.0 uses one Kimi architecture implementation for Kimi K2.5 through K2.7. (2026-07-03) — <https://github.com/huggingface/transformers/releases/tag/v5.13.0>
- **2026-07-11 — Patch release v5.13.1.** Patch release v5.13.1 enabled Transformers for the latest vllm release. It fixed custom code issues with new linear layer type names and \_LazyAutoMapping.register.
  - The patch also made legacy-layer remapping more defensive for custom models. (2026-07-11) — <https://github.com/huggingface/transformers/releases/tag/v5.13.1>
- **2026-07-15 — Transformers v5.14.0 release adds Inkling and TIPSv2 models.** On 2026-07-15 the Hugging Face Transformers project published release v5.14.0. The release adds the Inkling open-weights multimodal model \(975B total parameters, 41B active\) and TIPSv2 model variants. It notes breaking changes to GPTNeoX and GPTBigCode weight naming and attention backend behavior for vLLM compatibility. It also includes kernel fixes, a FlashAttention-based SDPA prefill update, and generation improvements such as multi-token prediction support.
  - Inkling accepts text, image and audio inputs and generates text. The release’s 975B total and 41B active parameter figures apply to that integration. (2026-07-15) — <https://github.com/huggingface/transformers/releases/tag/v5.14.0>
- **2026-07-16 — Transformers: release-v5-20-0 update.** Transformers v5.14.1 fixed Inkling-related failures affecting assisted generation with EncoderDecoderCache and SDPA prefill with StaticCache without padding.

## What changed

v5.13.0 added Kimi, MiMo, Nemotron ASR, Qwen3 ASR, ZAYA1-8B and VideoPrism integrations. v5.13.1 repaired vLLM and custom-code compatibility around updated linear-layer names and lazy auto-mapping registration. v5.14.0 added Inkling and TIPSv2 support, generation updates, and compatibility-relevant GPTNeoX/GPTBigCode changes. v5.14.1 corrected Inkling integration issues in assisted generation and SDPA prefill.

## How to use this

1. Install the stable Transformers package, then verify the installation with a small pipeline inference call.
  — <https://huggingface.co/docs/transformers/main/installation>
2. Load a pretrained model, run inference through Pipeline, or fine-tune through Trainer according to the task.
  — <https://huggingface.co/docs/transformers/en/quicktour>
3. For Inkling specifically, upgrade to at least v5.14.0 and use the any-to-any pipeline with a compatible checkpoint and GPU configuration.
  — <https://github.com/huggingface/blog/blob/main/thinkingmachines-inkling.md>

## Best practices

- Prefer the stable package for normal use. Install from source only when testing unreleased changes or a pending fix, because the latest source version may not be stable.
  — <https://huggingface.co/docs/transformers/main/installation>
- Treat v5.14.0 as a migration point for code relying on GPTNeoX \`embed\_out\` naming or GPTBigCode attention-backend behavior.
  — <https://github.com/huggingface/transformers/releases/tag/v5.14.0>
- Plan capacity before local inference for full Inkling checkpoints: the documented bf16 checkpoint requires 2 TB VRAM and the NVFP4 checkpoint requires 600 GB VRAM.
  — <https://github.com/huggingface/blog/blob/main/thinkingmachines-inkling.md>

## Superseded by this

- Code expecting GPTNeoX \`embed\_out\` as the output head is superseded by the v5.14.0 remapping to \`lm\_head\`.
  — <https://github.com/huggingface/transformers/releases/tag/v5.14.0>
- Using v5.14.0 for affected Inkling assisted-generation and unpadded StaticCache SDPA prefill paths is superseded by the v5.14.1 fixes.
  — <https://github.com/huggingface/transformers/releases?after=v4.2.0>

## Still unknown

- The subject display names release-v5-20-0, but all reviewed events concern v5.13.0 through v5.14.0. The supplied subject name may be a branch-label mismatch.
- No qualifying Simplified-Chinese source was retained.
- No practitioner community discussion meeting the required evidence standard was found in the completed searches.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/huggingface/transformers/releases/tag/v5.13.0 | Release v5.13.0 | 2026-11-25 |
| https://github.com/huggingface/transformers/releases/tag/v5.13.1 | Patch release v5.13.1 | 2026-11-25 |
| https://github.com/huggingface/transformers/releases/tag/v5.14.0 | Release v5.14.0 | 2026-11-25 |
| https://github.com/huggingface/transformers/releases?after=v4.2.0 | Transformers releases | 2026-11-25 |
| https://huggingface.co/docs/transformers/main/installation | Transformers installation | 2026-11-25 |
| https://huggingface.co/docs/transformers/en/quicktour | Transformers quickstart | 2026-11-25 |
| https://github.com/huggingface/blog/blob/main/thinkingmachines-inkling.md | Thinking Machines Inkling on Hugging Face | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:transformers, thread release-v5-20-0, 4 dated events 2026-07-03 → 2026-07-16.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
