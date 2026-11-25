---
title: Glob3R
category: projects

tags: [glob3r, project]
aliases: ["Glob3R"]
---

# Glob3R

**Development line:** `project:glob3r` · thread `glob3r`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

Glob3R is an offline global Structure-from-Motion pipeline that links frozen Pi3X 3D model predictions with dense matching, tracks, motion averaging, and bundle adjustment.

- Ordered and unordered image sets: processes both sequences and unordered image collections.
- Geometry refinement: refines camera poses and dense geometry together.
- Pipeline role: designed for offline reconstruction rather than an end-user product.

The official repository contains only a README; inference code and evaluation script are marked TODO. We can evaluate the method from the paper, but we cannot reproducibly deploy it from the official repository today.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-16 — Glob3R appeared as a global SfM pipeline: local Pi3X predictions turn into multi-view tracks and optimize globally.

## How to use this

As of 2026-07-16, use the linked Glob3R project page only as a starting point for primary-source verification; the dated link alone supports no implementation or workflow change.

1. Do not plan a production or research run from the official repository: it lacks inference code, evaluation script, weights, and launch instructions.
  — <https://github.com/aigc3d/Glob3R>
2. Use the paper to evaluate the approach: feed an image sequence or build a retrieval-based pseudo-sequence for an unordered set; the method then uses overlapping windows, keyframes, tracks, and global optimization.
  — <https://arxiv.org/html/2607.09225>

## Best practices

- Build a pseudo-sequence through image retrieval first for unordered images; preserve the frame order for an existing sequence.
  — <https://arxiv.org/html/2607.09225>
- Do not replace global optimization with simple window stitching: keyframes and window overlap are needed to link poses and tracks across windows.
  — <https://arxiv.org/html/2607.09225>
- Treat the paper results as a research baseline until code and evaluation script are published.
  — <https://github.com/aigc3d/Glob3R>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Official project and repository dates do not appear on the pages themselves; for the 2026-07-16 event, only project page availability on that date is confirmed.
- Official inference code, weights, license, system requirements, and reproducible launch commands are not published as of 2026-09-05.

## Sources

| source | title | read |
|---|---|---|
| https://junyuandeng.github.io/Glob3r/ | Glob3R | Global Structure-from-Motion with 3D Foundation Models | 2026-09-05 |
| https://arxiv.org/abs/2607.09225 | Glob3R: Global Structure-from-Motion with 3D Foundation Models | 2026-09-05 |
| https://arxiv.org/html/2607.09225 | Glob3R: Global Structure-from-Motion with 3D Foundation Models | 2026-09-05 |
| https://github.com/aigc3d/Glob3R | aigc3d/Glob3R | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:glob3r`, thread `glob3r`, 0 dated events - → -.
- **Practical note:** As of 2026-07-16, use the linked Glob3R project page only as a starting point for primary-source verification; the dated link alone supports no implementation or workflow change.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
