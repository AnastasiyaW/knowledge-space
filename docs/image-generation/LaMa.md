---
title: "LaMa: Resolution-Robust Large-Mask Inpainting"
description: "LaMa is a Fourier-convolution inpainting model for large masks and resolution generalization; use it with a compatible checkpoint and test texture continuity separately from semantic object restoration."
category: models
tags: [inpainting, ffc, fourier, large-mask, samsung, feed-forward, resolution-robust]
aliases: ["Large Mask Inpainting", "Big-LaMa"]
---

# LaMa: Resolution-Robust Large-Mask Inpainting

**Scope checked: 2026-09-04.** LaMa is a feed-forward inpainting method built for large missing regions and high-resolution images. The original work combines Fast Fourier Convolutions (FFC), a high-receptive-field perceptual loss, and large training masks. Its strong texture and structure completion behavior makes it a useful baseline, but it is not a deterministic object-reconstruction system.

## Why Fourier Convolutions Matter

An FFC layer splits feature processing into local and global paths. The global path uses Fourier-domain processing so a layer can incorporate information across the image rather than only a small spatial neighborhood. In the LaMa paper, that broader receptive field is paired with large masks and a perceptual objective to improve completion of challenging gaps and periodic structures.

The source repository reports that the model can generalize to substantially higher resolutions than its training resolution. Treat that as a capability to test on the intended image sizes, not as a guarantee that arbitrary megapixel inputs will preserve fine typography, jewelry facets, faces, or object identity.

## Use It for the Right Restoration Class

LaMa is a good candidate when the acceptance criterion is coherent background, texture, or simple structure continuity:

- remove a masked unwanted object from a textured or repetitive background;
- fill a large visual gap where source context is sufficient;
- produce a fast conservative baseline before a more expensive generative edit.

Use a separate semantic-editing or manual-compositing path when the task requires an exact logo, readable text, a specific person's identity, or a safety-critical object. A clean-looking fill is not proof that the removed or reconstructed content is correct.

## Reproducible Run Record

The upstream repository publishes several model configurations and links to checkpoints; some historic download links have changed. For each run, retain:

1. repository revision and the exact checkpoint origin/digest;
2. image preprocessing, mask creation method, and input resolution;
3. output compositing rule, especially whether unmasked pixels come from the original;
4. before/after image, mask, and a human acceptance result;
5. a fallback to the untouched source image when the fill crosses a critical boundary.

Third-party apps, ports, and ComfyUI nodes listed by the project are separate integrations. Verify their model source, privacy behavior, and license before treating them as equivalent to the upstream implementation.

## License Boundary

The checked `advimman/lama` source repository contains an Apache-2.0 license. Downloaded checkpoints, model-hosting terms, and third-party ports may add their own conditions, so verify the exact artifact before distribution or commercial deployment.

## References

- [LaMa official repository](https://github.com/advimman/lama)
- [LaMa paper](https://arxiv.org/abs/2109.07161)
- [LaMa project page](https://advimman.github.io/lama-project/)
