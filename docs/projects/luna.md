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

LUNA is a research model for generating animatable 3D human avatars from N=4 unposed images and a driving signal.

- 3D Gaussian representation: replaces Linear Blend Skinning with direct transformation.
- 2D driving control: animates the avatar using RGB video, keypoints, or a sketch.

The public page displays visual outputs, but provides no code, weights, or reproducible setup. It is material for research evaluation, not a finished tool.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-01 — LUNA: Learning Universal 3D Human Animation Beyond Skinning introduced an LBS-free model for 3D Gaussian animation using multiple 2D control types.

## How to use this

As of 2026-07-01, treat the linked LUNA site as an unreviewed discovery lead, not as verified project-development history, until the linked material and original post are researched.

1. Verify the required input: N=4 unposed images of one subject and one 2D driving signal across RGB, keypoints, or sketch.
  — <https://penghtyx.github.io/LUNA/>
2. Use the project page and paper to evaluate the method and results; check for official code, weights, and licensing before planning integration.
  — <https://arxiv.org/abs/2606.31981>

## Best practices

- Do not transfer demo results to production without local testing across target subjects, clothing, camera angles, and driving signals.
  — <https://penghtyx.github.io/LUNA/>
- Keep the N=4 limit: the published pipeline reconstructs canonical 3D Gaussians specifically from 4 multi-view images.
  — <https://penghtyx.github.io/LUNA/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The public page links no official repository, model weights, license, hardware requirements, or run instructions; current sources cannot confirm whether these materials are released.
- Substantive changes in arXiv v2 from 2026-09-01 remain unverified: metadata confirms the update, but provides no changelog.

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