---
title: ControlVideo
category: projects
tags: [controlvideo, project]
aliases: ["ControlVideo"]
---

# ControlVideo

**Development line:** `project:controlvideo` · thread `controlvideo`  
**Events:** 2 dated, 2023-05-23 → 2023-07-09 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ControlVideo — a research implementation for practitioners who want a new SD 1.5 video constrained by a source clip and a text prompt. - extracts per-frame ControlNet conditions such as depth, edges, and pose; - adds full cross-frame attention, interleaved smoothing, and an optional hierarchical long-video sampler. Measure: its documented reference starts at 15 frames and 512×512; both public Hugging Face Spaces are currently unavailable. Verdict: use it to reproduce or adapt a 2023 local workflow, not as a no-setup browser tool.

## Development line

- **2023-05-23 — ControlVideo repository recorded in the development line.** On 2023-05-23, the ControlVideo development line was recorded with a link to its GitHub repository. This establishes the repository as the dated source-code entry point for the project, without establishing whether that date was its initial release.
- **2023-07-09 — ControlVideo demo route recorded alongside the repository.** On 2023-07-09, the ControlVideo development line was recorded with both its GitHub repository and a Hugging Face Space. The additional Space link marks a dated interactive-demo route alongside the code reference, though the supplied evidence does not establish when the Space itself launched or what functionality it exposed.

## What changed

ControlVideo — 2023-05-23: the paper was released. 2023-05-25 (found today in the official repository): source code was released. 2023-05-28 (found today): a Replicate demo was added. 2023-07-09: the recorded links added the fffiloni Space beside the official repository. 2023-07-11 (found today): ControlNet 1.1 support was added. 2023-07-16 (found today): the author linked a Hugging Face demo. On 2026-09-04, the fffiloni Space is paused and the author-linked Yabo Space has a storage-limit runtime error, so neither is a usable documented browser route.

## How to use this

From 2023-07-09, practitioners should treat ControlVideo as having both a repository entry point and a linked Hugging Face Space for initial evaluation, while verifying current compatibility and capabilities independently.

1. Create an isolated Python 3.10 environment and install the repository's pinned requirements.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
2. Download Stable Diffusion v1.5, the required ControlNet weights, and RIFE FlowNet weights into the documented checkpoints paths.
  — <https://github.com/YBYBZhang/ControlVideo>
3. Choose a condition that exists for the selected ControlNet version; for v10, use keys such as depth_midas, canny, or openpose, and provide matching checkpoints.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
4. Run the current inference.sh reference command with a source video and prompt, starting at 15 frames and 512×512.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
5. After the short run works, add --is_long_video to activate the hierarchical sampler for longer sequences.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>

## Best practices

- Treat the supplied dependencies as a legacy reproducibility environment: Torch 1.13.1+cu116, Diffusers 0.14.0, Transformers 4.26.1, and xFormers 0.0.16 are pinned; port and test explicitly before mixing a modern stack.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/requirements.txt>
- Match --condition, --version, and checkpoint paths. The current code maps v10 and v11 to different valid condition keys.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Use depth_midas rather than the README's generic depth example: current inference.sh and the v10 mapping use depth_midas.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.sh>
- Keep width and height divisible by 32, begin at 15 frames and 512×512, and retain the seed while comparing changes.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Inspect the saved source_video.mp4 and condition video before judging the generated result; the inference path writes both before sampling.
  — <https://github.com/YBYBZhang/ControlVideo/blob/master/inference.py>
- Do not base a current workflow on the author-linked browser demo; it currently reports a runtime error after storage-limit eviction.
  — <https://huggingface.co/spaces/Yabo/ControlVideo>

## Superseded by this

- 2023-07-09: treating the fffiloni Hugging Face Space as a runnable hosted route is obsolete; it is paused as observed on 2026-09-04.
- 2023-07-16: treating the author-linked Yabo Hugging Face Space as a runnable route is obsolete; it currently reports a storage-limit runtime error.
- The 2023-era README quickstart spelling --condition depth is obsolete for current master: use a mapped key such as depth_midas with the matching --version.

## Still unknown

- No clean 2026 CUDA/Python environment run was performed; compatibility beyond the pinned 2023 stack is unverified.
- No first-party Simplified-Chinese setup or migration document was found in the direct Chinese search, so this language lane remains unproven.
- The original dated messages' text is unavailable: the 2023-07-09 event proves its links, not the exact claim made at the time.
- There is a distinct THU ControlVideo project, arXiv:2305.17098, for one-shot text-to-video editing. The linked YBYBZhang repository and arXiv paper identify this entry as the separate training-free text-to-video project.

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

- **Subject:** `project:controlvideo`, thread `controlvideo`, 2 dated events 2023-05-23 → 2023-07-09.
- **Practical note:** From 2023-07-09, practitioners should treat ControlVideo as having both a repository entry point and a linked Hugging Face Space for initial evaluation, while verifying current compatibility and capabilities independently.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
