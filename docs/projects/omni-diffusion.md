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

Omni-Diffusion is an any-to-any multimodal model using masked discrete diffusion. It gives researchers and engineers one open stack instead of separate autoregressive models.

- Text-to-image, speech-to-image, VQA, spoken VQA, ASR, and TTS tasks.
- Joint generation and understanding across text, images, and speech.

The published checkpoint has 8B parameters in BF16. Audio tasks require separate GLM-4-Voice tokenizer and decoder; images require MagViT-v2. This is a reproducible research stack rather than a hosted API, because the model card has no connected inference provider.

## Development line

- **2026-03-11 — Omni-Diffusion public project resources linked.** On 2026-03-11, a dated entry linked Omni-Diffusion's project website, source repository, and Hugging Face model page. Together, these resources establish a public reference point for the project's documentation, implementation, and model access. The dated links alone do not establish the release version, capabilities, or evaluation results.

## What changed

- 2026-03-11 — Code, project page, and the open 8B BF16 Omni-Diffusion checkpoint published for any-to-any text/image/speech tasks.
- 2026-07-03 — arXiv v2 updated the ICML version of the paper and specified an optimized model checkpoint.

## How to use this

As of 2026-03-11, evaluate Omni-Diffusion through its linked project site, source repository, and Hugging Face model page rather than relying on an unverified secondary description.

1. Clone the repository, initialize submodules, and install dependencies and the package in an environment from the official Docker image.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
2. Download the main checkpoint into ../models/Omni-Diffusion; for audio tasks add the GLM-4-Voice tokenizer and decoder, and for images add MagViT-v2.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
3. Run tools/inference.py with paths to the main weight, image tokenizer, audio tokenizer, audio decoder, and output directory.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Best practices

- Use the official repository inference path for multimodal tasks: loading through Transformers does not replace the required image and audio tokenizers.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>
- Pin and verify the model revision before enabling trust_remote_code, because the card explicitly requires custom architecture.
  — <https://huggingface.co/lijiang/Omni-Diffusion>
- Keep the main weight and the three helper artifacts in matching paths and environment, or the claimed full text/image/speech stack will not build.
  — <https://github.com/VITA-MLLM/Omni-Diffusion>

## Superseded by this

- 2026-07-03 — arXiv v2 replaces v1 from 2026-03-06 as the current paper version; v2 is marked as the ICML version with an optimized checkpoint.

## Still unknown

- Primary published requirements for VRAM, latency, or supported CUDA version for inference are not found.
- No official Chinese source or independent Chinese operating report is confirmed; Chinese search yielded only secondary summaries.
- The lack of an inference provider on the Hugging Face card confirms the absence of a listed hosted provider, but does not rule out self-hosted third-party deployments.

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
