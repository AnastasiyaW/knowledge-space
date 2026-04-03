---
title: Object Detection
category: computer-vision
tags: [object-detection, yolo, faster-rcnn, ssd, anchor-boxes, nms, pytorch, computer-vision]
---

# Object Detection

Locate and classify multiple objects in an image by predicting bounding boxes and class labels. Two families: two-stage detectors (Faster R-CNN - accurate) and single-stage detectors (YOLO, SSD - fast). Builds on [[convolutional-neural-networks]] backbones and is closely related to [[image-segmentation]].

## Key Facts

- **Bounding box**: rectangle defined by (x, y, w, h) or (x1, y1, x2, y2); localizes one object instance
- **IoU** (Intersection over Union): overlap measure between predicted and ground truth boxes; IoU > 0.5 typically considered a match
- **Anchor boxes**: predefined boxes at different scales and aspect ratios; model predicts offsets from anchors
- **NMS** (Non-Maximum Suppression): remove duplicate detections; keep highest confidence box, suppress overlapping ones (IoU > threshold)
- **Two-stage detectors**: (1) Region Proposal Network proposes candidate regions, (2) classifier/regressor refines them; Faster R-CNN is canonical
- **Single-stage detectors**: predict boxes and classes directly from feature maps; YOLO (You Only Look Once), SSD; faster but historically less accurate
- **YOLO evolution**: YOLOv1 (2016) -> YOLOv5 (2020) -> YOLOv8/YOLOv11 (2023+, Ultralytics); each version improves speed/accuracy
- **Feature Pyramid Network (FPN)**: multi-scale feature maps for detecting objects at different sizes; used in most modern detectors
- **mAP** (mean Average Precision): standard metric; average of AP across all classes; AP = area under precision-recall curve at different IoU thresholds
- **mAP@0.5**: AP at IoU=0.5; mAP@0.5:0.95: averaged over IoU from 0.5 to 0.95 in steps of 0.05 (COCO metric)
- **COCO dataset**: 80 object classes, 330K images; standard benchmark; COCO API for evaluation
- Modern trend: anchor-free detectors (FCOS, CenterNet); transformer-based (DETR, DINO)

## Patterns

```python
# YOLO with Ultralytics (most practical approach)
from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolov8n.pt')  # nano (fast), also: s, m, l, x

# Inference on image
results = model('image.jpg')
for result in results:
    boxes = result.boxes
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = box.conf[0].item()
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        print(f"{class_name}: {confidence:.2f} at [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")

# Train on custom dataset (YOLO format)
# Dataset structure:
# dataset/
#   train/images/, train/labels/  (txt files: class x_center y_center w h, normalized 0-1)
#   val/images/, val/labels/
model.train(data='dataset.yaml', epochs=100, imgsz=640, batch=16)

# Export for deployment
model.export(format='onnx')

# Torchvision Faster R-CNN
import torchvision
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2

model_frcnn = fasterrcnn_resnet50_fpn_v2(weights='DEFAULT')
model_frcnn.eval()

# Inference
import torch
from torchvision.transforms.functional import to_tensor
from PIL import Image

img = Image.open('image.jpg')
img_tensor = to_tensor(img).unsqueeze(0)

with torch.no_grad():
    predictions = model_frcnn(img_tensor)
# predictions[0] = {'boxes': tensor, 'labels': tensor, 'scores': tensor}

# Filter by confidence
keep = predictions[0]['scores'] > 0.5
boxes = predictions[0]['boxes'][keep]
labels = predictions[0]['labels'][keep]
scores = predictions[0]['scores'][keep]

# IoU computation
from torchvision.ops import box_iou
iou_matrix = box_iou(boxes_pred, boxes_gt)  # (N_pred, N_gt)

# NMS
from torchvision.ops import nms
keep_indices = nms(boxes, scores, iou_threshold=0.5)
```

## Gotchas

- YOLO label format is NORMALIZED (0-1) center coordinates: `class x_center y_center width height`; NOT pixel coordinates
- Faster R-CNN expects input as list of tensors (not batched tensor); each image can have different size
- NMS threshold too high (0.7+): keeps duplicate boxes; too low (0.3): removes valid detections for overlapping objects
- mAP@0.5 is lenient; mAP@0.5:0.95 is the standard COCO metric -- report this for comparison
- Small object detection is hard: FPN and higher-resolution inputs help but increase compute cost
- YOLO `.train()` modifies config in place; always specify full `data.yaml` path

## See Also

- [[convolutional-neural-networks]] - backbone architectures (ResNet, EfficientNet) used in detectors
- [[image-segmentation]] - extends detection to pixel-level masks (instance segmentation)
- [[transfer-learning]] - pretrained backbones dramatically improve detection accuracy
- [[model-evaluation-metrics]] - mAP computation requires understanding precision-recall
- Ultralytics YOLO: https://docs.ultralytics.com/
- torchvision detection: https://pytorch.org/vision/stable/models.html#object-detection
