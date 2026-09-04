---
title: ExAvatar — ExAvatar development
category: projects
tags: [exavatar, exavatar-development, project]
aliases: ["ExAvatar"]
---

# ExAvatar — ExAvatar development

**Development line:** `project:exavatar` · thread `exavatar-development`  
**Events:** 2 dated, 2024-08-01 → 2024-09-26 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ExAvatar — a research pipeline for graphics and avatar practitioners who need body, hand, and facial-expression control from a single-person monocular phone video, rather than X-Avatar’s 3D-scan/RGB-D input. — fits SMPL-X and FLAME to the capture; — trains a 3D Gaussian avatar; — renders novel body and hand poses, facial expressions, and viewpoints. Measure and limits: the project demonstrates a roughly 10-second neutral-pose phone scan; unseen mouth interiors, palm surfaces, and dynamic clothing can fail. Verdict: use it for controlled offline avatar research when the SMPL-X fitting stack is acceptable; do not use it where clothing deformation or unseen anatomy must be reliable.

## Development line

- **2024-08-01 — ExAvatar project website shared.** On 2024-08-01, ExAvatar was shared through its project website. The dated link provides a public project reference and marks an externally visible step in the project's development history.
- **2024-09-26 — ExAvatar release repository shared.** On 2024-09-26, ExAvatar was shared with a dedicated GitHub release repository. The dated repository link is a material public development step because it provides a release-oriented source beyond the earlier project website.

## What changed

2024-08-01 — ExAvatar was presented as an ECCV 2024 method combining SMPL-X with 3D Gaussian Splatting to make a controllable body, hand, and face avatar from a short phone scan. 2024-09-26 — ExAvatar_RELEASE made the official PyTorch reimplementation available with public assets and documented fitting, training, testing, and animation paths. Found today (2026-09-04) — the official repository and documentation remain public, but GitHub lists no packaged releases or release notes; reproducible use should record a chosen commit (inference).

## How to use this

As of 2024-09-26, practitioners should consult the ExAvatar release repository for release-oriented project materials, rather than relying only on the project website shared on 2024-08-01.

1. Create the Conda environment in an ExAvatar_RELEASE checkout: `conda env create -f environment.yml`, then `conda activate exavatar`.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/README.md>
2. Install the fitting prerequisites: SMPL-X 1.1, FLAME, DECA, Hand4Whole, MMPose, Segment Anything, Depth Anything V2, and COLMAP; run the repository’s `copy_code.py` customizations.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
3. Put one person’s video at `data/Custom/data/$SUBJECT_ID/video.mp4`, extract frames, create all/train/test frame lists, set `dataset = 'Custom'`, then fit SMPL-X with the documented camera mode.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
4. Generate foreground masks, create a background point cloud only for a static background, train with `main/train.py`, and inspect reconstruction output with `test.py`.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>
5. For an avatar exported under `output/model_dump/$SUBJECT_ID`, supply SMPL-X driving parameters and run `animation.py`; use `animate_view_rot.py` for a rotating camera render.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>

## Best practices

- Capture outdoors or otherwise avoid strong illumination and hard shadows; choose the static- or dynamic-background preprocessing path accordingly.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>
- Use fitting frames where most of the person is visible and untruncated; sampling about 5 fps from 30 fps is the documented speed-oriented starting point.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- Use COLMAP for a moving camera; use the virtual-camera path for a static capture or SMPL-X parameter extraction.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- If face fitting degrades, inspect `flame_init/renders` and verify that DECA results were prepared before rerunning the pipeline.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- Keep the SMPL-X shape, joint-offset, and face-offset identity parameters identical between training and evaluation.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>

## Superseded by this

- 2024-09-26 — For implementation, pre-release or project-page-only guidance is superseded by the public ExAvatar_RELEASE repository and its fitting and avatar READMEs.

## Still unknown

- The repository has no GitHub release package, and the reviewed sources provide no current VRAM target, training-time expectation, or supported CUDA/driver matrix.
- No reviewed first-party source declares ExAvatar deprecated or names an official successor.
- No reproducible Chinese-language operating report or independent community hardware recipe was verified; the listed practices are maintainer guidance.
- The 2024-09-26 The source permalink could not be retrieved and was not used as evidence.

## Sources

| source | title | read |
|---|---|---|
| https://mks0601.github.io/ExAvatar/ | ExAvatar project page | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE | ExAvatar_RELEASE official repository | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/README.md | ExAvatar_RELEASE README | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md | Fitting SMPL-X to a monocular video | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md | Creating an avatar from a phone scan | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/releases | ExAvatar_RELEASE GitHub Releases | 2026-09-04 |
| https://arxiv.org/abs/2407.21686 | Expressive Whole-Body 3D Gaussian Avatar | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:exavatar`, thread `exavatar-development`, 2 dated events 2024-08-01 → 2024-09-26.
- **Practical note:** As of 2024-09-26, practitioners should consult the ExAvatar release repository for release-oriented project materials, rather than relying only on the project website shared on 2024-08-01.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
