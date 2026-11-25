---
title: "Steppe-Wan2.1: steppe-wan2-1-latent-upscaler-release — Steppe Wan2 1 Latent Upscaler Release"
category: "projects"
date: 2026-11-22
tags: ["project", "steppe-wan2-1", "steppe-wan2-1-latent-upscaler-release"]
aliases: ["Steppe-Wan2.1: steppe-wan2-1-latent-upscaler-release"]
---

# Steppe-Wan2.1: steppe-wan2-1-latent-upscaler-release — Steppe Wan2 1 Latent Upscaler Release

**Development line:** project:steppe-wan2-1 · thread steppe-wan2-1-latent-upscaler-release  
**Last event:** 2026-11-22 · 2 dated since 2026-11-22 · **Researched:** 2026-11-23 · confidence: high

## What it is

Steppe-Wan2.1 is a latent-space upscaler from TensorForger for people who run diffusion pipelines in the Wan 2.1 VAE latent space. It does four things:

- Spatial upscaling, 2x, for image and video generations. It needs no text conditioning and no re-sampling of the base model.
- Temporal frame interpolation, 2x, in latent space. It doubles the video frame rate in a single forward pass.
- High-frequency feature (HFF) parameter. It sets edge sharpness and fine texture.
- Direct insertion in ComfyUI, between sampling and VAE decode.

Limit: it works only inside the Wan 2.1 VAE latent distribution. It cannot upscale pixel-space images directly. Models with incompatible latent dimensions need VAE re-encoding first. In return you get 2x resolution and 2x frame rate at lower compute cost than a full secondary diffusion pass.

## Development line

- **2026-11-22 — Steppe-Wan2.1 latent-space upscaler released.** On 2026-11-22 the Steppe-Wan2.1 project announced a 2x latent-space upscaler in three variants: a 200M base model with CFG, a one-step distilled variant, and a 20M lightweight model for real-time use. It was trained from scratch in about 300 GPU-hours. It uses local-window attention and a causal temporal branch for streaming frames. Code and model links were published.
- **2026-11-22 — Steppe-Wan2.1 latent-space upscaler released.** On 2026-11-22 the Steppe-Wan2.1 project announced a 2x latent-space upscaler in three variants: a 200M-parameter base with CFG, a one-step distilled version, and a 20M-parameter lightweight model. It was trained from scratch on millions of samples in about 300 GPU-hours. Its causal temporal branch suits streaming frames. Code and model links were published.
- **2026-11-22 — more detail on the same date.**
  - The Hugging Face files and sizes are `steppe_wan_2_1_200M_1step.safetensors` (222M parameters, single-step distilled), `steppe_wan_2_1_200M_base.safetensors` (222M parameters, 1–200 steps) and `steppe_wan_2_1_20M_1step.safetensors` (19.5M parameters, lightweight). The release adds High-Frequency Feature (HFF) conditioning for sharpness control. (2026-11-22) — <https://huggingface.co/TensorForger/Steppe-Wan2.1>
  - One pass gives 2x spatial upscaling and 2x temporal latent frame interpolation together, for example 640x512 at 16fps to 1280x1024 at 32fps. It plugs into ComfyUI through the ComfyUI-Steppe node (Steppe Upscale Latent). It needs no second text prompt, no hires fix and no re-sampling of the base model. (2026-11-22) — <https://github.com/tensorforger/ComfyUI-Steppe>

## What changed

The project started as a family of latent-space upscalers, trained from scratch on Wan 2.1 latent tensors. The release has three checkpoints. The multi-step base uses classifier-free guidance. The single-step distilled one is for high-throughput generation. The compact one is for tight memory. Tooling followed: dedicated ComfyUI nodes and Hugging Face demo spaces, so the latent can go in directly before VAE decoding.

## How to use this

1. Install the ComfyUI-Steppe extension with ComfyUI-Manager, or run comfy node install steppe in the terminal.
  — <https://github.com/tensorforger/ComfyUI-Steppe>
2. Download one checkpoint (`steppe_wan_2_1_200M_1step.safetensors`, `steppe_wan_2_1_200M_base.safetensors` or `steppe_wan_2_1_20M_1step.safetensors`) into ComfyUI/models/latent_upscale_models.
  — <https://huggingface.co/TensorForger/Steppe-Wan2.1>
3. Put the Steppe Upscale Latent node between the KSampler output latent and the VAE Decode node.
  — <https://github.com/tensorforger/ComfyUI-Steppe>
4. Set the scaling factor to 2x. If you want a sharper result, adjust the high-frequency feature (HFF) conditioning before decoding to pixel space.
  — <https://huggingface.co/TensorForger/Steppe-Wan2.1>

## Best practices

- Use `steppe_wan_2_1_200M_1step.safetensors` by default for standard workflows. In a single forward step it matches the fidelity of base model generation.
  — <https://huggingface.co/TensorForger/Steppe-Wan2.1>
- Pick `steppe_wan_2_1_20M_1step.safetensors` for extreme high-resolution canvases, or for real-time streaming video frames under strict VRAM limits.
  — <https://huggingface.co/TensorForger/Steppe-Wan2.1>
- Chain two 2x latent passes to get 4x. That avoids intermediate pixel-space VAE encodes and decodes.
  — <https://huggingface.co/TensorForger/Steppe-Wan2.1>

## Superseded by this

- Upscaling Wan 2.1 latents meant a full secondary base-model diffusion pass (such as Hires Fix with prompt re-conditioning). The other route was deterministic latent scaling, which loses high-frequency detail.
  — <https://huggingface.co/TensorForger/Steppe-Wan2.1>
- Temporal frame interpolation for latent video meant separate frame-interpolation models in pixel space, after VAE decoding.
  — <https://huggingface.co/TensorForger/Steppe-Wan2.1>

## Still unknown

- Long-term community benchmarks and independent quality checks are not indexed in the primary public repositories. That includes any comparison of Steppe-Wan2.1 with pixel-space ESRGAN or Compact upscalers on video artifacts.
- The Reddit discussion threads could not be verified, so their exact paths are unknown.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/TensorForger/Steppe-Wan2.1 | TensorForger/Steppe-Wan2.1 · Hugging Face | 2026-11-23 |
| https://github.com/tensorforger/ComfyUI-Steppe | tensorforger/ComfyUI-Steppe: ComfyUI node for Steppe latent upscaler | 2026-11-23 |
| https://huggingface.co/spaces/TensorForger/Steppe | Steppe - a Hugging Face Space by TensorForger | 2026-11-23 |

## Agent brief {#agent-brief}

- **Subject:** project:steppe-wan2-1, thread steppe-wan2-1-latent-upscaler-release, 2 dated events 2026-11-22 → 2026-11-22.
- **Practical note:** See the usage and practice sections above, with their limits.
- **Confidence:** high. The dated supersedes above say what is obsolete.
