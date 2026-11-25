---
title: Ray 3.2 — Luma AI Ray development
category: projects
date: 2026-06-10
tags: [luma-ray, project, ray]
aliases: ["Ray 3.2"]
---

# Ray 3.2 — Luma AI Ray development

**Development line:** `project:ray` · thread `luma-ray`  
**Last event:** 2026-06-10 · 1 dated since 2026-06-10 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Ray 3.2 is Luma’s video model for editors preserving real camera motion and developers embedding video generation.

- Modify Video in the Luma app: source-driven video-to-video that restyles a clip while retaining its duration.
- `ray-3.2` in the Agents API: handles text-to-video, image-to-video, video editing, extension, and reframing.

App-side video-to-video requires a source video and caps at 20 seconds; API generation requests run 5 or 10 seconds. Use the app when the source shot is the asset. Use the API for automated generation or editing. The app-side V2V restriction does not apply to the API.

## Development line

- **2026-06-10 — Luma AI presents Ray 3.2.** On 2026-06-10, a dated Luma AI link identified Ray 3.2 in the Ray product line as a distinct version-level update. The supplied evidence does not establish the release’s capabilities, availability, or migration implications.

## What changed

- 2026-05-27 — Luma published app-side guidance for Ray 3.2 Modify Video: source-driven V2V, exact-duration output, and multi-keyframe art direction.
- 2026-06-10 — The Ray3.2 release event added multi-keyframe direction, HDR/16-bit EXR, Reframe, and the first full-control API. Luma’s canonical announcement is dated 2026-06-09.
- 2026-07-13 — Luma’s current-status page listed Ray3.2 as the current video model and marked Dream Machine and Ray2 as deprecated.

## How to use this

1. In the Luma app, select a video asset and open Modify Video → Ray 3.2 for the standard V2V workflow.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
2. Provide a source clip, then describe the desired end state and/or attach guide-frame keyframes at exact source-frame positions.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
3. Use Motion, Structure, and character controls only for properties that must survive the restyle; iterate at a lower resolution before final output.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
4. For an integration, create an API key, submit `model: "ray-3.2"` jobs to `POST /v1/generations`, and choose `video`, `video_edit`, or `video_reframe` for the task.
  — <https://docs.agents.lumalabs.ai/>
5. Poll `GET /v1/generations/{id}` to `completed` or `failed`, then download the completed output; presigned output URLs expire after one hour.
  — <https://docs.agents.lumalabs.ai/guides/model/>

## Best practices

- For app-side V2V, write a concrete positive description of the final frame state; avoid commands, negation, and a new time-based story because the source clip already supplies motion and timing.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Use prompt plus keyframes for deliberate art direction, and place the keyframes at the source moments that must hold a look or composition.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- Explore in Speed mode at 540p or 720p, then move only the selected direction to Quality, 1080p, HDR, or EXR when the delivery pipeline needs it.
  — <https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video>
- For API image-to-video, use either start/end anchors or paired `keyframes` and `keyframe_indexes`; multi-keyframes require equal-length arrays with unique frame positions and cannot be mixed with the single-anchor route.
  — <https://docs.agents.lumalabs.ai/guides/videos/generation/>

## Superseded by this

- 2026-05-27 — For ordinary V2V transformation, the start/end-only Ray 3.14 Modify workflow is superseded by Ray 3.2’s arbitrary multi-keyframe workflow; Ray 3.14 remains the documented exception for duration changes or looping.
- 2026-06-09 — Treating Ray as an app-only tool with no full-control API is obsolete for Ray3.2.
- 2026-07-13 — Dream Machine and Ray2 are deprecated rather than current Luma video-model choices.

## Still unknown

- The 2026-06-10 event date and Luma’s canonical 2026-06-09 announcement differ by one day; no first-party source explains the difference, so we treat it as a date correction rather than a second launch.
- The supplied URL https://lumalabs.ai/ray3-2 did not return usable content when checked and is therefore not used as evidence.
- Luma has no dated changelog reconciling the launch/status-page figure of 16 keyframes per clip with the current app and API documentation’s 64-anchor workflows; the limits are kept surface-specific.
- We found no dated first-party Ray3.2 model or API release after 2026-06-10; the 2026-07-13 item is a current-status documentation update.

## Sources

| source | title | read |
|---|---|---|
| https://lumalabs.ai/news/introducing-ray-3-2 | Luma Introduces Ray3.2 Model & API: Complete Creative Control for Video Generation | 2026-09-06 |
| https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video | Ray 3.2 Video to Video | Luma | 2026-09-06 |
| https://docs.agents.lumalabs.ai/guides/model/ | Models | Luma Agents | 2026-09-06 |
| https://docs.agents.lumalabs.ai/ | Quickstart | Luma Agents | 2026-09-06 |
| https://docs.agents.lumalabs.ai/guides/videos/generation/ | Video generation | Luma Agents | 2026-09-06 |
| https://lumalabs.ai/llm-info | Luma — Official Information for AI Assistants | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:ray`, thread `luma-ray`, 1 dated events 2026-06-10 → 2026-06-10.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
