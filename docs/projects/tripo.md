---
title: Tripo
category: projects
date: 2026-06-23
tags: [project, tripo, tripo-development, triposg_triposf]
aliases: ["Tripo", "Tripo 2.0", "Tripo 3.0"]
---

# Tripo

**Development line:** `project:tripo` · thread `tripo-development`  
**Last event:** 2026-06-23 · 4 dated since 2024-09-20 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Tripo is a 3D asset generation suite for artists, game studios, and product teams.

- Studio: integrates generation, segmentation, retopology, texturing, and rigging in one web workspace.
- API: queues text-to-model, image-to-model, and multiview-to-model generation jobs.

The API serves the H2, H3, and P1 model families; pricing and parameters depend on the model and task. We use it to draft and refine assets fast, but we verify topology, scale, and materials in the destination DCC or game engine.

## Development line

- **2024-09-20 — Tripo web application entry point.** On September 20, 2024, Tripo linked directly to the Tripo 3D web application. The source does not give its launch date, version, or capabilities.
- **2025-03-31 — TripoSG public project and distribution links.** Weights and inference code for the image-to-3D model were released separately.
- **2025-08-20 — Tripo Studio generation workspace.** On August 20, 2025, Tripo opened the hosted Tripo Studio workspace, referencing the March 2025 TripoSG release. The notes do not confirm a new model, feature, or pricing change.
- **2026-06-23 — Tripo May product update.** On June 23, 2026, Tripo published the official post "May Update on Tripo." The post does not list the specific changes or verify its exact publication date.

## What changed

- 2024-09-20 — Tripo 2.0 moved the commercial lineup to a new generation of 3D synthesis.
- 2025-03-31 — TripoSG split open research from Studio, releasing image-to-3D weights and inference code separately.
- 2025-08-20 — Algorithm 3.0 reached public release with more detailed geometry, textures, and segmentation.
- 2026-06-23 — Studio added 8K Texture, Segmentation v2, a DCC Bridge for ZBrush, and team pricing tiers.

## How to use this

From 2025-03-31, treat TripoSG's public GitHub and Hugging Face resources as separate from Tripo's hosted app and Studio. From 2026-06-23, check the official update page before assuming the current hosted workflow or feature set.

1. Create an API key and pass it in Bearer Authorization for automation.
  — <https://docs.tripo3d.ai/get-started/quick-start.html>
2. Submit a task to POST /v2/openapi/task with text_to_model, image_to_model, or multiview_to_model.
  — <https://docs.tripo3d.ai/get-started/quick-start.html>
3. Store task_id and poll GET /v2/openapi/task/{task_id} until status is success; result URLs expire by default after five minutes.
  — <https://docs.tripo3d.ai/task-query/get-your-task-result.html>
4. Check credit costs before batch runs: image-to-model costs 20–50 credits, while segmentation, low-poly, and rigging bill separately.
  — <https://docs.tripo3d.ai/get-started/pricing.html>

## Best practices

- Specify object, material, shape, and intent for text 3D, and add a negative prompt to exclude unwanted features.
  — <https://www.tripo3d.ai/blog/text-to-3d-prompt-engineering>
- Check one imported asset for scale, orientation, pivot, and polygon budget before duplicating it across the scene.
  — <https://www.tripo3d.ai/zh-Hant/blog/ai-environment-creator>
- Do not accept automatic retopology for animation without checking deformations. Non-standard anatomy, facial edge loops, and proprietary rigs may require manual cleanup.
  — <https://www.tripo3d.ai/blog/retopo-an-ai-character-model-for-animation>

## Superseded by this

- 2025-02-11 — Claims that Algorithm 2.5 is the latest commercial model were superseded by the public release of Algorithm 3.0 in August 2025.
- 2025-05-22 — The generate-and-export-only workflow was superseded when Tripo Studio added segmentation, low-poly tools, texture editing, and Uni-Rig.
- 2024-09-20 — Tripo 2.0 is obsolete for new integrations; API documentation directs new integrations to H3, H2, P1, or Turbo-v1.0.

## Still unknown

- TripoSG is an open research model from VAST, while Tripo Studio and the API are commercial products in the same ecosystem. We cannot treat them as interchangeable releases.
- The exact launch date of Tripo 2.0 within September 2024 is unverified by a primary dated announcement; only the month and year are confirmed.
- Public API documentation uses H2, H3, and P1, while marketing uses 2.0, 2.5, and 3.0; direct mapping between these names is unconfirmed.

## Sources

| source | title | read |
|---|---|---|
| https://www.tripo3d.ai/blog/vast-open-source-month | VAST Open Source Month | TripoSG & TripoSF, Setting a New SOTA in 3D Generation | 2026-09-05 |
| https://github.com/VAST-AI-Research/TripoSG/blob/main/README.md | TripoSG README | 2026-09-05 |
| https://www.tripo3d.ai/blog/tripo-2-5-and-plugins | Tripo's Latest Releases & Updates: Algorithm 2.5, Blender & Unity Plugins | 2026-09-05 |
| https://www.tripo3d.ai/blog/introducing-tripo-studio | Introducing Tripo Studio: Your Next 3D Workspace with AI | 2026-09-05 |
| https://www.accessnewswire.com/newsroom/en/business-and-professional-services/tripo-the-frontrunner-of-3d-ai-boom-supercharges-new-era-in-cont-1066689 | Tripo 3.0 Upgrade announcement | 2026-09-05 |
| https://www.tripo3d.ai/blog/may-update-on-tripo | What's New on Tripo | May | 2026-09-05 |
| https://docs.tripo3d.ai/get-started/quick-start.html | Tripo OpenAPI quick start and authentication | 2026-09-05 |
| https://docs.tripo3d.ai/task-query/get-your-task-result.html | Get your task result | 2026-09-05 |
| https://docs.tripo3d.ai/get-started/pricing.html | Tripo OpenAPI pricing | 2026-09-05 |
| https://docs.tripo3d.ai/model-generation/image-to-model-v1-4-20240625.html | Image to model v1.4 API reference | 2026-09-05 |
| https://www.tripo3d.ai/blog/text-to-3d-prompt-engineering | How to Master Prompt Engineering for Text to 3D Models | 2026-09-05 |
| https://www.tripo3d.ai/zh-Hant/blog/ai-environment-creator | AI Environment Creator | 2026-09-05 |
| https://www.tripo3d.ai/blog/retopo-an-ai-character-model-for-animation | How to Retopo an AI Character Model for Animation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:tripo`, thread `tripo-development`, 4 dated events 2024-09-20 → 2026-06-23.
- **Practical note:** From 2025-03-31, treat TripoSG's public GitHub and Hugging Face resources as a distinct research/distribution route from Tripo's hosted application and Studio; from 2026-06-23, consult the official update page before assuming the current hosted workflow or feature set.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
