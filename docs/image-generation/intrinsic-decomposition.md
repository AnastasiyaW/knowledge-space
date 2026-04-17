---
title: Intrinsic Decomposition - Albedo and Illumination Separation
category: techniques
tags: [intrinsic-decomposition, albedo, relighting, illumination, color-transfer, reflectance, shading, neural-rendering]
---

# Intrinsic Decomposition - Albedo and Illumination Separation

Separating an image into intrinsic components (reflectance/albedo vs. shading/illumination). Applications: physics-correct relighting, illumination-independent color transfer, specular removal, white balance estimation.

## Core Decomposition

```
Observed image = Albedo (reflectance) × Shading (illumination)
RGB_observed   = L(albedo)  ×  I(light direction, intensity, color)
```

Albedo = surface reflectance without light effects. Shading = light-dependent component. Simple Lambertian model: `I = A * S`. Real materials add specularity, subsurface scattering, transmission.

## Methods

### FlowIID (2025)

**Paper:** arxiv 2601.12329

Single-step intrinsic decomposition via latent flow matching.

```python
# Albedo computed as:
albedo = input_image / estimated_shading  # per-pixel division in linear light
```

- Single inference step — fastest available method
- LMSE albedo: 0.0043 (SOTA on benchmarks at time of publication)
- Suitable for production pipeline where throughput matters

### Colorful Diffuse Intrinsic Decomposition (Aksoy et al., TOG 2024)

**Repo:** github.com/compphoto/Intrinsic  
**Paper:** arxiv 2409.13690 (SIGGRAPH Asia Best Paper HM)

Three-pass pipeline:
1. Grayscale ordinal shading estimation
2. Low-resolution chromaticity (light color) estimation
3. High-resolution albedo with sparse constraints

**Outputs:**

| Key | Content |
|-----|---------|
| `hr_alb` | High-res albedo (final reflectance estimate) |
| `dif_shd` | Diffuse shading |
| `residual` | Specular highlights + visible light sources |
| `wb_img` | White-balanced reconstruction |
| `dif_img` | albedo × diffuse shading |
| `gry_shd` | Grayscale shading (light-color-free) |

```python
from intrinsic.pipeline import load_models, run_pipeline
models = load_models('v2')
results = run_pipeline(models, image)
albedo  = results['hr_alb']
shading = results['dif_shd']
wb      = results['wb_img']
```

Key property: separates **colorful illumination** from albedo. Per-pixel white balance via colored shading layer. Works on arbitrary in-the-wild photographs.

**License:** Academic only (patent pending).

### DiffusionRenderer (NVIDIA, CVPR 2025 Oral)

**Repo:** github.com/nv-tlabs/diffusion-renderer

Full G-buffer extraction via video diffusion:

- Albedo, normals, metallic, roughness
- Forward + inverse rendering pipeline
- Cosmos-DiffusionRenderer: updated version with improved generalization

**License:** Non-commercial (NVIDIA).

### UniRelight (NVIDIA, NeurIPS 2025)

**Paper:** arxiv 2506.15673  
**Repo:** github.com/nv-tlabs/UniRelight

Joint albedo extraction + relighting via Cosmos-Predict1-7B-Video2World DiT backbone.

**Architecture:** Three latents concatenated along temporal axis, processed by single DiT:

```
f_theta([z_tau^E + h^E,  z_tau^a,  z^I];  c_emb, tau)
```

Where `z^I` = input video (conditioned), `z^a` = albedo (denoised), `z^E` = relit output (denoised). `h^E` = HDRI encoding added **only** to relit branch.

**HDRI encoding** (three representations concatenated by channel):
1. LDR panorama via Reinhard tonemapping
2. Log-intensity map: `E_log = log(E+1)/E_max`
3. Directional encoding: unit vectors in camera coordinates

**Inference specs:**

| Parameter | Value |
|-----------|-------|
| Resolution | 480 × 848 px |
| Steps | 35 (no CFG) |
| Time per 57 frames | 445.5s (1× A100) |
| VRAM estimate | 40-60 GB (7B DiT + VAE) |

**SyntheticScenes relit benchmark:**

| Method | PSNR | SSIM | LPIPS |
|--------|------|------|-------|
| DiffusionRenderer | 26.61 | 0.841 | 0.222 |
| UniRelight | **26.97** | **0.847** | **0.190** |

**License:** NVIDIA OneWay Noncommercial — production use requires explicit NVIDIA agreement.

### Other Models

| Model | Paper | Key Feature |
|-------|-------|------------|
| IDArb | arxiv 2412.12083 (ICLR 2025) | Multi-view consistent decomposition (normals + material) |
| IC-Light | ICLR 2025 | Diffusion-based, exploits linearity of light transport |
| LightLab | arxiv 2505.09608 (SIGGRAPH 2025) | Fine-grained per-light-source control |
| Facial Intrinsic (MSSID) | arxiv 2512.16511 | Full 6-pass PBR for faces: albedo, normals, AO, specular, translucency |
| FlowIID | arxiv 2601.12329 | Single-step, fastest, SOTA LMSE |

## Albedo-Domain Color Transfer

Standard color transfer methods (Reinhard, histogram matching, optimal transport) operate on full RGB. Problems:

1. Shadows shift the histogram toward dark — biases transfer
2. Specular highlights inflate mean brightness — incorrect shift
3. Colored light makes albedo appear different from what it is
4. Different illumination = different histograms despite identical surface color

**Solution: transfer in albedo domain then recompose.**

```
Source → Decompose → Source_albedo, Source_shading
Reference → Decompose → Ref_albedo

color_transfer(Source_albedo, Ref_albedo) → Matched_albedo

Output = Matched_albedo × Source_shading  [+ specular residual]
```

Lambertian recomposition works for diffuse surfaces. For specular: preserve the `residual` layer from Aksoy method and add back after albedo transfer.

## Method Selection

| Scenario | Recommended Method |
|----------|-------------------|
| Maximum speed, production | FlowIID |
| Best albedo quality + per-pixel WB | Colorful Intrinsic (Aksoy) — check license |
| Full G-buffer (normals needed) | DiffusionRenderer |
| Video temporal consistency | UniRelight — check license, A100 required |
| Face-specific PBR | Facial Intrinsic MSSID |

## Gotchas

- **Shadow misattributed as dark material**: decomposition models trained on indoor synthetic data may classify dark shadow regions as low-albedo material rather than illumination. Produces incorrect albedo map where shadows should be in the shading layer. Validate on your specific photography style before relying on results.
- **Albedo × shading recomposition is Lambertian only**: `output = albedo × shading` is valid for purely diffuse surfaces. Specular highlights, transparency, subsurface scattering are non-linear and will produce incorrect results if recomposed naively. Always add the `residual` layer back after color transfer.
- **Colorful vs. grayscale shading**: most older methods estimate grayscale shading. Aksoy's colorful shading is critical when the scene has colored light sources — grayscale shading methods will incorrectly attribute colored illumination to albedo, making the albedo appear "colored by the light" and defeating the purpose of the decomposition.
- **UniRelight inference-only limitation**: UniRelight does not output shading maps or normals directly — only albedo and relit image. Cannot use it to recompose output with modified albedo.
- **Temporal consistency gap**: FlowIID and Aksoy operate per-frame with no temporal attention. Frame-by-frame albedo estimates flicker on video. UniRelight solves this but requires A100 and non-commercial license.

## See Also

- [[color-theory-for-ml]] - Volkov local vs radiation color, theoretical foundation
- [[color-space-and-gamma-reference]] - color space pipelines, Log/RAW handling
- [[color-checker-and-white-balance]] - calibration-based color correction
- [[sana-denoiser-architecture]] - diffusion architecture reference
