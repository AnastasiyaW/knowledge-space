---
title: "ComfyUI"
category: "projects"
date: 2026-10-14
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-development", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "nvidia-rtx-vfx-nodes-comfyui", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI

**Development line:** project:nvidia-rtx-vfx-nodes-comfyui · thread comfyui-development  
**Last event:** 2026-10-14 · 20 dated since 2023-11-24 · **Researched:** 2026-11-28 · confidence: high

## What it is

NVIDIA RTX VFX Nodes for ComfyUI: a ComfyUI custom-node pack for VFX practitioners using an NVIDIA RTX GPU. It provides RTX Video Super Resolution, RTX Video Frame Generation, and RTX Video HDR; Super Resolution supports up to 4× scaling or target dimensions through 8192 px, while Frame Generation requires an RTX 40-series GPU or later. Verdict: it is a local finishing tool for RTX-based ComfyUI workflows, not a CPU or non-NVIDIA solution.

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
- **2026-10-14 — NVIDIA RTX VFX nodes for ComfyUI released.** NVIDIA VFX nodes for ComfyUI were announced with RTX Video super resolution up to 8192 px, frame generation, and HDR conversion, plus EXR support with extended color management. The post recommends chaining super resolution, frame generation, and HDR.
  - The accompanying first-party release material specifies 19 Super Resolution modes; 4× scaling or target dimensions up to 8192 px; Frame Generation from 2× to 16×; and HDR output as BT.2020 HLG or PQ with a 400–2000-nit target-luminance control. (2026-10-13) — <https://blog.comfy.org/p/nvidia-vfx-nodes-for-video-upscaling>

## What changed

The node pack introduced RTX Video Super Resolution, RTX Video Frame Generation, and RTX Video HDR as a single ComfyUI finishing workflow, alongside EXR and color-management improvements in ComfyUI.

## How to use this

1. Install the extension from ComfyUI Manager, then restart ComfyUI; alternatively clone it under \`ComfyUI/custom\_nodes\` and install \`requirements.txt\` with ComfyUI's own Python interpreter.
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes>
2. For upscaling, connect an IMAGE batch to RTX Video Super Resolution, choose the resize method and quality mode, then send \`upscaled\_images\` to a save or downstream node.
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes>
3. For frame interpolation, supply at least two ordered frames to RTX Video Frame Generation and encode multiplier-mode output at the source frame rate multiplied by the selected multiplier to preserve duration.
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes>
4. For SDR-to-HDR conversion, send decoded frames through RTX Video HDR and configure the downstream encoder or image tool to interpret the result as BT.2020/HLG or BT.2020/PQ rather than SDR.
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes>

## Best practices

- Use the documented finishing order—Super Resolution, then Frame Generation, then HDR—when all three effects are required.
  — <https://blog.comfy.org/p/nvidia-vfx-nodes-for-video-upscaling>
- For long HDR jobs, process frames in chunks and join the results to limit memory use.
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes>
- Do not treat HDR node output as ordinary SDR/sRGB data: preserve the selected HDR transfer function in the downstream encoder.
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes>
- For multi-GPU work involving different NvVFX effect types, one practitioner recommends phased processing—finish one effect type, close it, then run the next—because GPU selection is reported as SDK-global.
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes/issues/28>

## What practitioners say

- One practitioner reports that using different NvVFX effect types concurrently across multiple GPUs fails because the SDK's GPU selection is global; they recommend processing effect types in separate phases. (2026-04-01)
  — <https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes/issues/28>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No accessible Simplified-Chinese source supplied verifiable details beyond the English primary material.
- The public sources reviewed do not establish a dated supersession point for the older project name, so no name-change date is asserted.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes | ComfyUI Nvidia VFX Nodes | 2026-11-28 |
| https://blog.comfy.org/p/nvidia-vfx-nodes-for-video-upscaling | Releasing Nvidia VFX Nodes for Video Upscaling, Frame Generation and SDR-to-HDR, for VFX Professionals | 2026-11-28 |
| https://github.com/Comfy-Org/ComfyUI_Nvidia_VFX_Nodes/issues/28 | NvVFX SDK does not support multiple effect types across GPUs simultaneously | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:nvidia-rtx-vfx-nodes-comfyui, thread comfyui-development, 20 dated events 2023-11-24 → 2026-10-14.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
