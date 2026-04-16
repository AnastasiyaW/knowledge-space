---
title: "Face Detection & Filtering Pipeline"
description: "Reusable pipeline for filtering image collections by face presence, quality, and type using YOLO, MediaPipe, CLIP, and VGG16"
---

# Face Detection & Filtering Pipeline

Reusable pipeline for filtering large image collections by face presence, quality, and type. Primary use case: dataset preparation for face-related LoRA training.

## Tool Chain

### 1. YOLO11n-face - Real Face Detection

Model: `AdamCodd/YOLOv11n-face-detection` (5.4 MB). Trained on WIDERFACE - detects only real human faces (no dolls, masks, illustrations).

```python
from ultralytics import YOLO

model = YOLO("yolov11n-face.pt")
results = model("image.jpg", conf=0.5)

for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        face_area = (x2 - x1) * (y2 - y1)
        image_area = r.orig_shape[0] * r.orig_shape[1]
        face_pct = face_area / image_area * 100
```

- Single class: `{0: 'face'}`
- ~40 img/s on RTX 4090, ~27 img/s mixed workload
- Filter by face area as % of image (e.g., >= 10% for portrait datasets)

### 2. MediaPipe selfie_multiclass - Face+Hair Segmentation

6-class pixel-level segmentation: 0=background, 1=hair, 2=body, 3=face, 4=clothes, 5=accessories.

```python
import mediapipe as mp
import numpy as np

model = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

# Process image (RGB)
result = model.process(image_rgb)
mask = result.segmentation_mask  # float32, values 0-1

# Calculate face+hair area
face_hair_pct = np.mean(mask > 0.5) * 100
```

- CPU only (TFLite), ~20 img/s with 4 ProcessPoolExecutor workers
- Detects "face texture" on dolls/illustrations - use YOLO first to filter real faces

### 3. Glasses Detection via Mask Overlap

```python
# Face mask (category 3) AND accessories mask (category 5) overlap > 3% = glasses
face_mask = (segmentation == 3).astype(float)
acc_mask = (segmentation == 5).astype(float)
overlap = np.sum(face_mask * acc_mask) / max(np.sum(face_mask), 1)
has_glasses = overlap > 0.03  # earrings/necklaces don't trigger (outside face region)
```

### 4. CLIP ViT-B/32 - Photo vs Drawing Classification

Zero-shot classification separating photographs from illustrations/drawings/3D renders.

```python
import clip
import torch

model, preprocess = clip.load("ViT-B/32")

photo_prompts = ["photograph of a person", "real photo of a human face"]
drawing_prompts = ["drawing of a person", "illustration", "painting", "3d render"]

# Batch inference: ~27 img/s on RTX 4090
# Threshold 0.55 works well for photo/drawing split
```

Use multiple prompts per category and average similarities for robust classification.

### 5. VGG16 fc6 - Image Deduplication

Extract 4096-dim features from VGG16 fc6 layer, L2 normalize, compute cosine similarity.

```python
import torch
from torchvision.models import vgg16

model = vgg16(pretrained=True)
model.classifier = model.classifier[:2]  # truncate after fc6
model.eval()

# GPU feature extraction: ~1400 img/s
# CPU comparison ~10 min for 90K images
```

**Progressive dedup thresholds:**

| Threshold | Detects |
|-----------|---------|
| 0.95 | Exact duplicates (rescaled, recompressed) |
| 0.90 | Near-duplicates (slight crop, color shift) |
| 0.85 | Similar poses (same subject, same angle) |

Use chunked matrix multiplication for large collections to avoid OOM on NxN similarity matrix.

### 6. HSEmotion - Emotion Classification

Model: `enet_b2_8` (EfficientNet-B2, AffectNet trained). 8 emotions: Anger, Contempt, Disgust, Fear, Happiness, Neutral, Sadness, Surprise.

```python
# Requires specific versions:
# pip install timm==0.9.16  (newer timm breaks it)

import torch
# Patch required for loading:
torch.serialization.add_safe_globals([...])
# Or: torch.load(path, weights_only=False, map_location='cpu')
```

On glamour/processed photos, emotion models disagree heavily between each other. Use single model (HSEmotion) rather than ensemble for consistency.

## Pipeline Example

Typical filtering cascade with yield at each stage:

```
42,910 source images
  -> 24,655 (MediaPipe face+hair >= 10% of image)
  -> 16,961 (YOLO11 real face >= 10% of image)
  -> 14,309 (CLIP photo classification, threshold 0.55)
  -> deduplicated with VGG16 at 0.90
```

Each stage runs independently - can parallelize with ProcessPoolExecutor.

## Performance Patterns

### HDD vs SSD for Large Collections

```python
# os.listdir() on 43K files on HDD: ~7 minutes
# os.scandir() is faster than Path.glob() for large dirs
# Cache file lists to JSON for repeat runs

import json
from pathlib import Path

cache_path = Path("filelist_cache.json")
if cache_path.exists():
    files = json.loads(cache_path.read_text())
else:
    files = [str(p) for p in Path("images/").iterdir() if p.suffix in ('.jpg', '.png')]
    cache_path.write_text(json.dumps(files))
```

### PyTorch + TensorFlow Conflict

DeepFace (TensorFlow) can silently overwrite CUDA PyTorch with CPU-only version during install.

```bash
# Always verify after installing TF packages:
python -c "import torch; print(torch.cuda.is_available())"

# Fix if broken:
pip install torch==2.6.0+cu124 --index-url https://download.pytorch.org/whl/cu124
```

## Gotchas

- **MediaPipe detects non-real faces**: unlike YOLO11n-face (trained on WIDERFACE for real faces only), MediaPipe will trigger on doll faces, mannequins, face masks, and face-like illustrations. Always run YOLO detection first, then MediaPipe only on confirmed real-face images.
- **HSEmotion requires timm==0.9.16**: newer timm versions break the model loading. Pin the version explicitly in requirements. Also requires `weights_only=False` in `torch.load()` which is a security consideration for untrusted model files.
- **VGG16 dedup OOM on large sets**: for N > 50K images, computing the full NxN similarity matrix will OOM. Use chunked matrix multiplication (process 1000x1000 blocks at a time) or approximate nearest neighbor search.

## See Also

- [[diffusion-lora-training]] - dataset preparation for LoRA training
- [[in-context-segmentation]] - INSID3 for batch annotation by example
- [[flux-klein-9b-inference]] - inference settings for generated image quality
