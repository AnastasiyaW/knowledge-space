---
title: "Data-Science-Workflow und Best Practices"
category: practices
tags: [data-science, workflow, methodology, best-practices]
level: 3
source_sha256: eda26c01e742aa2cc3921c73c6f97fa30bdc2d405ee01dbdd6df1823015ebb59
translation: machine
translated_at: '2026-10-24'
---
# Data-Science-Workflow und Best Practices {#data-science-workflow-and-best-practices}

Methodik für End-to-End-Projekte. Der Unterschied zwischen einem Spielzeugmodell und einer produktionsreifen Lösung liegt in der Prozessdisziplin.

## Projektablauf {#project-workflow}

### 1. Problemdefinition {#1-problem-definition}
- Geschäftsziel verstehen (nicht nur das ML-Ziel)
- Erfolgsmetrik definieren (sowohl ML-Metrik ALS AUCH Geschäftsmetrik)
- Klären, ob ML überhaupt nötig ist – manchmal reichen einfache Regeln

### 2. Datenerhebung {#2-data-collection}
- SQL-Abfragen aus Datenbanken
- API-Aufrufe, CSV/Excel von Fachabteilungen
- Feature Stores / Data Warehouses
- Web Scraping (mit Erlaubnis)

### 3. EDA (Explorative Datenanalyse) {#3-eda-exploratory-data-analysis}
- Shape, dtypes, `describe()`
- Fehlende Werte (Anteil pro Spalte)
- Verteilung der Zielvariable (ausgeglichen? schief?)
- Univariat: Histogramme (numerisch), value_counts (kategorisch)
- Bivariat: Korrelationsmatrix, groupby + Mittelwert des Ziels
- Ausreißer: Boxplots, z-Scores, IQR-Methode

### 4. Vorverarbeitung {#4-preprocessing}
- Fehlende Werte behandeln (imputieren oder entfernen)
- Ausreißer behandeln (kappen, entfernen oder beibehalten)
- Kategorische Merkmale kodieren
- Numerische Merkmale skalieren
- Train-/Validation-/Test-Splits erstellen
- Feature Engineering

### 5. Modellierung {#5-modeling}
- Mit einer einfachen Baseline beginnen (Mittelwertvorhersage, logistische Regression)
- Mehrere Modellfamilien ausprobieren (linear, baumbasiert, Ensemble)
- Kreuzvalidierung für verlässliche Schätzungen verwenden
- Experimente nachverfolgen

### 6. Evaluation {#6-evaluation}
- Mit der Baseline vergleichen
- Auf Overfitting prüfen (Lücke zwischen Train- und Validation-Performance)
- Fehleranalyse: Was macht das Modell falsch?
- Feature-Importance
- Finale Evaluation auf dem zurückgehaltenen Testset EINMALIG

### 7. Deployment {#7-deployment}
- Modell exportieren (pickle, ONNX, model.save())
- Prediction-API erstellen (Flask, FastAPI)
- Monitoring einrichten (Data Drift, Modellverschlechterung)
- A/B-Test in der Produktion

## Häufige Fallstricke {#common-pitfalls}

### Data Leakage {#data-leakage}
Informationen aus der Zukunft oder aus dem Testset fließen in das Training ein. **Der gefährlichste Fehler.**

- **Target Leakage**: Merkmal stammt aus dem Ziel oder korreliert damit
- **Train-Test-Leakage**: Vorverarbeitung wird auf dem gesamten Datensatz inklusive Testset gefittet
- **Temporal Leakage**: Zukünftige Daten werden zur Vorhersage der Vergangenheit verwendet

**Prävention**: Immer VOR jeder Vorverarbeitung splitten. Sklearn-Pipelines verwenden.

### Overfitting {#overfitting}
Das Modell memoriert die Trainingsdaten und versagt bei neuen Daten.
- **Symptome**: große Lücke zwischen Train- und Validation-Performance
- **Lösungen**: Regularisierung, einfacheres Modell, mehr Daten, Early Stopping, Dropout, CV

### Klassenungleichgewicht {#class-imbalance}
Eine Klasse übertrifft die anderen deutlich (99 % negativ, 1 % positiv).
- **Problem**: Das Modell sagt die Mehrheitsklasse vorher und erreicht dadurch hohe Accuracy
- **Lösungen**: Klassengewichte, SMOTE/Oversampling, Undersampling, F1-/PR-AUC-Metriken

### Selection Bias {#selection-bias}
- **Survivorship Bias**: Es werden nur erfolgreiche Beispiele betrachtet
- **Sampling Bias**: Nicht zufällige Datenerhebung

## Reproduzierbarkeit {#reproducibility}

```python
import numpy as np
import random
import torch

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

# sklearn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=SEED)
```

**Checkliste:**
- Bibliotheksversionen in requirements.txt festschreiben
- Datenquellen und Vorverarbeitungsschritte dokumentieren
- Trainierte Modelle und Parameter speichern
- Code mit Versionskontrolle (git) verwalten
- Experimentergebnisse festhalten

## Kommunikation {#communication}

- **Mit dem geschäftlichen Nutzen beginnen**, nicht mit dem Modell
- Metriken zeigen, die das Business versteht (Umsatz, Kosteneinsparungen)
- Grenzen und Randfälle erläutern
- Visualisierungen verwenden (Heatmap der Confusion Matrix, Feature-Importance)
- Konfidenzintervalle angeben, nicht nur Punktschätzungen

## Stolperfallen {#gotchas}
- Wochenlang am Modell arbeiten, obwohl das eigentliche Problem schlechte Datenqualität ist
- Die falsche Metrik optimieren (hohe Accuracy bei unausgewogenen Daten)
- Nicht zuerst mit einer einfachen Baseline vergleichen
- Ohne Monitoring deployen – Modelle verschlechtern sich unbemerkt
- Domänenexperten ignorieren, die die Daten besser verstehen als jeder Algorithmus

## Siehe auch {#see-also}
- [[model-evaluation]] - Metriken und Validierungsstrategien
- [[feature-engineering]] - der Schritt mit dem höchsten ROI
- [[pandas-eda]] - praktische Umsetzung der EDA
- [[hypothesis-testing]] - A/B-Tests bereitgestellter Modelle
