---
title: dots3-note preview
category: projects
date: 2026-08-17
tags: [dots-studio/dots3-note-prev, dots3-note-prev, dots3-note-preview-release, project]
aliases: ["dots3-note preview"]
---

# dots3-note preview

**Development line:** `project:dots3-note-prev` · thread `dots3-note-preview-release`  
**Last event:** 2026-08-17 · 1 dated since 2026-08-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

dots3-note preview is a model from dots studio for teams that need a local multimodal agent: text output, understanding of images, documents, charts, audio and video, tool use and long context. It has 280B parameters in total, 16B active, and a context of up to 512K tokens. Verdict: practical only for large-GPU inference; it is not a model for a single ordinary graphics card.

## Development line

- **2026-08-17 — Dots Studio published public resources for dots3-note preview.** `dots3-note-prev` and the FP8 variant `dots3-note-prev-fp8`; the 280B/16B MoE was published, with text, image, video and audio inputs and text output.

## What changed

2026-08-17 — the preview of the first open weights of the dots3 family was released: `dots3-note-prev` and the FP8 variant `dots3-note-prev-fp8`; the 280B/16B MoE was published, with text, image, video and audio inputs and text output. 2026-08-25 — the official Transformers integration remained open as PR #47844, which adds inference-only handling of all four modalities, BF16/FP8 and tests, but is not yet support in a stable library release.

## How to use this

As of 2026-08-17, practitioners should treat dots3-note preview as a separately documented project line and consult its Studio Dots, GitHub, and Hugging Face resources before attempting use; its exact capabilities and setup remain unverified from this evidence.

1. For server-side launch, take the FP8 checkpoint `dots-studio/dots3-note-prev-fp8` and serve it with vLLM or SGLang on one 8-GPU node; set a smaller context if memory or the required parallelism does not allow 512K.
  — <https://github.com/studio-dots-ai/dots3-note-prev>
2. Start an OpenAI-compatible endpoint with the model name `dots3-note-prev`, then call `/v1/chat/completions`; for direct answers disable thinking with `enable_thinking=False`.
  — <https://github.com/studio-dots-ai/dots3-note-prev>
3. Pass images, audio or video as multimodal content; video with an audio track is processed together with its sound.
  — <https://github.com/studio-dots-ai/dots3-note-prev>

## Best practices

- For production-like serving, FP8 on eight GPUs is preferred: BF16 needs more memory, and the context length must be tuned together with the number of concurrent requests and modalities.
  — <https://github.com/studio-dots-ai/dots3-note-prev>
- Do not rely on stable Transformers for native loading: official PR #47844 was still open at the time of checking; use the PR revision only deliberately, or choose vLLM main/nightly.
  — <https://github.com/huggingface/transformers/pull/47844>

## Superseded by this

- 2026-08-25 — the assumption that the model already has stable native Transformers support is outdated: official PR #47844 remains open.

## Still unknown

- The 2026-08-17 date confirms the recorded step, but the first available initial commit on Hugging Face appeared about 11 days before 2026-09-05; the exact cause of the date mismatch cannot be established without a historical release timestamp.
- The full technical report on the project page is marked as forthcoming, so independent verification of the stated benchmarks and quality has not been performed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/studio-dots-ai/dots3-note-prev | studio-dots-ai/dots3-note-prev README | 2026-09-05 |
| https://huggingface.co/dots-studio/dots3-note-prev | dots-studio/dots3-note-prev model card | 2026-09-05 |
| https://huggingface.co/dots-studio/dots3-note-prev/commit/09293f609e9df8ec1b165792420bc7be2cfb86a8 | Release dots3-note preview model commit | 2026-09-05 |
| https://github.com/huggingface/transformers/pull/47844 | Transformers PR #47844: Add dots3-note Preview model support | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:dots3-note-prev`, thread `dots3-note-preview-release`, 1 dated events 2026-08-17 → 2026-08-17.
- **Practical note:** As of 2026-08-17, practitioners should treat dots3-note preview as a separately documented project line and consult its Studio Dots, GitHub, and Hugging Face resources before attempting use; its exact capabilities and setup remain unverified from this evidence.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
