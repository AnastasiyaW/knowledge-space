# Frequency Decomposition for Image Editing

Methods for separating images into low-frequency (LF) and high-frequency (HF) components, editing each independently, and recombining — used in retouching pipelines, diffusion model conditioning, and restoration networks.

## Decomposition Methods

### Gaussian Blur Subtraction

```python
import cv2
import numpy as np

def freq_sep(img: np.ndarray, radius: int = 12) -> tuple:
    """Returns (LF, HF). LF + HF == original exactly."""
    lf = cv2.GaussianBlur(img.astype(np.float32), (0, 0), radius)
    hf = img.astype(np.float32) - lf
    return lf, hf
```

**Reconstruction:** `result = edited_lf + original_hf` (exact, no artifacts).  
**Radius guidelines:** 3-5px = pore-level texture; 8-12px = skin retouching; 30-50px = volume/shadows.

### Stationary Wavelet Transform (SWT)

```python
import pywt

def swt_decompose(img: np.ndarray, wavelet: str = 'bior1.1', level: int = 4):
    """SWT preferred over DWT for editing: shift-invariant, no boundary artifacts."""
    coeffs = pywt.swt2(img, wavelet, level=level)
    # coeffs[0] = finest detail (Level 1: pores/noise)
    # coeffs[-1] = coarsest structure
    return coeffs

def edit_lf_only(coeffs, edit_fn):
    """Edit only the approximation (LF), keep all detail subbands."""
    new_coeffs = list(coeffs)
    # Edit the approximation at the coarsest level
    cA, (cH, cV, cD) = new_coeffs[-1]
    new_coeffs[-1] = (edit_fn(cA), (cH, cV, cD))
    return pywt.iswt2(new_coeffs, 'bior1.1')
```

**SWT vs DWT:**

| Feature | DWT | SWT |
|---------|-----|-----|
| Downsampling | Yes (halves resolution) | No (maintains size) |
| Shift invariance | No | Yes |
| Editing artifacts | Boundary artifacts possible | Clean |
| Compute cost | Lower | Higher (no downsampling savings) |

**Use SWT for editing, DWT for compression.**

### Wavelet Family Selection

| Wavelet | Best for |
|---------|---------|
| `bior1.1` (= Haar) | Sharp edges, fast prototyping |
| `db4`–`db8` | General purpose, best compression efficiency |
| `CDF 9/7` | Linear-phase requirements (JPEG 2000 standard) |
| Symlets | When symmetry + Daubechies properties needed |

### Laplacian Pyramid

Multi-scale decomposition: each level captures one octave of spatial frequencies.

```python
def laplacian_pyramid(img: np.ndarray, levels: int = 4) -> list:
    gaussian = [img.astype(np.float32)]
    for _ in range(levels):
        gaussian.append(cv2.pyrDown(gaussian[-1]))
    laplacian = []
    for i in range(levels):
        up = cv2.pyrUp(gaussian[i + 1], dstsize=(gaussian[i].shape[1], gaussian[i].shape[0]))
        laplacian.append(gaussian[i] - up)
    laplacian.append(gaussian[-1])  # residual LF
    return laplacian

def reconstruct(pyramid: list) -> np.ndarray:
    img = pyramid[-1]
    for lap in reversed(pyramid[:-1]):
        img = cv2.pyrUp(img, dstsize=(lap.shape[1], lap.shape[0])) + lap
    return img
```

**Level frequency ranges** (for 5472px image):
- Level 1: ~2700-5472 Hz band (pores, finest noise)
- Level 2: ~1350-2700 Hz (hair strands, fabric)
- Level 3: ~675-1350 Hz (wrinkles, coarse texture)
- Level 4+: smooth structure (shadows, volume, color)

### Edge-Preserving: Bilateral / Guided Filter

```python
# Bilateral (edge-preserving LF, but staircase artifacts):
lf = cv2.bilateralFilter(img, d=15, sigmaColor=75, sigmaSpace=75)
hf = img - lf  # approx only — LF + HF != original exactly

# Guided (better edge behavior, O(N) cost):
from cv2.ximgproc import guidedFilter
lf = guidedFilter(guide=img, src=img, radius=15, eps=200)
hf = img - lf
```

**Warning:** Both are non-linear — `LF + HF ≠ original`. Use Gaussian/wavelet when perfect reconstruction is required.

## HF Reinjection Patterns

### Simple Addition
```python
result = edited_lf + original_hf
```
Works for small LF edits. Fails when LF brightness changes significantly (intensity mismatch), geometric edits occur, or color domain shifts.

### Alpha-Masked Blending
```python
change_map = np.abs(edited_lf - original_lf).mean(axis=-1, keepdims=True)
alpha = 1.0 - (change_map / change_map.max())
alpha = cv2.GaussianBlur(alpha, (0, 0), feather_radius)
result = edited_lf + alpha * original_hf
```
Fades HF proportional to edit magnitude. Practical for moderate retouching edits.

### Wavelet Recombination (Recommended for Multi-Scale)
```python
coeffs = pywt.wavedec2(image, 'bior1.1', level=4)
# Edit only LL approximation (index 0)
coeffs[0] = diffusion_edit(coeffs[0])
# LH/HL/HH subbands preserved automatically
result = pywt.waverec2(coeffs, 'bior1.1')
```
Mathematically exact. Preserves per-level and per-orientation detail independently.

### MoFRR-Style Conditioned HF Generation (Most Robust)

For significant LF edits where original HF won't match:
1. Wavelet-decompose input → LL and LH/HL/HH
2. Diffusion model edits LL
3. HF cross-attention module conditioned on **edited** LL regenerates HF
4. IDWT reconstruction

Ensures HF adapts to new LF context. Requires training the HF module.

## Diffusion Models and Frequency Hierarchy

Diffusion models generate **low frequencies first, high frequencies last**:

| Timestep | What model generates |
|----------|---------------------|
| t ≈ T (early denoising) | Global layout, major color blobs |
| t ≈ T/2 (middle) | Medium-scale features, shapes |
| t ≈ 0 (late denoising) | Fine texture, skin pores, noise |

**Theoretical basis (Dieleman 2024):** Under DDPM noise schedule, HF components have lower SNR — they are destroyed first and recovered last. Diffusion = spectral autoregression.

**Practical implication:** To edit LF while preserving HF, inject LF guidance in early timesteps (t > T/2) and preserve/inject original HF in late timesteps (t < T/3).

### Timestep-Based Editing
```text
1. DDIM inversion of input
2. Inject LF edit guidance at t > 0.5T (only LF visible here)
3. At t < 0.3T: blend generated HF with original HF using alpha mask
4. Transition zone 0.3T < t < 0.5T: linear blend
```

## Neural Frequency Architectures

| Architecture | Mechanism | Use case |
|-------------|-----------|---------|
| **MoFRR** (ICCV 2025) | Dual-branch: DDIM restores LL, cross-attn module restores HF conditioned on edited LL | Face retouching with significant LF edits |
| **HiWave** (SIGGRAPH Asia 2025) | Wavelet detail enhancer in diffusion sampling; retain LF from base, guide HF selectively | High-res enhancement, training-free |
| **W-Edit** (2024) | DWT on intermediate diffusion features; edit specific subbands | Plug-and-play frequency-selective editing |
| **DeCo** (CVPR 2026) | DiT for LF semantics + lightweight pixel decoder for HF | 10x faster training, 1.62 FID |
| **SFNet** (ICLR 2023) | Learned per-input frequency selection via channel attention | Restoration (deblur, dehaze, denoise) |
| **Focal Frequency Loss** | Fourier-domain loss weighting hard (HF) frequencies higher | Add to any generator training |
| **FreeDiff** (ECCV 2024) | Progressive frequency truncation in timestep guidance | Reduce excessive LF leakage in editing |

## Frequency Separation Workflow (Professional)

Photoshop industry standard directly maps to neural pipeline:

| Photoshop step | Neural pipeline equivalent |
|---------------|--------------------------|
| Gaussian blur → Low layer | LF extraction (Gaussian, wavelet LL) |
| Apply Image → High layer | `HF = image - LF` or wavelet detail subbands |
| Edit Low (D&B, color grade) | Diffusion model processes LF |
| Preserve High | Original wavelet HF subbands kept |
| Merge (Linear Light) | Wavelet IDWT reconstruction |

## Gotchas

- **Issue:** Simple HF reinjection on bright-region edits causes texture intensity mismatch (pores look too dark/light). -> **Fix:** Use change-map alpha mask; `alpha = 1 - normalize(|edited_LF - original_LF|)`.
- **Issue:** DWT lacks shift invariance — the same spatial edit produces different coefficient changes depending on pixel position, causing visible periodic artifacts. -> **Fix:** Use SWT for any editing task; reserve DWT for compression.
- **Issue:** Bilateral filter staircase effect (cartoon-like plateaus) when used as LF for retouching. -> **Fix:** Use guided filter instead; or use Gaussian with `fill_mask=0` approach.
- **Issue:** DeCo / HiWave wavelet techniques require knowing internal latent dimensions. For SDXL/FLUX, latent channels ≠ image channels. -> **Fix:** Apply wavelet decomposition to pixel space or to all 4 (or 16) latent channels independently; do not mix across channels.
- **Issue:** Focal Frequency Loss (FFL) at high weight can force the generator to hallucinate HF content (over-sharpen). -> **Fix:** Weight FFL at 0.1–0.5 relative to L1/perceptual loss; monitor HF quality metrics separately.

## See Also

- [[skin-retouch-pipeline]]
- [[diffusion-inference-acceleration]]
- [[recurrent-depth-transformer]]
- [[tiled-inference]]
