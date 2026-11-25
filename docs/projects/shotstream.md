---
title: ShotStream
category: projects
date: 2026-03-31
tags: [project, shotstream]
aliases: ["ShotStream"]
---

# ShotStream

**Development line:** `project:shotstream` · thread `shotstream`  
**Last event:** 2026-03-31 · 1 dated since 2026-03-31 · **Researched:** 2026-09-06 · confidence: medium

## What it is

ShotStream is a CUDA research implementation for creators and video-model developers who need to steer a multi-shot text-to-video narrative while it runs.

- Next-shot generation from historical shots and streaming prompts.
- Execution on Wan2.1-T2V-1.3B with local checkpoints.
- Separate global and local caches for cross-shot and within-shot continuity.

The authors report 15.95 FPS at 832×480 on one NVIDIA H200. Demos show 5–6 shots and nearly 500 frames. This is a local research reproduction path, not a hosted video service. Public demos do not guarantee parity with the internal training setup.

## Development line

- **2026-03-31 — ShotStream public project, code, and model pages were linked.** On 2026-03-31, a dated post pointed readers to the public project page, GitHub repository, and Hugging Face page. The evidence provides a public reference point for the development line. It does not establish a release version, capabilities, authorship, or the exact text of the original message.

## What changed

- 2026-03-25 — ShotStream’s Hugging Face history records configuration and three checkpoint uploads.
- 2026-03-26 — ShotStream’s arXiv v1 was submitted.
- 2026-03-27 — ShotStream released its project page, arXiv version, training/inference code, and checkpoints.
- 2026-03-31 — ShotStream’s model card received a text-to-video tag plus expanded documentation, usage, and citation material.
- 2026-06-18 — ShotStream’s repository reported acceptance to ECCV 2026.

## How to use this

1. Clone the repository and create the documented Python 3.10, CUDA, PyTorch, requirements, and FlashAttention environment.
  — <https://github.com/KlingAIResearch/ShotStream>
2. Download both the Wan2.1-T2V-1.3B base model and ShotStream checkpoints with Git LFS into the documented directories.
  — <https://github.com/KlingAIResearch/ShotStream>
3. Prepare prompt JSON with one global_caption and shot1 through shotN descriptions for the sequence.
  — <https://github.com/KlingAIResearch/ShotStream/blob/main/demo/testdata/json/01.json>
4. Run the documented autoregressive four-step multi-shot inference launcher.
  — <https://github.com/KlingAIResearch/ShotStream>

## Superseded by this

- 2026-03-27 — Released training code, inference code, and checkpoints supersede the pre-release paper state.
- 2026-03-31 — Model-card documentation and pipeline metadata updated; this date brought no new weights or code.
- 2026-06-18 — ECCV 2026 acceptance supersedes pre-acceptance venue status without announcing a new runtime artifact.

## Still unknown

- The links alone do not establish whether the 2026-03-31 event specifically referred to the same-day model-card update.
- Primary sources list no supported hosted endpoint, consumer-GPU minimum, VRAM requirement, or independent reproduction benchmark. The reported throughput is an author H200 measurement.
- Primary sources contain no first-party Simplified-Chinese operating guidance or independent practitioner discussion. Secondary summaries were not used as evidence.

## Sources

| source | title | read |
|---|---|---|
| https://luo0207.github.io/ShotStream/ | ShotStream project page | 2026-09-07 |
| https://github.com/KlingAIResearch/ShotStream | KlingAIResearch/ShotStream repository and README | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream | KlingTeam/ShotStream model card | 2026-09-07 |
| https://arxiv.org/abs/2603.25746 | ShotStream: Streaming Multi-Shot Video Generation for Interactive Storytelling | 2026-09-07 |
| https://arxiv.org/html/2603.25746 | ShotStream paper HTML | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream/commits/main | KlingTeam/ShotStream commit history | 2026-09-07 |
| https://huggingface.co/KlingTeam/ShotStream/discussions/1 | Improve model card and add pipeline tag | 2026-09-07 |
| https://github.com/KlingAIResearch/ShotStream/blob/main/demo/testdata/json/01.json | ShotStream demo prompt JSON | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:shotstream`, thread `shotstream`, 1 dated events 2026-03-31 → 2026-03-31.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
