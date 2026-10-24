---
title: "Détection d'objets et YOLO"
category: concepts
tags: [data-science, computer-vision, yolo, object-detection, cnn, tracking]
level: 3
source_sha256: 985fab727053f09f4bcaf116294c24f43061f8f4fd77e7f51a778627b9b1b9ce
translation: machine
translated_at: '2026-10-24'
---
# Détection d'objets et YOLO {#object-detection-and-yolo}

La détection d'objets permet de localiser et de classer plusieurs objets dans une image à l'aide de boîtes englobantes. Il existe deux familles : les détecteurs à deux étages (famille R-CNN, précis mais lents) et les détecteurs à un étage (YOLO, SSD, rapides et adaptés au temps réel). YOLO (You Only Look Once) domine les applications pratiques.

## Paradigmes de détection {#detection-paradigms}

**Détecteurs à deux étages** : proposer d'abord des régions, puis classer chacune d'elles.
- R-CNN -> Fast R-CNN -> Faster R-CNN (Region Proposal Network)
- Plus précis sur les petits objets, inférence plus lente

**Détecteurs à un étage** : prédire les boîtes et les classes en une seule passe.
- Famille YOLO, SSD, RetinaNet
- Plus rapides, mieux adaptés aux applications temps réel
- Les variantes sans ancres (FCOS, CenterNet) suppriment la conception des boîtes d'ancrage

## Évolution de YOLO {#yolo-evolution}

| Version | Innovation clé | FPS (GPU) |
|---------|---------------|-----------|
| YOLOv1 | Détection en une seule passe | ~45 |
| YOLOv3 | Détection multi-échelle, Darknet-53 | ~30 |
| YOLOv5 | Natif PyTorch, prêt pour la production | ~140 |
| YOLOv8 | Sans ancres, tête découplée | ~160 |
| YOLOv11 | Blocs C3k2, mécanismes d'attention | ~180 |
| YOLOv12 | Attention par zones, blocs R-ELAN | ~190 |

## YOLOv8/v11 avec Ultralytics {#yolov8v11-with-ultralytics}

### Entraînement d'un détecteur personnalisé {#training-custom-detector}

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

### Format du jeu de données (YOLO) {#dataset-format-yolo}

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

Fichiers d'étiquettes (un par image, même nom avec l'extension .txt) :
```markdown
# class_id center_x center_y width height (all normalized 0-1)
0 0.5 0.4 0.3 0.6
1 0.2 0.7 0.15 0.2
```

### Inférence {#inference}

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

### Suivi d'objets {#object-tracking}

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

## Métriques d'évaluation {#evaluation-metrics}

- **IoU (Intersection over Union)** : recouvrement entre la boîte prédite et la boîte de référence (ground truth). IoU > 0,5 = détection correcte (standard)
- **mAP@50** : précision moyenne moyenne (mean Average Precision) pour un seuil d'IoU de 0,5
- **mAP@50:95** : moyenne calculée pour des seuils d'IoU de 0,5 à 0,95 (pas de 0,05). Métrique plus exigeante
- **Précision/Rappel** par classe, pour le seuil de confiance choisi

```python
# Validate model
metrics = model.val(data="dataset.yaml")
print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")
```

## Augmentation de données pour la détection {#data-augmentation-for-detection}

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

**Augmentation Mosaic** : combine 4 images d'entraînement en une seule. Aide à détecter les petits objets et réduit les besoins en taille de lot. La désactiver pendant les 10 dernières époques pour obtenir les meilleurs résultats.

## Déploiement {#deployment}

### Inférence avec ONNX Runtime {#onnx-runtime-inference}

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

### TensorRT pour une vitesse maximale {#tensorrt-for-maximum-speed}

```python
# Export from Ultralytics
model.export(format="engine", imgsz=640, half=True, device=0)

# Load TensorRT engine
trt_model = YOLO("best.engine")
results = trt_model("image.jpg")  # 2-5x faster than PyTorch
```

## Pièges à éviter {#gotchas}

- **La détection de petits objets est difficile** : les objets de moins de 32x32 pixels sont fréquemment manqués. Utilisez une résolution d'entrée plus élevée (1280 au lieu de 640), ajoutez une tête de détection P2 pour les petits objets, ou découpez les grandes images en tuiles avec recouvrement et fusionnez les détections via NMS
- **Déséquilibre des classes en détection** : les zones de fond sont largement plus nombreuses que les zones d'objets. La focal loss (RetinaNet) répond à ce problème. Dans YOLO, ajustez le poids de la perte `cls` et assurez-vous que les données d'entraînement représentent les classes de manière équilibrée
- **La qualité des annotations prime sur la quantité** : 500 images annotées avec précision surpassent 5000 images annotées sans soin. Des boîtes serrées, des critères d'étiquetage cohérents et la prise en compte des cas limites (objets occultés, tronqués) comptent davantage que la taille du jeu de données

## Voir aussi {#see-also}

- [[cnn-computer-vision]]
- [[data-augmentation]]
- [[transfer-learning]]
