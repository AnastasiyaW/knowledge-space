---
title: DEMON
category: projects
date: 2026-06-03
tags: [demon, project]
aliases: ["DEMON"]
---

# DEMON

**Development line:** `project:demon` · thread `demon`  
**Last event:** 2026-06-03 · 1 dated since 2026-06-03 · **Researched:** 2026-09-06 · confidence: medium

## What it is

DEMON turns ACE-Step v1.5 into a live music generator and transformer on GPU. It is an audio counterpart to StreamDiffusion for performers, creative-tool developers, and researchers.

- Ring-buffer diffusion streams finished audio while source audio, prompts, LoRAs, and curves change during playback.
- The web interface exposes prompt blending, timbre and structure references, automation, MIDI mapping, recording, and a Session API.

## Development line

- **2026-06-03 — DEMON public resource set documented.** The core project had no GitHub Releases record. The separately versioned demonTD TouchDesigner client released v0.2.11 and v0.2.12 for hosted-session and socket-protocol fixes.

## What changed

- 2026-04-22: DreamVAE was published as a standalone ACE-Step decoder asset.
- 2026-05-27: the DEMON paper published the ring-buffer and TensorRT runtime with RTX 5090 measurements.
- 2026-06-02: DreamVAE was positioned as part of DEMON research while remaining a decoder-only asset.
- 2026-06-03: the core project had no GitHub Releases record; the separately versioned demonTD TouchDesigner client released v0.2.11 and v0.2.12 for hosted-session and socket-protocol fixes.
- 2026-06-04: demonTD v0.2.13 added an audio-output-device picker.
- 2026-06-09: demonTD v0.2.15 added automatic LoRA-trigger handling and prompt-B wiring. demonTD v0.2.16 moved pacing work off the UI thread to address choppy audio.
- 2026-06-11: demonTD v0.2.17 consolidated connection and audio-bleed fixes and documented bundle installation.

## How to use this

1. For a no-install trial, open the hosted instance at music.daydream.live; it is the stated path for users without a local GPU.
  — <https://huggingface.co/daydreamlive/DEMON>
2. For a local web workflow, use an NVIDIA GPU, uv, and about 40 GB free disk. Clone daydreamlive/DEMON, run `uv sync`, and run `uv run demon-setup` to obtain supported ACE-Step v1.5 assets and build minimal TensorRT engines.
  — <https://github.com/daydreamlive/DEMON>
3. Launch `uv run python -u -m demos.realtime_motion_graph_web.run` and open http://localhost:6660. If setup skipped engines, use `-- --accel compile` rather than the default all-TensorRT launch.
  — <https://github.com/daydreamlive/DEMON>
4. Load source audio, prompts, and optional references in the web interface. Use prompt blending, strength, LoRAs, curves, MIDI, or recording according to the performance goal.
  — <https://huggingface.co/daydreamlive/DEMON>
5. Add compatible optional LoRAs as .safetensors files under $ACESTEP_MODELS_DIR/loras/ (default ~/.daydream-scope/models/demon/loras/) and adjust their strength in the live session.
  — <https://huggingface.co/daydreamlive/DEMON>

## Best practices

- Keep the supplied ACE-Step v1.5 checkpoints and DEMON setup together; do not substitute arbitrary checkpoints or paths for a TensorRT configuration that expects the pinned model layout.
  — <https://github.com/daydreamlive/DEMON>
- Start with the TensorRT windowed VAE decoder plus a compiled decoder to avoid a full engine build; it is the documented low-cost route to streaming decode.
  — <https://huggingface.co/daydreamlive/DEMON>
- Rebuild TensorRT plans after changing GPU, CUDA, driver, or TensorRT version, because plans are hardware- and version-specific.
  — <https://github.com/daydreamlive/DEMON>
- Treat prompt, source, and scalar-denoise changes as ring-buffered controls: make changes deliberately and judge audio after propagation rather than expecting every control to be audible in the same tick.
  — <https://daydreamlive.github.io/DEMON/>
- If using DreamVAE separately, pair its decoder with the stock ACE-Step encoder; only the decoder is distilled.
  — <https://huggingface.co/daydreamlive/DreamVAE>
- For the TouchDesigner integration, install the release ZIP with demonTD.tox beside its vendor directory; the bare .tox is only for an installation that already has matching dependencies.
  — <https://github.com/daydreamlive/demonTD>

## Superseded by this

- 2026-06-04: For demonTD, instructions to use Edit -> Preferences -> Audio -> Audio Device -> None are obsolete. demonTD v0.2.13 says that setting does not exist and provides an audio-output-device picker. Source: https://github.com/daydreamlive/demonTD/releases
- 2026-06-09: For demonTD, treating a selected LoRA as automatically effective without its trigger word is obsolete. demonTD v0.2.15 prepends stored primary triggers and re-sends the prompt when the LoRA changes. Source: https://github.com/daydreamlive/demonTD/releases

## Still unknown

- No official core-engine GitHub Release identifies 2026-06-03 as a versioned DEMON release. We should not treat that date as a core-model or core-runtime release date.
- The Civitai URL https://civitai.com/models/2416425/acestep-loras did not provide a verifiable model card during research. Exact files, versions, dates, triggers, and compatibility with DEMON remain unverified; treat those LoRAs as optional external assets rather than a default dependency.
- The published core-code license is AGPL-3.0-or-later, while the Hugging Face DEMON card and project page display MIT. The sources do not reconcile that difference; confirm the applicable distribution license before modification, network deployment, or redistribution.
- The Daydream project page calls the XL Turbo base 5B, while the upstream ACE-Step repository calls its XL DiT 4B. The sources do not explain the parameter-count difference.
- Performance figures are author-reported RTX 5090 measurements under stated 60-second, TensorRT, depth, and step settings. No independent cross-hardware benchmark or universal latency and VRAM floor was found.

## Sources

| source | title | read |
|---|---|---|
| https://daydreamlive.github.io/DEMON/ | DEMON: Diffusion Engine for Musical Orchestrated Noise | 2026-09-06 |
| https://music.daydream.live/ | Daydream Demo | 2026-09-06 |
| https://github.com/daydreamlive/DEMON | daydreamlive/DEMON | 2026-09-06 |
| https://github.com/daydreamlive/DEMON/releases | Releases · daydreamlive/DEMON | 2026-09-06 |
| https://huggingface.co/daydreamlive/DEMON | daydreamlive/DEMON model card | 2026-09-06 |
| https://arxiv.org/abs/2605.28657 | DEMON: Diffusion Engine for Musical Orchestrated Noise | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE | daydreamlive/DreamVAE model card | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE/commit/53e74f7ed07cd053680fc2aa2b072124c63528d0 | DreamVAE initial release | 2026-09-06 |
| https://huggingface.co/daydreamlive/DreamVAE/commit/abb4c6d9913df0aedd685fed2e2f5aef3d742707 | DreamVAE: add links to paper, project page, and code repository | 2026-09-06 |
| https://github.com/daydreamlive/demonTD | daydreamlive/demonTD | 2026-09-06 |
| https://github.com/daydreamlive/demonTD/releases | Releases · daydreamlive/demonTD | 2026-09-06 |
| https://huggingface.co/ACE-Step/Ace-Step1.5 | ACE-Step/Ace-Step1.5 model card | 2026-09-06 |
| https://github.com/ACE-Step/ACE-Step-1.5 | ACE-Step/ACE-Step-1.5 | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:demon`, thread `demon`, 1 dated events 2026-06-03 → 2026-06-03.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
