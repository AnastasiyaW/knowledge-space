---
title: FireRed Image Edit — ComfyUI Resources
category: projects
date: 2026-03-17
tags: [comfyui-resources, firered, firered-image-edit, project]
aliases: ["FireRed Image Edit"]
---

# FireRed Image Edit — ComfyUI Resources

**Development line:** `project:firered-image-edit` · thread `comfyui-resources`  
**Last event:** 2026-03-17 · 1 dated since 2026-03-17 · **Researched:** 2026-09-06 · confidence: medium

## What it is

FireRed Image Edit is a local instruction-driven image editor for ComfyUI and Diffusers.

- Source image edits from text.
- Reference fusion with 1 to 3 images for portraits, text style, makeup, restoration and virtual try-on.

The BF16 transformer alone needs 40.9 GB. The separate optimized path claims 30 GB and approximately 4.5-second runtime.

## Development line

- **2026-03-17 — A ComfyUI resource for FireRed Image Edit 1.1 was linked.** A message in the FireRed thread linked a Hugging Face repository for FireRed Image Edit 1.1 for ComfyUI on 2026-03-17. The same message included 3 RunningHub URLs. We have no evidence on the linked content, a release, capability changes or workflow details. We record only the dated publication of these resource links.

## What changed

- 2026-02-12 — The v1 technical report established the instruction-editing model.
- 2026-02-14 — FireRed-Image-Edit-1.0 weights became available.
- 2026-02-27 — The team added an Agent path and a 1.0 ComfyUI workflow.
- 2026-03-01 — An optimized local inference path was documented.
- 2026-03-03 — FireRed-Image-Edit-1.1 released as the 1.0 successor for portrait consistency, multi-element fusion, styled text and makeup.
- 2026-03-04 — The official 1.1 ComfyUI package appeared.
- 2026-03-08 — 3 independent single-, double- and multi-image comparison graphs appeared without changing the official package.
- 2026-03-09 — REDEdit-Bench was released.
- 2026-03-13 — An 8-step 1.0-Lightning v1.1 accelerator was added to the 1.1 ComfyUI package.
- 2026-03-17 — The official JSON switched its optional accelerator from 1.0-Lightning 8steps v1.0 to v1.1; this was not the base 1.1 release.
- 2026-03-24 — LoRA training code landed.
- 2026-03-25 — ModelScope LoRA-training support was announced.
- 2026-03-26 — The official collection marked LoRA Zoo updated.
- 2026-04-03 — Multi-provider recaption support merged to the canonical code.
- 2026-04-10 — A 1.1-Lightning 8-step v1.1 file was added.
- 2026-04-14 — A 1.1-Lightning 8-step v1.2 file was added.

## How to use this

1. Choose a supported route: load FireRedTeam/FireRed-Image-Edit-1.1 with Diffusers, or start from the official 1.1 ComfyUI package.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1>
2. For the stock ComfyUI graph, place the 1.1 transformer in models/diffusion_models, qwen2.5vl-7b-bf16 in models/text_encoders, qwen_image_vae in models/vae, then import the official JSON.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
3. Put the source image in the primary loader, add up to 2 optional references, and identify the intended change and image numbers in the prompt.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
4. Run an unmodified stock profile first: 40 steps and CFG 4 without the acceleration LoRA, or 8 steps and CFG 1 with the bundled Lightning path.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
5. For more than 3 inputs, use the separate Agent preprocessor and review its Gemini ROI-processing dependency before sending images.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>

## Best practices

- Pin the workflow JSON, transformer and Lightning LoRA together: the March 17 graph intentionally used a 1.1 transformer with the 1.0-Lightning v1.1 adapter.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/179def9bfaad5170a00b7760d7d1526ca53de019>
- Do not treat the later 1.1-Lightning v1.2 file as a documented drop-in replacement for the March 17 graph; test it as a separate versioned run.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/tree/main>
- Begin with the supplied sampler and settings rather than rewiring the graph; the saved profiles are 40 steps/CFG 4 or 8 steps/CFG 1.
  — <https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true>
- Do not translate the project’s 30 GB and approximately 4.5-second optimized-script claim into a ComfyUI capacity or speed guarantee.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>
- For jobs above 3 images, treat Agent preprocessing as an external-service boundary: ROI detection still uses Gemini even when recaption uses another provider.
  — <https://github.com/FireRedTeam/FireRed-Image-Edit>
- Treat independently assembled comparison graphs as custom workflows until their checkpoint, settings and node provenance are inspected.
  — <https://www.runninghub.ai/post/2030612111793065986>

## Superseded by this

- 2026-03-03 — treating the 2026-03-17 event as the release of FireRed-Image-Edit-1.1 is obsolete; 1.1 was announced on 2026-03-03.
- 2026-03-08 — treating the linked multi-image comparison graph as the official FireRedTeam 1.1 ComfyUI package is obsolete.
- 2026-04-14 — calling FireRed-Image-Edit-1.1-Lightning-8steps-v1.1 the newest official 1.1 Lightning artifact is obsolete.

## Still unknown

- No official source read announces a base-model version after 1.1; this does not prove that no unindexed regional release exists.
- The official package gives no explicit ComfyUI-version minimum, tested-GPU matrix or ComfyUI-specific performance benchmark.
- The March 17 workflow does not document compatibility between its 1.0-Lightning v1.1 pairing and the later 1.1-Lightning v1.2 file.
- GGUF weights are published, but the stock JSON selects safetensors and does not prove a GGUF loader graph.
- ControlNet and OpenPose compatibility were not confirmed by a primary FireRed source.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2602.13344 | FireRed-Image-Edit-1.0 Technical Report | 2026-09-06 |
| https://github.com/FireRedTeam/FireRed-Image-Edit | FireRedTeam/FireRed-Image-Edit README | 2026-09-06 |
| https://github.com/FireRedTeam/FireRed-Image-Edit/commits/main/ | Commits · FireRedTeam/FireRed-Image-Edit | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1 | FireRedTeam/FireRed-Image-Edit-1.1 | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commits/main | Commit history · FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/179def9bfaad5170a00b7760d7d1526ca53de019 | Upload firered-image-edit-1.1.json · commit 179def9 | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/blob/main/firered-image-edit-1.1.json?download=true | firered-image-edit-1.1.json | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/tree/main | FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI file tree | 2026-09-06 |
| https://huggingface.co/collections/FireRedTeam/firered-image-edit | FireRed-Image-Edit · FireRedTeam Collection | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/02dd2dc5586fcf7a60451506e7dee8dd31021455 | Upload FireRed-Image-Edit-1.1-Lightning-8steps-v1.1 · commit 02dd2dc | 2026-09-06 |
| https://huggingface.co/FireRedTeam/FireRed-Image-Edit-1.1-ComfyUI/commit/8625b60ec52d4fa0d128d8a6ebc8adba296f8592 | Upload FireRed-Image-Edit-1.1-Lightning-8steps-v1.2 · commit 8625b60 | 2026-09-06 |
| https://www.runninghub.ai/post/2030611704802971649 | Xiaohongshu FireRed Image edit 1.1 Single image editing VS qwen | 2026-09-06 |
| https://www.runninghub.ai/post/2030612012606169089 | Xiaohongshu FireRed Image edit1.1 Double image editing VS qwen | 2026-09-06 |
| https://www.runninghub.ai/post/2030612111793065986 | Xiaohongshu FireRed Image edit1.1 Multi-image editing vs qwen | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:firered-image-edit`, thread `comfyui-resources`, 1 dated events 2026-03-17 → 2026-03-17.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.