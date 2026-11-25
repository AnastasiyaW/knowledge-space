---
title: "Diffusers ControlNet SDXL: v0-35-1"
category: "projects"
date: 2026-07-03
tags: ["diffusers", "diffusers_controlnet", "project", "v0-35-1"]
aliases: ["Diffusers ControlNet SDXL", "Diffusers ControlNet SDXL: v0-35-1"]
---

# Diffusers ControlNet SDXL: v0-35-1

**Development line:** project:diffusers · thread v0-35-1  
**Last event:** 2026-07-03 · 1 dated since 2026-07-03 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Diffusers ControlNet SDXL is a Stable Diffusion XL pipeline for practitioners guiding generation with depth maps, edge maps, or poses.

- Model loading: loads an SDXL base model with one or more ControlNet checkpoints.
- Generation modes: supports text-to-image, image-to-image, and inpainting.
- Base checkpoint limit: dimensions below 512 pixels are not recommended for SDXL base checkpoints.
- Integration status: Diffusers maintains the integration, while several SDXL ControlNet checkpoints remain experimental.

## Development line

- **2026-07-03 — Diffusers 0.39.0: New image and video pipelines, core library improvements, and more.** Diffusers 0.39.0 added new image and video pipelines. Added pipelines include Cosmos 3, Ideogram 4, Krea 2, DreamLite, and PRX Pixel. Other new pipelines include Motif-Video, AnyFlow, JoyAI-Image-Edit, DiffusionGemma, Anima, and LTX-2.X IC LoRA and HDR Pipelines. It added modular pipeline support for SD3 and Anima. Core library improvements added AutoRound quantization, safetensors TorchAO support, and BitsAndBytes on MPS. It added AutoPipelineForText2Audio, AWS Neuron compatibility, and a safetensors bump to 0.8.0.
  - Release notes include a fix to ControlNet tests. They name no SDXL ControlNet checkpoint, API, pipeline behavior, or compatibility change. The supported scope is general ControlNet test maintenance within 0.39.0. (2026-07-03) — <https://github.com/huggingface/diffusers/releases/tag/v0.39.0>

## What changed

Diffusers 0.39.0 added image and video pipelines, core library updates, and a ControlNet test fix. Its release notes name no ControlNet SDXL pipeline or checkpoint change.

## How to use this

1. Load an SDXL-compatible ControlNet checkpoint, then construct StableDiffusionXLControlNetPipeline with the SDXL base model, ControlNet, and optional VAE.
  — <https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sdxl>
2. Prepare a control image matching the checkpoint signal, such as Canny edges or a depth map, and pass it with the prompt to the pipeline.
  — <https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sdxl>
3. To build a custom SDXL adapter, train with train\_controlnet\_sdxl.py against an SDXL base model, then load the saved ControlNet into the SDXL pipeline for inference.
  — <https://github.com/huggingface/diffusers/blob/main/docs/source/zh/training/controlnet.md>

## Best practices

- Tune controlnet\_conditioning\_scale first. Official SDXL examples use 0.5, while the API allows a separate scale for each ControlNet.
  — <https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sdxl>
- Use control\_guidance\_start and control\_guidance\_end when the control signal should guide only part of denoising.
  — <https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sdxl>
- Enable memory-efficient attention for local SDXL ControlNet runs only when its dependency is installed. Use CPU offload when memory is constrained.
  — <https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- “v0-35-1” matches no public Diffusers release or documented ControlNet SDXL component version. It appears to be a grouping label rather than a public version.
- The cited 0.39.0 release records a ControlNet test fix. It establishes no functional change specific to ControlNet SDXL.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/huggingface/diffusers/releases/tag/v0.39.0 | Diffusers 0.39.0: New image and video pipelines, core library improvements, and more | 2026-11-25 |
| https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sdxl | ControlNet with Stable Diffusion XL | 2026-11-25 |
| https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md | ControlNet training example for Stable Diffusion XL \(SDXL\) | 2026-11-25 |
| https://github.com/huggingface/diffusers/blob/main/docs/source/zh/training/controlnet.md | ControlNet 训练（中文） | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:diffusers, thread v0-35-1, 1 dated events 2026-07-03 → 2026-07-03.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium.
