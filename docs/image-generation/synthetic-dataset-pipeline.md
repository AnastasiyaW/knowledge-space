---
title: Synthetic Dataset Pipeline for Object Detection
category: pipelines
tags: [dataset, yolo, sam, synthetic, annotation, deduplication, clip, florence2]
---

# Synthetic Dataset Pipeline for Object Detection

Pipeline for building high-quality annotated datasets for YOLO + SAM fine-tuning from raw image collections. Focused on small/specialized object domains (gemstones, products, defects). Five-phase workflow: clean → analyze → annotate → review → train.

## Phase 1: Dataset Cleaning

### 1.1 Deduplication (Embedding-Based)

```python
import torch
from transformers import CLIPModel, CLIPProcessor
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

def get_embeddings(image_paths, batch_size=64):
    embeddings = []
    for i in range(0, len(image_paths), batch_size):
        batch = [Image.open(p) for p in image_paths[i:i+batch_size]]
        inputs = processor(images=batch, return_tensors="pt", padding=True)
        with torch.no_grad():
            feats = model.get_image_features(**inputs)
        embeddings.append(feats.cpu().numpy())
    return np.vstack(embeddings)

# Find duplicates
sim_matrix = cosine_similarity(embeddings)
np.fill_diagonal(sim_matrix, 0)
dup_pairs = np.argwhere(sim_matrix > 0.95)  # threshold configurable
# Keep highest-quality from each pair (resolution × file_size as proxy)
```

**Threshold guidance:**
- 0.98+: near-exact duplicates only
- 0.95: catches most visual duplicates (recommended)
- 0.90: aggressive dedup, may remove valid variations

### 1.2 Quality Filtering

```python
from brisque import BRISQUE
import cv2

brisque = BRISQUE()

def quality_filter(image_path, min_resolution=512, max_brisque=40):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    if min(h, w) < min_resolution:
        return False
    score = brisque.score(img)
    return score < max_brisque  # lower score = better quality

# Alternative: JPEG artifact detection via DCT block analysis
def has_jpeg_artifacts(img, threshold=5.0):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)
    blocks = [gray[r:r+8, c:c+8] for r in range(0,gray.shape[0],8) 
              for c in range(0,gray.shape[1],8) if gray[r:r+8,c:c+8].shape == (8,8)]
    dct_blocks = [cv2.dct(b.astype(np.float32)) for b in blocks]
    block_noise = np.mean([np.std(b[4:, 4:]) for b in dct_blocks])
    return block_noise < threshold
```

## Phase 2: Color Analytics

For domain-specific object discovery (gemstones, products):

```python
from sklearn.cluster import KMeans
import cv2

def analyze_object_colors(image, mask, n_clusters=8):
    """Extract dominant colors from masked region."""
    masked_pixels = image[mask > 0]
    lab_pixels = cv2.cvtColor(
        masked_pixels.reshape(1, -1, 3).astype(np.uint8),
        cv2.COLOR_RGB2LAB
    )[0]
    
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(lab_pixels)
    
    # Map cluster centers to prompt vocabulary
    return cluster_to_prompt_map(kmeans.cluster_centers_)
```

Output: `color_prompt_map.json` - maps color clusters to optimal detection prompts for SAM/Florence2.

## Phase 3: Auto-Annotation

### Method A: SAM3 with Prompt Conditioning (Primary)

```python
# SAM3 Pipeline Conditioning (per-image)
def annotate_with_sam3(image_path, prompts, pipeline):
    """
    prompts: list of text prompts from color_prompt_map.json
    pipeline: ComfyUI SAM3 pipeline
    """
    results = []
    for prompt in prompts:
        boxes, masks, scores = pipeline.run(
            image=image_path,
            prompt=prompt,
            output_format="json"
        )
        results.extend(zip(boxes, masks, scores))
    
    # Keep predictions above confidence threshold
    return [(box, mask, score) for box, mask, score in results if score > 0.85]
```

Store: JSON per image with boxes + masks (PNG) + scores + prompts + dominant colors.

### Method B: Florence-2 + SAM 2.1 (Cross-Validation)

```python
from transformers import AutoProcessor, AutoModelForCausalLM
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

# Florence-2: open-vocabulary object detection
florence = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-large")
boxes = florence_detect(image, task="<OD>", prompt="gemstone")

# SAM2.1: boxes → pixel-precise masks
sam2 = SAM2ImagePredictor(build_sam2("sam2.1_hiera_large.pt"))
masks = sam2.predict(image, box=boxes, multimask_output=False)
```

Use for cross-validation against SAM3 annotations. Flag disagreements for human review.

### Method C: Caption-Based Vocabulary Expansion

```python
# Generate descriptions → extract new prompts → re-annotate
captions = florence_caption(image, task="<CAPTION>")
new_prompts = parse_object_vocabulary(captions)  # NLP extraction
# A/B test new vs existing prompts on held-out images
```

## Phase 4: Review Tool

Minimal HTML/JS annotation reviewer (no server required):

```javascript
// Key features for production review:
// 1. Arrow key navigation (← →)
// 2. Canvas overlay showing all bboxes
// 3. Drag to resize/reposition bbox
// 4. Delete key: remove false positives
// 5. Click canvas: add missed annotations
// 6. Approve/Reject per image (keyboard shortcuts)
// 7. Export to YOLO .txt format

// YOLO export format:
// <class_id> <cx> <cy> <w> <h>  (normalized 0-1)
function exportToYOLO(annotation) {
    const {bbox, class_id, img_w, img_h} = annotation;
    const cx = (bbox.x + bbox.w/2) / img_w;
    const cy = (bbox.y + bbox.h/2) / img_h;
    return `${class_id} ${cx} ${cy} ${bbox.w/img_w} ${bbox.h/img_h}`;
}
```

## Phase 5: YOLO Training

```yaml
# data.yaml
path: /data/dataset
train: images/train
val: images/val
nc: 3  # number of classes
names: ['diamond', 'ruby', 'emerald']
```

```bash
# Training
yolo train \
  model=yolov8m.pt \
  data=data.yaml \
  epochs=100 \
  imgsz=640 \
  batch=16 \
  device=0

# Evaluation
yolo val model=runs/detect/train/weights/best.pt data=data.yaml
# Report: mAP@0.5, mAP@0.5:0.95, precision, recall
```

**Hardware allocation:**
- Dedup + quality filter: CPU or consumer GPU (CLIP inference, ~RTX 4090)
- SAM3 annotation: H100/H200 for large batches
- YOLO training: RTX 4090 adequate for most configs

## Dataset Quality Metrics

| Metric | Target | How to Check |
|--------|--------|-------------|
| Dedup rate | <5% duplicates remain | CLIP sim histogram |
| Annotation coverage | >90% true objects annotated | Sample 100, manual count |
| False positive rate | <10% | Review tool statistics |
| Inter-annotator agreement | >0.85 IoU on 50 shared images | If multiple annotators |
| mAP@0.5 on val | >0.7 for specialized domain | YOLO eval output |

## Gotchas

- **CLIP dedup misses semantic duplicates with different backgrounds**: two photos of same ring, one on white velvet, one on marble, get cosine ~0.75 (not caught). Supplement with perceptual hashing for exact duplicates.
- **SAM3 annotation quality depends heavily on prompt vocabulary**: generic prompts ("object", "item") give poor masks. Domain-specific prompts ("round brilliant cut diamond", "oval ruby") improve masks dramatically.
- **Florence-2 open-set detection hallucinates with very small objects**: objects <50×50px at 640px resolution get missed or produce garbage boxes. Use SAM3 or manual annotation for micro-details.
- **BRISQUE scores vary significantly by domain**: the default thresholds calibrated on natural images are wrong for product photography (often scored as "low quality" due to clean backgrounds). Calibrate threshold on 50 manual quality-labeled images from your domain.
- **YOLO imgsz=640 vs 1024**: YOLOv8 default is 640. For small objects (gemstones, jewelry detail), training at 1024 improves mAP@0.5:0.95 by 5-15% at 2× memory cost.

## See Also

- [[flux-klein-jewelry-photography]] - how this dataset feeds jewelry LoRA training
- [[face-detection-filtering-pipeline]] - detection pipelines for quality gating
- [[Diffusion LoRA Training]] - using annotated datasets for LoRA training
