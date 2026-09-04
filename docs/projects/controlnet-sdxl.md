---
title: SDXL — SDXL development
category: projects
tags: [controlnet-sdxl, project, sdxl, sdxl-development]
aliases: ["SDXL", "SDXL 0.9", "SDXL 1.0"]
---

# SDXL — SDXL development

**Development line:** `project:controlnet-sdxl` · thread `sdxl-development`  
**Events:** 2 dated, 2023-05-24 → 2023-06-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

SDXL: a Stable Diffusion model for practitioners who need prompt-driven image generation. - Generates text-to-image, image-to-image, and inpainting outputs. - Runs the official 1.0 base checkpoint alone or with an optional refiner. - Default target: 1024×1024; default checkpoints are not recommended below 512 pixels. Verdict: use SDXL 1.0 for established SDXL workflows, with review for generated text, people, and factual-looking scenes.

## Development line

- **2023-05-24 — SDXL training-progress milestone was reported.** On 2023-05-24, a dated SDXL development link indicated that model training had reached a midway milestone and pointed readers to a community discussion channel. This is a material checkpoint because it records the project in an active pre-release training and feedback stage.
- **2023-06-22 — Stability AI published an SDXL 0.9 update.** On 2023-06-22, Stability AI published a dated official page identifying an SDXL 0.9 Stable Diffusion update. This is material because it marks a named version-level step after the preceding training-progress report. The supplied evidence does not establish release scope, availability, or technical specifications, so none are asserted here.

## What changed

2023-05-24 — SDXL was still about half trained; a Discord bot collected image-preference votes while testing parameters, so this was training feedback rather than a release. 2023-06-22 — SDXL 0.9 moved from beta toward a limited research release: it was available through Clipdrop, research weights were available, and 1.0 was planned for mid-July. 2023-06-25 — the linked official post cannot be retrieved today, so no additional technical change can be verified from it. 2023-07-26 (found 2026-09-04) — SDXL 1.0 was released as an open model, replacing the limited research-only 0.9 release with the base-plus-optional-refiner 1.0 line. 2026-09-04 (found today) — the maintained practical path is the official `stabilityai/stable-diffusion-xl-base-1.0` checkpoint through Diffusers; the base remains usable without the refiner.

## How to use this

From 2023-06-22, practitioners should track SDXL 0.9 separately in model and workflow notes: this line moves from a training-status update to a named SDXL 0.9 publication.

1. Install Diffusers, Transformers, Accelerate, and the optional invisible-watermark dependency from the current SDXL guide.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
2. Load `stabilityai/stable-diffusion-xl-base-1.0` with `StableDiffusionXLPipeline` or `AutoPipelineForText2Image`, preferably as fp16 safetensors on a supported accelerator.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
3. Start text-to-image work at 1024×1024; use 768×768 or 512×512 only when the workflow needs it, and avoid smaller dimensions with the default checkpoint.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
4. For an edit, reuse the loaded pipeline as image-to-image with an input image, or as inpainting with an input image and mask.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
5. Add `stabilityai/stable-diffusion-xl-refiner-1.0` only when a final denoising pass is worth the extra compute; the documented ensemble handoff is 80% base denoising and 20% refiner denoising.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
6. Before publishing or automating output, check the model card's license, intended-use boundary, and known failures for text, faces, composition, and factual depictions.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>

## Best practices

- Use the official 1.0 base checkpoint as the baseline and treat the refiner as optional; the base model is a supported standalone path.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>
- Keep default SDXL generation near its 1024×1024 native target; use size and crop conditioning for composition rather than expecting the default checkpoint to perform well below 512 pixels.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- For out-of-memory errors, use model CPU offload before sacrificing the documented resolution range; use `torch.compile` or xFormers only when the runtime supports them.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- Keep the invisible-watermark dependency when generated-image marking is required by the workflow; Diffusers enables it by default when installed.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- Do not use SDXL output as a factual representation of people or events, and retain human review for legible text, faces, and spatial relationships.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>

## Superseded by this

- 2023-05-24 — Discord voting and parameter experiments were a pre-release training-feedback process, not a deployment path; SDXL 1.0 open weights superseded that state on 2023-07-26.
- 2023-06-22 — SDXL 0.9 research-weight and Clipdrop-preview guidance is obsolete for a new deployment; use the named SDXL 1.0 base checkpoint instead.
- 2023-06-22 — The planned mid-July move to 1.0 is no longer future guidance; the open SDXL 1.0 release occurred on 2023-07-26.

## Still unknown

- The supplied 2023-06-25 Twitter URL returned no readable post data in the available reader; its exact claim and technical impact remain unverified.
- This does not assert current availability, pricing, or support status for the legacy Stability API engines named in 2023; the current evidence supports the checkpoint-and-Diffusers workflow only.

## Sources

| source | title | read |
|---|---|---|
| https://www.reddit.com/r/StableDiffusion/comments/13ppmtk/sdxl_is_now_50_trained_and_we_need_your_help/ | SDXL is now ~50% trained — and we need your help! | 2026-09-04 |
| https://stability.ai/blog/sdxl-09-stable-diffusion | Stability AI launches SDXL 0.9: A Leap Forward in AI Image Generation | 2026-09-04 |
| https://twitter.com/emostaque/status/1672700056154275841?s=21&t=RcamOh5xDIh5ilUsd6CSdA | Emad Mostaque post on SDXL (content unavailable to retrieve) | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-sdxl-1-announcement | Announcing SDXL 1.0 | 2026-09-04 |
| https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 | stabilityai/stable-diffusion-xl-base-1.0 — SD-XL 1.0-base Model Card | 2026-09-04 |
| https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl | Stable Diffusion XL — Diffusers documentation | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:controlnet-sdxl`, thread `sdxl-development`, 2 dated events 2023-05-24 → 2023-06-22.
- **Practical note:** From 2023-06-22, practitioners should track SDXL 0.9 separately in model and workflow notes: this line moves from a training-status update to a named SDXL 0.9 publication.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
