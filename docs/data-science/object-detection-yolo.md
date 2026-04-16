---
title: Object Detection and YOLO
category: concepts
tags: [data-science, computer-vision, yolo, object-detection, cnn, tracking]
---

# Object Detection and YOLO

Object detection finds and classifies multiple objects in images with bounding boxes. Two families: two-stage (R-CNN family - accurate but slow) and one-stage (YOLO, SSD - fast, good for real-time). YOLO (You Only Look Once) dominates practical applications.

## Detection Paradigms

**Two-stage detectors**: first propose regions, then classify each.
- R-CNN -> Fast R-CNN -> Faster R-CNN (Region Proposal Network)
- More accurate on small objects, slower inference

**One-stage detectors**: predict boxes and classes in single pass.
- YOLO family, SSD, RetinaNet
- Faster, better for real-time applications
- Anchor-free variants (FCOS, CenterNet) eliminate anchor box design

## YOLO Evolution

| Version | Key Innovation | FPS (GPU) |
|---------|---------------|-----------|
| YOLOv1 | Single-pass detection | ~45 |
| YOLOv3 | Multi-scale detection, Darknet-53 | ~30 |
| YOLOv5 | PyTorch native, production-ready | ~140 |
| YOLOv8 | Anchor-free, decoupled head | ~160 |
| YOLOv11 | C3k2 blocks, attention mechanisms | ~180 |
| YOLOv12 | Area attention, R-ELAN blocks | ~190 |

## YOLOv8/v11 with Ultralytics

### Training Custom Detector

```python
from ultralytics import YOLO

# Load pretrained model
model = YOLO("yolov8n.pt")  # nano (fastest), s, m, l, x (most accurate)

# Train on custom dataset
results = model.train(
    data="dataset.yaml",     # path to data config
    epochs=100,
    imgsz=640,
    batch=16,
    device=0,                # GPU index
    patience=20,             # early stopping
    augment=True,
    mosaic=1.0,              # mosaic augmentation
    mixup=0.1,
    lr0=0.01,
    weight_decay=0.0005,
    project="runs/detect",
    name="custom_v1"
)
```

### Dataset Format (YOLO)

```yaml
# dataset.yaml
path: /data/my_dataset
train: images/train
val: images/val
test: images/test

names:
  0: person
  1: car
  2: bicycle
```

Label files (one per image, same name .txt):
```markdown
# class_id center_x center_y width height (all normalized 0-1)
0 0.5 0.4 0.3 0.6
1 0.2 0.7 0.15 0.2
```

### Inference

```python
model = YOLO("best.pt")

# Single image
results = model("image.jpg", conf=0.25, iou=0.45)

# Process results
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = box.conf[0].item()
        class_id = int(box.cls[0].item())
        class_name = model.names[class_id]
        print(f"{class_name}: {confidence:.2f} at [{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}]")

# Export for deployment
model.export(format="onnx", imgsz=640, half=True)
```

### Object Tracking

```python
# Built-in tracking with ByteTrack or BoT-SORT
results = model.track(
    source="video.mp4",
    tracker="bytetrack.yaml",
    persist=True,            # maintain track IDs across frames
    conf=0.3,
    iou=0.5
)

for result in results:
    if result.boxes.id is not None:
        track_ids = result.boxes.id.int().cpu().tolist()
        boxes = result.boxes.xyxy.cpu().numpy()
```

## Evaluation Metrics

- **IoU (Intersection over Union)**: overlap between predicted and ground truth box. IoU > 0.5 = correct detection (standard)
- **mAP@50**: mean Average Precision at IoU threshold 0.5
- **mAP@50:95**: averaged over IoU thresholds 0.5 to 0.95 (step 0.05). Stricter metric
- **Precision/Recall** per class at chosen confidence threshold

```python
# Validate model
metrics = model.val(data="dataset.yaml")
print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")
```

## Data Augmentation for Detection

```python
# Ultralytics built-in augmentations (in training config)
augmentation_params = {
    "hsv_h": 0.015,    # hue
    "hsv_s": 0.7,      # saturation
    "hsv_v": 0.4,      # value
    "degrees": 10,      # rotation
    "translate": 0.1,
    "scale": 0.5,
    "shear": 2.0,
    "flipud": 0.0,     # vertical flip (set 0 if orientation matters)
    "fliplr": 0.5,     # horizontal flip
    "mosaic": 1.0,     # 4-image mosaic
    "mixup": 0.1,      # image blending
    "copy_paste": 0.1, # instance copy-paste
}
```

**Mosaic augmentation**: combines 4 training images into one. Helps detect small objects and reduces batch size requirements. Disable in last 10 epochs for best results.

## Deployment

### ONNX Runtime Inference

```python
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("best.onnx", providers=["CUDAExecutionProvider"])

# Preprocess
input_tensor = preprocess_image(image, imgsz=640)  # resize, normalize, CHW

# Run inference
outputs = session.run(None, {"images": input_tensor})

# Post-process (NMS)
boxes, scores, class_ids = postprocess(outputs, conf_threshold=0.25, iou_threshold=0.45)
```

### TensorRT for Maximum Speed

```python
# Export from Ultralytics
model.export(format="engine", imgsz=640, half=True, device=0)

# Load TensorRT engine
trt_model = YOLO("best.engine")
results = trt_model("image.jpg")  # 2-5x faster than PyTorch
```

## Gotchas

- **Small object detection is hard**: objects < 32x32 pixels are frequently missed. Use higher input resolution (1280 instead of 640), add P2 detection head for small objects, or tile large images with overlap and merge detections via NMS
- **Class imbalance in detection**: background patches vastly outnumber object patches. Focal loss (RetinaNet) addresses this. In YOLO, use `cls` loss weight tuning and ensure training data has balanced class representation
- **Annotation quality > quantity**: 500 precisely annotated images outperform 5000 sloppy ones. Tight bounding boxes, consistent labeling criteria, and handling edge cases (occluded, truncated objects) matter more than dataset size

## See Also

- [[cnn-computer-vision]]
- [[data-augmentation]]
- [[transfer-learning]]
