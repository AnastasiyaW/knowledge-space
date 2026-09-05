---
title: Stream.FM
category: projects
date: 2026-05-14
tags: [project, stream-fm, stream-fm-development, stream_fm]
aliases: ["Stream.FM"]
---

# Stream.FM

**Development line:** `project:stream-fm` · thread `stream-fm-development`  
**Last event:** 2026-05-14 · 1 dated since 2026-05-14 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Stream.FM is an AGPL-3.0 PyTorch research codebase for audio ML engineers building frame-by-frame speech restoration.

- Speech enhancement and dereverberation
- Codec post-filtering, bandwidth extension and STFT phase retrieval
- Mel vocoding through the bundled related MelFlow implementation

## Development line

- **2026-05-14 — Stream.FM project resources were linked.** On 2026-05-14, Stream.FM was linked through an examples site, a GitHub source repository, and a Google Drive folder. Together, these references establish a public project-resource bundle for the line, although they do not establish a versioned release or the contents of the supplementary materials.

## What changed

- 2025-09-18 — MelFlow, the related streaming Mel-vocoder work later bundled with Stream.FM, appeared as an arXiv preprint.
- 2025-12-22 — Stream.FM appeared as an arXiv preprint.
- 2026-04-21 — arXiv v3 became the latest listed Stream.FM paper revision.
- 2026-05-05 — the authors demonstrated joint real-time speech enhancement and bandwidth extension at ICASSP.
- 2026-05-11 — the initial public Stream.FM and MelFlow source code was committed.
- 2026-05-13 — AGPL-3.0 was added to the source repository.
- 2026-05-14 — the project page, repository and checkpoint-folder links were recorded together; no separate upstream commit or GitHub Release is evidenced for this date.
- 2026-05-23 — repository citation maintenance changed documentation only.
- 2026-06-05 — the last shown upstream push updated the Stream.FM TASL citation only.

## How to use this

Check the examples site, repository, and Drive materials together when evaluating Stream.FM as of 2026-05-14. No specific setup, result, or release version is verified yet.

1. Create a Python 3.10+ environment and install the documented requirements with a PyTorch CUDA wheel index matching the local CUDA runtime.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
2. Download a checkpoint from the documented Google Drive folder into a local checkpoints directory using the maintained gdown command.
  — <https://drive.google.com/drive/folders/1u2QKjGAdxblQVV8-qmifSM9AwhT86LER>
3. Choose the task configuration that matches the checkpoint architecture, then run inference.py with an input WAV directory, output directory, solver and checkpoint path.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
4. For live frame-by-frame integration, implement state initialization and forward_step calls around the CausalNCSNpp backbone rather than expecting a ready-made streaming server.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>

## Best practices

- Start with the authors' suggested 5xeuler solver, and only increase GPU parallelism when the target machine has those GPUs.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Keep the Hydra config and checkpoint architecture matched; the documented inference path requires this pairing.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- For streaming, evaluate CUDA graphs and the default torch.compile wrapper on the target hardware rather than assuming the paper latency transfers unchanged.
  — <https://github.com/sp-uhh/streamfm/blob/main/README.md>
- Benchmark end-to-end target-hardware latency; the published 48 ms result is a measured research setup, not a hardware-independent guarantee.
  — <https://arxiv.org/abs/2512.19442>
- Load only trusted checkpoints: inference uses torch.load with weights_only=False.
  — <https://raw.githubusercontent.com/sp-uhh/streamfm/main/inference.py>
- Review AGPL-3.0 obligations before incorporating repository code into a product or network service.
  — <https://github.com/sp-uhh/streamfm/blob/main/LICENSE>

## Superseded by this

- 2026-05-14 — Corrected: this is a date on which the links were recorded, not a separately evidenced upstream Stream.FM release; public source code began on 2026-05-11 and GitHub lists no releases.
- 2026-05-23 — Citation-only repository maintenance is not evidence of a new model, checkpoint or runtime release.
- 2026-06-05 — The TASL citation update is documentation-only; no later official model, dataset or package release was found in the checked sources.

## Still unknown

- The linked Drive folder could not be enumerated here, so its 2026-05-14 checkpoint inventory, hashes, availability and contents are unverified.
- AGPL-3.0 is verified for the repository source; no separate checkpoint licence or model card for the Drive-hosted weights was verified.
- The paper's latency results do not prove target-device, audio-I/O or production latency.
- No GitHub Release, package artifact or checkpoint-version manifest was found; adopters need to record the exact source commit and checkpoint identity they use.

## Sources

| source | title | read |
|---|---|---|
| https://sp-uhh.github.io/streamfm_examples/ | Stream.FM | Real-Time Streamable Generative Speech Restoration with Flow Matching | 2026-09-05 |
| https://github.com/sp-uhh/streamfm | sp-uhh/streamfm | 2026-09-05 |
| https://drive.google.com/drive/folders/1u2QKjGAdxblQVV8-qmifSM9AwhT86LER | Stream.FM checkpoint folder | 2026-09-05 |
| https://arxiv.org/abs/2512.19442 | Real-Time Streamable Generative Speech Restoration with Flow Matching — arXiv:2512.19442 | 2026-09-05 |
| https://arxiv.org/abs/2509.15085 | Real-Time Streaming Mel Vocoding with Generative Flow Matching — arXiv:2509.15085 | 2026-09-05 |
| https://cmsworkshops.com/ICASSP2026/view_demosession.php?mid=55 | ICASSP 2026 Show-and-Tell demo listing | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/17ec317c3974e1a4b0b4e3ebfe2a3a99fbbd616c | Initial Stream.FM & MelFlow public code — 17ec317 | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/c4b9c2b | sp-uhh/streamfm commit c4b9c2b | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/1a8226884432a17c7b71945a4b7d3c015dfe6cc8 | sp-uhh/streamfm commit 1a822688 | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/commit/ab2700c1154acc5c2ce67a5344182028336413f5 | sp-uhh/streamfm commit ab2700c | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/blob/main/README.md | README.md — sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/blob/main/LICENSE | LICENSE — sp-uhh/streamfm | 2026-09-05 |
| https://github.com/sp-uhh/streamfm/releases | Releases — sp-uhh/streamfm | 2026-09-05 |
| https://raw.githubusercontent.com/sp-uhh/streamfm/main/inference.py | inference.py — sp-uhh/streamfm | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:stream-fm`, thread `stream-fm-development`, 1 dated events 2026-05-14 → 2026-05-14.
- **Practical note:** As of 2026-05-14, practitioners evaluating Stream.FM should consult the examples site, source repository, and supplementary Drive materials together; no specific setup, result, or release version is yet verified.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
