---
title: "ComfyUI"
category: "projects"
date: 2026-10-17
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-development", "comfyui-drama3", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI

**Development line:** project:comfyui-drama3 · thread comfyui-development  
**Last event:** 2026-10-17 · 20 dated since 2023-11-24 · **Researched:** 2026-10-19 · confidence: high

## What it is

ComfyUI-Drama3 is a custom node extension for ComfyUI. It runs Fish Audio's Drama 3, a 35-billion parameter text-to-speech and voice cloning model, locally on consumer GPUs.

- Zero-shot voice cloning from clean speech audio.
- Multi-speaker dialogue with up to 16 distinct voices in a single script.
- Emotional performances directed by bracketed tags.
- Speech recognition through local companion aligner nodes.

Inactive MoE routing experts are offloaded to system RAM, and active experts stay cached on the GPU. It needs at least 8 GB of VRAM.

## Development line

- **2023-11-24 — Stable Video Diffusion workflows.** ComfyUI published first-party Stable Video Diffusion example workflows for image-to-video. They documented model placement and the controls for frame count, motion, frame rate and classifier-free guidance.
- **2024-06-12 — SD3 in core.** Commit 8c4a9be added SD3 support to the core engine. SD3 workflows could now be built natively.
- **2024-09-16 — SD3 and Flux inpainting ControlNet.** Commit f48e390 added support for AliMama ControlNet models for SD3 and Flux inpainting. This widened structurally conditioned inpainting for both model families.
- **2024-10-21 — V1 interface and Desktop beta.** ComfyUI introduced the V1 interface and opened closed-beta Desktop packaging. V1 added a bundled Manager, tabs, settings, model and workflow browsers, and model-download help. The original interface moved to a maintenance path.
- **2024-12-06 — Ultralytics package compromise.** Malicious Ultralytics 8.3.41 and 8.3.42 packages turned up through some custom-node dependency chains. ComfyUI documented its response and separated the compromised dependency from ComfyUI core. The Manager gained warnings and version pinning.
- **2025-07-28 — Day-zero Wan 2.2.** Native support arrived on day zero. It came with official mixture-of-experts text-to-video and image-to-video workflows and packaged model files.
- **2025-08-13 — Wan 2.2 Fun InP, Control and LightX2V.** The workflows enabled first-and-last-frame generation, structural controls, and faster four-step generation with LoRA acceleration.
- **2025-08-26 — Qwen-Image DiffSynth ControlNet.** Native support widened controllable image generation. Optional cache-based workflow acceleration was documented.
- **2025-08-27 — Hosted Gemini and local Qwen-Image control.** Two distinct paths were added. Google Gemini 2.5 Flash Image runs through credit-billed Partner Nodes. InstantX Qwen-Image Unified ControlNet workflows run locally, with canny, depth, pose and soft-edge controls.
- **2025-08-28 — Second Comfy Challenge.** The community showcase and workflow-learning program grew with the second Comfy Challenge. This was an ecosystem and education milestone, not a core runtime release.
- **2025-09-24 — Wan 2.2 Animate and Qwen image editing.** Native workflows for Wan 2.2 Animate and Qwen-Image-Edit-2509 were added. They cover performer-driven character animation and replacement, and multi-image editing.
- **2025-10-07 — ComfyUI 0.3.63: publishable subgraphs.** Subgraphs could be published as reusable blueprint nodes. Selection tooling for graph editing was redesigned.
- **2025-10-09 — Sora 2 Partner Nodes.** Sora 2 and Sora 2 Pro became available through paid Partner Nodes. They support text-to-video and image-to-video with sound.
- **2025-10-22 — ComfyUI 0.3.66: subgraph and template tooling.** Subgraphs got a parameter panel. Workflow-template discovery and filtering were redesigned.
- **2025-11-26 — Comfy Cloud infrastructure and allowances.** Comfy Cloud announced a move to RTX 6000 Pro infrastructure and support for personal LoRAs. It also described longer Pro runs and unified credits across Cloud GPU execution and Partner Nodes.
- **2025-12-30 — Repository moves to Comfy-Org.** The canonical GitHub repository began moving from comfyanonymous/ComfyUI to Comfy-Org/ComfyUI. GitHub redirects were kept, and users were advised to update their Git remotes.
- **2026-01-27 — Day-zero Z-Image.** ComfyUI added support for the non-distilled Z-Image model. It shipped with an official workflow and model-specific sampling guidance.
- **2026-02-05 — Open-model grant initiative.** Alongside the Anima launch, the ComfyUI ecosystem announced a grant initiative described as a $1 million program. It was presented as funding for open model development.
- **2026-03-26 — Stable Dynamic VRAM.** ComfyUI documented Dynamic VRAM as stable. It reduces memory pressure and out-of-memory failures on supported Nvidia systems. The guidance says to measure total workflow time, not isolated iteration speed.
- **2026-10-17 — ComfyUI-Drama3 nodes 3x+ faster.** A user report said the updated ComfyUI-Drama3 nodes run at least 3x faster and work with 8GB VRAM. The report links to the project's GitHub repository.
  - The update optimizes expert caching between host RAM and GPU for Fish Audio's 35B parameter Drama 3 MoE architecture. Generation is 3x to 4x faster, and 8 GB VRAM consumer GPUs still work. (2026-10-17) — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## What changed

The project began as an adaptation of the Drama 3 architecture and became an optimized ComfyUI custom node package. It keeps experts in RAM so the 35B mixture-of-experts model runs on consumer hardware. Later kernel optimizations and caching improvements cut inference latency by more than threefold on 8 GB systems.

## How to use this

1. Clone the repository into the ComfyUI `custom_nodes` directory.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
2. Put the Drama 3 model weights in `models/diffusion_models` and the codec weights in `models/vae`.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
3. Load the voice clone or text-to-speech example workflow. Attach reference audio for speaker cloning, add emotion tags and queue it.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Best practices

- On 8 GB cards, offload routed experts to system RAM and keep GPU VRAM for the active expert cache.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
- Use short, clean reference speech with no background noise, so the cloned voice stays faithful.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
- Add bracketed cues such as `[whispers]` or `[laughs]` to shape tone across multi-speaker dialogue scripts.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## What practitioners say

- Practitioners report a noticeable 3x to 4x speedup after the node update. That makes local 35B model inference practical on 8 GB cards. (2026-10-17)
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8dj76/comfyuidrama3_is_34x_faster_now/>

## Superseded by this

- Earlier node versions took much longer to run on 8 GB VRAM GPUs, because expert transfers from RAM to VRAM were not optimized.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Still unknown

- Commit dates before the 2026-10-17 optimization release were not independently dated in public search summaries.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/PedroMarinhoDev/ComfyUI-Drama3 | PedroMarinhoDev/ComfyUI-Drama3: ComfyUI custom nodes for Drama 3 | 2026-10-19 |
| https://www.reddit.com/r/StableDiffusion/comments/1x8dj76/comfyuidrama3_is_34x_faster_now/ | ComfyUI-Drama3 is 3-4x faster now : r/StableDiffusion | 2026-10-19 |

## Agent brief {#agent-brief}

- **Subject:** project:comfyui-drama3, thread comfyui-development, 20 dated events 2023-11-24 → 2026-10-17.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
