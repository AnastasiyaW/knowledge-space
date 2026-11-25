---
title: MolmoMotion
category: projects
date: 2026-06-18
tags: [molmomotion, molmomotion-model-availability, project]
aliases: ["MolmoMotion"]
---

# MolmoMotion

**Development line:** `project:molmomotion` · thread `molmomotion-model-availability`  
**Last event:** 2026-06-18 · 1 dated since 2026-06-18 · **Researched:** 2026-09-05 · confidence: high

## What it is

MolmoMotion is a Molmo 2-based 4B model for researchers building robot planning or trajectory-guided video generation.

- 3D point paths: forecasts object-attached paths.
- Conditioning: conditions on RGB history, 2D/3D query points, and an action.
- Model variants: supplies AR and flow-matching variants.

The H3-F30 checkpoint needs three frames and predicts 30 future frames, about two seconds at 15 fps.
Use it for 3D motion-forecasting experiments, not as a text-to-video model or a robot policy by itself.

## Development line

- **2026-06-18 — MolmoMotion-4B-H3-F30 model resource recorded.** The autoregressive 4B checkpoint takes three history frames and forecasts 30 future 3D positions per query point.

## What changed

2026-06-18 — MolmoMotion-4B-H3-F30 became available: the autoregressive 4B checkpoint takes three history frames and forecasts 30 future 3D positions per query point.

## How to use this

As of 2026-06-18, track MolmoMotion-4B-H3-F30 as a separately identifiable MolmoMotion model resource. Verify its model card before relying on its capabilities, license, or deployment requirements.

1. Install the official repository in a Python 3.11 environment with the visualization extra.
  — <https://github.com/allenai/molmo-motion>
2. Download and load `allenai/MolmoMotion-4B-H3-F30` with `MolmoMotionProcessor` and `MolmoMotion`; run the internal model in bf16 on CUDA.
  — <https://github.com/allenai/molmo-motion>
3. Provide three RGB frames ordered from earliest to t0, 2D point coordinates at t0, 3D point history in the camera-at-t0 frame, an action description, and future horizon 30.
  — <https://github.com/allenai/molmo-motion>
4. Call `predict_trajectory` and consume `future_3d` as an 8-by-30-by-3 tensor of meter-scale camera-frame coordinates; render or pass the trajectories to a downstream system.
  — <https://github.com/allenai/molmo-motion>

## Best practices

- Choose H3-F30 for ordinary video input; choose H1-F32 only when there is a single query keyframe.
  — <https://huggingface.co/allenai/MolmoMotion-4B-H3-F30>
- Treat trajectories as planning or generation guidance and fine-tune for a downstream robotics task rather than presenting the base forecaster as a deployable policy.
  — <https://huggingface.co/allenai/MolmoMotion-4B-H3-F30>
- Use the official quick-start input contract; query-point 3D history must be expressed in the camera frame at t0.
  — <https://github.com/allenai/molmo-motion>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- We found no dated first-party successor release after the 2026-06-18 checkpoint event in the consulted sources. The public repository documents H1-F32 and model families, but does not establish a later release date for them.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/allenai/MolmoMotion-4B-H3-F30 | allenai/MolmoMotion-4B-H3-F30 model card | 2026-09-05 |
| https://github.com/allenai/molmo-motion | allenai/molmo-motion official repository | 2026-09-05 |
| https://allenai.org/blog/molmo-motion | MolmoMotion: Language-guided 3D motion forecasting | 2026-09-05 |
| https://arxiv.org/abs/2606.18558 | MolmoMotion: Forecasting Point Trajectories in 3D with Language Instruction | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:molmomotion`, thread `molmomotion-model-availability`, 1 dated events 2026-06-18 → 2026-06-18.
- **Practical note:** As of 2026-06-18, track MolmoMotion-4B-H3-F30 as a separately identifiable MolmoMotion model resource and verify its model card before relying on its capabilities, license, or deployment requirements.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.