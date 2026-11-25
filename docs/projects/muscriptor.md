---
title: MuScriptor — Public project availability
category: projects
date: 2026-07-22
tags: [muscriptor, project, public-project-availability]
aliases: ["MuScriptor"]
---

# MuScriptor — Public project availability

**Development line:** `project:muscriptor` · thread `public-project-availability`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-05 · confidence: high

## What it is

MuScriptor is an open-weight music transcription model from Mirelo and Kyutai. It turns multi-instrument recordings into MIDI note events.

- Checkpoints: small (100M), medium (300M) and large (1.3B) parameter models.
- Runtime: Python API, CLI and local HTTP serving.
- Input: 16 kHz mono audio in 5-second chunks.
- Output: pitch, onset, offset and 36-group instrument labels.

Weights are CC-BY-NC and gated; predictions do not include velocity.

## Development line

- **2026-07-22 — MuScriptor public project resources were available.** On 2026-07-22, public links opened for the project site, repository, model page, interactive demo and installation. These links confirm project availability on that date. They do not fix a specific release version, model capability or technical change.

## What changed

- 2026-07-22 — Project links opened the public MuScriptor ecosystem. The preceding v0.2.2 release on 2026-07-21 added strict instrument-constrained decoding, direct MIDI HTTP output, Apple Silicon FP16/MPS support, optimized decoding kernels and Windows GPU instructions.
- 2026-07-21 — GitHub v0.2.2 expanded the runnable package alongside demo and service workflows.
- 2026-07-10 — Release v0.2.1 enabled serving without building. Kyutai published the project announcement.
- 2026-07-09 — The paper introduced the open-weight multi-instrument model. Training combined synthetic pre-training, real-audio fine-tuning and RL post-training.
- 2026-06-30 — Public checkpoint collection created. This marks repository metadata, not a training date.

## How to use this

We can evaluate MuScriptor through its public code, model, demo and installation entry points since 2026-07-22. Confirm exact capabilities and versions from primary sources before adoption.

1. Install from the Git repository; PyPI installation remains listed as forthcoming.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
2. Choose small, medium or large. Run `muscriptor transcribe --model large audio.wav -o out.mid` or call `TranscriptionModel.load_model()` and `transcribe_to_midi()` from Python.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
3. Upload audio to the hosted transcription Space for an interactive trial. For local integration, use the repository CLI or server implementation.
  — <https://huggingface.co/spaces/hugging-apps/muscriptor-music-transcription>

## Best practices

- Use instrument conditioning when track instrument groups are known. The model card notes that conditioning improves scores and keeps assignments coherent across chunks.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Treat output as an editable MIDI draft rather than a finished score, especially on dense, unusual or heavily processed audio.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Use only recordings with confirmed rights. The model card explicitly prohibits unauthorized transcription.
  — <https://huggingface.co/MuScriptor/muscriptor-large>

## Superseded by this

- 2026-07-21 — v0.2.2 supersedes v0.2.1 for users needing direct MIDI HTTP responses, strict instrument constraints or native Apple Silicon FP16 inference.
- 2026-07-10 — v0.2.1 superseded v0.2.0 for serving without a build step.

## Still unknown

- The 2026-07-22 event does not identify which linked surface changed that day. GitHub dates v0.2.2 to 2026-07-21, so that update is reported as the nearest first-party addition rather than a 2026-07-22 release.
- The schema supplies no separate fields for `event_findings` or `new_events`, so dated findings remain under `what_changed`.
- The hosted demo was reachable, but its rendered page text showed no operational documentation.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/MuScriptor/muscriptor-large | MuScriptor — large (≈1.3B) model card | 2026-09-05 |
| https://github.com/muscriptor/muscriptor/releases | MuScriptor GitHub releases | 2026-09-05 |
| https://arxiv.org/abs/2607.08168 | MuScriptor: An Open Model for Multi-Instrument Music Transcription | 2026-09-05 |
| https://kyutai.org/blog/2026-07-10-muscriptor/ | MuScriptor: Automatic Multi-instrument Transcription | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/muscriptor-music-transcription | MuScriptor Music Transcription Space | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:muscriptor`, thread `public-project-availability`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** From 2026-07-22, practitioners could evaluate MuScriptor through its public code, model, demo, and installation entry points; confirm exact capabilities and versions from the linked primary resources before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
