---
title: "Agsoft Crop Face: agsoft-crop-face-update-line — Agsoft Crop Face Update Line"
category: "projects"
date: 2026-11-21
tags: ["agsoft-crop-face", "agsoft-crop-face-update-line", "project"]
aliases: ["Agsoft Crop Face: agsoft-crop-face-update-line"]
---

# Agsoft Crop Face: agsoft-crop-face-update-line — Agsoft Crop Face Update Line

AGSoft Crop Face is a ComfyUI node suite that detects, crops and masks faces in images and video, with RetinaFace weights bundled.

**Development line:** project:agsoft-crop-face · thread agsoft-crop-face-update-line  
**Last event:** 2026-11-21 · 1 dated since 2026-11-21 · **Researched:** 2026-11-22 · confidence: medium

## What it is

AGSoft Crop Face is a ComfyUI custom node suite for cropping faces in image and video workflows. It finds the face bounding box, builds a soft mask and stitches the crop back into the frame. It needs no InsightFace and no Impact Pack.

- Bundled MobileNet0.25 RetinaFace weights, so it runs locally with no setup
- Detection cache that holds across parameter changes
- Aspect ratio enforcement
- Configurable edge handling
- Crop metadata passed on to the companion Crop Stitch nodes

Detection is only as good as RetinaFace, so dense crowds and extreme occlusion are weak spots. Complex lighting needs manual threshold tuning.

## Development line

- **2026-11-21 — AGSoft Crop Face update adds face mask, detection cache and Crop Stitch integration.** AGSoft released an update to the AGSoft Crop Face ComfyUI node. It adds:
  - a face-shaped mask with `mask_softness`
  - a detection cache, so parameter changes skip re-running RetinaFace
  - a `crop_data` output for Crop Stitch, and a bbox output
  - sort and min-size filtering
  - `edge_mode` with `shift_inside` (the default) and `clamp`
  - `on_error` handling
  - per-frame mask support

  Crop Stitch gained a `face_mask` input, a `poisson_blend` fix and channel handling.
  - The node keeps the MobileNet0.25 RetinaFace weights inside its own repository. Face detection and cropping run without external pip dependencies or separate weight downloads. Cropped face dimensions are aligned to multiples of 8. (2026-11-21) — <https://github.com/Art-xmaster/comfyui-AGSoft>

## What changed

The first version made detection self-contained: RetinaFace with bundled MobileNet0.25 weights, so no model download. Later changes added:

- a face-shaped mask with adjustable softness
- a detection cache, so editing a parameter does not re-run the model
- crop data passed into Crop Stitch
- sorting and scale controls
- edge shifting
- per-frame mask tracking

## How to use this

1. Install comfyui-AGSoft through ComfyUI Manager, or clone the repository into the ComfyUI/custom_nodes directory.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
2. Connect an input image or batch to the AGSoft Crop Face node on the ComfyUI canvas.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
3. Set `confidence_threshold`, `number_of_faces`, `scale_factor` and `aspect_ratio` to isolate the target face box.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
4. Send the cropped face image to downstream processing. Link the `crop_data` and face mask outputs to Crop Stitch for compositing.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Best practices

- Keep `divisible_by` at 8, so cropped face sizes match the tensor requirements of standard VAE and diffusion models.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
- Set `scale_factor` to 2.0 to keep the hair and head around the face, instead of cropping at the face edge.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
- Set `edge_mode` to `shift_inside`, so faces near the image border do not cause coordinate clipping errors.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Superseded by this

- Downloading RetinaFace checkpoints by hand, or installing external InsightFace dependencies, is no longer required for face cropping in ComfyUI.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Still unknown

- Release version tags and commit hashes for the 2026-11-21 update are not documented in the material found.
- Community discussions and user benchmarks on Reddit or Hugging Face did not turn up in search results.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Art-xmaster/comfyui-AGSoft | Art-xmaster/comfyui-AGSoft: Custom nodes for ComfyUI | 2026-11-22 |

## Agent brief {#agent-brief}

- **Subject:** project:agsoft-crop-face, thread agsoft-crop-face-update-line, 1 dated events 2026-11-21 → 2026-11-21.
- **Practical note:** the usage and practice sections above carry the sources and their limits.
- **Confidence:** medium. The dated entries under "Superseded by this" say what is obsolete.
