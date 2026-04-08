---
title: Neural Networks for Grayscale Overlay Prediction
category: reference
tags: [image-restoration, nafnet, restormer, u-net, retouching, dodge-burn, soft-light, regression, image-to-image]
---

# Neural Networks for Grayscale Overlay Prediction

Predicting single-channel grayscale overlay maps for Photoshop Soft Light blending - a pixel-aligned regression task. Architectures, loss functions, training strategy, and inference patterns for professional retouching overlays.

## Task Definition

**Input:** RGB photo (portrait/fashion)
**Output:** Single-channel grayscale map, values centered at 128 (0.5 normalized)
- Brighter than 128 = lighten in Soft Light blend
- Darker than 128 = darken in Soft Light blend
- 128 = no change (neutral mid-gray)

Fundamentally a **residual prediction task**: predict deviation from neutral gray, not absolute pixel values.

## Architecture Comparison

| Architecture | Params | Inference 512² | Smoothness | Global Context | Impl. Difficulty |
|---|---|---|---|---|---|
| NAFNet-w32 | ~17M | ~30ms | Excellent | Good | Medium |
| U-Net+ConvNeXt-T | ~30M | ~40ms | Good | Moderate | Low (smp) |
| Restormer | ~26M | ~150ms | Good | Excellent | Medium |
| SCUNet | ~18M | ~50ms | Very Good | Good | Medium |
| SwinIR | ~12M | ~70ms | Good | Good | Medium |
| HDRNet | ~1M | ~5ms | Very Good | Limited | Medium |
| Pix2Pix | ~54M | ~30ms | Poor | Moderate | High |

## Recommended Architectures

### NAFNet (Primary)

Nonlinear Activation Free Network - replaces all nonlinear activations with SimpleGate (elementwise multiply), producing inherently smoother feature maps. Critical for artifact-free overlay maps.

```python
# Clone: https://github.com/megvii-research/NAFNet
# Modification for single-channel output:

from basicsr.models.archs.NAFNet_arch import NAFNet

model = NAFNet(
    img_channel=3,         # RGB input
    width=32,              # width32 variant (~17M params)
    middle_blk_num=1,
    enc_blks=[1, 1, 1, 28],
    dec_blks=[1, 1, 1, 1],
)
# Replace output conv:
import torch.nn as nn
model.ending = nn.Conv2d(32, 1, kernel_size=3, padding=1)  # single channel out

# Residual init: init bias to 0 so initial output is exactly 0 (mid-gray offset)
nn.init.zeros_(model.ending.bias)
```

**Why:** SimpleGate (no ReLU/GELU) avoids sharp activation artifacts. Empirically produces smoother outputs than any other architecture for this task.

### U-Net + Pretrained Backbone (Baseline)

Fastest path to a working baseline with 23K dataset.

```python
import segmentation_models_pytorch as smp

model = smp.Unet(
    encoder_name='efficientnet-b4',    # strong baseline
    encoder_weights='imagenet',
    in_channels=3,
    classes=1,
    activation=None,                   # raw logits, clamp manually
)

# Or ConvNeXt-Tiny for modern CNN features:
model = smp.Unet(
    encoder_name='tu-convnextv2_tiny',
    encoder_weights='imagenet',
    in_channels=3,
    classes=1,
)

# U-Net++ for better multi-scale fusion:
model = smp.UnetPlusPlus(encoder_name='efficientnet-b4', ...)
```

**Output normalization:**
```python
# Option A: sigmoid -> remap to [0, 255] centered at 128
output = torch.sigmoid(raw_logits)          # [0, 1]
overlay = (output * 255).clamp(0, 255)      # [0, 255], 0.5 = 128

# Option B: tanh -> offset from mid-gray (residual formulation)
output = torch.tanh(raw_logits) * 0.5 + 0.5  # [-0.5, 0.5] + 0.5 = [0, 1]
overlay = (output * 255).clamp(0, 255)
```

### Restormer (Global Context Variant)

Best for Volume enhancement tasks needing full-face 3D structure understanding. Uses channel-wise attention (linear complexity) instead of spatial attention (quadratic).

```python
# Clone: https://github.com/swz30/Restormer
# Key modification: reduce model size to prevent overfitting on 23K samples

model = Restormer(
    inp_channels=3,
    out_channels=1,          # single channel output
    dim=24,                  # reduced from 48 for smaller dataset
    num_blocks=[2,2,4,8],    # fewer blocks
    heads=[1,2,4,8],
    ffn_expansion_factor=2.66,
    LayerNorm_type='BiasFree',
)
```

## Loss Functions

### Recommended Combination

```python
import torch
import torch.nn.functional as F

class OverlayLoss(torch.nn.Module):
    def __init__(self, tv_weight=0.005):
        super().__init__()
        self.tv_weight = tv_weight
    
    def ms_ssim_loss(self, pred, target):
        # Use pytorch_msssim library
        from pytorch_msssim import ms_ssim
        return 1 - ms_ssim(pred, target, data_range=1.0, size_average=True)
    
    def tv_loss(self, pred):
        dx = torch.abs(pred[:, :, :, 1:] - pred[:, :, :, :-1])
        dy = torch.abs(pred[:, :, 1:, :] - pred[:, :, :-1, :])
        return dx.mean() + dy.mean()
    
    def forward(self, pred, target):
        l1 = F.l1_loss(pred, target)
        ssim = self.ms_ssim_loss(pred, target)
        tv = self.tv_loss(pred)
        
        # Best combo from image restoration literature:
        return 0.84 * ssim + 0.16 * l1 + self.tv_weight * tv
```

**Loss ranking for this task:**
1. `L1` - primary, stable, sharper than L2
2. `MS-SSIM + L1` (0.84/0.16 split) - preserves multi-scale structure
3. `TV regularization` (weight 0.001-0.01) - smoothness penalty
4. `Smooth L1 / Huber` - good when most pixels near mid-gray
5. `Perceptual loss` - only on composited result, NOT raw grayscale map (VGG features meaningless for gradient maps)
6. `Adversarial loss` - last resort; PatchGAN pushes toward sharpness, counterproductive for smooth overlays

## Training Strategy

### Residual Formulation

```python
# Train to predict OFFSET from 0.5, not absolute value
# This initializes network to output neutral (no-op) overlay

def predict_overlay(model, img):
    raw = model(img)              # model learns to output ~0 initially
    offset = torch.tanh(raw)     # [-1, 1]
    overlay = offset * 0.5 + 0.5 # [0, 1], centered at 0.5
    return overlay

# Loss computed on offset, not absolute:
loss = criterion(offset_pred, offset_target)  # offset_target = (target - 0.5) / 0.5
```

### Progressive Training

```python
schedule = [
    {"size": 256, "lr": 1e-3, "epochs": 50},
    {"size": 384, "lr": 3e-4, "epochs": 30},
    {"size": 512, "lr": 1e-4, "epochs": 20},
]

optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100, eta_min=1e-6)

# EMA for stable inference:
from torch_ema import ExponentialMovingAverage
ema = ExponentialMovingAverage(model.parameters(), decay=0.999)
# After each optimizer step: ema.update()
# At inference: with ema.average_parameters(): ...
```

### Data Augmentation

```python
import albumentations as A

# Safe (preserve overlay alignment):
safe_transforms = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomCrop(256, 256),
    A.Rotate(limit=15, p=0.3),
    # Brightness on INPUT only, not target:
], additional_targets={"target": "image"})

# Dangerous (break overlay semantics):
# - Color jitter on both (invalidates target)
# - Vertical flip (unnatural faces)
# - MixUp / CutMix (produces invalid overlay combinations)
# - Elastic distortion (misaligns skin features)
```

## Conditioning: One Model vs Two

**Two separate models** (recommended start):
- Simpler, faster to iterate
- `23K → ~11.5K per model` still sufficient

**One model with FiLM conditioning:**
```python
class FiLM(torch.nn.Module):
    def __init__(self, feature_dim: int, condition_dim: int = 2):
        super().__init__()
        self.scale = torch.nn.Linear(condition_dim, feature_dim)
        self.shift = torch.nn.Linear(condition_dim, feature_dim)
    
    def forward(self, x, condition):
        # condition: one-hot [0,1] = D&B, [1,0] = Volume
        gamma = self.scale(condition).unsqueeze(-1).unsqueeze(-1)
        beta  = self.shift(condition).unsqueeze(-1).unsqueeze(-1)
        return x * (1 + gamma) + beta  # scale/shift feature maps
```

## High-Resolution Inference (Tiling)

```python
def inference_tiled(model, img: torch.Tensor, tile: int = 512, overlap: int = 64):
    """Overlap-and-blend tiling for full-resolution inference."""
    B, C, H, W = img.shape
    result = torch.zeros(B, 1, H, W, device=img.device)
    weight = torch.zeros(B, 1, H, W, device=img.device)
    
    for y in range(0, H, tile - overlap):
        for x in range(0, W, tile - overlap):
            y2, x2 = min(y + tile, H), min(x + tile, W)
            patch = img[:, :, y:y2, x:x2]
            
            with torch.no_grad():
                pred = model(patch)
            
            # Cosine blending window to avoid seams:
            win_h = torch.hann_window(y2 - y, device=img.device)
            win_w = torch.hann_window(x2 - x, device=img.device)
            w = win_h.unsqueeze(1) * win_w.unsqueeze(0)
            
            result[:, :, y:y2, x:x2] += pred * w
            weight[:, :, y:y2, x:x2] += w
    
    return result / weight.clamp(min=1e-8)
```

## Experiment Order

1. **U-Net + EfficientNet-B4** - baseline PSNR/SSIM, understand data difficulty (1-2 days)
2. **NAFNet-w32** - primary architecture, compare with baseline (2-3 days)
3. **Restormer-lite** - for Volume variant, test global coherence (3-4 days)
4. **FiLM conditioning** - single model covering both variants (2 days)
5. **Loss ablation** - L1 vs L1+TV vs MS-SSIM+L1 on best architecture
6. **High-res tiling** - for full-resolution deployment

## Gotchas

- **GANs are counterproductive here** - PatchGAN discriminators push toward sharpness (high-frequency detail), but overlay maps must be smooth. Introducing adversarial loss creates checkerboard artifacts that ruin the Soft Light blend. Only add if L1-trained outputs are provably too blurry, and use very low weight (lambda_GAN 0.01-0.05)
- **Perceptual loss on raw map is meaningless** - VGG features were trained to recognize RGB image semantics, not grayscale gradient maps. Compute perceptual loss on the COMPOSITED result (apply predicted overlay to input, compare with target-composited) if using it at all
- **Vertical flip breaks face models** - upside-down faces are out-of-distribution for most pretrained encoders and produce pathological predictions. Only use horizontal flip
- **NAFNet was designed for 256² patches** - for high-res inference, use tiling with at least 64px overlap and blend with a Hann window to avoid visible seams at tile boundaries
- **IVFFlat nprobe** - (if using FAISS for embedding search in the training data pipeline): default nprobe=1 gives poor recall; set to n_lists/4 for production

## See Also

- [[image-generation/Image Restoration Survey]] - broader restoration architectures
- [[image-generation/Paired Training for Restoration]] - paired dataset training strategies
- [[image-generation/LoRA Fine-Tuning for Editing Models]] - adaptation of generalist models
