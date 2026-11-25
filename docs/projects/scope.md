---
title: SCoPE
category: projects
date: 2026-08-14
tags: [project, scope, scope-public-resources]
aliases: ["SCoPE"]
---

# SCoPE

**Development line:** `project:scope` · thread `scope-public-resources`  
**Last event:** 2026-08-14 · 1 dated since 2026-08-14 · **Researched:** 2026-09-07 · confidence: medium

## What it is

SCoPE — an image-to-video research release for teams that need camera-path control on Wan2.2-I2V-A14B.

- Inputs: takes a first frame, text prompt, and target camera trajectory.
- Positional coordinate: adds each token’s camera ray as a second coordinate without a separate control branch.
- Inference weights: ships self-contained weights for its Wan2.2-I2V-A14B base.

The checkpoint is about 67 GB. Local inference requires Python 3.11 and a CUDA-capable GPU. The documented default example runs 81 frames at 480×832. Use it when you can supply compatible camera poses; inaccurate geometry, out-of-distribution paths, occlusion, and fast motion can reduce quality.

## Development line

- **2026-08-14 — SCoPE project resources were linked.** On 2026-08-14, public links connected the SCoPE project site, TencentARC source repository, and Hugging Face page. Together, these links provided public entry points for project information, source code, and model-hosting materials. They do not establish a release date, version, authorship, or capabilities.

## What changed

- 2026-06-25 — SCoPE paper v1 established ray-based positional encoding for video diffusion transformers.
- 2026-08-12 — arXiv v3 became the latest paper revision before the public links. The initial public code drop added inference and training code, examples, documentation, and a license.
- 2026-08-14 — The linked materials described an already-public SCoPE release. No distinct first-party release or paper change was found for this date.
- 2026-08-15 — The README documented the official Hugging Face demo.
- 2026-08-16 — The repository improved trajectory selection and demonstration workflows.
- 2026-08-22 — The repository restored missing vendored DiffSynth model sources. This repaired source layout rather than establishing new model performance.

## How to use this

1. Use the official browser demo to inspect the image-to-video camera-control workflow before a local setup.
  — <https://huggingface.co/TencentARC/SCoPE>
2. For reproducible local inference, clone the repository and create its pinned environment with `uv sync`. The documented release uses Python 3.11, PyTorch 2.9.1, and CUDA 12.8.
  — <https://github.com/TencentARC/SCoPE>
3. Download `TencentARC/SCoPE` into a local checkpoint directory. Keep room for the approximately 67 GB checkpoint and cache.
  — <https://huggingface.co/TencentARC/SCoPE>
4. Run a bundled case with an explicit trajectory, such as `omni-misty-forest` and `truck_right`, for a repeatable baseline.
  — <https://github.com/TencentARC/SCoPE>
5. For a custom run, supply a first image, prompt, OpenCV camera-to-world pose array, and horizontal field of view.
  — <https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md>

## Best practices

- Match the documented Python 3.11, PyTorch 2.9.1, and CUDA 12.8 environment when reproducing outputs. The project warns that PyTorch-version changes can alter numerical results.
  — <https://github.com/TencentARC/SCoPE>
- Use an explicit `--trajectory` for automated or repeatable jobs, and do not combine it with `--camera_path`.
  — <https://github.com/TencentARC/SCoPE>
- Validate custom poses as finite OpenCV camera-to-world arrays shaped `[81, 3, 4]` or `[81, 4, 4]`. Provide `x_fov` in horizontal radians and use `xi=0` for a pinhole camera.
  — <https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md>
- Keep both checkpoint and Hugging Face cache on local storage. Use `--vram_limit_gb` when VRAM management or offloading is needed.
  — <https://github.com/TencentARC/SCoPE>
- Use source at or after commit `449343d` for local checkout work because it restores omitted vendored DiffSynth model sources. Do not treat that repair as end-to-end inference proof.
  — <https://github.com/TencentARC/SCoPE/commit/449343d217c54b98cb182cbc00f318f892bfecef>

## Superseded by this

- 2026-08-22 — Guidance based on a pre-449343d checkout is superseded for a complete source layout. The later commit restores omitted vendored DiffSynth model sources. This is a repository repair, not a new model release.

## Still unknown

- No first-party page establishes an independent SCoPE release or paper change on 2026-08-14; the public code release and latest pre-event arXiv revision are dated 2026-08-12.
- Current README instructions include post-2026-08-14 improvements, so they are current operating guidance rather than proof of the exact initial workflow.
- No independent English- or Simplified-Chinese operator report was sufficient to elevate setup advice beyond the official documentation.
- SCoPE has unrelated name collisions in research and model search. The exact TencentARC repository, model ID, and arXiv ID define this entry.

## Sources

| source | title | read |
|---|---|---|
| https://visual-ai.github.io/scope/ | SCoPE: Sightline-Coordinate Positional Encoding for Video Diffusion Transformers | 2026-09-07 |
| https://github.com/TencentARC/SCoPE | TencentARC/SCoPE repository and README | 2026-09-07 |
| https://huggingface.co/TencentARC/SCoPE | TencentARC/SCoPE model card | 2026-09-07 |
| https://arxiv.org/abs/2606.27345 | SCoPE: Sightline-Coordinate Positional Encoding for Video Diffusion Transformers, arXiv:2606.27345 | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commits/main | TencentARC/SCoPE commit history | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/30226072dd5314dc7c4d91a25cdf3771b485e13e | Release SCoPE: inference + training code, examples, docs, and license | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/69baf9815e10afcb44cf794f76cb80e1f5c4155b | Update README.md | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/6658d0e | Improve inference trajectory selection and README demos | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/449343d217c54b98cb182cbc00f318f892bfecef | Fix missing vendored DiffSynth model sources | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md | SCoPE for Wan2.2-I2V-A14B model card | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:scope`, thread `scope-public-resources`, 1 dated events 2026-08-14 → 2026-08-14.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
