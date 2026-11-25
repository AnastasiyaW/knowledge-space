---
title: comfyui-lrw-nodes — ComfyUI LRW Nodes
category: projects
date: 2026-06-09
tags: [comfyui-lrw-nodes, comfyui_lrw_nodes, project]
aliases: ["comfyui-lrw-nodes"]
---

# comfyui-lrw-nodes — ComfyUI LRW Nodes

**Development line:** `project:comfyui-lrw-nodes` · thread `comfyui-lrw-nodes`  
**Last event:** 2026-06-09 · 1 dated since 2026-06-09 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI-LRW-Nodes provides custom nodes for ComfyUI to guide WAN2.2 First–Last Frame intermediate motion without replacing endpoint conditioning.

- Geodesic and SLERP latent interpolation.
- Latent distance, curvature, and parallel-transport experiments.
- WAN2.2 geodesic keyframe blending into video latents before KSampler.

Requires `latent-riemannian-world >= 0.3.0`, `torch >= 2.4`, and extra WAN and video nodes for the supplied workflow.
Use it as an experimental soft guide and compare against a fixed-seed direct-FLF baseline; it does not replace WAN2.2 endpoint continuity.

## Development line

- **2026-06-09 — ComfyUI LRW Nodes repository and workflow examples were documented.** A dated message on 2026-06-09 linked ComfyUI LRW Nodes to its GitHub repository and example-workflows directory. This confirms people referenced the project and workflows on that date. It shows no specific release, feature change, or repository state.

## What changed

- 2026-06-07 — Initial public rollout targeted WAN2.2 First–Last Frame. LRW endpoint latents produced a geodesic guide blended before KSampler. A same-day registration and import-path fix followed.
- 2026-06-09 — The repository and its workflow directory went public. We have no release version or dated changelog for this step.

## How to use this

As of 2026-06-09, evaluate ComfyUI LRW Nodes through the repository and example workflows.

1. Install through ComfyUI Manager by searching `comfyui-lrw-nodes`, or clone the repository into `ComfyUI/custom_nodes`, run `pip install -r requirements.txt`, and restart ComfyUI.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
2. For WAN2.2, install workflow dependencies: ComfyUI-GGUF, WAN First–Last Frame support, and ComfyUI-VideoHelperSuite; KJNodes is optional.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
3. Load the practical workflow. Feed first and last images to direct `WanFirstLastFrameToVideo`, then VAE-encode both endpoint images for LRW.
  — <https://github.com/lajjadred/comfyui-lrw-nodes/tree/main/examples/workflows>
4. Create geodesic keyframes, pass one through `LRW_WanLatentGuideBlend`, sample with KSampler, and decode/combine the video.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>

## Best practices

- Keep direct WAN2.2 FLF as the continuity path. Blend the LRW guide into its video latent instead of replacing target last-frame conditioning.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
- Start with `blend_strength=0.15`, `time_schedule=middle_focus`, and `normalize_guide=true`; the documented range is 0.10–0.20.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
- If nodes show as unknown or fail to import, keep one installation only, update or reclone it, restart ComfyUI fully, and inspect the startup log around this node pack.
  — <https://www.reddit.com/r/comfyui/comments/1tz4qnu/i_built_comfyui_nodes_that_use_riemannian/>

## Superseded by this

- 2026-06-07 — Stale `__init__.py` registration importing `LRW_LatentKeyframePicker` from `wan_nodes.py` is obsolete. Update the node pack and restart ComfyUI.
- 2026-06-07 — Guidance that treats LRW as a direct quality upgrade or replacement for WAN2.2 FLF end-frame conditioning is obsolete. Its documented role is a soft pre-KSampler latent guide.

## Still unknown

- No dated first-party release, tag, or changelog establishes the exact repository revision on 2026-06-09.
- The README lists four example workflows, while the linked workflow directory shows only `wan22_practical_direct_flf_plus_lrw_guided_blend.json`. Baseline, image-interpolation, and style-transfer JSON files are unverified.
- GitHub reports ten commits, but their dated history could not be retrieved during this check.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/lajjadred/comfyui-lrw-nodes | lajjadred/comfyui-lrw-nodes README | 2026-09-05 |
| https://github.com/lajjadred/comfyui-lrw-nodes/tree/main/examples/workflows | comfyui-lrw-nodes example workflows | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1tz4qnu/i_built_comfyui_nodes_that_use_riemannian/ | I built ComfyUI nodes that use Riemannian geometry to guide WAN2.2 latent interpolation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui-lrw-nodes`, thread `comfyui-lrw-nodes`, 1 dated events 2026-06-09 → 2026-06-09.
- **Practical note:** As of 2026-06-09, practitioners can use the linked project repository and example workflows as the starting point for evaluating or adopting ComfyUI LRW Nodes.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
