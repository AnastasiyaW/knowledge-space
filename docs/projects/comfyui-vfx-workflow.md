---
title: heydoughogan ComfyUI VFX Workflow — ComfyUI VFX passes
category: projects
date: 2026-06-12
tags: [comfyui-vfx-passes, comfyui-vfx-workflow, project]
aliases: ["heydoughogan ComfyUI VFX Workflow"]
---

# heydoughogan ComfyUI VFX Workflow — ComfyUI VFX passes

**Development line:** `project:comfyui-vfx-workflow` · thread `comfyui-vfx-passes`  
**Last event:** 2026-06-12 · 1 dated since 2026-06-12 · **Researched:** 2026-09-05 · confidence: medium

## What it is

VFX Utilities is a ComfyUI workflow by Doug Hogan for compositors and VFX artists. It generates passes for relighting, compositing, and look development without a separate CG render.

- Alpha and matte extraction with RMBG and SAM3
- Text prompt and point segmentation
- Face segmentation
- Depth and normal pass generation

The card currently provides 1 downloadable JSON graph.

## Development line

- **2026-06-12 — Dated Comfy workflow reference for VFX passes.** The graph combines source video ingestion, RMBG, SAM3 prompts and points, face segmentation, depth, and normals in 1 ComfyUI graph. The current card lists alpha, depth, and normal maps as outputs. We do not have confirmation for the graph state on the publication date.

## What changed

2026-06-12 — Published VFX Utilities workflow. It combines source video ingestion, RMBG, SAM3 prompts and points, face segmentation, depth, and normals in 1 ComfyUI graph. The current card lists alpha, depth, and normal maps as outputs. The historical version of the graph on the release date remains unconfirmed.

## How to use this

As of 2026-06-12, treat the linked Comfy workflow as a reference to inspect manually for VFX-pass work, rather than as a verified or fully documented recipe.

1. Open the card and download the workflow JSON.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>
2. Load the JSON into ComfyUI, provide an image or video plate, and set prompt text or segmentation points.
  — <https://comfy.org/workflows/download/be0889296f65.json?filename=be0889296f65>
3. Run the required paths and use the alpha, depth, and normal outputs as passes for compositing, relighting, or look development.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The event listed an account URL for heydoughogan, but we could not verify it. The confirmed card author is Doug Hogan (@doughogan).
- The card displays the current JSON with a relative creation date, so the exact node and model setup on 2026-06-12 is not confirmed.
- We found no dated primary source confirming later changes to this workflow, so no new dated events are added.

## Sources

| source | title | read |
|---|---|---|
| https://comfy.org/workflows/be0889296f65-be0889296f65/ | VFX Utilities - ComfyUI Workflow | 2026-09-05 |
| https://comfy.org/workflows/download/be0889296f65.json?filename=be0889296f65 | be0889296f65 workflow JSON | 2026-09-05 |
| https://comfy.org/workflows/doughogan/ | Doug Hogan - ComfyUI Workflow Templates | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-vfx-workflow`, thread `comfyui-vfx-passes`, 1 dated events 2026-06-12 → 2026-06-12.
- **Practical note:** As of 2026-06-12, practitioners should treat the linked Comfy workflow as a reference to inspect manually for VFX-pass work, rather than as a verified or fully documented recipe.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.