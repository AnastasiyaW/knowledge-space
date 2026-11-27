---
title: "Foundation 1: foundation-1 — Foundation 1"
category: "projects"
date: 2026-09-11
tags: ["foundation-1", "project"]
aliases: ["Foundation 1: foundation-1"]
---

# Foundation 1: foundation-1 — Foundation 1

**Development line:** project:foundation-1 · thread foundation-1  
**Last event:** 2026-09-11 · 2 dated since 2026-09-11 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Foundation-1 is a music generation model family for producers who need structured samples, loops and instruments.

- Structured text-to-sample generation for loops and individual notes.
- Controls for BPM, musical key, and bar length.
- Pitch-consistent keybeds that keep timbre uniform across notes.
- Sampler export to DecentSampler or SFZ through RC Stable Audio Tools.

The original checkpoint is a 2.43 GB download, and the publisher recommends at least 8 GB VRAM. Use it for local sample and instrument workflows, not as a general full-song generator.

## Development line

- **2026-09-11 — Foundation-1 Release Announcement.** The release announced Foundation-1 as a generative model family for musicians. It separates instrument from timbre, runs in a Gradio interface, needs 7GB VRAM, and exports to DecentSampler and SFZ formats.
- **2026-09-11 — Foundation-1: AI Music Generation Model Family Released.** The release introduced Foundation-1 for musicians. The models separate instrument and timbre, analyze BPM, key, and structure through loops, and generate individual notes for samplers. They build full-range keybeds with consistent timbre and create three-layer instruments through prompt separation. The interface is a Gradio app based on RC Stable Audio Tools. Generation requires 7GB VRAM and takes 7-8 seconds per sample.
- **2026-09-11 — other reporting on this date.**
  - The repository identifies the original Foundation-1 checkpoint as based on stabilityai/stable-audio-open-1.0. It supports loop structures of 4 or 8 bars at listed BPM values from 100 to 150. Hardware guidance lists about 7 GB VRAM during generation, with at least 8 GB recommended. (undated) — <https://huggingface.co/RoyalCities/Foundation-1>
  - An independent report describes the initial release as a structured text-to-sample model rather than a full-song generator. It notes a 16-bit Foundation_1.safetensors checkpoint and recommends the RC Stable Audio Tools fork as its interface. Because that report is dated 2026-03-17, public evidence does not explain why this reviewed announcement is dated 2026-09-11. (2026-03-17) — <https://rits.shanghai.nyu.edu/ai/foundation-1-a-producer-focused-ai-model-for-structured-music-sample-generation/>

## What changed

The September release established Foundation-1 as a structured loop checkpoint. The model card now lists three versions. It keeps original Foundation-1 for loops, adds Foundation-1.2 Samples for loops and one-shots, and adds Foundation-1.2 Keybeds for pitch-consistent playable instruments. Public pages do not date those later checkpoint additions.

## How to use this

1. Download the Foundation-1 checkpoint and its model_config.json into one subfolder, then select that model in RC Stable Audio Tools.
  — <https://huggingface.co/RoyalCities/Foundation-1>
2. Run RC Stable Audio Tools locally on Python 3.10 with pinned dependencies, then start the Gradio interface with python run_gradio.py.
  — <https://github.com/RoyalCities/RC-stable-audio-tools>
3. Build a prompt with instrument type, timbre, musical behavior, FX, key, bars, and BPM. Always set bars and BPM so sample duration matches the loop structure.
  — <https://huggingface.co/RoyalCities/Foundation-1>
4. For a playable instrument, use the Keybed workflow to generate pitch-specific samples, then export the assembled keybed as DecentSampler or SFZ.
  — <https://huggingface.co/RoyalCities/Foundation-1>

## Best practices

- Use structured prompts instead of generic genre tags. Start with the instrument, add one to three timbre descriptors, then specify structure, key, bars, and BPM.
  — <https://huggingface.co/RoyalCities/Foundation-1>
- Keep generation length matched to your requested bars and BPM. Use RC Stable Audio Tools because it handles timing alignment automatically.
  — <https://huggingface.co/RoyalCities/Foundation-1>
- Pick the Samples checkpoint for loops and one-shots, and the Keybeds checkpoint for pitch consistency. Longer keybed training trades away some general loop quality to keep timbre consistent across notes.
  — <https://huggingface.co/RoyalCities/Foundation-1>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- An independent report dates the Foundation-1 release to 2026-03-17, while both reviewed announcements are dated 2026-09-11. Public evidence does not explain the difference between those dates.
- The model card lists Foundation-1.2 Samples and Foundation-1.2 Keybeds, but public sources give no release dates for them.
- No dated public practitioner discussions specific to Foundation-1 were found.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/RoyalCities/Foundation-1 | RoyalCities/Foundation-1 | 2026-11-25 |
| https://github.com/RoyalCities/RC-stable-audio-tools | RoyalCities/RC-stable-audio-tools | 2026-11-25 |
| https://rits.shanghai.nyu.edu/ai/foundation-1-a-producer-focused-ai-model-for-structured-music-sample-generation/ | Foundation-1: A Producer-Focused AI Model for Structured Music Sample Generation | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:foundation-1, thread foundation-1, 2 dated events 2026-09-11 → 2026-09-11.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
