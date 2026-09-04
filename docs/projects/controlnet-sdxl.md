---
title: ControlNet for SDXL — SDXL ControlNet model releases
category: projects
date: 2023-08-14
tags: [controlnet-sdxl, controlnet_sdxl, project, sdxl-controlnet-model-releases]
aliases: ["ControlNet Depth for SDXL", "ControlNet OpenPose for SDXL", "ControlNet for SDXL"]
---

# ControlNet for SDXL — SDXL ControlNet model releases

**Development line:** `project:controlnet-sdxl` · thread `sdxl-controlnet-model-releases`  
**Last event:** 2023-08-14 · 3 dated since 2023-08-10 · **Researched:** not yet · confidence: unresearched

## What it is

ControlNet for SDXL adapts conditioning models to SDXL. We have not run present-state research yet, so this page carries the dated line and the practical note below, nothing more.

## Development line

- **2023-08-10 — Diffusers published an SDXL ControlNet example and model.** On 2023-08-10, Hugging Face Diffusers linked an SDXL-specific ControlNet example and the diffusers/controlnet-sdxl-1.0 model repository. This was a public development step to adapt ControlNet workflows to SDXL. The accompanying Reddit link is supplementary context rather than a separate event.
- **2023-08-14 — An OpenPose ControlNet model for SDXL was linked.** On 2023-08-14, the thibaud/controlnet-openpose-sdxl-1.0 model repository was linked. It provides an SDXL ControlNet option for OpenPose pose control, extending the available SDXL ControlNet model set.
- **2023-08-14 — A depth ControlNet model for SDXL was linked.** On 2023-08-14, the diffusers/controlnet-depth-sdxl-1.0 model repository was linked. It adds an SDXL ControlNet checkpoint for depth conditioning, providing a separate control modality alongside the OpenPose model.

## How to use this

As of 2023-08-14, choose SDXL-specific ControlNet checkpoints by control signal instead of assuming an earlier ControlNet checkpoint fits SDXL. Use OpenPose for pose guidance and depth for depth guidance.

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

We have not researched the present state. The dated development line above is not yet checked against first-party sources.

## Sources

| source |
|---|
| https://github.com/huggingface/diffusers/blob/main/examples/controlnet/README_sdxl.md |
| https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0 |
| https://huggingface.co/diffusers/controlnet-sdxl-1.0 |
| https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0 |
| https://www.reddit.com/r/StableDiffusion/comments/15n6lso/comment/jvki53u/ |

## Agent brief {#agent-brief}

- **Subject:** `project:controlnet-sdxl`, thread `sdxl-controlnet-model-releases`, 3 dated events 2023-08-10 → 2023-08-14.
- **Practical note:** As of 2023-08-14, practitioners could choose SDXL-specific ControlNet checkpoints by control signal, including OpenPose for pose guidance and depth for depth guidance, instead of assuming an earlier ControlNet checkpoint was appropriate for SDXL.
- **Confidence:** unresearched. Dated supersedes above are the authority for what is obsolete.