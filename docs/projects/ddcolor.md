---
title: DDColor — DDColor development
category: projects
tags: [ddcolor, ddcolor-development, project]
aliases: ["DDColor"]
---

# DDColor — DDColor development

**Development line:** `project:ddcolor` · thread `ddcolor-development`  
**Events:** 1 dated, 2024-01-15 → 2024-01-15 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DDColor — an ICCV 2023 PyTorch model for automatic photo colorization. - Colorizes monochrome images. - Recolorizes color images from their grayscale channel. - Runs through a local script, Hugging Face, ModelScope, Gradio, or ONNX export. Limit: its natural-image training makes comics, low-resolution inputs, and visibly noisy images unreliable. Verdict: use it as a colorization component, not as a complete damaged-photo restoration pipeline.

## Development line

- **2024-01-15 — DDColor source repository and Colab workflow were linked.** On 2024-01-15, links to the DDColor GitHub repository and a related Colab repository were recorded. This establishes a dated public access point for the project's source and a notebook-based way to work with it. The supplied evidence does not describe the exact software version or capabilities at that time.

## What changed

DDColor — the two January 2024 routes were wrappers around the same model, followed by official inference options. - 2024-01-15: camenduru published Colab and Gradio-Colab notebooks pointing to canonical DDColor code; this was a community wrapper, not a core-model release. - 2024-01-22: ModelScope's Old Photo Restoration Space used `iic/cv_ddcolor_image-colorization` behind an upload-and-slider interface, confirming it was a DDColor integration rather than a separate restoration model. - Found today: official history records Hugging Face integration on 2024-01-26, its fix on 2024-01-29, ONNX export support on 2024-10-25, a non-BasicSR local-inference refactor on 2024-12-31, and loading/inference streamlining on 2026-01-17. Limit: the sources do not document the relationship between historical `iic/` and current-repository `damo/` ModelScope identifiers. Verdict: use the current canonical repository workflow instead of relying on legacy hosted or Colab entry points.

## How to use this

From 2024-01-15, practitioners can begin DDColor work from the linked source repository and its related Colab workflow; the exact supported workflow should be verified from those resources before use.

1. Create the documented Python 3.9 environment, install PyTorch 2.2.0 with CUDA 11.8 and `requirements.txt`; the local inference route does not require BasicSR.
  — <https://github.com/piddnad/DDColor>
2. Start with `ddcolor_modelscope` for ordinary images outside ImageNet; use `ddcolor_paper` only for paper reproduction, `ddcolor_artistic` for an alternate result, or `ddcolor_paper_tiny` when footprint matters.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
3. Run `python scripts/infer.py --model_name ddcolor_modelscope --input ./assets/test_images`, or download the ModelScope checkpoint and pass its `pytorch_model.pt` through `--model_path`.
  — <https://github.com/piddnad/DDColor>
4. For Python integration, create a ModelScope `Tasks.image_colorization` pipeline with `iic/cv_ddcolor_image-colorization`, pass an image, and save `OutputKeys.OUTPUT_IMG`.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
5. Run `python demo/gradio_app.py` locally when an upload UI is needed.
  — <https://github.com/piddnad/DDColor>

## Best practices

- Use `ddcolor_modelscope` as the default for images outside ImageNet; reserve the paper model for reproduction rather than general use.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Compare `ddcolor_artistic` when color artifacts are a concern; its training omitted colorfulness loss, while `ddcolor_paper_tiny` is the lightweight variant.
  — <https://github.com/piddnad/DDColor/blob/master/MODEL_ZOO.md>
- Treat comics, low-resolution inputs, and noticeably noisy images as out-of-scope or review-required outputs because the model was trained on natural images.
  — <https://www.modelscope.cn/models/iic/cv_ddcolor_image-colorization/summary>
- Do not use the hosted Old Photo Restoration Space as the current entry point: when checked, it returned a runtime error caused by an incomplete model configuration download.
  — <https://huggingface.co/spaces/modelscope/old_photo_restoration>

## Superseded by this

- 2024-01-15 — Colab-only setup guidance is superseded in practice by official local-script, Hugging Face, ModelScope, Gradio, and ONNX routes.
- 2024-01-22 — treating the hosted Old Photo Restoration Space as a working DDColor demo is obsolete; it currently returns a runtime error.
- 2024-12-31 — the older local inference route that depended on BasicSR is superseded by the current local-script route documented as not requiring BasicSR.

## Still unknown

- The recorded link text was inaccessible, so its editorial claim and intended comparison could not be verified.
- The sources do not state whether the historical ModelScope ID `iic/cv_ddcolor_image-colorization` and the current repository ID `damo/cv_ddcolor_image-colorization` are aliases or a migration; do not assume they are interchangeable.
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
- **Practical note:** From 2024-01-15, practitioners can begin DDColor work from the linked source repository and its related Colab workflow; the exact supported workflow should be verified from those resources before use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
