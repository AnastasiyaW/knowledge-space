---
title: Color Theory for ML Image Generation
category: reference
tags: [color, theory, itten, composition, correction, palette, wavelength]
aliases: ["Color Theory", "Color Reference for Diffusion"]
---

# Color Theory for ML Image Generation

Applied color theory for diffusion model training, color correction, and palette control. Covers perceptual relationships, spectral foundations, and psychological effects.

## Itten's 12-Part Color Wheel

Johannes Itten's system underpins most color harmony logic in art and design:

```
Primary:    Red (0°), Yellow (120°), Blue (240°)
Secondary:  Orange (60°), Green (180°), Violet (300°)
Tertiary:   Red-Orange, Yellow-Orange, Yellow-Green,
            Blue-Green, Blue-Violet, Red-Violet
```

### Complementary Pairs (180° separation)

| Color | Complement | ML Use |
|-------|-----------|--------|
| Red | Green | Skin vs foliage; high contrast backgrounds |
| Blue | Orange | Sky vs warm metals; winter vs autumn |
| Yellow | Violet | High contrast for text/logo placement |
| Red-Orange | Blue-Green | Warm portraits on cool backgrounds |
| Yellow-Green | Red-Violet | Spring tones vs rose accents |

**For diffusion prompts**: complementary pairs create visual tension and high perceived contrast. Analogous colors (adjacent on wheel) create harmony.

### Harmony Types

| Harmony | Definition | Effect |
|---------|-----------|--------|
| Complementary | 2 colors, 180° apart | Bold, energetic |
| Analogous | 3 colors, 30° apart | Calm, cohesive |
| Triadic | 3 colors, 120° apart | Vibrant, balanced |
| Split-complementary | 1 + 2 near-complement | Harmony with contrast |
| Tetradic | 4 colors, 90° apart | Rich, complex |
| Monochromatic | 1 hue, varied saturation/value | Elegant, unified |

### Itten's Color Ball (3D Model)

The color ball extends the wheel into 3D:
- **Equator**: fully saturated hues (12-part wheel)
- **Top pole**: white
- **Bottom pole**: black
- **Axis**: grey scale (desaturation toward center)
- **Any point** on ball = unique HSL coordinate

This maps directly to HSL/HSV color spaces used in image processing.

## Volkov's Dual-Color Nature

Russian color theorist Nikolai Volkov distinguished two types of color perception:

### Local Color vs Radiation Color

| Type | Definition | Example |
|------|-----------|---------|
| Local color | Inherent color of object's surface | A red apple in neutral light |
| Radiation color | Color as modified by illumination | Same apple under blue moonlight |

**For auto-correction pipelines:**
- Color correction must separate **surface reflectance** from **illumination**
- Correcting "the red apple" means preserving local color while adjusting radiation
- White balance correction = adjusting radiation component
- Object-specific corrections = adjusting local color

### Implementation Relevance

```python
# Simplified separation: linear light model
# observed_color = local_color * illumination_color

# To correct illumination (white balance):
corrected = observed / illumination_estimate

# To correct local color without changing light:
corrected = swap_local_color(observed, illumination_estimate)
```

In ML: training data that confuses local vs radiation color creates models that "correct" well-lit images or fail to correct poorly-lit ones. Dataset should balance lighting conditions.

## Zaytsev Spectral Reference

Wavelength table for precise color-to-spectrum mapping:

| Color Name | Wavelength Range (nm) | Peak (nm) |
|-----------|----------------------|-----------|
| Violet | 380-450 | 415 |
| Blue | 450-495 | 470 |
| Cyan | 495-520 | 505 |
| Green | 520-565 | 540 |
| Yellow-Green | 565-580 | 572 |
| Yellow | 580-590 | 585 |
| Orange | 590-625 | 607 |
| Red | 625-700 | 660 |

Full visible spectrum: 380-700 nm. Camera sensors and display gamuts are defined relative to these ranges.

### ML Relevance

- **Camera spectral response**: cameras don't sample uniformly; sensor bias toward certain wavelengths affects training data color distribution
- **Display gamut**: sRGB covers ~35% of CIE Lab; P3 ~45%; ProPhoto ~90% — models trained on sRGB data will have compressed color range
- **Color shift in training data**: batch normalization at pixel level can shift spectral balance if not applied channel-wise with appropriate constants

## Golubeva: Psychological Color Effects

Physiological and psychological responses to color — relevant for image quality scoring and dataset curation:

| Color | Effect | Application |
|-------|--------|-------------|
| Red | Stimulating, excitatory, raises heart rate | High-energy product images, alerts |
| Orange | Warm, appetite-stimulating | Food photography baseline |
| Yellow | Cheerful, attention-grabbing, slightly straining | Highlights, callouts |
| Green | Calming, restful, reduces eye strain | Nature, wellness, "safe" content |
| Blue | Cool, trustworthy, slightly sedating | Tech, finance, medical |
| Violet | Mysterious, spiritual, sometimes oppressive | Luxury, creative |
| Black/Dark | Heavy, formal, sophisticated | Luxury, editorial |
| White/Light | Airy, clean, spacious | Product on white, medical |

### For Dataset Scoring

When building training data for aesthetic scoring models, include color temperature and dominant hue as features — psychological valence of color is measurable and correlates with human preference ratings.

```python
# Extract dominant hue for scoring
import cv2
import numpy as np

def dominant_hue(image_bgr):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    hue_channel = hsv[:, :, 0]
    # Weighted by saturation (ignore grey pixels)
    sat = hsv[:, :, 1]
    mask = sat > 30
    if mask.sum() == 0:
        return None
    return np.average(hue_channel[mask], weights=sat[mask])
```

## Color in Diffusion Prompting

### Effective Color Description Hierarchy

```
1. Global temperature: "warm golden light", "cool overcast"
2. Dominant palette: "earthy oranges and browns"
3. Key object color: "red velvet dress"
4. Accent colors: "silver jewelry details"
5. Background/environment: "deep blue gradient background"
```

### Harmony-Based Prompts

```yaml
Complementary:   "red dress, teal background, high contrast"
Analogous:       "warm amber, golden yellow, pale cream palette"
Monochromatic:   "desaturated blue tones, monochrome"
Split-comp:      "orange subject, blue-violet and blue-green background"
```

### Color Grading Terms (Recognized by Diffusion Models)

- `warm grade`, `cool grade`, `teal and orange grade`, `bleach bypass`
- `golden hour`, `blue hour`, `overcast soft light`
- `high saturation`, `muted palette`, `desaturated`, `vivid`
- `Kodachrome film look`, `Fuji Velvia`, `Portra 400`

## Gotchas

- **Complementary color rendering inconsistency**: diffusion models trained on internet data under-represent high-saturation complementary combinations (these are rare in photography). Force with stronger prompts or LoRA-trained color style.
- **sRGB training data gamut limitation**: most diffusion models are trained on sRGB data and cannot generate colors outside that gamut even when prompted for wide-gamut colors (neon greens, deep saturated purples). This is a dataset artifact, not a model failure.
- **Local vs radiation confusion in correction**: auto color correction applied naively shifts both local and radiation components together. Always segment or estimate illumination map before correcting for consistent results.
- **Hue vocabulary mismatch**: "cerulean" and "cobalt" mean specific wavelengths to artists but may be interpreted inconsistently by diffusion models trained on non-specialist captions. Test empirically; hex-to-name mappings from CSS/web vocabulary are more reliably rendered.

## Chromatic Adaptation and Color Appearance

### Chromatic Adaptation Transform (CAT)

Humans adapt to different illuminants so a white surface appears white under 2700K tungsten and 6500K daylight. Models must account for this when transferring color between images shot under different lighting.

Key adaptation models (ascending accuracy):
- **Von Kries**: per-channel gain applied in LMS cone space. Fast, used in many ICC workflows.
- **Bradford**: modified LMS matrix with improved blue channel behavior. ICC standard.
- **CIECAM02 / CAM16**: full Color Appearance Model including lightness, chroma, hue, contrast, and adaptation. Used for cross-media reproduction.

```python
# Von Kries chromatic adaptation (D50 → D65)
import numpy as np
# Convert sRGB to XYZ (simplified):
# Apply Bradford matrix to XYZ
# Scale LMS channels by ratio of white points
# Invert to get adapted XYZ
# Formula: LMS_adapted = (LMS_D65 / LMS_D50) * LMS_source
```

### Color Appearance Model (CAM) Dimensions

| Attribute | Symbol | Description |
|-----------|--------|-------------|
| Lightness | J | Perceived luminance relative to white |
| Chroma | C | Colorfulness relative to reference white |
| Hue | h | Hue angle in perceptual space |
| Saturation | s | Colorfulness relative to own luminance |
| Brightness | Q | Absolute perceived luminance |
| Colorfulness | M | Absolute colorfulness |

For ML: when building perceptual loss functions or scoring models, CIECAM02 attributes correlate better with human preference than CIEDE2000 or simple MSE in RGB.

## ICC Color Management Pipeline

### ICC Profile Chain

```
Input device (camera) → [ICC input profile]
  → Profile Connection Space (PCS = D50 XYZ or LAB)
  → [ICC output profile]
  → Output device (display/printer)
```

PCS is device-independent. Profiles encode characterization of each device. This two-step architecture allows any input → any output without per-pair conversion.

### Rendering Intents

| Intent | Use Case | Behavior |
|--------|----------|---------|
| Perceptual | Photography, general | Compresses entire gamut, preserves relationships |
| Relative Colorimetric | Proofing | Clips out-of-gamut, maps white points |
| Saturation | Presentation graphics | Maximizes saturation, not accuracy |
| Absolute Colorimetric | Reference proofing | No white point mapping |

Perceptual rendering intent is most relevant for image transfer tasks — it compresses wide-gamut source into narrow-gamut destination while maintaining gradient continuity.

### Display Gamut Implications for ML

- Models trained on sRGB data (≈ Rec.709) cannot generalize to wide-gamut inputs without remapping
- P3-wide monitors on macOS display sRGB content with inflated saturation unless ICC management is active
- Training data from mixed-gamut sources requires normalization to a common PCS before use

## Gotchas

- **Complementary color rendering inconsistency**: diffusion models trained on internet data under-represent high-saturation complementary combinations (these are rare in photography). Force with stronger prompts or LoRA-trained color style.
- **sRGB training data gamut limitation**: most diffusion models are trained on sRGB data and cannot generate colors outside that gamut even when prompted for wide-gamut colors (neon greens, deep saturated purples). This is a dataset artifact, not a model failure.
- **Local vs radiation confusion in correction**: auto color correction applied naively shifts both local and radiation components together. Always segment or estimate illumination map before correcting for consistent results.
- **Hue vocabulary mismatch**: "cerulean" and "cobalt" mean specific wavelengths to artists but may be interpreted inconsistently by diffusion models trained on non-specialist captions. Test empirically; hex-to-name mappings from CSS/web vocabulary are more reliably rendered.
- **Von Kries fails with large adaptation shifts**: Von Kries adaptation works well for small illuminant shifts (e.g., 5500K → 6500K) but degrades for large shifts (e.g., tungsten 2700K → daylight). Use Bradford or CIECAM02 for cross-condition color transfer pipelines.

## See Also

- [[color-checker-and-white-balance]] - color correction and white balance
- [[color-space-and-gamma-reference]] - gamma, color spaces, CMS workflows
- [[intrinsic-decomposition]] - albedo/illumination separation for color transfer
- [[flux-klein-jewelry-photography]] - color challenges in jewelry compositing
- [[defect-detection-small-objects]] - color anomaly detection for defects
