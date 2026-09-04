---
title: DDColor
category: projects
date: 2024-01-15
tags: [ddcolor, ddcolor-development, project]
aliases: ["DDColor"]
---

# DDColor

**Development line:** `project:ddcolor` · thread `ddcolor-development`  
**Last event:** 2024-01-15 · 1 dated since 2024-01-15 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DDColor is a PyTorch model from ICCV 2023 for automatic photo colorization.

- Monochrome photos: colorizes them automatically.
- Grayscale channels: recolorizes existing color images from them.
- Deployment: runs via local scripts, Hugging Face, ModelScope, Gradio, or ONNX export.

## Development line

- **2024-01-15 — DDColor source repository and Colab workflow were linked.** Camenduru published Colab and Gradio-Colab notebooks pointing to canonical DDColor code. This was a community wrapper, not a core-model release.

## What changed

The two January 2024 routes were wrappers around the same model, followed by official inference options.

- 2024-01-15: Camenduru published Colab and Gradio-Colab notebooks pointing to canonical DDColor code as a community wrapper, not a core-model release.
- 2024-01-22: ModelScope's Old Photo Restoration Space used `iic/cv_ddcolor_image-colorization` behind an upload-and-slider interface, confirming a DDColor integration rather than a separate restoration model.
- Official updates added Hugging Face integration on 2024-01-26, a fix on 2024-01-29, ONNX export support on 2024-10-25, a non-BasicSR local inference refactor on 2024-12-31, and streamlined loading and inference on 2026-01-17.

## How to use this

We can work with DDColor from the source repository and its Colab workflow since 2024-01-15. Verify the supported workflow in those resources before running it.

1. Create the documented Python 3.9 environment, then install PyTorch 2.2.0 with CUDA 11.8 and `requirements.txt`. The local inference route does not require BasicSR.
  — <https://github.com/piddnad/DDColor>
2. Start with `ddcolor_modelscope` for ordinary images outside ImageNet. Use `ddcolor_paper` only for paper reproduction, `ddcolor_artistic` for an alternate result, or `ddcolor_paper_tiny` when footprint matters.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
3. Run `python scripts/infer.py --model_name ddcolor_modelscope --input ./assets/test_images`. Alternatively, download the ModelScope checkpoint and pass its `pytorch_model.pt` through `--model_path`.
  — <https://github.com/piddnad/DDColor>
4. For Python integration, create a ModelScope `Tasks.image_colorization` pipeline with `iic/cv_ddcolor_image-colorization`, pass an image, and save `OutputKeys.OUTPUT_IMG`.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
5. Run `python demo/gradio_app.py` locally when an upload UI is needed.
  — <https://github.com/piddnad/DDColor>

## Best practices

- Use `ddcolor_modelscope` by default for images outside ImageNet. Reserve the paper model for reproduction rather than general use.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Compare `ddcolor_artistic` when color artifacts are a concern, since its training omitted colorfulness loss. Use `ddcolor_paper_tiny` when footprint matters.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Review comics, low-resolution inputs, and noisy images carefully, because the model was trained on natural photos.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
- Do not use the hosted Old Photo Restoration Space as the current entry point. It returns a runtime error caused by an incomplete model configuration download.
  — <https://huggingface.co/spaces/modelscope/old_photo_restoration>

## Superseded by this

- 2024-01-15 — Colab-only setup guidance: official local scripts, Hugging Face, ModelScope, Gradio, and ONNX routes replace it.
- 2024-01-22 — Hosted Old Photo Restoration Space demo: obsolete because it returns a runtime error.
- 2024-12-31 — BasicSR-dependent local inference: the current local script route does not require BasicSR.

## Still unknown

- The recorded link text was inaccessible, so its editorial claim and intended comparison could not be verified.
- The sources do not state whether historical ModelScope ID `iic/cv_ddcolor_image-colorization` and current repository ID `damo/cv_ddcolor_image-colorization` are aliases or a migration. Do not assume they are interchangeable.
- No current local inference run, hardware measurement, or benchmark against a newer colorizer was verified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/piddnad/DDColor | DDColor — official PyTorch implementation | 2026-09-04 |
| https://github.com/piddnad/DDColor/commits/master/ | DDColor commit history | 2026-09-04 |
| https://github.com/camenduru/DDColor-colab | camenduru/DDColor-colab | 2026-09-04 |
| https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md | DDColor Model Zoo | 2026-09-04 |
| https://huggingface.co/spaces/modelscope/old_photo_restoration | Old Photo Restoration — a Hugging Face Space by modelscope | 2026-09-04 |
| https://huggingface.co/spaces/modelscope/old_photo_restoration/blob/main/app.py | Old Photo Restoration app.py | 2026-09-04 |
| https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary | DDColor for Image Colorization | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:ddcolor`, thread `ddcolor-development`, 1 dated events 2024-01-15 → 2024-01-15.
- **Practical note:** We can begin DDColor work from the linked source repository and Colab workflow since 2024-01-15. Verify the exact supported workflow from those resources before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
