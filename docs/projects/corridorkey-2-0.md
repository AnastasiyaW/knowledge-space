---
title: "CorridorKey 2.0: corridorkey-keying-tool — Corridorkey Keying Tool"
category: "projects"
date: 2026-10-22
tags: ["corridorkey-2-0", "corridorkey-keying-tool", "project"]
aliases: ["CorridorKey 2.0: corridorkey-keying-tool"]
---

# CorridorKey 2.0: corridorkey-keying-tool — Corridorkey Keying Tool

**Development line:** project:corridorkey-2-0 · thread corridorkey-keying-tool  
**Last event:** 2026-10-22 · 1 dated since 2026-10-22 · **Researched:** 2026-11-28 · confidence: medium

## What it is

CorridorKey 2.0 is a machine-learning keying and video-matting tool for green and blue screen footage. Its model was designed and trained by Zachary Harris in direct collaboration with Niko and Corridor Digital. It is available as a Python repository and as a paid plugin and stand-alone app sold at corridorkey.com.

## Development line

- **2026-10-22 — CorridorKey 2.0 released as a paid keying and matting tool.** The recorded link on 2026-10-22 announced CorridorKey 2.0, a second version of a keying tool offering matting without hints, separate alpha and foreground outputs, color spill removal, HDR and EXR output, and a paid version. It lists RTX 30-series or newer GPU requirements and about 5 GB weights, and states it is built on three third-party models: C-RADIOv4, MoGe-2 and RVM.
  - The repository confirms the free-versus-paid split. The Python repository and model may be used freely for commercial or personal work. The plugin and stand-alone app require a one-time purchase that covers all supported software. It also confirms the hardware requirements: an NVIDIA RTX 30-series or newer GPU, at least 4 GB of VRAM for footage up to 1440p and 6 GB for 4K. The model weights are about 5 GB. The three foundation models are C-RADIOv4-SO400M \(NVIDIA\), MoGe-2 ViT-B \(Microsoft\) and RVM small \(Google DeepMind\), downloaded from their original publishers. The tool supports a first-frame hint or a full hint video, and also runs native-resolution inference with no external hint. (undated) — <https://github.com/nikopueringer/CorridorKey2.0>

## What changed

The second version of CorridorKey is out. The repository says the model and software may be used freely for commercial or personal work, subject to the license. A separate plugin and stand-alone app, led by Ale Alvaro, covers almost every media software package. A one-time purchase unlocks all of them. The model builds on three frozen foundation models: C-RADIOv4-SO400M \(NVIDIA\), MoGe-2 ViT-B \(Microsoft\) and RVM small \(Google DeepMind\).

## How to use this

1. Check the requirements: an NVIDIA RTX 30-series or newer GPU with 4 GB of VRAM \(up to 1440p\) or 6 GB \(4K\), ffmpeg on PATH, and a Python environment with CUDA-enabled PyTorch. The package was tested with torch==2.9.1 and torchvision==0.24.1.
  — <https://github.com/nikopueringer/CorridorKey2.0>
2. From the repository root, create a virtual environment, install PyTorch and the dependencies from requirements.txt, then run python scripts/download\_weights.py. This fetches the CorridorKey 2.0 weights \(about 5 GB\) into weights/ and the three foundation models into vfms/.
  — <https://github.com/nikopueringer/CorridorKey2.0>
3. Drag a clip, a frame-sequence folder, or a folder of clips onto CorridorKey\_DRAG\_CLIPS\_HERE.bat \(Windows\) or CorridorKey\_DRAG\_CLIPS\_HERE.sh \(Linux\). The launcher walks you through the inference mode, outputs and GPU memory profile. You can also start the same guided session with python run\_interactive.py /path/to/clip.mp4.
  — <https://github.com/nikopueringer/CorridorKey2.0>
4. For a direct run, use python infer.py --input /path/to/input.mp4 --output\_dir /path/to/output. This does native-resolution inference with no external hint.
  — <https://github.com/nikopueringer/CorridorKey2.0>

## Best practices

- To give the model guidance, place companion hint files next to the input. The launcher picks them up automatically: \<clip\>FrameHint.png for a first-frame hint, and \<clip\>\_AlphaHint.mp4 for a full hint video.
  — <https://github.com/nikopueringer/CorridorKey2.0>
- On smaller GPUs or with long clips, consult the repository's 'Long Clips And Low VRAM' section.
  — <https://github.com/nikopueringer/CorridorKey2.0>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The price of the paid plugin and stand-alone app is not stated on the linked page.
- The repository excerpt does not describe the HDR/EXR output options, color spill removal strength control, or the alpha/foreground output variants in detail.
- The page is undated, so the exact release date of the repository is not confirmed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/nikopueringer/CorridorKey2.0 | GitHub - nikopueringer/CorridorKey2.0: Corridor Key 2.0 for all your green and blue screen needs | 2026-10-22 |

## Agent brief {#agent-brief}

- **Subject:** project:corridorkey-2-0, thread corridorkey-keying-tool, 1 dated events 2026-10-22 → 2026-10-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
