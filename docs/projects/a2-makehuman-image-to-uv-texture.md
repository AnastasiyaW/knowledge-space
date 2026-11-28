---
title: "A2 Makehuman Image To Uv Texture: a2-makehuman-image-to-uv-texture-workflow — A2 Makehuman Image To Uv Texture Workflow"
category: "projects"
date: 2026-10-13
tags: ["a2-makehuman-image-to-uv-texture", "a2-makehuman-image-to-uv-texture-workflow", "project"]
aliases: ["A2 Makehuman Image To Uv Texture: a2-makehuman-image-to-uv-texture-workflow"]
---

# A2 Makehuman Image To Uv Texture: a2-makehuman-image-to-uv-texture-workflow — A2 Makehuman Image To Uv Texture Workflow

**Development line:** project:a2-makehuman-image-to-uv-texture · thread a2-makehuman-image-to-uv-texture-workflow  
**Last event:** 2026-10-13 · 1 dated since 2026-10-13 · **Researched:** 2026-11-28 · confidence: low

## What it is

A ComfyUI workflow that generates UV textures for MakeHuman characters from a single reference image, with no hand-written prompts. Qwen3-VL examines the reference and describes each body part. Flux 2 Klein 9B then generates each part, using the UV layout as guidance. Cavity and normal maps preserve surface detail, and the parts are blended with color matching. Required components are Flux 2 Klein 9B, the Qwen3-VL-4B node, rgthree and UV Painter.

## Development line

- **2026-10-13 — A2 MakeHuman Image-to-UV Texture workflow released for ComfyUI.** A ComfyUI workflow was posted that generates MakeHuman UV textures from a reference image without prompts, using Qwen3-VL for per-part descriptions and Flux 2 Klein 9B for generation, with UV-map guidance, cavity and normal maps, and color-matched blending. It supports per-part controls, re-rolls, and a single style across four parts, and also works for MakeHuman distribution clothing.
  - The linked Reddit thread, whose title says the author is still updating a workflow for retexturing, suggests that retexturing workflows of this kind are revised after release. Only the thread title and URL were available, so its contents are not confirmed. (undated) — <https://www.reddit.com/r/comfyui/comments/1x4hdod/im_still_updating_the_workflow_for_retexturing/>

## What changed

The workflow was released on 2026-10-13. It offers per-part control: automatic Qwen descriptions or custom text, which Qwen can be turned off for individually or all at once. Each part can take an extra prompt and an extra reference. Passes can be toggled, and individual parts can be re-rolled with their own seeds. A finished part can be saved and loaded back for refinement. A single style \(photo, cartoon or anime\) can be applied across all four parts. It also works for clothing from the MakeHuman distribution.

## How to use this

1. Before downloading the workflow, open the linked Reddit thread and check for update notes. Its title says the retexturing workflow is still being updated, so a newer version may exist.
  — <https://www.reddit.com/r/comfyui/comments/1x4hdod/im_still_updating_the_workflow_for_retexturing/>

## Best practices

- Treat this workflow as a work in progress: the linked thread's title says the retexturing workflow is still being updated, so re-check it for changes before relying on a particular version.
  — <https://www.reddit.com/r/comfyui/comments/1x4hdod/im_still_updating_the_workflow_for_retexturing/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked page's contents were not available beyond its title and URL, so its relationship to this specific workflow is unconfirmed.
- The workflow's version history and any later changes are unknown.
- Performance, VRAM requirements and result quality have not been independently verified.

## Sources

| source | title | read |
|---|---|---|
| https://www.reddit.com/r/comfyui/comments/1x4hdod/im_still_updating_the_workflow_for_retexturing/ | Reddit: I'm still updating the workflow for retexturing \(r/comfyui\) | 2026-10-13 |

## Agent brief {#agent-brief}

- **Subject:** project:a2-makehuman-image-to-uv-texture, thread a2-makehuman-image-to-uv-texture-workflow, 1 dated events 2026-10-13 → 2026-10-13.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** low. Dated supersedes above are the authority for what is obsolete.
