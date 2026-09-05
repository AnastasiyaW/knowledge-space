---
title: LUNA
category: projects

tags: [luna, luna-development, project]
aliases: ["LUNA"]
---

# LUNA

**Development line:** `project:luna` · thread `luna-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

LUNA is a research model for generating animatable 3D human avatars from unposed images. It replaces Linear Blend Skinning with direct 3D Gaussian transformation.

- 3D avatar synthesis: builds an animatable human avatar from N=4 unposed images.
- Multi-signal driving: controls motion from RGB video, keypoints, or a sketch.
- Direct transformation: deforms 3D Gaussians without Linear Blend Skinning.

The public page shows demo results without code, weights, or runnable instructions, so this is material to evaluate rather than a ready tool.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-01 — LUNA: Learning Universal 3D Human Animation Beyond Skinning presented, an LBS-free model for 3D Gaussian animation from multiple 2D control signals.

## How to use this

As of 2026-07-01, treat the linked LUNA site as an unreviewed discovery lead, not as verified project-development history, until the linked material and original post are researched.

1. Verify the required input: four unposed images of one subject and one 2D driving signal; RGB, keypoints, and sketch are supported.
  — <https://penghtyx.github.io/LUNA/>
2. Use the project page and paper to evaluate the method and results before planning integration; check for official code, weights, and license release first.
  — <https://arxiv.org/abs/2606.31981>

## Best practices

- Test demo results on your own subjects, clothing, camera angles, and driving signals before moving to production.
  — <https://penghtyx.github.io/LUNA/>
- Maintain the N=4 limit: the published pipeline reconstructs canonical 3D Gaussians specifically from four multi-view images.
  — <https://penghtyx.github.io/LUNA/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The public page links no official repository, weights, license, hardware requirements, or reproduction guide; we found no confirmation that these assets are published.
- Changes in arXiv v2 from 2026-09-01 remain unknown: metadata confirms the new version without a changelog.

## Sources

| source | title | read |
|---|---|---|
| https://penghtyx.github.io/LUNA/ | LUNA: Learning Universal 3D Human Animation Beyond Skinning | 2026-09-05 |
| https://arxiv.org/abs/2606.31981 | LUNA: Learning Universal 3D Human Animation Beyond Skinning | 2026-09-05 |
| https://rawalkhirodkar.github.io/ | Rawal Khirodkar — Publications | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:luna`, thread `luna-development`, 0 dated events - → -.
- **Practical note:** As of 2026-07-01, treat the linked LUNA site as an unreviewed discovery lead, not as verified project-development history, until the linked material and original post are researched.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.