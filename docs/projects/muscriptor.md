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

MuScriptor is an open-weight music transcription model from Mirelo and Kyutai for turning multi-instrument recordings into MIDI note events.

It offers small (100M), medium (300M) and large (1.3B) checkpoints. It runs through a Python API, a CLI and local HTTP serving. The model processes 16 kHz mono audio in 5-second chunks. It emits pitch, onset, offset and 36-group instrument labels, but not velocity. The weights are gated under CC-BY-NC.

## Development line

- **2026-07-22 — MuScriptor public project resources were available.** On 2026-07-22, a dated MuScriptor item linked the project website, source repository, model page, interactive demo, and installation resources. Together, those links establish a public project-access milestone by that date. They do not, on their own, establish a specific release version, model capability, or technical change.

## What changed

- 2026-07-22 — The supplied project links match the public MuScriptor ecosystem. The preceding v0.2.2 release (2026-07-21) added strict instrument-constrained decoding, direct MIDI HTTP output, Apple Silicon FP16/MPS support, optimized decoding kernels and Windows GPU instructions.
- 2026-07-21 — GitHub v0.2.2 expanded the runnable package and demo/service workflow.
- 2026-07-10 — v0.2.1 added serving without building; Kyutai published the project announcement.
- 2026-07-09 — The paper introduced the open-weight multi-instrument model, trained with synthetic pre-training, real-audio fine-tuning and RL post-training.
- 2026-06-30 — The public checkpoint collection was created; this is repository metadata, not a training date.

## How to use this

From 2026-07-22, we can evaluate MuScriptor through its public code, model, demo, and installation entry points. Confirm exact capabilities and versions from the linked primary resources before adoption.

1. Install from the Git repository; PyPI installation remains listed as forthcoming.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
2. Choose small, medium or large, then run `muscriptor transcribe --model large audio.wav -o out.mid` or call `TranscriptionModel.load_model()` and `transcribe_to_midi()` from Python.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
3. For an interactive trial, upload audio to the hosted transcription Space; for local integration, use the repository CLI/server implementation.
  — <https://huggingface.co/spaces/hugging-apps/muscriptor-music-transcription>

## Best practices

- Use instrument conditioning when the track’s instrument groups are known; the model card notes it improves scores and keeps assignments coherent across chunks.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Treat output as an editable MIDI draft, not a hand-annotated score, especially for dense, unusual or heavily processed mixes.
  — <https://huggingface.co/MuScriptor/muscriptor-large>
- Use only recordings for which you have the necessary rights; the model card prohibits unauthorized transcription.
  — <https://huggingface.co/MuScriptor/muscriptor-large>

## Superseded by this

- 2026-07-21 — v0.2.2 supersedes v0.2.1 for users needing direct MIDI HTTP responses, strict instrument constraints or native Apple Silicon FP16 inference.
- 2026-07-10 — v0.2.1 superseded v0.2.0 for serving without a build step.

## Still unknown

- The supplied 2026-07-22 event does not identify which linked surface was the contemporaneous change. GitHub records v0.2.2 on 2026-07-21, so its scope is reported as the closest dated first-party addition rather than asserted as a 2026-07-22 release.
- The response schema supplied for this task has no `event_findings` or `new_events` fields. Their date-bound findings are retained in `what_changed`; no separate structured entries can be emitted without violating the schema.
- The official hosted demo page was reachable but did not expose operational documentation in its rendered text.

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
