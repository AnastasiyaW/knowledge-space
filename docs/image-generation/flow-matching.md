---
title: Flow Matching: Conditional Vector-Field Training
description: Flow matching trains a continuous vector field along a chosen probability path; scheduler, path, and inference settings are checkpoint-specific rather than universal diffusion defaults.
category: architectures
tags: [flow-matching, conditional-flow-matching, scheduler, sampling, continuous-normalizing-flow, ode]
aliases: ["Flow Matching", "Rectified Flow", "Flow Matching Scheduler"]
---

# Flow Matching: Conditional Vector-Field Training

[Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)
defines a simulation-free way to train continuous normalizing flows (CNFs).
Instead of requiring simulation of the learned flow during training, the model
regresses a vector field on a chosen family of conditional probability paths.

The path matters. The original formulation can cover diffusion paths and
optimal-transport-style paths; it is not a single universal straight-line
interpolation or one fixed equation for every checkpoint.

## What inference integrates

At inference, a compatible pipeline starts from its configured source
distribution and numerically integrates the learned vector field toward a
sample. The solver, time schedule, conditioning, guidance, and number of
function evaluations are part of that pipeline/model contract.

Do not infer that every flow-matching checkpoint:

- accepts the same scheduler class or schedule shift;
- improves at a particular number of steps;
- supports a particular img2img strength mapping; or
- can safely refine its own output in repeated passes.

Those claims need evidence from the checkpoint publisher and a result on the
intended task.

## Scheduler compatibility

Diffusers provides
[FlowMatchEulerDiscreteScheduler](https://huggingface.co/docs/diffusers/api/schedulers/flow_match_euler_discrete)
as one implementation. Its exposed configuration includes training timesteps,
shift behavior, dynamic shifting, sequence-length settings, and alternative
sigma schedules. These options describe an implementation interface; they are
not universal defaults to copy into another flow model.

Load the scheduler and configuration published with the checkpoint whenever
possible. If an experiment changes the scheduler, shift, solver, or step
schedule, treat it as a new sampling contract and retain a reproducible result
before using it operationally.

## Evaluation protocol

For each supported model/pipeline pair:

1. record checkpoint, pipeline and scheduler revisions, input fixture, seed,
   dimensions, guidance, steps, and device/runtime;
2. make a small supported grid of step counts or schedule settings;
3. compare output determinism, task-relevant fidelity, artifacts, and latency;
4. review img2img or editing preservation separately from text-to-image
   quality; and
5. publish the selected configuration with its validation fixture and known
   limits.

This is especially important for restoration and editing: an image can look
more polished while drifting from the source, changing text, or altering a
material property that must be preserved.

## Related pages

- [[diffusion-inference-acceleration]]
- [[SANA]]
- [[flux-klein-9b-inference]]
- [[diffusion-lora-training]]
