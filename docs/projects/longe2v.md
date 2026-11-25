---
title: LongE2V
category: projects

tags: [longe2v, longe2v-development, project]
aliases: ["LongE2V"]
---

# LongE2V

**Development line:** `project:longe2v` · thread `longe2v-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-06 · confidence: medium

## What it is

LongE2V is an open-source research stack for event vision, fine-tuned as a LoRA on THUDM/CogVideoX-5B-I2V.

- Video reconstruction from sparse event streams.
- Long-horizon prediction from sparse event streams.
- Frame interpolation from sparse event streams.

Standard run requires Linux, NVIDIA/CUDA 12.8, Python 3.10, and event voxels; no hosted inference provider exists. The stack fits reproduction and evaluation of event-camera tasks, not standard video generation from photos.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-12 — LongE2V appeared as a SIGGRAPH 2026 project with code for a unified diffusion approach to event-based reconstruction, prediction, and frame interpolation. 2026-07-14 — The associated LongE2V model and dataset on Hugging Face were marked updated; the public path now includes ready LoRA weights and preprocessed data for local reproduction.

## How to use this

1. Clone the repository, create a Python 3.10 environment, and install PyTorch 2.8.0 for CUDA 12.8 and project dependencies.
  — <https://github.com/cdfan0627/LongE2V>
2. Download the published LoRA file into weights/ and fetch the preprocessed data, or prepare event voxels manually.
  — <https://github.com/cdfan0627/LongE2V>
3. Choose reconstruction, prediction, or interpolation, and run the matching infer_*.sh with the DATASET value set.
  — <https://github.com/cdfan0627/LongE2V>
4. Process output frames before comparing metrics: resize, apply brightness correction for reconstruction and prediction, then run the matching metrics script.
  — <https://github.com/cdfan0627/LongE2V>

## Best practices

- LongE2V: do not substitute standard input images for event streams; the methods condition on event voxels and solve event-camera tasks.
  — <https://arxiv.org/abs/2607.08770>
- LongE2V: use the published data structure for reproducible results; missing or extra voxel files alter event chunks, and reverse voxels are needed only for interpolation.
  — <https://github.com/cdfan0627/LongE2V>
- LongE2V: run on one GPU and preserve compatibility with CUDA 12.8 and pinned packages; multi-GPU remains untested, and smaller ATTENTION_SCORE_CHUNK_SIZE saves memory at the cost of speed.
  — <https://github.com/cdfan0627/LongE2V>
- LongE2V: do not compare raw frames against published metrics; reconstruction and prediction metrics require a separate EVREAL environment because pyiqa conflicts with core dependencies.
  — <https://github.com/cdfan0627/LongE2V>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- LongE2V — no public changelog, tag, or GitHub Release exists, so exact dates of initial code and weight publication and subsequent semantic changes cannot be reliably recovered.
- LongE2V — availability and compatibility with arbitrary custom event data and GPUs were not confirmed by a live run; documentation confirms only the published research path.

## Sources

| source | title | read |
|---|---|---|
| https://cdfan0627.github.io/LongE2V-page/ | LongE2V — project page | 2026-09-06 |
| https://github.com/cdfan0627/LongE2V | cdfan0627/LongE2V — official implementation and README | 2026-09-06 |
| https://arxiv.org/abs/2607.08770 | LongE2V: Long-Horizon Event-based Video Reconstruction, Prediction, and Frame Interpolation with Video Diffusion Models | 2026-09-06 |
| https://huggingface.co/fansam39/LongE2V | fansam39/LongE2V — LoRA model card | 2026-09-06 |
| https://huggingface.co/datasets/fansam39/LongE2V-data | fansam39/LongE2V-data — preprocessed dataset | 2026-09-06 |
| https://huggingface.co/papers/2607.08770 | Hugging Face paper page for arXiv:2607.08770 | 2026-09-06 |
| https://github.com/cdfan0627/LongE2V/releases | LongE2V GitHub Releases | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:longe2v`, thread `longe2v-development`, 0 dated events - → -.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
