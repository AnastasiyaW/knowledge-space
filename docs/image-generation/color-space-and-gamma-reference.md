---
title: Color Space and Gamma Reference for Video/Image Pipelines
category: reference
tags: [color-space, gamma, rec709, log, hlg, aces, davinci-wide-gamut, raw, chroma-subsampling, lut, cms, icc]
---

# Color Space and Gamma Reference for Video/Image Pipelines

Practical reference for color management in video/photo processing pipelines. Covers color spaces, gamma transfer functions, RAW workflows, and Color Management System (CMS) architecture.

## Architecture Overview

```
Camera sensor (linear light)
  → OETF (Opto-Electronic Transfer Function) applied at recording
  → File (with color space + gamma metadata)
  → EOTF (Electro-Optical Transfer Function) applied at display
  → Monitor output
```

Most display devices apply Rec.709 gamma regardless of file metadata. Log-encoded material must be explicitly transformed before output.

## Dynamic Range by Format

| Format | Dynamic Range | Notes |
|--------|--------------|-------|
| Rec.709 Gamma (SDR display) | 5-6 stops | Most consumer monitors |
| Human eye (simultaneous) | ~14 stops | With adaptation: up to 24 |
| Film negative | ~13 stops | |
| ARRI Mini LF | 14.5 stops | |
| Log Gamma | ~14 stops | Camera-specific curves |
| HLG (Hybrid Log Gamma) | >14 stops | Backward-compatible with SDR |

## Color Space Standards

### Display Standards (ascending gamut size)

```
Rec.709 ≈ sRGB  <  DCI-P3  <  Rec.2020
```

| Standard | Year | Coverage | Typical Use |
|----------|------|----------|------------|
| Rec.709 (BT.709) | 1991 | ~35% CIE | ~90% of consumer displays, broadcast TV |
| sRGB | 1996 | ≈Rec.709 | Computer monitors, web images |
| DCI-P3 | 2010 | ~45% CIE | Digital cinema, HDR displays |
| Rec.2020 (BT.2020) | 2012 | ~75% CIE | 4K TV, wide-gamut reference |

### Camera-Specific Wide Gamut

| Manufacturer | Color Space | Paired Gamma |
|---|---|---|
| Sony | S-Gamut2, S-Gamut3, S-Gamut3.Cine | S-Log2, S-Log3 |
| Panasonic | V-Gamut | V-Log |
| ARRI | ARRI Wide Gamut | LogC3, LogC4 |
| Blackmagic | Blackmagic Wide Gamut | Blackmagic Film |
| RED | REDWideGamutRGB | Log3G10, Log3G12 |
| DaVinci | DaVinci Wide Gamut RGB | DaVinci Intermediate |

## Gamma Transfer Functions

### Standard Gamma (SDR)

- **Rec.709 Gamma**: gamma 2.4, standard for broadcast
- **sRGB**: piecewise function ≈ gamma 2.2, for monitors
- 90% of displays automatically apply Rec.709 decoding to all input regardless of file gamma

### Log Gamma

Logarithmic curve compressing ~14 stops into standard bit depth. Each manufacturer has a different curve — not interchangeable:

```python
# Conceptual: log-encoded value from linear light
import numpy as np
# Generic approximation (NOT S-Log or V-Log specific):
log_val = np.log(linear_val + 1) / np.log(max_scene_luminance + 1)
```

**Critical**: Displaying Log on an SDR monitor without transform = washed-out image (monitor applies Rec.709 EOTF to Log data — wrong).

### HLG (Hybrid Log Gamma)

Hybrid curve with two segments:
- Below reference white: standard Rec.709 gamma (backward-compatible with SDR)
- Above reference white: logarithmic extension (used on HDR displays)

Result: single file plays correctly on both SDR and HDR displays without separate versioning.

## RAW Format

Linear photon counts from sensor, no gamma or color space applied.

**Advantages:**
- Maximum dynamic range for the camera
- Maximum color gamut
- Post-process can apply any color space / gamma

**Processing:** Requires debayering (demosaicing) + explicit gamma + color space assignment. In NLEs this is the Camera RAW step.

**Common mistake:** Importing RAW without setting correct Input Color Space — NLE assumes Rec.709 and clips dynamic range.

## Bit Depth vs. Chroma Subsampling

### Bit Depth

| Bits | Steps | Gradient Banding |
|------|-------|-----------------|
| 8-bit | 256 | Visible posterization in gradients |
| 10-bit | 1024 | Smooth transitions |
| 12-bit | 4096 | Professional, no visible banding |

Publishing to social platforms at 8-bit: gradients in backgrounds become visible bands. Mitigations: add subtle grain, avoid large smooth-tone backgrounds, publish in 4K (platform applies softer compression).

### Chroma Subsampling (YUV)

Reduces color resolution while preserving luma:

| Format | Description | Artifact |
|--------|------------|---------|
| 4:4:4 | Full luma + chroma per pixel | None |
| 4:2:2 | Chroma sampled at half horizontal res | Mild on large color regions |
| 4:2:0 | Chroma sampled at 1/4 spatial res | Visible blocks on highly-saturated areas |

Noise in camera footage concentrates in chroma channels. Denoising: apply to chroma (UV) channels only, not luma.

## CMS Workflows

### ColorSpace Transform (CST) — Explicit Pipeline

```
Input clip → CST node (Log+WideGamut → Rec.709+Gamma2.4)
           → Color corrections (in Rec.709)
           → Output
```

Most explicit and understandable. Balance/exposure corrections should be applied **before** CST to preserve full dynamic range during correction.

### DaVinci Wide Gamut (Internal Working Space)

```
Input → Interpreted as camera color space (auto or manual)
      → All corrections in DaVinci Wide Gamut (~ACES-like container)
      → Output Color Space = Rec.709 (applied at render only)
```

Advantage over CST: corrections in wide gamut, no clipping risk during grading. Single compression step at output.

### ACES

- Input Device Transform (IDT): camera color space → ACES
- All work in AP0/AP1 linear
- Output Device Transform (ODT): ACES → target display

ACES is linear — VFX/CG compositing integrates perfectly. Expensive to configure per-camera, Lift/Gamma controls behave non-intuitively.

## Color Analysis Scopes

### Parade (RGB/YRGB)

Separate R, G, B waveforms stacked. Neutral color = all channels at same height and parallel.

```python
# Detect color cast programmatically
r_mean = img[:,:,0].mean()
g_mean = img[:,:,1].mean()
b_mean = img[:,:,2].mean()
avg = (r_mean + g_mean + b_mean) / 3
threshold = 0.05

cast = {c: (v - avg)/avg for c, v in zip('RGB', [r_mean, g_mean, b_mean])}
# cast['R'] > threshold → warm/red cast
```

### Vectorscope

Plots hue angle vs. saturation radius. Center = neutral (no saturation). Skin tones fall on a specific diagonal line regardless of ethnicity — use skin tone indicator for white balance.

```
Skin tone hue angle: ~20-25° (reddish-orange sector)
Neutral white balance: distribution centroid near (0,0) in UV space
```

Broadcast legal limit: saturation must not exceed outer box markers on vectorscope.

### Waveform

Horizontal pixel position mapped to brightness value (0–1023 in 10-bit). Useful for exposure: clip checking, IRE targets (18% grey = ~512).

## Practical Input Interpretation Rules

| Camera / Format | Input Color Space | Gamma |
|---|---|---|
| Rec.709 material | None (pass through) | — |
| ARRI LogC in ProRes | ARRI Wide Gamut | LogC3 |
| Sony S-Log3 | S-Gamut3.Cine | S-Log3 |
| Panasonic V-Log | V-Gamut | V-Log |
| RED IPP2 | REDWideGamutRGB | Log3G10 |
| Blackmagic RAW | Blackmagic Wide Gamut | Blackmagic Film |
| DJI D-Log | D-Gamut (DLog-M) | D-Log M |
| iPhone HDR | HLG | HLG |

**White balance and exposure** corrections: apply **before** transform (in log/wide-gamut space) to leverage full bit depth.

## Gotchas

- **Log on display without transform**: 90% of displays apply Rec.709 EOTF to any input. Log footage shows as desaturated/flat unless explicitly converted. NLEs often silently apply wrong gamma.
- **ARRI ProRes container ≠ Rec.709**: ARRI frequently records LogC3 encoded video into ProRes .mov containers. Container format says nothing about color space — check camera metadata or ask the shooter.
- **DaVinci Histogram axis reversal**: in Resolve, histogram left = brighter, right = darker — opposite of Photoshop/Lightroom. Applying Lightroom histogram intuition causes incorrect exposure adjustments.
- **HLG auto-detected as Rec.709**: auto color managed workflows often misidentify HLG-encoded clips as Rec.709. Verify manually: HLG footage has a characteristic toe in dark areas that looks wrong under Rec.709 gamma.
- **Chroma denoising target**: camera noise is predominantly in UV channels, not luma. Applying spatial noise reduction equally to all channels sharpens luma artifacts while leaving chroma noise. Target the chroma channel specifically.
- **Wide-gamut monitor + sRGB signal**: consumer monitors with P3-wide panels often display Rec.709 signal too saturated without explicit color management. Calibration + ICC profile in OS is required for accurate monitoring.

## See Also

- [[color-theory-for-ml]] - perceptual color theory, Volkov local vs radiation color
- [[color-checker-and-white-balance]] - automated calibration pipeline
- [[intrinsic-decomposition]] - separating albedo from illumination
- [[diffusion-lora-training]] - color space considerations for training data
