---
title: "Gaussian Light Transport: gaussian-light-transport — Gaussian Light Transport"
category: "projects"
date: 2026-09-13
tags: ["gaussian-light-transport", "project"]
aliases: ["Gaussian Light Transport: gaussian-light-transport"]
---

# Gaussian Light Transport

**Development line:** project:gaussian-light-transport · thread gaussian-light-transport  
**Last event:** 2026-09-13 · 2 dated since 2026-09-13 · **Researched:** 2026-11-18 · confidence: high

## What it is

Gaussian Light Transport is a view-independent global illumination method for graphics engines and offline renderers. It stores scene radiance as a mixture of multidimensional Gaussians instead of evaluating path tracing rays or neural radiosity fields.

- 13-dimensional Gaussian primitives: each one holds 3D position, direction, surface normal, albedo and roughness.
- Optimization: parameters are fitted directly against the rendering equation residual.
- Evaluation: world-space tiling and separable culling, built with Taichi, PyTorch and Mitsuba 3.

A scene takes a few megabytes and evaluates in milliseconds per frame. Non-diffuse, high-frequency specular reflections and dynamic geometry changes need re-optimization.

## Development line

- **2026-09-13 — Gaussian Light Transport.** A rendering technique announced at SIGGRAPH Asia 2026. It represents scene lighting as a mixture of multidimensional Gaussians, for faster training and higher quality global illumination without ray tracing.
- **2026-09-13 — Gaussian Light Transport.** The same technique, announced at SIGGRAPH Asia 2026, described for faster frame times and compact data sizes.
- **2026-09-13 — other reporting on this date.**
  - The primitives are 13-dimensional Gaussians: 3D spatial coordinates, outgoing light directions, surface normals, albedo and roughness. They are trained by minimizing the rendering equation residual directly, not through a Neumann series expansion. (2026-09-13) — <https://patrick-attimont.com/projects/gaussian-light-transport/>
  - The official open-source code uses Mitsuba 3 and Dr.Jit for ray tracing, PyTorch for parameter optimization and Taichi kernels for separable culling and spatial evaluation. Storage is a few megabytes, rendering takes milliseconds. (2026-09-13) — <https://github.com/StokastX/gaussian-light-transport>

## What changed

The first publication and repository release introduced the 13-dimensional Gaussian mixture for the rendering equation. Global illumination moved from per-frame Monte Carlo path tracing to Gaussian optimization against the residual. Later the code was organized into reproducible training pipelines with Mitsuba 3, Dr.Jit and Taichi kernels. It ships pre-trained scene weights, evaluation benchmarks and culling scripts.

## How to use this

1. Clone the StokastX/gaussian-light-transport repository. Set up an environment with PyTorch, Taichi, and Mitsuba 3 with Dr.Jit support.
  — <https://github.com/StokastX/gaussian-light-transport>
2. Prepare a 3D scene with geometry meshes, emitter descriptions and surface reflectance properties \(albedo and roughness\).
  — <https://github.com/StokastX/gaussian-light-transport>
3. Run the optimization script. It initializes the 13D Gaussian mixture and fits it by minimizing the rendering equation residual.
  — <https://patrick-attimont.com/projects/gaussian-light-transport/>
4. Evaluate the result with world-space tiling and separable culling for interactive, view-independent global illumination playback.
  — <https://patrick-attimont.com/projects/gaussian-light-transport/>

## Best practices

- Group disconnected geometry with the same albedo and roughness, so one high-dimensional Gaussian can represent their shared light transport.
  — <https://patrick-attimont.com/projects/gaussian-light-transport/>
- Use world-space tiling and separable culling during evaluation, so overlapping high-dimensional Gaussians do not drag down frame rates in complex scenes.
  — <https://patrick-attimont.com/projects/gaussian-light-transport/>
- Check surface normal alignment and mesh topology in Mitsuba 3 before residual minimization, so the PyTorch optimization converges numerically.
  — <https://github.com/StokastX/gaussian-light-transport>

## Superseded by this

- View-independent global illumination requires per-frame Monte Carlo ray tracing or multi-gigabyte neural radiance field weight checkpoints.
  — <https://patrick-attimont.com/projects/gaussian-light-transport/>

## Still unknown

- No community discussion threads are linked here: their exact URLs could not be confirmed.
- Independent benchmarks on consumer GPUs, outside the authors' test scenes, are not documented.

## Sources

| source | title | read |
|---|---|---|
| https://patrick-attimont.com/projects/gaussian-light-transport/ | Gaussian Light Transport | 2026-11-18 |
| https://github.com/StokastX/gaussian-light-transport | StokastX/gaussian-light-transport: Official implementation of Gaussian Light Transport \(SIGGRAPH Asia 2026\) | 2026-11-18 |

## Agent brief {#agent-brief}

- **Subject:** project:gaussian-light-transport, thread gaussian-light-transport, 2 dated events 2026-09-13 → 2026-09-13.
- **Practical note:** See the usage and practice sections above, with their limits.
- **Confidence:** high. The dated supersedes above decide what is obsolete.
