---
title: "Perf Gs: perf-gs-release — Perf Gs Release"
category: "projects"
date: 2026-11-26
tags: ["perf-gs", "perf-gs-release", "project"]
aliases: ["Perf Gs: perf-gs-release"]
---

# Perf Gs: perf-gs-release — Perf Gs Release

PERF-GS is Electronic Arts' open-source 3D Gaussian Splatting training engine that runs on NVIDIA and AMD GPUs without CUDA.

**Development line:** project:perf-gs · thread perf-gs-release  
**Last event:** 2026-11-26 · 3 dated since 2026-11-26 · **Researched:** 2026-11-27 · confidence: high

## What it is

PERF-GS is a cross-platform, differentiable 3D Gaussian Splatting training framework from Electronic Arts. It targets real-time 3D reconstruction on consumer GPUs. It is a lean, GPU-agnostic alternative to the usual CUDA-locked Gaussian splatting implementations.

The frontend is Python, the backend is SlangPy, and the shaders are written in Slang and run over Vulkan and Direct3D 12. It needs no hard CUDA dependency and no PyTorch native C\+\+ extensions, and it supports NVIDIA and AMD hardware.

Abilities:

- COLMAP point cloud enrichment: adds points by stereo triangulation
- Morton curve ordering: sorts the scene spatially
- Cluster-based culling
- GPU gradient accumulation
- bfloat16 Adam optimizer moments
- System memory image streaming: keeps memory bounded by the streaming image buffers
- Presets: Ultrafast, Balanced, Quality and Quality\+

The fastest runs finish Mip-NeRF 360 scenes in about 10 to 22 seconds on an RTX 4090.

## Development line

- **2026-11-26 — Electronic Arts releases PERF-GS open-source 3D Gaussian Splatting training engine.** Electronic Arts released PERF-GS, a cross-platform differentiable 3D Gaussian Splatting training engine. It uses a Python front end, a SlangPy backend, and Slang shaders for Vulkan and Direct3D 12. Benchmarks cover Mip-NeRF 360 scenes (RTX 4090, Vulkan) with the Ultrafast, Balanced and Quality presets. The engine is stated to run without CUDA on NVIDIA and AMD GPUs.
- **2026-11-26 — Electronic Arts releases PERF-GS gaussian splatting training engine.** Electronic Arts published PERF-GS, a gaussian splatting training engine that runs without CUDA or PyTorch. It uses Vulkan and Direct3D 12 shaders written in Slang, with a Python frontend and a SlangPy backend. It supports NVIDIA and AMD GPUs and has presets from Ultrafast through Quality\+. It also includes PyTorch interop and custom 3D primitive support.
- **2026-11-26 — Electronic Arts releases PERF-GS Gaussian splatting engine.** Electronic Arts announced PERF-GS, a Gaussian splatting training engine that runs without CUDA or PyTorch. It uses Vulkan and Direct3D 12 shaders through a Python frontend and a SlangPy backend. Benchmark results include a 94.6-second Ultrafast run over the full set. PyTorch interop and custom 3D primitive support are noted.
- **2026-11-26 — other reporting on this date.**
  - The repository documentation says PERF-GS was developed by Stefano Scolari at EA SEED and Worldwide Studios. It uses blue-noise sampling in Ultrafast mode (~10.5 s training), Morton curve spatial ordering, and bfloat16 optimizer moments. (2026-11-26) — <https://github.com/electronicarts/perf-gs>
  - The project documentation says Vulkan and Direct3D 12 execution relies on SlangPy, which compiles the Slang shaders at runtime. It implements cluster-based culling, GPU gradient accumulation, and image streaming straight from system memory, across the Ultrafast through Quality\+ profiles. (2026-11-26) — <https://electronicarts.github.io/perf-gs/>
  - The benchmark releases show single Mip-NeRF 360 scenes finishing in 10 to 22 seconds on an RTX 4090 over Vulkan. Under the Ultrafast preset the complete benchmark set adds up to 94.6 seconds. (2026-11-26) — <https://github.com/electronicarts/perf-gs>

## What changed

Electronic Arts moved 3D Gaussian Splatting training from NVIDIA-specific CUDA pipelines to cross-vendor graphics APIs. PERF-GS replaces the custom CUDA rasterizers with Slang shaders. SlangPy compiles them to Vulkan and Direct3D 12, so the engine runs natively on AMD and NVIDIA hardware with no PyTorch runtime dependency.

The presets range from blue-noise accelerated reconstructions to multi-level spherical harmonics with structural Gaussian splitting. PyTorch interop and custom 3D primitive support come with it.

## How to use this

1. Clone the PERF-GS repository and install the Python frontend with the SlangPy runtime dependencies.
  — <https://github.com/electronicarts/perf-gs>
2. Prepare camera poses and point clouds from COLMAP reconstructions or synthetic camera sets.
  — <https://github.com/electronicarts/perf-gs>
3. Set the execution target to Vulkan or Direct3D 12, depending on your NVIDIA or AMD GPU.
  — <https://github.com/electronicarts/perf-gs>
4. Start training with a preset: Ultrafast, Balanced, Quality or Quality\+. The choice trades reconstruction time against visual fidelity.
  — <https://electronicarts.github.io/perf-gs/>

## Best practices

- Use the Ultrafast preset with blue-noise pixel sampling for first scene alignment and quick geometry checks, before moving to a higher-fidelity profile.
  — <https://electronicarts.github.io/perf-gs/>
- Turn on stereo triangulation at initialization when loading sparse COLMAP point clouds. It enriches the starting set up to 256,000 Gaussian splats.
  — <https://github.com/electronicarts/perf-gs>
- Use bfloat16 Adam optimizer moments and system RAM image streaming to cut VRAM pressure on high-resolution scenes.
  — <https://github.com/electronicarts/perf-gs>

## Superseded by this

- The idea that 3D Gaussian Splatting training strictly requires NVIDIA CUDA environments and proprietary PyTorch C\+\+/CUDA extensions.
  — <https://electronicarts.github.io/perf-gs/>

## Still unknown

- Independent community benchmarks of stability and performance on AMD GPUs under Direct3D 12 are not available yet.
- Long-term integration with commercial DCC tools and production game engine pipelines has not been disclosed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/electronicarts/perf-gs | electronicarts/perf-gs: Cross-platform differentiable 3D Gaussian Splatting engine | 2026-11-27 |
| https://electronicarts.github.io/perf-gs/ | PERF-GS: Differentiable 3D Gaussian Splatting Training Engine | 2026-11-27 |

## Agent brief {#agent-brief}

- **Subject:** project:perf-gs, thread perf-gs-release, 3 dated events 2026-11-26 → 2026-11-26.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
