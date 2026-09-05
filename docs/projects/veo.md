---
title: Veo
category: projects
date: 2024-05-14
tags: [google_io_2024, project, veo, veo-development]
aliases: ["Veo", "Veo 3"]
---

# Veo

**Development line:** `project:veo` · thread `veo-development`  
**Last event:** 2024-05-14 · 1 dated since 2024-05-14 · **Researched:** 2026-09-05 · confidence: high

## What it is

Veo is Google DeepMind’s video-generation model family for filmmakers, creators, and API users.

- Video clips: generates text-to-video and image-to-video clips.
- Frame controls: supports reference images, first/last-frame generation, and extension.
- Audio tracks: generates synchronized dialogue, sound effects, and ambience.

## Development line

- **2024-05-14 — Veo introduced at Google I/O 2024.** On 2024-05-14, Google introduced Veo at Google I/O 2024. This marks the start of the identified Veo development line and is material to its public history.

## What changed

- 2024-05-14 — Google introduced Veo as a 1080p video model, available only to select creators through VideoFX private preview.
- 2025-05-20 — Veo 3 added native audio. Google introduced Flow and made Veo 3 available in Gemini, Flow, and Vertex AI under announced access conditions.
- 2025-09-26 — Veo 3 was the subject of a zero-shot research report covering visual perception, manipulation, physical modeling, and simple visual reasoning. This was research evidence, not a new product endpoint.
- 2025-10-15 — Veo 3.1 added audio to Ingredients to Video, Frames to Video, and Extend in Flow, with stronger image-to-video prompt adherence.
- 2026-01-13 — Veo 3.1 Ingredients to Video added native 9:16 output and 1080p/4K options in supported professional workflows.

## How to use this

From 2024-05-14, practitioners should treat Veo as a distinct video-generation project and track its subsequent releases, access changes, and model capabilities separately from general Google I/O announcements.

1. Create a Gemini API client, submit a generation request with a Veo model name, poll the long-running operation, then download the generated video.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
2. Write the prompt as subject, action, style, camera, composition, focus, and ambience. Include quoted dialogue or explicit sound cues when audio matters.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
3. Supply an initial image, up to three reference images, or first and last frames for controlled image-to-video work. Use extension only for a Veo-generated clip.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
4. Download the output promptly: Google documents a two-day server retention period.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>

## Best practices

- Specify camera position or movement, framing, lens/focus, and ambience instead of relying on style labels alone.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Use reference images for character, product, or scene consistency; the documented limit is three assets.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Plan high-resolution, reference-image, and extension shots as eight-second units; extension is limited to 720p.
  — <https://ai.google.dev/gemini-api/docs/veo?hl=en>
- Keep speech and sound requirements explicit, then review outputs. Google documents remaining limitations with natural, consistent spoken audio.
  — <https://deepmind.google/models/veo/>

## Superseded by this

- 2024-05-14 — Veo is no longer accurately described as VideoFX private-preview-only; current documentation exposes it through the Gemini API and multiple Google products.
- 2024-05-14 — The original “beyond a minute” positioning does not describe the current documented API unit, which is a 4-, 6-, or 8-second generated clip.

## Still unknown

- The 2024-05-14 item carried no URL, so its association is based on Google’s same-date Veo announcement rather than the original linked material.
- The 2025-09-26 item links to a Veo 3 research project, not a product-release page. Its official publication page is dated 2025-09-24; the exact relationship between the September 26 item and a particular paper revision is not stated.
- The zero-shot research result should not be treated as a supported production workflow or as evidence that Veo exposes segmentation, editing, or reasoning APIs.

## Sources

| source | title | read |
|---|---|---|
| https://blog.google/innovation-and-ai/products/google-generative-ai-veo-imagen-3/ | New generative media models and tools, built with and for creators | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/ | Fuel your creativity with new generative media models and tools | 2026-09-05 |
| https://deepmind.google/research/publications/203190/ | Video models are zero-shot learners and reasoners | 2026-09-05 |
| https://video-zero-shot.github.io/ | Video models are zero-shot learners and reasoners | 2026-09-05 |
| https://blog.google/innovation-and-ai/products/veo-updates-flow/ | Introducing Veo 3.1 and advanced capabilities in Flow | 2026-09-05 |
| https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/ | Veo 3.1 Ingredients to Video: More consistency, creativity and control | 2026-09-05 |
| https://ai.google.dev/gemini-api/docs/veo?hl=en | Generate videos with Veo 3.1 in Gemini API | 2026-09-05 |
| https://deepmind.google/models/veo/ | Veo 3.1 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:veo`, thread `veo-development`, 1 dated events 2024-05-14 → 2024-05-14.
- **Practical note:** From 2024-05-14, practitioners should treat Veo as a distinct video-generation project and track its subsequent releases, access changes, and model capabilities separately from general Google I/O announcements.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.