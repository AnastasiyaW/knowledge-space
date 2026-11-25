---
title: "ComfyUI"
category: "projects"
date: 2026-11-21
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-dettato", "comfyui-development", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI

**Development line:** project:comfyui-dettato · thread comfyui-development  
**Last event:** 2026-11-21 · 21 dated since 2023-11-24 · **Researched:** 2026-11-22 · confidence: medium

## What it is

ComfyUI-Dettato is an audio-to-MIDI custom node set for ComfyUI. It is for people who work with symbolic music rather than direct audio diffusion.

Abilities:

- Transcribes polyphonic audio recordings into multi-track MIDI.
- Extracts note events for melody, chords and percussion.
- Adapts symbolic structures for downstream generative pipelines, including YuE.

It needs local model weights, and a run is bounded by audio duration and VRAM. It bridges raw audio recordings and symbolic conditioning inside ComfyUI graphs.

## Development line

- **2023-11-24 — ComfyUI Publishes Stable Video Diffusion Workflows.** On 2023-11-24, ComfyUI published first-party Stable Video Diffusion example workflows for image-to-video generation. The examples showed where to place the model and how to set frame count, motion, frame rate and classifier-free guidance.
- **2024-06-12 — ComfyUI Core Adds SD3 Support.** On 2024-06-12, ComfyUI added SD3 support to its core engine in commit 8c4a9be. SD3 workflows now run on native engine support.
- **2024-09-16 — ComfyUI Adds SD3 and Flux Inpainting ControlNet Support.** On 2024-09-16, ComfyUI added support for AliMama ControlNet models for SD3 and Flux inpainting in commit f48e390. It extends structurally conditioned inpainting to both model families.
- **2024-10-21 — ComfyUI V1 Introduces a New Interface and Desktop Beta.** On 2024-10-21, ComfyUI introduced its V1 interface and opened closed-beta Desktop packaging. The release added a bundled Manager, tabs, settings, model and workflow browsers, and help with model downloads. The original interface moves to maintenance only.
- **2024-12-06 — ComfyUI Responds to the Ultralytics Package Compromise.** On 2024-12-06, ComfyUI documented its response to malicious Ultralytics 8.3.41 and 8.3.42 packages, which reached users through some custom-node dependency chains. The project separated the compromised dependency from ComfyUI core. It added Manager warnings and version pinning.
- **2025-07-28 — ComfyUI Adds Day-Zero Wan 2.2 Support.** On 2025-07-28, ComfyUI added native day-zero support for Wan 2.2. The release came with official mixture-of-experts text-to-video and image-to-video workflows and packaged model files.
- **2025-08-13 — ComfyUI Expands Wan 2.2 Fun InP and Control Workflows.** On 2025-08-13, ComfyUI added Wan 2.2 Fun InP, Control and LightX2V support. The workflows allow first-and-last-frame generation and structural controls. LoRA acceleration gives faster four-step generation.
- **2025-08-26 — ComfyUI Adds Native Qwen-Image DiffSynth ControlNet Support.** On 2025-08-26, ComfyUI added native Qwen-Image DiffSynth ControlNet support. It widens controllable image generation. The update also documents optional cache-based workflow acceleration.
- **2025-08-27 — ComfyUI Adds Hosted Gemini and Local Qwen-Image Control Paths.** On 2025-08-27, ComfyUI added two separate execution paths. One is Google Gemini 2.5 Flash Image through credit-billed Partner Nodes. The other is local InstantX Qwen-Image Unified ControlNet workflows, which support canny, depth, pose and soft-edge controls.
- **2025-08-28 — Second Comfy Challenge Expands the Community Workflow Program.** On 2025-08-28, ComfyUI expanded its community showcase and workflow-learning program through the second Comfy Challenge. This was an ecosystem and education milestone, not a core runtime release.
- **2025-09-24 — ComfyUI Adds Wan 2.2 Animate and Qwen Image Editing Workflows.** On 2025-09-24, ComfyUI added native workflows for Wan 2.2 Animate and Qwen-Image-Edit-2509. They cover performer-driven character animation and replacement, and multi-image editing.
- **2025-10-07 — ComfyUI 0.3.63 Makes Subgraphs Publishable.** On 2025-10-07, ComfyUI 0.3.63 made subgraphs publishable as reusable blueprint nodes. The release also redesigned the selection tools for graph editing.
- **2025-10-09 — ComfyUI Adds Sora 2 Partner Nodes.** On 2025-10-09, ComfyUI made Sora 2 and Sora 2 Pro available through paid Partner Nodes. They support text-to-video and image-to-video generation with sound.
- **2025-10-22 — ComfyUI 0.3.66 Improves Subgraph and Template Tooling.** On 2025-10-22, ComfyUI 0.3.66 added a parameter panel for subgraphs. The release also redesigned how workflow templates are found and filtered.
- **2025-11-26 — Comfy Cloud Expands Infrastructure and Feature Allowances.** On 2025-11-26, Comfy Cloud announced a move to RTX 6000 Pro infrastructure and support for personal LoRAs. It also described longer Pro runs and unified credits across Cloud GPU execution and Partner Nodes.
- **2025-12-30 — ComfyUI Begins Moving Its Canonical Repository to Comfy-Org.** On 2025-12-30, ComfyUI began moving its canonical GitHub repository from comfyanonymous/ComfyUI to Comfy-Org/ComfyUI. GitHub redirects stay in place. Users should update their Git remotes.
- **2026-01-27 — ComfyUI Adds Day-Zero Z-Image Support.** On 2026-01-27, ComfyUI added day-zero support for the non-distilled Z-Image model. The release includes an official workflow and sampling guidance for that model.
- **2026-02-05 — ComfyUI Ecosystem Announces an Open-Model Grant Initiative.** On 2026-02-05, the ComfyUI ecosystem announced an open-model grant initiative, described as a $1 million program, alongside the Anima launch. It was presented as funding for open model development.
- **2026-03-26 — ComfyUI Introduces Stable Dynamic VRAM Management.** On 2026-03-26, ComfyUI documented Dynamic VRAM as a stable mechanism that reduces memory pressure and out-of-memory failures on supported Nvidia systems. Its guidance says to measure total workflow time, not isolated iteration speed.
- **2026-11-21 — ComfyUI-Dettato adds adapter for yue2.** A ComfyUI-Dettato adapter for the yue2 model was announced, placed under audio-to-MIDI and music-to-MIDI tooling.
- **2026-11-21 — ComfyUI-Dettato adds adapter for YuE 2 audio-to-MIDI.** The announcement covers a Dettato adapter for the yue2 model inside the ComfyUI-Dettato project, tagged for audio-to-MIDI and music-to-MIDI workflows.
- **2026-11-21 — other reporting on this date.**
  - Describes feeding the Dettato audio-to-MIDI transcription weights into a node adapter that targets YuE 2 symbolic music representation pipelines. (2026-11-21) — <https://github.com/StanShumsky/ComfyUI-Dettato>
  - Describes a dedicated bridge that maps transcription output into multi-track conditioning for YuE 2 full-song generation workflows. (2026-11-21) — <https://github.com/StanShumsky/ComfyUI-Dettato>

## What changed

The integration started as basic audio-to-MIDI transcription nodes. It now has adapters that map transcribed note streams into the multi-track conditioning formats symbolic music generation frameworks need.

## How to use this

1. Clone the ComfyUI-Dettato repository into the ComfyUI custom\_nodes directory.
  — <https://github.com/StanShumsky/ComfyUI-Dettato>
2. Place the Dettato audio-to-MIDI model weights in the ComfyUI models directory.
  — <https://github.com/StanShumsky/ComfyUI-Dettato>
3. Add the Dettato audio transcription node to the workflow and connect an audio input node.
  — <https://github.com/StanShumsky/ComfyUI-Dettato>
4. Route the multi-track MIDI output into the downstream symbolic generation conditioning nodes.
  — <https://github.com/StanShumsky/ComfyUI-Dettato>

## Best practices

- Use isolated stems or clean recordings, so polyphonic pitch detection is more accurate before conditioning.
  — <https://github.com/StanShumsky/ComfyUI-Dettato>
- Check track assignments and note ranges before sending symbolic tokens to music generation models.
  — <https://github.com/StanShumsky/ComfyUI-Dettato>

## Superseded by this

- Manual external audio-to-MIDI transcription workflows, from before the direct ComfyUI node integration for YuE pipelines.
  — <https://github.com/StanShumsky/ComfyUI-Dettato>

## Still unknown

- Commit history and node parameter schemas were not inspected. Only search snippets of the repository were available.
- Community discussions on forums and chat channels could not be traced to direct URLs.
- How tightly the Dettato adapter depends on specific versions of YuE is not confirmed beyond the repository announcement.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/StanShumsky/ComfyUI-Dettato | StanShumsky/ComfyUI-Dettato: Audio-to-MIDI transcription custom nodes for ComfyUI | 2026-11-22 |

## Agent brief {#agent-brief}

- **Subject:** project:comfyui-dettato, thread comfyui-development, 21 dated events 2023-11-24 → 2026-11-21.
- **Practical note:** see the usage and best-practice sections above, with their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
