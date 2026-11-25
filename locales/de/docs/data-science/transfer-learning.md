---
title: "Transfer Learning"
category: techniques
tags: [data-science, deep-learning, transfer-learning, fine-tuning, pretrained]
level: 3
source_sha256: 104522c3ff093670d85edd64f2a8b1a5bb919a03891652654e8c817e33e0fb83
translation: machine
translated_at: '2026-10-24'
---
# Transfer Learning {#transfer-learning}

Wissen aus einer Aufgabe (Quelle) nutzen, um das Lernen auf einer anderen Aufgabe (Ziel) zu verbessern. Das dominierende Paradigma im modernen Deep Learning – fast nie von Grund auf neu trainieren.

## Kernidee {#core-idea}

Vortrainierte Modelle lernen allgemeine Merkmale auf großen Datensätzen. Untere Schichten erfassen universelle Muster (Kanten, Texturen, Worthäufigkeiten). Höhere Schichten werden aufgabenspezifisch.

## Strategien {#strategies}

### Feature Extraction {#feature-extraction}
Alle vortrainierten Schichten einfrieren. Nur den finalen Klassifikationskopf ersetzen und trainieren.

```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet50(pretrained=True)
for param in model.parameters():
    param.requires_grad = False  # freeze everything
model.fc = nn.Linear(2048, num_classes)  # replace head
```

**Verwenden, wenn**: kleiner Datensatz (< 1000 Samples), Zielaufgabe ähnlich zur Quelle.

### Fine-Tuning {#fine-tuning}
Einige Schichten freigeben und mit niedriger Lernrate trainieren.

```python
# Unfreeze last block
for param in model.layer4.parameters():
    param.requires_grad = True

# Lower LR for pre-trained layers, higher for new head
optimizer = torch.optim.Adam([
    {'params': model.layer4.parameters(), 'lr': 1e-5},
    {'params': model.fc.parameters(), 'lr': 1e-3}
])
```

**Verwenden, wenn**: mittelgroßer Datensatz, Zielaufgabe etwas anders als die Quelle.

### Full Fine-Tuning {#full-fine-tuning}
Alle Schichten freigeben, durchgehend sehr niedrige Lernrate.

**Verwenden, wenn**: großer Datensatz, Aufgabe deutlich anders als die Quelle.

## Transfer Learning in der Bildverarbeitung {#vision-transfer-learning}

**Quelle**: ImageNet (1,2 Mio. Bilder, 1000 Klassen). Die meisten torchvision-Modelle stellen vortrainierte Gewichte bereit.

**Faustregel**: kleinerer Zieldatensatz = mehr Schichten einfrieren; größer = mehr Schichten feinabstimmen.

**Standardnormalisierung** (ImageNet-Statistiken):
```python
from torchvision import transforms
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
```

## Transfer Learning in NLP {#nlp-transfer-learning}

**Quelle**: große Textkorpora (Wikipedia, BooksCorpus, Common Crawl).

**Vortrainingsziele:**
- BERT: Masked Language Model + Next Sentence Prediction
- GPT: autoregressive Sprachmodellierung
- T5: Text-to-Text (alle Aufgaben als Generierung formuliert)

**Fine-Tuning mit HuggingFace:**
```python
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
args = TrainingArguments(
    output_dir='./results',
    learning_rate=2e-5,  # much lower than training from scratch
    num_train_epochs=3,
    per_device_train_batch_size=16
)
trainer = Trainer(model=model, args=args, train_dataset=train_ds)
trainer.train()
```

## Wann Transfer Learning hilft {#when-transfer-learning-helps}

| Ähnlichkeit Quelle/Ziel | Größe der Zieldaten | Strategie |
|--------------------------|-----------------|----------|
| Ähnlich, wenig Daten | < 1K | Feature Extraction |
| Ähnlich, mittlere Datenmenge | 1K-10K | Letzte Schichten fine-tunen |
| Unterschiedlich, große Datenmenge | > 10K | Full Fine-Tuning |
| Sehr unterschiedlich, wenig Daten | < 1K | Hilft womöglich nicht; trotzdem ausprobieren |

## Domain Adaptation {#domain-adaptation}

Wenn sich Quell- und Zieldomäne unterscheiden (z. B. Fotos -> medizinische Bilder):
- **Gradual Unfreezing**: Schichten von oben nach unten einzeln freigeben
- **Discriminative LR**: niedrigere Lernrate für frühere Schichten
- **Data Augmentation**: Domänenlücke überbrücken
- **Domänenspezifisches Pre-Training**: zuerst auf unannotierten In-Domain-Daten vortrainieren

## Fallstricke {#gotchas}
- Das vortrainierte Modell erwartet ein bestimmtes Eingabeformat (Größe, Normalisierung, Tokenisierung)
- Zu hohe Fine-Tuning-Lernrate zerstört die vortrainierten Merkmale ("catastrophic forgetting")
- Für NLP-Modelle immer den passenden Tokenizer verwenden
- Transfer von ImageNet hilft womöglich nicht bei Nicht-Naturbildern (medizinisch, Satellit)
- Bei tabellarischen Daten hilft Transfer Learning selten – Gradient Boosting gewinnt meist

## Siehe auch {#see-also}
- [[neural-networks]] - grundlegende Architekturen
- [[cnn-computer-vision]] - Bildverarbeitungsarchitekturen für Transfer
- [[nlp-text-processing]] - BERT und Fine-Tuning von Transformern
- [[model-evaluation]] - Bewertung feinabgestimmter Modelle
