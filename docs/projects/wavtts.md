---
title: WavTTS
category: projects
date: 2026-06-08
tags: [project, wavtts, wavtts-development]
aliases: ["WavTTS"]
---

# WavTTS

**Development line:** `project:wavtts` · thread `wavtts-development`  
**Last event:** 2026-06-08 · 1 dated since 2026-06-08 · **Researched:** 2026-09-05 · confidence: high

## What it is

WavTTS is an open-source zero-shot text-to-speech system that conditions on a short reference recording and its transcript.

- Direct raw-waveform generation.
- CLI and script inference.
- 16 kHz official checkpoint.
- Training and evaluation code.

The released weights are CC BY-NC 4.0, and the model is not served by a Hugging Face Inference Provider. Use it for local non-commercial voice-conditioned synthesis, not as a drop-in hosted production API.

## Development line

- **2026-06-08 — WavTTS public project resources were recorded.** On 2026-06-08, public links appeared for the WavTTS project website, source repository, model page, demo, and ComfyUI integration. They provide a dated reference point to locate the project and related tooling. The evidence does not show what release or code change accompanied the links.

## What changed

2026-06-08 — WavTTS appeared with its project page, official code, 16 kHz checkpoint, web demo, and a community ComfyUI integration. The official release was dated 2026-06-03.

## How to use this

As of 2026-06-08, use the WavTTS project, source, model, demo, and ComfyUI links as the starting point to evaluate or integrate the project. This line alone establishes no specific release behavior.

1. Clone the official repository, create a Python 3.10 Conda environment, install CUDA-compatible PyTorch, then install WavTTS in editable mode.
  — <https://github.com/cwx-worst-one/WavTTS>
2. Run `wavtts_infer-cli` with `--model WavTTS`, a reference WAV, that recording’s transcript, and the text to synthesize. The default configuration downloads the official checkpoint automatically.
  — <https://huggingface.co/worstchan/WavTTS>
3. For ComfyUI, install the community node through ComfyUI Manager or into `custom_nodes`, restart ComfyUI, then connect a reference-audio input, required reference transcript, model loader, and generator node.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>

## Best practices

- Use the supplied Conda and Python 3.10 setup with a CUDA-supported PyTorch build. The upstream repository recommends Conda for dependency management.
  — <https://github.com/cwx-worst-one/WavTTS>
- Supply an accurate transcript with the reference recording. The ComfyUI integration treats `reference_text` as required and recommends a clean 5–12 second voice prompt.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>
- For the community ComfyUI integration, prefer FP32 for reliability or its mixed-BF16 preset for lower VRAM. Avoid FP16 presets, because the maintainer reports they can yield non-finite samples.
  — <https://github.com/Saganaki22/WavTTS-ComfyUI>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The Hugging Face Space linked on 2026-06-08 returned an internal error during review, so its current availability and exact interface are unverified.
- The ComfyUI integration is a separate community repository, not an official WavTTS release.

## Sources

| source | title | read |
|---|---|---|
| https://wavtts.github.io/ | WavTTS project page | 2026-09-05 |
| https://github.com/cwx-worst-one/WavTTS | WavTTS official GitHub repository | 2026-09-05 |
| https://huggingface.co/worstchan/WavTTS | worstchan/WavTTS official model card | 2026-09-05 |
| https://github.com/Saganaki22/WavTTS-ComfyUI | WavTTS-ComfyUI community integration | 2026-09-05 |
| https://arxiv.org/abs/2606.03455 | WavTTS: Towards High-Quality Zero-Shot TTS via Direct Raw Waveform Modeling | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:wavtts`, thread `wavtts-development`, 1 dated events 2026-06-08 → 2026-06-08.
- **Practical note:** As of 2026-06-08, use the recorded WavTTS project, source, model, demo, and ComfyUI links as the dated starting point to evaluate or integrate the project. This line alone establishes no specific release behavior.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.