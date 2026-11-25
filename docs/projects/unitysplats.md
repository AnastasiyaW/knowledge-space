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

UnitySplats — a Unity 6 package for importing, loading and rendering 3D Gaussian Splats instead of building a renderer from scratch. It supports PLY, SOG, SPZ and KHR_gaussian_splatting GLB; Built-in, URP and HDRP; runtime file, byte-array and stream loading; GPU and CPU sorting. Minimum engine version is Unity 6000.0; WebGL 2 uses main-thread CPU sorting and is unsuitable for large uncompressed scenes. Verdict: use it when a Unity project needs multi-format splat playback, but benchmark the target GPU and rendering path before committing to mobile, VR or web delivery.

## Development line

- **2026-07-26 — UnitySplats public project references.** On 2026-07-26, UnitySplats was associated with a public GitHub repository and an Arloopa experience page. Together, those dated references establish a public development reference point for the project.

## What changed

2026-07-26 — UnitySplats was presented as an open-source Unity package; the linked repository’s initial v1.0.0 release was dated 2026-07-22 and introduced the multi-format import/runtime-rendering baseline. 2026-08-18 — v1.2.0 corrected Direct3D 11 CPU-sort depth ordering and viewport-selection defects.

## How to use this

From 2026-07-26, practitioners can use the UnitySplats repository and linked Arloopa experience as starting points for evaluating the project, while verifying implementation details before adoption.

1. Add the OpenUPM registry for the com.netpyoung scope and the UnitySplats Git dependency to Packages/manifest.json, or install Unity.WebP first and then UnitySplats from Git URLs in Package Manager.
  — <https://github.com/arloopa/UnitySplats>
2. For URP, add Gsplat URP Feature to the active renderer; for HDRP, add Gsplat HDRP Pass in a Custom Pass Volume before transparent rendering.
  — <https://github.com/arloopa/UnitySplats>
3. Import a binary PLY, SOG, SPZ or qualifying GLB into Assets, choose the UnitySplats GLB importer when needed, then place the generated GsplatAsset in the scene.
  — <https://github.com/arloopa/UnitySplats>
4. For runtime content, load a local path with GsplatRuntimeLoader.LoadFile or fetch URI data with UnityWebRequest and pass the bytes to GsplatRuntimeLoader.Load; create and destroy Unity objects on the main thread.
  — <https://github.com/arloopa/UnitySplats>

## Best practices

- Prefer Vulkan on Android and Vulkan or Direct3D 12 on Windows; Direct3D 11 and OpenGL use the portable CPU sorter.
  — <https://github.com/arloopa/UnitySplats>
- Use Spark-packed assets for lower memory and faster upload; reserve Uncompressed for cases requiring exact in-project values.
  — <https://github.com/arloopa/UnitySplats>
- Keep cross-renderer sorting enabled for overlapping Spark renderers on compatible Vulkan, Direct3D 12 and Metal targets; it cannot provide a merged order on CPU-sort paths.
  — <https://github.com/arloopa/UnitySplats>
- For WebGL 2, use Spark compression and moderate splat counts because sorting is synchronous on the Unity main thread and browser memory is limited.
  — <https://github.com/arloopa/UnitySplats>

## Superseded by this

- 2026-08-18 — v1.2.0 supersedes the former Direct3D 11 CPU fallback’s 16-bit depth ordering and Main-camera-derived Scene-view sort behavior.
- 2026-07-22 — v1.1.0 changes the earlier optional cross-renderer sorting posture by enabling compatible Spark-renderer sorting by default, while migrating existing settings once.

## Still unknown

- No primary performance benchmark for a specific splat count, device class, frame-rate target or XR configuration was found in the sources reviewed.
- The ARLOOPA experience URL was supplied with the event but did not return readable page content during research, so it is not used as evidence.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/arloopa/UnitySplats | arloopa/UnitySplats — GitHub repository and installation documentation | 2026-09-05 |
| https://raw.githubusercontent.com/arloopa/UnitySplats/main/CHANGELOG.md | UnitySplats changelog | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:unitysplats`, thread `unitysplats`, 1 dated events 2026-07-26 → 2026-07-26.
- **Practical note:** From 2026-07-26, practitioners can use the UnitySplats repository and linked Arloopa experience as starting points for evaluating the project, while verifying implementation details before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
