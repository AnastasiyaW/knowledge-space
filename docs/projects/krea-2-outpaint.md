---
title: Krea 2 Outpaint — Public resource distribution
category: projects
date: 2026-07-19
tags: [krea-2-outpaint, project, public-resource-distribution]
aliases: ["Krea 2 Outpaint"]
---

# Krea 2 Outpaint — Public resource distribution

**Development line:** `project:krea-2-outpaint` · thread `public-resource-distribution`  
**Last event:** 2026-07-19 · 1 dated since 2026-07-19 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Krea 2 Outpaint is a ComfyUI custom node pack that runs a rectangular outpainting LoRA on the open-weight Krea 2 Turbo image model.

- Users: ComfyUI users who extend images in a single pass.
- Key capability: the source image is placed at an explicit box in a larger canvas, extended right, left, up, down, or on both sides, and the original pixels are restored with a feathered seam.
- Limits: single pass only; rectangular extension only (not a mask-based inpainter); GGUF forks may break if they rename the Krea 2 model attributes the patch uses.

The LoRA weights are under the Krea 2 Community License; the node code is MIT. The node pack has 9 commits and no published releases or tags.

## Development line

- **2026-07-19 — Krea 2 Outpaint resources documented across Hugging Face and ComfyUI.** The stub recorded this date. This research did not verify the date of the source update; the repository and model links were read in their current state.

## What changed

- 2026-06-22 — Krea 2 open weights (Raw and Turbo, v1.0) published on Hugging Face; the node pack targets Krea 2 Turbo (model card date).
- 2026-07-19 — Resource links recorded (development line; date not independently verified).
- No release tags or dated releases for the node pack were found as of 2026-11.

## How to use this

1. Install a ComfyUI build with native Krea 2 support (or a compatible GGUF fork), then get Krea 2 Turbo, the Krea 2 VAE, and the Krea 2 Qwen3-VL CLIP. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>
2. Clone the repository into `ComfyUI/custom_nodes` and restart ComfyUI. The README states there are no extra Python dependencies. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>
3. Place `krea2_outpaint_rank32.safetensors` in `models/loras`. The LoRA is distributed on Hugging Face. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>
4. Wire Load Diffusion Model → Load LoRA → Rebels Krea2 Outpaint Model Patch (with `kv_cache` on) → KSampler. Use the Canvas node for source, direction, and target size. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>
5. Set 8 steps, euler sampler, CFG 1.0, denoise 1.0. Write the prompt to describe the complete output image, because the empty latent covers the full canvas. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>

## Best practices

- Use the node pack only for rectangular extension; for mask-based edits use a different inpainting tool. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>
- For a box fully inside the canvas, plan two passes; chaining passes is manual in this version. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>
- Check the license before commercial use: the LoRA falls under the Krea 2 Community License, while the node code is MIT. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>
- Pin the ComfyUI build and record the LoRA file hash, because forks may rename model attributes. — <https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The two Hugging Face Spaces listed in the stub were not read; their function and status are unverified.
- The LoRA model card was not read in full; the license summary comes from the node README.
- The relationship between the node pack and the LoRA author's release is not fully documented; the README credits the pipeline math to that release.
- The repository's first commit date and any output-quality results were not found.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/RealRebelAI/ComfyUI-Rebels-Krea2-Outpaint | ComfyUI-Rebels-Krea2-Outpaint README | 2026-11-21 |
| https://www.krea.ai/krea-2 | Krea 2 (product page and FAQ) | 2026-11-21 |
| https://huggingface.co/krea/Krea-2-Raw | Krea 2 Raw model card (search snippet; release date June 22, 2026) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:krea-2-outpaint`, thread `public-resource-distribution`, 1 dated event 2026-07-19 (stub, unverified date); base-model release 2026-06-22.
- **Practical note:** As of 2026-11, use the ComfyUI node pack for single-pass rectangular outpainting on Krea 2 Turbo, with the 8-step euler settings from the README. Check the Krea 2 Community License before commercial use.
- **Confidence:** medium. Node README and Krea product page read; LoRA model card and Spaces not read. Dated supersedes above are the authority for what is obsolete.
