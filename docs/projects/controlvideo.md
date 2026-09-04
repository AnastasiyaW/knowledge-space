---
title: ControlVideo
category: projects
date: 2023-07-09
tags: [controlvideo, project]
aliases: ["ControlVideo"]
---

# ControlVideo

**Development line:** `project:controlvideo` · thread `controlvideo`  
**Last event:** 2023-07-09 · 2 dated since 2023-05-23 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ControlVideo generates a new SD 1.5 video conditioned on a source video and a text prompt.

- Per-frame conditions: extracts ControlNet signals including depth, edges, and pose.
- Frame consistency: adds full cross-frame attention and interleaved smoothing.
- Long sequences: includes an optional hierarchical video sampler.

## Development line

- **2023-05-23 — ControlVideo GitHub repository appears.** On 2023-05-23, we track the GitHub repository as the source-code entry point for the project. The date marks when we saw the repository, not its confirmed initial release.
- **2023-07-09 — Hugging Face Space demo appears alongside the repository.** On 2023-07-09, we add the Hugging Face Space demo alongside the GitHub repository. The link provides an interactive demo route, though the exact launch date and original features remain unverified.

## What changed

ControlVideo releases progressed in stages:
- 2023-05-23: the paper was released.
- 2023-05-25: the source code was released in the official repository.
- 2023-05-28: a Replicate demo was added.
- 2023-07-09: the fffiloni Space appeared beside the official repository.
- 2023-07-11: ControlNet 1.1 support was added.
- 2023-07-16: the author linked a Hugging Face demo.
- 2026-09-04: the fffiloni Space is paused, and the author-linked Yabo Space fails with a storage-limit runtime error. Neither works as a documented browser demo.

## How to use this

From 2023-07-09, evaluate ControlVideo using the code repository or the linked Hugging Face Space, and verify compatibility locally.

1. Create an isolated Python 3.10 environment and install the pinned requirements.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
2. Download Stable Diffusion v1.5, the required ControlNet weights, and RIFE FlowNet weights into the documented checkpoints paths.
  — <https://github.com/YBYBZhang/ControlVideo>
3. Choose a condition supported by the target ControlNet version; for v10, pass keys such as depth_midas, canny, or openpose with matching checkpoints.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
4. Run the inference.sh reference command with a source video and prompt, starting at 15 frames and 512×512.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
5. Add --is_long_video after the short run succeeds to activate the hierarchical sampler for longer sequences.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>

## Best practices

- Isolate the pinned dependencies before upgrading. Torch 1.13.1+cu116, Diffusers 0.14.0, Transformers 4.26.1, and xFormers 0.0.16 form a legacy reproducibility stack.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
- Align --condition, --version, and checkpoint paths. The code maps v10 and v11 to distinct condition keys.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Specify depth_midas instead of the README generic depth option. The inference.sh script and the v10 mapping require depth_midas.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
- Keep frame width and height divisible by 32. Start tests at 15 frames and 512×512, and fix the seed to compare iterations.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Check the generated source_video.mp4 and condition video before evaluating output quality. The pipeline writes both files before sampling frames.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Avoid the author-linked browser demo for active work. The hosted Space crashes with a storage-limit runtime error.
  — <https://huggingface.co/spaces/Yabo/ControlVideo>

## Superseded by this

- 2023-07-09: running the fffiloni Hugging Face Space is obsolete because it is paused as of 2026-09-04.
- 2023-07-16: running the author-linked Yabo Hugging Face Space is obsolete because it fails with a storage-limit runtime error.
- The 2023 README argument --condition depth is obsolete on master. Pass a mapped key such as depth_midas with the corresponding --version.

## Still unknown

- Compatibility beyond the pinned 2023 stack remains unverified because we ran no tests in a clean 2026 CUDA and Python environment.
- Setup instructions in Simplified Chinese remain unverified because searches found no first-party documentation.
- The original 2023-07-09 message text is unavailable, so we verify the recorded links rather than the initial claim.
- The THU ControlVideo project under arXiv:2305.17098 is a distinct one-shot text-to-video editing method, not the training-free generation project tracked here.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/YBYBZhang/ControlVideo | ControlVideo — official PyTorch implementation | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt | ControlVideo requirements.txt — master | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py | ControlVideo inference.py — master | 2026-09-04 |
| https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh | ControlVideo inference.sh — master | 2026-09-04 |
| https://arxiv.org/abs/2305.13077 | ControlVideo: Training-free Controllable Text-to-Video Generation | 2026-09-04 |
| https://huggingface.co/spaces/fffiloni/ControlVideo | ControlVideo — Hugging Face Space by fffiloni | 2026-09-04 |
| https://huggingface.co/spaces/Yabo/ControlVideo | ControlVideo — Hugging Face Space by Yabo | 2026-09-04 |
| https://ml.cs.tsinghua.edu.cn/controlvideo/ | ControlVideo: Adding Conditional Control for One Shot Text-to-Video Editing | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:controlvideo`, thread `controlvideo`, 2 dated events from 2023-05-23 to 2023-07-09.
- **Practical note:** From 2023-07-09, evaluate ControlVideo using the code repository and Hugging Face Space, but test local dependencies independently.
- **Confidence:** medium. Superseded items above identify obsolete routes.