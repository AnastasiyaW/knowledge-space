---
title: ChronoEdit — ChronoEdit release and adapters
category: projects
tags: [chronoedit, chronoedit-release-and-adapters, project]
aliases: ["ChronoEdit"]
---

# ChronoEdit — ChronoEdit release and adapters

**Development line:** `project:chronoedit` · thread `chronoedit-release-and-adapters`  
**Events:** 3 dated, 2025-10-31 → 2025-11-18 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ChronoEdit — a Diffusers image editor for creators and developers who need an object edit to remain plausible within its scene. - Treats the source and edited image as endpoints of a short video, then uses temporal reasoning to guide the edit. - Supports prompt-based editing, an eight-step distillation LoRA, an upscaling LoRA, and a sketch-to-object Paint Brush LoRA. - The 14B base workflow needs about 34 GB of VRAM with model offload, or about 38 GB with temporal reasoning; the upscaler is tested to 2K. Verdict: use it for local CUDA image-editing workflows where object interaction matters; it is not a lightweight desktop editor.

## Development line

- **2025-10-31 — ChronoEdit project, code, demo, and 14B model resources were linked.** On 2025-10-31, the supplied links pointed to the ChronoEdit research page, GitHub repository, Hugging Face Space, and ChronoEdit-14B-Diffusers model. This is the earliest supplied ChronoEdit entry and establishes the project's code, demo, and model-resource presence in this record.
- **2025-11-11 — ChronoEdit 14B Diffusers Upscaler LoRA was added to the line.** On 2025-11-11, the supplied links pointed to a separate ChronoEdit-14B-Diffusers-Upscaler-Lora resource and back to the earlier The source item. Because this identifies a new companion artifact rather than only repeating the base-resource links, it is treated as a material development step.
- **2025-11-18 — ChronoEdit 14B Diffusers Paint Brush LoRA was added to the line.** On 2025-11-18, the supplied link pointed to a separately named ChronoEdit-14B-Diffusers-Paint-Brush-Lora resource. This adds another identified companion artifact after the base model and Upscaler LoRA in the supplied chronology.

## What changed

ChronoEdit — the line progressed from a 14B base editor to an upstream Diffusers pipeline with two task-specific LoRAs. - 2025-10-31 — the 14B Diffusers checkpoint, source code, and demo made the base workflow usable; NVIDIA’s repository dates the checkpoint release to 2025-10-29. - 2025-11-11 — the Upscaler LoRA added a dedicated content-preserving super-resolution workflow; NVIDIA dates its release to 2025-11-10. - 2025-11-18 — the Paint Brush LoRA added black-sketch-to-object editing; NVIDIA dates its release to 2025-11-16 and recommends pairing it with the eight-step distillation LoRA. - Found today, 2026-09-04 — the official Diffusers documentation lists the 14B base model and both LoRAs as the supported ChronoEdit assets.

## How to use this

As of 2025-11-18, practitioners should treat ChronoEdit as a base 14B Diffusers resource accompanied by separately named Upscaler and Paint Brush LoRA artifacts, and verify their compatibility and usage instructions in primary documentation before use.

1. Use the official local path: Linux with Python 3.10, install the repository environment, and download `nvidia/ChronoEdit-14B-Diffusers`.
  — <https://github.com/nv-tlabs/ChronoEdit>
2. Load the base checkpoint through `ChronoEditPipeline` in Diffusers, place it on CUDA, load the source image, and resize it to the pipeline’s supported latent grid.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
3. Run the image with a concrete edit instruction that states both the requested change and the content that must remain unchanged; take the final generated frame as the edited image.
  — <https://huggingface.co/docs/diffusers/api/pipelines/chronoedit>
4. For fast standard editing, load the supplied eight-step distillation LoRA and use `flow_shift=2.0`, guidance scale `1.0`, and eight inference steps.
  — <https://github.com/nv-tlabs/ChronoEdit>
5. For content-preserving enlargement, load the Upscaler LoRA with its prescribed super-resolution prompt; keep the job at or below the officially tested 2K limit.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
6. For a drawn-object edit, load Paint Brush together with the eight-step distillation LoRA, use a black pencil sketch, and describe the object the sketch should become.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Paint-Brush-Lora>

## Best practices

- Use the provided prompt enhancer and prompt guidance for base editing when memory permits; the repository calls this its best-results path.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Enable temporal reasoning only when scene consistency is worth the extra memory: the documented requirement rises from about 34 GB to 38 GB VRAM.
  — <https://github.com/nv-tlabs/ChronoEdit>
- Keep the distillation-LoRA settings at eight steps, guidance scale 1.0, and flow shift 2.0 rather than treating it as an arbitrary LoRA preset.
  — <https://github.com/nv-tlabs/ChronoEdit>
- For Upscaler LoRA, use its content-preserving trigger prompt and do not add the prompt enhancer; the official card says it is unnecessary.
  — <https://huggingface.co/nvidia/ChronoEdit-14B-Diffusers-Upscaler-Lora>
- For Paint Brush LoRA, prefer black sketches and combine it with the eight-step distillation LoRA; other sketch colours can work but are documented as worse.
  — <https://github.com/nv-tlabs/ChronoEdit>

## Superseded by this

- 2025-11-10 — treating the repository wrapper as the only official inference route is obsolete: ChronoEdit was merged into the Hugging Face Diffusers pipeline.
- 2025-11-10 — for dedicated content-preserving enlargement, base-only editing guidance is superseded by the Upscaler LoRA workflow, whose documented test limit is 2K.
- 2025-11-16 — for turning a black sketch into an in-scene object, text-only editing guidance is superseded by the Paint Brush LoRA plus eight-step distillation workflow.

## Still unknown

- No first-party Simplified Chinese usage guide was found; the operational guidance cited here is English.
- The official sources reviewed list the 14B base model and two LoRAs, but do not prove that no newer checkpoint exists elsewhere.
- The official hosted Space returned an internal error during this check, so its live-demo availability is unverified.

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
- **Practical note:** As of 2025-11-18, practitioners should treat ChronoEdit as a base 14B Diffusers resource accompanied by separately named Upscaler and Paint Brush LoRA artifacts, and verify their compatibility and usage instructions in primary documentation before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
