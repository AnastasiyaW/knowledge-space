---
title: "Modellbewertung und Validierung"
category: techniques
tags: [data-science, ml, metrics, cross-validation, evaluation]
level: 3
source_sha256: 01a49cc78ad24adadf7d30fa113abd9ee7b4097740526b185591c6ac788f8784
translation: machine
translated_at: '2026-10-24'
---
# Modellbewertung und Validierung {#model-evaluation-and-validation}

Die Wahl der richtigen Metrik und der Validierungsstrategie ist genauso wichtig wie die Wahl des Modells. Falsche Metrik = Optimierung auf das falsche Ziel. Falsche Validierung = Überschätzung der Leistung.

## Metriken für Regression {#regression-metrics}

| Metrik | Formel | Wann verwenden |
|--------|--------|----------------|
| MAE | mean(\|actual - predicted\|) | Intuitiv, in den Originaleinheiten |
| MAPE | mean(\|actual - predicted\| / actual) | Wenn ein prozentualer Fehler benötigt wird |
| MSE | mean((actual - predicted)^2) | Bestraft große Fehler stärker |
| RMSE | sqrt(MSE) | Gleiche Einheiten wie das Ziel, bestraft große Fehler |
| R^2 | 1 - SS_res/SS_tot | Anteil der erklärten Varianz |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
```

**Fallstrick**: MAPE funktioniert nicht, wenn die tatsächlichen Werte nahe null liegen (Division durch null). R^2 kann negativ werden (Modell schlechter als die Vorhersage des Mittelwerts).

## Metriken für Klassifikation {#classification-metrics}

### Konfusionsmatrix {#confusion-matrix}

| | Vorhersage 0 | Vorhersage 1 |
|--|------------|------------|
| **Tatsächlich 0** | TN | FP |
| **Tatsächlich 1** | FN | TP |

```python
from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_true, y_pred)
print(classification_report(y_true, y_pred))
```

### Zentrale Metriken {#key-metrics}

| Metrik | Formel | Optimieren, wenn |
|--------|--------|------------------|
| Precision | TP / (TP + FP) | FP teuer sind (Spam-Filter, fälschliche Betrugsbeschuldigung) |
| Recall | TP / (TP + FN) | FN teuer sind (Krankheitserkennung, Betrugserkennung) |
| F1 | 2*P*R / (P+R) | Ausgleich zwischen Precision und Recall |
| Accuracy | (TP+TN) / total | Bei unausgewogenen Klassen **vermeiden** |

### ROC AUC {#roc-auc}

Schwellenwertunabhängige Metrik. Bewertet die Rangordnungsqualität der Modell-Scores.

```python
from sklearn.metrics import roc_auc_score, roc_curve

auc = roc_auc_score(y_true, scores)  # scores, not predictions!
fpr, tpr, thresholds = roc_curve(y_true, scores)

import matplotlib.pyplot as plt
plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.plot([0,1], [0,1], 'k--')  # random baseline
plt.xlabel('FPR'); plt.ylabel('TPR')
plt.legend()
```

**Interpretation**: Wahrscheinlichkeit, dass ein zufällig gewähltes positives Beispiel einen höheren Score hat als ein zufällig gewähltes negatives. 0.5 = Zufall, 1.0 = perfekt.

### Precision-Recall-Kurve {#precision-recall-curve}

Bei stark unausgewogenen Daten besser geeignet als ROC:

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

prec, rec, thresholds = precision_recall_curve(y_true, scores)
ap = average_precision_score(y_true, scores)
```

### Wahl des Schwellenwerts {#threshold-selection}

Modelle liefern Scores (Wahrscheinlichkeiten). Um daraus binäre Vorhersagen zu machen, muss ein Schwellenwert gewählt werden.

```python
# Business context determines threshold
threshold = 0.3  # lower = higher recall, lower precision
y_pred = (scores >= threshold).astype(int)
```

Ein höherer Schwellenwert = weniger, aber sicherere Vorhersagen (höhere Precision, geringerer Recall).

## Metriken für Ranking {#ranking-metrics}

| Metrik | Beschreibung |
|--------|--------------|
| precision@k | Anteil relevanter Elemente unter den Top-k |
| mAP@k | Mittlere Average Precision über alle Anfragen |
| nDCG@k | Positionsgewichtete Relevanz: DCG = sum((2^y_i - 1) / log(i+1)) |

## Kreuzvalidierung {#cross-validation}

Eine einzelne Train/Test-Aufteilung hängt vom Zufallsseed ab. K-Fold liefert robustere Schätzungen.

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

# Simple K-fold
scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
print(f"Mean AUC: {scores.mean():.3f} +/- {scores.std():.3f}")

# Stratified (preserves class ratio) - use for classification
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='f1')

# Time series: use TimeSeriesSplit (no future leakage)
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
```

### Aufteilung in Training / Validierung / Test {#train-validation-test-split}

```python
from sklearn.model_selection import train_test_split

# 60/20/20 split
train, test = train_test_split(df, test_size=0.2, random_state=42)
train, val = train_test_split(train, test_size=0.25, random_state=42)
# 0.25 of 0.8 = 0.2
```

- **Training**: Modell anpassen
- **Validierung**: Hyperparameter abstimmen, Features auswählen
- **Test**: finale Bewertung EINMAL (niemals auf dem Testset abstimmen)

## Bias-Varianz-Tradeoff {#bias-variance-tradeoff}

- **Hoher Bias** (Underfitting): Modell zu einfach, erfasst Muster nicht. Fehler sowohl im Training als auch in der Validierung hoch
- **Hohe Varianz** (Overfitting): Modell zu komplex, memoriert Rauschen. Trainingsfehler niedrig, Validierungsfehler hoch
- **Diagnose**: große Lücke zwischen Training- und Validierungsleistung = Overfitting

**Lösungen für Overfitting**: Regularisierung, einfacheres Modell, mehr Daten, Early Stopping, Dropout, Kreuzvalidierung.

## Fallstricke {#gotchas}
- **Accuracy-Falle**: Bei einer Klassenverteilung von 99/1 erreicht die Vorhersage „immer 0“ eine Accuracy von 99 %
- **Data Leakage**: Vorverarbeitung auf dem gesamten Datensatz (einschließlich Testdaten) gefittet, dies verfälscht die Metriken nach oben
- **Kontamination des Testsets**: Wer irgendetwas auf dem Testset abstimmt, dessen Ergebnis ist nicht mehr unverzerrt
- **Klassenungleichgewicht**: F1, PR-AUC oder ROC AUC statt Accuracy verwenden
- **Metrikauswahl**: die Metrik optimieren, die zum Geschäftsziel passt, nicht diejenige, die am besten aussieht
- **Overfitting auf die Validierung**: intensives Hyperparameter-Tuning kann auch auf das Validierungsset overfitten

## Siehe auch {#see-also}
- [[gradient-boosting]] - primäre Modelle zur Bewertung
- [[linear-models]] - einfache Baselines zum Vergleich
- [[hypothesis-testing]] - statistische Tests für Modellunterschiede
- [[ds-workflow]] - Bewertung im Kontext des gesamten Projekts
