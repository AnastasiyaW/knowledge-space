---
title: "Datenaugmentierung"
category: techniques
tags: [data-science, deep-learning, augmentation, computer-vision, regularization]
level: 3
source_sha256: b7fb3b3293f938e022594a9b131f8435fae1a087eb6bec35231c32b76378e89d
translation: machine
translated_at: '2026-10-24'
---
# Datenaugmentierung {#data-augmentation}

Künstliche Vergrößerung der Trainingsdaten durch Anwendung zufälliger Transformationen. Reduziert Overfitting und verbessert die Generalisierung. Praktisch kostenlose Leistungssteigerung für Vision- und NLP-Aufgaben.

## Bildaugmentierung {#image-augmentation}

### Grundlegende Transformationen {#basic-transforms}

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Validation: NO augmentation (except resize + normalize)
val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

### Fortgeschrittene Techniken {#advanced-techniques}

- **Cutout/Random Erasing**: zufälliges Maskieren rechteckiger Bereiche
- **Mixup**: Mischen zweier Bilder und ihrer Labels: x = lambda*x1 + (1-lambda)*x2
- **CutMix**: Einfügen eines Ausschnitts aus einem Bild in ein anderes, Mischen der Labels nach Flächenanteil
- **AutoAugment**: gelernte Augmentierungsstrategien

## Textaugmentierung {#text-augmentation}

- **Synonymersetzung**: Ersetzen von Wörtern durch Synonyme
- **Back-Translation**: Übersetzung in eine andere Sprache und zurück
- **Zufälliges Einfügen/Löschen/Vertauschen**: Störung der Wortreihenfolge
- **Kontextuelle Augmentierung**: Verwendung eines Sprachmodells zum Ersetzen von Wörtern

## Augmentierung tabellarischer Daten {#tabular-data-augmentation}

- **SMOTE**: Erzeugung synthetischer Minderheitsstichproben für unausgewogene Klassen
- **Rauschinjektion**: Hinzufügen von Gauß'schem Rauschen zu Merkmalen
- **Mixup**: Mischen von Merkmalsvektoren und Labels

```python
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=42)
X_resampled, y_resampled = sm.fit_resample(X_train, y_train)
```

## Grundprinzipien {#principles}

- Augmentierung **nur auf Trainingsdaten** anwenden, niemals auf Validierungs- oder Testdaten
- Augmentierungen sollten labelerhaltend sein (das Spiegeln einer "6" kann eine "9" ergeben)
- Domänenspezifisch wählen: Text nicht horizontal spiegeln, medizinische Bilder nicht rotieren, wenn die Orientierung relevant ist
- Bei kleineren Datensätzen aggressivere Augmentierung einsetzen
- Mehrere Augmentierungen für maximale Wirkung kombinieren

## Stolpersteine {#gotchas}
- Zu aggressive Augmentierung kann die Leistung verschlechtern (das Modell lernt, mit Rauschen umzugehen, statt das Signal zu nutzen)
- Vertikales Spiegeln ist selten sinnvoll (die meisten natürlichen Bilder haben eine "Schwerkraftrichtung")
- Farbaugmentierung kann wichtige Farbinformationen zerstören (medizinische Bildgebung)
- SMOTE erzeugt synthetische Punkte im Merkmalsraum – dabei können unrealistische Stichproben entstehen
- Augmentierung verlängert die Trainingszeit – Nutzen und Kosten abwägen

## Siehe auch {#see-also}
- [[cnn-computer-vision]] - primärer Nutznießer der Bildaugmentierung
- [[nlp-text-processing]] - Techniken zur Textaugmentierung
- [[feature-engineering]] - SMOTE für tabellarische Daten
- [[model-evaluation]] - Messung der Auswirkung der Augmentierung
