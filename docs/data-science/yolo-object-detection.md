---
title: YOLO Object Detection - Architecture, API, and Metrics
category: concepts
tags: [misc, computer-vision, yolo, object-detection, ultralytics, opencv, deep-learning]
---

# YOLO Object Detection - Architecture, API, and Metrics

YOLO (You Only Look Once) object detection - bounding box representation, IoU, NMS, evaluation metrics (mAP), YOLOv12 architecture, Ultralytics Python API, and video processing with OpenCV.

## Key Facts

- Detection output: `[x1, y1, x2, y2, confidence, class_id]` per object
- IoU (Intersection over Union) measures bounding box overlap; 0.5 = lenient, 0.7 = strict threshold
- NMS (Non-Maximum Suppression) eliminates duplicate detections by confidence ranking + IoU filtering
- mAP@0.5:0.95 (COCO protocol) is the standard benchmark metric, averaging over 10 IoU thresholds
- YOLOv12 uses attention mechanisms (not conv backbone) with area attention for O(N) complexity
- Ultralytics API: `model.predict()`, `model.train()`, `model.val()` for full workflow

## Patterns

### IoU Calculation

```python
def iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0.0
```

### NMS Algorithm

1. Sort all boxes by confidence (descending)
2. Take highest-confidence box as a keeper
3. Remove all boxes with IoU > threshold with the keeper
4. Repeat until no boxes remain

```python
def nms(boxes, confidences, iou_threshold=0.5):
    order = sorted(range(len(confidences)),
                   key=lambda i: confidences[i], reverse=True)
    keep = []
    while order:
        i = order.pop(0)
        keep.append(i)
        order = [j for j in order if iou(boxes[i], boxes[j]) < iou_threshold]
    return keep
```

Lower IoU threshold = more aggressive suppression (fewer boxes).

### Evaluation Metrics

- **Precision** = TP / (TP + FP) - of all detections, how many correct
- **Recall** = TP / (TP + FN) - of all actual objects, how many found
- **AP** = area under precision-recall curve (per class)
- **mAP** = mean AP across all classes

**COCO protocol**: average over IoU 0.5 to 0.95, step 0.05 (10 thresholds), 101-point interpolation. Also reports mAP@0.5, mAP@0.75, mAP by object size (S/M/L).

### YOLOv12 Architecture

- **Area attention**: divides feature map into fixed areas, runs attention within each (not globally)
- **Residual ELAN**: efficient layer aggregation with skip connections
- **Flash attention**: memory-efficient implementation for larger batch sizes
- **No positional encoding**: 7x7 depthwise convolution captures position implicitly

| Model | Parameters | Use case |
|-------|-----------|----------|
| nano (n) | ~3M | Mobile, edge, real-time CPU |
| small (s) | ~9M | Embedded GPU |
| medium (m) | ~20M | Balanced |
| large (l) | ~43M | High accuracy |
| XL (x) | ~59M | Maximum accuracy |

### Ultralytics API

```python
from ultralytics import YOLO

model = YOLO("yolov12n.pt")

# Predict
results = model.predict(
    source="image.jpg",    # path, URL, directory, video, webcam (0)
    conf=0.25,             # confidence threshold
    iou=0.7,               # NMS IoU threshold
    classes=[0, 1, 2],     # filter by class IDs
    save=True,             # save annotated output
)

# Access results
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        cls = int(box.cls[0].item())
        label = result.names[cls]

# Train on custom dataset
model.train(data="dataset.yaml", epochs=100, imgsz=640, batch=16, device=0)

# Evaluate
metrics = model.val(data="dataset.yaml")
print(metrics.box.map)    # mAP@0.5:0.95
print(metrics.box.map50)  # mAP@0.5
```

### Dataset YAML Format

```yaml
path: /data/my-dataset
train: images/train
val: images/val
nc: 3
names: ["cat", "dog", "bird"]
```

### Video Processing with OpenCV

```python
import cv2
from ultralytics import YOLO
import time

model = YOLO("yolov12n.pt")
cap = cv2.VideoCapture("input.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

prev_time = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    results = model.predict(frame, conf=0.25, verbose=False)
    annotated = results[0].plot()

    curr_time = time.time()
    fps_display = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(annotated, f"FPS: {fps_display:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    out.write(annotated)
    cv2.imshow("Detection", annotated)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release()
out.release()
cv2.destroyAllWindows()
```

## Gotchas

- COCO class IDs are not contiguous (e.g., ID 12 is skipped); use `model.names` dict for mapping
- `model.predict(show=True)` adds 1ms delay per frame for video display
- `save_crop=True` saves individual detected objects as separate images
- Lower NMS IoU threshold = fewer boxes (more aggressive); higher = more permissive
- `verbose=False` in predict suppresses per-frame logging for video processing

## See Also

- [[stdlib-patterns]] - Python data processing for detection results
