---
title: SAM2Matting
category: projects
date: 2026-07-15
tags: [project, sam2matting, sam2matting-public-release]
aliases: ["SAM2Matting"]
---

# SAM2Matting

**Development line:** `project:sam2matting` · thread `sam2matting-public-release`  
**Last event:** 2026-07-15 · 1 dated since 2026-07-15 · **Researched:** 2026-09-08 · confidence: medium

## What it is

SAM2Matting is an inference framework that turns foreground prompts into alpha mattes for image and video compositing.

- Matte refinement: turns masks, points, boxes, and SAM3 text prompts into fine-edge mattes.
- Video matting: combines temporal tracking with dedicated matting heads.

The released weights are 216 MB Tiny, 383 MB Base+, and 3.51 GB SAM3. Training code remains unreleased and CC BY-NC-SA 4.0 is non-commercial, so use it to evaluate inference rather than as a released training or commercial deployment stack.

## Development line

- **2026-07-15 — SAM2Matting public project resources became available.** On 2026-07-15, SAM2Matting was presented through linked official project, source-code, model-hosting, and interactive-demo resources. This marks a material public-access step for the project because readers could locate the implementation and evaluate it through the linked resources.

## What changed

- 2026-06-22 — SAM2Matting source repository was initialized.
- 2026-06-25 — SAM2Matting arXiv v1 was submitted and its three inference checkpoints were uploaded.
- 2026-06-30 — SAM2Matting removed `pip install -e .` and corrected dependencies; this remains the latest upstream GitHub change.
- 2026-07-09 — SAM2Matting received a Hugging Face model card and `image-segmentation` tag; this changed documentation, not weights or code.
- 2026-07-15 — SAM2Matting was available as a project-code-checkpoint-demo bundle; primary histories do not establish a new upstream release on this date.

## How to use this

1. Clone the upstream repository, create its Python 3.10 Conda environment, then run `pip install -r requirements.txt`.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>
2. Download an official checkpoint into `checkpoints/` and match it to the SAM2 or SAM3 script family.
  — <https://huggingface.co/FudanCVL/SAM2Matting>
3. For video, provide a first-frame foreground mask, then modify the demo script's hard-coded variant, input, mask, and output paths—or wrap it—before using your own media.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py>
4. For interactive prompts, use `interactive_sam2.py` for points or boxes and `interactive_sam3.py` for text.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>
5. For a browser trial, use the official Space with an image and rough foreground mask; it returns an alpha matte, composite preview, and transparent PNG.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>

## Best practices

- Use a mask that roughly covers the foreground with white as foreground; soft grayscale masks are recommended.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- Use SAM2.1-Tiny when speed matters; reserve SAM3 for cases where its prompt support justifies more VRAM and time.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- For Space-hosted video, seed the first frame and keep frame count modest; that limit is specific to the ZeroGPU demo.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- Do not automate the README's `--save_mp4` command unchanged: current code defines it as `store_false` while saving is the default.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py>
- Keep use non-commercial or obtain permission for another use case under the stated license.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>

## Superseded by this

- 2026-06-30 — the earlier setup instruction to add `pip install -e .` is obsolete; upstream removed it in favor of installing the listed requirements.

## Still unknown

- No first-party Chinese-language page or independently reproducible Chinese practitioner report was found in the Chinese search lane; no Chinese practical recipe is asserted.
- No owned local run or independent current quality/throughput benchmark was found; paper results are not used as production expectations.
- The official Space does not expose a stable absolute timestamp for its current deployment, so its current app state is not entered as a dated development event.
- The README and current code disagree about `--save_mp4`; a wrapper or code fix needs testing before repeatable automation.
- Official training code, a finetuning procedure, a supported-GPU matrix, and a minimum-VRAM requirement were not found.

## Sources

| source | title | read |
|---|---|---|
| https://henghuiding.com/SAM2Matting/ | SAM2Matting project page | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting | FudanCVL/SAM2Matting repository | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting | FudanCVL/SAM2Matting model repository | 2026-09-08 |
| https://huggingface.co/spaces/FudanCVL/sam2matting | FudanCVL/sam2matting Space | 2026-09-08 |
| https://arxiv.org/abs/2606.27339 | SAM2Matting: Generalized Image and Video Matting — arXiv | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/commits/main | Commits — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting/commit/6f92789a2a16ae899e81470a1b4dc47e08f40db3 | Upload checkpoints — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/commit/73dd721d77b56749248aefe5e8824d7f61b9d13c | update install and requirements — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting/discussions/1 | Model-card and pipeline-tag pull request — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/releases | Releases — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/blob/main/README.md | SAM2Matting README — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py | inference_video_sam2.py — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py | app.py — FudanCVL/sam2matting Space | 2026-09-08 |

## Agent brief {#agent-brief}

- **Subject:** `project:sam2matting`, thread `sam2matting-public-release`, 1 dated events 2026-07-15 → 2026-07-15.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
