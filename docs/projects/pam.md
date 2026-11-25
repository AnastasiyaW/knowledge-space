---
title: PAM — Public release
category: projects
date: 2026-03-26
tags: [pam, project, public-release]
aliases: ["PAM"]
---

# PAM — Public release

**Development line:** `project:pam` · thread `public-release`  
**Last event:** 2026-03-26 · 1 dated since 2026-03-26 · **Researched:** 2026-09-06 · confidence: medium

## What it is

PAM is a research pipeline for teams creating hand-object interaction data from simulation.

- Pose builds a trajectory from start and goal MANO poses, 6-DoF object pose, and object mesh.
- Appearance generates the first frame from depth, segmentation, and hand keypoints.
- Motion turns conditions and the chosen first frame into a video clip.

Authors report 301,1 s for 40 frames and a 41,4 GB peak on NVIDIA H20. This is an offline generator of synthetic HOI data, not a prompt-only video endpoint.

## Development line

- **2026-03-26 — PAM public project resources were made available.** The project website, code, and weight collection were linked together. The primary source confirms no new code or weight release on this day.

## What changed

- 2025-12-04 — PAM: Hugging Face added a four-part all-condition motion checkpoint for OakInk2.
- 2026-03-23 — PAM: arXiv v1 presented the three-stage pose–appearance–motion approach.
- 2026-03-25 — PAM: arXiv v2 published results on DexYCB and OAKINK2 before the primary mention date.
- 2026-03-26 — PAM: The project website, code, and weight collection were linked together, but the primary source confirms no new code or weight release on this day.
- 2026-04-02 — PAM: arXiv v3 updated the entry; the entry comment notes acceptance to CVPR 2026.

## How to use this

1. Check task fit first: PAM takes simulated HOI geometry and poses, not a single text prompt.
  — <https://arxiv.org/html/2603.22193v2>
2. Pick and pin a dataset-specific artifact, such as `dexycb_all_cond` or `oakink2_all_cond`, instead of treating the Hub root as a single checkpoint.
  — <https://huggingface.co/GasaiYU/PAM/tree/main>
3. Deploy the environment from `environment.yaml`, use CUDA 12.1, and install `manopth` as required by the official code.
  — <https://github.com/GasaiYU/PAM>
4. Prepare DexYCB or OakInk2: video, foreground-masked depth, segmentation, hand keypoints, captions, and filelists.
  — <https://github.com/GasaiYU/PAM>
5. For sim-to-real, pass rendered GraspXL RGB/normal/depth/segmentation/keypoints, generate and pick the first frame, then run the motion stage via `testing/evaluation_sim.py`.
  — <https://github.com/GasaiYU/PAM>

## Best practices

- Do not take the auto-generated prompt-only Diffusers example on the Hub as a verified recipe: use separate artifacts and input conditions from the authors' pipeline.
  — <https://huggingface.co/GasaiYU/PAM/tree/main>
- Keep all three conditions: depth, segmentation, and hand keypoints. The authors' ablation shows the best result when combining them.
  — <https://arxiv.org/html/2603.22193v2>
- Check geometry and filter the first frame before the motion stage: contact errors and a poor reference frame turn into physically implausible video and temporal flicker.
  — <https://arxiv.org/html/2603.22193v3>
- Plan the run as a heavy offline workload: one full 40-frame pass took 301,1 s on H20 in the paper, and the appearance stage reached 41,4 GB.
  — <https://arxiv.org/html/2603.22193v3>

## Superseded by this

- 2026-04-02 — arXiv v1 (2026-03-23) and v2 (2026-03-25) are replaced by the current v3 for citation and checking paper status.

## Still unknown

- The primary source provides no verifiable timestamp for the state of the project website, GitHub repository, and full Hugging Face tree on 2026-03-26; we cannot call this date a code or weight release.
- A separate weight license and author model card on the Hub are unconfirmed; Apache-2.0 on the source code does not prove terms for each checkpoint.
- No independent replication verified on the current code exists, so reported metrics and resource numbers remain author results.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/html/2603.22193v2 | PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/abs/2603.22193v2 | [2603.22193v2] PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/html/2603.22193v3 | PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://arxiv.org/abs/2603.22193v3 | [2603.22193v3] PAM: A Pose-Appearance-Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://github.com/GasaiYU/PAM | GitHub - GasaiYU/PAM: PAM: A Pose–Appearance–Motion Engine for Sim-to-Real HOI Video Generation | 2026-09-06 |
| https://huggingface.co/GasaiYU/PAM/tree/main | GasaiYU/PAM at main | 2026-09-06 |
| https://huggingface.co/GasaiYU/PAM/commit/1253ebb77e4b9ad9506aed5a770bfa2b1ffbc1a9 | Upload folder using huggingface_hub · GasaiYU/PAM at 1253ebb | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:pam`, thread `public-release`, 1 dated events 2026-03-26 → 2026-03-26.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
