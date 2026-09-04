---
title: ControlNet
category: projects
date: 2023-04-13
tags: [controlnet, controlnet-development, controlnet_face_landmarks, controlnet_v1_1, open_source_release, project]
aliases: ["ControlNet"]
---

# ControlNet

**Development line:** `project:controlnet` · thread `controlnet-development`  
**Last event:** 2023-04-13 · 3 dated since 2023-02-12 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ControlNet is a spatial-conditioning adapter for diffusion models. We use it when a prompt must follow a reference image rather than only text.

- Edge and line maps, depth, segmentation, poses, and sketches steer generation.
- Frozen base model weights stay untouched while adapter branches add visual structure.

## Development line

- **2023-02-12 — ControlNet source and runnable entry points became publicly available.** On 2023-02-12, the linked GitHub repository, Hugging Face Space, and Colab notebook opened public access to code and runnable demos. The links give no specific release tag or feature set.
- **2023-03-20 — A ControlNet face-landmark model was introduced to the community.** On 2023-03-20, a community resource published a ControlNet model for facial landmarks. It added facial structure conditioning to the ecosystem. We have no numbers for its distribution, performance, or adoption.
- **2023-04-13 — ControlNet v1.1 entered a nightly development line.** On 2023-04-13, a GitHub repository marked the start of the v1.1 nightly line. It continued active project development. The repository listed no stable-release date and did not enumerate changes.

## What changed

ControlNet grew from an SD 1.x research implementation into model-specific control workflows. 2023-02-12 - The original project documented transfer of ControlNet to community SD 1.x models. 2023-03-20 - A community Face-Landmark checkpoint added a control type without altering the core architecture. 2023-04-13 - ControlNet 1.1 kept the 1.0 architecture, standardized names, and expanded the SD 1.5 catalog to 14 models: 11 production-ready and 3 experimental. 2023-05-31 - The A1111 extension added a cascaded high-resolution inpainting workflow in 1.1.202 without changing ControlNet itself. 2026-09-04 - Current guides document ControlNet workflows for Flux, Hunyuan-DiT, Stable Diffusion 3, and SDXL through ComfyUI nodes and Diffusers pipelines.

## How to use this

Work started on 2023-02-12 with source and runnable entry points. From 2023-04-13, identify the v1.1 nightly line directly instead of treating all resources as one release.

1. Pick a structural constraint and preprocess the matching reference image; different ControlNet types expect different reference images.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
2. In ComfyUI, put the checkpoint under `ComfyUI/models/controlnet`, load the base checkpoint and ControlNet, then upload the reference image.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
3. Connect ControlNet to positive and negative conditioning, set strength and optional start/end percentages, then queue generation.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
4. In code, load a control model into the Diffusers pipeline, pass the prompt and `control_image`, and tune `controlnet_conditioning_scale`.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
5. In AUTOMATIC1111, install or update `sd-webui-controlnet`, add model files, refresh the list, and select the preprocessor in the UI.
  — <https://github.com/Mikubill/sd-webui-controlnet>

## Best practices

- Match the preprocessor and reference map to the checkpoint; different ControlNet types require different reference images.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- Keep checkpoints and pipelines within one model family instead of treating SD 1.5, SDXL, Flux, and others as interchangeable.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Tune Control Strength or `controlnet_conditioning_scale` directly so the reference does not overpower or under-constrain output.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- For Multi-ControlNet, resize inputs to expected dimensions, mask conditions to avoid overlap, and tune each conditioning scale separately.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- In ComfyUI, use `Apply ControlNet`; `Apply ControlNet (Old)` is deprecated.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- For AUTOMATIC1111, use `sd-webui-controlnet`; do not install the `ControlNet-v1-1-nightly` research repository as an A1111 extension.
  — <https://github.com/lllyasviel/ControlNet-v1-1-nightly>

## Superseded by this

- 2023-04-13 - Installing `ControlNet-v1-1-nightly` in AUTOMATIC1111 is an incorrect legacy path; its own instructions direct A1111 users to `sd-webui-controlnet`.
- 2023-05-31 - Treating A1111 v1.1.202 as current integration is obsolete; the extension documents later v1.1.454 work dated 2024-07-09.
- 2023-era - ComfyUI graphs using `Apply ControlNet (Old)` are deprecated; use `Apply ControlNet`.

## Still unknown

- The Face-Landmark item rests on one community post and demo; we have not verified its model card, license, checkpoint compatibility, or current hosting.
- The dated events combine core architecture, a community checkpoint, and an AUTOMATIC1111 extension into an ecosystem rather than one maintained distribution.
- We cannot inspect the historical Hugging Face Space or Colab notebook, so original instructions and availability remain unconfirmed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/lllyasviel/ControlNet | GitHub - lllyasviel/ControlNet: Let us control diffusion models! | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/11v3dgj/new_controlnet_model_trained_on_face_landmarks/ | New ControlNet Model Trained on Face Landmarks | 2026-09-04 |
| https://github.com/lllyasviel/ControlNet-v1-1-nightly | GitHub - lllyasviel/ControlNet-v1-1-nightly: Nightly release of ControlNet 1.1 | 2026-09-04 |
| https://github.com/Mikubill/sd-webui-controlnet/discussions/1464 | [1.1.202 Inpaint] Improvement: Everything Related to Adobe Firefly Generative Fill | 2026-09-04 |
| https://huggingface.co/docs/diffusers/using-diffusers/controlnet | ControlNet - Hugging Face Diffusers | 2026-09-04 |
| https://docs.comfy.org/tutorials/controlnet/controlnet | ComfyUI ControlNet Usage Example | 2026-09-04 |
| https://github.com/Mikubill/sd-webui-controlnet | GitHub - Mikubill/sd-webui-controlnet: WebUI extension for ControlNet | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:controlnet`, thread `controlnet-development`, 3 dated events 2023-02-12 → 2023-04-13.
- **Practical note:** From 2023-02-12, practitioners could obtain ControlNet through linked source and runnable entry points; from 2023-04-13, they should identify the v1.1 nightly line explicitly rather than treat all ControlNet resources as one static release.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
