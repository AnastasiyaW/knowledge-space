---
title: HunyuanVideo-I2V — Public project availability
category: projects
tags: [hunyuanvideo, hunyuanvideo-i2v, project, public-project-availability]
aliases: ["HunyuanVideo-I2V"]
---

# HunyuanVideo-I2V — Public project availability

**Development line:** `project:hunyuanvideo-i2v` · thread `public-project-availability`  
**Events:** 1 dated, 2025-03-06 → 2025-03-06 · **Researched:** 2026-09-04 · confidence: medium

## What it is

HunyuanVideo-I2V — Tencent’s 2025 local image-to-video stack for practitioners who need first-frame-guided generation rather than a hosted API. - Takes a reference image and text prompt. - Includes official PyTorch code, pretrained weights, sampling, LoRA-effect training, and xDiT multi-GPU inference. - Generates up to 720p and 129 frames (about five seconds); official single-GPU guidance specifies 60 GB peak VRAM and tests on 80 GB. Verdict: the original stack remains runnable, but new deployments should compare the later HunyuanVideo-1.5 I2V line before committing hardware and integration work.

## Development line

- **2025-03-06 — HunyuanVideo-I2V public project resources were recorded.** On 2025-03-06, a dated record linked HunyuanVideo-I2V to its official Hugging Face page and Tencent GitHub repository. This establishes a public reference point for the project's model and source resources, without establishing a specific version, capability, or release claim.

## What changed

HunyuanVideo-I2V — the documented line starts with a local 720p release, then corrects its initial weights and adds scale-out inference. - 2025-03-06: Tencent released the inference code and model weights. - 2025-03-07, found today: Tencent replaced the release state after fixing an ID-change bug; the corrected weights are the source of truth for first-frame consistency. - 2025-03-09: no separate official code, weights, or version change dated this day was found; no implementation delta can be verified. - 2025-03-11, found today: Tencent updated LoRA training and inference code after the bug fix. - 2025-03-13, found today: Tencent released xDiT-powered parallel inference. - 2025-11-21, found today: Tencent released the separate HunyuanVideo-1.5 T2V/I2V line, with 480p and 720p I2V checkpoints; it is not documented as a drop-in continuation of this repository.

## How to use this

From 2025-03-06, practitioners should use the linked official Hugging Face page and Tencent GitHub repository as the canonical starting points for HunyuanVideo-I2V, and wait for archived update contents before acting on later announcements.

1. Confirm the original stack fits the machine: Linux and an NVIDIA CUDA GPU are required; plan for 60 GB peak VRAM at 720p, with 80 GB the tested configuration.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
2. Clone the official repository, create its Python 3.11.9 environment, install the documented PyTorch/CUDA dependencies and requirements; use the published CUDA 12 container if that matches the deployment.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
3. Download the current official HunyuanVideo-I2V weights from the Tencent model card and review the Tencent Hunyuan Community License before use.
  — <https://huggingface.co/tencent/HunyuanVideo-I2V>
4. Run sample_image2video.py with HYVideo-T/2, --i2v-mode, a reference-image path, a concise prompt, 720p resolution, sampling steps, video length, and an output path; enable CPU offload when needed for high-resolution generation.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
5. Choose stable or dynamic motion deliberately: stable mode uses --i2v-stability with --flow-shift 7.0; dynamic output uses stability off with --flow-shift 17.0. Set a seed when the result must be reproducible.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
6. For a custom effect, prepare video-caption training data, run the supplied LoRA training script, then load the produced safetensors file through --use-lora and --lora-path during inference.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>

## Best practices

- Do not retain the March 6 launch weights: use the corrected weights announced after the identity-change fix.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Keep the prompt short and concrete: specify subject and action, then add background or camera only when needed; overly detailed prompts can introduce unwanted transitions.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Use flow shift 7 with stable mode for steadier motion, and flow shift 17 with stable mode off when motion matters more than stability.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- Budget hardware from the documented 60 GB minimum rather than assuming CPU offload makes the 720p workflow low-VRAM; the official tested setup is 80 GB.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>
- For LoRA effects, put a phrase or short-sentence trigger directly in each video caption; train at 360p, then use the resulting LoRA for 720p inference.
  — <https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news>

## Superseded by this

- 2025-03-06 initial HunyuanVideo-I2V weights are superseded by the 2025-03-07 corrected weights because the initial open-source release could change identity.
- The 2025-03-06 deployment choice is dated, not formally deprecated: HunyuanVideo-1.5 released on 2025-11-21 as a separate later Tencent T2V/I2V line with 480p and 720p I2V checkpoints. Evaluate it for new deployments, but do not assume checkpoint or workflow compatibility.

## Still unknown

- The March 9 event cannot be tied to a distinct upstream release from the reviewed first-party records; the linked The source page was not retrievable.
- No first-party source reviewed here calls HunyuanVideo-1.5 a drop-in upgrade or formal replacement for HunyuanVideo-I2V.
- The reviewed sources do not state a current maintenance commitment, support window, or hosted API availability for the original HunyuanVideo-I2V stack.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Tencent/HunyuanVideo-I2V?tab=readme-ov-file#-news | HunyuanVideo-I2V README and news — Tencent-Hunyuan on GitHub | 2026-09-04 |
| https://huggingface.co/tencent/HunyuanVideo-I2V | tencent/HunyuanVideo-I2V model card — Hugging Face | 2026-09-04 |
| https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5 | HunyuanVideo-1.5 README — Tencent-Hunyuan on GitHub | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:hunyuanvideo-i2v`, thread `public-project-availability`, 1 dated events 2025-03-06 → 2025-03-06.
- **Practical note:** From 2025-03-06, practitioners should use the linked official Hugging Face page and Tencent GitHub repository as the canonical starting points for HunyuanVideo-I2V, and wait for archived update contents before acting on later announcements.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
