---
title: ChronoEdit
category: projects
date: 2025-11-18
tags: [chronoedit, chronoedit-release-and-adapters, project]
aliases: ["ChronoEdit"]
---

# ChronoEdit

**Development line:** `project:chronoedit` · thread `chronoedit-release-and-adapters`  
**Last event:** 2025-11-18 · 3 dated since 2025-10-31 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ChronoEdit — a Diffusers image editor for creators and developers who need an object edit to remain plausible within its scene.

- Treats the source and edited image as endpoints of a short video, then uses temporal reasoning to guide the edit.
- Supports prompt-based editing, an eight-step distillation LoRA, an upscaling LoRA, and a sketch-to-object Paint Brush LoRA.
- The 14B base workflow needs about 34 GB of VRAM with model offload, or about 38 GB with temporal reasoning; the upscaler is tested to 2K.

Use it for local CUDA image-editing workflows where object interaction matters. It is not a lightweight desktop editor.

## Development line

- **2025-10-31 — ChronoEdit project, code, demo, and 14B model resources were linked.** On 2025-10-31, links published the ChronoEdit research page, GitHub repository, Hugging Face Space, and ChronoEdit-14B-Diffusers model.
- **2025-11-11 — ChronoEdit 14B Diffusers Upscaler LoRA was added to the line.** On 2025-11-11, links published the separate ChronoEdit-14B-Diffusers-Upscaler-Lora companion artifact.
- **2025-11-18 — ChronoEdit 14B Diffusers Paint Brush LoRA was added to the line.** On 2025-11-18, links published the separate ChronoEdit-14B-Diffusers-Paint-Brush-Lora companion artifact after the base model and Upscaler LoRA.

## What changed

ChronoEdit moved from a 14B base editor to an upstream Diffusers pipeline with two task-specific LoRAs.

- 2025-10-31 — the 14B Diffusers checkpoint, source code, and demo made the base workflow usable; NVIDIA’s repository dates the checkpoint release to 2025-10-29.
- 2025-11-11 — the Upscaler LoRA added a dedicated content-preserving super-resolution workflow; NVIDIA dates its release to 2025-11-10.
- 2025-11-18 — the Paint Brush LoRA added black-sketch-to-object editing; NVIDIA dates its release to 2025-11-16 and recommends pairing it with the eight-step distillation LoRA.
- 2026-09-04 — the official Diffusers documentation lists the 14B base model and two LoRAs as the supported ChronoEdit assets.

## How to use this

We treat ChronoEdit as a base 14B Diffusers model with separate Upscaler and Paint Brush LoRA adapters as of 2025-11-18. Check primary documentation to verify compatibility and usage before running.

1. Set up Linux with Python 3.10, install the repository environment, and download `nvidia/ChronoEdit-14B-Diffusers`.
  — <https://github.com/nv-tlabs/ChronoEdit>
2. Load the base checkpoint through `ChronoEditPipeline` in Diffusers on CUDA, load the source image, and resize it to the supported latent grid.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
3. Run the image with a prompt stating the change and what stays unchanged; take the final generated frame as the edited image.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
4. For fast standard editing, load the supplied eight-step distillation LoRA with `flow_shift=2.0`, guidance scale `1.0`, and eight inference steps.
  — <https://github.com/nv-tlabs/ChronoEdit>
5. For content-preserving enlargement, load the Upscaler LoRA with its super-resolution prompt; stay at or below the tested 2K limit.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
6. For a drawn-object edit, load Paint Brush with the eight-step distillation LoRA, provide a black pencil sketch, and describe the target object.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora>

## Best practices

- Use the provided prompt enhancer and prompt guidance for base editing when memory permits; the repository calls this its best-results path.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Enable temporal reasoning only when scene consistency is worth the extra memory: the documented requirement rises from about 34 GB to 38 GB VRAM.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Keep distillation-LoRA settings at eight steps, guidance scale 1.0, and flow shift 2.0 rather than treating it as an arbitrary LoRA preset.
  — <https://github.com/nv-tlabs/ChronoEdit>
- For Upscaler LoRA, use its content-preserving trigger prompt and skip the prompt enhancer; the official card says it is unnecessary.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
- For Paint Brush LoRA, use black sketches and combine it with the eight-step distillation LoRA; other sketch colours work worse.
  — <https://github.com/nv-tlabs/ChronoEdit>

## Superseded by this

- 2025-11-10 — the repository wrapper as the sole inference route is obsolete: ChronoEdit was merged into Hugging Face Diffusers.
- 2025-11-10 — base-only enlargement is superseded by the Upscaler LoRA workflow, tested up to 2K.
- 2025-11-16 — text-only editing for sketches is superseded by Paint Brush LoRA with the eight-step distillation workflow.

## Still unknown

- No first-party Simplified Chinese guide was found; the operational guidance cited here is English.
- Official sources list the 14B base model and two LoRAs, but do not confirm whether newer checkpoints exist elsewhere.
- The official hosted Space returned an internal error during this check; live-demo availability remains unverified.

## Sources

| source | title | read |
|---|---|---|
| https://research.nvidia.com/labs/toronto-ai/chronoedit/ | ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation | 2026-09-04 |
| https://github.com/nv-tlabs/ChronoEdit | nv-tlabs/ChronoEdit — ChronoEdit: Towards Temporal Reasoning for Image Editing and World Simulation | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/chronoedit | ChronoEdit — Hugging Face Diffusers documentation | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers | nvidia/ChronoEdit-14B-Diffusers | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora | nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora | 2026-09-04 |
| https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora | nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:chronoedit`, thread `chronoedit-release-and-adapters`, 3 dated events 2025-10-31 → 2025-11-18.
- **Practical note:** We treat ChronoEdit as a base 14B Diffusers model with separate Upscaler and Paint Brush LoRA adapters as of 2025-11-18. Check primary documentation to verify compatibility and usage instructions before use.
- **Confidence:** medium. Dated supersedes above determine what is obsolete.
