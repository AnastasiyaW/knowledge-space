---
title: "ComfyUI"
category: "projects"
date: 2026-11-08
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-development", "comfyui-tbg-revealayer", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI

**Development line:** project:comfyui-tbg-revealayer · thread comfyui-development  
**Last event:** 2026-11-08 · 22 dated since 2023-11-24 · **Researched:** 2026-11-25 · confidence: high

## What it is

ComfyUI TBG RevealLayer is a custom node for ComfyUI users who need foreground, reconstructed background, and selected-object RGBA layers from one image.

- Manual bounding boxes set pixel coordinates for target objects.
- Optional SAM3.1 text grounding detects object boxes from prompts.
- Layer outputs deliver foreground, background, object, mask, composite, and all-layer RGBA images.
- FLUX.1-dev handles layer inference.

Processes at a 1024-pixel long side and reserves two layers, leaving at most ten selected object boxes.

Use it for generative layer decomposition and compositing, not to recover pixels hidden in the source image.

## Development line

- **2023-11-24 — ComfyUI Publishes Stable Video Diffusion Workflows.** On 2023-11-24, ComfyUI published first-party Stable Video Diffusion example workflows for image-to-video generation. The examples documented model placement and controls for frame count, motion, frame rate, and classifier-free guidance.
- **2024-06-12 — ComfyUI Core Adds SD3 Support.** On 2024-06-12, ComfyUI added native SD3 support to its core engine in commit 8c4a9be to enable SD3 workflows.
- **2024-09-16 — ComfyUI Adds SD3 and Flux Inpainting ControlNet Support.** On 2024-09-16, ComfyUI added support for AliMama ControlNet models for SD3 and Flux inpainting in commit f48e390. This expanded structurally conditioned inpainting workflows for both model families.
- **2024-10-21 — ComfyUI V1 Introduces a New Interface and Desktop Beta.** On 2024-10-21, ComfyUI introduced its V1 interface and opened closed-beta Desktop packaging. The release added a bundled Manager, tabs, settings, model and workflow browsers, and model-download assistance while moving the original interface to maintenance.
- **2024-12-06 — ComfyUI Responds to the Ultralytics Package Compromise.** On 2024-12-06, ComfyUI responded to malicious Ultralytics 8.3.41 and 8.3.42 packages found in custom-node dependency chains. ComfyUI core was unaffected, and the project added Manager warnings and version pinning.
- **2025-07-28 — ComfyUI Adds Day-Zero Wan 2.2 Support.** On 2025-07-28, ComfyUI added native day-zero support for Wan 2.2. The release packaged model files and provided official mixture-of-experts text-to-video and image-to-video workflows.
- **2025-08-13 — ComfyUI Expands Wan 2.2 Fun InP and Control Workflows.** On 2025-08-13, ComfyUI added Wan 2.2 Fun InP, Control, and LightX2V support. The workflows enabled first-and-last-frame generation, structural controls, and faster four-step generation with LoRA acceleration.
- **2025-08-26 — ComfyUI Adds Native Qwen-Image DiffSynth ControlNet Support.** On 2025-08-26, ComfyUI added native Qwen-Image DiffSynth ControlNet support. The update expanded controllable image generation and documented optional cache-based workflow acceleration.
- **2025-08-27 — ComfyUI Adds Hosted Gemini and Local Qwen-Image Control Paths.** On 2025-08-27, ComfyUI added two distinct execution paths: Google Gemini 2.5 Flash Image through credit-billed Partner Nodes and local InstantX Qwen-Image Unified ControlNet workflows. The local workflows supported canny, depth, pose, and soft-edge controls.
- **2025-08-28 — Second Comfy Challenge Expands the Community Workflow Program.** On 2025-08-28, ComfyUI expanded its community showcase and workflow-learning program through the second Comfy Challenge. This was an ecosystem and education milestone rather than a core runtime release.
- **2025-09-24 — ComfyUI Adds Wan 2.2 Animate and Qwen Image Editing Workflows.** On 2025-09-24, ComfyUI added native workflows for Wan 2.2 Animate and Qwen-Image-Edit-2509. They supported performer-driven character animation and replacement alongside multi-image editing.
- **2025-10-07 — ComfyUI 0.3.63 Makes Subgraphs Publishable.** On 2025-10-07, ComfyUI 0.3.63 made subgraphs publishable as reusable blueprint nodes. The release also redesigned selection tooling for graph editing.
- **2025-10-09 — ComfyUI Adds Sora 2 Partner Nodes.** On 2025-10-09, ComfyUI made Sora 2 and Sora 2 Pro available through paid Partner Nodes. The integration supported text-to-video and image-to-video generation with sound.
- **2025-10-22 — ComfyUI 0.3.66 Improves Subgraph and Template Tooling.** On 2025-10-22, ComfyUI 0.3.66 added a parameter panel for subgraphs. The release also redesigned workflow-template discovery and filtering.
- **2025-11-26 — Comfy Cloud Expands Infrastructure and Feature Allowances.** On 2025-11-26, Comfy Cloud moved to RTX 6000 Pro infrastructure and added support for personal LoRAs. It also allowed longer Pro runs and unified credits across Cloud GPU execution and Partner Nodes.
- **2025-12-30 — ComfyUI Begins Moving Its Canonical Repository to Comfy-Org.** On 2025-12-30, ComfyUI began moving its canonical GitHub repository from comfyanonymous/ComfyUI to Comfy-Org/ComfyUI. GitHub redirects remain active, and users were advised to update their Git remotes.
- **2026-01-27 — ComfyUI Adds Day-Zero Z-Image Support.** On 2026-01-27, ComfyUI added day-zero support for the non-distilled Z-Image model. The release included an official workflow and model-specific sampling guidance.
- **2026-02-05 — ComfyUI Ecosystem Announces an Open-Model Grant Initiative.** On 2026-02-05, the ComfyUI ecosystem announced a $1 million grant initiative alongside the Anima launch to fund open model development.
- **2026-03-26 — ComfyUI Introduces Stable Dynamic VRAM Management.** On 2026-03-26, ComfyUI documented Dynamic VRAM as a stable feature to reduce memory pressure and out-of-memory failures on supported Nvidia systems. Guidance emphasized measuring total workflow time rather than isolated iteration speed.
- **2026-05-01 — ComfyUI update.** RevealLayer released its paper and inference code, followed by a Hugging Face checkpoint release during the same month.
- **2026-06-01 — ComfyUI update.** RevealLayer announced V2 and released RevealLayer-100K and RevealLayerBench on Hugging Face.
- **2026-11-08 — ComfyUI node for RevealLayer RGBA layer decomposition released.** A ComfyUI node called TBG RevealLayer was announced for splitting a single flat image into separate RGBA layers based on RevealLayer research from 360 AI Research and Wenzhou University. It is built on FLUX.1-dev, supports optional SAM3 selection, handles up to 12 layers per frame, and includes checksum-verified resumable weight downloads.
  - A dated hands-on test identifies the node revision as 949e2c4 and documents the practical workflow: draw object boxes with ComfyUI’s Create Bounding Boxes node, connect them to the node, and use FLUX.1-dev with CLIP-L, T5-XXL, and a FLUX VAE. The test found that a 3-box run took 75.8 seconds and peaked at about 28.4 GB GPU memory on an RTX 5090; these are one practitioner’s measurements, not a general hardware requirement. (2026-11-09) — <https://localai-kobo.com/comfyui-reveallayer-rgba-layers/>
  - The release repository specifies two bundled workflows: manual bounding boxes and optional text-grounded selection using an existing local SAM3.1 checkpoint. It also states that first execution fetches four RevealLayer checkpoint files, about 697 MB total, with pinned revisions, SHA-256 verification, atomic replacement, and resumable partial downloads. (undated) — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>

## What changed

RevealLayer’s upstream project released inference code and a checkpoint in May 2026, then added a V2 announcement and public dataset releases in June 2026. The reviewed release packages that upstream method as a ComfyUI custom node with native loaders, bounding-box workflows, optional SAM3.1 grounding, and managed RevealLayer checkpoint setup.

## How to use this

1. Place the repository in ComfyUI/custom_nodes, restart ComfyUI, and import either the manual or grounded bundled workflow.
  — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>
2. Load a standard FLUX.1-dev model with matching CLIP-L/T5XXL encoders and FLUX VAE, then connect the model, CLIP, VAE, and input image to TBG RevealLayer.
  — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>
3. For direct control, draw pixel-space object boxes and connect them; for semantic selection, use a locally installed SAM3.1 checkpoint to propose boxes, then review them in the editor.
  — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>
4. Set max_layers to at least the number of requested objects plus two, queue the workflow, and use the individual RGBA outputs in later compositing nodes.
  — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>

## Best practices

- Use bounding boxes for the objects that must become separate layers; without boxes, one documented test produced no decomposition.
  — <https://localai-kobo.com/comfyui-reveallayer-rgba-layers/>
- Leave two layer slots for foreground and background: max_layers of 12 accommodates up to ten selected objects, while later boxes are skipped when the limit is too low.
  — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>
- Do not apply the RevealLayer LoRA through a separate loader: the node applies it internally at strength 1.0.
  — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>
- Treat hidden-area completion as generated reconstruction and inspect every extracted layer before using it as production artwork.
  — <https://localai-kobo.com/comfyui-reveallayer-rgba-layers/>

## What practitioners say

- One hands-on tester found useful reconstructed background completion, but reported missing parts in an extracted subject, residual subject pixels in the background, and an empty object layer in the same test. (2026-11-09)
  — <https://localai-kobo.com/comfyui-reveallayer-rgba-layers/>
- The same tester found that changing the seed altered whether one object layer appeared, while a 20-step run looked close to the 30-step run and completed faster in that setup. (2026-11-14)
  — <https://localai-kobo.com/comfyui-reveallayer-rgba-layers/>

## Superseded by this

- The original upstream setup was a standalone inference project; this integration replaces that route for ComfyUI users with a native custom-node workflow, without replacing the upstream method itself.
  — <https://github.com/Ltamann/ComfyUI-TBG-RevealLayer>

## Still unknown

- The custom-node repository does not expose a stable page-level publication date in the reviewed page; its event-specific repository evidence is therefore marked undated.
- The upstream RevealLayer project and the ComfyUI integration are related but separately maintained; upstream V2 availability does not establish that this custom node implements V2.
- The Chinese official product page describes a hosted Reveal-Layer service with up to 20 selectable boxes, which is not the same limit as this ComfyUI node’s maximum of ten selected boxes.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Ltamann/ComfyUI-TBG-RevealLayer | Ltamann/ComfyUI-TBG-RevealLayer | 2026-11-25 |
| https://github.com/360CVGroup/RevealLayer | 360CVGroup/RevealLayer | 2026-11-25 |
| https://research.360.cn/products/Reveal-Layer | 高可控图层分解 — 360人工智能研究院 | 2026-11-25 |
| https://localai-kobo.com/comfyui-reveallayer-rgba-layers/ | ComfyUI-TBG-RevealLayerの使い方｜1枚の画像を透明レイヤーに分解、隠れた背景も描き足した（FLUX.1-dev） | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:comfyui-tbg-revealayer, thread comfyui-development, 22 dated events 2023-11-24 → 2026-11-08.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
