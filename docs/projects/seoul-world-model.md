---
title: Seoul World Model — Public project release
category: projects
date: 2026-03-17
tags: [project, public-project-release, seoul-world-model]
aliases: ["Seoul World Model"]
---

# Seoul World Model — Public project release

**Development line:** `project:seoul-world-model` · thread `public-project-release`  
**Last event:** 2026-03-17 · 1 dated since 2026-03-17 · **Researched:** 2026-09-05 · confidence: high

## What it is

Seoul World Model (SWM) is a research world model. It generates route video from coordinates, camera trajectories, and text scripts by retrieving Seoul street-view imagery from a spatial index.

- Retrieval-augmented conditioning preserves place geometry and visual appearance.
- Free camera motion supports arbitrary trajectories and text scene modifications.
- Virtual Lookahead Sink re-anchors video generation to upcoming route waypoints.

As of 2026-09-05, weights, inference code, synthetic data, and interpolation code remain unreleased, so we cannot deploy it.

## Development line

- **2026-03-17 — Seoul World Model public project and code references recorded.** On 2026-03-17, the project published links to a public project website and a GitHub repository, establishing its official presentation page and source repository.

## What changed

2026-03-17 — Seoul World Model launched as the official project for Grounding World Simulation Models in a Real-World Metropolis. The repository announced future publication of weights, inference code, synthetic data, and training video preparation tools.

Addition to 2026-03-17 event: the preprint from 2026-03-16 names the system Seoul World Model (SWM) and describes it as fine-tuning on a pretrained video-world model. It specifies training data of 440 thousand Seoul street-view images, real driving videos, and synthetic urban data.
  — <https://arxiv.org/abs/2603.15583>

New event 2026-03-16: authors published the preprint Grounding World Simulation Models in a Real-World Metropolis. The paper defines the core method: georeferenced retrieval, cross-temporal pairing, synthetic trajectories, and Virtual Lookahead Sink.
  — <https://arxiv.org/abs/2603.15583>

## How to use this

From 2026-03-17, use the Seoul World Model project website and linked GitHub repository to evaluate the project instead of unverified reposts.

1. Check the official repository before planning experiments: it currently provides no model downloads or inference instructions.
  — <https://github.com/naver-ai/seoul-world-model>
2. Use the project page and paper as research reproduction specifications: system inputs are initial geographic position, camera trajectory, text prompt, and local street-view references.
  — <https://seoul-world-model.github.io/>
3. Do not claim reproducibility or production readiness until authors release weights, inference code, and data.
  — <https://github.com/naver-ai/seoul-world-model>

## Best practices

- Measure location grounding separately from visual realism: in ablations, fewer reference images reduced mPSNR even when FID and FVD showed no clear degradation.
  — <https://arxiv.org/abs/2603.15583>
- Retrieve forward references along the trajectory for long routes instead of relying only on the initial frame: this follows the Virtual Lookahead Sink method from the paper.
  — <https://arxiv.org/abs/2603.15583>
- Do not treat an expected release as an available tool: the repository still notes that weights and code will arrive later.
  — <https://github.com/naver-ai/seoul-world-model>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The official repository contains only a README and no GitHub Releases. The authors have not announced release dates for weights, inference code, synthetic data, or interpolation code.
- Dataset numbers conflict across sources. The project page cites 1,2 million panoramas and 10 thousand synthetic videos, while the paper specifies 440 thousand street-view images for fine-tuning. The authors have not published the prepared dataset or exact training configurations.

## Sources

| source | title | read |
|---|---|---|
| https://seoul-world-model.github.io/ | Seoul World Model: Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model | naver-ai/seoul-world-model | 2026-09-05 |
| https://github.com/naver-ai/seoul-world-model/releases | Releases · naver-ai/seoul-world-model | 2026-09-05 |
| https://arxiv.org/abs/2603.15583 | Grounding World Simulation Models in a Real-World Metropolis | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:seoul-world-model`, thread `public-project-release`, 1 dated events 2026-03-17 → 2026-03-17.
- **Practical note:** From 2026-03-17, practitioners should use the Seoul World Model project website together with its linked GitHub repository as the starting point for evaluating and obtaining the project, rather than relying on an unverified repost.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
