---
title: MOSS-Video-Preview
category: projects
date: 2026-06-10
tags: [moss-video-preview, project]
aliases: ["MOSS-Video-Preview"]
---

# MOSS-Video-Preview

**Development line:** `project:moss-video-preview` · thread `moss-video-preview`  
**Last event:** 2026-06-10 · 1 dated since 2026-06-10 · **Researched:** 2026-09-05 · confidence: medium

## What it is

MOSS-Video-Preview is an Apache-2.0, custom-code video-language model family built on gated image-video cross-attention: Base for pretraining, SFT for offline instruction following, and Real-Time-SFT for live frame-by-frame inference. The released Base checkpoint is 11B BF16; the project reports a single-H200 measurement of 1.9537 s average TTFT on a 256-frame test. Verdict: use Real-Time-SFT only when streaming behavior is required; this is an exploratory research release, not a hosted inference service.

## Development line

- **2026-06-10 — MOSS-Video-Preview public project resources referenced.** On 2026-06-10, the MOSS-Video-Preview development line was associated with a public GitHub repository and a Hugging Face collection. The dated links establish a public project reference point, but do not by themselves establish a specific release, model capability, or version change.

## What changed

2026-06-10 — The linked project package was publicly discoverable; first-party material identifies the family as a roughly 10.7B/11B gated-cross-attention video model with separate Base, offline SFT, and Real-Time-SFT checkpoints. 2026-06-01 — OpenMOSS published the technical report and released Realtime-QA-100K, a 100,000-sample training subset for real-time video QA. 2026-04-08 — OpenMOSS released MOSS-VL-Base-0408 and MOSS-VL-Instruct-0408 after starting the MOSS-VL line. 2026-03-04 — Source code and architecture details for MOSS-Video-Preview were released. 2025-10-18 — The project recorded a post-mortem and began MOSS-VL. 2025-10-08 — An internal demo was shown. 2025-09 — The Real-Time-SFT checkpoint was ready. 2025-08 — The offline SFT checkpoint was ready.

## How to use this

As of 2026-06-10, practitioners should use the linked GitHub repository and Hugging Face collection as the initial public reference points for MOSS-Video-Preview, while verifying any claimed release details from primary project materials.

1. Clone the repository, create the documented Python 3.12.4 environment, and install the package; the tested stack is PyTorch 2.4.0 with CUDA 12.1 and DeepSpeed 0.16.1.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
2. Use `moss-video-preview-sft` with `inference.offline_infer` for a prerecorded video and an instruction prompt; use the Base checkpoint for completion or as an SFT starting point.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
3. Use `moss-video-preview-realtime-sft` with `inference.realtime_streaming_infer` for incoming frames; Base and plain SFT are not compatible with the streaming path.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
4. Load Realtime-QA-100K with the Hugging Face `datasets` library when reproducing or adapting real-time SFT data; it provides annotations, YouTube IDs, and timestamps rather than video files.
  — <https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K>

## Best practices

- Select the checkpoint by task: Base needs downstream SFT for instruction following, offline SFT is for whole clips, and Real-Time-SFT is the required checkpoint for streaming.
  — <https://huggingface.co/OpenMOSS-Team/moss-video-preview-base>
- Use `trust_remote_code=True` only after reviewing the repository code, because this model family requires custom Transformers mappings; use FlashAttention 2 on CUDA when low latency matters.
  — <https://huggingface.co/OpenMOSS-Team/moss-video-preview-realtime-sft>
- Treat the published speed comparison as one H200 setup, not as a general benchmark; its test used 256 extracted frames from one 97.56-second, 1080p video.
  — <https://github.com/OpenMOSS/MOSS-Video-Preview>
- For Realtime-QA-100K, plan for video availability and rights yourself: the release contains no videos, and the original YouTube material can disappear or be region-restricted.
  — <https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The supplied Hugging Face collection endpoint did not return readable content during this check, so its creation date and the exact collection state on 2026-06-10 are unverified.
- No first-party source examined declares MOSS-Video-Preview formally deprecated or states that MOSS-VL supersedes it; MOSS-VL is therefore recorded as a related successor development line, not a formal replacement.
- The project’s current README still describes further scaling, distributed training, and broader code/data releases as future work; production readiness, maintained release cadence, and third-party serving support are unverified.
- event_findings:[2026-06-10] The project documentation identifies the linked release as an approximately 10.7B (marketed as 11B) model family with 40 decoder layers, including 8 gated cross-attention layers; it separates Base, offline SFT, and Real-Time-SFT rather than shipping one interchangeable checkpoint. Source date: 2026-06-01 project news entry; source URL: https://github.com/OpenMOSS/MOSS-Video-Preview.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/OpenMOSS/MOSS-Video-Preview | OpenMOSS/MOSS-Video-Preview repository and README | 2026-09-05 |
| https://huggingface.co/collections/OpenMOSS-Team/moss-video-preview | OpenMOSS-Team MOSS-Video-Preview collection | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-base | OpenMOSS-Team/moss-video-preview-base model card | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-sft | OpenMOSS-Team/moss-video-preview-sft model card | 2026-09-05 |
| https://huggingface.co/OpenMOSS-Team/moss-video-preview-realtime-sft | OpenMOSS-Team/moss-video-preview-realtime-sft model card | 2026-09-05 |
| https://huggingface.co/datasets/OpenMOSS-Team/Realtime-QA-100K | OpenMOSS-Team/Realtime-QA-100K dataset card | 2026-09-05 |
| https://github.com/OpenMOSS/MOSS-VL | OpenMOSS/MOSS-VL repository | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:moss-video-preview`, thread `moss-video-preview`, 1 dated events 2026-06-10 → 2026-06-10.
- **Practical note:** As of 2026-06-10, practitioners should use the linked GitHub repository and Hugging Face collection as the initial public reference points for MOSS-Video-Preview, while verifying any claimed release details from primary project materials.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
