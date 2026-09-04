---
title: CutLER — CutLER development
category: projects
tags: [cutler, cutler-development, project]
aliases: ["CutLER", "VideoCutLER"]
---

# CutLER — CutLER development

**Development line:** `project:cutler` · thread `cutler-development`  
**Events:** 2 dated, 2023-03-01 → 2024-03-11 · **Researched:** 2026-09-04 · confidence: medium

## What it is

CutLER — a pseudo-mask-to-detector pipeline for unsupervised object detection and instance segmentation. - MaskCut generates multiple-instance pseudo-masks. - CutLER trains image detectors and segmentors from those masks. - VideoCutLER turns pairs of images into synthetic video trajectories, then trains video instance segmentation without human labels, natural video, or optical flow. Limit: the published setup targets Linux/macOS, Python 3.8+, PyTorch 1.8+, Detectron2, and OpenCV 4.6+; the repository has no tagged releases. Verdict: use it as research code or a reproducible baseline, and smoke-test the legacy dependency stack before committing to training.

## Development line

- **2023-03-01 — CutLER project resources became available.** On 2023-03-01, the CutLER project line was represented by a project page, source repository, MaskCut interactive space, and Colab notebook. Together, these linked resources made the work accessible for inspection and practical experimentation.
- **2024-03-11 — VideoCutLER documentation extended the CutLER project line.** On 2024-03-11, the CutLER repository linked to VideoCutLER documentation. This marked a video-focused development within the CutLER project line and connected it back to the earlier CutLER reference.

## What changed

2023-03-01 — CutLER established the image workflow: MaskCut produces pseudo-masks, then CutLER learns object detection and instance segmentation from ImageNet-1K without human annotations. 2023-08-27–29 [found today] — the official Git history places the VideoCutLER code addition before the later documentation event, in commits labelled “Add videocutler.” 2024-03-02 [found today] — official history records two further VideoCutLER commits, but their terse messages do not establish a specific functional delta. 2024-03-11 — VideoCutLER is documented as a separate video workflow: MaskCut → ImageCut2Video → video-model training, extending the project to tracking multiple instances across frames. 2025-06-03–04 [found today] — upstream updated VideoCutLER checkpoint links and its README. No tagged release is available.

## How to use this

From 2023-03-01, practitioners could use the CutLER repository, MaskCut space, and Colab resources to evaluate the project; from 2024-03-11, they should also consult the VideoCutLER documentation when their use case involves video.

1. Install the documented local stack: Linux or macOS, compatible PyTorch/torchvision and Detectron2, then clone CutLER recursively and install its requirements.
  — <https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md>
2. For still images, start with the local MaskCut or pretrained CutLER demo, selecting the matching model-zoo config and checkpoint and saving outputs locally.
  — <https://github.com/facebookresearch/CutLER>
3. For video inference, download the official VideoCutLER checkpoint and run `videocutler/demo_video/demo.py` on sequential image frames with the supplied Mask2Former config, an output directory, and model weights.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>
4. For retraining, prepare ImageNet-1K, generate or download MaskCut pseudo-masks, place the CutLER pretrain in `videocutler/pretrain`, then run `train_net_video.py`.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>

## Best practices

- Keep PyTorch, torchvision, and Detectron2 versions mutually compatible; the upstream example uses PyTorch 1.8.1, so treat a modern environment as a separate validation target.
  — <https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md>
- Use the local workflow instead of the MaskCut web demo: the official Hugging Face Space currently reports a build error.
  — <https://huggingface.co/spaces/facebook/MaskCut>
- For VideoCutLER, begin with the documented 0.8 confidence threshold; lower it only when higher recall is the priority, and save frames or masks for inspection.
  — <https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md>
- For large MaskCut annotation runs, shard folders with `--num-folder-per-job` and `--job-index`, then merge JSON files using matching `fixed_size`, `tau`, and `N` settings.
  — <https://github.com/facebookresearch/CutLER>
- Pin the exact repository commit and checkpoint used for a run, because upstream provides no tagged releases.
  — <https://github.com/facebookresearch/CutLER/tags>

## Superseded by this

- 2023-03-01: the MaskCut web-demo route is obsolete for current use; its official Hugging Face Space now reports a build error, so use local code instead.
- 2023-03-01: image-only CutLER guidance is incomplete for multi-instance video work; use VideoCutLER's dedicated inference and training workflow while retaining CutLER for still images.
- 2024-03-11: stale VideoCutLER checkpoint documentation should yield to the upstream README revision recorded on 2025-06-03–04; checkpoint availability was not independently downloaded.

## Still unknown

- The repository was not installed or run in this session; compatibility with current CUDA, PyTorch, and Detectron2 versions remains unverified.
- The original Berkeley project page and Colab notebook from 2023 could not be independently retrieved or run in this session, so neither supports a current-use claim.
- The official history identifies the March 2024 VideoCutLER update but not its exact behavioral change.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/facebookresearch/CutLER | Cut and Learn for Unsupervised Image & Video Object Detection and Instance Segmentation — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/blob/main/INSTALL.md | CutLER installation instructions — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/blob/main/videocutler/README.md | VideoCutLER: Unsupervised Video Instance Segmentation — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/commits/main | CutLER commit history — GitHub | 2026-09-04 |
| https://github.com/facebookresearch/CutLER/tags | CutLER releases and tags — GitHub | 2026-09-04 |
| https://huggingface.co/spaces/facebook/MaskCut | MaskCut — Hugging Face Space by facebook | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:cutler`, thread `cutler-development`, 2 dated events 2023-03-01 → 2024-03-11.
- **Practical note:** From 2023-03-01, practitioners could use the CutLER repository, MaskCut space, and Colab resources to evaluate the project; from 2024-03-11, they should also consult the VideoCutLER documentation when their use case involves video.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
