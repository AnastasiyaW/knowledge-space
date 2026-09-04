---
title: Project Starlight
category: projects
date: 2025-02-11
tags: [project, project-starlight, project-starlight-public-rollout, project_starlight]
aliases: ["Project Starlight"]
---

# Project Starlight

**Development line:** `project:project-starlight` · thread `project-starlight-public-rollout`  
**Last event:** 2025-02-11 · 2 dated since 2025-02-06 · **Researched:** 2026-09-04 · confidence: high

## What it is

Topaz's original generative diffusion model for restorers of archival video and low-resolution GenAI clips.

- Resolution upscaling.
- Structural reconstruction.
- Temporal consistency recovery.

The original model runs in the API as Starlight Precise 1 (`sl-1`) without manual controls, capped at 9 000 input frames. It is not one fixed product but the start of a model family, so choose by specific Starlight variant and run target.

## Development line

- **2025-02-06 — Topaz Labs publicly referenced Project Starlight.** A cloud research diffusion model for video restoration, prioritizing quality over speed and model size.
- **2025-02-11 — Project Starlight appeared in Topaz Labs Experiments.** On 2025-02-11, a Project Starlight URL in Topaz Labs' Experiments web application was recorded. The supplied evidence does not preserve page contents, so this entry records the dated experiments endpoint without claiming a precise workflow, eligibility, or feature set.

## What changed

- 2025-02-06 — Topaz introduced Project Starlight as a cloud research diffusion model for video restoration, prioritizing quality over speed and size.
- 2025-02-11 — The model became available through an experimental web interface. At the time, free previews and paid renders carried different content terms.
- 2025-03-05 — Early access added 4K Starlight renders.
- 2025-03-25 — Topaz prepared the first locally runnable variant of the series.
- 2025-05-13 — Starlight Mini launched for local rendering on Windows with NVIDIA GPUs.
- 2025-09-17 — Starlight Sharp expanded the local and cloud lineup with a more detailed variant.

## How to use this

Treat the Topaz Labs Experiments route from 2025-02-11 as a dated discovery path. Verify the current experiment page before attempting use, because these links alone do not establish capabilities or access requirements.

1. Decide whether we need a local model in Topaz Video or a cloud model. The documentation lists Mini, Sharp, Fast 2, HQ, and Precise 2.5/2.6, and notes that cloud models also run in Astra.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
2. For local rendering, install Topaz Video alongside Neuroserver. All Starlight diffusion models require it. If Neuroserver fails, Topaz advises reinstalling the application in Repair mode.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
3. For programmatic processing, submit video to the Video API using the `sl-1` model. Set technical parameters as needed and do not exceed 9 000 input frames.
  — <https://developer.topazlabs.com/video-models/starlight/starlight-precise-1>

## Best practices

- Plan the queue by actual duration, resolution, and frame rate. Starlight diffusion runs can take from several minutes to several days.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
- Test a short representative clip before a full render when original identity and fine detail matter. Early user samples showed altered facial expressions and artifacts on degraded VHS footage.
  — <https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10>
- Do not upload sensitive footage to the free preview tier. In February 2025, Topaz separated modes: paid renders were not used for model training without consent, while free previews could be stored, reviewed, and used in research.
  — <https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10>

## Superseded by this

- 2025-05-13 — The old rule that Starlight is cloud-only no longer holds for the whole family. Starlight Mini received local rendering on Windows with NVIDIA GPUs, though this does not prove local support for original `sl-1`.
- 2025-09-17 — The earlier two-model split between Project Starlight and Starlight Mini is obsolete. Starlight Sharp joined the product lineup.

## Still unknown

- The original experimental URL no longer proves the current interface or pricing tier. Current Topaz entry points lead to Astra, Topaz Video, and the API.
- We have not verified the primary text of the 2025-02-06 X post directly. A dated Topaz Community post from that same day confirms its substance.
- The exact date when Topaz officially renamed Project Starlight to Starlight Precise 1 remains unrecorded. Current documentation confirms continuity, but not the renaming date.

## Sources

| source | title | read |
|---|---|---|
| https://x.com/topazlabs/status/1887497602398073234 | Topaz Labs announcement of Project Starlight | 2026-09-05 |
| https://app.topazlabs.com/experiments/starlight | Project Starlight experiment | 2026-09-05 |
| https://community.topazlabs.com/t/the-process-of-improving-video-quality-with-project-starlight/87143 | The process of improving video quality with Project Starlight | 2026-09-05 |
| https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10 | Project Starlight - Video AI 6.1 Beta | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-6-0-4/87385 | Topaz Video AI 6.0.4 | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-6-1-2-6-1-3/88231 | Topaz Video AI 6.1.2 + 6.1.3 | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-beta-6-2-0-0-b/89146 | Topaz Video AI Beta 6.2.0.0.b | 2026-09-05 |
| https://community.topazlabs.com/t/video-ai-7-0-new-starlight-mini-local-ai-model/90631 | Video AI 7.0 - NEW Starlight Mini (Local) AI Model | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-1-0-0-new-studio-release/95523/1 | Topaz Video 1.0.0 (New Studio Release) | 2026-09-05 |
| https://developer.topazlabs.com/video-models/starlight/starlight-precise-1 | Starlight Precise 1 | Developer Documentation | 2026-09-05 |
| https://docs.topazlabs.com/topaz-video/project-starlight-series | Starlight Series | Topaz Video | 2026-09-05 |
| https://www.topazlabs.com/starlight | Project Starlight | AI Video Enhancement | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:project-starlight`, thread `project-starlight-public-rollout`, 2 dated events 2025-02-06 → 2025-02-11.
- **Practical note:** Treat the Topaz Labs Experiments route from 2025-02-11 as a dated discovery path for Project Starlight. Verify the current experiment page before attempting use, because these links alone do not establish capabilities or access requirements.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
