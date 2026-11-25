---
title: "AGSoft Image Crop Plus: agsoft-image-crop-plus-releases — Agsoft Image Crop Plus Releases"
category: "projects"
date: 2026-11-20
tags: ["agsoft-image-crop-plus", "agsoft-image-crop-plus-releases", "project"]
aliases: ["AGSoft Image Crop Plus: agsoft-image-crop-plus-releases"]
---

# AGSoft Image Crop Plus: agsoft-image-crop-plus-releases — Agsoft Image Crop Plus Releases

AGSoft Image Crop Plus is a ComfyUI custom node for manual in-graph image cropping, an alternative to external editors for inpainting.

**Development line:** project:agsoft-image-crop-plus · thread agsoft-image-crop-plus-releases  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

AGSoft Image Crop Plus is an interactive cropping and framing custom node for ComfyUI. It is for workflow builders doing localized generation and inpainting. It is a lightweight alternative to a standalone graphic editor when the crop is done by hand inside the graph.

What it does:

- Crop frame: move it directly on the canvas.
- Preview: a node preview window that can be resized.
- Upload: load an image straight into the node.
- Buttons: reset and resume controls.
- Outputs: images that keep their coordinates for downstream processing.

It runs on the standard ComfyUI frontend. It does not detect features or segment subjects on its own.

## Development line

- **2026-11-20 — AGSoft Image Crop Plus update adds Nodes 2.0 support and resizable preview.** On 2026-11-20 the ComfyUI custom node got full Nodes 2.0 compatibility. The preview now resizes with the node, and crop-frame dragging is fixed. Labels are in English with bilingual tooltips, and there are new Upload, Reset and Resume buttons.
  - The first-party repository documentation lists AGSoft Image Crop Plus in the comfyui-AGSoft node suite by Art-xmaster. The suite has in-node interactive canvas tools, directory batching and image processing utilities, with no external model dependencies. (2026-11-20) — <https://github.com/Art-xmaster/comfyui-AGSoft>

## What changed

The node moved from basic coordinate cropping to an interactive UI node that works with ComfyUI Nodes 2.0. The canvas preview now scales with the node size, and crop-frame dragging is stable. Tooltips are bilingual. Separate buttons upload an image, reset the crop or resume it.

## How to use this

1. Install the comfyui-AGSoft extension pack through ComfyUI Manager, or clone https://github.com/Art-xmaster/comfyui-AGSoft into the ComfyUI custom\_nodes directory.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
2. Place the AGSoft Image Crop Plus node in the graph and connect an input image to its input port.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
3. Resize the node to scale the preview, drag the crop frame on the canvas, or press Upload to load a source image directly.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
4. Send the cropped image output downstream. Use Reset or Resume to change the crop boundaries without rebuilding the node.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Best practices

- Pair the node with inpainting workflows and stitching nodes, so cropped regions are processed at native resolution and the full-frame context is kept.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
- Use the bilingual tooltips to check coordinate parameters. The labels stay in standard English across ComfyUI Nodes 2.0 graphs.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Superseded by this

- Earlier versions needed the coordinate node recreated by hand. Their preview frames were fixed and did not scale, and they had no ComfyUI Nodes 2.0 compatibility.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Still unknown

- Release version tags and commit hashes for this update could not be isolated from search summaries. Reading the git commits directly would settle it.
- Third-party forum discussions and user feedback threads did not show up in direct search results.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Art-xmaster/comfyui-AGSoft | Art-xmaster/comfyui-AGSoft: ComfyUI custom nodes for image batching, directory management, and utilities | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:agsoft-image-crop-plus, thread agsoft-image-crop-plus-releases, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
