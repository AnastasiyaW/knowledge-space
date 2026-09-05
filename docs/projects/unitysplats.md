---
title: UnitySplats
category: projects
date: 2026-07-26
tags: [project, unitysplats]
aliases: ["UnitySplats"]
---

# UnitySplats

**Development line:** `project:unitysplats` · thread `unitysplats`  
**Last event:** 2026-07-26 · 1 dated since 2026-07-26 · **Researched:** 2026-09-05 · confidence: high

## What it is

UnitySplats is a Unity 6 package for importing, loading and rendering 3D Gaussian Splats instead of building a renderer from scratch. It supports PLY, SOG, SPZ and KHR_gaussian_splatting GLB across Built-in, URP and HDRP pipelines. It loads files, byte arrays and streams at runtime, using GPU or CPU sorting. Unity 6000.0 is the minimum engine version. WebGL 2 relies on main-thread CPU sorting and cannot handle large uncompressed scenes. Use it when a Unity project needs multi-format splat playback, but benchmark the GPU and render pipeline before targeting mobile, VR or web delivery.

## Development line

- **2026-07-26 — UnitySplats public project references.** On 2026-07-26, UnitySplats linked to a public GitHub repository and an Arloopa experience page. These references set the public development baseline for the project.

## What changed

2026-07-26 — UnitySplats launched as an open-source Unity package. The initial v1.0.0 release from 2026-07-22 introduced multi-format import and runtime rendering.  
2026-08-18 — v1.2.0 fixed Direct3D 11 CPU-sort depth ordering and viewport selection bugs.

## How to use this

Evaluate the project starting from the UnitySplats repository and the linked Arloopa experience as of 2026-07-26, checking implementation details before adopting it.

1. Add the OpenUPM registry for the com.netpyoung scope and the UnitySplats Git dependency to Packages/manifest.json, or install Unity.WebP first and then UnitySplats from Git URLs in Package Manager.
  — <https://github.com/arloopa/UnitySplats>
2. For URP, add Gsplat URP Feature to the active renderer; for HDRP, add Gsplat HDRP Pass in a Custom Pass Volume before transparent rendering.
  — <https://github.com/arloopa/UnitySplats>
3. Import a binary PLY, SOG, SPZ or qualifying GLB into Assets, choose the UnitySplats GLB importer when needed, then place the generated GsplatAsset in the scene.
  — <https://github.com/arloopa/UnitySplats>
4. For runtime content, load a local path with GsplatRuntimeLoader.LoadFile or fetch URI data with UnityWebRequest and pass the bytes to GsplatRuntimeLoader.Load; create and destroy Unity objects on the main thread.
  — <https://github.com/arloopa/UnitySplats>

## Best practices

- Prefer Vulkan on Android and Vulkan or Direct3D 12 on Windows, because Direct3D 11 and OpenGL fall back to the CPU sorter.
  — <https://github.com/arloopa/UnitySplats>
- Use Spark-packed assets to save memory and speed up uploads; reserve Uncompressed for assets that need exact source values.
  — <https://github.com/arloopa/UnitySplats>
- Keep cross-renderer sorting enabled for overlapping Spark renderers on Vulkan, Direct3D 12 and Metal; it cannot merge sorting on CPU paths.
  — <https://github.com/arloopa/UnitySplats>
- Use Spark compression and moderate splat counts for WebGL 2, because browser memory is limited and sorting runs on the main thread.
  — <https://github.com/arloopa/UnitySplats>

## Superseded by this

- 2026-08-18 — v1.2.0 replaces the earlier Direct3D 11 CPU fallback’s 16-bit depth ordering and Main-camera Scene-view sort behavior.
- 2026-07-22 — v1.1.0 enables compatible Spark-renderer sorting by default instead of keeping it optional, and migrates existing settings once.

## Still unknown

- No primary performance benchmark exists in the reviewed sources for a specific splat count, device class, frame-rate target or XR setup.
- The ARLOOPA experience page did not return readable text during research, so we do not use it as evidence.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/arloopa/UnitySplats | arloopa/UnitySplats — GitHub repository and installation documentation | 2026-09-05 |
| https://raw.githubusercontent.com/arloopa/UnitySplats/main/CHANGELOG.md | UnitySplats changelog | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:unitysplats`, thread `unitysplats`, 1 dated events 2026-07-26 → 2026-07-26.
- **Practical note:** Start evaluating the project from the UnitySplats repository and the linked Arloopa experience as of 2026-07-26, verifying implementation details before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
