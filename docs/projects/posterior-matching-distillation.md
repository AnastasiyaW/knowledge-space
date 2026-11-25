---
title: "Posterior Matching Distillation: posterior-matching-distillation-release — Posterior Matching Distillation Release"
category: "projects"
date: 2026-11-23
tags: ["posterior-matching-distillation", "posterior-matching-distillation-release", "project"]
aliases: ["Posterior Matching Distillation: posterior-matching-distillation-release"]
---

# Posterior Matching Distillation: posterior-matching-distillation-release — Posterior Matching Distillation Release

Posterior Matching Distillation \(PMD\) distills diffusion and flow models into few-step stochastic students for ML practitioners.

**Development line:** project:posterior-matching-distillation · thread posterior-matching-distillation-release  
**Last event:** 2026-11-23 · 1 dated since 2026-11-23 · **Researched:** 2026-11-24 · confidence: high

## What it is

PMD is a distribution-matching distillation method for people who deploy diffusion and flow models in few-step inference pipelines. It replaces the mode-seeking reverse-KL objective with matching of conditional posterior distributions.

What it does:

- Distills pretrained multi-step diffusion and flow models into stochastic few-step students.
- Matches the sample means of exponentially tilted posteriors to the teacher's posterior means. It uses single evaluations on shifted inputs under Gaussian corruption.
- Drops the auxiliary student-score networks from distillation training.
- Generates diverse outputs at any step count within the trained timestep schedule.

Limits: training still needs teacher model evaluations, and the tilted mean identity relies on Gaussian corruption. In return PMD gives few-step acceleration without the mode collapse and loss of diversity typical of reverse-KL distillation.

## Development line

- **2026-11-23 — NVIDIA releases Posterior Matching Distillation for few-step diffusion.** PMD is an NVIDIA diffusion distillation method that matches full posterior distributions instead of using reverse-KL mode-seeking. It reports stochastic students that allow variable step counts within a trained schedule. It also reports the best FID among four-step methods on SDXL and FLUX.2 klein 4B, with code linked on GitHub.
  - NVIDIA and Virginia Tech researchers released it. They show that matching exponentially tilted posterior means under Gaussian noise recovers the full conditional posterior. This takes single teacher evaluations and no auxiliary score networks, and gives competitive four-step FID scores on SDXL and FLUX.2 klein 4B. (2026-11-23) — <https://pmd-distillation.github.io/>

## What changed

PMD replaces reverse-KL distribution matching in diffusion compression. Its stochastic students evaluate tilted posterior means without auxiliary score networks. The result is few-step inference on large text-to-image backbones.

## How to use this

1. Pick a pretrained diffusion or flow model as teacher. Configure the stochastic student to match teacher posterior means across the target timestep grid.
  — <https://pmd-distillation.github.io/>
2. Train the student by matching exponentially tilted sample averages to the teacher's conditional posterior means. Compute those means with single shifted evaluations under Gaussian corruption.
  — <https://pmd-distillation.github.io/>
3. Deploy the student for few-step sampling across the trained schedule. A new step budget does not need retraining.
  — <https://pmd-distillation.github.io/>

## Best practices

- Use four-step sampling on architectures such as SDXL and FLUX.2 klein 4B. It balances diversity against low FID.
  — <https://pmd-distillation.github.io/>
- Supervise the conditional distribution directly with the family of tilted mean constraints, so no auxiliary student score network is needed.
  — <https://pmd-distillation.github.io/>

## Superseded by this

- Reverse-KL divergence distillation objectives. They are mode-seeking and compress generation diversity in few-step students.
  — <https://pmd-distillation.github.io/>

## Still unknown

- Direct URLs for the arXiv preprint and the GitHub repository were not returned.
- No independent third-party benchmarks or practitioner discussions with verified, accessible links have turned up yet.

## Sources

| source | title | read |
|---|---|---|
| https://pmd-distillation.github.io/ | Posterior Matching Distillation | 2026-11-24 |

## Agent brief {#agent-brief}

- **Subject:** project:posterior-matching-distillation, thread posterior-matching-distillation-release, 1 dated events 2026-11-23 → 2026-11-23.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
