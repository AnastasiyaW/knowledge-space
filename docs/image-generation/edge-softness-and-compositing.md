---
title: "Edge Softness and Compositing"
description: "Measure the edge instead of choosing it: 10-90 transition width, robust outline fitting, signed-distance rounding without the two classic bugs, area-integrated minification, premultiplied resampling, and coverage alpha instead of blurred alpha."
---

# Edge Softness and Compositing

Any paste, mask, matte or composite meets its surroundings **at the edge**, and the eye
catches the edge before it catches colour or geometry: stair-stepping, halo, mush and
sticker-on-top all read as edge defects. So the edge is not a taste decision and not a
library default - it is measured on the frame being worked and then reproduced.

## 1. Softness is measured, not chosen

Sample the intensity profile perpendicular to the boundary and take the 10-90% transition
width. Across one set of six photographic frames the measured width was **1.75-2.50 px**,
driven by optics and compression rather than preference. A hard 1.0 px edge dropped into a
neighbourhood whose own transitions are 2.2 px *is* the stair-stepping the client reports.

```python
import numpy as np

def edge_softness_px(gray, points, normals, half=6.0, step=0.25, min_contrast=0.15):
    """Median 10-90 transition width across samples along one boundary.

    points/normals: Nx2 arrays of boundary positions and unit normals (image coords).
    Bilinear sampling at sub-pixel offsets; low-contrast profiles are discarded so
    noise does not dominate the median.
    """
    offsets = np.arange(-half, half + step, step)
    widths = []
    for p, n in zip(points, normals):
        xs = p[0] + n[0] * offsets
        ys = p[1] + n[1] * offsets
        prof = bilinear_sample(gray, xs, ys)
        lo, hi = np.percentile(prof, 2), np.percentile(prof, 98)
        if hi - lo < min_contrast:
            continue
        t = (prof - lo) / (hi - lo)
        i10 = np.interp(0.10, t, offsets) if t[0] < t[-1] else np.interp(0.10, t[::-1], offsets[::-1])
        i90 = np.interp(0.90, t, offsets) if t[0] < t[-1] else np.interp(0.90, t[::-1], offsets[::-1])
        widths.append(abs(i90 - i10))
    return float(np.median(widths)) if widths else float("nan")
```

Take the median over roughly a hundred samples per side; a single profile crossing a
specular highlight will not represent the edge.

## 2. Straight things get straight edges

A segmentation mask wanders around the true boundary. Measured against a fitted line, the
outline of a planar rectangular object deviated by **0.29-0.60 px RMS**. For an object
known to be planar and rectangular (a plate, a screen, a label, a facet), that wander is
model noise, not shape.

Fit the four sides robustly and intersect them for the corners:

```python
def fit_line_huber(pts, iters=6, delta=1.0):
    """Robust line fit; a specular blob or shadow otherwise drags a least-squares fit."""
    w = np.ones(len(pts))
    for _ in range(iters):
        mean = np.average(pts, axis=0, weights=w)
        cov = np.cov((pts - mean).T, aweights=w)
        direction = np.linalg.eigh(cov)[1][:, -1]          # principal direction
        normal = np.array([-direction[1], direction[0]])
        r = (pts - mean) @ normal
        s = 1.4826 * np.median(np.abs(r - np.median(r))) + 1e-9
        a = np.abs(r / s)
        w = np.where(a <= delta, 1.0, delta / a)           # Huber weights
    return mean, normal
```

Fitting the outline also closes holes the mask left inside the object where dark details
were mistaken for background.

## 3. Rounded corners: use the definition, not an approximation

A rounded polygon is the set of points no further than `r` from the polygon shrunk inward
by `r`. Implemented per-edge:

```python
def rounded_signed_distance(depths, r):
    """depths: per-edge inside-depth (positive inside). Returns signed distance.

    Two classic bugs live in these four lines - see below.
    """
    violation = np.maximum(r - depths, 0.0)                # per-edge shortfall
    outside = np.sqrt(np.sum(violation ** 2, axis=0))      # Euclidean, NOT min()
    inner = np.min(depths, axis=0)
    return np.where(outside > 0, r - outside, inner)       # keep growing inside
```

**Bug 1 - taking `min` over edges before the square root.** Algebraically that reduces to
`min(depth, r)`, i.e. exactly the un-rounded boundary: the radius silently does nothing
while the mask still looks plausible. Detect it by rendering `r=12` against `r=0` and
requiring a difference. The expected area removed at one right-angle corner is
`r^2 * (1 - pi/4)`; for four corners at `r=12` that is 124 px, and a correct
implementation measured 126.

**Bug 2 - clamping the interior at `r`.** If distance stops growing once inside, alpha
saturates at `r / (2 * half) + 0.5`. With `r = 2.1 px` and softness `5.0 px` that is
**0.92 across the whole interior** - the paste is translucent and the thing it is supposed
to cover shows through. Both bugs pass a green test suite; only a render diff catches them.

The radius is measured too: across the same six frames it ranged **0.91-15.39 px**
(13.8x as a fraction of object height). A hardcoded radius is wrong nearly everywhere.

## 4. Minification: integrate, do not sample

At 3-4.5x downscale, `INTER_LANCZOS4` **samples** rather than averaging area, so a thin
stroke breaks into a dotted line. Supersampled area averaging fixed a measured stroke error
of **33-39% -> 0.5-2.2%**.

```python
import cv2

def integrate_minified_warp(src, M, out_size, scale_x, scale_y, ss=4):
    """Area-integrated warp. Gate: only when BOTH axes shrink by >= 1.2x."""
    if scale_x > 1/1.2 or scale_y > 1/1.2:
        return cv2.warpPerspective(src, M, out_size, flags=cv2.INTER_LANCZOS4)
    w, h = out_size
    big = cv2.warpPerspective(
        src, np.diag([ss, ss, 1.0]) @ M, (w * ss, h * ss), flags=cv2.INTER_NEAREST)
    return big.reshape(h, ss, w, ss, -1).mean(axis=(1, 3)).astype(src.dtype)
```

The gate matters: on an axis being *enlarged*, block averaging produces blockiness.

## 5. Premultiply before any resample

Every interpolation that mixes colour with alpha (resize, rotate, warp) must run on
premultiplied data, otherwise background colour bleeds through the partially transparent
rim - the dark halo around a bright paste.

```python
def to_premultiplied(rgba_f32):
    rgb, a = rgba_f32[..., :3], rgba_f32[..., 3:4]
    return np.concatenate([rgb * a, a], axis=-1)

def from_premultiplied(pm_f32, eps=1e-6):
    rgb, a = pm_f32[..., :3], pm_f32[..., 3:4]
    return np.concatenate([rgb / np.maximum(a, eps), a], axis=-1)
```

Do the round trip in linear light, not in gamma-encoded sRGB - see
[[color-space-and-gamma-reference]].

## 6. Coverage alpha, not blurred alpha

Stair-stepping is cured by the **fraction of the pixel covered** by the shape, not by
blurring the alpha channel. Blur "cures" it by smearing: measured over 12 boundaries,
coverage alpha gave a transition band of **6.0 -> 2.0 px** and deviation from the true line
of **0.21 -> 0.08 px RMS**. A soft wide edge is not a fix for aliasing - it is a different
complaint (mush instead of steps).

```python
def coverage_alpha(signed_distance, softness_px):
    """Analytic coverage from a signed distance field; softness measured in step 1."""
    half = max(softness_px, 1e-3) / 2.0
    return np.clip(0.5 + signed_distance / (2.0 * half), 0.0, 1.0)
```

## 7. Verify a parameter by rendering two settings that must differ

A parameter is proved by rendering with and without it and **requiring** the images to
differ, then checking the magnitude against geometry (the `r^2 (1 - pi/4)` corner-area
check above). Both rounding bugs in section 3 passed the unit suite; the render diff is
what exposed them. See [[negative-controls-for-verification]].

## Gotchas

- **Issue:** softness picked as a constant "because it looks nice". On half the frames it
  is visibly wrong, and the complaint arrives as "stair-stepping" or "mush" depending on
  direction. -> **Fix:** measure the 10-90 width on the frame and match it.
- **Issue:** `min` over per-edge depths before the square root in the rounded-corner SDF.
  The radius parameter is dead while the mask looks correct. -> **Fix:** Euclidean norm of
  per-edge violations; assert `r=12` differs from `r=0`, and check corner area against
  `r^2 (1 - pi/4)`.
- **Issue:** distance clamped at `r` inside the shape, so interior alpha saturates below 1
  and the paste is see-through. -> **Fix:** `where(outside > 0, r - outside, inner_depth)`;
  assert interior alpha == 1.
- **Issue:** RGBA resized or warped without premultiplying, producing a dark rim on light
  content over dark backgrounds. -> **Fix:** premultiply, resample, unpremultiply, in
  linear light.
- **Issue:** Lanczos used for a 4x downscale of thin strokes, which disintegrate into
  dashes. -> **Fix:** supersampled area integration, gated on both axes shrinking.
- **Issue:** aliasing "fixed" by blurring the alpha, trading a sharp complaint for a soft
  one. -> **Fix:** coverage-based alpha; keep the transition band at the measured width.
- **Issue:** the edge parameter is believed correct because the test suite is green,
  without a single side-by-side render. -> **Fix:** render two settings that must differ
  and compare against a geometric prediction.

## See Also

- [[retouch-patch-harmonization]] - matching the patch interior to its surroundings
- [[perspective-calibration-for-compositing]] - geometry before the edge treatment
- [[object-removal-inpainting]] - boundary handling for removals
- [[tiled-inference]] - seam blending between tiles
- [[color-space-and-gamma-reference]] - why the resample happens in linear light
- [[intrinsic-decomposition]] - separating shading from albedo before blending
- [[negative-controls-for-verification]] - proving a rendering parameter is alive
