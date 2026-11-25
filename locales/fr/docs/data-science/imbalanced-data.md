---
title: "Gestion des données déséquilibrées"
category: concepts
tags: [data-science, class-imbalance, smote, oversampling, undersampling]
level: 3
source_sha256: 4fb234ec352cb080b88a6bbd4806743d3a01479a40ab4321e5427a1fe1cda34c
translation: machine
translated_at: '2026-10-24'
---
# Gestion des données déséquilibrées {#handling-imbalanced-data}

Lorsqu'une classe domine le jeu de données (par exemple 99 % de négatifs et 1 % de positifs), les classifieurs standard deviennent biaisés en faveur de la classe majoritaire. La détection de fraude, le diagnostic médical et la détection de défauts sont tous touchés par ce problème. Un modèle qui prédit systématiquement « négatif » atteint 99 % d'exactitude, mais ne sert à rien.

## Mesurer le problème {#measuring-the-problem}

```python
import pandas as pd

# Check imbalance ratio
print(y.value_counts(normalize=True))
# 0    0.985
# 1    0.015  <- severe imbalance

imbalance_ratio = y.value_counts()[0] / y.value_counts()[1]
# > 10:1 = moderate, > 100:1 = severe
```

**Règle essentielle** : ne jamais utiliser l'exactitude (accuracy) comme métrique pour les problèmes déséquilibrés. Utilisez plutôt la précision, le rappel, le F1, l'AUROC ou l'AUPRC.

## Méthodes au niveau des données {#data-level-methods}

### Sur-échantillonnage et sous-échantillonnage aléatoires {#random-oversampling-undersampling}

```python
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

# Oversample minority to match majority
ros = RandomOverSampler(random_state=42)
X_res, y_res = ros.fit_resample(X_train, y_train)

# Undersample majority to match minority
rus = RandomUnderSampler(random_state=42)
X_res, y_res = rus.fit_resample(X_train, y_train)
```

- Sur-échantillonnage : risque de surapprentissage (échantillons de la classe minoritaire dupliqués)
- Sous-échantillonnage : perte d'information provenant de la classe majoritaire

### SMOTE (Synthetic Minority Oversampling) {#smote-synthetic-minority-oversampling}

Crée des échantillons synthétiques en interpolant entre les points existants de la classe minoritaire et leurs k plus proches voisins.

```python
from imblearn.over_sampling import SMOTE, BorderlineSMOTE, ADASYN

# Basic SMOTE
smote = SMOTE(sampling_strategy='auto', k_neighbors=5, random_state=42)
X_res, y_res = smote.fit_resample(X_train, y_train)

# Borderline-SMOTE: only synthesize near decision boundary
bl_smote = BorderlineSMOTE(kind='borderline-1', random_state=42)

# ADASYN: adaptively generate more samples in harder regions
adasyn = ADASYN(random_state=42)
```

### SMOTE + Tomek Links (combiné) {#smote-tomek-links-combined}

Sur-échantillonner la classe minoritaire, puis nettoyer les échantillons bruités de la classe majoritaire situés près de la frontière de décision :

```python
from imblearn.combine import SMOTETomek

smt = SMOTETomek(random_state=42)
X_res, y_res = smt.fit_resample(X_train, y_train)
```

## Méthodes au niveau de l'algorithme {#algorithm-level-methods}

### Poids de classe {#class-weights}

La plupart des classifieurs acceptent le paramètre `class_weight`. Il pénalise plus fortement la mauvaise classification de la classe minoritaire.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Automatic weight inversely proportional to class frequency
rf = RandomForestClassifier(class_weight='balanced', random_state=42)

# Manual weights
lr = LogisticRegression(class_weight={0: 1, 1: 50})

# CatBoost / XGBoost
import xgboost as xgb
model = xgb.XGBClassifier(scale_pos_weight=imbalance_ratio)
```

### Focal Loss {#focal-loss}

Réduit le poids des exemples faciles (bien classés) et se concentre sur les exemples difficiles :

```python
import torch
import torch.nn.functional as F

def focal_loss(logits, targets, alpha=0.25, gamma=2.0):
    bce = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
    pt = torch.exp(-bce)  # probability of correct class
    loss = alpha * (1 - pt) ** gamma * bce
    return loss.mean()
```

gamma=0 correspond à l'entropie croisée standard. gamma=2 est un point de départ typique.

### Apprentissage sensible au coût {#cost-sensitive-learning}

Attribuer des coûts d'erreur de classification différents. Un faux négatif (fraude non détectée) peut coûter 1000 fois plus cher qu'un faux positif (transaction légitime signalée à tort).

```python
# Custom scoring with business costs
def business_cost(y_true, y_pred):
    fn_cost = 1000  # missed fraud
    fp_cost = 10    # false alarm
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    return fn * fn_cost + fp * fp_cost
```

## Ajustement du seuil {#threshold-tuning}

Le seuil par défaut de 0,5 est presque jamais optimal pour des données déséquilibrées.

```python
from sklearn.metrics import precision_recall_curve

probas = model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, probas)

# Find threshold for target recall (e.g., catch 90% of fraud)
target_recall = 0.90
idx = np.argmin(np.abs(recalls - target_recall))
optimal_threshold = thresholds[idx]

y_pred = (probas >= optimal_threshold).astype(int)
```

## Stratégie d'évaluation {#evaluation-strategy}

- **K-Fold stratifié** : préserve la distribution des classes dans chaque pli
- **AUPRC plutôt qu'AUROC** : l'AUPRC est plus informative lorsque la classe positive est rare
- **Matrice de confusion** : toujours examiner les effectifs bruts VP/FP/VN/FN

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import average_precision_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
ap_scores = []
for train_idx, val_idx in skf.split(X, y):
    model.fit(X[train_idx], y[train_idx])
    probas = model.predict_proba(X[val_idx])[:, 1]
    ap_scores.append(average_precision_score(y[val_idx], probas))
```

## Pièges à éviter {#gotchas}

- **Ne jamais appliquer SMOTE au jeu de test** : appliquer le rééchantillonnage uniquement aux données d'entraînement, à l'intérieur de la boucle de validation croisée. Appliquer SMOTE sur l'ensemble des données avant la séparation provoque une fuite de données : les points synthétiques de test sont des interpolations de points d'entraînement, ce qui gonfle artificiellement les métriques
- **SMOTE échoue sur les données creuses de grande dimension** : SMOTE interpole dans l'espace des caractéristiques. Pour du texte (TF-IDF) ou des variables catégorielles encodées en one-hot, les points interpolés n'ont aucun sens. Utilisez plutôt les poids de classe ou le sur-échantillonnage aléatoire
- **Le ratio de déséquilibre évolue en production** : si les données d'entraînement contiennent 1 % de fraudes mais que la production n'en voit que 0,01 %, le seuil et les poids de classe doivent être recalibrés. Surveillez la distribution des classes dans les données entrantes

## Voir aussi {#see-also}

- [[model-evaluation]]
- [[feature-engineering]]
- [[gradient-boosting]]
