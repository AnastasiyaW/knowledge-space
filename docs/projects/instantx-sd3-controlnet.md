---
title: InstantX SD3 ControlNet — SD3 ControlNet checkpoint releases
category: projects
date: 2024-06-17
tags: [instantx-sd3-controlnet, project, sd3-controlnet-checkpoint-releases]
aliases: ["InstantX SD3 ControlNet"]
---

# InstantX SD3 ControlNet — SD3 ControlNet checkpoint releases

**Development line:** `project:instantx-sd3-controlnet` · thread `sd3-controlnet-checkpoint-releases`  
**Last event:** 2024-06-17 · 2 dated since 2024-06-15 · **Researched:** 2026-09-04 · confidence: medium

## What it is

InstantX SD3 ControlNet provides control-image adapters for practitioners who need Stable Diffusion 3 to follow structural inputs:
- Canny: follows edge outlines.
- Pose: follows human poses.
- Tile: follows tile and image guidance.
- Depth: follows depth maps.

Canny and Pose are 0.6B F16 checkpoints whose cards say training used 1024×1024 only. We use them when gated SD3 Medium and a 1024-square workflow fit. Compatibility with the later SD3-family is not established here.

## Development line

- **2024-06-15 — InstantX SD3 ControlNet Canny repositories appeared on Hugging Face.** On 2024-06-15, Hugging Face links associated with InstantX SD3 ControlNet pointed to a Canny_alpha_512 repository and a Canny repository. This made Canny-conditioned SD3 ControlNet artifacts available in this project line.
- **2024-06-17 — InstantX SD3 ControlNet Pose repository appeared on Hugging Face.** On 2024-06-17, a Hugging Face link associated with InstantX SD3 ControlNet pointed to the SD3-Controlnet-Pose repository. This added a pose-conditioned artifact to the recorded project line.

## What changed

- 2024-06-15 — Canny was initialized and received its config and checkpoint; the separate `Canny_alpha_512` endpoint remains unverified today.
- 2024-06-17 — Pose documentation and assets changed, while Tile received its checkpoint; Pose’s original checkpoint had landed on 15 June.
- 2024-06-19 — Canny installation moved from the InstantX `sd3_control` fork to `diffusers >= 0.30.0.dev0`.
- 2024-06-23 — SD3-Controlnet-Depth was created and received its checkpoint.
- 2025-04-24 — Canny’s config class name was corrected so direct `AutoModel.from_pretrained` loading works.

## How to use this

From 2024-06-15, practitioners could investigate InstantX SD3 ControlNet Canny artifacts for edge-guided workflows. From 2024-06-17, they could also investigate its pose-conditioned artifact for pose-guided workflows. Verify compatibility, licensing, revision, and workflow requirements before use.

1. Accept the Stable Diffusion 3 Medium access gate and authenticate with Hugging Face before downloading the base model.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>
2. Load `InstantX/SD3-Controlnet-Canny` as `SD3ControlNetModel`, attach it to `StableDiffusion3ControlNetPipeline` with `stabilityai/stable-diffusion-3-medium-diffusers`, and run it on CUDA in FP16.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
3. For pose control, substitute `InstantX/SD3-Controlnet-Pose` and provide a pose control image. Canny and Pose use distinct matching control inputs.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Pose>
4. Pass a prompt and `control_image`. For multiple controls, load a list of SD3 ControlNets and pass one matching image per control.
  — <https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sd3>
5. On constrained GPUs, use FP16 and model CPU offload before reducing quality settings. SD3’s three text encoders are challenging below 24 GB VRAM even in FP16.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>

## Best practices

- Start Canny or Pose at 1024×1024. Their cards say other resolutions can be suboptimal because training used 1024×1024 only.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
- Start with the author demo’s `controlnet_conditioning_scale=0.5`. Tune deliberately for each control image rather than treating it as universal.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Pose>
- Use the documented SD3 Medium base for a known-compatible recipe. Do not assume these checkpoints work unchanged with another SD3-family base.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
- A June 2024 Chinese ComfyUI hands-on report advised low weights, early control end, and treating results as a starting image. Retain that as a historical workflow observation, not a current universal range.
  — <https://www.youtube.com/watch?v=5SdRiZ53WPM>

## Superseded by this

- 2024-06-19 — The old installation path that cloned `instantX-research/diffusers_sd3_control` at `sd3_control` was replaced by the Diffusers requirement. Source: https://huggingface.co/InstantX/SD3-Controlnet-Canny/commit/a59221661ea027c11d813cbc595133ca8e56adb5
- 2025-04-24 — Canny configurations before the class-name correction do not support direct `AutoModel.from_pretrained` loading. Source: https://huggingface.co/InstantX/SD3-Controlnet-Canny/discussions/12

## Still unknown

- https://huggingface.co/InstantX/SD3-Controlnet-Canny_alpha_512 could not be retrieved in this research session. Its exact weights, resolution, and relationship to Canny are unverified.
- The retrieved 2024-07-03 Depth update is described only as an upload of two files, not as a named release, so its functional scope is unknown.
- No first-party current compatibility matrix was found for these Canny, Pose, Tile, and Depth checkpoints with SD3.5, current ComfyUI versions, or modern consumer-GPU VRAM.
- No explicit licence was verified from the retrieved Canny, Pose, or Tile cards. Do not infer their terms from the Apache-2.0 label visible on Depth.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/InstantX/SD3-Controlnet-Canny | InstantX/SD3-Controlnet-Canny | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose | InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose/tree/main | InstantX/SD3-Controlnet-Pose files | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/commits/e42ecba9741dee3de8c54039eba8a879c0070ced | Commit history — InstantX/SD3-Controlnet-Canny | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose/commits/main | Commit history — InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Tile/commits/main | Commit history — InstantX/SD3-Controlnet-Tile | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Depth/commits/main | Commit history — InstantX/SD3-Controlnet-Depth | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/commit/a59221661ea027c11d813cbc595133ca8e56adb5 | Canny README update, 19 June 2024 | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/discussions/12 | Canny config class-name correction | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sd3 | ControlNet with Stable Diffusion 3 — Diffusers | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3 | Stable Diffusion 3 — Diffusers | 2026-09-04 |
| https://www.youtube.com/watch?v=5SdRiZ53WPM | 在ComfyUI中使用新发布的SD3 ControlNet模型，对比SD1.5及SDXL同款，能控制但不够稳定 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:instantx-sd3-controlnet`, thread `sd3-controlnet-checkpoint-releases`, 2 dated events 2024-06-15 → 2024-06-17.
- **Practical note:** Practitioners could investigate InstantX SD3 ControlNet Canny artifacts for edge-guided workflows from 2024-06-15. They could also investigate its pose-conditioned artifact for pose-guided workflows from 2024-06-17. Verify compatibility, licensing, revision, and workflow requirements before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
