---
title: SeFi-Image
category: projects
date: 2026-06-26
tags: [project, sefi-image, sefi-image-development]
aliases: ["SeFi-Image"]
---

# SeFi-Image

**Development line:** `project:sefi-image` · thread `sefi-image-development`  
**Last event:** 2026-06-26 · 1 dated since 2026-06-26 · **Researched:** 2026-09-05 · confidence: high

## What it is

SeFi-Image separates semantic and texture latent streams so structure denoises ahead of detail. It offers 1B, 2B, and 5B Base models, a 5B RL model, and 1B/2B/5B Turbo models. Base and RL use 50 steps at guidance 4.0; Turbo defaults to four steps at guidance 1.0. Use it for controlled local research, not commercial deployment or hosted inference.

## Development line

- **2026-06-26 — SeFi-Image official project resources were linked.** On 2026-06-26, links appeared for the project website, source repository, and Hugging Face page. They give the starting resources, but no specific release, model, or technical milestone.

## What changed

2026-06-26 — arXiv v3 documented SeFi-Image as a public semantic-first-diffusion T2I family with 1B, 2B, and 5B scales and DMD2-distilled Turbo variants.

## How to use this

As of 2026-06-26, use the linked project website, GitHub repository, and Hugging Face page to evaluate or follow SeFi-Image.

1. Accept the checkpoint access conditions, then choose a checkpoint: Base for analysis or fine-tuning, RL for alignment-oriented generation, or Turbo for fast generation.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base>
2. Install the repository runtime in a Python 3.11 environment with a PyTorch build compatible with the local CUDA stack, then install Diffusers, Transformers, Accelerate, Safetensors, Hugging Face Hub, OmegaConf, and Pillow.
  — <https://github.com/jmliu206/SeFi-Image>
3. Run `inference.py` with a checkpoint ID, prompt, output directory, and seed; use a Base checkpoint such as `SeFi-Image/SeFi-Image-5B-Base` for the default 50-step path.
  — <https://github.com/jmliu206/SeFi-Image>
4. For low-latency generation, select a Turbo checkpoint and set four steps with guidance scale 1.0.
  — <https://github.com/jmliu206/SeFi-Image>
5. For a standard Diffusers workflow, load a `-diffusers` checkpoint with `SeFiPipeline` or `DiffusionPipeline` in BF16 on CUDA.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-turbo-diffusers>

## Best practices

- Keep Turbo at 4, 8, or 10 denoising steps and guidance scale 1.0; the project documents four steps as its default.
  — <https://github.com/jmliu206/SeFi-Image>
- Use Base checkpoints as the starting point for fine-tuning and analysis; reserve Turbo for fast generation and RL for stronger alignment-oriented output.
  — <https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base>
- Treat the released weights as CC BY-NC 4.0, gated, research-use material; apply human oversight, moderation, validation, and compliance checks before any broader use.
  — <https://github.com/jmliu206/SeFi-Image>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The sources do not provide a dated changelog describing the substantive differences between arXiv v3, v4, and v5.
- No first-party source provides a production-serving option; the Hugging Face Diffusers cards state that no Inference Provider deploys the models.

## Sources

| source | title | read |
|---|---|---|
| https://jmliu206.github.io/sefi-web/ | SeFi-Image | Semantic-First Diffusion | 2026-09-05 |
| https://github.com/jmliu206/SeFi-Image | GitHub - jmliu206/SeFi-Image | 2026-09-05 |
| https://huggingface.co/SeFi-Image | SeFi-Image organization on Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2606.22568 | SeFi-Image: A Text-to-Image Foundation Model with Semantic-First Diffusion | 2026-09-05 |
| https://huggingface.co/SeFi-Image/SeFi-Image-5B-Base | SeFi-Image/SeFi-Image-5B-Base | 2026-09-05 |
| https://huggingface.co/SeFi-Image/SeFi-Image-5B-turbo-diffusers | SeFi-Image/SeFi-Image-5B-turbo-diffusers | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sefi-image`, thread `sefi-image-development`, 1 dated events 2026-06-26 → 2026-06-26.
- **Practical note:** As of 2026-06-26, use the linked project website, GitHub repository, and Hugging Face page as the starting points to evaluate or follow SeFi-Image.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
