---
title: "AGSoft Save Image Plus: agsoft-save-image-plus-update — Agsoft Save Image Plus Update"
category: "projects"
date: 2026-11-19
tags: ["agsoft-save-image-plus", "agsoft-save-image-plus-update", "project"]
aliases: ["AGSoft Save Image Plus: agsoft-save-image-plus-update"]
---

# AGSoft Save Image Plus: agsoft-save-image-plus-update — Agsoft Save Image Plus Update

AGSoft Save Image Plus is a ComfyUI node for saving images, an alternative to the standard Save Image node and to wcgrnway Save Image Plus.

**Development line:** project:agsoft-save-image-plus · thread agsoft-save-image-plus-update  
**Last event:** 2026-11-19 · 1 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: medium

## What it is

The node works only in ComfyUI. It needs the parent comfyui-AGSoft custom node suite installed. It makes image inspection and export setup easier inside modern node graph layouts.

Abilities:

- Batch preview: shows every image of a batch
- Tooltips: button hints in two languages
- Focus mode: inspects images of a multi-image generation one by one
- Workflow metadata: embeds the workflow in the saved file
- Pass-through: outputs the image onward

## Development line

- **2026-11-19 — AGSoft Save Image Plus adds focus mode, tooltips and Nodes 2.0 support.** On 2026-11-19 the ComfyUI custom node got an update. It adds a focus mode for batch previews and button tooltips in two languages. Previews now work in the Nodes 2.0 interface, and the classic canvas mode still works.
  - Focus mode and the bilingual tooltips ship in the comfyui-AGSoft repository, with Nodes 2.0 preview support and classic canvas rendering kept for compatibility. (2026-11-19) — <https://github.com/Art-xmaster/comfyui-AGSoft>

## What changed

Early releases wrote images and serialized metadata inside the comfyui-AGSoft extension. Later updates added focus mode for multi-image batches and bilingual button tooltips. They also made previews work in the ComfyUI Nodes 2.0 interface, with classic canvas rendering kept.

## How to use this

1. Clone the repository into the ComfyUI custom\_nodes directory with git clone https://github.com/Art-xmaster/comfyui-AGSoft.git, or install comfyui-AGSoft through ComfyUI Manager.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
2. Restart the ComfyUI server so it loads the custom node definitions.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
3. Add the AGSoft Save Image Plus node to the workflow and connect the generated image tensor to its image input.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
4. Set the filename prefix and format options, then turn on focus mode to preview batch generations in the classic canvas or in Nodes 2.0.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Best practices

- Keep the classic canvas fallback on if the UI renders inconsistently in early Nodes 2.0 builds.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>
- Use focus mode for multi-image batches, so each preview frame can be checked without leaving the node graph.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Superseded by this

- Image previews for AGSoft Save Image Plus did not work in the ComfyUI Nodes 2.0 interface and needed classic canvas mode.
  — <https://github.com/Art-xmaster/comfyui-AGSoft>

## Still unknown

- Independent Chinese community discussions and issue trackers for the 2026-11-19 release have no direct URLs outside search engine redirects.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Art-xmaster/comfyui-AGSoft | Art-xmaster/comfyui-AGSoft | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:agsoft-save-image-plus, thread agsoft-save-image-plus-update, 1 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
