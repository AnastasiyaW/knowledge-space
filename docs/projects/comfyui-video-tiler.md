---
title: ComfyUI Video Tiler
category: projects
date: 2026-08-05
tags: [comfyui-video-tiler, comfyui_video_tiler, project]
aliases: ["ComfyUI Video Tiler"]
---

# ComfyUI Video Tiler

**Development line:** `project:comfyui-video-tiler` · thread `comfyui-video-tiler`  
**Last event:** 2026-08-05 · 1 dated since 2026-08-05 · **Researched:** 2026-09-05 · confidence: high

## What it is

ComfyUI Video Tiler splits an IMAGE video batch into overlapping tiles, processes them through an upscale workflow, and merges them back without a visible grid. It targets LTX 2.3 and MiniMax H3 workflows.

- Variable and fixed slicers split the frames.
- Feathered merge blends tile seams without a visible grid.
- Disk-backed tile jobs save memory across runs.
- Reference alignment and color matching preserve consistency across tiles.
- Audio detection and sampler timing track clip pacing.

Disk mode reduces cached-tile memory, but the completed merged IMAGE still needs RAM or VRAM. Use it for a tiled upscale workflow already proven with its target model, not as a general-purpose video pipeline.

## Development line

- **2026-08-05 — ComfyUI Video Tiler repository was referenced.** On 2026-08-05, the recorded link referenced the GitHub repository for ComfyUI Video Tiler. That record establishes the public project reference, but does not establish a release, version, feature set, or installation guidance.

## What changed

- **2026-08-05** — The pack registered with the Comfy Registry and received LTX 2.3 and MiniMax H3 example workflows, disk-buffered workflows, and sampler-timing nodes. Repository history identifies seven commits that day, including registry registration, `disk buffered workflows`, both model-specific examples, and `timer nodes added`.
- **2026-08-07** — Example workflows were updated.
- **2026-08-08** — Disk merge was decoupled and tile preview was added, enabling an independent folder-based assembly and review path after tile processing.

## How to use this

As of 2026-08-05, we treat the linked GitHub repository as the confirmed project reference. Verify current documentation and compatibility before use.

1. Install into `ComfyUI/custom_nodes` with `git clone https://github.com/maDcaDDie2000/comfyui-video-tiler`, then restart ComfyUI; normal nodes appear under Video Tiler and disk nodes under Video Tiler/Disk.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
2. For a clip that fits in memory, connect either slicer to the upscale workflow, then feed the processed tile list and the unchanged `tile_config` into Video Tile Merge.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
3. For low-VRAM processing, create a Disk Job, process and save each indexed tile, then use Disk Folder Merge with the completed job folder or manifest and send its IMAGE/audio outputs to a video encoder.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>

## Best practices

- Keep `tile_config` paired with the slicer that created it; use overlap and feathering to avoid hard seams.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
- Use disk-backed processing when processed tiles cannot remain cached, but budget memory for the final full-size merged IMAGE.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>
- Use the included LTX 2.3 or MiniMax H3 workflows as the starting point; other model stacks sit outside the pack's primary tested scope.
  — <https://github.com/maDcaDDie2000/comfyui-video-tiler>

## Superseded by this

- 2026-08-05 — Disk-buffered tile workflows supersede in-memory-only workflow guidance for constrained hardware.
- 2026-08-08 — Independent folder-based merge and preview supersedes connected-graph-only disk merging where appropriate.

## Still unknown

- The repository does not publish formal release tags in the sources inspected, so the August 2026 changes are identified by commit date rather than a versioned release.
- The output schema lacks dedicated fields for event findings and new events; `what_changed` records their required content.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/maDcaDDie2000/comfyui-video-tiler | ComfyUI Video Tiler repository and README | 2026-09-05 |
| https://github.com/maDcaDDie2000/comfyui-video-tiler/commits/main | ComfyUI Video Tiler commit history | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-video-tiler`, thread `comfyui-video-tiler`, 1 dated events 2026-08-05 → 2026-08-05.
- **Practical note:** As of 2026-08-05, practitioners can treat the linked GitHub repository as the confirmed project reference, while verifying its current documentation and compatibility before use.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
