---
title: "Anomalieerkennung"
category: concepts
tags: [data-science, anomaly-detection, outlier-detection, isolation-forest, autoencoder]
level: 3
source_sha256: 443c9f92c2723b45b7025b083856f0fbb615d160e7aea609e98562e06753949e
translation: machine
translated_at: '2026-10-24'
---
# Anomalieerkennung {#anomaly-detection}

Identifizierung von Datenpunkten, die deutlich vom normalen Verhalten abweichen. Entscheidend für Betrugserkennung, Systemüberwachung, Qualitätssicherung in der Fertigung und Cybersicherheit. Es gibt drei Typen: Punktanomalien (einzelner Ausreißer), kontextuelle Anomalien (im Kontext auffällig) und kollektive Anomalien (Gruppe von Punkten, die gemeinsam auffällig sind).

## Statistische Methoden {#statistical-methods}

### Z-Score / IQR {#z-score-iqr}

```python
import numpy as np
from scipy import stats

# Z-score: flag points > 3 standard deviations
z_scores = np.abs(stats.zscore(data))
anomalies = data[z_scores > 3]

# IQR method: robust to non-normal distributions
Q1, Q3 = np.percentile(data, [25, 75])
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
anomalies = data[(data < lower) | (data > upper)]
```

- Der Z-Score setzt eine Normalverteilung voraus. Er versagt bei schiefen Daten
- Der IQR ist robuster, übersieht aber Anomalien in multimodalen Verteilungen
- Grubbs-Test für einzelne Ausreißer in univariaten, normalverteilten Daten

### Mahalanobis-Distanz {#mahalanobis-distance}

Multivariate Erweiterung, die Korrelationen zwischen Merkmalen berücksichtigt:

```python
from scipy.spatial.distance import mahalanobis

mean = np.mean(X, axis=0)
cov = np.cov(X.T)
cov_inv = np.linalg.inv(cov)

distances = [mahalanobis(x, mean, cov_inv) for x in X]
threshold = np.percentile(distances, 97.5)  # chi-squared distribution
```

## Methoden des maschinellen Lernens {#machine-learning-methods}

### Isolation Forest {#isolation-forest}

Variante des Random Forest. Anomalien lassen sich leichter isolieren (kürzere Pfadlänge in zufälligen Bäumen).

```python
from sklearn.ensemble import IsolationForest

iso_forest = IsolationForest(
    n_estimators=100,
    contamination=0.05,  # expected fraction of anomalies
    random_state=42
)
predictions = iso_forest.fit_predict(X)  # -1 = anomaly, 1 = normal
scores = iso_forest.decision_function(X)  # lower = more anomalous
```

**Funktionsweise**: Ein Merkmal und ein Split-Wert werden zufällig gewählt. Anomalien benötigen weniger Splits, um isoliert zu werden. Die durchschnittliche Pfadlänge über alle Bäume ist der Anomalie-Score.

### Local Outlier Factor (LOF) {#local-outlier-factor-lof}

Dichtebasiert. Vergleicht die lokale Dichte eines Punktes mit der seiner Nachbarn. Punkte, die im Vergleich zu ihren Nachbarn in Regionen niedriger Dichte liegen, sind Anomalien.

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
predictions = lof.fit_predict(X)  # -1 = anomaly
scores = lof.negative_outlier_factor_  # more negative = more anomalous
```

### One-Class SVM {#one-class-svm}

Lernt eine Grenze um die normalen Daten im Kernel-Raum:

```python
from sklearn.svm import OneClassSVM

oc_svm = OneClassSVM(kernel='rbf', gamma='auto', nu=0.05)
oc_svm.fit(X_train)  # train on normal data only
predictions = oc_svm.predict(X_test)
```

## Deep-Learning-Methoden {#deep-learning-methods}

### Autoencoder-basierte Erkennung {#autoencoder-based-detection}

Trainiere einen Autoencoder auf normalen Daten. Ein hoher Rekonstruktionsfehler bedeutet eine Anomalie.

```python
import torch
import torch.nn as nn

class AnomalyAutoencoder(nn.Module):
    def __init__(self, input_dim, latent_dim=16):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

# Training: minimize reconstruction error on NORMAL data only
model = AnomalyAutoencoder(input_dim=X.shape[1])
criterion = nn.MSELoss()

# Detection: threshold on reconstruction error
with torch.no_grad():
    reconstructed = model(X_test)
    errors = ((X_test - reconstructed) ** 2).mean(dim=1)
    threshold = errors.quantile(0.95)
    anomalies = errors > threshold
```

### Variational Autoencoder (VAE) {#variational-autoencoder-vae}

Besser kalibrierte Anomalie-Scores durch probabilistische Rekonstruktion:
- Anomalie-Score = Rekonstruktionswahrscheinlichkeit (nicht nur Fehler)
- KL-Divergenz-Term regularisiert den latenten Raum
- Robustere Schwellenwertwahl

## Anomalieerkennung bei Zeitreihen {#time-series-anomaly-detection}

- **Saisonale Zerlegung + Überwachung der Residuen**: STL-Zerlegung, Residuen über dem Schwellenwert markieren
- **Anomalieerkennung mit Prophet**: Prophet-Modell anpassen, Punkte außerhalb der Vorhersageintervalle markieren
- **LSTM-Autoencoder**: zeitliche Muster kodieren, Rekonstruktionsfehler auf gleitenden Fenstern
- **Change-Point-Erkennung**: CUSUM, Bayesian Online Changepoint Detection (BOCD)

```python
# Simple sliding window approach
def detect_anomalies_timeseries(series, window=50, threshold=3):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    z_scores = (series - rolling_mean) / rolling_std
    return z_scores.abs() > threshold
```

## Bewertungsmetriken {#evaluation-metrics}

Die Standard-Genauigkeit ist irreführend, weil Anomalien selten sind (unausgewogene Daten).

- **Precision/Recall/F1** bei verschiedenen Schwellenwerten
- **AUROC**: Fläche unter der ROC-Kurve. Unabhängig vom Schwellenwert
- **AUPRC**: Fläche unter der Precision-Recall-Kurve. Besser für unausgewogene Datensätze
- **Contamination-Tuning**: Validierungsmenge mit bekannten Anomalien verwenden, um den Schwellenwert festzulegen

## Stolperfallen {#gotchas}

- **Der Contamination-Parameter ist entscheidend**: Ist er zu hoch gesetzt, werden normale Punkte als Anomalien markiert; ist er zu niedrig, werden echte Anomalien übersehen. Ist der Wert unbekannt, beginne mit unüberwachten Methoden (Isolation Forest) und prüfe die höchst bewerteten Punkte manuell, um ihn abzuschätzen
- **Die Merkmalsskalierung ist wichtig**: Distanzbasierte Methoden (LOF, One-Class SVM, Mahalanobis) reagieren empfindlich auf die Skalen der Merkmale. Vor dem Fitting immer StandardScaler oder RobustScaler verwenden. Isolation Forest ist skaleninvariant
- **Concept Drift im Produktivbetrieb**: Das normale Verhalten ändert sich mit der Zeit. Modelle, die auf alten Daten trainiert wurden, markieren neues Normalverhalten als anomal. Regelmäßig neu trainieren oder Online-Lernverfahren verwenden (Streaming Isolation Forest)

## Siehe auch {#see-also}

- [[unsupervised-learning]]
- [[time-series-analysis]]
- [[feature-engineering]]
- [[model-evaluation]]
