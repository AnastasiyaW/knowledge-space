# Color Correction by Numbers

Deterministic color correction using measurable channel targets rather than perceptual judgment. Core premise: neutral objects have R=G=B; world-average scene balance follows known channel ratios; skin tones follow a fixed channel hierarchy.

## Neutral Detection — R=G=B Test

Any object that should appear achromatic (white, grey, black) has equal RGB values when correctly white-balanced.

```python
def detect_color_cast(img_rgb: np.ndarray, sample_region=None) -> dict:
    """
    img_rgb: float32 in [0..255] or [0..1]
    sample_region: (x, y, w, h) or None for full image center
    """
    if sample_region:
        x, y, w, h = sample_region
        patch = img_rgb[y:y+h, x:x+w]
    else:
        # Center crop — tends to contain subject, fewer border casts
        h, w = img_rgb.shape[:2]
        patch = img_rgb[h//4:3*h//4, w//4:3*w//4]

    r, g, b = patch[:,:,0].mean(), patch[:,:,1].mean(), patch[:,:,2].mean()
    avg = (r + g + b) / 3
    cast = {
        'R': (r - avg) / avg,
        'G': (g - avg) / avg,
        'B': (b - avg) / avg,
        'channels': (r, g, b)
    }
    # cast['R'] > 0.05 → warm/red cast; < -0.05 → cool/cyan cast
    return cast
```

**Neutral sampling rules:**
- Sample grey card, white wall, or specular highlight (if not clipped)
- Avoid surfaces with indirect color bounce (sky-lit walls go blue)
- Parade scope: neutral = all three channel traces at equal height and parallel
- Vectorscope: neutral = distribution center at origin

## World-Average Balance (Margulis Targets)

Real-world scenes have a statistical color bias toward warm (yellow) due to sunlight/incandescent prevalence. Perfectly neutral balance often looks "too cold."

**Margulis average scene targets (8-bit):**

| Channel | Target | Notes |
|---------|--------|-------|
| R | 130 | Dominant — warm bias in most scenes |
| G | 128 | Middle |
| B | 120 | Weakest — contributes yellow warmth |

**Interpretation:** R > G > B in a correctly balanced outdoor/indoor scene. A scene with R≈G≈B looks clinically neutral and often wrong.

```python
MARGULIS_TARGETS = {'R': 130, 'G': 128, 'B': 120}

def margulis_correction(img_rgb: np.ndarray) -> np.ndarray:
    """Apply per-channel scale to hit Margulis targets."""
    means = {
        'R': img_rgb[:,:,0].mean(),
        'G': img_rgb[:,:,1].mean(),
        'B': img_rgb[:,:,2].mean()
    }
    out = img_rgb.astype(np.float32).copy()
    for i, ch in enumerate('RGB'):
        scale = MARGULIS_TARGETS[ch] / (means[ch] + 1e-6)
        out[:,:,i] = np.clip(out[:,:,i] * scale, 0, 255)
    return out.astype(np.uint8)
```

## Skin Tone Validation

Regardless of ethnicity or lighting, correctly-rendered skin tones obey a fixed channel hierarchy:

```text
R > G > B (always)
R / G ≈ 1.3  (± 0.1)
R / B ≈ 1.6  (± 0.15)
```

```python
def validate_skin_tone(r: float, g: float, b: float) -> dict:
    """Validate skin tone channel ratios (8-bit input)."""
    return {
        'hierarchy_ok': r > g > b,
        'rg_ratio': r / (g + 1e-6),    # target: 1.2–1.4
        'rb_ratio': r / (b + 1e-6),    # target: 1.45–1.75
        'rg_ok': 1.2 <= r/g <= 1.4,
        'rb_ok': 1.45 <= r/b <= 1.75
    }

# Vectorscope: skin tones cluster on a fixed diagonal line
# regardless of ethnicity — "skin tone indicator" overlay
# Hue angle: ~20-25° (reddish-orange sector)
```

**Practical range table:**

| Skin tone | R | G | B |
|-----------|---|---|---|
| Very light | 240 | 185 | 150 |
| Medium | 190 | 145 | 115 |
| Dark | 130 | 100 | 80 |

All rows satisfy R > G > B and the ratio constraints.

## Overlay White Balance Automation

Automated WB correction using the Overlay blend mode. Overlay acts as a multiplicative contrast enhancer: values above 128 push lighter, below 128 push darker. Applied in Color blending mode, it corrects color without affecting luminance.

**4-step algorithm:**

```python
def overlay_wb_correction(img_rgb: np.ndarray) -> np.ndarray:
    """
    Automated white balance via overlay blend.
    img_rgb: uint8 [0..255]
    """
    img = img_rgb.astype(np.float32)

    # 1. Compute per-channel average
    avg = img.mean(axis=(0, 1))  # shape (3,)

    # 2. Invert and normalize to 128
    # "Gray world with Margulis correction"
    correction = 128.0 - avg          # shift each channel to neutral 128
    correction_img = np.full_like(img, 128)
    for i in range(3):
        correction_img[:,:,i] = np.clip(128 + correction[i], 0, 255)

    # 3. Apply Overlay blend
    def overlay(base, blend):
        b = base / 255.0
        o = blend / 255.0
        return np.where(b < 0.5,
                        2 * b * o,
                        1 - 2 * (1 - b) * (1 - o)) * 255.0

    result = overlay(img, correction_img)

    # 4. Blend in Color mode (preserve luminance from original)
    # Convert to HSV, replace H+S from result, keep V from original
    import cv2
    orig_hsv = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    res_hsv  = cv2.cvtColor(result.clip(0,255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(np.float32)
    orig_hsv[:,:,0] = res_hsv[:,:,0]   # hue from result
    orig_hsv[:,:,1] = res_hsv[:,:,1]   # saturation from result
    # value channel (luminance) stays from original

    out = cv2.cvtColor(orig_hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    return out
```

**Margulis correction adjustment:** After step 3, optionally shift channels toward Margulis targets (R130/G128/B120) rather than perfect neutral (all 128). Increases perceptual warmth.

## 4-Stage Curves Workflow

Order of operations for tonal correction using Curves. Each stage builds on the previous; do not skip or reorder.

```text
Stage 1: White / Black Point
  Set endpoints — clip pure white and pure black
  Scopes: waveform endpoints touch 0 and 1023 (or 0/255)

Stage 2: Redistribute Contrast
  S-curve on midtones — shadows darker, highlights brighter
  Protect endpoint values from Stage 1

Stage 3: Brightness / Exposure
  Single control point at midpoint (128/512)
  Push up (brighten) or down (darken) overall exposure
  After S-curve so contrast shape is preserved

Stage 4: Per-Channel Color
  Individual R / G / B curves
  Fix casts identified by Parade scope
  Validate skin tone ratios after changes
```

```python
def apply_curves(img: np.ndarray, control_points: dict) -> np.ndarray:
    """
    control_points: {'master': [(in, out), ...], 'R': [...], 'G': [...], 'B': [...]}
    Values in 0-255 range.
    """
    from scipy.interpolate import PchipInterpolator
    import numpy as np

    def build_lut(points):
        if not points:
            return np.arange(256, dtype=np.uint8)
        xs, ys = zip(*sorted(points))
        xs = [0] + list(xs) + [255]
        ys = [0] + list(ys) + [255]
        f = PchipInterpolator(xs, ys)
        lut = np.clip(f(np.arange(256)), 0, 255).astype(np.uint8)
        return lut

    result = img.copy().astype(np.uint8)
    # Apply master curve
    if 'master' in control_points:
        lut = build_lut(control_points['master'])
        result = lut[result]
    # Apply per-channel curves
    for i, ch in enumerate('RGB'):
        if ch in control_points:
            lut = build_lut(control_points[ch])
            result[:,:,i] = lut[result[:,:,i]]
    return result
```

## LUT Generation from Color Checker Neutral Patches

Color checker cards have known neutral patches (near-white to near-black). The difference between measured and ideal neutral values captures the camera+light color error.

```python
def build_wb_lut_from_checker(
    measured_neutrals: list[tuple],   # [(r, g, b), ...] measured per patch
    ideal_neutrals: list[tuple]       # [(r, g, b), ...] standard values
) -> np.ndarray:
    """
    Returns a 3x3 correction matrix (RGB → RGB).
    Uses linear regression: ideal = M @ measured
    """
    import numpy as np
    M = np.array(measured_neutrals, dtype=np.float32)   # (N, 3)
    T = np.array(ideal_neutrals, dtype=np.float32)      # (N, 3)
    # Solve M @ X = T  → X = M+ @ T  (least squares)
    X, _, _, _ = np.linalg.lstsq(M, T, rcond=None)
    return X  # 3x3 matrix, apply as: corrected = img @ X

def apply_color_matrix(img_rgb: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    """Apply 3x3 color correction matrix."""
    h, w, _ = img_rgb.shape
    flat = img_rgb.reshape(-1, 3).astype(np.float32)
    corrected = flat @ matrix
    return np.clip(corrected, 0, 255).reshape(h, w, 3).astype(np.uint8)
```

**Standard X-Rite ColorChecker neutral row values (D50, 8-bit):**

| Patch | R | G | B |
|-------|---|---|---|
| White | 243 | 243 | 242 |
| Light grey | 200 | 200 | 200 |
| Mid grey | 160 | 160 | 160 |
| Dark grey | 122 | 122 | 121 |
| Near-black | 85 | 85 | 85 |
| Black | 52 | 52 | 52 |

The diagonal of a perfect shot equals these values; deviations encode the per-channel error.

## Gotchas

- **Issue:** Sampling saturated color areas for WB reference → channels diverge by saturation, not cast. -> **Fix:** Sample only achromatic (grey/white) objects. Exclude walls receiving colored bounce light (a sky-lit wall is blue even if it's physically white).
- **Issue:** Correcting to perfect neutral (R=G=B=128) looks artificially cold in most natural scenes. -> **Fix:** Target Margulis values (R130/G128/B120) or deliberately leave slight warm bias. Cold-neutral is perceptually wrong for most content.
- **Issue:** Skin tone R/G ratio check fails on dark-skinned subjects or under colored key light. -> **Fix:** Validate R>G>B hierarchy first (always true); ratios vary more at extremes. Under non-neutral key light, balance to key light hue before validating skin tone.
- **Issue:** Overlay WB algorithm leaves luminance unchanged but still shifts perceived brightness on monitors with different gamma. -> **Fix:** After Overlay correction, do a final luminance pass (Stage 3 of curves workflow). The blend-mode Color step is only an approximation of true hue isolation.

## See Also

- [[color-space-and-gamma-reference]] - color spaces, gamma, camera interpretation pipeline
- [[color-checker-and-white-balance]] - automated calibration pipeline
- [[color-theory-for-ml]] - perceptual color theory, CIE LAB, chromatic adaptation
- [[frequency-decomposition-editing]] - luminance/color separation for HF/LF editing
