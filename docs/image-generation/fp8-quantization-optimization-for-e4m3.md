---
title: FP8 E4M3: Measured Quantization Contract
description: "FP8 E4M3 quantization is a release- and backend-specific numerical contract; bind the tensor format, scaling recipe, supported operations and hardware, calibration or amax evidence, serialization/runtime path, and quality/latency/memory measurements, and never substitute clipping or another format silently."
category: optimization
tags: [fp8, e4m3, quantization, transformer-engine, inference, measurement]
aliases: ["FP8 Quantization Optimization for E4M3", "E4M3 Quantization"]
---

# FP8 E4M3: Measured Quantization Contract

FP8 is not one interchangeable optimization switch. The
[Transformer Engine current-scaling documentation](https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/features/low_precision_training/fp8_current_scaling/fp8_current_scaling.html)
describes E4M3 as an FP8 format with one sign bit, four exponent bits, three
mantissa bits, finite values up to plus or minus 448, and NaN. It contrasts
E4M3 with E5M2, whose range and precision trade-off differ. Those formats,
their kernels, and their scaling recipes must not be substituted silently.

## Select a documented numerical path

The cited Transformer Engine release describes current scaling as one FP32
scale per tensor: compute absolute maximum, scale to the chosen FP8 range, and
cast. It notes that this requires two tensor reads. That explains one
trade-off for that named recipe; it does not justify a universal static scale,
hard-clipping path, layer count, latency claim, or hardware promise for a
different framework or model.

Record the exact framework/engine release, GPU and driver, model/checkpoint,
precision settings, supported operations, tensor layout, and fallback/error
behavior. Verify the supported-device and operation matrix for the release in
use rather than extending a documented result to another accelerator or
runtime.

## Keep calibration and measurement evidence

For every intended execution path, retain:

- tensor format and scaling recipe by operation, including whether amax,
  delayed, block, or another documented strategy is used;
- calibration inputs or live amax evidence, scale-update policy, and
  outlier/saturation observations;
- checkpoint loading, serialization, compilation, and serving path, including
  where conversions occur;
- comparable baseline and FP8 runs with warm and steady-state latency, peak
  memory, throughput, reproducibility, numerical failures, and task-quality
  results; and
- acceptance thresholds set for the actual task, plus the measurement
  environment and source-disjoint evaluation set.

One model's activation distribution, calibration pass, or compiler behavior
does not certify another model, prompt distribution, resolution, batch shape,
or training phase.

## Failure boundary

If a required operation or device does not support the declared path, amax or
quality evidence is absent, a serialization boundary changes format, or
measurements violate the task threshold, report a visible failure/review
state. Do not replace E4M3 with E5M2, disable scaling, clamp values, or fall
back to another precision while describing the result as the same FP8 run.

## Related pages

- [[low-vram-inference-strategies]]
- [[diffusion-inference-acceleration]]
- [[diffusion-lora-training]]
- [[tiled-inference]]
