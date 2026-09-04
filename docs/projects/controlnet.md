---
title: ControlNet — ControlNet development
category: projects
tags: [controlnet, controlnet-development, controlnet_face_landmarks, controlnet_v1_1, open_source_release, project]
aliases: ["ControlNet"]
---

# ControlNet — ControlNet development

**Development line:** `project:controlnet` · thread `controlnet-development`  
**Events:** 3 dated, 2023-02-12 → 2023-04-13 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ControlNet is a spatial-conditioning adapter for image-generation practitioners who need a prompt to follow a reference image rather than only describe it. - Follows edge and line maps, depth, segmentation, poses, and sketches. - Adds the visual condition while preserving the frozen base model. Limit: checkpoints and preprocessors are specific to a control type and model family; current documentation covers Flux, Hunyuan-DiT, Stable Diffusion 3, and SDXL. Verdict: use it when geometry, composition, or pose must be constrained.

## Development line

- **2023-02-12 — ControlNet source and runnable entry points became publicly available.** On 2023-02-12, the linked GitHub repository, Hugging Face Space, and Colab notebook placed ControlNet source and runnable access points in public view. This is the earliest sealed event in this development line. The supplied links do not establish a specific release tag or feature set.
- **2023-03-20 — A ControlNet face-landmark model was introduced to the community.** On 2023-03-20, the linked community resource indicated a ControlNet model associated with facial-landmark guidance. This records a material specialization of the ControlNet ecosystem toward facial-structure conditioning. The sealed evidence does not establish its distribution, performance, or adoption.
- **2023-04-13 — ControlNet v1.1 entered a nightly development line.** On 2023-04-13, the linked GitHub resource indicated a ControlNet v1.1 nightly development line. This is a material versioned continuation of the project’s development. The sealed evidence does not establish a stable-release date or enumerate the changes.

## What changed

ControlNet grew from an SD 1.x research implementation into model-family-specific control workflows. 2023-02-12 - The original project documented transfer of ControlNet to community SD 1.x models. 2023-03-20 - A community Face-Landmark checkpoint showed an additional control type; the available evidence does not show a core architecture change. 2023-04-13 - ControlNet 1.1 retained the 1.0 architecture, introduced standardized names, and expanded the SD 1.5 catalog to 14 models: 11 production-ready and 3 experimental. 2023-05-31 - A1111-side 1.1.202 work added a cascaded high-resolution inpainting workflow, not a new ControlNet architecture. Found 2026-09-04 - Current guides document ControlNet workflows for Flux, Hunyuan-DiT, Stable Diffusion 3, and SDXL through ComfyUI nodes and Diffusers pipelines.

## How to use this

From 2023-02-12, practitioners could obtain ControlNet through the linked source and runnable entry points; from 2023-04-13, they should identify the v1.1 nightly line explicitly rather than treat all ControlNet resources as one static release.

1. Choose the structural constraint, then create or preprocess the matching reference image; different ControlNet types expect different reference images.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
2. In ComfyUI, place the selected checkpoint under `ComfyUI/models/controlnet`, load the base checkpoint and ControlNet, then upload the reference image.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
3. Apply the ControlNet to positive and negative conditioning, set strength and optional start/end percentages, then queue the generation.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
4. For code, load a control-specific model into the appropriate Diffusers pipeline, then pass both the prompt and `control_image`; tune `controlnet_conditioning_scale`.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
5. If working in AUTOMATIC1111, install or update the `sd-webui-controlnet` extension, add model files, refresh the model list, and select the control/preprocessor in the UI.
  — <https://github.com/Mikubill/sd-webui-controlnet>

## Best practices

- Choose the preprocessor and reference-map type together with the checkpoint; different ControlNet types require different reference images.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- Use a checkpoint and pipeline from the same documented model family instead of treating SD 1.5, SDXL, Flux, and other ControlNets as interchangeable.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Tune Control Strength or `controlnet_conditioning_scale` deliberately because it directly controls how much the reference constrains the result.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- For Multi-ControlNet, resize inputs to the expected size, mask conditions so they do not overlap, and tune each conditioning scale separately.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- In ComfyUI, use `Apply ControlNet`; `Apply ControlNet (Old)` is deprecated.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- For AUTOMATIC1111, use `sd-webui-controlnet`; do not install the `ControlNet-v1-1-nightly` research repository as an A1111 extension.
  — <https://github.com/lllyasviel/ControlNet-v1-1-nightly>

## Superseded by this

- 2023-04-13 - Installing `ControlNet-v1-1-nightly` in AUTOMATIC1111 is an incorrect legacy path; its own instructions direct A1111 users to `sd-webui-controlnet`.
- 2023-05-31 - Treating A1111 v1.1.202 as the current integration is obsolete; the extension documents later v1.1.454 work dated 2024-07-09.
- 2023-era - ComfyUI graphs using `Apply ControlNet (Old)` are deprecated; use `Apply ControlNet`.

## Still unknown

- The Face-Landmark item is supported only by a community post and a linked demo; its model card, license, checkpoint compatibility, and current availability were not verified.
- The dated events mix the ControlNet architecture, a community checkpoint, and an AUTOMATIC1111 extension. They describe one ecosystem, not one maintained distribution.
- The historical Hugging Face Space and Colab notebook could not be read in this environment, so their original instructions and current availability remain unverified.

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
- **Practical note:** From 2023-02-12, practitioners could obtain ControlNet through the linked source and runnable entry points; from 2023-04-13, they should identify the v1.1 nightly line explicitly rather than treat all ControlNet resources as one static release.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
