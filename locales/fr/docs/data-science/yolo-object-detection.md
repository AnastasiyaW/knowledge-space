---
title: "Détection d'objets YOLO - Architecture, API et métriques"
category: concepts
tags: [computer-vision, yolo, object-detection, ultralytics, opencv, deep-learning]
level: 3
source_sha256: 561b5d5a6691dc72febb24abcc04491a86df33e5387170ff6b5cb24b02ca7806
translation: machine
translated_at: '2026-10-24'
---
# Détection d'objets YOLO - Architecture, API et métriques {#yolo-object-detection-architecture-api-and-metrics}

Détection d'objets YOLO (You Only Look Once) : représentation des boîtes englobantes, IoU, NMS, métriques d'évaluation (mAP), architecture YOLOv12, API Python Ultralytics et traitement vidéo avec OpenCV.

## Faits clés {#key-facts}

- Sortie de détection : `[x1, y1, x2, y2, confidence, class_id]` par objet
- IoU (Intersection over Union) mesure le recouvrement des boîtes englobantes ; 0,5 = seuil permissif, 0,7 = seuil strict
- NMS (Non-Maximum Suppression) élimine les détections en double par classement selon la confiance et filtrage par IoU
- mAP@0.5:0.95 (protocole COCO) est la métrique de référence standard, moyennée sur 10 seuils d'IoU
- YOLOv12 utilise des mécanismes d'attention (et non un backbone convolutif) avec une attention par zones pour une complexité en O(N)
- API Ultralytics : `model.predict()`, `model.train()`, `model.val()` pour le flux de travail complet

## Modèles {#patterns}

### Calcul de l'IoU {#iou-calculation}

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

### Algorithme NMS {#nms-algorithm}

1. Trier toutes les boîtes par confiance (ordre décroissant)
2. Retenir la boîte de confiance la plus élevée comme boîte conservée
3. Supprimer toutes les boîtes dont l'IoU avec la boîte conservée est supérieur au seuil
4. Répéter jusqu'à ce qu'il ne reste plus aucune boîte

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

Un seuil d'IoU plus bas = suppression plus agressive (moins de boîtes).

### Métriques d'évaluation {#evaluation-metrics}

- **Précision** = TP / (TP + FP) - parmi toutes les détections, combien sont correctes
- **Rappel** = TP / (TP + FN) - parmi tous les objets réels, combien ont été trouvés
- **AP** = aire sous la courbe précision-rappel (par classe)
- **mAP** = moyenne des AP sur toutes les classes

**Protocole COCO** : moyenne sur les IoU de 0,5 à 0,95, par pas de 0,05 (10 seuils), avec interpolation sur 101 points. Sont également reportés mAP@0.5, mAP@0.75 et le mAP par taille d'objet (S/M/L).

### Architecture YOLOv12 {#yolov12-architecture}

- **Attention par zones** : divise la carte de caractéristiques en zones fixes et calcule l'attention au sein de chacune (et non globalement)
- **ELAN résiduel** : agrégation efficace des couches avec connexions résiduelles
- **Flash attention** : implémentation économe en mémoire pour des tailles de lot plus grandes
- **Pas d'encodage positionnel** : une convolution depthwise 7x7 capture la position de manière implicite

| Modèle | Paramètres | Cas d'usage |
|-------|-----------|----------|
| nano (n) | ~3M | Mobile, edge, CPU temps réel |
| small (s) | ~9M | GPU embarqué |
| medium (m) | ~20M | Équilibré |
| large (l) | ~43M | Haute précision |
| XL (x) | ~59M | Précision maximale |

### API Ultralytics {#ultralytics-api}

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

### Format YAML du jeu de données {#dataset-yaml-format}

```yaml
path: /data/my-dataset
train: images/train
val: images/val
nc: 3
names: ["cat", "dog", "bird"]
```

### Traitement vidéo avec OpenCV {#video-processing-with-opencv}

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

## Pièges courants {#gotchas}

- Les identifiants de classes COCO ne sont pas contigus (par exemple, l'ID 12 est sauté) ; utilisez le dictionnaire `model.names` pour la correspondance
- `model.predict(show=True)` ajoute un délai de 1 ms par image pour l'affichage vidéo
- `save_crop=True` enregistre chaque objet détecté sous forme d'image séparée
- Seuil NMS d'IoU plus bas = moins de boîtes (plus agressif) ; plus élevé = plus permissif
- `verbose=False` dans predict supprime la journalisation par image lors du traitement vidéo

## Voir aussi {#see-also}

- [[stdlib-patterns]] - Traitement de données Python pour les résultats de détection
