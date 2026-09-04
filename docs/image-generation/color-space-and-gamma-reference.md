---
title: Color Management: Versioned Transform Contract
description: "Color management is a versioned chain of input interpretation, working space, creative transforms, display or view transform, and output encoding; camera or container labels and generic gamma rules are insufficient without the exact profile, transform version, metadata policy, and validation display."
category: reference
tags: [color-management, color-space, transfer-function, icc, ocio, aces, output-transform]
aliases: ["Color Space and Gamma Reference", "Color Pipeline Reference"]
---

# Color Management: Versioned Transform Contract

Color management makes numerical image values interpretable between capture,
processing, and display. A filename, container, camera brand, or informal
label such as "log" does not identify a complete input transform. Treat every
transform chain as a versioned contract, then validate the delivered image on
the intended viewing path.

## Declare the transform chain

Record every stage, in order:

```text
source file or raw data
  -> input interpretation and decode
  -> working or reference space
  -> approved creative operations
  -> display or view transform
  -> output encoding, profile, and delivery metadata
```

For each job, bind the source digest, embedded metadata, chosen input
assignment, transform/configuration revision, working-space policy, display
or view name, output encoding, and validation display. A raw decode, camera
input transform, LUT, and display transform are distinct operations even when
one application presents them in one interface.

## Do not guess input interpretation

Metadata can be absent, stale, or inconsistent with the captured image.
Container type and camera family are not enough to select a transform. If the
input assignment cannot be verified from authoritative metadata, capture
records, or an approved reference, stop for review or mark the output as an
explicit interpretation. Do not silently choose a "closest" camera profile,
transfer function, or wide-gamut space.

The same rule applies to transfer curves. Gamma, logarithmic encodings, and
HDR transfer functions are defined by a named encoding and delivery context;
one generic gamma rule cannot safely decode every source or display every
output.

## Use managed, inspectable configurations

The [International Color Consortium](https://www.color.org/getting-started/)
defines a Profile Connection Space that connects independently made input and
output profiles. [OpenColorIO](https://opencolorio.readthedocs.io/en/latest/guides/authoring/authoring.html)
uses an explicit configuration for colorspaces, displays, views, looks, and
transforms. [ACES output transforms](https://docs.acescentral.com/system-components/output-transforms/)
are likewise selected for named target gamut, luminance, white point, and
display encoding combinations.

These systems do not make a generic transform correct by themselves. Pin the
profile/configuration and transform version, preserve it with the job, and
validate its input/output assumptions after an upgrade.

## Validate source, working, and delivery images

Use authorized test images or calibrated targets that cover neutral regions,
near-gamut colors, gradients, highlights, shadows, text, and protected
detail. Evaluate:

- input decoding and metadata handling;
- color, tone, and gamut behavior through the full transform chain;
- consistency between the chosen validation display/view and delivered file;
- clipping, banding, unexpected gamut mapping, and irreversible bake-in; and
- reproducibility after restart, cache reset, or configuration upgrade.

Record the output file/profile and a review receipt. Numeric pixel equality is
only meaningful if the same encoding and transform path are named.

## Failure policy

An unrecognized input, missing profile, unsupported display target, or failed
configuration validation is a visible capability failure. It is not permission
to strip metadata, bake a guess, or change the output path without recording
the choice. Keep color-management and creative-grade changes separately
auditable so a visual look is never misrepresented as a correction.

## Related pages

- [[color-correction-by-numbers]]
- [[color-checker-and-white-balance]]
- [[color-theory-for-ml]]
- [[diffusion-lora-training]]
