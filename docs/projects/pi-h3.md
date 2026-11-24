---
title: "Pi H3: pi-h3-acceleration — Pi H3 Acceleration"
category: "projects"
date: 2026-11-22
tags: ["pi-h3", "pi-h3-acceleration", "project"]
aliases: ["Pi H3: pi-h3-acceleration"]
---

# Pi H3: pi-h3-acceleration — Pi H3 Acceleration

**Development line:** project:pi-h3 · thread pi-h3-acceleration  
**Last event:** 2026-11-22 · 3 dated since 2026-11-22 · **Researched:** 2026-11-24 · confidence: high

## What it is

pi-H3 is an open-source distilled adapter and inference pipeline for MiniMax H3 video generation. It is for researchers and creative practitioners who run video generation locally or on a cluster.

- Fewer steps: sampling drops from twenty steps to two or four.
- Audio: synchronized stereo audio is kept.
- Decoding Without a Decoder (DWD): predicts output pixels directly, with no full VAE video decoder.
- Quantization: INT8 ConvRot is available for consumer GPUs.

It runs on ComfyUI 0.45.0 or later with the ComfyUI-piFlow extension, or with the LakonLab standalone inference scripts. At few steps it is faster than Sol-H3. Two-step motion fidelity still depends on the prompt and the conditioning setup.

## Development line

- **2026-11-22 — pi-H3 1.0 released with weights, inference code, and ComfyUI support.** On 2026-11-22 the pi-H3 1.0 video model came out as the fastest MiniMax H3 variant. It predicts pixels directly and uses a lightweight refiner instead of a full VAE decoder. Weights, inference code and ComfyUI support through the piFlow extension were published. Version 1.0 fixed minor motion and coherence problems at two steps.
- **2026-11-22 — pi-H3 1.0 released with faster video generation.** pi-H3 1.0 is a faster variant of the MiniMax H3 video model. It predicts pixels directly with a lightweight refiner, with no full VAE decoder. Weights, inference code and ComfyUI support through the piFlow extension were published, along with fixes to motion and coherence at two steps.
- **2026-11-22 — pi-H3 adapters released to speed up MiniMax H3 video generation.** Stanford researchers released pi-H3 adapters for MiniMax H3 that cut video generation to 2 to 4 steps. They cover text-to-video, image-to-video and first+last frame, with synchronized stereo audio. The adapters come in 2-step and 4-step variants, each with and without a DWD decoder-free option. The authors report 2.4 to 2.7 times faster than Sol-H3 at two steps on B200. They also report about 14.6 s for 480p/5 s on an RTX 3090 with ComfyUI int8.
- **2026-11-22 — other reporting on this date.**
  - The documentation says ComfyUI-piFlow needs ComfyUI 0.45.0 or later. It ships ready-to-use JSON workflows for the standard and the DWD decoder-free pipelines, with motion stabilization. (2026-11-22) — <https://github.com/Lakonik/ComfyUI-piFlow/blob/main/docs/piH3.md>
  - The model repository confirms separate 2-step and 4-step adapters in the weights. The DWD variants use pi-Flow v2 distillation plus a lightweight refiner to skip the full VAE decoder. (2026-11-22) — <https://huggingface.co/Lakonik/pi-H3>
  - The benchmarks show a 2.4x to 2.7x speedup over Sol-H3 at two steps on NVIDIA B200. They also confirm that the INT8 ConvRot quantized model generates 480p 5-second video in 14.6 seconds on a desktop RTX 3090. (2026-11-22) — <https://hanshengchen.com/blog/pi-h3/>

## What changed

The first goal was few-step distillation of MiniMax H3, to remove the delay of iterative twenty-step diffusion sampling. The design then split into standard distilled adapters and DWD decoder-free variants, which skip the heavy video VAE stage. ComfyUI support followed through dedicated piFlow nodes. After that came INT8 ConvRot quantization so the model fits consumer GPUs, plus adjustments to keep two-step motion coherent.

## How to use this

1. Update ComfyUI to 0.45.0 or later so the custom pi-Flow nodes work.
  — <https://github.com/Lakonik/ComfyUI-piFlow>
2. Install the ComfyUI-piFlow custom node package by cloning the repository into the `custom_nodes` directory.
  — <https://github.com/Lakonik/ComfyUI-piFlow/blob/main/docs/piH3.md>
3. Download the pi-H3 2-step or 4-step adapter weights from Hugging Face. The optional DWD decoder-free refiner checkpoint is there too.
  — <https://huggingface.co/Lakonik/pi-H3>
4. Load the bundled pi-H3 or pi-H3-DWD workflow JSON into ComfyUI, set the text prompts or reference frames, and run the sampling.
  — <https://github.com/Lakonik/ComfyUI-piFlow/blob/main/docs/piH3.md>

## Best practices

- On VRAM-constrained hardware, use the DWD decoder-free adapter so the full video VAE does not take the memory.
  — <https://huggingface.co/Lakonik/pi-H3>
- For local generation on consumer 24 GB GPUs such as the RTX 3090, use the INT8 ConvRot weights. That gives roughly 14 seconds for a 480p clip.
  — <https://hanshengchen.com/blog/pi-h3/>
- Pick the 4-step adapter over the 2-step one when a scene has fast, complex motion or needs precise fine detail.
  — <https://github.com/Lakonik/LakonLab/blob/main/docs/piH3.md>

## Superseded by this

- Standard 20-step iterative diffusion sampling with full VAE decoding, which MiniMax H3 needed for high-quality video with synchronized audio.
  — <https://huggingface.co/Lakonik/pi-H3>

## Still unknown

- Links to community discussion threads on Reddit and Discord could not be verified through search redirects, so none are listed.
- The training recipes and source code for the pi-Flow v2 distillation itself are not fully disclosed in the inference repositories.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Lakonik/pi-H3 | Lakonik/pi-H3 · Hugging Face | 2026-11-24 |
| https://github.com/Lakonik/ComfyUI-piFlow | Lakonik/ComfyUI-piFlow: Custom nodes for pi-Flow and pi-H3 acceleration in ComfyUI | 2026-11-24 |
| https://github.com/Lakonik/ComfyUI-piFlow/blob/main/docs/piH3.md | ComfyUI-piFlow/docs/piH3.md at main · Lakonik/ComfyUI-piFlow | 2026-11-24 |
| https://github.com/Lakonik/LakonLab/blob/main/docs/piH3.md | LakonLab/docs/piH3.md at main · Lakonik/LakonLab | 2026-11-24 |
| https://hanshengchen.com/blog/pi-h3/ | pi-H3: Accelerating MiniMax H3 Video Generation | 2026-11-24 |

## Agent brief {#agent-brief}

- **Subject:** project:pi-h3, thread pi-h3-acceleration, 3 dated events 2026-11-22 → 2026-11-22.
- **Practical note:** See the usage and best-practice sections above, including their limits.
- **Confidence:** high. The dated "Superseded by this" entries are the authority for what is obsolete.
