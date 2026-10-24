---
title: "Apprentissage par transfert"
category: techniques
tags: [data-science, deep-learning, transfer-learning, fine-tuning, pretrained]
level: 3
source_sha256: 104522c3ff093670d85edd64f2a8b1a5bb919a03891652654e8c817e33e0fb83
translation: machine
translated_at: '2026-10-24'
---
# Apprentissage par transfert {#transfer-learning}

Utiliser les connaissances acquises sur une tâche (source) pour améliorer l'apprentissage sur une autre (cible). C'est le paradigme dominant en deep learning moderne : on n'entraîne presque jamais un modèle depuis zéro.

## Idée centrale {#core-idea}

Les modèles pré-entraînés apprennent des caractéristiques générales sur de grands jeux de données. Les couches basses capturent des motifs universels (contours, textures, fréquences de mots). Les couches hautes deviennent spécifiques à la tâche.

## Stratégies {#strategies}

### Extraction de caractéristiques {#feature-extraction}
Geler toutes les couches pré-entraînées. Remplacer et entraîner uniquement la tête de classification finale.

```python
import torchvision.models as models
import torch.nn as nn

model = models.resnet50(pretrained=True)
for param in model.parameters():
    param.requires_grad = False  # freeze everything
model.fc = nn.Linear(2048, num_classes)  # replace head
```

**À utiliser quand** : petit jeu de données (< 1000 échantillons), tâche cible proche de la source.

### Fine-tuning {#fine-tuning}
Dégeler certaines couches et entraîner avec un learning rate faible.

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

**À utiliser quand** : jeu de données de taille moyenne, tâche cible légèrement différente de la source.

### Fine-tuning complet {#full-fine-tuning}
Dégeler toutes les couches, avec un learning rate très faible sur l'ensemble du réseau.

**À utiliser quand** : grand jeu de données, tâche nettement différente de la source.

## Apprentissage par transfert en vision {#vision-transfer-learning}

**Source** : ImageNet (1,2 M d'images, 1000 classes). La plupart des modèles de torchvision fournissent des poids pré-entraînés.

**Règle empirique** : plus le jeu de données cible est petit, plus on gèle de couches ; plus il est grand, plus on fine-tune de couches.

**Normalisation standard** (statistiques d'ImageNet) :
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

## Apprentissage par transfert en NLP {#nlp-transfer-learning}

**Source** : de grands corpus de texte (Wikipedia, BooksCorpus, Common Crawl).

**Objectifs de pré-entraînement :**
- BERT : Masked Language Model + Next Sentence Prediction
- GPT : modélisation du langage autorégressive
- T5 : text-to-text (toutes les tâches formulées comme de la génération)

**Fine-tuning avec HuggingFace :**
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

## Quand l'apprentissage par transfert aide {#when-transfer-learning-helps}

| Similarité source/cible | Taille des données cibles | Stratégie |
|--------------------------|-----------------|----------|
| Similaire, peu de données | < 1K | Extraction de caractéristiques |
| Similaire, données moyennes | 1K-10K | Fine-tuning des dernières couches |
| Différente, grand jeu de données | > 10K | Fine-tuning complet |
| Très différente, peu de données | < 1K | Peut ne pas aider ; à tester quand même |

## Adaptation de domaine {#domain-adaptation}

Lorsque les domaines source et cible diffèrent (par exemple, photos -> images médicales) :
- **Dégel progressif** : dégeler une couche à la fois, en partant du haut
- **Learning rate discriminant** : learning rate plus faible pour les couches initiales
- **Augmentation de données** : réduire l'écart entre domaines
- **Pré-entraînement spécifique au domaine** : pré-entraîner d'abord sur des données non étiquetées du domaine

## Pièges à éviter {#gotchas}
- Le modèle pré-entraîné attend un format d'entrée précis (taille, normalisation, tokenisation)
- Un learning rate de fine-tuning trop élevé détruit les caractéristiques pré-entraînées (« catastrophic forgetting »)
- Toujours utiliser le tokenizer correspondant au modèle NLP
- Le transfert depuis ImageNet peut ne pas aider pour des images non naturelles (médicales, satellites)
- Pour les données tabulaires, l'apprentissage par transfert aide rarement : le gradient boosting l'emporte généralement

## Voir aussi {#see-also}
- [[neural-networks]] - architectures de base
- [[cnn-computer-vision]] - architectures de vision pour le transfert
- [[nlp-text-processing]] - BERT et fine-tuning de transformers
- [[model-evaluation]] - évaluation des modèles fine-tunés
