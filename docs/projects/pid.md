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

- Latent decoding: decodes latents into pixels with 4× upscaling, and 8× upscaling for Scale-RAE.
- Latent support: handles conventional VAE and semantic latents, including DINOv2 and SigLIP.
- Distilled sampling: runs distilled checkpoints in four steps.

NSCLv1 weights permit only non-commercial research or evaluation.
Choose PiD when you need controlled latent-to-2K/4K decoding on a supported backbone instead of a separate pixel upscaler after VAE.

## Development line

- **2026-05-25 — PiD research, code, and model resources were made publicly available.** On 2026-05-25, PiD published linked research, source code, and Hugging Face model resources. These links establish usable technical entry points, though the supplied evidence does not establish a precise version or capabilities.

## What changed

- **2026-05-25** — Published paper, source code, and PiD weights for FLUX, FLUX.2, Z-Image, Z-Image-Turbo, SD3, DINOv2, and SigLIP.
- **2026-05-27** — ComfyUI added PiD support.
- **2026-06-02** — Released SDXL, Qwen-Image, and Qwen-Image-2512 checkpoints; cleaned code and added `torch.compile` mode.
- **2026-07-09** — Released training code, distilled and undistilled PiD v1.5 2K→4K, and v1.5 for FLUX, Z-Image, Z-Image-Turbo, FLUX.2, and Qwen-Image.
- **2026-07-14** — Added optional Boogu-Image support for native generation and PiD decoding of its Flux-style VAE latents.

## How to use this

From 2026-05-25, treat PiD's research page, source repository, and Hugging Face model page as dated public technical entry points.

1. Clone the repository, create a Python 3.12/CUDA environment with `uv sync --frozen` or install the listed dependencies, then run `PYTHONPATH=. python verify_env.py`.
  — <https://github.com/nv-tlabs/PiD>
2. Download only the checkpoints tree: `hf download nvidia/PiD --local-dir . --include "checkpoints/*"`.
  — <https://github.com/nv-tlabs/PiD>
3. For prompt-to-image, use `from_ldm` with `--backbone`. For existing images, use `from_clean` to encode and then decode with PiD.
  — <https://github.com/nv-tlabs/PiD>
4. For 2K, choose `--pid_ckpt_type 2k`. For supported 4K, choose `2kto4k_v1pt5`; for SD3 and SDXL, choose `2kto4k`.
  — <https://github.com/nv-tlabs/PiD>

## Best practices

- Test the environment with `verify_env.py` before the first inference; run commands from the repository root with `PYTHONPATH=.`.
  — <https://github.com/nv-tlabs/PiD>
- Do not mistake VAE files for PiD models: `PiD_*` are distilled decoder checkpoints, while `ae.safetensors`, VAE/RAE, and similar files are dependency encoders and decoders.
  — <https://huggingface.co/nvidia/PiD>
- For FLUX, FLUX.2, and Qwen-Image, select v1.5 2K→4K: it fixes color and corner-grid artifacts, but the 2K variant stays sharper at exactly 2048 px.
  — <https://github.com/nv-tlabs/PiD>
- Check licenses before deployment: published weights are restricted to non-commercial research or evaluation.
  — <https://huggingface.co/nvidia/PiD>

## Superseded by this

- 2026-07-09 — Earlier FLUX, FLUX.2, and Qwen-Image `2kto4k` checkpoints are obsolete; use `2kto4k_v1pt5`. Old weights moved to `checkpoints_deprecated/`.
- 2026-07-09 — Guidance to use v1 `2kto4k` for new FLUX, FLUX.2, and Qwen-Image 4K decodes is obsolete; v1 `2kto4k` remains current for SD3 and SDXL.

## Still unknown

- The initial README records dates of subsequent releases, but GitHub publishes no separate versioned releases; exact commit SHAs and timestamps remain unverified.
- Speed and quality claims come from author measurements; independent reproducible evaluation on a specific workflow has not been tested here.

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
