---
title: PowerPaint
category: projects
date: 2024-07-21
tags: [powerpaint, project]
aliases: ["PowerPaint"]
---

# PowerPaint

**Development line:** `project:powerpaint` · thread `powerpaint`  
**Last event:** 2024-07-21 · 2 dated since 2023-12-12 · **Researched:** 2026-09-04 · confidence: medium

## What it is

PowerPaint is an inpainting system based on Stable Diffusion for editing masked image areas.

- Text-guided object insertion to add elements from text prompts.
- Prompt-free object removal with optional negative prompts to erase objects.
- Image outpainting to extend canvas boundaries.
- Shape-guided object insertion to fit added elements to a mask outline.

## Development line

- **2023-12-12 — PowerPaint became publicly available.** On 2023-12-12, the project launched across its website, an MMagic implementation, and an OpenXLab application page.
- **2024-07-21 — Standalone OpenMMLab repository link.** On 2024-07-21, PowerPaint pointed users to the standalone open-mmlab/PowerPaint repository. The links mark this move without showing code or model changes.

## What changed

- 2023-12-12 — PowerPaint's paper introduced learnable task prompts so one model handles context filling, object insertion, removal, and shape guidance.
- 2023-12-18 — Stable v1 weights replaced the earlier build.
- 2023-12-22 — The maintainers fixed the ControlNet-loading error in the demo path.
- 2024-04-06 — Retraining with BrushNet produced PowerPaint v2 while keeping task-prompt cross-attention layers.
- 2024-04-07 — PowerPaint v2 code and weights were released.
- 2024-05-22 — PowerPaint v2-1 weights replaced initial v2 weights to fix training issues.
- 2024-07-21 — The public repository was available, but its changelog records no separate July 21 model release.

## How to use this

From 2023-12-12, the project ran through its site, MMagic, and OpenXLab; from 2024-07-21, use the standalone OpenMMLab repository.

1. Clone the repository, create a Conda environment with Python 3.9, and install the pinned requirements.
  — <https://github.com/open-mmlab/PowerPaint>
2. Install Git LFS, then download the PowerPaint v2 checkpoint into a local checkpoint directory.
  — <https://github.com/open-mmlab/PowerPaint>
3. Start the v2 Gradio UI with `python app.py --share --version ppt-v2 --checkpoint_dir checkpoints/ppt-v2`.
  — <https://github.com/open-mmlab/PowerPaint>
4. Upload an image, paint the edit mask, pick the task tab, and supply text only for object insertion or shape guidance.
  — <https://github.com/open-mmlab/PowerPaint>
5. Leave the text prompt empty for removal or outpainting; set horizontal and vertical expansion ratios for outpainting.
  — <https://github.com/open-mmlab/PowerPaint>

## Best practices

- Leave the prompt empty for object removal; add a negative prompt and raise Guidance Scale to 10 or higher if unwanted objects appear.
  — <https://github.com/open-mmlab/PowerPaint>
- Set fitting degree to 0.5–0.6 when the object can diverge from the mask, and 0.8–0.95 to match the mask shape closely.
  — <https://github.com/open-mmlab/PowerPaint>
- Use v2-1 weights instead of the initial v2 release, as maintainers shipped v2-1 specifically to correct training issues.
  — <https://github.com/open-mmlab/PowerPaint>

## Superseded by this

- 2023-12-22 — Early ControlNet demo guidance is obsolete because the loading logic was fixed.
- 2024-05-22 — Initial PowerPaint v2 weights are superseded by v2-1, which corrected training issues.

## Still unknown

- The repository has no tagged release for a distinct 2024-07-21 release; that date may reflect a repository move rather than a model update.
- Documentation covers local setup and the Gradio UI, but omits GPU memory limits, operating system support, and Diffusers compatibility.
- Neither the original project page nor the OpenXLab demo endpoint returned usable technical details during this check.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2312.03594 | A Task is Worth One Word: Learning with Task Prompts for High-Quality Versatile Image Inpainting | 2026-09-04 |
| https://github.com/open-mmlab/mmagic | MMagic — OpenMMLab generative-image and video toolbox | 2026-09-04 |
| https://github.com/open-mmlab/PowerPaint | open-mmlab/PowerPaint | 2026-09-04 |
| https://huggingface.co/JunhaoZhuang/PowerPaint_v2 | JunhaoZhuang/PowerPaint_v2 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:powerpaint`, thread `powerpaint`, 2 dated events 2023-12-12 → 2024-07-21.
- **Practical note:** From 2023-12-12, practitioners could find PowerPaint through its site, MMagic, and OpenXLab; from 2024-07-21, consult the standalone OpenMMLab repository.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
