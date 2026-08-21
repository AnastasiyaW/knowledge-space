---
title: "Retouch Patch Harmonization for Paired Before/After Images"
description: "A training-data design for defect inpainting that preserves the clean target image colour domain while injecting localized defect detail from an aligned before image."
category: techniques
tags: [retouching, inpainting, image-harmonization, paired-data, frequency-separation, poisson-blending]
---

# Retouch Patch Harmonization for Paired Before/After Images

Use this construction when aligned `before`/`after` pairs contain both local defect removal and broader colour or tonal edits. The objective is defect inpainting, not reproduction of every edit made to the `after` image. Build corrupted inputs on the clean image's colour domain; retain the clean `after` image as target.

## Problem Boundary

Let `B` be an aligned before image, `A` the retouched image, and `M` a defect mask. A raw paired mapping `B -> A` makes one model explain at least two different transformations:

- removal or replacement of localized texture and defect detail;
- global or local grading, illumination, smoothing, and colour edits.

That separation is a dataset-design choice, not a result claimed by the cited papers. It follows the image-harmonization formulation: a foreground should be made compatible with its background domain. DoveNet frames harmonization that way and trains on synthetic composites paired with real images; its iHarmony4 data is built from COCO, Adobe5k, Flickr, and day2night sources [DoveNet / iHarmony4, CVPR 2020](https://openaccess.thecvf.com/content_CVPR_2020/html/Cong_DoveNet_Deep_Image_Harmonization_via_Domain_Verification_CVPR_2020_paper.html).

## Recommended Pair Construction

1. Geometrically align `B` to `A`; reject pairs with visible landmark, hair, or pose displacement inside the expanded mask.
2. Estimate removable detail from a multi-scale high-pass decomposition.
3. Start each synthetic input from `A`, not `B`.
4. Inject only selected defect/detail residuals from `B` inside an expanded mask `M+`.
5. Harmonize the pasted boundary to the surrounding `A` canvas.
6. Train against unchanged target `A`; provide `M` as an input channel when the model contract permits it.

```text
input  = harmonize(A, inject(A, defect_residual(B, A), M+), M+)
target = A
model_input = concat(input, M)  # optional but explicit conditioning
```

This deliberately asks the model to remove an inserted local inconsistency, rather than to infer an inverse global retouch operation.

## Frequency and Colour Decomposition

For a blur operator `G_sigma`, define a residual at scale `sigma`:

```text
low_sigma(I)    = G_sigma(I)
detail_sigma(I) = I - low_sigma(I)
```

One conservative defect residual is:

```text
D = M * max(0, detail_sigma(B) - detail_sigma(A))
X0 = clip(A + D, 0, 1)
```

Evaluate this at multiple blur scales, for example `sigma in {2, 4, 8}` pixels after normalizing resolution. The formula is a practical synthesis rule, not a detector guarantee: select connected components only after checking that they correspond to removed detail rather than alignment error or deliberate texture reduction.

For colour-specific spots, add a bounded local chroma residual in a perceptual colour space:

```text
delta_ab = clamp(ab(B) - ab(A), -c, c)
X0_lab[M+] = A_lab[M+] + [0, delta_ab]
```

Keep luminance and chroma controls separate. HDRNet shows that paired input/output edits can be approximated with local affine colour transforms in bilateral space, including content-dependent photographic edits; it does not establish that a single global inverse transform recovers a retoucher's original image [HDRNet project and paper](https://groups.csail.mit.edu/graphics/hdrnet/).

## Boundary Harmonization Options

### Local Statistics Baseline

Match patch statistics to a ring immediately outside `M+`, per channel or in Lab. For source patch `P` and destination ring `R`:

```text
P' = (P - mean(P)) * std(R) / max(std(P), epsilon) + mean(R)
```

Apply only to channels intended for harmonization; do not let a local statistics pass erase the injected defect signal. Global colour transfer is a useful diagnostic baseline, but the classical method transfers global image appearance statistics and does not encode spatially local lighting decisions [Color Transfer Between Images](https://www.cs.tau.ac.il/~turkel/imagepapers/ColorTransfer.pdf).

### Gradient-Domain Baseline

Poisson editing solves a boundary-constrained gradient-matching problem. For unknown patch values `f`, guidance field `v`, and destination boundary `f*`:

```text
min_f integral_Ω ||grad(f) - v||², subject to f|∂Ω = f*|∂Ω
```

Equivalently:

```text
Laplacian(f) = div(v) in Ω, with f|∂Ω = f*|∂Ω
```

Use source gradients as guidance when preserving injected structure matters; use mixed gradients when destination texture should dominate. This is a seam-control baseline, not evidence that Poisson blending produces a semantically correct inpaint. The original method explicitly supports seamless cloning and local changes to texture, illumination, and colour [Poisson Image Editing](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf).

## Runnable Reference: Detail Injection + Poisson Seam Control

Requires Python 3.10+, NumPy, and OpenCV. Inputs must already be pixel-aligned; `before.png`, `after.png`, and `mask.png` must have equal spatial dimensions; nonzero mask pixels mark defects.

```python
from pathlib import Path

import cv2
import numpy as np

root = Path(".")
before = cv2.imread(str(root / "before.png"), cv2.IMREAD_COLOR)
after = cv2.imread(str(root / "after.png"), cv2.IMREAD_COLOR)
mask = cv2.imread(str(root / "mask.png"), cv2.IMREAD_GRAYSCALE)
if (before is None or after is None or mask is None
        or before.shape != after.shape or mask.shape != after.shape[:2]):
    raise ValueError("aligned before/after/mask inputs are required")

mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)[1]
expanded = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
blur_b = cv2.GaussianBlur(before, (0, 0), sigmaX=4)
blur_a = cv2.GaussianBlur(after, (0, 0), sigmaX=4)
detail_b = before.astype(np.int16) - blur_b.astype(np.int16)
detail_a = after.astype(np.int16) - blur_a.astype(np.int16)
removed = np.maximum(detail_b - detail_a, 0)

candidate = after.astype(np.int16)
inside = expanded > 0
candidate[inside] += removed[inside]
candidate = np.clip(candidate, 0, 255).astype(np.uint8)

ys, xs = np.where(expanded > 0)
if len(xs) == 0:
    raise ValueError("mask contains no defect pixels")
center = (int(xs.mean()), int(ys.mean()))
input_image = cv2.seamlessClone(candidate, after, expanded, center, cv2.MIXED_CLONE)
cv2.imwrite(str(root / "synthetic-input.png"), input_image)
```

`cv2.seamlessClone` is used here only to construct a corruption with a controlled seam. The training target remains `after.png`.

## Loss and Evaluation Boundary

A masked reconstruction objective keeps the intended region explicit:

```text
L = lambda_m * mean(M * |prediction - A|)
  + lambda_b * mean(ring(M) * |prediction - A|)
  + lambda_u * mean((1 - M) * |prediction - input|)
```

The unmasked term is optional and should be chosen according to the model's desired edit scope. Do not report image-harmonization benchmark numbers as skin-retouch results: iHarmony4 consists of synthetic composite/real-image pairs, not paired clinical or cosmetic retouch images. Evaluate separately for alignment quality, residual-mask precision, seam visibility, texture retention, and unwanted edits outside `M`.

## Limitations

- Paired images with pose, expression, focus, or lighting changes violate the pixel-residual assumption; registration errors become synthetic defects.
- A blurred residual cannot distinguish an undesirable lesion from intentional texture removal, makeup, denoising, or lighting retouch. Use a reviewed mask generator and retain reject cases.
- Poisson methods enforce boundary compatibility but can shift low-frequency colour or preserve unsuitable source gradients; inspect patch interiors as well as seams.
- Local mean/std matching assumes the surrounding ring is representative. It fails across occlusions, sharp shadows, skin/hair boundaries, and strong specular highlights.
- A synthetic corruption distribution can be narrower than production defects. It is not proof that the trained model will generalize to new cameras, skin tones, or retouch styles.

## Gotchas

- **Issue: applying a global before-to-after colour rollback before synthesis.** This changes the target domain and can reintroduce unrelated grading into the defect task. **Fix:** use rollback only as a diagnostic; create the corrupted input on the `after` canvas.
- **Issue: injecting raw `before` pixels.** Raw patches carry low-frequency illumination, smoothing, and white-balance differences, making the seam task dominate the defect signal. **Fix:** begin with a high-frequency residual; add a separately bounded chroma residual only for reviewed spot classes.
- **Issue: using an undilated mask for seam control.** The blend boundary can sit on the defect edge and leave a ring or halo. **Fix:** dilate the injection/blend region while retaining the original defect mask for the primary loss and evaluation.
- **Issue: treating seamless cloning as inpainting ground truth.** Gradient-domain blending can make a boundary continuous while preserving the wrong detail. **Fix:** use it only as an input-corruption baseline and keep the verified clean `after` image as target.

## See Also

- [[skin-retouch-pipeline]] - defect detection, mask dilation, and texture-preserving retouch routing
- [[object-removal-inpainting]] - model selection and mask-based inpainting boundaries
- [[frequency-decomposition-editing]] - frequency-separated image editing concepts
- [[color-space-and-gamma-reference]] - colour-space and linear-light handling
