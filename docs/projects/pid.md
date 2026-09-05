---
title: PiD — Research release
category: projects
date: 2026-05-25
tags: [pid, project, research-release]
aliases: ["PiD"]
---

# PiD — Research release

**Development line:** `project:pid` · thread `research-release`  
**Last event:** 2026-05-25 · 1 dated since 2026-05-25 · **Researched:** 2026-09-05 · confidence: high

## What it is

PiD is a pixel diffusion decoder for generative image pipelines that replaces standard VAE and RAE decoders.

- Latent decoding: decodes latents to pixels with simultaneous 4× upscale, or 8× upscale for Scale-RAE.
- Latent support: works with conventional VAE latents and semantic latents, including DINOv2 and SigLIP.
- Fast inference: distilled checkpoints decode in four steps.

NSCLv1 weights are restricted to non-commercial research or evaluation.
Use PiD when you need controlled latent-to-2K/4K decoding on a supported backbone instead of a separate pixel upscaler after the VAE.

## Development line

- **2026-05-25 — PiD research, code, and model resources were made publicly available.** On 2026-05-25, PiD was released with linked research, source code, and Hugging Face model resources. These links establish public technical entry points for the project, though the release evidence does not establish a precise version or full capabilities.

## What changed

- 2026-05-25 — Published paper, source code, and PiD weights for FLUX, FLUX.2, Z-Image, Z-Image-Turbo, SD3, DINOv2, and SigLIP.
- 2026-05-27 — Added PiD support to ComfyUI.
- 2026-06-02 — Released checkpoints for SDXL, Qwen-Image, and Qwen-Image-2512; cleaned the codebase and enabled torch.compile support.
- 2026-07-09 — Released training code, distilled and undistilled PiD v1.5 2K→4K, and v1.5 checkpoints for FLUX, Z-Image, Z-Image-Turbo, FLUX.2, and Qwen-Image.
- 2026-07-14 — Added optional support for Boogu-Image native generation and PiD decoding of its Flux-style VAE latents.

## How to use this

From 2026-05-25, practitioners should treat PiD's research page, source repository, and Hugging Face model page as its dated public technical entry points.

1. Clone the repository, create a Python 3.12/CUDA environment with `uv sync --frozen` or install the dependencies, then run `PYTHONPATH=. python verify_env.py`.
  — <https://github.com/nv-tlabs/PiD>
2. Download only the checkpoints tree: `hf download nvidia/PiD --local-dir . --include "checkpoints/*"`.
  — <https://github.com/nv-tlabs/PiD>
3. Use `from_ldm` with `--backbone` for prompt-to-image generation; use `from_clean` to encode an existing image and decode it with PiD.
  — <https://github.com/nv-tlabs/PiD>
4. Select `--pid_ckpt_type 2k` for 2K output; choose `2kto4k_v1pt5` for supported 4K models, or `2kto4k` for SD3 and SDXL.
  — <https://github.com/nv-tlabs/PiD>

## Best practices

- Verify the environment with `verify_env.py` before running inference, and run commands from the repository root with `PYTHONPATH=.`.
  — <https://github.com/nv-tlabs/PiD>
- Do not confuse VAE files with PiD models: `PiD_*` files are distilled decoder checkpoints, while `ae.safetensors`, VAE/RAE, and similar files are dependent encoders and decoders.
  — <https://huggingface.co/nvidia/PiD>
- Choose v1.5 2K→4K for FLUX, FLUX.2, and Qwen-Image to resolve color and corner-grid artifacts; the 2K checkpoint remains sharper at exactly 2048 px.
  — <https://github.com/nv-tlabs/PiD>
- Verify the license before deployment: published weights are restricted to non-commercial research or evaluation.
  — <https://huggingface.co/nvidia/PiD>

## Superseded by this

- 2026-07-09 — Earlier FLUX, FLUX.2, and Qwen-Image `2kto4k` checkpoints are deprecated in favor of `2kto4k_v1pt5`; older weights moved to `checkpoints_deprecated/`.
- 2026-07-09 — Advice to use v1 `2kto4k` for new FLUX, FLUX.2, and Qwen-Image 4K decodes is obsolete; v1 `2kto4k` remains current for SD3 and SDXL.

## Still unknown

- The initial README lists dates for subsequent updates, but GitHub does not publish separate versioned releases; exact commit SHAs and timestamps are not established.
- Speed and quality claims come from the authors' own benchmarks; independent reproducible evaluation on a specific workflow was not tested here.

## Sources

| source | title | read |
|---|---|---|
| https://research.nvidia.com/labs/sil/projects/pid/ | PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion | 2026-09-05 |
| https://github.com/nv-tlabs/PiD | nv-tlabs/PiD — PiD: Pixel Diffusion Decoder | 2026-09-05 |
| https://huggingface.co/nvidia/PiD | nvidia/PiD model repository | 2026-09-05 |
| https://arxiv.org/abs/2605.23902 | PiD: Fast and High-Resolution Latent Decoding with Pixel Diffusion | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:pid`, thread `research-release`, 1 dated events 2026-05-25 → 2026-05-25.
- **Practical note:** From 2026-05-25, practitioners should treat PiD's research page, source repository, and Hugging Face model page as its dated public technical entry points.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
