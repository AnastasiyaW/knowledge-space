---
title: ComfyUI-NKD-VFX-Tools
category: projects

tags: [comfyui-nkd-vfx-tools, comfyui-nkd-vfx-tools-development, comfyui_nkd_vfx_tools, project]
aliases: ["ComfyUI-NKD-VFX-Tools"]
---

# ComfyUI-NKD-VFX-Tools

**Development line:** `project:comfyui-nkd-vfx-tools` · thread `comfyui-nkd-vfx-tools-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI-NKD-VFX-Tools provides interactive VFX-oriented nodes rather than a model: Relight, Lens Blur, Preview 3D, fSpy Camera, Camera Delta Prompt, Perspective Unwarp/Rewarp, Lens Distort, and Mask Scheduler. Current package metadata reports version 1.7.4; it requires a recent ComfyUI frontend and numpy, while seamless Perspective Rewarp edges additionally use OpenCV. Verdict: use it to construct controllable image conditions and hand them to an existing ComfyUI generation workflow, not as a replacement for a diffusion model.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-24 — The package was in its first public-release line: first-party history places the initial public release on July 21 and adds usage instructions on July 23; the July 24 item therefore represents an early public availability step, but no first-party commit is recorded specifically for July 24. 2026-07-27 — Lens Distort was documented as version 1.4.0, and Preview 3D gained direct MESH input plus FOV, roll, and backdrop-color controls. 2026-07-30 — Preview 3D added Hunyuan3D/output-model input support, viewport-controlled depth output, auto-smoothed normals, and a pop-out viewer with keyboard gizmo shortcuts. 2026-07-31 — The contact-shadow calculation was corrected to mark actual ground contact; the package was bumped to 1.7.2. Current observed state — package metadata reports version 1.7.4.

## How to use this

As of 2026-07-24, no practitioner-facing change can be proposed because the source post, links, and research evidence were unavailable.

1. Install from ComfyUI Manager by searching for NKD VFX Tools, or clone the repository into ComfyUI/custom_nodes; restart ComfyUI afterward.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
2. Open nodes under the NKD Nodes menu and build the control image first: solve camera or perspective, position 3D content, and create depth or lighting conditions before passing outputs to the generation graph.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
3. For camera matching, draw two pairs of vanishing lines in NKD fSpy Camera; for a perspective edit, unwarp the surface, edit it, then rewarp it back.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
4. Use Preview 3D with GLB/GLTF, gaussian splats, or supported mesh inputs to produce a composite, object layer, mask, depth map, and camera information for downstream nodes.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>

## Best practices

- Treat the nodes as pre-generation art direction: make light, camera, depth, placement, and perspective explicit in the control image instead of relying on prompt text alone.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
- Keep ComfyUI's frontend current and install numpy; install OpenCV only when Perspective Rewarp needs Seamless Edges, because the rest of that node remains usable without it.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
- Use the interactive viewports to inspect controls visually before queueing an expensive generation pass.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>

## Superseded by this

- 2026-07-23: the early README described its usage guide as temporary until example workflows were ready; current first-party documentation still does not provide a dated replacement workflow collection, so no specific replacement guidance is verified.

## Still unknown

- The July 24 event has no extracted URL or public source text. First-party evidence establishes nearby release and documentation dates, but does not identify an exact July 24 commit, version, or announcement payload.
- No dated first-party release record was found for the current 1.7.4 metadata version, so its exact release date is unverified.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools | Nekodificador / ComfyUI-NKD-VFX-Tools repository and README | 2026-09-05 |
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/commits/master/ | ComfyUI-NKD-VFX-Tools commit history | 2026-09-05 |
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/blob/master/pyproject.toml | ComfyUI-NKD-VFX-Tools package metadata | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-nkd-vfx-tools`, thread `comfyui-nkd-vfx-tools-development`, 0 dated events - → -.
- **Practical note:** As of 2026-07-24, no practitioner-facing change can be proposed because the source post, links, and research evidence were unavailable.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
