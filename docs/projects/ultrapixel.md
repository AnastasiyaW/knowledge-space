---
title: UltraPixel
category: projects
date: 2024-09-20
tags: [project, ultrapixel, ultrapixel-development]
aliases: ["UltraPixel"]
---

# UltraPixel

**Development line:** `project:ultrapixel` · thread `ultrapixel-development`  
**Last event:** 2024-09-20 · 2 dated since 2024-07-09 · **Researched:** 2026-09-05 · confidence: high

## What it is

UltraPixel — a NeurIPS 2024 research implementation built on Stable Cascade for text-to-image generation at multiple high resolutions.

- generates images through Stable Cascade stages with low-resolution semantic guidance;
- supports text-to-image, a supplied personalized-cat example, and Canny ControlNet;
- has a community ComfyUI wrapper with supplied workflows.

The published 24 GB RTX 4090 figures place a 4096×4096 generation across stages C, B and tiled A at roughly 311 seconds total. Verdict: usable for local high-resolution experiments, but its official demo is currently on Zero and no managed inference provider is listed.

## Development line

- **2024-07-09 — UltraPixel project page was shared.** On 2024-07-09, a dated UltraPixel post linked to the project's website. This is the earliest visible public reference for the project in the sealed development line. The underlying announcement text and technical claims were not provided.
- **2024-09-20 — UltraPixel repository and hosted demo were shared.** On 2024-09-20, a dated UltraPixel post linked to a GitHub repository and a Hugging Face Space, alongside a link back to the earlier The recorded link. This recorded public source and demo entry points for the project in the sealed line. The evidence does not establish the exact release state, code changes, or announcement wording.

## What changed

2024-07-09 — UltraPixel was presented as a cascade-diffusion method for 1K–6K text-to-image generation, using low-resolution guidance, implicit neural representations and scale-aware normalization. 2024-09-20 — the runnable implementation and hosted demo became available; the release supplied local Gradio and script inference, model downloads, ControlNet and personalization paths.

## How to use this

As of 2024-09-20, practitioners should use the linked GitHub repository and Hugging Face Space as UltraPixel's recorded source and demo entry points, while treating technical claims and exact release status as unverified until the linked materials are reviewed.

1. Install the repository dependencies, download the required Stable Cascade weights plus UltraPixel parameters, and place them in the repository's models directory.
  — <https://github.com/catcathh/UltraPixel>
2. Run the Gradio interface with CUDA_VISIBLE_DEVICES=0 python app.py, or use inference/test_t2i.py for scripted text-to-image generation.
  — <https://github.com/catcathh/UltraPixel>
3. For ComfyUI, clone the community node into custom_nodes, install its requirements, load workflow_default.json or workflow_controlnet.json, then queue the prompt; first run downloads models into ComfyUI/models/ultrapixel.
  — <https://github.com/2kpr/ComfyUI-UltraPixel>

## Best practices

- Use stage_a_tiled for Stage A decoding when VRAM is constrained; it avoids the documented out-of-memory condition at 4096×4096 on a 24 GB RTX 4090, at a substantial time cost.
  — <https://github.com/catcathh/UltraPixel>
- Use a prompt that specifies subject, background, colour, lighting and mood; treat quality modifiers as optional prompt experiments rather than a guarantee.
  — <https://github.com/catcathh/UltraPixel>
- Keep ControlNet within the documented 4K ceiling unless you fine-tune control weights; the published setup cites 3840×2160 and 2048×2048.
  — <https://github.com/catcathh/UltraPixel>

## Superseded by this

- 2024-09-19 — the repository’s earlier roughly three-minute RTX 4090 figure for a 2560×5120 generation was replaced by an approximately 60-second figure after its PyTorch and Torchvision environment update.
- 2024-09-26 — UltraPixel’s status changed from a preprint implementation to a NeurIPS 2024 accepted paper.

## Still unknown

- The official GitHub repository declares AGPL-3.0 while the Hugging Face model card declares Apache-2.0; the sources reviewed do not explain which licence governs a combined deployment, so verify this before commercial use.
- The public demo page reports that it is running on Zero; this does not establish that the Space is permanently unavailable, only that a live hosted session was not available when checked.
- No current, first-party maintained ComfyUI integration was found. The available ComfyUI node calls itself a work in progress and describes itself as a modified wrapper.
- No Chinese-language first-party or community operating source was verified for this item.

## Sources

| source | title | read |
|---|---|---|
| https://jingjingrenabc.github.io/ultrapixel/ | UltraPixel Gallery | 2026-09-05 |
| https://arxiv.org/abs/2407.02158 | UltraPixel: Advancing Ultra-High-Resolution Image Synthesis to New Peaks | 2026-09-05 |
| https://github.com/catcathh/UltraPixel | catcathh/UltraPixel | 2026-09-05 |
| https://huggingface.co/roubaofeipi/UltraPixel | roubaofeipi/UltraPixel model card | 2026-09-05 |
| https://huggingface.co/spaces/roubaofeipi/UltraPixel-demo | roubaofeipi/UltraPixel-demo | 2026-09-05 |
| https://github.com/2kpr/ComfyUI-UltraPixel | 2kpr/ComfyUI-UltraPixel | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ultrapixel`, thread `ultrapixel-development`, 2 dated events 2024-07-09 → 2024-09-20.
- **Practical note:** As of 2024-09-20, practitioners should use the linked GitHub repository and Hugging Face Space as UltraPixel's recorded source and demo entry points, while treating technical claims and exact release status as unverified until the linked materials are reviewed.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
