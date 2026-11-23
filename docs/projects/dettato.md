---
title: "Dettato: dettato-audio-to-midi-model — Dettato Audio To Midi Model"
category: "projects"
date: 2026-11-22
tags: ["dettato", "dettato-audio-to-midi-model", "project"]
aliases: ["Dettato: dettato-audio-to-midi-model"]
---

# Dettato: dettato-audio-to-midi-model — Dettato Audio To Midi Model

Dettato is an open-source multi-instrument audio-to-MIDI transcription pipeline for music producers and developers.

**Development line:** project:dettato · thread dettato-audio-to-midi-model  
**Last event:** 2026-11-22 · 1 dated since 2026-11-22 · **Researched:** 2026-11-23 · confidence: medium

## What it is

Dettato is an open-source multi-instrument audio-to-MIDI transcription pipeline for music producers, software developers, and transcription researchers. It does the following:

- Transcribes mixed polyphonic audio into MIDI note events
- Separates tracks, grouping notes by instrument
- Generates a dedicated drum track
- Writes structured JSON with detailed note parameters
- Runs from the command line on GPU or CPU, as configured
- Downloads model weights from the Hugging Face Hub automatically

The pipeline is four models with 28.1 million parameters in total. They are trained on non-commercial and synthetic data, not on commercial master recordings. It is a light Apache-2.0 alternative to heavy monolithic transcription models for local audio-to-MIDI work.

## Development line

- **2026-11-22 — Dettato open model releases MIDI and stem separation tool.** An open-source neural model named dettato was released. It analyzes audio recordings, transcribes notes to MIDI, separates parts by instrument and processes drums separately. Reported speed is 15 seconds for a four-minute track on an RTX 5060. Code and weights are free.
  - The release is a modular chain of four sub-models totaling 28.1M parameters: Transcriber at ~15.3M, Evidence Repairer at ~4.9M, Grouper at ~2.9M and Drum Model at ~5.0M. It is licensed under Apache-2.0. It outputs multi-track MIDI and JSON note metadata, and fetches weights from the Hugging Face Hub automatically. Training data is limited to synthetic mixes and Creative Commons solo recordings, with no copyrighted commercial music. (2026-11-22) — <https://github.com/kobimusic/dettato>

## What changed

KobiMusic released the project as open source. It is a modular four-stage chain: note transcription, evidence repair, instrument grouping and dedicated drum handling, under an Apache-2.0 license.

## How to use this

1. Install the package and CLI tool from GitHub with pip: pip install git\+https://github.com/kobimusic/dettato.
  — <https://github.com/kobimusic/dettato>
2. Run dettato \<input\_file\> -o \<output\_directory\> on an audio file. It writes separated multi-track MIDI and JSON descriptor files.
  — <https://github.com/kobimusic/dettato>
3. Pick the hardware with the --device flag, for example --device cpu on a machine without an accelerator.
  — <https://github.com/kobimusic/dettato>

## Best practices

- Use the GPU for long polyphonic audio or batches of songs, which gives near real-time speed. Keep CPU mode for light evaluation.
  — <https://github.com/kobimusic/dettato>
- Read the JSON metadata next to the MIDI tracks. It shows note confidence scores, timing bounds and instrument grouping, so you can check the result.
  — <https://github.com/kobimusic/dettato>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Independent accuracy benchmarks against commercial audio-to-MIDI transcription tools are not widely published yet, since the release is recent.
- Training hours, loss curves and architectural hyperparameters beyond the sub-model parameter counts are not documented publicly.
- Chinese-language searches returned only domain-level aggregators, with no verifiable article paths. The zh-CN lane is a coverage gap.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/kobimusic/dettato | kobimusic/dettato: Multi-instrument audio-to-MIDI transcription | 2026-11-23 |

## Agent brief {#agent-brief}

- **Subject:** project:dettato, thread dettato-audio-to-midi-model, 1 dated events 2026-11-22 → 2026-11-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
