---
title: Flux2-Klein-9B-Consistency
category: projects
date: 2026-03-13
tags: [flux2-klein-9b-consistency, flux2-klein-9b-consistency-releases, lora_releases, project]
aliases: ["Flux2-Klein-9B-Consistency"]
---

# Flux2-Klein-9B-Consistency

**Development line:** `project:flux2-klein-9b-consistency` · thread `flux2-klein-9b-consistency-releases`  
**Last event:** 2026-03-13 · 1 dated since 2026-03-13 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Flux2-Klein-9B-Consistency is an image-to-image LoRA for base model black-forest-labs/FLUX.2-klein-9B.

- Source composition and detail preservation during semantic editing.
- Reduced color shift and oversaturation in V2.

The adapter is not an independent 9B model; base model license terms apply separately. Use V2 for controlled source image editing, not as a general generator.

## Development line

- **2026-03-13 — Flux2-Klein-9B-Consistency resource linked.** On 2026-03-13, the Flux2-Klein-9B-Consistency line linked to a Hugging Face resource under dx8152 and to a YouTube video. The links mark a public availability milestone without establishing model capabilities, version details, or intended workflow.

## What changed

- 2026-03-13 — Released the Consistency adapter for FLUX.2 Klein 9B; a third-party entry from 2026-03-06 specified the workflow graph and CFG=1.
- 2026-04-17 — Added Flux2-Klein-9B-consistency-V2.safetensors to fix color tint, excessive detail, and oversaturation in V1. The V2 file is 331 MB with SHA-256 61db2017ce420b97bd5ef11984e5a894c90003a6bbf0dc9473f8d7b9ebb3ff93.

## How to use this

Check the dx8152 Hugging Face repository and linked video from 2026-03-13 to evaluate fit before adoption.

1. Install current diffusers, transformers, and accelerate; load base black-forest-labs/FLUX.2-klein-9B in bfloat16 on CUDA.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
2. Load adapter weights via load_lora_weights("dx8152/Flux2-Klein-9B-Consistency") and pass the source image with edit instructions.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
3. For local ComfyUI, place the base 9B model, Qwen 3 8B text encoder, and flux2 VAE in their respective directories, then apply the LoRA in an image-edit workflow.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>

## Best practices

- Prefer V2 over V1: it addresses color shift, noisy detail, and oversaturation.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
- Start at strength 0.3–0.5 when combining with lighting LoRAs: this protects details but dampens the lighting shift.
  — <https://www.patreon.com/foxfuressence/posts/lighting-angle-162733880>
- Test against your base model version and workflow: user reports diverge, with poor results reported on FP8 and GGUF variants.
  — <https://www.reddit.com/r/comfyui/comments/1rv6juw/fixing_the_plastic_look_in_flux2_klein_9b_with/>

## Superseded by this

- 2026-04-17 — V1 is obsolete whenever neutral color, clean detail, and controlled saturation matter.

## Still unknown

- Primary logs do not confirm the exact upload date for V1; records from 2026-03-06 confirm the base model, purpose, and CFG=1 for the 2026-03-13 release.
- Video JXMbbbdfnSg was unreadable, leaving its contents unused as evidence.
- No independent reproducible benchmark confirms the claimed consistency gains; user reports diverge on quality and compatibility.
- The adapter repository lists Apache-2.0, whereas BFL documentation specifies the FLUX Non-Commercial License for 9B Base; verify base model weights before commercial use.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency | dx8152/Flux2-Klein-9B-Consistency | 2026-09-05 |
| https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency/commit/ab936d843fea26adb9fac23132d7fc834c529ed7 | Upload Flux2-Klein-9B-consistency-V2.safetensors | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1rm3g3j/dx8152_flux_2_klein_9b_consistency_lora/ | DX8152 Flux 2 Klein 9b consistency lora | 2026-09-05 |
| https://docs.comfy.org/tutorials/flux/flux-2-klein | ComfyUI Flux.2 Klein Guide | 2026-09-05 |
| https://www.patreon.com/foxfuressence/posts/lighting-angle-162733880 | Lighting Angle Change workflow! | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1rv6juw/fixing_the_plastic_look_in_flux2_klein_9b_with/ | Fixing the “Plastic” Look in Flux.2 Klein 9B with the Consistency LoRA | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_klein_training | FLUX.2 [klein] Training | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:flux2-klein-9b-consistency`, thread `flux2-klein-9b-consistency-releases`, 1 dated events 2026-03-13 → 2026-03-13.
- **Practical note:** As of 2026-03-13, practitioners should recognize Flux2-Klein-9B-Consistency as a publicly linked dx8152 resource and inspect its Hugging Face page and linked video before deciding whether it fits their workflow; its capabilities and compatibility remain unverified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
