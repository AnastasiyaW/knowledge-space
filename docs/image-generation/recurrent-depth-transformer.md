---
title: Recurrent-Depth Transformer: Runtime Evidence Contract
description: "Recurrent-depth transformers reuse a version-specific shared block across iterations; bind the published architecture, checkpoint and runtime, recurrence budget, cache and termination behavior, and measured quality/cost, and do not infer latent reasoning, early exit, stability, or deployability from the family name."
category: techniques
tags: [recurrent-depth, transformers, recurrence, inference, evaluation, runtime, evidence]
aliases: ["Recurrent-Depth Transformer", "RDT Architecture", "Looped Transformer"]
---

# Recurrent-Depth Transformer: Runtime Evidence Contract

Recurrent-depth transformer is a family name, not a standardized checkpoint or
serving interface. The defining idea is reuse of a shared computation across
iterations, but the placement of blocks, input injection, gating, cache
layout, stop condition, training procedure, and supported recurrence depths
belong to a specific implementation.

## Bind the architecture before discussing it

One published layout can be summarized as:

`input → prelude → shared recurrent core repeated r times → coda → logits`

[Scaling up Test-Time Compute with Latent Reasoning](https://arxiv.org/abs/2502.05171)
describes a prelude/shared-core/coda design. A newer
[Gated Recurrent Transformers paper](https://arxiv.org/abs/2608.15062) demonstrates a different
gated recurrent design. Neither source proves that every “RDT” model has the
same update rule, adapters, mixture-of-experts layers, attention mechanism,
stability constraint, or early-exit behavior.

For a concrete release, retain:

- paper/code release, checkpoint digest, license, tokenizer, precision,
  runtime/backend, and any non-default patches;
- exact prelude/core/coda composition, whether core weights are tied, input
  injection/gating policy, and supported recurrence values;
- cache format, batching policy, determinism, termination/early-exit
  implementation, error behavior, and source of the chosen recurrence budget;
- evaluation corpus/split, prompt/template policy, quality metrics, safety
  tests, and baseline; and
- measured latency, memory, throughput, and output changes at each released
  recurrence setting on the deployed hardware.

## Treat recurrence as a measured control

More iterations add computation but do not universally improve every task.
Changing `r` can change quality, latency, memory pressure, batch packing, and
the distribution of failures. A deployment may expose only the depth values it
was trained and tested to support. Do not extrapolate an arbitrary loop count
from a paper diagram or assume that a shared core is stable beyond the
documented runtime range.

Compare recurrence settings on a source-disjoint evaluation set and record the
complete quality/cost curve. Report failures, not only the best point. If
early exit is claimed, evaluate its exit decision and final outputs against
the full-depth baseline for the named release; do not infer it from recurrent
weight sharing.

## Do not overstate latent computation

Repeated hidden-state updates are not a visible chain of thought, an
explanation, a proof of reasoning, or an inspection interface. Do not claim
that latent steps are equivalent to a number of written reasoning steps,
that their contents are interpretable, or that hidden computation makes a
model safe. Evaluate outputs and declared controls directly.

## Serving boundary

Only deploy a recurrent-depth model after the actual runtime can load the
named artifact, preserve the requested recurrence/cache behavior, and produce
the measured outputs under workload. A generic transformer server, quantized
checkpoint, or adapter loader is not assumed compatible. Surface a failure if
the recurrence budget, cache policy, or artifact identity cannot be verified;
never silently run a dense substitute or an unspecified depth.

## Related pages

- [[low-vram-inference-strategies]]
- [[tiled-inference]]
- [[diffusion-lora-training]]
