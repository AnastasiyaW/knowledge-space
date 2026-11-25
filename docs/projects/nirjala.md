---
title: "Nirjala: nirjala-underwater-gaussian-splatting — Nirjala Underwater Gaussian Splatting"
category: "projects"
date: 2026-11-19
tags: ["nirjala", "nirjala-underwater-gaussian-splatting", "project"]
aliases: ["Nirjala: nirjala-underwater-gaussian-splatting"]
---

# Nirjala: nirjala-underwater-gaussian-splatting — Nirjala Underwater Gaussian Splatting

NIRJALA is a 3D Gaussian Splatting framework that recovers water-free appearance and geometry for underwater scenes.

**Development line:** project:nirjala · thread nirjala-underwater-gaussian-splatting  
**Last event:** 2026-11-19 · 2 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: medium

## What it is

NIRJALA is an underwater 3D Gaussian Splatting framework. It jointly recovers medium-free surface appearance and scene geometry. It has three parts:

- a three-path optical formation model with forward scattering
- a bidirectional ten-parameter physical medium anchor
- range-binned color balancing objectives

It renders novel views in real time, at 44 FPS on SeaThru-NeRF scenes. It also bounds color error propagation across deep water ranges.

## Development line

- **2026-11-19 — NIRJALA: 3D Gaussian Splatting framework for water-free underwater scene reconstruction.** An arXiv preprint (2611.23450, published 2026-11-19) introduces NIRJALA. It recovers water-free appearance and geometry for underwater scenes in one framework. It adds a three-path image formation model (TRIVENI), a reversible physics anchor (PRATIBIMBA), physics-informed objectives (SAMARASA) and a new 30-scene path-traced benchmark (SAJALA). The authors report PSNR improving from 24.34 to 24.76 dB and depth AbsRel from 0.109 to 0.091 on SAJALA, against the strongest baseline. LPIPS improves from 0.194 to 0.175 on SeaThru-NeRF at 44 FPS.
- **2026-11-19 — NIRJALA: water-free 3D Gaussian Splatting for underwater scenes.** An arXiv preprint (2611.23450v1, announced 2026-11-19) introduces NIRJALA. It recovers water-free appearance and geometry for underwater scenes in one framework. It adds a bounded-gain three-path image formation model (TRIVENI), a reversible physics anchor (PRATIBIMBA), physics-informed objectives (SAMARASA) and a new 30-scene path-traced benchmark (SAJALA). The authors report PSNR rising from 24.34 to 24.76 dB and depth AbsRel falling from 0.109 to 0.091 on SAJALA. LPIPS falls from 0.194 to 0.175 on SeaThru-NeRF at 44 FPS.
- **2026-11-19 — other reporting on this date.**
  - Authors Latchan Chhetri and Aman Kumar introduce TRIVENI. It sets mathematical bounds on inversion gain and color error propagation by adding range-saturating forward scattering. (2026-11-19) — <https://arxiv.org/abs/2611.23450>
  - The PRATIBIMBA reversible anchor integrates a 10-parameter global physical model that links water recovery and re-formation. It is evaluated on 30 synthetic Blender Cycles path-traced scenes with ground-truth normals. (2026-11-19) — <https://arxiv.org/abs/2611.23450>

## What changed

The framework targets unbounded inversion gain in underwater reconstruction. It puts range-saturating forward scattering into image formation, next to attenuation and backscatter. It then adds a reversible ten-parameter physical anchor, so water parameters stay apart from scene geometry. A 30-scene path-traced synthetic benchmark comes with it, for controlled depth and color validation.

## How to use this

1. Calibrate multi-view underwater camera images and estimate camera poses with structure-from-motion.
  — <https://arxiv.org/abs/2611.23450>
2. Initialize 3D Gaussians. Fit the 10-parameter global physical water model and the neural transmission parameters with the TRIVENI three-path formation model.
  — <https://arxiv.org/abs/2611.23450>
3. Optimize geometry and appearance with the SAMARASA objectives. Enforce range-binned color priors so channel attenuation stays balanced across distances.
  — <https://arxiv.org/abs/2611.23450>
4. Render novel views in real time. Invert the estimated water medium to get medium-free imagery.
  — <https://arxiv.org/abs/2611.23450>

## Best practices

- Constrain neural water field estimation with the PRATIBIMBA bidirectional physical anchor, so scene geometry does not absorb medium parameters.
  — <https://arxiv.org/abs/2611.23450>
- Use range-binned color balancing during optimization, because wavelengths attenuate differently across depth intervals.
  — <https://arxiv.org/abs/2611.23450>

## Superseded by this

- Two-path underwater image formation models that divide color by exponential transmission terms, with no forward-scattering bounds.
  — <https://arxiv.org/abs/2611.23450>

## Still unknown

- Whether a public code repository exists, and when the authors will release an official implementation.
- How it performs in independent community tests on turbid coastal waters, outside the SAJALA and SeaThru-NeRF datasets.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2611.23450 | NIRJALA: 3D Gaussian Splatting for Water-Free Underwater Scene Reconstruction | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:nirjala, thread nirjala-underwater-gaussian-splatting, 2 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
