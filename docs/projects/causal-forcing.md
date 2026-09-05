---
title: Causal Forcing++
category: projects
date: 2026-05-16
tags: [causal-forcing, causal_forcing, project]
aliases: ["Causal Forcing++"]
---

# Causal Forcing++

**Development line:** `project:causal-forcing` · thread `causal-forcing`  
**Last event:** 2026-05-16 · 1 dated since 2026-05-16 · **Researched:** 2026-09-05 · confidence: high

## What it is

Causal Forcing++ is a research pipeline and frame-wise checkpoints for low-latency text-to-video and image-to-video generation. It replaces precomputed causal-ODE trajectories with causal consistency distillation before asymmetric DMD. The reference implementation provides 1-step and 2-step frame-wise models. The paper reports gains over 4-step chunk-wise Causal Forcing, but those are benchmark results rather than a general production guarantee.

## Development line

- **2026-05-16 — Causal Forcing++ public project resources were recorded.** On 2026-05-16, we recorded the Causal Forcing++ development line with links to a project site, source repository, and Hugging Face repository. The supplied links establish a public project-resource milestone, but do not establish a specific version, technical result, or usage workflow.

## What changed

2026-05-16 — Causal Forcing++ was available with causal consistency distillation and open 1-step and 2-step frame-wise checkpoints. The repository dated history places the release on 2026-05-15. The authors submitted paper v1 on 2026-05-14.

## How to use this

From 2026-05-16, practitioners can evaluate Causal Forcing++ through its linked project, source, and model-resource locations. The dated evidence alone does not justify a specific implementation or performance recommendation.

1. Create the Python 3.10 environment, install the project requirements, CLIP, FlashAttention, and the package in development mode.
  — <https://github.com/thu-ml/Causal-Forcing>
2. Download a Wan2.1 base model plus either `causal-forcing++/framewise-1step.pt` or `framewise-2step.pt` from the published model repository.
  — <https://github.com/thu-ml/Causal-Forcing>
3. Run `inference.py` with the matching 1-step or 2-step frame-wise configuration and `--use_ema`. Use the frame-wise path with an initial image condition for I2V.
  — <https://github.com/thu-ml/Causal-Forcing>

## Best practices

- Use the released checkpoints for inference before attempting the three-stage training pipeline.
  — <https://github.com/thu-ml/Causal-Forcing>
- For training, switch from BF16 to FP32 if causal-CD or DMD training collapses or outputs remain blurry.
  — <https://github.com/thu-ml/Causal-Forcing>
- Do not treat the native model as a long-video generator beyond 81 frames. Use the documented Rolling Forcing extension for minute-scale generation.
  — <https://github.com/thu-ml/Causal-Forcing>

## Superseded by this

- 2026-05-15 — The Causal Forcing++ route supersedes the causal-ODE Stage 2 route for few-step initialization without generating and storing ODE-paired trajectories.
- 2026-05-15 — 1-step and 2-step frame-wise checkpoints supersede the assumption that Causal Forcing is only a 4-step chunk-wise model.

## Still unknown

- The available response schema has no `event_findings` or `new_events` fields. The dated correction and release scope are therefore recorded in `what_changed` and `supersedes`.
- The official materials describe a research implementation and checkpoints. We verified no maintained production deployment guide or hardware requirement for the released Causal Forcing++ checkpoints.

## Sources

| source | title | read |
|---|---|---|
| https://thu-ml.github.io/CausalForcing.github.io/ | Causal Forcing project page | 2026-09-05 |
| https://github.com/thu-ml/Causal-Forcing | thu-ml/Causal-Forcing official repository and README | 2026-09-05 |
| https://github.com/thu-ml/Causal-Forcing/commits/main | Causal-Forcing commit history | 2026-09-05 |
| https://huggingface.co/zhuhz22/Causal-Forcing/tree/main | zhuhz22/Causal-Forcing model files | 2026-09-05 |
| https://arxiv.org/abs/2605.15141 | Causal Forcing++: Scalable Few-Step Autoregressive Diffusion Distillation for Real-Time Interactive Video Generation | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:causal-forcing`, thread `causal-forcing`, 1 dated events 2026-05-16 → 2026-05-16.
- **Practical note:** From 2026-05-16, practitioners can evaluate Causal Forcing++ through its linked project, source, and model-resource locations. The dated evidence alone does not justify a specific implementation or performance recommendation.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
