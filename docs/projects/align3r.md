---
title: Align3R
category: projects
date: 2024-12-18
tags: [align3r, project]
aliases: ["Align3R"]
---

# Align3R

**Development line:** `project:align3r` · thread `align3r`  
**Last event:** 2024-12-18 · 2 dated since 2024-12-06 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Align3R is research code for reconstructing dynamic video from one camera.

- aligns per-frame monocular depth with a fine-tuned DUSt3R model
- produces temporally consistent depth maps, dynamic point clouds, and camera poses
- supports Depth Pro and Depth Anything V2 checkpoint paths

## Development line

- **2024-12-06 — Align3R public project resources were linked.** On 2024-12-06, Align3R published an official project page, a public source repository, and a supplementary project page. These links establish public code resources without detailing the release contents.
- **2024-12-18 — Align3R was linked to a hosted Hugging Face Space.** On 2024-12-18, a follow-up Align3R entry linked to the earlier project page and to an Align3R Hugging Face Space. The link shows a hosted access point, but the source post does not describe changes in the demo.

## What changed

2024-12-06 — Align3R appeared as an arXiv method with a project page, source code, and reconstructed point clouds. It combines monocular depth priors with DUSt3R alignment and optimization for dynamic video. 2024-12-18 — an interactive Align3R Space became available alongside local code; it is running today. Found today (2026-09-04) — the main README identifies version 1.0.2 and CVPR 2025 Highlight status. PromptDA refinement is complete; static-scene evaluation, more real training data, and camera-pose and point-correspondence prediction remain open.

## How to use this

As of 2024-12-06, practitioners could locate Align3R project materials and source code; as of 2024-12-18, they can also check the Hugging Face Space for hosted access.

1. Clone the official repository, create the documented Python 3.11 Conda environment, install a matching PyTorch/CUDA build, and install requirements.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
2. Compile the CroCo RoPE CUDA extension in croco/models/curope before running inference.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
3. Choose Depth Pro or Depth Anything V2, install that depth stack, then obtain the matching Align3R checkpoint and DUSt3R base weight.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
4. Set the input, output, and sequence placeholders in demo.sh, then run it on the selected GPU; the supplied launcher uses an interval of 50.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/demo.sh>
5. Use an MP4 or a directory of JPG/PNG frames; the demo generates monocular depth, reconstructs the scene, and writes poses, intrinsics, depth maps, masks, confidence maps, and RGB outputs.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/tool/demo.py>
6. For original-resolution refinement, install PromptDA separately and run demo_refine.sh; use the supplied viser command to inspect point clouds.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>

## Best practices

- Pin a repository commit and record the exact checkpoint set for reproducibility: no GitHub release artifact is published.
  — <https://github.com/jiah-cloud/Align3R/releases>
- Build the custom RoPE CUDA extension after dependency installation; a plain pip environment is not the documented runtime.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Keep the selected depth prior, its Align3R checkpoint, and the depth_prior_name evaluation setting consistent.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Establish a baseline with demo.sh before adding PromptDA refinement, which has a separate installation path.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>
- Before reporting Sintel results, reconcile the clean-versus-final split in the checkout; an open issue reports this mismatch.
  — <https://github.com/jiah-cloud/Align3R/issues/27>
- Review the repository's CC BY-NC-SA 4.0 terms before selecting it for commercial work.
  — <https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md>

## Superseded by this

- 2024-12-06: “arXiv preprint only” is obsolete as a status description; the repository labels Align3R a CVPR 2025 Highlight and exposes runnable v1.0.2 code.
- 2024-12-18: No verified replacement or deprecation of the interactive Space; it remains a secondary demo route rather than the reproducible local workflow.

## Still unknown

- No current GPU, driver, model-download, or end-to-end reconstruction receipt was obtained, so runtime compatibility and quality on a target video remain unverified.
- The version 1.0.2 README label does not identify an immutable package or checkpoint bundle because the repository has no GitHub release artifact.
- MPI-Sintel benchmark reproduction has an unresolved clean-versus-final split ambiguity in an open issue.
- The official README links the same Hugging Face Space, so the two dated entries do not appear to be different subjects; whether the deployed Space code exactly matches main is not stated.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2412.03079 | Align3R: Aligned Monocular Depth Estimation for Dynamic Videos — arXiv | 2026-09-04 |
| https://igl-hkust.github.io/Align3R.github.io/ | Align3R — official project page | 2026-09-04 |
| https://igl-hkust.github.io/Align3R.github.io/page1.html | Align3R — reconstructed point clouds | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R | jiah-cloud/Align3R — official repository | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/README.md | Align3R README — main branch | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/demo.sh | Align3R demo launcher — main branch | 2026-09-04 |
| https://raw.githubusercontent.com/jiah-cloud/Align3R/main/tool/demo.py | Align3R demo implementation — main branch | 2026-09-04 |
| https://huggingface.co/spaces/cyun9286/Align3R | Align3R — Hugging Face Space | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R/releases | Align3R releases | 2026-09-04 |
| https://github.com/jiah-cloud/Align3R/issues/27 | Align3R issue #27 — Sintel dataset split confusion | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:align3r`, thread `align3r`, 2 dated events 2024-12-06 → 2024-12-18.
- **Practical note:** As of 2024-12-06, practitioners could locate Align3R's project materials and source code; as of 2024-12-18, they should also check the linked Hugging Face Space for a hosted project access route.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
