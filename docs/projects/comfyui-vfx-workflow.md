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

VFX Utilities is a ComfyUI workflow by Doug Hogan for compositors and VFX artists. It builds passes without a separate CG render.

- Source-video ingestion: feeds image or video plates into the pipeline.
- RMBG and SAM3: extract alpha and mattes via text prompts or points.
- Face segmentation: isolates facial regions for targeted passes.
- Depth and normal passes: generate spatial maps for relighting, compositing, and look development.

The card provides one downloadable JSON graph.

## Development line

- **2026-06-12 — Dated Comfy workflow reference for VFX passes.** The workflow combines source-video ingestion, RMBG, SAM3 prompt and points, face segmentation, depth, and normals in one ComfyUI graph. The current card lists alpha, depth, and normal maps as outputs. The graph version from the publication date is unconfirmed.

## What changed

2026-06-12 — Doug Hogan published the VFX Utilities workflow. It combines source-video ingestion, RMBG, SAM3 prompt and points, face segmentation, depth, and normals in one ComfyUI graph. The card lists alpha, depth, and normal maps as outputs.

## How to use this

As of 2026-06-12, we treat the workflow as a reference for manual inspection on VFX passes, not as a verified recipe.

1. Open the card and download the workflow JSON.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>
2. Load the JSON into ComfyUI, supply an image or video plate, and set a text prompt or segmentation points.
  — <https://comfy.org/workflows/download/be0889296f65.json?filename=be0889296f65>
3. Run the needed branches and use the alpha, depth, and normal outputs as passes for compositing, relighting, or look development.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The event listed an account URL for heydoughogan, but we could not verify it. The confirmed card author is Doug Hogan / @doughogan.
- The card displays the current JSON and a relative creation date. We cannot confirm the exact nodes and models active on 2026-06-12.
- No dated primary source confirms later changes to this workflow. We added no new dated events.

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
