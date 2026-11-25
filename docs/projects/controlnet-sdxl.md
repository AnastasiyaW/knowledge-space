---
title: ControlNet for SDXL — SDXL ControlNet model releases
category: projects
date: 2023-08-14
tags: [controlnet-sdxl, controlnet_sdxl, project, sdxl-controlnet-model-releases]
aliases: ["ControlNet Depth for SDXL", "ControlNet OpenPose for SDXL", "ControlNet for SDXL"]
---

# ControlNet for SDXL — SDXL ControlNet model releases

**Development line:** `project:controlnet-sdxl` · thread `sdxl-controlnet-model-releases`  
**Last event:** 2023-08-14 · 3 dated since 2023-08-10 · **Researched:** 2026-11-21 · confidence: medium

## What it is

ControlNet for SDXL is a set of ControlNet checkpoints trained on Stable Diffusion XL base 1.0 for canny edge, depth and OpenPose pose conditioning.

- Checkpoints: diffusers/controlnet-sdxl-1.0 (canny), diffusers/controlnet-depth-sdxl-1.0 (depth), thibaud/controlnet-openpose-sdxl-1.0 (OpenPose v2).
- Users: diffusers pipeline users and ComfyUI users who condition SDXL on a structure image.
- Key capability: each checkpoint adds one control signal to SDXL image generation, with no change to the base model.
- Limits: the model cards state no known limitations; the depth card gives controlnet_conditioning_scale 0.5 as the recommended value; the OpenPose card lists its license as "other".

## Development line

- **2023-08-10 — Diffusers published an SDXL ControlNet example and model.** On 2023-08-10, Hugging Face Diffusers linked an SDXL-specific ControlNet example and the diffusers/controlnet-sdxl-1.0 model repository. This was a public development step to adapt ControlNet workflows to SDXL. The accompanying Reddit link is supplementary context rather than a separate event.
- **2023-08-14 — An OpenPose ControlNet model for SDXL was linked.** On 2023-08-14, the thibaud/controlnet-openpose-sdxl-1.0 model repository was linked. It provides an SDXL ControlNet option for OpenPose pose control, extending the available SDXL ControlNet model set.
- **2023-08-14 — A depth ControlNet model for SDXL was linked.** On 2023-08-14, the diffusers/controlnet-depth-sdxl-1.0 model repository was linked. It adds an SDXL ControlNet checkpoint for depth conditioning, providing a separate control modality alongside the OpenPose model.

## What changed

- 2023-08-12 — diffusers/controlnet-depth-sdxl-1.0 repository created (Hugging Face API, `createdAt`).
- 2023-08-13 — thibaud/controlnet-openpose-sdxl-1.0 repository created (Hugging Face API, `createdAt`).
- 2023-09-07 — the "SDXL ControlNets" collection that holds these checkpoints was last updated (model card).
- 2024-04-24 — the depth checkpoint repository was last modified (Hugging Face API, `lastModified`).

## How to use this

1. Choose the checkpoint by control signal: canny for edges, depth for depth maps, and OpenPose for human pose skeletons.
  — <https://huggingface.co/diffusers/controlnet-sdxl-1.0>
2. Load the checkpoint with `StableDiffusionXLControlNetPipeline` in float16. For depth, the card uses variant fp16, the sdxl-vae-fp16-fix VAE and 30 steps.
  — <https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0>
3. Preprocess the control image: depth maps from the Intel DPT estimator; OpenPose skeletons from controlnet_aux's OpenposeDetector, at 1024 × 1024 with 25 steps in the example.
  — <https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0>
4. Start with controlnet_conditioning_scale 0.5, the value both cards describe as recommended for generalization, and adjust from there.
  — <https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0>
5. Check the license before use: canny and depth are OpenRAIL++; OpenPose is "other" and refers to the OpenPose license.
  — <https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0>
6. To train a custom SDXL ControlNet, use diffusers' `train_controlnet_sdxl.py` and its README.
  — <https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md>

## Best practices

- Do not load SD 1.5 ControlNet checkpoints on SDXL; these checkpoints are trained on SDXL base 1.0.
  — <https://huggingface.co/diffusers/controlnet-sdxl-1.0>
- Use the fp16-fix VAE for SDXL. The diffusers README warns that SDXL's VAE "is known to suffer from numerical instability issues"; an alternative VAE must also be used at inference.
  — <https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md>

## Superseded by this

- Using an SD 1.5-era ControlNet checkpoint with SDXL is superseded by the SDXL-specific checkpoints above, which the cards state were trained on SDXL base 1.0.

## Still unknown

- The canny card's base-model field conflicts: its text names SDXL base 1.0, while the model-tree section lists runwayml/stable-diffusion-v1-5. We did not resolve this.
- The 2023-08-10 event (the Diffusers example) was not re-verified against a dated primary post.
- None of the three cards gives a release date; repository creation dates are shown above.
- Newer ControlNet families for SDXL are out of scope for this page.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/diffusers/controlnet-sdxl-1.0 | diffusers/controlnet-sdxl-1.0 model card (canny) | 2026-11-21 |
| https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0 | diffusers/controlnet-depth-sdxl-1.0 model card | 2026-11-21 |
| https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0 | thibaud/controlnet-openpose-sdxl-1.0 model card | 2026-11-21 |
| https://huggingface.co/api/models/diffusers/controlnet-depth-sdxl-1.0 | Hugging Face API: depth checkpoint dates | 2026-11-21 |
| https://huggingface.co/api/models/thibaud/controlnet-openpose-sdxl-1.0 | Hugging Face API: OpenPose checkpoint dates | 2026-11-21 |
| https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md | diffusers SDXL ControlNet training README | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:controlnet-sdxl`, thread `sdxl-controlnet-model-releases`, 3 dated events 2023-08-10 → 2023-08-14; checkpoint repositories created 2023-08-12 and 2023-08-13.
- **Practical note:** Pick the SDXL checkpoint by control signal, use the cards' recommended scale of 0.5 as a starting point, and check each card's license.
- **Confidence:** medium. Checkpoint facts are from the cards; the canny base-model field conflicts and was left unresolved. Dated supersedes above are the authority for what is obsolete.
