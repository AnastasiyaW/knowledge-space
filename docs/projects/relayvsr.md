---
title: "Relayvsr: relayvsr-release — Relayvsr Release"
category: "projects"
date: 2026-11-12
tags: ["project", "relayvsr", "relayvsr-release"]
aliases: ["Relayvsr: relayvsr-release"]
---

# RelayVSR: relayvsr-release — RelayVSR Release

**Development line:** project:relayvsr · thread relayvsr-release  
**Last event:** 2026-11-12 · 1 dated since 2026-11-12 · **Researched:** 2026-11-14 · confidence: high

## What it is

RelayVSR is an open-source framework for video super-resolution and enhancement. It is for researchers and video practitioners who want real-world restoration without the full latency of per-frame video diffusion models.

- Sparse generative keyframes: a large diffusion backbone generates only the keyframes.
- Intermediate frames: a lightweight Dual-Memory Video Transformer reconstructs the frames in between.
- Video-Aware Reference Optimization: suppresses temporal error propagation.
- Streaming inference: processes video in chunks with crossfading.

1080p video needs about 13.8 GB to 14 GB of VRAM and runs at 29.29 FPS on an NVIDIA A100 GPU. It fits local video restoration pipelines and ComfyUI workflows where standard video diffusion models are too slow or need too much memory.

## Development line

- **2026-11-12 — RelayVSR video enhancement neural network released.** RelayVSR came out as a neural network for local video enhancement. It runs on a GPU with more than 14 GB of memory. It is said to improve old VHS tapes and low-quality phone recordings. The code is in the project's GitHub repository.
  - The repository release includes code and model weights. A sparse generative backbone processes keyframes, for example every 15 frames, and a Dual-Memory Video Transformer handles the rest. At 1080p on an NVIDIA A100 GPU it reaches 29.29 FPS with 13.82 GB peak VRAM and 0.327-second initial latency. (2026-11-12) — <https://github.com/kopperx/RelayVSR>

## What changed

The framework started as research on large-small model collaboration in video processing. It is now a public codebase with dual-memory transformer decoding and sparse keyframe relay. Development then added:

- model checkpoints for two-times and four-times upscaling;
- reinforcement-learning-based reference optimization to curb drift between frames;
- community integration for streaming inference in ComfyUI nodes.

## How to use this

1. Clone the repository and install the dependencies, including PyTorch and torchvision.
  — <https://github.com/kopperx/RelayVSR>
2. Download the pretrained RelayVSR weights from Hugging Face for the 2x or 4x target.
  — <https://github.com/kopperx/RelayVSR>
3. Run inference with the provided test scripts or the ComfyUI custom nodes. Use streaming mode for long videos.
  — <https://github.com/kopperx/RelayVSR>

## Best practices

- Use a keyframe interval such as 15 frames. Throughput stays high and generative detail is still reconstructed.
  — <https://github.com/kopperx/RelayVSR>
- Turn on streaming mode with linear cross-fading for long sequences. VRAM use stays stable and chunk boundaries leave no artifacts.
  — <https://github.com/kopperx/RelayVSR>
- Use a GPU with at least 14 GB of VRAM so peak memory during keyframe latent generation fits.
  — <https://github.com/kopperx/RelayVSR>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Direct links to specific community discussions, such as ComfyUI node issues or forum threads. Search result redirects did not let us verify them without guessing.
- The exact minimum VRAM on consumer GPUs, for example 8 GB or 12 GB with aggressive quantization or offloading. The primary repository benchmarks do not document it; they report 13.82 GB peak on an A100.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/kopperx/RelayVSR | kopperx/RelayVSR: Official repository for RelayVSR video super-resolution | 2026-11-14 |

## Agent brief {#agent-brief}

- **Subject:** project:relayvsr, thread relayvsr-release, 1 dated events 2026-11-12 → 2026-11-12.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
