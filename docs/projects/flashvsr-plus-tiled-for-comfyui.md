---
title: "ComfyUI"
category: "projects"
date: 2026-10-31
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-development", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "flashvsr-plus-tiled-for-comfyui", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI

**Development line:** project:flashvsr-plus-tiled-for-comfyui · thread comfyui-development  
**Last event:** 2026-10-31 · 20 dated since 2023-11-24 · **Researched:** 2026-11-28 · confidence: medium

## What it is

FlashVSR\+ is an efficient one-step diffusion framework for video super-resolution. Its official repository describes Hybrid Attention and Reward-Yield Distribution Matching Distillation \(RY-DMD\), and says it enables spatially untiled 4K inference on a single 24GB RTX 4090. The tiled fork is a community ComfyUI node that splits each frame into overlapping tiles and processes them separately, so the model can run on GPUs with less memory.

## Development line

- **2023-11-24 — ComfyUI Publishes Stable Video Diffusion Workflows.** On 2023-11-24, ComfyUI published first-party Stable Video Diffusion example workflows for image-to-video generation. The examples documented model placement and controls for frame count, motion, frame rate, and classifier-free guidance.
- **2024-06-12 — ComfyUI Core Adds SD3 Support.** On 2024-06-12, ComfyUI added SD3 support to its core engine in commit 8c4a9be. The change established native engine support for building SD3 workflows.
- **2024-09-16 — ComfyUI Adds SD3 and Flux Inpainting ControlNet Support.** On 2024-09-16, ComfyUI added support for AliMama ControlNet models for SD3 and Flux inpainting in commit f48e390. The change expanded structurally conditioned inpainting workflows for those model families.
- **2024-10-21 — ComfyUI V1 Introduces a New Interface and Desktop Beta.** On 2024-10-21, ComfyUI introduced its V1 interface and opened closed-beta Desktop packaging. The release added a bundled Manager, tabs, settings, model and workflow browsers, and model-download assistance while placing the original interface on a maintenance path.
- **2024-12-06 — ComfyUI Responds to the Ultralytics Package Compromise.** On 2024-12-06, ComfyUI documented its response to malicious Ultralytics 8.3.41 and 8.3.42 packages encountered through some custom-node dependency chains. The project distinguished the compromised dependency from ComfyUI core and added Manager warnings and version pinning.
- **2025-07-28 — ComfyUI Adds Day-Zero Wan 2.2 Support.** On 2025-07-28, ComfyUI added native day-zero support for Wan 2.2. The release provided official mixture-of-experts text-to-video and image-to-video workflows and packaged model files.
- **2025-08-13 — ComfyUI Expands Wan 2.2 Fun InP and Control Workflows.** On 2025-08-13, ComfyUI added Wan 2.2 Fun InP, Control, and LightX2V support. The workflows enabled first-and-last-frame generation, structural controls, and faster four-step generation with LoRA acceleration.
- **2025-08-26 — ComfyUI Adds Native Qwen-Image DiffSynth ControlNet Support.** On 2025-08-26, ComfyUI added native Qwen-Image DiffSynth ControlNet support. The update expanded controllable image generation and documented optional cache-based workflow acceleration.
- **2025-08-27 — ComfyUI Adds Hosted Gemini and Local Qwen-Image Control Paths.** On 2025-08-27, ComfyUI added two distinct execution paths: Google Gemini 2.5 Flash Image through credit-billed Partner Nodes and local InstantX Qwen-Image Unified ControlNet workflows. The local workflows supported canny, depth, pose, and soft-edge controls.
- **2025-08-28 — Second Comfy Challenge Expands the Community Workflow Program.** On 2025-08-28, ComfyUI expanded its community showcase and workflow-learning program through the second Comfy Challenge. This was an ecosystem and education milestone rather than a core runtime release.
- **2025-09-24 — ComfyUI Adds Wan 2.2 Animate and Qwen Image Editing Workflows.** On 2025-09-24, ComfyUI added native workflows for Wan 2.2 Animate and Qwen-Image-Edit-2509. They supported performer-driven character animation and replacement as well as multi-image editing.
- **2025-10-07 — ComfyUI 0.3.63 Makes Subgraphs Publishable.** On 2025-10-07, ComfyUI 0.3.63 made subgraphs publishable as reusable blueprint nodes. The release also redesigned selection tooling for graph editing.
- **2025-10-09 — ComfyUI Adds Sora 2 Partner Nodes.** On 2025-10-09, ComfyUI made Sora 2 and Sora 2 Pro available through paid Partner Nodes. The integration supported text-to-video and image-to-video generation with sound.
- **2025-10-22 — ComfyUI 0.3.66 Improves Subgraph and Template Tooling.** On 2025-10-22, ComfyUI 0.3.66 added a parameter panel for subgraphs. The release also redesigned workflow-template discovery and filtering.
- **2025-11-26 — Comfy Cloud Expands Infrastructure and Feature Allowances.** On 2025-11-26, Comfy Cloud announced a move to RTX 6000 Pro infrastructure and support for using personal LoRAs. It also described longer Pro runs and unified credits across Cloud GPU execution and Partner Nodes.
- **2025-12-30 — ComfyUI Begins Moving Its Canonical Repository to Comfy-Org.** On 2025-12-30, ComfyUI began moving its canonical GitHub repository from comfyanonymous/ComfyUI to Comfy-Org/ComfyUI. GitHub redirects were retained, and users were advised to update their Git remotes.
- **2026-01-27 — ComfyUI Adds Day-Zero Z-Image Support.** On 2026-01-27, ComfyUI added day-zero support for the non-distilled Z-Image model. The release included an official workflow and model-specific sampling guidance.
- **2026-02-05 — ComfyUI Ecosystem Announces an Open-Model Grant Initiative.** On 2026-02-05, the ComfyUI ecosystem announced an open-model grant initiative described as a $1 million program alongside the Anima launch. The initiative was presented as funding for open model development.
- **2026-03-26 — ComfyUI Introduces Stable Dynamic VRAM Management.** On 2026-03-26, ComfyUI documented Dynamic VRAM as a stable mechanism for reducing memory pressure and out-of-memory failures on supported Nvidia systems. Its guidance emphasized measuring total workflow time instead of isolated iteration speed.
- **2026-10-31 — FlashVSR\+ Tiled fork for ComfyUI released.** A fork of FlashVSR\+ for ComfyUI was announced on 2026-10-31. It upscales video by splitting frames into overlapping tiles processed separately, to suit low-memory GPUs. It offers configurable tile size and overlap, three edge-blending modes \(cosine, linear, Gaussian\), streamed float16 tile output with audio preservation, per-tile progress display, separate VAE tile settings, and outputs for frames, audio, and frame rate. It requires NVIDIA CUDA, and the spatial-tiling branch is installed by cloning into custom\_nodes.
  - The official FlashVSR\+ repository lists a ComfyUI video upscaling node named FlashVSRPlusTiledUpscaleVideo under third-party integrations, next to a separate community FlashVSR\+ ComfyUI integration. It carries a disclaimer that these community contributions have not been officially tested or verified by the FlashVSR\+ team. The repository itself is Apache-2.0 licensed. Its released inference pipeline is CUDA-only with no CPU inference, which matches the fork's NVIDIA-only requirement. The upstream project's selling point is untiled 4K inference on one 24GB RTX 4090, which is the memory ceiling the tiled fork is meant to get below. (undated page; observed 2026-10-31) — <https://github.com/OpenImagingLab/FlashVSR_Plus>

## What changed

On 2026-10-31 a fork of FlashVSR\+ for ComfyUI, with spatial tiling, was announced. It adds configurable tile size and overlap, three edge-blending modes \(cosine, linear, Gaussian\), streamed float16 tile output with audio preserved, per-tile progress display, separate VAE tile settings, and outputs for frames, audio and frame rate. It needs NVIDIA CUDA and is installed from the spatial-tiling branch by cloning into custom\_nodes. The announcement warns that connecting the frames output unnecessarily is costly: 192 frames at 4K take about 17.8 GB of RAM.

## How to use this

1. Use an NVIDIA GPU with CUDA. The upstream FlashVSR\+ requirements list Linux, Python 3.10 and Conda or a venv, and say the pipeline does not support CPU inference.
  — <https://github.com/OpenImagingLab/FlashVSR_Plus>
2. For the upstream project, create a Python 3.10 environment, run pip install -r requirements.txt, then pip install -e . --no-deps. The --no-deps flag is intentional: it stops the install from changing an existing PyTorch/CUDA environment.
  — <https://github.com/OpenImagingLab/FlashVSR_Plus>
3. For the tiled ComfyUI node, clone the spatial-tiling branch of the fork into ComfyUI's custom\_nodes folder. Then set tile width, tile height and overlap, and pick a blending mode \(cosine, linear or Gaussian\).
  — <https://github.com/OpenImagingLab/FlashVSR_Plus>

## Best practices

- Upstream FlashVSR\+ requires input height and width to both be divisible by 128. Check this when choosing input sizes, and check whether the tiled node has the same limit.
  — <https://github.com/OpenImagingLab/FlashVSR_Plus>
- For videos with large motion, upstream suggests lowering --temporal-compression from the default 4 to 2 or 1 to better preserve motion detail. For long videos, a numeric --decode-every reads and writes video in segments instead of loading the whole input.
  — <https://github.com/OpenImagingLab/FlashVSR_Plus>
- Treat third-party nodes as unverified: the upstream authors state that community integrations are not officially tested.
  — <https://github.com/OpenImagingLab/FlashVSR_Plus>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The URL of the tiled fork's own repository is not given, so its code and license were not checked.
- Whether the fork keeps the upstream requirement that input height and width be divisible by 128 is unknown.
- Whether the fork works on Linux only, like upstream, or on other operating systems is unknown.
- No benchmark figures for speed or memory with tiling were provided, apart from the stated 17.8 GB of RAM for 192 frames at 4K when the frames output is connected.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/OpenImagingLab/FlashVSR_Plus | GitHub - OpenImagingLab/FlashVSR\_Plus: official repo of FlashVSR\+ \(Efficient Video Super-Resolution via Hybrid Attention and Reward-Yield Distribution Matching\) | 2026-10-31 |

## Agent brief {#agent-brief}

- **Subject:** project:flashvsr-plus-tiled-for-comfyui, thread comfyui-development, 20 dated events 2023-11-24 → 2026-10-31.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
