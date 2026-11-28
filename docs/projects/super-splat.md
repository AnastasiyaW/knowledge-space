---
title: "Super Splat: supersplat-snap — Supersplat Snap"
category: "projects"
date: 2026-09-28
tags: ["project", "super-splat", "supersplat-snap"]
aliases: ["Super Splat: supersplat-snap"]
---

# Super Splat: supersplat-snap — Supersplat Snap

**Development line:** project:super-splat · thread supersplat-snap  
**Last event:** 2026-09-28 · 1 dated since 2026-09-28 · **Researched:** 2026-11-28 · confidence: high

## What it is

Supersplat-snap is an MIT-licensed add-on tool for SuperSplat, the open-source 3D Gaussian Splat editor by PlayCanvas. It adds a point-correspondence alignment tool. You place matching control points across two or more splat files, and the tool computes the best-fit transform to align them. It is distributed as a patch applied to a separate SuperSplat clone, not as a fork.

## Development line

- **2026-09-28 — Supersplat-snap: Multi-scene alignment via control points in Gaussian splatting.** Introduces a tool for aligning multiple yf Gaussian scenes using paired control points, supporting secondary splat adjustment and iterative refinement with full undo support for .splat and .ply formats.
  - The README describes the tool as a patch on top of SuperSplat v2.27.3, not a fork. It uses the Umeyama similarity method \(rotation, translation and scale\) as a least-squares fit over all point pairs. Secondary splats \(B, C, D…\) align to Splat A. Points can be edited by dragging X/Y/Z values, and Shift gives fine steps while Alt gives coarse ones. Points travel with the splat after alignment, so alignment can be repeated. Ctrl\+Z undoes it, .splat and .ply files are supported, and 3\+ splats are supported. The panel shows a residual error after alignment. Four files are changed: a new src/tools/align-tool.ts \(about 400 lines\), plus modified src/camera.ts \(adds an intersectSplat\(\) method that picks depth on a specific splat only, which matters for overlapping splats\), src/main.ts, and src/ui/bottom-toolbar.ts. The repository is MIT-licensed and showed 28 stars and 1 fork when observed. (undated page) — <https://github.com/VFX-Soup/supersplat-snap>

## What changed

SuperSplat gains an Align tool, shown as a ⊕ icon in the bottom toolbar. It uses the Umeyama similarity method to compute rotation, translation and scale by least squares across all point pairs at once. Every secondary splat is aligned to Splat A, the first one you place points on. Points stay editable through X/Y/Z values. After alignment the points move with the splat, so you can re-align iteratively. The tool is fully undoable, works with .splat and .ply files, and supports three or more splats.

## How to use this

1. Install Node.js, then clone SuperSplat \(git clone https://github.com/playcanvas/supersplat.git\), enter the folder and run npm install. The README targets SuperSplat v2.27.3.
  — <https://github.com/VFX-Soup/supersplat-snap>
2. Clone the supersplat-snap repository and copy src/tools/align-tool.ts, src/camera.ts, src/main.ts and src/ui/bottom-toolbar.ts into the matching folders of the SuperSplat clone.
  — <https://github.com/VFX-Soup/supersplat-snap>
3. Run npm run develop in the SuperSplat folder, open http://localhost:3000 and hard-refresh \(Ctrl\+Shift\+R\).
  — <https://github.com/VFX-Soup/supersplat-snap>
4. Load two or more splat files through the SuperSplat Open menu and click the ⊕ \(Align\) icon in the bottom toolbar, which appears after the ruler/measure tool.
  — <https://github.com/VFX-Soup/supersplat-snap>
5. In the Scene Manager select Splat A \(the base/reference\) and click recognisable features in the viewport to place points A1, A2, A3…. Then select Splat B and click the matching features in the same order to place B1, B2, B3…. Repeat for any additional splats.
  — <https://github.com/VFX-Soup/supersplat-snap>
6. Click Align so B \(and C, D…\) transform to match A. Check the residual error in the panel. If it is high, add more points or adjust them with the X/Y/Z drag inputs, then export with SuperSplat's built-in export.
  — <https://github.com/VFX-Soup/supersplat-snap>

## Best practices

- Do not place all control points on a flat plane such as the ground. Three coplanar points cannot define a unique 3D rotation.
  — <https://github.com/VFX-Soup/supersplat-snap>
- Place points at different heights \(for example the top of a pole or structure, a ground point, the top of a bench or wall, a tree base versus a higher branch\). The more spread out they are in 3D, the more accurate the alignment; 4–6 well-distributed points is ideal.
  — <https://github.com/VFX-Soup/supersplat-snap>
- Place points on secondary splats in the same order as on Splat A, so that A1↔B1, A2↔B2 and so on correspond.
  — <https://github.com/VFX-Soup/supersplat-snap>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The README gives no release date or version number for supersplat-snap itself.
- Compatibility with SuperSplat versions other than v2.27.3 is not stated.
- The README's copy commands use inconsistent folder names \(supersplat-2.27.3 and supersplat\), so the correct path should be checked.
- The README does not state a numeric threshold for an acceptable residual error.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/VFX-Soup/supersplat-snap | GitHub - VFX-Soup/supersplat-snap: Snap align multiple splats with this additional tool for supersplat | 2026-09-28 |

## Agent brief {#agent-brief}

- **Subject:** project:super-splat, thread supersplat-snap, 1 dated events 2026-09-28 → 2026-09-28.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
