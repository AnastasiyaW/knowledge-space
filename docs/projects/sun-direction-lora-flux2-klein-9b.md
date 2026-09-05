---
title: Sun Direction LoRA Flux 2 Klein 9B — Flux 2 Klein LoRAs
category: projects
date: 2026-07-03
tags: [flux2-klein-loras, project, sun-direction-lora-flux2-klein-9b]
aliases: ["Sun Direction LoRA Flux 2 Klein 9B"]
---

# Sun Direction LoRA Flux 2 Klein 9B — Flux 2 Klein LoRAs

**Development line:** `project:sun-direction-lora-flux2-klein-9b` · thread `flux2-klein-loras`  
**Last event:** 2026-07-03 · 1 dated since 2026-07-03 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Sun Direction LoRA Flux 2 Klein 9B is a 331 MB image-to-image LoRA for FLUX.2 [klein] 9B users. It shifts the apparent sun position in exterior photographs.

- Sun elevation and rotation: sets the angle relative to the camera.
- Lit-sphere reference: conditions the edit on a rendered sphere.
- Preparatory overcast pass: strips existing shadows before relighting.

## Development line

- **2026-07-03 — Sun Direction LoRA Flux 2 Klein 9B resource reference recorded.** On 2026-07-03, the Flux 2 Klein LoRAs thread linked to its Hugging Face repository. We have no post body or model card yet, so we make no claims about release version, training setup, license, or performance.

## What changed

2026-07-03 — a runnable FLUX.2 [klein] 9B demo documented the two-pass relighting workflow using sphere conditioning for the v1 adapter.

## How to use this

Inspect the Hugging Face repository from 2026-07-03 before use. We have no confirmed compatibility, triggers, license, or quality claims.

1. Update ComfyUI, then install the required FLUX.2 [klein] 9B diffusion model, 9B text encoder, and FLUX.2 VAE for an image-edit workflow.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>
2. Download the v1 LoRA and use the supplied workflow; use the Sphere Light Render node or the included Blender scene to make the lit-sphere reference.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
3. If the input already has strong directional light, first create an overcast, shadow-reduced version; use that image and the sphere image as latent references for the relight pass.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
4. Include `match the sun direction from the reference` in the prompt, then add scene instructions such as sky conditions after it.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>

## Best practices

- Use exterior photos and treat indoor output as unsupported rather than a broken setup.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Skip overcast preparation only when the input already lacks clear shadow direction.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Keep the seed fixed when rendering a relighting timelapse to reduce flicker.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Update ComfyUI if the supplied workflow has missing core nodes.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No public v2 weights, release notes, benchmarks, or training datasets were published. The v1 card only states that v2 is in progress.
- The author does not publish a validated LoRA-strength range or hardware requirements for this adapter.
- The 2026-07-03 development entry is a same-day runnable demo; repository v1 weights and workflows were committed on 2026-06-29.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B | Sun Direction LoRA Flux 2 Klein 9B v1 | 2026-09-05 |
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B/tree/main | Sun-Direction-Lora-Flux2Klein9B repository files | 2026-09-05 |
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B/commits/main | Sun-Direction-Lora-Flux2Klein9B commit history | 2026-09-05 |
| https://huggingface.co/spaces/linoyts/sun-direction-flux2-klein/commit/36259bd5c170a583fac16461a64b6ebc05f2ab84 | Sun Direction LoRA demo (FLUX.2 klein 9B) | 2026-09-05 |
| https://docs.comfy.org/tutorials/flux/flux-2-klein | ComfyUI Flux.2 Klein Guide | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:sun-direction-lora-flux2-klein-9b`, thread `flux2-klein-loras`, 1 dated events 2026-07-03 → 2026-07-03.
- **Practical note:** From 2026-07-03, inspect the linked Hugging Face resource before attempting use; we establish no compatibility, triggers, licensing, or quality claims.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.