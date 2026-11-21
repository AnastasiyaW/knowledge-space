---
title: Covo-Audio
category: projects
date: 2026-03-24
tags: [covo-audio, covo-audio-development, covo_audio, project]
aliases: ["Covo-Audio"]
---

# Covo-Audio

**Development line:** `project:covo-audio` · thread `covo-audio-development`  
**Last event:** 2026-03-24 · 1 dated since 2026-03-24 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Covo-Audio is Tencent's 7B-parameter end-to-end audio language model, which takes audio in and produces audio out; the released variant is Covo-Audio-Chat.

- Architecture: LLM initialized from Qwen2.5-7B; audio encoder initialized from Whisper-large-v3.
- Users: researchers and developers of spoken dialogue and speech understanding systems.
- Key capability: spoken dialogue, speech and audio understanding, and a full-duplex variant (Covo-Audio-Chat-FD).
- Limits: the model card says "for research and experimental purposes only"; no inference provider hosted it at capture; the paper abstract gives no benchmark numbers.

## Development line

- **2026-03-24 — Covo-Audio-Chat Hugging Face resource linked.** On 2026-03-24, we linked the Hugging Face resource tencent/Covo-Audio-Chat under the Covo-Audio development line. The dated link establishes an associated public resource, but not its capabilities, version, release status, or change details. It confirms only that resource association.

## What changed

- 2026-02-10 — technical report arXiv:2602.09823 submitted (v1); revised 2026-03-16 (v2).
- 2026-03-16 — tencent/Covo-Audio-Chat Hugging Face repository created and last modified on the same day (Hugging Face API). The stub link of 2026-03-24 is later than this creation date.
- The model card gives size as 7B in the text and 8B in the Hub metadata; the paper says 7B.

## How to use this

1. Read the technical report for architecture, training and the evaluation tables before adopting the model.
  — <https://arxiv.org/abs/2602.09823>
2. Download weights with `hf download tencent/Covo-Audio-Chat`; the card recommends Python 3.11 or later.
  — <https://huggingface.co/tencent/Covo-Audio-Chat>
3. Run inference from the GitHub repository's `example.sh` (with `example.py` and `requirements.txt`).
  — <https://github.com/Tencent/Covo-Audio>
4. Confirm the license in the repository's LICENSE file before any use: the Hub metadata has no license tag, and the card does not name the license.
  — <https://huggingface.co/api/models/tencent/Covo-Audio-Chat>
5. Verify any output against a trusted source; the card warns the model "may occasionally produce inaccurate, inappropriate, biased, outdated, or factually incorrect content".
  — <https://huggingface.co/tencent/Covo-Audio-Chat>

## Best practices

- Use the model for English and Chinese only; the card lists those as the languages it covers.
  — <https://huggingface.co/api/models/tencent/Covo-Audio-Chat>
- Keep use to research and evaluation, as the card's intended-use statement says.
  — <https://huggingface.co/tencent/Covo-Audio-Chat>

## Superseded by this

- Nothing marked obsolete. The paper describes Covo-Audio-Chat-FD as an updated full-duplex version; we did not establish which earlier variant it replaces.

## Still unknown

- License name: not stated on the model card or in the Hub metadata; the GitHub repository has a LICENSE file whose type was not read.
- Benchmark numbers: the abstract and card give only qualitative claims ("state-of-the-art or competitive performance among models of comparable scale"); the full tables were not read.
- Parameter count: 7B in the paper and card text, 8B in the Hub metadata.
- Paper affiliation: the arXiv page lists authors but no organization in the captured text; attribution beyond Tencent's repository is unconfirmed.
- Whether the stub's 2026-03-24 event matches a Tencent announcement is unknown.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/tencent/Covo-Audio-Chat | Covo-Audio-Chat model card | 2026-11-21 |
| https://huggingface.co/api/models/tencent/Covo-Audio-Chat | Hugging Face API: dates, tags, pipeline | 2026-11-21 |
| https://arxiv.org/abs/2602.09823 | Covo-Audio Technical Report (arXiv:2602.09823) | 2026-11-21 |
| https://github.com/Tencent/Covo-Audio | Covo-Audio GitHub repository | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:covo-audio`, thread `covo-audio-development`, 1 dated event 2026-03-24; technical report submitted 2026-02-10, model repository created 2026-03-16.
- **Practical note:** Research and evaluation use only; confirm the license file and check outputs against trusted sources before any adoption.
- **Confidence:** medium. Architecture and intended use come from the card and report; benchmark tables and license name are not verified. Dated supersedes above are the authority for what is obsolete.
