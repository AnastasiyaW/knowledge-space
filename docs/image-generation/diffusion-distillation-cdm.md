---
title: "Continuous-Time Distribution Matching: Research Distillation Contract"
description: "Continuous-Time Distribution Matching (CDM) is a research method for few-step diffusion distillation, not a drop-in speed switch; bind the paper/code/checkpoint and license, teacher/student parameterization and schedule, training/distributed runtime, source-disjoint quality/diversity/preservation evaluation, and rollback-ready serving evidence before use."
category: optimization
tags: [cdm, diffusion-distillation, flow-matching, evaluation, serving, reproducibility]
aliases: ["CDM Diffusion Distillation", "Continuous-Time Distribution Matching Distillation"]
---

# Continuous-Time Distribution Matching: Research Distillation Contract

[Continuous-Time Distribution Matching](https://arxiv.org/abs/2605.06376)
is a research method for few-step diffusion distillation. The paper describes
continuous-time distribution matching for the named experimental
architectures, and links to code. It is evidence for reproducing or extending
that release under its conditions, not a drop-in promise of a specific step
count, speedup, quality level, GPU topology, or compatibility with another
teacher.

## Bind teacher, student, and trajectory

For every experiment, retain:

- paper version, code commit, checkpoint/artifact identifiers and digests,
  license/access terms, framework/dependency revisions, and distributed
  runtime/hardware record;
- teacher and student parameterization, conditioning path, prediction target,
  noise/trajectory schedule, loss branches/weights, data pipeline, seeds, and
  checkpoint/resume policy;
- a source-disjoint evaluation set with task quality, diversity, non-target
  preservation, safety/rights, reproducibility, and failure measurements;
- comparable baseline runs using the same prompt/input distribution, output
  resolution, inference environment, warm/steady-state latency, throughput,
  memory, and error policy; and
- serving artifact/version, rollback target, output provenance, monitoring,
  and release decision.

Changing the teacher, base architecture, scheduler, conditioning contract, or
distributed implementation changes the distillation problem. Do not inherit
an adapter interface, schedule, loss branch, or published result from a
different model family without an explicit implementation and measured
validation.

## Evaluate acceleration separately from output trust

Few-step output must be compared with the declared teacher and baseline for
the requested task. Report speed/cost separately from fidelity, diversity,
text/geometry preservation, and artifact rate. A visually attractive sample
cannot prove that a student preserves source facts, behaves consistently on a
new prompt distribution, or is safe to serve.

Keep checkpoints and output lineage sufficient to rerun a failed evaluation
or roll back a deployed student. A training run that stops early, loses
provenance, or cannot reproduce its evaluation remains incomplete.

## Failure boundary

If the teacher/student contract, code/artifacts, licensing, source-disjoint
evaluation, or rollback path is missing, keep CDM in research state. Do not
substitute a different distillation method, publish an unmeasured checkpoint,
or advertise a faster sampler as an equivalent CDM result.

## Related pages

- [[flow-matching]]
- [[diffusion-inference-acceleration]]
- [[MMDiT]]
- [[diffusion-lora-training]]
