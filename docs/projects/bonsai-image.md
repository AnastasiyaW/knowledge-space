---
title: Bonsai Image 4B — Bonsai Image development
category: projects
date: 2026-05-29
tags: [bonsai-image, project]
aliases: ["Bonsai Image 4B"]
---

# Bonsai Image 4B — Bonsai Image development

**Development line:** `project:bonsai-image` · thread `bonsai-image`  
**Last event:** 2026-05-29 · 1 dated since 2026-05-29 · **Researched:** 2026-09-05 · confidence: high

## What it is

Bonsai Image 4B is a family of text-to-image diffusion models for local devices.
Binary 1-bit gives the smallest size, and Ternary gives better quality.
The WebGPU version remains experimental.

- Binary 1-bit, smallest size.
- Ternary, better image quality.
- WebGPU variant, experimental browser execution.

The ternary transformer takes 1,21 GB, and the full Apple Silicon payload takes 3,88 GB.
Start with the ternary low-bit pack for local generation instead of FP16.

## Development line

- **2026-05-29 — Bonsai Image 4B appeared on Hugging Face.** A dated record linked to the Hugging Face collection and WebGPU Space for the project. The links identify public project resources for evaluation. The links alone do not establish a model release, update, or benchmark on that date.

## What changed

2026-05-26 — PrismML released Bonsai Image 4B in Binary 1-bit and Ternary variants.
2026-05-29 — Links to the weight collection and WebGPU demo showed model availability. The initial release specifies the FLUX.2 Klein 4B base, 0,93 GB for Binary, 1,21 GB for the Ternary diffusion transformer, and local paths for Apple Silicon and CUDA.
2026-06-01 — Platform low-bit packs and unpacked FP16 variants arrived in the collection. FP16 exists for standard Diffusers compatibility, not for memory savings or speed.

## How to use this

From 2026-05-29, practitioners can use the linked Hugging Face collection and WebGPU Space to find and evaluate Bonsai Image 4B. Release status, capabilities, or usage guidance require more than these links alone.

1. Clone Bonsai Image Demo and run the setup for your platform: MLX on macOS, or gemlite/HQQ on Linux or Windows.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
2. Download the Ternary variant by default; pick Binary when minimum size matters more than quality.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
3. Run the studio via scripts/serve, or send requests to the running backend via send_request to avoid a cold start on every image.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
4. Open the WebGPU demo for experimental browser generation, load the Ternary model, and set the prompt and parameters; the page requests a Hugging Face access token.
  — <https://huggingface.co/spaces/webml-community/bonsai-image-webgpu>

## Best practices

- Use Ternary as the default choice: the official demo recommends it for better quality with moderate size growth.
  — <https://github.com/PrismML-Eng/Bonsai-image-demo>
- Do not choose unpacked FP16 safetensors for local efficiency: they serve as a fallback for stock Diffusers and lose low-bit pack benefits.
  — <https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked>
- Treat browser demo compatibility as unverified outside Apple M4 Max and M5 Max; Chrome/Edge offers the unsafe WebGPU flag for performance only.
  — <https://webml-community-bonsai-image-webgpu.static.hf.space/index.html>

## Superseded by this

- 2026-06-01 — The recommendation to use unpacked FP16 as the primary path is obsolete: official cards recommend optimized MLX or gemlite low-bit packs.

## Still unknown

- The initial release is dated 2026-05-26, while the recorded step is 2026-05-29; checked sources do not confirm the exact creation date of the collection and WebGPU Space.
- Required fields event_findings and new_events are absent in the provided output schema; what_changed reflects the clarified event and the earlier release.

## Sources

| source | title | read |
|---|---|---|
| https://prismml.com/news/bonsai-image-4b | Introducing 1-bit and Ternary Bonsai Image 4B: Image Generation for Local Devices | 2026-09-05 |
| https://huggingface.co/collections/prism-ml/bonsai-image | Bonsai Image - a prism-ml Collection | 2026-09-05 |
| https://huggingface.co/spaces/webml-community/bonsai-image-webgpu | Bonsai Image WebGPU - a Hugging Face Space by webml-community | 2026-09-05 |
| https://webml-community-bonsai-image-webgpu.static.hf.space/index.html | Bonsai image generation WebGPU demo | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-mlx-2bit | prism-ml/bonsai-image-ternary-4B-mlx-2bit | 2026-09-05 |
| https://huggingface.co/prism-ml/bonsai-image-ternary-4B-unpacked | Bonsai Image Ternary 4B — Unpacked FP16 Safetensors | 2026-09-05 |
| https://github.com/PrismML-Eng/Bonsai-image-demo | PrismML-Eng/Bonsai-Image-Demo | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:bonsai-image`, thread `bonsai-image`, 1 dated events 2026-05-29 → 2026-05-29.
- **Practical note:** From 2026-05-29, practitioners can use the linked Hugging Face collection and WebGPU Space as starting points for locating and evaluating Bonsai Image 4B; they should not infer release status, capabilities, or usage guidance from these links alone.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
