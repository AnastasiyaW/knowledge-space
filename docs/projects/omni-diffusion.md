---
title: Omni-Diffusion
category: projects
date: 2026-03-11
tags: [multimodal_models, omni-diffusion, omni-diffusion-development, project]
aliases: ["Omni-Diffusion"]
---

# Omni-Diffusion

**Development line:** `project:omni-diffusion` · thread `omni-diffusion-development`  
**Last event:** 2026-03-11 · 1 dated since 2026-03-11 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Omni-Diffusion is an open any-to-any multimodal model built on masked discrete diffusion for researchers and engineers who need one shared stack instead of separate autoregressive models.

- Text-to-image, speech-to-image, VQA, spoken VQA, ASR, and TTS.
- Joint generation and understanding across text, images, and speech.

The published checkpoint has 8B parameters in BF16. Audio tasks require separate GLM-4-Voice tokenizer and decoder; image tasks require MagViT-v2. Omni-Diffusion is a reproducible research stack rather than a hosted API: the model card has no connected inference provider.

## Development line

- **2026-03-11 — Omni-Diffusion public project resources linked.** On 2026-03-11, a dated entry linked Omni-Diffusion's project website, source repository, and Hugging Face model page. Together, these resources establish a public reference point for the project's documentation, implementation, and model access. The dated links alone do not establish the release version, capabilities, or evaluation results.

## What changed

- 2026-03-11 — Code, project page, and open 8B BF16 checkpoint released for any-to-any text, image, and speech tasks.
- 2026-07-03 — arXiv v2 updated the ICML paper version and noted an optimized model checkpoint.

## How to use this

As of 2026-03-11, practitioners should evaluate Omni-Diffusion through its linked project site, source repository, and Hugging Face model page rather than relying on an unverified secondary description.

1. Clone the repository, initialize submodules, and install dependencies and the package inside the official Docker image.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
2. Download the main checkpoint into `../models/Omni-Diffusion`. For audio tasks, add the GLM-4-Voice tokenizer and decoder; for images, add MagViT-v2.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
3. Run `tools/inference.py` with paths to the main weights, image tokenizer, audio tokenizer, audio decoder, and output directory.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Best practices

- Use the official repository inference path for multimodal tasks: standard loading via Transformers does not replace the required image and audio tokenizers.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
- Pin and verify the model revision before enabling `trust_remote_code`: the model card requires custom architecture.
  — <https://huggingface.co/lijiang/Omni-Diffusion>
- Keep the main weights and the three helper artifacts in matching paths and environments so the complete text, image, and speech stack functions.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Superseded by this

- 2026-07-03 — arXiv v2 supersedes v1 from 2026-03-06 as the active paper version; v2 is marked as the ICML version with an optimized checkpoint.

## Still unknown

- Primary published requirements for VRAM, latency, and supported CUDA versions for inference remain unlisted.
- No official Chinese primary source or independent Chinese operating report is confirmed; Chinese search returned only secondary summaries.
- The lack of an inference provider on the Hugging Face model card confirms no listed hosted provider, but third-party standalone deployments remain possible.

## Sources

| source | title | read |
|---|---|---|
| https://omni-diffusion.github.io/ | Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion | 2026-09-05 |
| https://github.com/VITA-MLLM/Omni-Diffusion | VITA-MLLM/Omni-Diffusion repository | 2026-09-05 |
| https://huggingface.co/lijiang/Omni-Diffusion | lijiang/Omni-Diffusion model card | 2026-09-05 |
| https://arxiv.org/abs/2603.06577 | Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:omni-diffusion`, thread `omni-diffusion-development`, 1 dated events 2026-03-11 → 2026-03-11.
- **Practical note:** As of 2026-03-11, practitioners should evaluate Omni-Diffusion through its linked project site, source repository, and Hugging Face model page rather than relying on an unverified secondary description.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
