---
title: Defect Detection and Small Object Detection
category: reference
tags: [defect-detection, anomaly, efficientad, yolo, anomalib, small-objects, jewelry]
aliases: ["Anomaly Detection", "Defect Detection Models", "Small Object Detection"]
---

# Defect Detection and Small Object Detection

Reference for detecting defects (scratches, dust, surface anomalies) and small objects in high-resolution images. Focuses on <2GB VRAM constraints and jewelry/skin domain.

## Model Overview

| Model | Type | Speed | VRAM | AUROC | Use Case |
|-------|------|-------|------|-------|---------|
| EfficientAD | Anomaly (unsupervised) | <100ms | <2GB | 98.9% | Surface defects, no labels needed |
| PatchCore | Anomaly (unsupervised) | 200-500ms | 2-4GB | 99.1% | Highest accuracy, more VRAM |
| PP-YOLOE-SOD-S | Detection (supervised) | Fast | <2GB | 38.5 mAP* | Small objects, labeled dataset |
| Siamese change-aware | Detection (supervised) | Varies | 2-4GB | - | Before/after change detection |

*VisDrone-S benchmark

## EfficientAD (WACV 2024)

Best choice for surface defect detection without labeled training data.

```python
from anomalib.models import EfficientAd
from anomalib.data import MVTec
from anomalib.engine import Engine

# Training (on normal/defect-free samples only)
model = EfficientAd()
datamodule = MVTec(root="data/", category="jewelry")
engine = Engine()
engine.fit(model=model, datamodule=datamodule)

# Inference
engine.test(model=model, datamodule=datamodule)
```

**Key specs:**
- Inference: sub-100ms on single image
- VRAM: <2GB (runs on GT1030/GTX 1650)
- Training: only needs normal samples (no defect labels)
- Produces pixel-level anomaly maps (heatmaps)
- Architecture: efficient student-teacher with PDN (Patch Description Network)

### EfficientAD vs PatchCore Trade-off

| Aspect | EfficientAD | PatchCore |
|--------|-------------|----------|
| AUROC | 98.9% | 99.1% |
| Inference speed | <100ms | 200-500ms |
| VRAM | <2GB | 2-4GB |
| Memory bank | No | Yes (grows with dataset) |
| Best for | Real-time inspection | Maximum accuracy batch |

## Anomalib Framework (Intel)

Unified framework covering 20+ anomaly detection models:

```bash
pip install anomalib
anomalib train --model EfficientAd --data MVTec --data.category bottle
anomalib test --model EfficientAd --data MVTec
```

**Supported models**: EfficientAD, PatchCore, FastFlow, STFPM, CFlow, WinCLIP, and more.

```python
from anomalib.models import Padim, Patchcore, EfficientAd, FastFlow
from anomalib.data import Folder  # custom folder structure

# Custom dataset
datamodule = Folder(
    root="data/jewelry/",
    normal_dir="normal/",
    abnormal_dir="defects/",
    task="segmentation",  # or "classification"
    image_size=(256, 256),
)
```

## PP-YOLOE-SOD-S (Baidu PaddleDetection)

Optimized for small object detection. Fits 2GB VRAM.

```python
# Install PaddlePaddle + PaddleDetection
pip install paddlepaddle-gpu paddledet

# Config for small objects
configs/smalldet/ppyoloe_plus_sod_s_80e_sliced_visdrone_640_025.yml

# Training on custom data
python tools/train.py -c configs/smalldet/... \
  --slim_config configs/slim/prune/... \
  -o TrainReader.batch_size=8
```

**Key features:**
- SOD (Small Object Detection) variants use tiling inference internally
- 38.5 mAP on VisDrone-S (small drone objects, challenging benchmark)
- S model: fits 2GB VRAM at batch=1

## Siamese Change-Aware Detection (Nature 2025)

For detecting changes between before/after image pairs — useful for defect monitoring after processing:

```python
# Conceptual: siamese encoder for change detection
class SiameseChangeDetector(nn.Module):
    def __init__(self, encoder):
        super().__init__()
        self.encoder = encoder  # shared weights
        self.change_head = nn.Sequential(
            nn.Conv2d(512, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 1, 1),
        )

    def forward(self, img_before, img_after):
        feat_a = self.encoder(img_before)
        feat_b = self.encoder(img_after)
        diff = torch.abs(feat_a - feat_b)
        return self.change_head(diff)
```

**Use case**: inspect image before and after post-processing to detect introduced artifacts or changes.

## Jewelry-Specific Considerations

### Domain Challenges

| Challenge | Impact | Mitigation |
|-----------|--------|-----------|
| Specular highlights | Fake anomalies on reflective metal | Mask by specular map before detection |
| Gemstone facets | Regular high-frequency patterns | Train per-region models |
| Scale variation | Micro-scratches vs macro-scratches | Multi-scale inference / tiling |
| Background reflections | Ghost edges | Controlled background (velvet) in capture |

### Recommended Pipeline

```
1. EfficientAD for anomaly heatmap (unsupervised, fast)
2. Threshold heatmap → candidate regions
3. YOLO / PP-YOLOE-SOD for classification of candidates
4. Optional: Siamese comparison if before/after pairs available
```

### Training Data

- **Normal samples**: 100-200 defect-free images per product category
- **Defect examples**: needed for PP-YOLOE, not needed for EfficientAD
- **Annotation format**: COCO JSON (pixel masks) for segmentation; YOLO .txt for boxes
- **Augmentation**: avoid geometric transforms that create fake texture artifacts

## Tiling for High-Resolution Input

Defect images are often 8-24MP. All models above work best at 640-1024px input.

```python
import sahi  # Slicing Aided Hyper Inference

from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

model = AutoDetectionModel.from_pretrained(
    model_type="yolov8",
    model_path="pp_yoloe_sod.pt",
    confidence_threshold=0.3,
    device="cuda",
)

result = get_sliced_prediction(
    "jewelry_8mp.jpg",
    model,
    slice_height=640,
    slice_width=640,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2,
)
```

## Gotchas

- **EfficientAD memory bank**: unlike PatchCore, EfficientAD does not use a growing memory bank — this is why it's fast and low-VRAM, but means it can't be updated incrementally without retraining.
- **Per-category training required**: anomaly models are trained per product category. A model trained on gold rings will not perform well on gemstone pendants — different normal texture distributions.
- **Specular masking**: for jewelry, specular highlights score as high anomalies in EfficientAD. Pre-mask specular regions using highlight detection (HSV V>240, S<30) before feeding to anomaly model.
- **PP-YOLOE-SOD requires labeled data**: unlike EfficientAD, PP-YOLOE needs bounding box annotations for each defect type. Plan for annotation pipeline before choosing this approach.
- **Tiling tile size vs model training**: if using SAHI tiling at inference, the model must have been trained at a compatible resolution. Mismatched tile sizes cause degraded accuracy.

## See Also

- [[skin-retouch-pipeline]] - skin defect detection (INSID3, YOLOE, LaMa)
- [[low-vram-inference-strategies]] - running models on <2GB VRAM
- [[tiled-inference]] - tiling strategies for high-resolution images
- [[color-theory-for-ml]] - color anomaly in quality inspection context
