---
title: QuerySplat
category: projects
date: 2026-08-04
tags: [project, querysplat, querysplat-development]
aliases: ["QuerySplat"]
---

# QuerySplat

**Development line:** `project:querysplat` · thread `querysplat-development`  
**Last event:** 2026-08-04 · 1 dated since 2026-08-04 · **Researched:** 2026-09-05 · confidence: medium

## What it is

QuerySplat is a feed-forward 3D Gaussian Splatting framework for people who need a renderable scene and novel views from multi-view images without pre-supplied camera poses.

- A dual-branch query decoder separates geometry from appearance.
- VGGT-Omega supplies camera and depth prediction; test-time optimisation is optional.

## Development line

- **2026-08-04 — On 2026-08-04, QuerySplat was linked through its project site, GitHub repository, and Hugging Face page..** On 2026-08-04, the dated record connected QuerySplat with a public project website, a GitHub repository, and a Hugging Face page. This is a material public-development milestone because it establishes linked project resources, but the available evidence does not support claims about a release version, functionality, or results.

## What changed

2026-08-02 — InSpatio labelled QuerySplat open source. 2026-08-04 — No separately versioned QuerySplat release is evidenced; its public paper and open-source status both point to the August 2 release.

## How to use this

As of 2026-08-04, practitioners should consult QuerySplat's linked project site, source repository, and Hugging Face page as its public resource set, and verify capabilities and release status directly from those resources before adopting it.

1. Prepare the tested stack: Linux, a CUDA-capable NVIDIA GPU, Python 3.12, PyTorch 2.11.0 and CUDA 12.8; then clone the official inference repository and install its requirements.
  — <https://github.com/inspatio/querysplat>
2. Download the QuerySplat checkpoint and bundled configuration into checkpoints, download vggt_omega_1b_512.pt there, then run sha256sum -c SHA256SUMS before inference.
  — <https://github.com/inspatio/querysplat>
3. Log in and accept the VGGT-Omega access conditions before downloading its checkpoint; its access is separately gated.
  — <https://huggingface.co/facebook/VGGT-Omega>
4. Put images from one scene in the input folder and run python -m scripts.infer with the supplied config, QuerySplat checkpoint, input folder and output directory.
  — <https://github.com/inspatio/querysplat>
5. Add --use_tto for test-time optimisation; omit it for feed-forward-only inference.
  — <https://github.com/inspatio/querysplat>

## Best practices

- Keep only one scene's images in each input folder. Any number of images is the upstream input interface, not a published scalability guarantee.
  — <https://github.com/inspatio/querysplat>
- Use the tested PyTorch/CUDA combination and make gsplat and fused-ssim extensions match it; LPIPS can download VGG16 weights on first use.
  — <https://github.com/inspatio/querysplat>
- Verify both downloaded checkpoints with the project's SHA-256 manifest before starting a run.
  — <https://github.com/inspatio/querysplat>
- Treat 30+ views as an unverified capacity zone: one August 6 user reported out-of-memory failure, without hardware, resolution, reproduction details or a maintainer response. Start smaller and measure VRAM; this is anecdotal, not an official limit.
  — <https://github.com/inspatio/querysplat/issues/2>
- Review licenses per component: QuerySplat-authored code is Apache-2.0, while the bundled VGGT-Omega/DINOv3 source is under the FAIR Noncommercial Research License.
  — <https://github.com/inspatio/querysplat>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No separately versioned QuerySplat release dated 2026-08-04 was found; public paper and open-source status are independently dated 2026-08-02.
- The checked official repository describes inference only. No official training-code release was verified in this research pass; an August 7 question about it remains open without a maintainer answer.
- No independent reproduction of the DL3DV result was located in this research pass; the reported 2.30 dB pose-free and 1.04 dB pose-required gains are author-reported paper results.
- The required VGGT-Omega dependency posted an August 18 warning about possible benchmark contamination in an ancestor checkpoint. It says downstream use can continue, but this does not establish a direct error in QuerySplat's DL3DV result.
- A first-party Simplified-Chinese description was found, but no independent Simplified-Chinese operating report was used.

## Sources

| source | title | read |
|---|---|---|
| https://inspatio.github.io/querysplat/ | QuerySplat project page | 2026-09-05 |
| https://github.com/inspatio/querysplat | QuerySplat official inference repository | 2026-09-05 |
| https://huggingface.co/inspatio/querysplat | QuerySplat model card and checkpoint | 2026-09-05 |
| https://arxiv.org/abs/2608.01186 | QuerySplat: Decoupling Geometry and Appearance Representations in 3DGS Prediction | 2026-09-05 |
| https://www.inspatio.com/models/querysplat | InSpatio QuerySplat model page | 2026-09-05 |
| https://huggingface.co/facebook/VGGT-Omega | VGGT-Omega model card and access conditions | 2026-09-05 |
| https://github.com/inspatio/querysplat/issues/2 | large scene reconstruction, QuerySplat issue 2 | 2026-09-05 |
| https://github.com/inspatio/querysplat/issues/3 | Will the training code be open-sourced?, QuerySplat issue 3 | 2026-09-05 |
| https://www.inspatio.com/zh/models | InSpatio open models, Simplified Chinese | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:querysplat`, thread `querysplat-development`, 1 dated events 2026-08-04 → 2026-08-04.
- **Practical note:** As of 2026-08-04, practitioners should consult QuerySplat's linked project site, source repository, and Hugging Face page as its public resource set, and verify capabilities and release status directly from those resources before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
