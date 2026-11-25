---
title: "Objekterkennung und YOLO"
category: concepts
tags: [data-science, computer-vision, yolo, object-detection, cnn, tracking]
level: 3
source_sha256: 985fab727053f09f4bcaf116294c24f43061f8f4fd77e7f51a778627b9b1b9ce
translation: machine
translated_at: '2026-10-24'
---
# Objekterkennung und YOLO {#object-detection-and-yolo}

Objekterkennung findet und klassifiziert mehrere Objekte in Bildern mithilfe von Bounding Boxes. Es gibt zwei Familien: Zweistufige Verfahren (R-CNN-Familie – genau, aber langsam) und einstufige Verfahren (YOLO, SSD – schnell, geeignet für Echtzeitanwendungen). YOLO (You Only Look Once) dominiert die praktischen Anwendungen.

## Detektionsparadigmen {#detection-paradigms}

**Zweistufige Detektoren**: Zuerst werden Regionen vorgeschlagen, dann wird jede klassifiziert.
- R-CNN -> Fast R-CNN -> Faster R-CNN (Region Proposal Network)
- Genauer bei kleinen Objekten, langsamere Inferenz

**Einstufige Detektoren**: Sagen Boxen und Klassen in einem einzigen Durchlauf voraus.
- YOLO-Familie, SSD, RetinaNet
- Schneller, besser für Echtzeitanwendungen
- Ankerfreie Varianten (FCOS, CenterNet) machen das Entwerfen von Anchor-Boxen überflüssig

## YOLO-Entwicklung {#yolo-evolution}

| Version | Wichtigste Neuerung | FPS (GPU) |
|---------|---------------|-----------|
| YOLOv1 | Detektion in einem Durchlauf | ~45 |
| YOLOv3 | Multi-Scale-Detektion, Darknet-53 | ~30 |
| YOLOv5 | Nativ in PyTorch, produktionsreif | ~140 |
| YOLOv8 | Ankerfrei, entkoppelter Head | ~160 |
| YOLOv11 | C3k2-Blöcke, Attention-Mechanismen | ~180 |
| YOLOv12 | Area Attention, R-ELAN-Blöcke | ~190 |

## YOLOv8/v11 mit Ultralytics {#yolov8v11-with-ultralytics}

### Training eines eigenen Detektors {#training-custom-detector}

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

### Datensatzformat (YOLO) {#dataset-format-yolo}

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

Label-Dateien (eine pro Bild, gleicher Name mit .txt):
```markdown
# class_id center_x center_y width height (all normalized 0-1)
0 0.5 0.4 0.3 0.6
1 0.2 0.7 0.15 0.2
```

### Inferenz {#inference}

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

### Objekt-Tracking {#object-tracking}

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

## Evaluationsmetriken {#evaluation-metrics}

- **IoU (Intersection over Union)**: Überlappung zwischen vorhergesagter und Ground-Truth-Box. IoU > 0,5 = korrekte Detektion (Standard)
- **mAP@50**: mittlere Average Precision bei IoU-Schwellenwert 0,5
- **mAP@50:95**: gemittelt über IoU-Schwellenwerte von 0,5 bis 0,95 (Schrittweite 0,05). Strengere Metrik
- **Precision/Recall** pro Klasse bei gewähltem Konfidenz-Schwellenwert

```python
# Validate model
metrics = model.val(data="dataset.yaml")
print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")
```

## Datenaugmentierung für Detektion {#data-augmentation-for-detection}

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

**Mosaic-Augmentierung**: Kombiniert 4 Trainingsbilder zu einem. Hilft bei der Erkennung kleiner Objekte und reduziert die Anforderungen an die Batch-Größe. In den letzten 10 Epochen deaktivieren, für beste Ergebnisse.

## Deployment {#deployment}

### ONNX-Runtime-Inferenz {#onnx-runtime-inference}

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

### TensorRT für maximale Geschwindigkeit {#tensorrt-for-maximum-speed}

```python
# Export from Ultralytics
model.export(format="engine", imgsz=640, half=True, device=0)

# Load TensorRT engine
trt_model = YOLO("best.engine")
results = trt_model("image.jpg")  # 2-5x faster than PyTorch
```

## Stolperfallen {#gotchas}

- **Die Erkennung kleiner Objekte ist schwierig**: Objekte < 32x32 Pixel werden häufig übersehen. Eine höhere Eingabeauflösung verwenden (1280 statt 640), einen P2-Detektionskopf für kleine Objekte ergänzen oder große Bilder mit Überlappung kacheln und die Detektionen per NMS zusammenführen
- **Klassenungleichgewicht bei der Detektion**: Hintergrund-Patches übertreffen Objekt-Patches bei Weitem. Focal Loss (RetinaNet) adressiert dieses Problem. In YOLO die Gewichtung des `cls`-Verlusts anpassen und sicherstellen, dass die Trainingsdaten eine ausgewogene Klassenverteilung haben
- **Annotationsqualität vor Quantität**: 500 präzise annotierte Bilder übertreffen 5000 nachlässig annotierte. Enge Bounding Boxes, einheitliche Labeling-Kriterien und der Umgang mit Grenzfällen (verdeckte, abgeschnittene Objekte) sind wichtiger als die Größe des Datensatzes

## Siehe auch {#see-also}

- [[cnn-computer-vision]]
- [[data-augmentation]]
- [[transfer-learning]]
