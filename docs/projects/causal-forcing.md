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

Causal Forcing++ is a research pipeline and frame-wise model release for low-latency text-to-video and image-to-video generation.

- Causal consistency distillation: replaces precomputed causal-ODE trajectories before asymmetric DMD.
- Reference checkpoints: provides 1-step and 2-step frame-wise models.
- Benchmark gains: outpaces 4-step chunk-wise Causal Forcing in paper benchmarks, but not as a production guarantee.

## Development line

- **2026-05-16 — Causal Forcing++ public project resources were recorded.** On 2026-05-16, we recorded project links to the site, source repository, and Hugging Face repository. The links mark public project resources, but confirm no specific version, technical result, or usage workflow.

## What changed

2026-05-16 — Causal Forcing++ shipped causal consistency distillation with open 1-step and 2-step frame-wise checkpoints. Repository history dates the release to 2026-05-15, after paper v1 was submitted on 2026-05-14.

## How to use this

From 2026-05-16, practitioners can evaluate Causal Forcing++ through linked project, source, and model locations. The dated record alone warrants no specific deployment or performance claims.

1. Create a Python 3.10 environment, then install requirements, CLIP, FlashAttention, and the package in editable mode.
  — <https://github.com/thu-ml/Causal-Forcing>
2. Download a Wan2.1 base model and either `causal-forcing++/framewise-1step.pt` or `framewise-2step.pt` from the model repository.
  — <https://github.com/thu-ml/Causal-Forcing>
3. Run `inference.py` with matching 1-step or 2-step frame-wise configs and `--use_ema`. Use the frame-wise path with an initial image for I2V.
  — <https://github.com/thu-ml/Causal-Forcing>

## Best practices

- Test inference with the released checkpoints before running the three-stage training pipeline.
  — <https://github.com/thu-ml/Causal-Forcing>
- Switch training from BF16 to FP32 if causal-CD or DMD diverges or leaves frames blurry.
  — <https://github.com/thu-ml/Causal-Forcing>
- Do not use the base model past 81 frames; run Rolling Forcing for minute-scale video.
  — <https://github.com/thu-ml/Causal-Forcing>

## Superseded by this

- 2026-05-15 — Causal Forcing++ replaces the causal-ODE Stage 2 step when initializing few-step models without saving paired ODE trajectories.
- 2026-05-15 — 1-step and 2-step frame-wise checkpoints replace the premise that Causal Forcing runs only as a 4-step chunk-wise model.

## Still unknown

- Separate event logs and structured event feeds are not provided for the release.
- Official documentation covers only the research code and checkpoints, with no verified production deployment guides or hardware requirements.

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
- **Practical note:** From 2026-05-16, practitioners can evaluate Causal Forcing++ through linked project, source, and model locations; the dated record alone justifies no specific implementation or performance claims.
- **Confidence:** high. Dated supersedes above mark what is obsolete.