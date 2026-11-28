---
title: "RD Flow 64: rd-flow-64-release — Rd Flow 64 Release"
category: "projects"
date: 2026-11-27
tags: ["project", "rd-flow-64", "rd-flow-64-release"]
aliases: ["RD Flow 64: rd-flow-64-release"]
---

# RD Flow 64: rd-flow-64-release — Rd Flow 64 Release

RD Flow 64 is a 271M-parameter text-to-image model from Retro Diffusion that draws 64x64 pixel art sprites for game developers.

**Development line:** project:rd-flow-64 · thread rd-flow-64-release  
**Last event:** 2026-11-27 · 2 dated since 2026-11-27 · **Researched:** 2026-11-28 · confidence: high

## What it is

RD Flow 64 is a 271-million-parameter text-to-image generator from Retro Diffusion, for game developers and pixel artists making retro game assets. Latent diffusion systems such as Stable Diffusion decode compressed latents through a VAE. RD Flow 64 works directly on a native 64x64 pixel grid instead.

Abilities:

- Sprites: draws 64x64 pixel art directly, without VAE downscaling artifacts or color blurring.
- Palettes: indexes pixels to explicit color palettes, so contours stay clean and color boundaries stay discrete.
- Backgrounds: outputs transparent or solid backgrounds that can go straight into an engine.
- Text prompts: conditions generation through a frozen Qwen3-VL-4B vision-language model.
- Local use: runs in ComfyUI through nodes, with open weights.

The model file is about 542 megabytes and runs on consumer GPUs with 2 gigabytes of VRAM. Resolution is fixed at 64x64. For low-resolution 2D game production it gives clean sprites where latent diffusion models blur the transitions.

## Development line

- **2026-11-27 — Retro Diffusion Releases RD Flow 64 Pixel Art Model.** Retro Diffusion released RD Flow 64, a 271M-parameter pixel art generator. It produces 64x64 sprites natively, with no VAE and no upscaling, and ships with a frozen Qwen3-VL-4B model for text conditioning.
- **2026-11-27 — Retro Diffusion Releases RD Flow 64 Pixel Art Model.** Retro Diffusion announced RD Flow 64, a 271M-parameter pixel-art generator. It produces native 64x64 sprites with transparent or paletted backgrounds, without a VAE or an upscaler.
- **2026-11-27 — other reporting on this date.**
  - The technical report says the 271M-parameter model (542 MB file) draws images directly on a 64x64 pixel grid. It pairs with a frozen Qwen3-VL-4B vision-language text encoder, so there are no latent VAE decoding artifacts. (2026-11-27) — <https://retrodiffusion.ai/blog/rd-flow-64-technical-report>
  - The product documentation confirms palette-indexed color generation that matches retro hardware specifications (including PICO-8 and Game Boy) and native alpha transparency. It also lists official ComfyUI node workflows that run on GPUs with 2 GB VRAM. (2026-11-27) — <https://retrodiffusion.ai/rd-flow>

## What changed

Retro Diffusion moved pixel art generation from latent diffusion plus post-processing to direct grid synthesis. RD Flow 64 draws the 64x64 grid directly and indexes palettes, instead of decoding latents through a VAE. The flow network is paired with a frozen Qwen3-VL-4B text encoder. Support also grew from online web generation to standalone open weights and ComfyUI node integration.

## How to use this

1. Open the RD Flow 64 model or the hosted web demo on Retro Diffusion.
  — <https://retrodiffusion.ai/rd-flow>
2. Pick a target palette or a transparency setting, and write the prompt for the 64x64 grid.
  — <https://retrodiffusion.ai/blog/rd-flow-64-technical-report>
3. Load the open weights into a local ComfyUI workflow with the official node pack.
  — <https://retrodiffusion.ai/rd-flow>

## Best practices

- Generate with palette indexing, so colors do not bleed and pixel boundaries stay discrete for game engines.
  — <https://retrodiffusion.ai/blog/rd-flow-64-technical-report>
- Prompt for single 64x64 sprite subjects such as character icons, items or equipment, not complex scenes.
  — <https://retrodiffusion.ai/rd-flow>

## Superseded by this

- Pixel art used to mean downscaling high-resolution latent diffusion outputs and then applying post-hoc palette quantizers.
  — <https://retrodiffusion.ai/blog/rd-flow-64-technical-report>

## Still unknown

- Commercial licensing terms for third-party fine-tunes are not verified in public documentation.
- Community discussion threads from Reddit and the ComfyUI wiki came back only as search-engine redirect links. No direct, non-redirected URL could be verified, so community views are left out.

## Sources

| source | title | read |
|---|---|---|
| https://retrodiffusion.ai/blog/rd-flow-64-technical-report | RD Flow 64 Technical Report | 2026-11-28 |
| https://retrodiffusion.ai/rd-flow | RD Flow - Retro Diffusion | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:rd-flow-64, thread rd-flow-64-release, 2 dated events 2026-11-27 → 2026-11-27.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
