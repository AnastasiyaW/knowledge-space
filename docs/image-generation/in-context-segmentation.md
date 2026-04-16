---
title: In-Context Segmentation
category: reference
tags: [segmentation, dinov3, few-shot, zero-shot, training-free, insid3, positional-bias, pca, semantic-correspondence]
---

# In-Context Segmentation

Segmenting images by example: provide one or more (image, mask) pairs and the model segments the same category in new images, without fine-tuning or retraining. Also called in-context segmentation (ICS) or few-shot segmentation.

## Key Facts

- Training-free ICS uses frozen vision backbone features to match semantics between reference and target
- DINOv3 dense features cluster into semantically coherent regions without any supervision (emergent from scale)
- RoPE positional encoding in DINOv3 creates stronger positional bias than DINOv2's learned embeddings - must be debiased for semantic correspondence
- PCA-based debiasing: project features onto the orthogonal complement of the positional subspace to separate position from semantics
- Multi-domain segmentation from a single model: natural images, medical (dermoscopy, lung), underwater, aerial, satellite
- INSID3 achieves 3.31 FPS vs. GF-SAM 0.97 FPS vs. Matcher 0.11 FPS - the training-free approach is also faster

## INSID3 (Training-Free, DINOv3)

**Paper:** arXiv:2603.28480 | **Code:** github.com/visinf/INSID3 | **Venue:** CVPR 2026 | **License:** Apache-2.0

### Architecture

```
Reference (image + mask)
    ↓
DINOv3 frozen backbone (ViT-S/B/L)
    ↓
Positional Bias Debiasing (PCA projection)
    ↓ semantic features, position-free
Semantic matching with target features
    ↓
Clustering → binary mask
    ↓
(Optional) CRF refinement for sharp boundaries
```

### Positional Bias Debiasing

DINOv3 uses RoPE (Rotary Position Embedding) instead of learned positional embeddings. Side effect: absolute pixel position is encoded more strongly in DINOv3 features than in DINOv2. Two semantically identical patches in different image regions get different feature vectors - this breaks cross-image semantic matching.

**Fix:** PCA-based projection onto the orthogonal complement of the positional subspace.

```python
def debias_positional(features: torch.Tensor, n_pos_components: int = 8) -> torch.Tensor:
    """
    features: (N, D) - N patch features from DINOv3
    Returns: position-debiased features of same shape
    """
    # Center features
    mu = features.mean(dim=0, keepdim=True)
    centered = features - mu
    
    # PCA: find positional subspace (low-rank components encoding position)
    U, S, Vh = torch.linalg.svd(centered, full_matrices=False)
    pos_subspace = Vh[:n_pos_components]  # (n_pos, D) - positional directions
    
    # Project out positional subspace (orthogonal complement projection)
    P = pos_subspace.T @ pos_subspace           # (D, D) positional projector
    debiased = centered - centered @ P          # remove positional component
    
    return debiased + mu
```

No learnable parameters - this is a purely linear operation applied at inference time.

### DINOv3 vs DINOv2 for Dense Tasks

| | DINOv2 | DINOv3 |
|---|---|---|
| Teacher params | ~1B | 7B (7x) |
| Training images | 142M | 1.7B (12x) |
| Positional encoding | Learned | RoPE |
| Dense features (ADE20K) | Baseline | +6 mIoU |
| High-res support | ~518px | Stable >4K |
| Gram Anchoring | No | Yes |

**Gram Anchoring** (new in DINOv3): anchors patch-level feature similarity to an early checkpoint. Prevents the common degeneration where long training improves global features but hurts patch-level semantic density.

### Usage

```python
from models import build_insid3  # from official repo

model = build_insid3(backbone='vitl')  # vitl gives best quality

# Single-example segmentation:
model.set_reference("reference.jpg", "reference_mask.png")
model.set_target("target.jpg")
mask = model.segment()  # (H, W) boolean

# Multi-shot (multiple reference examples improve consistency):
model.set_references([
    ("ref1.jpg", "mask1.png"),
    ("ref2.jpg", "mask2.png"),
])
mask = model.segment("target.jpg")
```

## Performance

### Benchmarks (One-Shot Segmentation)

| Method | Architecture | mIoU | FPS | Params | Fine-tuning |
|--------|-------------|------|-----|--------|-------------|
| INSID3 | DINOv3 ViT-L | **SOTA +7.5%** | 3.31 | 3x fewer | None |
| GF-SAM | DINO+SAM | — | 0.97 | — | None |
| Matcher | DINOv2 + decoder | — | 0.11 | — | Yes |
| PerSAM | SAM + adapter | — | — | — | Yes |

**Multi-domain coverage:** natural objects, medical imaging (ISIC skin lesions, lung CT), underwater (SUIM), aerial/satellite (iSAID)

**Multi-granularity:** whole objects, object parts, personalized instances

### Backbone Ablation

Replacing DINOv3 with alternatives degrades significantly:
- DINOv2: -6 mIoU on dense tasks
- Perception Encoder: below DINOv3
- Stable Diffusion 2.1 features: weakest

The quality gap validates that DINOv3's dense feature quality (not just the pipeline) is the key factor.

## Practical Applications

### Batch Annotation for Datasets

```python
from pathlib import Path

def annotate_batch(reference_img: str, reference_mask: str, 
                   target_dir: str, output_dir: str):
    """
    Annotate all images in target_dir using single reference.
    Useful for: LoRA dataset preparation, fine-tuning data collection.
    """
    model = build_insid3()
    model.set_reference(reference_img, reference_mask)
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for img_path in Path(target_dir).glob("*.jpg"):
        model.set_target(str(img_path))
        mask = model.segment()
        
        # Save as PNG mask
        mask_out = Path(output_dir) / (img_path.stem + "_mask.png")
        (mask * 255).astype("uint8")  # to PIL and save
```

### Part Segmentation Pipeline

```python
# Segment specific body parts or object components
# by providing a reference showing only that part's mask

parts = {
    "hair": ("ref_full.jpg", "ref_hair_mask.png"),
    "face": ("ref_full.jpg", "ref_face_mask.png"),
    "hands": ("ref_full.jpg", "ref_hands_mask.png"),
}

for part_name, (ref_img, ref_mask) in parts.items():
    model.set_reference(ref_img, ref_mask)
    part_mask = model.segment("target.jpg")
    save_mask(part_mask, f"target_{part_name}_mask.png")
```

### Quality Control

```python
def validate_mask_quality(mask, min_area_ratio=0.001, max_area_ratio=0.9):
    """Basic sanity checks for auto-generated masks."""
    area_ratio = mask.mean()
    
    if area_ratio < min_area_ratio:
        return "too_small"  # likely missed the object
    if area_ratio > max_area_ratio:
        return "too_large"  # likely leaked to background
    
    # Check connectivity (fragmented masks often indicate failure):
    from scipy import ndimage
    labeled, n_components = ndimage.label(mask)
    if n_components > 10:
        return "fragmented"  # noisy segmentation
    
    return "ok"
```

## When to Use INSID3 vs SAM

| Scenario | INSID3 | SAM (click-based) |
|----------|--------|-------------------|
| Batch annotation, same category | Best | Slow (needs clicks per image) |
| Novel/rare category | Good | N/A (requires prompt engineering) |
| Interactive click-based | Slow (3.31 FPS) | Better (<20ms per click) |
| Soft boundaries (hair, fur) | Needs CRF, human review | Also struggles |
| Medical imaging domain | Validated (ISIC, lung) | Often needs fine-tuning |
| Non-English labels | Works (vision-only) | Works |

## Setup

```bash
git clone https://github.com/visinf/INSID3
cd INSID3

# DINOv3 backbone weights (from Meta FAIR):
# https://github.com/facebookresearch/dinov3
# Download ViT-L weights for best quality

pip install -r requirements.txt
# PyTorch >= 2.0, Python 3.10, CUDA 12.6
```

## Gotchas

- **Reference selection is critical** - INSID3 transfers the visual semantics of YOUR reference mask, not a category name. A poorly cropped or ambiguous reference mask will produce poor results. Use tight, unambiguous reference masks with diverse visual examples of the target category
- **3.31 FPS means batch, not real-time** - at ~300ms per image, INSID3 is not suitable for interactive annotation or video. Use it for offline batch processing of large datasets
- **Soft/ambiguous boundaries need human review** - masks for hair, fur, transparent objects, and motion-blurred edges are systematically less accurate. CRF post-processing helps but doesn't solve the fundamental ambiguity; plan for human-in-the-loop on these categories
- **Positional debiasing requires calibration** - the number of PCA components to remove (`n_pos_components`) may need tuning per domain; too few leaves residual position encoding, too many removes semantic signal along with position

## See Also

- [[image-generation/sana-denoiser-architecture]] - related dense feature architectures
- [[data-science/cnn-computer-vision]] - CNN backbones used in segmentation
- [[data-science/attention-mechanisms]] - ViT attention used in DINOv3
