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

<!-- live-update:9a22698ca8b1d44c45b9878f61fb75f78790f49dd7737df4a921e79e94e2a88d -->
## 2026-10-17 — Tripo launches early access to UV unwrap and retopology

Tripo opened early access to automated UV unwrapping and retopology. Low-poly mesh conversion and UV layout generation now sit directly inside its 3D modeling workflow.

### Usage and practices

- Generate a 3D asset in Tripo from a text description or a 2D image prompt. [Source](https://customuse.com/)
- Run automated retopology to turn the dense generated mesh into an optimized quad or triangle structure, within polygon limits you set. [Source](https://customuse.com/)
- Apply automated UV unwrapping: it calculates seams, packs 2D UV islands and rebakes texture maps onto the unwrapped mesh. [Source](https://customuse.com/)
- Export the optimized asset as FBX, OBJ or USD for a game engine or a digital content creation tool. [Source](https://customuse.com/)
- Set the target polygon count before you run retopology, so asset density matches the engine's performance budget. [Source](https://customuse.com/)
- Check the 2D UV island layout and the seams on high-curvature areas before you bake the final texture maps. [Source](https://customuse.com/)

### Additional evidence

- 2026-10-17: Retopology produces low-poly output as quads or triangles, with what Tripo calls intelligent density allocation. UV seam calculation and island packing run in the same 3D asset generation pipeline. [Source](https://customuse.com/)

### Superseded guidance (retained for history)

- 2026-10-17: AI-generated 3D meshes need manual retopology and UV unwrapping in external software before texturing or going into a game engine. [Source](https://customuse.com/)

### Limits and open questions

- Direct paths to Tripo's documentation on tripo3d.ai could not be verified, because search results masked them behind redirects. So there is no direct first-party citation yet.
- Long-term pricing and tier gating for the early access retopology and UV unwrapping are not announced.


<!-- Retained base: 694331793733b8221866d9072af7e45999930387; article blob: 11d856f6dc8c75d0fae16ee7b15ee410955295d4 -->

<!-- live-update:9bcb91cd3e2d7094b7f6c1e8ebd6eb64e2fe47fe3bfc2d61e36252d582e1a65e -->
## 2026-10-23 — Tripo Studio adds skeletal auto-rigging and text-driven animation

Tripo Studio now rigs characters automatically and animates them from text. Auto-rigging comes with five humanoid skeleton presets: UE5 Mannequin, Mixamo, VRM 1.0, Unity Humanoid and ActorCore. Text to Motion turns a prompt into a 1-10 second clip and can chain clips into multi-stage sequences. Humanoid auto-rigging only accepts meshes under 100,000 triangles. Skin weights may still need fixing in an external DCC tool.

## 2026-10-23 — Tripo Studio introduces auto-rigging and motion generation workflow

Rigging and animation now live inside Tripo Studio. Bones are placed automatically for five standard game engine presets. Animation comes from text prompts, and up to five motion segments can be chained. All of this works on models up to 100,000 triangles.

### Usage and practices

- Get a mesh: generate a 3D character from a text prompt or reference images in Tripo Studio, or import an existing 3D mesh. [Source](https://studio.tripo3d.ai/)
- Rig it: open the Auto-Rigging module and pick one of the five presets (UE5 Mannequin, Mixamo, Unity Humanoid, VRM 1.0 or ActorCore). Check first that the mesh is under 100,000 triangles. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Animate it: pick a ready movement from the motion library, or type a prompt into Text to Motion for a custom 1-10 second clip or a multi-stage sequence. [Source](https://www.tripo3d.ai/blog/rigging-animation)
- Export it: preview deformation in the 3D viewport, adjust stage timings for multi-stage sequences, then export as FBX or GLB with the skeletal animation embedded. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Retopologise first: keep the base mesh below 100,000 triangles before auto-rigging so vertex weights and joint deformation stay consistent. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- Check the hard joints: shoulders, hips and fingers often need their automatic skin weights repaired in Blender or Maya before the character goes into a game engine. [Source](https://www.tripo3d.ai/blog/rigging-animation)
- Block out with free presets: test with the free motion library first, so credits go to custom Text to Motion only when needed. [Source](https://www.tripo3d.ai/blog/rigging-animation)

### Additional evidence

- 2026-10-23: The post-processing release notes say exported rigs and text-to-motion sequences come out as standard editable skeletal animation tracks inside FBX and GLB. They can be retargeted in Unreal Engine, Unity, Blender and WebGL viewers. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)
- 2026-10-23: The technical documentation says auto-rigging positions joints and applies initial heat-map skin weights across five skeletal hierarchies (UE5 Mannequin, Mixamo, VRM 1.0, Unity Humanoid, ActorCore). Prompt chaining allows up to five consecutive motion segments, each with its own duration of up to 10 seconds. [Source](https://www.tripo3d.ai/blog/rigging-animation)

### Superseded guidance (retained for history)

- 2026-10-23: Rigging a Tripo character meant exporting the static mesh to Mixamo, Blender or a similar tool and placing and weighting the skeleton by hand. [Source](https://www.tripo3d.ai/blog/rigging-animation)
- 2026-10-23: Animating Tripo assets meant third-party motion capture libraries or manual keyframing outside Tripo Studio. [Source](https://www.tripo3d.ai/product-doc/module-post-processing/rigging-animation)

### Limits and open questions

- How well deformation holds up over time on non-humanoid or quadruped models with text-driven animation.
- Independent community benchmarks of Tripo Studio skin weighting against the auto-rigging built into DCC tools.
- The neural network architecture and training data behind Text to Motion.

<!-- Retained base: d42a348223e0670592e2f1b683c46992af48130e; article blob: 990e6d08d55ddbad4d5d0b851ef0456aa73dd67f -->
