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

Video-DeepResearch is an open research stack and two models for questions grounded in video objects and events before checking external sources.

- Keyframe selection: selects video frames.
- Crop search: inspects visual subregions.
- Text search: queries external sources.
- Evidence extraction: pulls structured proof from web pages.

Running the documented setup requires separate inference, judge, and extract services; raw checkpoints and API keys do not replace them. The stack fits reproducible evaluation and fine-tuning of video-grounded agents, not a standalone chat service.

## Development line

- **2026-08-10 — Video-DeepResearch public project and source references were recorded.** The video task splits from earlier image-centric Vision-DeepResearch and enforces visual grounding before web search.

## What changed

2026-08-10 — Video-DeepResearch appeared as a project page and a section in the Vision-DeepResearch repository: the video task splits from earlier image-centric Vision-DeepResearch and enforces visual grounding before web search.

## How to use this

As of 2026-08-10, evaluate Video-DeepResearch from the linked project page and source repository, and verify capabilities and release status directly.

1. Clone the repository and work inside the Video-DeepResearch subfolder; it contains separate preprocessing, evaluation, SFT, and RL modules.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
2. Extract keyframes from the video; the documentation recommends CLIP similarity filtering, with pixel-difference only as a rough fallback.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
3. Run a VLM for inference, a separate OpenAI-compatible judge, and the required extract server for Visit; the example uses Qwen3-VL-30B-A3B-Instruct for judge and extract.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
4. Launch an evaluation script for SGLang, vLLM, or OpenAI-compatible MaaS, and pick tool, direct, or both mode.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Best practices

- Collect evidence from frames and crops before opening text search: this order keeps the agent from answering from memory or a single text query.
  — <https://costaliya.github.io/Video-DeepResearch/>
- Use CLIP cosine-similarity for keyframes; use pixel-difference only when CLIP is unavailable and account for rougher selection.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Keep the extract server running: without it, Visit returns raw HTML instead of structured evidence, and documentation warns that agentic accuracy drops sharply.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Compare tool and direct modes through an independent judge to separate search gains from answers based solely on keyframes.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Public materials confirm code, paper, and checkpoint announcements, but we did not run inference or verify the current availability, license, and hardware requirements of each checkpoint.
- VideoDR-Bench500 is listed as coming soon; we cannot treat it as released or use it for comparison.

## Sources

| source | title | read |
|---|---|---|
| https://costaliya.github.io/Video-DeepResearch/ | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch | Osilly/Vision-DeepResearch | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md | Video-DeepResearch README | 2026-09-05 |
| https://arxiv.org/abs/2608.03979 | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:video-deepresearch`, thread `video-deepresearch`, 1 dated events 2026-08-10 → 2026-08-10.
- **Practical note:** As of 2026-08-10, practitioners should use the linked project page and source repository as the starting points for evaluating Video-DeepResearch, while independently verifying its capabilities and release status.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
