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

Flux2-Klein-9B-Consistency is an image-to-image LoRA adapter for black-forest-labs/FLUX.2-klein-9B.

- Source composition and detail preservation during semantic edits.
- Reduced color shift and oversaturation in V2.

It is an adapter rather than a standalone 9B model, so the base model license applies separately. Use V2 for controlled source image edits instead of general generation.

## Development line

- **2026-03-13 — Flux2-Klein-9B-Consistency resource linked.** On 2026-03-13, the Flux2-Klein-9B-Consistency development line was linked to a Hugging Face resource under dx8152 and to a YouTube video. The dated links mark a public release milestone, but leave model capabilities, version details, and intended workflow unverified.

## What changed

- 2026-03-13: dx8152 published the Consistency adapter for FLUX.2 Klein 9B. A 2026-03-06 third-party post clarifies the workflow graph and sets CFG=1.
- 2026-04-17: dx8152 added Flux2-Klein-9B-consistency-V2.safetensors to fix color tint, excessive detail, and V1 oversaturation. The V2 file is 331 MB with SHA-256 61db2017ce420b97bd5ef11984e5a894c90003a6bbf0dc9473f8d7b9ebb3ff93.

## How to use this

As of 2026-03-13, check the dx8152 Hugging Face repository and linked video before deciding on adoption; capabilities and compatibility remain unverified.

1. Install current diffusers, transformers, and accelerate, then load black-forest-labs/FLUX.2-klein-9B in bfloat16 on CUDA.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
2. Load adapter weights with load_lora_weights("dx8152/Flux2-Klein-9B-Consistency") and pass the source image with the edit prompt.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
3. In local ComfyUI, place the base 9B model, Qwen 3 8B text encoder, and flux2 VAE into their directories, then apply the LoRA in an image-edit workflow.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>

## Best practices

- Prefer V2 over V1 to eliminate color shift, dirty detail, and excessive saturation.
  — <https://huggingface.co/dx8152/Flux2-Klein-9B-Consistency>
- Set strength to 0.3–0.5 when pairing with lighting LoRAs to preserve details without losing the lighting effect.
  — <https://www.patreon.com/foxfuressence/posts/lighting-angle-162733880>
- Test outputs against your base model setup; user reports diverge, with poor results on FP8 and GGUF variants.
  — <https://www.reddit.com/r/comfyui/comments/1rv6juw/fixing_the_plastic_look_in_flux2_klein_9b_with/>

## Superseded by this

- 2026-04-17 — V1 is obsolete for tasks that require neutral color, clean detail, and controlled saturation.

## Still unknown

- The exact first commit or upload date for V1 is unconfirmed in primary logs; only the purpose, base model, and CFG=1 from the 2026-03-06 post are verified for the 2026-03-13 event.
- Video JXMbbbdfnSg was unreadable, so we cannot verify its content.
- No independent benchmark confirms the claimed consistency gains, and user reports on quality and compatibility diverge.
- The adapter repository lists Apache-2.0, while BFL documentation specifies the FLUX Non-Commercial License for 9B Base; check the base weights license before commercial use.

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
- **Practical note:** As of 2026-03-13, check the dx8152 Hugging Face repository and linked video before adopting Flux2-Klein-9B-Consistency; capabilities and compatibility remain unverified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
