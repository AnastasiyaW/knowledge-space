---
title: "Umgang mit unausgewogenen Daten"
category: concepts
tags: [data-science, class-imbalance, smote, oversampling, undersampling]
level: 3
source_sha256: 4fb234ec352cb080b88a6bbd4806743d3a01479a40ab4321e5427a1fe1cda34c
translation: machine
translated_at: '2026-10-24'
---
# Umgang mit unausgewogenen Daten {#handling-imbalanced-data}

Wenn eine Klasse den Datensatz dominiert (z. B. 99 % negativ, 1 % positiv), werden Standard-Klassifikatoren zugunsten der Mehrheitsklasse verzerrt. Betrugserkennung, medizinische Diagnose, Fehlererkennung – alle sind davon betroffen. Ein Modell, das immer „negativ“ vorhersagt, erreicht 99 % Genauigkeit, ist aber nutzlos.

## Das Problem messen {#measuring-the-problem}

```python
import pandas as pd

# Check imbalance ratio
print(y.value_counts(normalize=True))
# 0    0.985
# 1    0.015  <- severe imbalance

imbalance_ratio = y.value_counts()[0] / y.value_counts()[1]
# > 10:1 = moderate, > 100:1 = severe
```

**Wichtige Regel**: Verwenden Sie bei unausgewogenen Problemen niemals die Accuracy als Metrik. Verwenden Sie stattdessen Precision, Recall, F1, AUROC oder AUPRC.

## Methoden auf Datenebene {#data-level-methods}

### Zufälliges Oversampling / Undersampling {#random-oversampling-undersampling}

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

- Oversampling: Risiko von Overfitting (duplizierte Samples der Minderheitsklasse)
- Undersampling: Verlust von Informationen aus der Mehrheitsklasse

### SMOTE (Synthetic Minority Oversampling) {#smote-synthetic-minority-oversampling}

Erzeugt synthetische Samples durch Interpolation zwischen bestehenden Punkten der Minderheitsklasse und deren k nächsten Nachbarn.

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

### SMOTE + Tomek Links (kombiniert) {#smote-tomek-links-combined}

Zuerst die Minderheitsklasse oversampeln, anschließend verrauschte Samples der Mehrheitsklasse nahe der Klassengrenze bereinigen:

```python
from imblearn.combine import SMOTETomek

smt = SMOTETomek(random_state=42)
X_res, y_res = smt.fit_resample(X_train, y_train)
```

## Methoden auf Algorithmusebene {#algorithm-level-methods}

### Klassengewichte {#class-weights}

Die meisten Klassifikatoren unterstützen den Parameter `class_weight`. Er bestraft Fehlklassifikationen der Minderheitsklasse stärker.

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

Gewichtet einfache (gut klassifizierte) Beispiele herab und fokussiert auf schwierige:

```python
import torch
import torch.nn.functional as F

def focal_loss(logits, targets, alpha=0.25, gamma=2.0):
    bce = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
    pt = torch.exp(-bce)  # probability of correct class
    loss = alpha * (1 - pt) ** gamma * bce
    return loss.mean()
```

gamma=0 entspricht der Standard-Cross-Entropy. gamma=2 ist ein typischer Ausgangswert.

### Kostensensitives Lernen {#cost-sensitive-learning}

Unterschiedliche Fehlklassifikationskosten zuweisen. Ein falsch negatives Ergebnis (übersehener Betrug) kann 1000-mal teurer sein als ein falsch positives (fälschlich markierte legitime Transaktion).

```python
# Custom scoring with business costs
def business_cost(y_true, y_pred):
    fn_cost = 1000  # missed fraud
    fp_cost = 10    # false alarm
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    return fn * fn_cost + fp * fp_cost
```

## Schwellenwert-Optimierung {#threshold-tuning}

Der Standard-Schwellenwert von 0,5 ist für unausgewogene Daten fast nie optimal.

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

## Evaluierungsstrategie {#evaluation-strategy}

- **Stratified K-Fold**: erhält die Klassenverteilung in jedem Fold
- **AUPRC statt AUROC**: AUPRC ist aussagekräftiger, wenn die positive Klasse selten ist
- **Konfusionsmatrix**: Prüfen Sie stets die rohen TP/FP/TN/FN-Zählwerte

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

## Stolperfallen {#gotchas}

- **Den Testdatensatz niemals mit SMOTE bearbeiten**: Wenden Sie Resampling nur auf die Trainingsdaten innerhalb der Cross-Validation-Schleife an. SMOTE auf den vollständigen Datensatz vor dem Splitting führt zu Data Leakage – synthetische Testpunkte sind Interpolationen von Trainingspunkten und liefern damit überhöhte Metriken
- **SMOTE auf hochdimensionalen, dünnbesetzten Daten funktioniert nicht**: SMOTE interpoliert im Merkmalsraum. Bei Text (TF-IDF) oder One-Hot-kodierten kategorialen Merkmalen sind interpolierte Punkte bedeutungslos. Verwenden Sie stattdessen Klassengewichte oder zufälliges Oversampling
- **Das Ungleichgewichtsverhältnis ändert sich im Produktivbetrieb**: Wenn die Trainingsdaten 1 % Betrug enthalten, der Produktivbetrieb aber 0,01 % sieht, müssen Schwellenwert und Klassengewichte neu kalibriert werden. Überwachen Sie die Klassenverteilung in den eingehenden Daten

## Siehe auch {#see-also}

- [[model-evaluation]]
- [[feature-engineering]]
- [[gradient-boosting]]
