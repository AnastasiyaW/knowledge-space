---
title: Nunchaku — Model integration expansion
category: projects
date: 2026-01-23
tags: [model-integration-expansion, nunchaku, project]
aliases: ["Nunchaku"]
---

# Nunchaku — Model integration expansion

**Development line:** `project:nunchaku` · thread `model-integration-expansion`  
**Last event:** 2026-01-23 · 3 dated since 2025-08-03 · **Researched:** 2026-09-04 · confidence: high

## What it is

Nunchaku is an SVDQuant 4-bit inference engine for Diffusers and ComfyUI users who need lower-precision FLUX or Qwen Image transformers rather than another base model.

- Transformer weights: loads INT4 or FP4 SVDQuant weights through Diffusers-compatible classes.
- Framework support: supplies Python and ComfyUI routes for FLUX, Qwen Image/Edit, ControlNets and Z-Image.

We must match the wheel to PyTorch, CUDA, Python and GPU; the docs are labelled 1.3.0 while GitHub marks v1.2.1 as the latest formal release.
We use an official Nunchaku model namespace and version-matched workflow, and treat the QuantFunc 2511 artifact as a separate implementation.

## Development line

- **2025-08-03 — Nunchaku published FLUX.1-Krea-dev integration resources.** On 2025-08-03, Nunchaku added a Hugging Face repository and a GitHub example for FLUX.1-Krea-dev. The example documented an implementation path for that model.
- **2025-09-24 — Nunchaku documented Qwen Image Edit 2509 integration.** On 2025-09-24, Nunchaku documented usage for Qwen Image Edit 2509 and linked a model repository and ComfyUI workflow. These files provide an operational integration route for that image-editing variant.
- **2026-01-23 — A Nunchaku-named Qwen Image Edit 2511 model repository appeared.** On 2026-01-23, QuantFunc published the Nunchaku-Qwen-Image-EDIT-2511 repository on Hugging Face. The file introduced a subsequent Qwen Image Edit model artifact after the 2509 integration.

## What changed

- 2025-08-03 — Nunchaku added 4-bit support for FLUX.1-Krea-dev using SVDQuant transformer weights for the FLUX-compatible checkpoint.
- 2025-09-24 — Nunchaku released 4-bit Qwen-Image-Edit-2509 weights and Diffusers/ComfyUI integration, with INT4/NVFP4 and rank choices.
- 2026-01-23 — QuantFunc released the Nunchaku-named Qwen-Image-Edit-2511 checkpoint as an independent re-quantization rather than an official Nunchaku release.

## How to use this

As of 2026-01-23, select Nunchaku resources by the exact supported model variant and use the supplied model-specific documentation or workflow, so we do not assume one setup covers FLUX.1-Krea-dev and Qwen Image Edit variants.

1. Install a prebuilt wheel only after matching it to PyTorch 2.5 or later, CUDA, Python and GPU architecture; build from source only when no compatible wheel exists.
  — <https://nunchaku.tech/docs/nunchaku/installation/installation.html>
2. For ComfyUI, install the ComfyUI-nunchaku plugin, then install the Nunchaku backend into the same Python environment that ComfyUI runs.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/installation.html>
3. Download the matching Nunchaku quantized model and base-model assets, import an official example workflow, start ComfyUI, then select that workflow.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/usage.html>
4. For Qwen-Image-Edit-2509 in Python, load the Nunchaku transformer through NunchakuQwenImageTransformer2DModel, use QwenImageEditPlusPipeline with the upstream base model, and pass the RGB image list used by the official example.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
5. In ComfyUI's Wheel Installer, refresh the version list, select an official version, install it, then fully restart ComfyUI; use the separate development-version control only for development builds.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html>

## Best practices

- Use FP4 with RTX 50-series Blackwell GPUs and INT4 on the other listed GPU architectures; Blackwell also needs PyTorch 2.7 or later with CUDA 12.8 or later.
  — <https://nunchaku.tech/docs/nunchaku/installation/installation.html>
- For Qwen-Image-Edit-2509, choose r32 when speed matters and r128 when output quality matters more; do not compare their throughput as if they were equivalent configurations.
  — <https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509>
- On low VRAM, use Nunchaku asynchronous offloading; if adding Diffusers sequential CPU offload, exclude the Nunchaku transformer because its offloading path is different. The documented configuration can reduce use to about 3 GB.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
- Pin Qwen-Image-Edit-2509 to diffusers 0.36.0 or later and do not plan on official custom-LoRA support for it until the documentation changes.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
- Prefer the Wheel Installer's official version selector over its development-version selector for production work, and restart ComfyUI after any package change.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html>
- Keep QuantFunc's Qwen-Image-Edit-2511 weights outside the official Nunchaku compatibility path; they target QuantFunc's own engine and are explicitly independent of Nunchaku.
  — <https://www.modelscope.cn/models/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511>

## Superseded by this

- The 2025-09-24 state that Qwen-Image-Edit-2509 Lightning models would arrive later — obsolete since 2025-09-25.
- The assumption that every checkpoint bearing the word Nunchaku is an official Nunchaku project release — obsolete since the later QuantFunc clarification in 2026-07.

## Still unknown

- The current docs are labelled 1.3.0, but GitHub marks v1.2.1 as the latest formal release and lists only v1.3.0dev pre-releases; we found no stable v1.3.0 release note.
- We found no current official Nunchaku support page for Qwen-Image-Edit-2511. The 2026-01-23 QuantFunc checkpoint is an independent re-quantization, so it is not evidence of official Nunchaku compatibility.
- The original nunchaku-tech links redirect to nunchux-ai on GitHub and nunchaku-ai on Hugging Face. We found no separate official rename announcement, so reproduce workflows from the resolved target and pin the exact release or model file.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/nunchaku-tech/nunchaku | Nunchaku repository README | 2026-09-04 |
| https://github.com/nunchux-ai/nunchaku/releases | Nunchaku GitHub releases | 2026-09-04 |
| https://www.krea.ai/blog/flux-krea-open-source-release | Releasing Open Weights for FLUX.1 Krea | 2026-09-04 |
| https://huggingface.co/nunchaku-tech/nunchaku-flux.1-krea-dev/tree/main | nunchaku-flux.1-krea-dev model files | 2026-09-04 |
| https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509 | Nunchaku Qwen-Image-Edit-2509 model card | 2026-09-04 |
| https://huggingface.co/Qwen/Qwen-Image-Edit-2509 | Qwen-Image-Edit-2509 model card | 2026-09-04 |
| https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511 | QuantFunc Nunchaku-Qwen-Image-EDIT-2511 model card | 2026-09-04 |
| https://www.modelscope.cn/models/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511 | QuantFunc Nunchaku-Qwen-Image-EDIT-2511 on ModelScope | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/ | Nunchaku documentation 1.3.0 | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/installation/installation.html | Nunchaku installation guide | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509 | Nunchaku Qwen-Image-Edit usage guide | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/installation.html | ComfyUI-nunchaku installation guide | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/usage.html | ComfyUI-nunchaku usage guide | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html | ComfyUI-nunchaku wheel-installer workflow | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:nunchaku`, thread `model-integration-expansion`, 3 dated events 2025-08-03 → 2026-01-23.
- **Practical note:** As of 2026-01-23, select Nunchaku resources by the exact supported model variant and use the supplied model-specific documentation or workflow, so we do not assume one setup covers FLUX.1-Krea-dev and Qwen Image Edit variants.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
