---
title: ComfyUI-3D-Pack
category: projects
date: 2024-02-12
tags: [comfyui-3d-pack, comfyui-3d-pack-development, comfyui_3d_pack, project]
aliases: ["ComfyUI-3D-Pack"]
---

# ComfyUI-3D-Pack

**Development line:** `project:comfyui-3d-pack` · thread `comfyui-3d-pack-development`  
**Last event:** 2024-02-12 · 1 dated since 2024-02-12 · **Researched:** 2026-11-21 · confidence: medium

## What it is

ComfyUI-3D-Pack is an MIT-licensed set of ComfyUI custom nodes for generating, previewing and converting 3D meshes and Gaussian splats from images.

- Inputs: single images and multi-view images; outputs: .obj, .ply and .glb meshes, and .ply for 3DGS.
- Users: ComfyUI users who want 3D asset generation in the same graph as image and video workflows.
- Key capability: many image-to-3D models, including TripoSG, TRELLIS, Hunyuan3D 2.1, InstantMesh and TripoSR; 3DGS and NeRF training; mesh texture baking with nvdiffrast.
- Limits: Windows pre-builds target Python 3.12, CUDA 12.4 and PyTorch 2.5.1; Era3D needs at least 16 GB VRAM; InstantNGP and 3DGS-to-mesh nodes need Visual Studio Build Tools on Windows.

## Development line

- **2024-02-12 — ComfyUI-3D-Pack roadmap reference.** On 2024-02-12, ComfyUI-3D-Pack referenced its published roadmap. The reference sets the planned development direction, but the evidence does not list individual roadmap items or their status.

## What changed

- 2025-06-05 — the README feature section carries the marker "Last update: 5/June/2025"; this is the latest content date the README itself states.
- 2025-12-29 — last push to the default branch, per the GitHub API (`pushed_at`). The repository has no published releases.
- The roadmap lists four open items as captured. The item "Integrate CharacterGen" is already marked as supported in the features list, so it is treated as stale.

## How to use this

1. Clone the repository into ComfyUI's `custom_nodes` folder and install its requirements; the Windows pre-builds target Python 3.12, CUDA 12.4 and PyTorch 2.5.1.
  — <https://github.com/MrForExample/ComfyUI-3D-Pack>
2. On Windows, install Visual Studio Build Tools before using the InstantNGP and 3DGS-to-mesh nodes; on Linux, `gcc` and `g++` are needed for some nodes.
  — <https://github.com/MrForExample/ComfyUI-3D-Pack>
3. Check VRAM before choosing a model: the README states at least 16 GB for Era3D.
  — <https://github.com/MrForExample/ComfyUI-3D-Pack>
4. Treat the README model list as the supported set; roadmap items are not delivered features.
  — <https://github.com/MrForExample/ComfyUI-3D-Pack>

## Best practices

- Confirm the output format your DCC or engine needs (.obj, .ply or .glb) against the README list before generating batches.
  — <https://github.com/MrForExample/ComfyUI-3D-Pack>
- Check the current README and commit history before relying on a roadmap item, since the roadmap is not dated.
  — <https://github.com/MrForExample/ComfyUI-3D-Pack>

## Superseded by this

- The roadmap item "Integrate CharacterGen" is superseded by the features list, which already names CharacterGen as supported.

## Still unknown

- The minimum ComfyUI version is not stated in the README.
- Roadmap item status is not shown in the captured page; no completion markers were visible.
- Licenses of the individual bundled models (for example TRELLIS or Hunyuan3D) were not checked; the repository's MIT license covers only the node code.
- The stub's 2024-02-12 roadmap reference was not re-verified against an archived copy of the roadmap.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/MrForExample/ComfyUI-3D-Pack | README: features, roadmap, requirements | 2026-11-21 |
| https://api.github.com/repos/MrForExample/ComfyUI-3D-Pack | GitHub REST API: pushed_at, license, archived flag | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-3d-pack`, thread `comfyui-3d-pack-development`, 1 dated event 2024-02-12; README content dated 2025-06-05; last push 2025-12-29.
- **Practical note:** Verify Python, CUDA and VRAM requirements before installing; treat roadmap items as unscheduled.
- **Confidence:** medium. The README is the main source; there are no releases. Dated supersedes above are the authority for what is obsolete.
