---
title: TAPTR
category: projects
date: 2024-12-13
tags: [project, taptr, taptr-public-availability]
aliases: ["TAPTR"]
---

# TAPTR

**Development line:** `project:taptr` · thread `taptr-public-availability`  
**Last event:** 2024-12-13 · 2 dated since 2024-08-01 · **Researched:** 2026-09-04 · confidence: high

## What it is

TAPTR is a transformer approach to Tracking Any Point for developers building video tools, 3D reconstruction, and mask tracking.

- Point and region input: accepts points or a bounding region in a frame.
- Trajectory tracking: returns point trajectories and visibility flags across video.
- Spatiotemporal context: TAPTRv3 adds spatial and temporal context with recovery across shot cuts.

The older demo Space from the original selection is stopped.
Use official code for the version you need rather than this demo Space.

## Development line

- **2024-08-01 — TAPTR project resources and task-specific demos were linked.** On 2024-08-01, an update linked the project website, source repository, and online demonstrations for video editing and trajectory tracking.
- **2024-12-13 — A TAPTR Hugging Face Space was linked.** On 2024-12-13, an update linked a Hugging Face Space named TAPTR alongside a source reference as a hosted access point.

## What changed

- 2024-08-01 — TAPTRv1 was available as an open DETR-like implementation for point tracking; official code was released 2024-07-16.
- 2024-12-13 — A third-party Hugging Face Space appeared for TAPTR rather than an official model release; by review time the Space is stopped.
- 2026-02-10 — Code for TAPTRv3 was published as the current version for long videos.

## How to use this

From 2024-08-01, practitioners could locate TAPTR public source and task-specific demos through project links; from 2024-12-13, they could also evaluate the linked Hugging Face Space after verifying its ownership and version.

1. Open the official repository and select v1, v2, or v3; for new long video tasks, start with v3.
  — <https://github.com/IDEA-Research/TAPTR>
2. Follow the README for your version, feed points or a sampled region in the initial frame, and save predicted coordinates with visibility flags.
  — <https://github.com/IDEA-Research/TAPTR>
3. For video editing, sample points inside the edit region and use their trajectories to transfer the region across frames.
  — <https://arxiv.org/abs/2407.16291>

## Best practices

- Pick TAPTRv3 for long clips and shot cuts: it uses Visibility-aware Long-Temporal Attention, Context-aware Cross Attention, and global matching when detecting cuts.
  — <https://taptr.github.io/>
- Do not build workflows around the HYeungLee/TAPTR Space: it is stopped at review time.
  — <https://huggingface.co/spaces/HYeungLee/TAPTR>
- Do not use TAPTRv2 as the default for long videos: the authors note unsatisfactory performance for v2 at length.
  — <https://github.com/IDEA-Research/TAPTR>

## Superseded by this

- 2024-07-24 — TAPTRv2 replaced the cost volume in TAPTRv1 with Attention-based Position Update; choosing v1 for peak quality is obsolete.
- 2024-11-27 / 2026-02-10 — TAPTRv3 supersedes v2 for long videos: v2 used RNN-like modeling and struggled with feature extraction over long sequences; v3 code was published 2026-02-10.

## Still unknown

- Exact install commands and version tag names in the official repository remain unconfirmed from GitHub; check the README for your version before deployment.
- The Hugging Face Space from the 2024-12-13 event is a third-party demonstration, not a verified official TAPTR interface.
- Two entries belong to the TAPTR family, but the first is the v1 release and demos while the second is a third-party Space; they are distinct event types, not two model releases.
- Original source links were not used as evidence because message text is unavailable.
- The TAPTRv3 paper appeared 2024-11-27, but official code was released only on 2026-02-10; before that date it was not an accessible implementation.
- Current benchmark metrics for v3 were not aggregated: sources claim competitive state of the art, but dataset selection requires reproducible evaluation.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/IDEA-Research/TAPTR | IDEA-Research/TAPTR — official implementation and release timeline | 2026-09-05 |
| https://taptr.github.io/ | TAPTR project page — v1 to v3 overview | 2026-09-05 |
| https://huggingface.co/spaces/HYeungLee/TAPTR | HYeungLee/TAPTR Hugging Face Space | 2026-09-05 |
| https://arxiv.org/abs/2407.16291 | TAPTRv2: Attention-based Position Update Improves Tracking Any Point | 2026-09-05 |
| https://arxiv.org/abs/2411.18671 | TAPTRv3: Spatial and Temporal Context Foster Robust Tracking of Any Point in Long Video | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:taptr`, thread `taptr-public-availability`, 2 dated events 2024-08-01 → 2024-12-13.
- **Practical note:** From 2024-08-01, practitioners could locate TAPTR's public source and task-specific demos through its project links; from 2024-12-13, they could also evaluate the linked Hugging Face Space, while first verifying its ownership and version.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
