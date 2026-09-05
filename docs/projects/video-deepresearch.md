---
title: Video-DeepResearch
category: projects
date: 2026-08-10
tags: [project, video-deepresearch]
aliases: ["Video-DeepResearch"]
---

# Video-DeepResearch

**Development line:** `project:video-deepresearch` · thread `video-deepresearch`  
**Last event:** 2026-08-10 · 1 dated since 2026-08-10 · **Researched:** 2026-09-05 · confidence: high

## What it is

Video-DeepResearch is an open research stack and two models for tasks that ground answers in video objects and events before checking external sources.

- Keyframe selection: locates visual anchors across video frames.
- Crop search: inspects spatial image crops.
- Text search: queries external web sources.
- Structured evidence extraction: extracts proofs from web pages.

A documented run requires separate inference, judge, and extract services; the initial checkpoint and API keys do not replace this setup. It suits reproducible evaluation and fine-tuning of video-grounded agents rather than a turnkey chat service.

## Development line

- **2026-08-10 — Video-DeepResearch public project and source references were recorded.** The video task splits from the earlier image-centric Vision-DeepResearch and requires visual grounding before web search.

## What changed

2026-08-10 — Video-DeepResearch launched as a project page and repository section within Vision-DeepResearch: the video task splits from the earlier image-centric Vision-DeepResearch and requires visual grounding before web search.

## How to use this

Use the linked project page and repository to evaluate Video-DeepResearch as of 2026-08-10, while verifying its capabilities and release status directly.

1. Clone the repository and work inside the Video-DeepResearch subfolder; it contains independent preprocessing, evaluation, SFT, and RL modules.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
2. Extract keyframes from the video; documentation recommends CLIP similarity filtering, with pixel-difference only as a rougher fallback.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
3. Start a VLM for inference, a separate OpenAI-compatible judge, and the required extract server for Visit; the example uses Qwen3-VL-30B-A3B-Instruct for judge and extract.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
4. Run an evaluation launcher for SGLang, vLLM, or OpenAI-compatible MaaS, and choose tool, direct, or both mode.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Best practices

- Collect frame and crop evidence before opening text search: this sequence prevents the agent from answering from memory or off a single text query.
  — <https://costaliya.github.io/Video-DeepResearch/>
- Prefer CLIP cosine-similarity for keyframes; use pixel-difference only when CLIP is unavailable and account for its rougher selection.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Keep the extract server running: without it, Visit returns raw HTML instead of structured evidence, and documentation warns that agentic accuracy drops sharply.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Compare tool and direct modes through an independent judge to separate tool search gains from answers based on keyframes alone.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Public materials confirm the code, the paper, and checkpoint announcements. We have not run inference, and the availability, license, and hardware requirements for each checkpoint remain unconfirmed.
- VideoDR-Bench500 is marked as coming soon; we cannot treat it as released or use it for benchmarks yet.

## Sources

| source | title | read |
|---|---|---|
| https://costaliya.github.io/Video-DeepResearch/ | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch | Osilly/Vision-DeepResearch | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md | Video-DeepResearch README | 2026-09-05 |
| https://arxiv.org/abs/2608.03979 | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:video-deepresearch`, thread `video-deepresearch`, 1 dated events 2026-08-10 → 2026-08-10.
- **Practical note:** As of 2026-08-10, use the linked project page and repository as starting points to evaluate Video-DeepResearch, while verifying its capabilities and release status directly.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
