---
title: Wan Video
category: projects
date: 2025-09-01
tags: [project, wan-video, wan-video-development, wan_video]
aliases: ["Wan 2.2", "Wan Video"]
---

# Wan Video

**Development line:** `project:wan-video` · thread `wan-video-development`  
**Last event:** 2025-09-01 · 2 dated since 2025-04-23 · **Researched:** 2026-09-05 · confidence: high

## What it is

Wan Video is Alibaba's open model family for video generation and video transformation.

- T2V: generates video from text prompts.
- I2V: animates still images into video.
- TI2V: generates video from combined text and image inputs.
- Speech-to-video: generates video driven by speech audio.
- Character animation and replacement: animates human figures and swaps characters across video.

TI2V-5B runs 720p on one GPU with 24 GB VRAM; A14B models require at least 80 GB VRAM in single-GPU mode. This is a practical local stack for controlled video generation, where model weight and VRAM set the runtime path.

## Development line

- **2025-04-23 — Wan Video opened a public video-creation workflow.** On 2025-04-23, an official wan.video page pointed users to a video-creation interface. The page alone does not show whether this marked a new launch, an update, or an existing tool.
- **2025-09-01 — Wan 2.2 received an orbit-shot camera LoRA.** On 2025-09-01, a Hugging Face repository published a Wan 2.2 I2V 14B LoRA for orbit camera motion. The repository does not clarify official status or tested environment compatibility.

## What changed

On 2025-04-23, the URL led to the Wan web interface. The current address redirects straight to the generator, but the source material does not tie this date to an independent model release. On 2025-09-01, a community LoRA for orbit camera motion on Wan2.2-I2V-A14B appeared. Repository commit history shows the files were added on 2025-08-20, so 1 September is not the release date of the adapter.

## How to use this

From 2025-04-23, practitioners can treat Wan Video as a public video-creation workflow; from 2025-09-01, they can evaluate a specialized Wan 2.2 I2V 14B orbit-shot LoRA when orbit-camera motion is needed, after verifying compatibility.

1. Choose TI2V-5B for a single 720p model covering T2V and I2V on one GPU with 24 GB VRAM; download the checkpoint and run `generate.py` with `--task ti2v-5B`.
  — <https://github.com/Wan-Video/Wan2.2>
2. Use Wan2.2-I2V-A14B for 480p or 720p I2V with an input image and prompt; the target resolution sets pixel area while aspect ratio comes from the input image.
  — <https://github.com/Wan-Video/Wan2.2>
3. Load both adapters into Diffusers on top of `Wan-AI/Wan2.2-I2V-A14B` to control camera orbit, then attach them to the I2V pipeline.
  — <https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora>
4. Feed a reference image and extracted pose and face features into Diffusers for character animation; raw video is not a valid pipeline input.
  — <https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan>

## Best practices

- Start with TI2V-5B when limited to one consumer GPU; allocate at least 80 GB VRAM or a distributed cluster for A14B.
  — <https://github.com/Wan-Video/Wan2.2>
- Enable `--offload_model True`, `--convert_model_dtype`, and `--t5_cpu` during OOM errors to trade execution speed for lower memory.
  — <https://github.com/Wan-Video/Wan2.2>
- Choose prompt expansion deliberately: local Qwen avoids external calls, while DashScope requires an API key and a remote dependency.
  — <https://github.com/Wan-Video/Wan2.2>
- Extract pose keypoints and facial features with default preprocessing scripts for Wan-Animate; never pass raw video files directly.
  — <https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan>

## Superseded by this

- 2025-07-28: Wan2.2 replaced Wan2.1 as the primary open baseline for new T2V, I2V, and TI2V tasks; Wan2.1 remains maintained for VACE and FLF2V.
- 2025-09-19: Wan2.2-Animate-14B replaced external pipelines as the official Wan path for animation and character replacement.

## Still unknown

- The primary source does not explain what changed in the web interface on 2025-04-23.
- Orbit Shot LoRA is a third-party adapter rather than an official Wan release; its model card lists Text-to-Image despite targeting Wan2.2 I2V.
- Test logs do not verify exact compatibility between the two LoRA files and specific Diffusers or UI wrapper versions.

## Sources

| source | title | read |
|---|---|---|
| https://wan.video/wanxiang/videoCreation | Wan AI: Leading AI Video Generation Model | 2026-09-05 |
| https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora | ostris/wan22_i2v_14b_orbit_shot_lora | 2026-09-05 |
| https://huggingface.co/ostris/wan22_i2v_14b_orbit_shot_lora/commits/main | Commit history for wan22_i2v_14b_orbit_shot_lora | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.1 | Wan2.1 | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.2 | Wan2.2 | 2026-09-05 |
| https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan | Wan pipelines — Diffusers documentation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:wan-video`, thread `wan-video-development`, 2 dated events 2025-04-23 → 2025-09-01.
- **Practical note:** From 2025-04-23, practitioners can treat Wan Video as a public video-creation workflow; from 2025-09-01, they can evaluate a specialized Wan 2.2 I2V 14B orbit-shot LoRA when orbit-camera motion is needed, after verifying compatibility.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
