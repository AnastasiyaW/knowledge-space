---
title: OrbitSheets
category: projects
date: 2026-08-17
tags: [comfyui-orbitsheets, lumosai8/comfyui-orbitsheets, project]
aliases: ["OrbitSheets"]
---

# OrbitSheets

**Development line:** `project:comfyui-orbitsheets` · thread `comfyui-orbitsheets`  
**Last event:** 2026-08-17 · 1 dated since 2026-08-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

OrbitSheets is a ComfyUI node pack for character turnarounds and location sheets. It builds them from one MiniMax-H3 video take instead of separate image prompts.

- Cut-shot prompts: writes prompt sequences for character and location views.
- Frame selection: picks sharp, distinct frames and builds a contact sheet.
- Frame judging: scores frames via in-graph CLIP, an OpenAI-compatible vision endpoint, or sharpness/diversity fallback.
- Audio reference: extracts a character voice track from the take.

Version 0.1.0 requires Python >=3.10 and `requests`. It needs MiniMax H3 assets and is not an H3 implementation. Use it as a workflow helper when H3 already runs, not as a standalone model or a released plugin.

## Development line

- **2026-08-17 — OrbitSheets GitHub repository linked in the development thread.** The visible development sequence ends at the 2026-08-14 commit, and GitHub has no release.

## What changed

2026-08-13 — Four commits added the MiniMax-H3 character and location pack, updated example workflows, and added an in-graph attention node.  
2026-08-14 — Commit 8952eae switched the default location workflow to cut views and added a turn-rate guard. Continuous motion became opt-in.  
2026-08-17 — No new version appeared on this date. The visible commits end on 2026-08-14, and GitHub has no release.

## How to use this

On 2026-08-17, the linked GitHub repository is the dated source for OrbitSheets. Verify files directly before relying on any feature claim.

1. Clone the repository into `ComfyUI/custom_nodes`, then restart ComfyUI. The nodes appear under the `OrbitSheets` category.
2. Put the MiniMax H3 diffusion model, Qwen3-VL 32B H3 text encoder, and H3 video VAE into ComfyUI model folders. Add the H3 audio VAE only when you need the voice track. Pick any anchor model; the examples use Krea2.
3. Drag a graph from `example_workflows/` for manual runs, or submit the matching graph in `api_workflows/`. The path runs anchor image → `MiniMaxH3ImageToVideo` → decoded frames/audio → Frame Select → Contact Sheet.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
4. Check the Frame Select `info` output after each run. It reports whether selection used in-graph CLIP, an HTTP vision model, or the deterministic fallback.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>

## Best practices

- Keep `coverage=cut views` for location sheets. Switch to `continuous move` only when cuts would invent unseen parts, and keep rotation under the 40°/s limit.
- Set `shots` to your target view count. Set `count` equal to it when you need one keeper per view. Prefer `shot_split=views (by content)`. Rerun the H3 take or lower `shots` if `info` reports fewer distinct views.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
- Use `full body, generous margin` for wings, tails, and props. Give the anchor the same margin so crop bounds do not break the turnaround.
- Keep `free_vram_first` enabled before vision scoring. Test renders before using the lossy `comfy kitchen (int8)` attention backend.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
- Pin the commit in shared workflows because the GitHub releases page has no release.
  — <https://github.com/lumosai8/ComfyUI-OrbitSheets/releases>

## Superseded by this

- 2026-08-14 — Continuous orbit guidance for location sheets is obsolete. `coverage=cut views` is now the default. Continuous motion remains only when cuts would invent unseen sides.
- 2026-08-14 — Unbounded turns in short takes are obsolete. The project clamps turns above 40°/s and documents roughly nine seconds for a 360-degree turn.

## Still unknown

- The README disagrees with the code on character shots. Some sections claim five shots or eight frames. Current node code and the character graph pick six views, including the optional frightened face, from a 124-frame take.
- The README and package metadata name no tested ComfyUI-core version, H3 package revision, or compatibility matrix.
- Upstream tests check selector and prompt code without a GPU. We verified no live MiniMax H3 render here.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/lumosai8/ComfyUI-OrbitSheets | GitHub — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/commits/main | Commits — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/commit/8952eae1d3298f241c538c029a6e929509c4813f | Cut the location sheet instead of moving the camera through it — commit 8952eae | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/blob/main/pyproject.toml | ComfyUI-OrbitSheets pyproject.toml | 2026-09-05 |
| https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py | ComfyUI-OrbitSheets nodes.py | 2026-09-05 |
| https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/example_workflows/CharacterTurnaroundSheetH3.json | Bundled CharacterTurnaroundSheetH3 canvas workflow | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/releases | Releases — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-orbitsheets`, thread `comfyui-orbitsheets`, 1 dated events 2026-08-17 → 2026-08-17.
- **Practical note:** As of 2026-08-17, practitioners can use the linked GitHub repository as the dated source location for OrbitSheets, while verifying its contents before relying on any installation or feature claim.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.