---
title: "LongCat"
category: "projects"
date: 2026-11-20
tags: ["longcat", "longcat-2-0", "longcat-avatar", "project"]
aliases: ["LongCat"]
---

# LongCat

**Development line:** project:longcat-avatar · thread longcat-2-0  
**Last event:** 2026-11-20 · 3 dated since 2026-06-30 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Longcat Avatar ComfyUI custom nodes are open-source packs that bring Meituan LongCat-Avatar, an audio-driven portrait animator, into ComfyUI graphs. They are an alternative to SadTalker or LivePortrait.

What the nodes do:

- Animate a character from a single image, zero-shot
- Sync lips to speech using Whisper audio embeddings
- Sample fast in eight steps through distilled model LoRA adapters
- Generate a single clip
- Auto-extend with a sliding window for long speech

The video diffusion backbone needs a lot of GPU VRAM. Precise audio alignment needs clean speech without background noise. For local workflows these packs give higher temporal stability than earlier audio-driven portrait tools.

## Development line

- **2026-06-30 — LongCat made LongCat 2.0 publicly discoverable.** On 2026-06-30, LongCat linked a versioned LongCat 2.0 page next to its source repository and model-hosting page. The links point to a substantive development step. The version became discoverable in documentation, code and model distribution.
- **2026-11-20 — Custom ComfyUI packs for LongCat-Avatar 1.6 released.** A post reports that custom ComfyUI node packs for LongCat-Avatar 1.6 are available. It links two GitHub repositories, PixelAILabs and PedroMarinhoDev, that implement the integration.
- **2026-11-20 — Custom ComfyUI packs for LongCat-Avatar 1.6 released.** Community packs for LongCat-Avatar 1.6 were announced. Two linked GitHub repositories cover audio-driven character animation and lip-sync video generation.
- **2026-11-20 — other reporting on this date.**
  - The PixelAILabs repository has custom node workflows for LongCat-Avatar 1.6. They cover Whisper-Large audio feature extraction, distilled 8-step inference schedules, and auto-extend windowing for long speech. (2026-11-20) — <https://github.com/Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs>
  - The PedroMarinhoDev ComfyUI-LongCat-Avatar repository has node wrappers for portrait image conditioning, audio track input and frame generation parameters. They target Meituan LongCat-Avatar 1.6 model weights. (2026-11-20) — <https://github.com/PedroMarinhoDev/ComfyUI-LongCat-Avatar>

## What changed

Community developers moved the LongCat-Avatar video diffusion architecture into modular ComfyUI workflows. Execution shifted from monolithic inference scripts to dedicated node packs. The packs add three things:

- Whisper-based audio feature extraction, for better phonetic alignment
- Distilled low-step sampling schedules
- Windowed frame concatenation, for audio with several sentences

## How to use this

1. Clone or install the custom node repository into the ComfyUI/custom\_nodes directory, then install the Python dependencies.
  — <https://github.com/Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs>
2. Download the LongCat-Avatar model checkpoint weights and the Whisper audio encoder into the matching ComfyUI models folders.
  — <https://github.com/PedroMarinhoDev/ComfyUI-LongCat-Avatar>
3. Load the LongCat Avatar workflow graph. Connect one character portrait image and one speech audio file to the node inputs.
  — <https://github.com/Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs>
4. Run the generation queue. Use distilled 8-step sampling for fast rendering, or the auto-extend loop for longer audio.
  — <https://github.com/PedroMarinhoDev/ComfyUI-LongCat-Avatar>

## Best practices

- Use clean speech without noise and with clear pronunciation, so Whisper extracts features accurately and the mouth sync stays precise.
  — <https://github.com/Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs>
- Add positive text prompts that describe stable framing and clothing, so camera motion and posture do not drift across frames.
  — <https://github.com/PedroMarinhoDev/ComfyUI-LongCat-Avatar>
- For audio longer than one clip, use auto-extend windowing with overlapping frames, so the timing stays consistent and no seams show at the boundaries.
  — <https://github.com/Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs>

## Superseded by this

- Standalone monolithic Python inference scripts for LongCat-Avatar are superseded by native ComfyUI custom node graphs for modular workflow execution.
  — <https://github.com/Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs>

## Still unknown

- Two independent community repositories, Pixelailabs and PedroMarinhoDev, released ComfyUI custom nodes for LongCat-Avatar on the same date. They are parallel wrapper implementations, not one unified upstream package.
- Searches for Chinese documentation and forum threads (zh-CN) returned only redirect endpoints, not direct article URLs. No source is cited for that language, to avoid failed automated fetches.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs | Pixelailabs/ComfyUI-LongCat-Avatar-PixelAILabs | 2026-11-21 |
| https://github.com/PedroMarinhoDev/ComfyUI-LongCat-Avatar | PedroMarinhoDev/ComfyUI-LongCat-Avatar | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:longcat-avatar, thread longcat-2-0, 3 dated events 2026-06-30 → 2026-11-20.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
