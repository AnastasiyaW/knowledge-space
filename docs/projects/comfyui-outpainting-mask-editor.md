---
title: "ComfyUI"
category: "projects"
date: 2026-09-19
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-development", "comfyui-outpainting-mask-editor", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI

**Development line:** project:comfyui-outpainting-mask-editor · thread comfyui-development  
**Last event:** 2026-09-19 · 20 dated since 2023-11-24 · **Researched:** 2026-11-25 · confidence: medium

## What it is

ComfyUI-OutpaintMask is a custom ComfyUI node published on GitHub by zaum for creating outpaint masks interactively.

We open an editor from the node image preview to draw the outpaint frame on the image. The node outputs a render tile, masks, and the full canvas.

## Development line

- **2023-11-24 — ComfyUI Publishes Stable Video Diffusion Workflows.** On 2023-11-24, ComfyUI published first-party Stable Video Diffusion example workflows for image-to-video generation. The examples documented model placement and controls for frame count, motion, frame rate, and classifier-free guidance.
- **2024-06-12 — ComfyUI Core Adds SD3 Support.** On 2024-06-12, ComfyUI added SD3 support to its core engine in commit 8c4a9be. This gave the engine native support for SD3 workflows.
- **2024-09-16 — ComfyUI Adds SD3 and Flux Inpainting ControlNet Support.** On 2024-09-16, ComfyUI added support for AliMama ControlNet models for SD3 and Flux inpainting in commit f48e390. The change added structural inpainting workflows for both model families.
- **2024-10-21 — ComfyUI V1 Introduces a New Interface and Desktop Beta.** On 2024-10-21, ComfyUI introduced its V1 interface and opened closed-beta Desktop packaging. The release added a bundled Manager, tabs, settings, model and workflow browsers, and model-download assistance, and put the original interface on maintenance.
- **2024-12-06 — ComfyUI Responds to the Ultralytics Package Compromise.** On 2024-12-06, ComfyUI documented its response to malicious Ultralytics 8.3.41 and 8.3.42 packages in custom-node dependency chains. The project separated the compromised package from ComfyUI core, pinned versions, and added Manager warnings.
- **2025-07-28 — ComfyUI Adds Day-Zero Wan 2.2 Support.** On 2025-07-28, ComfyUI added native day-zero support for Wan 2.2. The release included official mixture-of-experts text-to-video and image-to-video workflows with packaged model files.
- **2025-08-13 — ComfyUI Expands Wan 2.2 Fun InP and Control Workflows.** On 2025-08-13, ComfyUI added Wan 2.2 Fun InP, Control, and LightX2V support. The workflows enabled first-and-last-frame generation, structural controls, and faster four-step generation with LoRA acceleration.
- **2025-08-26 — ComfyUI Adds Native Qwen-Image DiffSynth ControlNet Support.** On 2025-08-26, ComfyUI added native Qwen-Image DiffSynth ControlNet support. The update expanded controllable image generation and documented optional cache-based workflow acceleration.
- **2025-08-27 — ComfyUI Adds Hosted Gemini and Local Qwen-Image Control Paths.** On 2025-08-27, ComfyUI added two distinct execution paths: Google Gemini 2.5 Flash Image through credit-billed Partner Nodes and local InstantX Qwen-Image Unified ControlNet workflows. The local workflows supported canny, depth, pose, and soft-edge controls.
- **2025-08-28 — Second Comfy Challenge Expands the Community Workflow Program.** On 2025-08-28, ComfyUI expanded its community showcase and workflow-learning program through the second Comfy Challenge. This was an ecosystem and education milestone rather than a core runtime release.
- **2025-09-24 — ComfyUI Adds Wan 2.2 Animate and Qwen Image Editing Workflows.** On 2025-09-24, ComfyUI added native workflows for Wan 2.2 Animate and Qwen-Image-Edit-2509. They supported performer-driven character animation, replacement, and multi-image editing.
- **2025-10-07 — ComfyUI 0.3.63 Makes Subgraphs Publishable.** On 2025-10-07, ComfyUI 0.3.63 made subgraphs publishable as reusable blueprint nodes. The release also redesigned selection tooling for graph editing.
- **2025-10-09 — ComfyUI Adds Sora 2 Partner Nodes.** On 2025-10-09, ComfyUI made Sora 2 and Sora 2 Pro available through paid Partner Nodes. The integration supported text-to-video and image-to-video generation with sound.
- **2025-10-22 — ComfyUI 0.3.66 Improves Subgraph and Template Tooling.** On 2025-10-22, ComfyUI 0.3.66 added a parameter panel for subgraphs. The release also redesigned workflow-template discovery and filtering.
- **2025-11-26 — Comfy Cloud Expands Infrastructure and Feature Allowances.** On 2025-11-26, Comfy Cloud announced a move to RTX 6000 Pro infrastructure and support for personal LoRAs. It also added longer Pro runs and unified credits across Cloud GPU execution and Partner Nodes.
- **2025-12-30 — ComfyUI Begins Moving Its Canonical Repository to Comfy-Org.** On 2025-12-30, ComfyUI began moving its canonical GitHub repository from comfyanonymous/ComfyUI to Comfy-Org/ComfyUI. GitHub redirects were kept, and we should update Git remotes.
- **2026-01-27 — ComfyUI Adds Day-Zero Z-Image Support.** On 2026-01-27, ComfyUI added day-zero support for the non-distilled Z-Image model. The release included an official workflow and model-specific sampling guidance.
- **2026-02-05 — ComfyUI Ecosystem Announces an Open-Model Grant Initiative.** On 2026-02-05, the ComfyUI ecosystem announced an open-model grant initiative described as a $1 million program alongside the Anima launch. The initiative funds open model development.
- **2026-03-26 — ComfyUI Introduces Stable Dynamic VRAM Management.** On 2026-03-26, ComfyUI documented Dynamic VRAM as a stable mechanism for reducing memory pressure and out-of-memory failures on supported Nvidia systems. The guidance emphasized measuring total workflow time instead of isolated iteration speed.
- **2026-09-19 — ComfyUI-OutpaintMask custom package with interactive mask editor released.** A custom package for ComfyUI added an interactive mask editor for outpainting. We draw frames directly on images to preview what will render.
  - The repository describes the node as an interactive outpaint mask editor. Clicking the image or the Outpaint Editor button opens the editor, and the preview includes a clipboard-paste icon. It offers 8 draggable handles: corners resize proportionally, while Shift allows free resize. It snaps to original image edges and 16 px multiples. It includes aspect-ratio presets from 1:1 to 9:21, a px/mm readout with a DPI field, and an optional megapixel cap. Outputs are cropped_image (the render tile, with empty outpaint areas mid-gray 128), cropped_mask, original_image, original_mask, and crop_x/crop_y. These let the generated tile composite back into original_image, referenced in a Flux2 Klein sample workflow. (undated (page observed 2026; footer shows © 2026 GitHub)) — <https://github.com/zaum/ComfyUI-OutpaintMask>

## What changed

A custom node package added an interactive editor where we draw the outpaint frame directly on the image. It outputs a cropped render tile and mask, the full-canvas image and mask, and crop coordinates to composite the result back.

## How to use this

1. Install through the ComfyUI extension manager: open Manager → Custom Nodes Manager, search for ComfyUI-OutpaintMask (author: zaum), click Install, and restart ComfyUI. Alternatively, copy or symlink the folder into ComfyUI/custom_nodes/ComfyUI-OutpaintMask and restart. No extra Python dependencies are needed beyond ComfyUI core.
  — <https://github.com/zaum/ComfyUI-OutpaintMask>
2. Select or upload an image on the node, then click the image or the wide Outpaint Editor button to open the editor. Drag the 8 handles to draw the outpaint frame, optionally using aspect-ratio presets.
  — <https://github.com/zaum/ComfyUI-OutpaintMask>
3. Use cropped_image and cropped_mask as the render tile and its inpaint mask. To place the generated tile back into the full canvas, composite it onto original_image using crop_x and crop_y with the Composite node, as in the Flux2 Klein sample workflow.
  — <https://github.com/zaum/ComfyUI-OutpaintMask>

## Best practices

- Hold Shift only when wanting a free non-proportional resize; corner handles keep proportions by default. Rely on snapping to 16 px multiples and the megapixel-cap slider to keep the frame within sizes the model handles well, as its stops track native model sizes.
  — <https://github.com/zaum/ComfyUI-OutpaintMask>
- When working on a cropped section of a high-resolution image, keep the original_image and original_mask outputs and the crop_x/crop_y offsets so the generated tile composites back into the full canvas.
  — <https://github.com/zaum/ComfyUI-OutpaintMask>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact release date and any version number are not stated on the repository page.
- The page shows only 4 stars and no formal releases, so maturity and community reception are unknown.
- Which models beyond the referenced Flux2 Klein sample workflow have been tested is not stated.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/zaum/ComfyUI-OutpaintMask | GitHub - zaum/ComfyUI-OutpaintMask: ComfyUI node: interactive outpaint mask editor with render-tile and merge outputs | 2026-09-19 |

## Agent brief {#agent-brief}

- **Subject:** project:comfyui-outpainting-mask-editor, thread comfyui-development, 20 dated events 2023-11-24 → 2026-09-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
