---
title: Flow Matching
category: architectures
tags: [flow-matching, rectified-flow, scheduler, sampling, diffusion, ode, cft]
aliases: ["Rectified Flow", "Flow Matching Scheduler"]
---

# Flow Matching

Generative modeling framework that learns **straight-line transport** between noise and data distributions. Replaces DDPM/DDIM schedulers in modern diffusion models. Used in FLUX, [[Step1X-Edit]], SD3, and most 2024-2026 models.

## Core Idea

### DDPM vs Flow Matching

**DDPM**: forward process adds Gaussian noise in T discrete steps. Reverse process learns to denoise step by step. Requires many steps (20-50+) because the denoising path is curved.

**Flow Matching**: learns a velocity field `v(x_t, t)` that transports samples along straight lines from noise `x_1` to data `x_0`. The ODE:

```
dx/dt = v(x_t, t)
x_t = (1-t) * x_0 + t * epsilon    # linear interpolation
v_target = epsilon - x_0             # velocity = direction from data to noise
```

Training objective: predict the velocity `v(x_t, t)` at each point along the straight path. Simpler than score matching, more stable gradients.

### Why Straight Lines Matter

Curved paths (DDPM) require many discretization steps to follow accurately. Straight paths (flow matching) can be traversed in fewer steps with minimal discretization error. Practical impact:

| Scheduler | Typical steps | Quality at 10 steps |
|-----------|--------------|---------------------|
| DDPM | 50-1000 | Poor |
| DDIM | 20-50 | Acceptable |
| Flow Matching | 20-30 | Good |
| Distilled FM | 1-4 | Good (with distillation) |

## Implementation in Step1X-Edit

[[Step1X-Edit]] uses `RealRestorerFlowMatchScheduler` (variant of `FlowMatchEulerDiscreteScheduler`):

```python
# Default inference config
num_inference_steps = 28
guidance_scale = 3.0
# Euler method ODE solver (simplest, sufficient for straight paths)
```

The scheduler:
1. Samples timesteps uniformly in [0, 1]
2. Computes `x_t = (1-t) * x_0 + t * noise` during training
3. At inference, starts from `x_1 = noise` and integrates backward using predicted velocity
4. Euler steps: `x_{t-dt} = x_t - dt * v(x_t, t)`

## Conditional Flow Matching (CFM)

Standard flow matching requires knowing the full transport map. CFM relaxes this — condition on individual data points:

```
p(x_t | x_0) = N((1-t)*x_0, t^2*I)   # Gaussian conditional path
```

This makes training tractable: sample `x_0` from data, sample `t ~ U(0,1)`, compute `x_t`, predict velocity. No need for optimal transport computation.

## Guidance

Classifier-free guidance works similarly to DDPM:

```
v_guided = v_uncond + guidance_scale * (v_cond - v_uncond)
```

[[Step1X-Edit]] default guidance_scale=3.0 (lower than typical DDPM models which use 7.5+). Flow matching needs less guidance because paths are straighter.

## Distillation

Flow matching is particularly amenable to progressive distillation:
- Teacher: 28 steps → Student: 4 steps (with minimal quality loss)
- Consistency distillation maps all points on the flow to the same endpoint
- FLUX.1-schnell demonstrates 4-step flow matching inference

## Relation to Other Approaches

| Method | What it learns | ODE/SDE | Steps needed |
|--------|---------------|---------|-------------|
| DDPM | Score ∇log p(x_t) | SDE (stochastic) | 50-1000 |
| DDIM | Score (deterministic sampling) | ODE | 20-50 |
| Flow Matching | Velocity v(x_t, t) | ODE | 20-30 |
| Consistency Models | Direct x_0 prediction | Single-step | 1-4 |

Flow matching sits in the sweet spot: simpler than DDPM, more flexible than consistency models, and competitive quality at moderate step counts.
