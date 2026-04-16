---
title: Flow Matching
category: architectures
tags: [flow-matching, rectified-flow, scheduler, sampling, diffusion, ode, cft, img2img, self-refinement, sana, flux]
aliases: ["Rectified Flow", "Flow Matching Scheduler"]
---

# Flow Matching

Generative modeling framework that learns **straight-line transport** between noise and data distributions. Replaces DDPM/DDIM schedulers in modern diffusion models. Used in FLUX, [[Step1X-Edit]], SD3, and most 2024-2026 models.

## Core Idea

### DDPM vs Flow Matching

**DDPM**: forward process adds Gaussian noise in T discrete steps. Reverse process learns to denoise step by step. Requires many steps (20-50+) because the denoising path is curved.

**Flow Matching**: learns a velocity field `v(x_t, t)` that transports samples along straight lines from noise `x_1` to data `x_0`. The ODE:

```sql
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

```text
p(x_t | x_0) = N((1-t)*x_0, t^2*I)   # Gaussian conditional path
```

This makes training tractable: sample `x_0` from data, sample `t ~ U(0,1)`, compute `x_t`, predict velocity. No need for optimal transport computation.

## Guidance

Classifier-free guidance works similarly to DDPM:

```toml
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
| DDPM | Score nabla log p(x_t) | SDE (stochastic) | 50-1000 |
| DDIM | Score (deterministic sampling) | ODE | 20-50 |
| Flow Matching | Velocity v(x_t, t) | ODE | 20-30 |
| Consistency Models | Direct x_0 prediction | Single-step | 1-4 |

## See Also

- [[SANA]] - efficient DiT using flow matching with linear attention
- [[flux-klein-9b-inference]] - FLUX flow matching model inference
- [[diffusion-lora-training]] - training with flow matching loss
- [[diffusion-inference-acceleration]] - sampling acceleration techniques

Flow matching sits in the sweet spot: simpler than DDPM, more flexible than consistency models, and competitive quality at moderate step counts.

## Flow Matching img2img

Unlike DDPM (add noise then denoise from intermediate step), flow matching img2img **interpolates along the ODE path**:

```python
# DDPM img2img: add noise to image, denoise from timestep t
# Flow matching img2img: interpolate between image latent and noise along ODE path

from diffusers import SanaSprintImg2ImgPipeline

pipe = SanaSprintImg2ImgPipeline.from_pretrained(
    "Efficient-Large-Model/Sana_Sprint_1.6B_1024px_diffusers",
    torch_dtype=torch.bfloat16
).to("cuda")

result = pipe(
    prompt="a detailed jewelry photo",
    image=input_image,
    strength=0.5,       # 0.0 = no change, 1.0 = full regeneration
    num_inference_steps=2,
    guidance_scale=4.5,
).images[0]
```

The `strength` parameter determines how far along the flow path to start. At 0.5: start halfway = moderate changes while preserving structure.

## Self-Refinement via Multi-Pass

DDPM models use a separate refiner model (SDXL refiner pattern). Flow matching models use **self-refinement** - the same model applied iteratively at decreasing strength:

```php
Pass 1: txt2img at 1024px -> base image
Pass 2: img2img on result, strength=0.3-0.4 -> refined details
Pass 3: img2img again, strength=0.2 -> final polish
```

Each pass partially re-noises along the flow path and re-solves. Low strength = mostly preserve structure, refine details. No separate refiner model exists for FLUX/SANA/SD3 because:
- Flow matching produces higher quality in fewer steps
- The ODE path is more direct than DDPM's stochastic path
- Consistency distillation achieves 1-step at high quality

## Iterative Flow Matching (Advanced)

Two academic approaches extend the self-refinement concept:
- **End-path correction**: fix the last portion of the ODE solution
- **Gradual refinement**: samples increasingly converge to target distribution

Not yet in production pipelines, but the multi-pass img2img approach achieves similar results in practice.

## Timestep Sampling: Logit-Normal

[[SANA]] and modern flow matching models use logit-normal timestep sampling during training:

```python
# Instead of uniform t ~ U(0, 1):
t = torch.sigmoid(mean + std * torch.randn(...))  # mean=0.0, std=1.0
```

This concentrates training signal on intermediate timesteps where the velocity field is hardest to predict, improving sample quality without extra compute.

## Flow Shift Parameter

Controls the noise schedule shape. [[SANA]] uses shift=3.0, which biases the schedule toward more denoising at later timesteps. Higher shift = more detail refinement in final steps.
