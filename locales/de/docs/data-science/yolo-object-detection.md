---
title: "YOLO-Objekterkennung - Architektur, API und Metriken"
category: concepts
tags: [computer-vision, yolo, object-detection, ultralytics, opencv, deep-learning]
level: 3
source_sha256: 561b5d5a6691dc72febb24abcc04491a86df33e5387170ff6b5cb24b02ca7806
translation: machine
translated_at: '2026-10-24'
---
# YOLO-Objekterkennung - Architektur, API und Metriken {#yolo-object-detection-architecture-api-and-metrics}

YOLO (You Only Look Once) Objekterkennung - Darstellung von Bounding Boxes, IoU, NMS, Evaluationsmetriken (mAP), YOLOv12-Architektur, Ultralytics-Python-API und Videoverarbeitung mit OpenCV.

## Wichtige Fakten {#key-facts}

- Ausgabe der Erkennung: `[x1, y1, x2, y2, confidence, class_id]` pro Objekt
- IoU (Intersection over Union) misst die Überlappung von Bounding Boxes; 0,5 = großzügig, 0,7 = strenger Schwellenwert
- NMS (Non-Maximum Suppression) entfernt doppelte Erkennungen durch Sortierung nach Konfidenz und IoU-Filterung
- mAP@0.5:0.95 (COCO-Protokoll) ist die gängige Benchmark-Metrik und mittelt über 10 IoU-Schwellenwerte
- YOLOv12 verwendet Attention-Mechanismen (statt eines Faltungs-Backbones) mit Area Attention für O(N)-Komplexität
- Ultralytics-API: `model.predict()`, `model.train()`, `model.val()` für den vollständigen Workflow

## Muster {#patterns}

### IoU-Berechnung {#iou-calculation}

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

### NMS-Algorithmus {#nms-algorithm}

1. Alle Boxen nach Konfidenz absteigend sortieren
2. Die Box mit der höchsten Konfidenz als Behalten-Box auswählen
3. Alle Boxen mit IoU > Schwellenwert zur Behalten-Box entfernen
4. Wiederholen, bis keine Boxen mehr übrig sind

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

Ein niedrigerer IoU-Schwellenwert bedeutet aggressivere Unterdrückung (weniger Boxen).

### Evaluationsmetriken {#evaluation-metrics}

- **Precision** = TP / (TP + FP) - von allen Erkennungen, wie viele korrekt sind
- **Recall** = TP / (TP + FN) - von allen tatsächlichen Objekten, wie viele gefunden wurden
- **AP** = Fläche unter der Precision-Recall-Kurve (pro Klasse)
- **mAP** = mittlere AP über alle Klassen

**COCO-Protokoll**: Mittelung über IoU 0,5 bis 0,95 in Schritten von 0,05 (10 Schwellenwerte), 101-Punkte-Interpolation. Zusätzlich werden mAP@0.5, mAP@0.75 und mAP nach Objektgröße (S/M/L) ausgewiesen.

### YOLOv12-Architektur {#yolov12-architecture}

- **Area Attention**: teilt die Feature-Map in feste Bereiche auf und führt Attention innerhalb jedes Bereichs aus (nicht global)
- **Residual ELAN**: effiziente Layer-Aggregation mit Skip-Verbindungen
- **Flash Attention**: speichereffiziente Implementierung für größere Batch-Größen
- **Keine Positional Encoding**: eine 7x7-Depthwise-Faltung erfasst die Position implizit

| Modell | Parameter | Anwendungsfall |
|--------|-----------|----------------|
| nano (n) | ~3M | Mobil, Edge, Echtzeit auf CPU |
| small (s) | ~9M | Embedded-GPU |
| medium (m) | ~20M | Ausgewogen |
| large (l) | ~43M | Hohe Genauigkeit |
| XL (x) | ~59M | Maximale Genauigkeit |

### Ultralytics-API {#ultralytics-api}

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

### Format der Dataset-YAML {#dataset-yaml-format}

```yaml
path: /data/my-dataset
train: images/train
val: images/val
nc: 3
names: ["cat", "dog", "bird"]
```

### Videoverarbeitung mit OpenCV {#video-processing-with-opencv}

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

## Fallstricke {#gotchas}

- COCO-Klassen-IDs sind nicht fortlaufend (z. B. wird ID 12 übersprungen); verwende das Dict `model.names` für die Zuordnung
- `model.predict(show=True)` fügt bei der Videoanzeige 1 ms Verzögerung pro Frame hinzu
- `save_crop=True` speichert jedes erkannte Objekt als eigenes Bild
- Niedrigerer NMS-IoU-Schwellenwert = weniger Boxen (aggressiver); höherer = nachgiebiger
- `verbose=False` in `predict` unterdrückt das Logging pro Frame bei der Videoverarbeitung

## Siehe auch {#see-also}

- [[stdlib-patterns]] - Python-Datenverarbeitung für Erkennungsergebnisse
