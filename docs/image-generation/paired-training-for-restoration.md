---
title: Paired Training for Restoration
category: techniques
tags: [img2img, paired-dataset, degradation, conditioning, channel-concat, restoration-training, flow-matching]
aliases: ["Image-to-Image Conditioning", "Paired Image Training", "Degradation Pipeline"]
---

# Paired Training for Image Restoration

How to train a diffusion model for image-to-image restoration (not text-to-image). Core technique: channel concatenation of degraded image latent with noise.

## The Problem

Standard [[flow-matching]] trains T2I: `noise → image` conditioned on text. For restoration we need: `degraded_image → clean_image`. Simply training T2I on clean images does NOT produce a denoiser.

## Solution: Channel Concatenation

```toml
clean_image → VAE.encode → latents (target)
degraded_image → VAE.encode → condition_latents

noise → x_t = (1-σ)*noise + σ*latents     # standard flow matching
model_input = concat([x_t, condition_latents], dim=1)  # [B, 2C, H, W]
projection = Conv2d(2C, C, kernel_size=1)   # project back to C channels
model(projection(model_input), timestep, text_embeddings)
```

### Initialization Trick (Critical)

The 1x1 projection conv must be zero-initialized for the condition channels:
```python
proj = nn.Conv2d(64, 32, kernel_size=1, bias=False)
proj.weight[:, :32, :, :] = torch.eye(32).unsqueeze(-1).unsqueeze(-1)  # identity
proj.weight[:, 32:, :, :] = 0.0  # condition starts as zero-contribution
```
This means at step 0 the model behaves exactly like the pretrained T2I model. The condition signal is learned gradually.

### Why NOT ControlNet?

| Approach | New params | Quality | Complexity |
|----------|-----------|---------|------------|
| Channel concat + 1x1 conv | ~1K params | Good for spatial-aligned tasks | Minimal |
| ControlNet | ~800M (full encoder copy) | Better for structural guidance | High |
| IP-Adapter | ~22M | Good for style/reference | Medium |

For restoration where input and output are **spatially identical**, channel concat is sufficient. ControlNet is overkill - the condition IS the image, just degraded.

Proven in: [[Step1X-Edit]], [[flux-kontext]], Palette (Google), InstructPix2Pix.

## Degradation Pipeline

Synthetic degradation from clean images. Apply 1-3 random degradations:

| Degradation | Parameters | Use Case |
|------------|------------|----------|
| Gaussian noise | σ = 5-50 | Camera noise |
| Poisson noise | scale = 1-5 | Low-light |
| JPEG artifacts | quality = 10-40 | Compression |
| Gaussian blur | kernel = 3-11 | Defocus |
| Downscale + upscale | factor = 2-4 | Low resolution |
| Color jitter | brightness/contrast ±0.2 | Color cast |

### Implementation (PIL/numpy only, no ML deps)

```python
def random_degradation(image, num_degradations=2):
    """Apply random degradation pipeline to PIL Image."""
    degradations = random.sample([
        lambda img: add_gaussian_noise(img, sigma=random.uniform(5, 50)),
        lambda img: add_jpeg_artifacts(img, quality=random.randint(10, 40)),
        lambda img: add_gaussian_blur(img, kernel=random.choice([3, 5, 7, 9, 11])),
        lambda img: add_downscale(img, factor=random.uniform(2, 4)),
    ], k=min(num_degradations, 4))
    for deg in degradations:
        image = deg(image)
    return image
```

## Dataset Strategy

### Size Guidelines

| Task | Pairs | Source |
|------|-------|--------|
| Denoising (general) | 17K-28K | DIV2K + Flickr2K, synthetic degradation |
| Retouching (domain) | 3K-5K | Before/after from Retouch4me or retoucher |
| Background replace | 150-300 | Paired photos or synthetic |

### PairedDataset Format

CSV: `image_path,condition_image_path,caption`

Both images MUST receive identical spatial augmentations (crop coords, flip state). Use shared random seed per sample.

### On-the-fly vs Pre-generated

- **On-the-fly**: more augmentation diversity, slower training, good for exploration
- **Pre-generated**: faster training (cache latents), fixed degradations, good for final runs
- **Recommendation**: on-the-fly for first experiments, pre-generate for production training

## Text Prompts for Restoration

The text condition describes the degradation to remove:
- "Remove gaussian noise from this image"
- "Remove JPEG compression artifacts, restore sharp details"
- "Enhance low-light image, recover shadows"
- Generic: "Restore this image to high quality"

Prompt diversity during training prevents overfitting to specific text patterns.

## Training Config (for [[SANA]] 1.6B)

```yaml
model:
  pretrained: "Efficient-Large-Model/SANA1.5_1.6B_1024px_diffusers"
  conditioning: "img2img"
  condition_channels: 32  # DC-AE latent channels
training:
  lr: 1e-5
  batch_size: 4
  steps: 10000
  optimizer: adamw8bit
  dtype: bf16
  ema_decay: 0.9999
data:
  type: paired_csv
  resolution: 512  # start small, curriculum to 1024
  degradation: on_the_fly
```

## Evaluation

| Metric | What it measures | Target |
|--------|-----------------|--------|
| PSNR | Pixel accuracy | > 30 dB (σ=25 noise) |
| SSIM | Structural similarity | > 0.85 |
| LPIPS | Perceptual similarity | < 0.1 |
| FID | Distribution quality | < 10 |
