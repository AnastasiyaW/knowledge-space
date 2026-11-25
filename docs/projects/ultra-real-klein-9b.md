---
title: Ultra Real - Klein 9b — Klein 9b
category: projects
date: 2026-03-23
tags: [klein-9b, project, ultra-real-klein-9b]
aliases: ["Ultra Real - Klein 9b"]
---

# Ultra Real - Klein 9b — Klein 9b

**Development line:** `project:ultra-real-klein-9b` · thread `klein-9b`  
**Last event:** 2026-03-23 · 1 dated since 2026-03-23 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Ultra Real - Klein 9b is a LoRA for FLUX.2 Klein 9B users in ComfyUI.

- Portrait generation: creates portraits.
- Image-edit: modifies existing images.
- Upscale: restores old images.

Versions run V1–V4: V3 produces a more delicate texture, while V4 handles detailing.
The LoRA is not a base model and requires a compatible Klein 9B workflow.
For natural skin, start with V3 and add V4 only for a detail pass.

## Development line

- **2026-03-23 — Ultra Real - Klein 9b linked to a Civitai model page and ComfyUI workflows.** V2 claims more natural skin texture with better preservation of tone and lighting.

## What changed

- 2026-03-23 — Ultra Real - Klein 9b was available as a V1/V2 LoRA line for FLUX.2 Klein 9B; V2 claimed more natural skin texture with better tone and lighting preservation.
- 2026-04-10 — The model entry was updated to show the V1–V4 line; V3 was described as a more delicate texture without extra freckles, and V4 as a separate detailing mode.
- 2026-04-13 — The current card lists FLUX.2 Klein 9B as the base model and V1–V4 as variants of one LoRA line.

## How to use this

From 2026-03-23, use the linked Civitai model page and ComfyUI workflows repository as dated reference points to evaluate Ultra Real - Klein 9b. The links alone do not verify a specific version, workflow compatibility, or performance claim.

1. Install compatible FLUX.2 Klein 9B components into the matching ComfyUI folders: the diffusion model, Qwen 3 8B text encoder, and flux2 VAE.
  — <https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx>
2. Load Ultra Real - Klein 9b into the LoRA slot of the Klein 9B workflow; for image editing with V3, start at weight 0.6, and for V4 at 0.55.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
3. For editing, use an instruction that preserves face, expression, build, pose, and composition; for V2 the published target weight is 0.5.
  — <https://tensor.art/models/981017447823890853>
4. For text-to-image, start at weight 0.7–0.8 and describe the shot as a photograph; the published V2 target weight is 0.7.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>

## Best practices

- Do not use V4 as a universal style LoRA: the description limits it to detailing; for standard generation, use a text prompt or another LoRA.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- Do not carry over V1 settings without testing: V1 can exaggerate pores and freckles or shift lighting and skin tone; V3 claims a more delicate result.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- For image-edit, explicitly instruct the model to keep features, expression, pose, and composition, so the LoRA does not change more than skin texture.
  — <https://tensor.art/models/981017447823890853>

## Superseded by this

- 2026-04-10 — V1 is no longer the preferred mode for natural skin: the current card describes V3 as a more delicate texture and V4 as a dedicated detail-pass.
- 2026-04-10 — The recommendation to use the same LoRA for both generation and detailing is obsolete: V4 is separately restricted to detailing.

## Still unknown

- The direct Civitai page and the workflow repository were unavailable for meaningful download during review; settings are confirmed by mirrors and publication pages rather than source workflow files.
- The current SeaArt card lists an announcement date of 2026-03-13, an update date of 2026-04-10, and a publication date of 2026-04-13, but gives no separate release dates for V3 and V4; we cannot date them more precisely.
- Civitai ID 2462105 appears later on some mirrors for UltraReal - Krea2, Klein9b as well; nothing proves this is a continuation of the same Klein 9B LoRA rather than card reuse.

## Sources

| source | title | read |
|---|---|---|
| https://civitai.com/models/2462105/ultra-real-klein-9b | Ultra Real - Klein 9b — Civitai model page | 2026-09-05 |
| https://github.com/vizsumit/comfyui-workflows | vizsumit/comfyui-workflows | 2026-09-05 |
| https://civarchive.com/seaart/models/0b4b3278ab4fd5b6471cd029ef88fc09/versions/4eaaed353d71f3ae09efa4411c954877 | Ultra Real - Klein 9b V2 — CivArchive | 2026-09-05 |
| https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09 | Ultra Real - Klein 9b — SeaArt model page | 2026-09-05 |
| https://tensor.art/models/981017447823890853 | Ultra Real - Klein 9b V1 — Tensor.Art | 2026-09-05 |
| https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx | FLUX.2 Klein ComfyUI tutorial | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ultra-real-klein-9b`, thread `klein-9b`, 1 dated events 2026-03-23 → 2026-03-23.
- **Practical note:** From 2026-03-23, practitioners should use the linked Civitai model page and ComfyUI workflows repository as the dated reference points for evaluating Ultra Real - Klein 9b; the links alone do not verify a specific version, workflow compatibility, or performance claim.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
