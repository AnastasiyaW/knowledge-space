---
title: 3DGS-PLY-3DTiles-Converter
category: projects
date: 2026-08-06
tags: [3dgs-ply-3dtiles-converter, 3dgs_ply_3dtiles_converter, project]
aliases: ["3DGS-PLY-3DTiles-Converter"]
---

# 3DGS-PLY-3DTiles-Converter

**Development line:** `project:3dgs-ply-3dtiles-converter` · thread `3dgs-ply-3dtiles-converter`  
**Last event:** 2026-08-06 · 1 dated since 2026-08-06 · **Researched:** 2026-09-06 · confidence: medium

## What it is

3DGS-PLY-3DTiles-Converter is a Node.js CLI, library, and ESM browser API for converting GraphDECO or KHR-native Gaussian Splatting PLY files into an explicit 3D Tiles tileset.

- Adaptive LOD tiles with SPZ-compressed GLB files.
- Standalone PLY reduction without tileset generation.
- WGS84 positioning and a root transform matrix.

Node.js CLI requires Node.js 18+; the browser API runs in a Web Worker and returns MEMORY_EXHAUSTED when memory runs out.

The converter suits delivering large 3DGS scenes through 3D Tiles, but EXT_splat_opacity is not a universally supported viewer format.

## Development line

- **2026-08-06 — 3DGS-PLY-3DTiles-Converter source repository and public site recorded.** On 2026-08-06, 3DGS-PLY-3DTiles-Converter was recorded with a GitHub source repository and a public Vercel site. This establishes a dated public reference point for the project, without asserting a specific release, feature, or launch event.

## What changed

- 2026-08-04 — GitHub Release v0.6.0 added standalone simplify for direct PLY reduction with --ratio or --target-count; the changelog heading dates this release 2026-08-05.
- 2026-08-05 — v0.6.1 added the ESM browser API with local processing in a Web Worker and raised default memoryBudget from 3 to 4 GB; the changelog heading dates the release 2026-08-06.
- 2026-08-06 — v0.6.2 enabled EXT_splat_opacity v2 by default for CLI, Node.js, and browser conversion, keeping an explicit opt-out.
- 2026-08-28 — v0.6.3 added package/version provenance to GLB and tileset outputs and fixed required Gaussian splat metadata.
- 2026-08-30 — the package index records v0.6.4, but primary release notes for its contents are unavailable.
- 2026-08-31 — the package index records v0.6.5, but primary release notes for its contents are unavailable.

## How to use this

1. Install the package in a Node.js 18+ project: npm install 3dgs-ply-3dtiles-converter.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
2. Convert a PLY file: 3dgs-ply-3dtiles-converter scene.ply out_tiles; for CI add --no-open-inspector.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
3. For georeferencing, pass either --coordinate [lat,long,height] or --transform with a 4×4 matrix and check source_coordinate_system in build_summary.json.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
4. If we only need a reduced PLY, use simplify --ratio 0.5 or simplify --target-count 250000.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/Splat-Simplify.md>

## Best practices

- Do not point an existing directory with valuable data to output_dir: standard conversion clears it before rebuilding; use --continue for interrupted runs.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
- Enable EXT_splat_opacity only for a verified path with 3D-Tiles-RendererJS-3DGS-Plugin; other viewers can ignore the extension and fall back to standard SPZ.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
- Pin the converter version and keep build_summary.json: v0.6.3 writes package/version provenance and fixes required metadata for splat content.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/releases>
- For three.js integration, generate 3D Tiles first: the companion renderer plugin loads tileset/GLB files, not the original PLY.
  — <https://github.com/WilliamLiu-1997/3D-Tiles-RendererJS-3DGS-Plugin>

## Superseded by this

- 2026-08-05 — deploying a separate site or worker for browser conversion is obsolete: v0.6.1 added the ESM browser API with an inline Web Worker.
- 2026-08-06 — integrations reading legacy Float32 opacityAccessor must move to sourceOpacityAccessor and coverageBoostRatioAccessor v2 or use the standard SPZ fallback.
- 2026-08-28 — prefer v0.6.3+ for new output: it always records colorSpace, VEC3 SH accessors, and required opacity/SH0 metadata.

## Still unknown

- Primary GitHub Releases and CHANGELOG end at v0.6.3, while the package index lists v0.6.4 and v0.6.5 on 2026-08-30 and 2026-08-31. Primary release notes for those two versions are unavailable, so we exclude their features from recommendations.
- GitHub Releases and CHANGELOG differ by one calendar day for v0.6.0 and v0.6.1; release timestamps lack a timezone. The timeline above uses the GitHub Release date and preserves the discrepancy.
- We could not independently read https://3dgs-ply-3dtiles-converter.vercel.app/, so its current features and alignment with the package and browser API remain unconfirmed.
- The Chinese search route yielded no primary Chinese-language source or reproducible operating report.
- Viewer compatibility lacks a confirmed matrix; only the companion renderer plugin has proven EXT_splat_opacity support.
- event_findings omitted from base schema?

## Sources

| source | title | read |
|---|---|---|
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter | GitHub — WilliamLiu-1997/3DGS-PLY-3DTiles-Converter | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/CHANGELOG.md | GitHub — 3DGS-PLY-3DTiles-Converter CHANGELOG.md | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/releases | GitHub — 3DGS-PLY-3DTiles-Converter Releases | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/Splat-Simplify.md | GitHub — Voxel-Based Gaussian Splat Simplification | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3D-Tiles-RendererJS-3DGS-Plugin | GitHub — 3D-Tiles-RendererJS-3DGS-Plugin | 2026-09-07 |
| https://greenflagged.dev/packages/3dgs-ply-3dtiles-converter | Greenflagged — 3dgs-ply-3dtiles-converter package history | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:3dgs-ply-3dtiles-converter`, thread `3dgs-ply-3dtiles-converter`, 1 dated events 2026-08-06 → 2026-08-06.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
