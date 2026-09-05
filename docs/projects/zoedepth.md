---
title: ZoeDepth
category: projects
date: 2023-03-01
tags: [project, zoedepth, zoedepth-public-release]
aliases: ["ZoeDepth"]
---

# ZoeDepth

**Development line:** `project:zoedepth` · thread `zoedepth-public-release`  
**Last event:** 2023-03-01 · 1 dated since 2023-03-01 · **Researched:** 2026-09-05 · confidence: high

## What it is

ZoeDepth is a PyTorch monocular depth estimation model that converts one RGB frame into an absolute depth map. ZoeD-M12-N, ZoeD-M12-K, and ZoeD-M12-NK cover indoor, outdoor, and mixed NYU+KITTI modes. The architecture combines relative-depth pretraining across 12 datasets with metric fine-tuning, and the NK version routes domains to their metric head automatically. Metric scale remains a single-camera estimate, and Intel no longer maintains the source repository. Use the Transformers checkpoint for reproducible legacy pipelines instead of waiting for repository fixes.

## Development line

- **2023-03-01 — ZoeDepth public project resources became available.** On 2023-03-01, ZoeDepth was linked through its GitHub repository, a Google Colab notebook, and two Hugging Face Spaces. The dated links show a public-access step spanning source code, a runnable notebook, and hosted demos. They do not establish a specific model version, benchmark result, or release wording.

## What changed

- 2023-03-01 — ZoeDepth became available through the official repository, Colab, and demos; published weights included ZoeD-M12-N, ZoeD-M12-K, and two-headed ZoeD-M12-NK.
- 2023-07-09 — no new confirmed version or model appeared: the link points to an earlier post about ZoeDepth.
- 2024-07-08 — Hugging Face Transformers added ZoeDepth, providing a standard loading and inference path through the depth-estimation pipeline.
- Current status — Intel declared the original repository unsupported; the Intel/zoedepth-nyu-kitti checkpoint remains available in Transformers.

## How to use this

From 2023-03-01, practitioners could evaluate ZoeDepth through its repository, Colab notebook, or hosted Hugging Face demos before integrating it into their own workflow.

1. Install compatible PyTorch and Transformers packages, then load Intel/zoedepth-nyu-kitti through pipeline("depth-estimation") for a single image.
  — <https://huggingface.co/Intel/zoedepth-nyu-kitti>
2. For the original ZoeDepth stack, load ZoeD_N, ZoeD_K, or ZoeD_NK through torch.hub; choose N for NYU indoor, K for KITTI outdoor, and NK for mixed settings.
  — <https://github.com/isl-org/ZoeDepth>
3. Pass an RGB image and save the numerical depth map; do not use color visualizations as raw metric data.
  — <https://github.com/isl-org/ZoeDepth>

## Best practices

- Use the published Transformers checkpoint and pin dependency versions for new inference pipelines: the official source repository receives no further updates.
  — <https://github.com/isl-org/ZoeDepth>
- Match the model to the data domain: N is trained for NYU, K for KITTI, and NK uses two metric heads for indoor and outdoor scenes.
  — <https://arxiv.org/abs/2302.12288>
- Test model loading and run test inference before batch processing; the repository provides sanity_hub.py and sanity.py for this check.
  — <https://github.com/isl-org/ZoeDepth>

## Superseded by this

- 2023-02-27: original torch.hub instructions are no longer the only launch path after the 2024-07-08 Transformers integration.
- Current guidance against treating the source repository as actively maintained: Intel explicitly announced the end of development, fixes, and new releases.

## Still unknown

- No standalone product release is confirmed for 2023-07-09: the available link points to an earlier post rather than a new ZoeDepth release.
- Metric depth accuracy on custom cameras and domains outside NYU and KITTI requires local ground-truth validation.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/isl-org/ZoeDepth | isl-org/ZoeDepth — official implementation and maintenance notice | 2026-09-05 |
| https://github.com/isl-org/ZoeDepth/releases | ZoeDepth releases — initial v1.0 | 2026-09-05 |
| https://arxiv.org/abs/2302.12288 | ZoeDepth: Zero-shot Transfer by Combining Relative and Metric Depth | 2026-09-05 |
| https://huggingface.co/docs/transformers/v4.48.0/model_doc/zoedepth | Hugging Face Transformers — ZoeDepth documentation | 2026-09-05 |
| https://huggingface.co/Intel/zoedepth-nyu-kitti | Intel/zoedepth-nyu-kitti model card | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:zoedepth`, thread `zoedepth-public-release`, 1 dated events 2023-03-01 → 2023-03-01.
- **Practical note:** From 2023-03-01, practitioners could evaluate ZoeDepth through its repository, Colab notebook, or hosted Hugging Face demos before integrating it into their own workflow.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
