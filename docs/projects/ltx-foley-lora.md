---
title: LTX-2.3-Foley-LoRA — LTX Video
category: projects
date: 2026-07-01
tags: [ltx-foley-lora, ltx-video, ltx_video, project]
aliases: ["LTX-2.3-Foley-LoRA"]
---

# LTX-2.3-Foley-LoRA — LTX Video

**Development line:** `project:ltx-foley-lora` · thread `ltx-video`  
**Last event:** 2026-07-01 · 1 dated since 2026-07-01 · **Researched:** 2026-09-05 · confidence: medium

## What it is

LTX-2.3-Foley-LoRA is a 400-step video-to-audio LoRA for LTX-2.3 base or distilled models. It takes a silent video and an action prompt to generate synchronised, non-speech Foley. It is not a general music or dialogue model. Use a LoRA multiplier of 1–3. It fixes LTX-2.3 generations that add background score, but speech behaviour remains insufficiently documented.

## Development line

- **2026-07-01 — LTX-2.3-Foley-LoRA model page was recorded.** On 2026-07-01, FuzzPuppy published the Hugging Face model page for LTX-2.3-Foley-LoRA. The page provides the Foley LoRA artifact, but does not detail its capabilities, provenance, compatibility, or release details.

## What changed

- 2026-07-01 — LTX-2.3-Foley-LoRA was released as a 400-step adapter to suppress music overlays and generate visually matched sound effects. Its author trained it without speech examples and did not test speech.
- 2026-07-04 — The companion ComfyUI repository added a long-video sliding-window workflow with overlap and audio stitching, extending the original short-clip workflow.

## How to use this

From 2026-07-01, evaluate and verify LTX-2.3-Foley-LoRA on Hugging Face before relying on it in production; this line alone does not support operational claims.

1. Download `ltx-2.3-foley-400-steps.safetensors`, load it with an LTX-2.3 base or distilled video-to-audio model, and start at LoRA strength 1.0.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
2. For ComfyUI, install the official LTXVideo nodes and the workflow repository's `ltx_foley_v2a` helper nodes; put the LoRA in `ComfyUI/models/loras`.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>
3. Use the short workflow for a quick clip; use `foley-sliding-window.json` for longer video so windows are overlapped and stitched.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>

## Best practices

- Describe only the visible action, then add “No speech is present. No music is present”; use an anti-music negative prompt.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
- Increase LoRA strength from 1 toward 2 or 3 only if score remains in the output.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
- Start ComfyUI with `--cache-classic` for the sliding-window workflow to avoid large LTX node outputs being evicted and recomputed between windows.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>

## Superseded by this

- 2026-07-04 — Treating the original short-clip workflow as the only supported route is obsolete for long videos; use the sliding-window workflow instead.

## Still unknown

- The model card does not document training data, evaluation metrics, exact VRAM requirements, or reliable dialogue preservation.
- The 2026-07-04 workflow update appears in repository history and long-video documentation, but lacks an immutable release note.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA | FuzzPuppy/LTX-2.3-Foley-LoRA | 2026-09-05 |
| https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow | FuzzPuppy/LTX-2.3-Foley-Workflow | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1uk60hg/ltx23_foley_lora_for_synced_sound_effects_without/ | LTX-2.3 Foley LoRA for synced sound effects without unwanted music | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ltx-foley-lora`, thread `ltx-video`, 1 dated events 2026-07-01 → 2026-07-01.
- **Practical note:** From 2026-07-01, practitioners should treat LTX-2.3-Foley-LoRA as a separately linked Hugging Face Foley-LoRA artifact to evaluate and verify before relying on it; this line alone does not support operational claims.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
