---
title: "Détection d'anomalies"
category: concepts
tags: [data-science, anomaly-detection, outlier-detection, isolation-forest, autoencoder]
level: 3
source_sha256: 443c9f92c2723b45b7025b083856f0fbb615d160e7aea609e98562e06753949e
translation: machine
translated_at: '2026-10-24'
---
# Détection d'anomalies {#anomaly-detection}

Identification des points de données qui s'écartent significativement du comportement normal. Essentielle pour la détection de fraude, la surveillance des systèmes, le contrôle qualité en fabrication et la cybersécurité. Trois types : les anomalies ponctuelles (valeur aberrante isolée), les anomalies contextuelles (anormales dans un contexte donné) et les anomalies collectives (groupe de points anormaux ensemble).

## Méthodes statistiques {#statistical-methods}

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

- Le Z-score suppose une distribution normale. Il est inefficace sur des données asymétriques
- L'IQR est plus robuste, mais il manque les anomalies dans les distributions multimodales
- Test de Grubbs pour une valeur aberrante unique dans des données univariées normales

### Distance de Mahalanobis {#mahalanobis-distance}

Extension multivariée : elle prend en compte les corrélations entre les variables :

```python
from scipy.spatial.distance import mahalanobis

mean = np.mean(X, axis=0)
cov = np.cov(X.T)
cov_inv = np.linalg.inv(cov)

distances = [mahalanobis(x, mean, cov_inv) for x in X]
threshold = np.percentile(distances, 97.5)  # chi-squared distribution
```

## Méthodes d'apprentissage automatique {#machine-learning-methods}

### Isolation Forest {#isolation-forest}

Variante de la forêt aléatoire. Les anomalies sont plus faciles à isoler (longueur de chemin plus courte dans les arbres aléatoires).

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

**Fonctionnement** : on sélectionne aléatoirement une variable, puis une valeur de coupure aléatoire. Les anomalies nécessitent moins de coupures pour être isolées. La longueur moyenne du chemin sur l'ensemble des arbres constitue le score d'anomalie.

### Local Outlier Factor (LOF) {#local-outlier-factor-lof}

Méthode fondée sur la densité. Elle compare la densité locale d'un point à celle de ses voisins. Les points situés dans des régions de faible densité par rapport à leurs voisins sont considérés comme des anomalies.

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
predictions = lof.fit_predict(X)  # -1 = anomaly
scores = lof.negative_outlier_factor_  # more negative = more anomalous
```

### One-Class SVM {#one-class-svm}

Apprend une frontière autour des données normales dans l'espace des noyaux :

```python
from sklearn.svm import OneClassSVM

oc_svm = OneClassSVM(kernel='rbf', gamma='auto', nu=0.05)
oc_svm.fit(X_train)  # train on normal data only
predictions = oc_svm.predict(X_test)
```

## Méthodes d'apprentissage profond {#deep-learning-methods}

### Détection par autoencodeur {#autoencoder-based-detection}

Entraînement d'un autoencodeur sur des données normales. Une erreur de reconstruction élevée indique une anomalie.

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

### Autoencodeur variationnel (VAE) {#variational-autoencoder-vae}

Scores d'anomalie mieux calibrés grâce à une reconstruction probabiliste :
- Score d'anomalie = probabilité de reconstruction (et non uniquement l'erreur)
- Le terme de divergence KL régularise l'espace latent
- Sélection du seuil plus robuste

## Détection d'anomalies dans les séries temporelles {#time-series-anomaly-detection}

- **Décomposition saisonnière + surveillance des résidus** : décomposition STL, signalement des résidus supérieurs à un seuil
- **Détection d'anomalies avec Prophet** : ajustement d'un modèle Prophet, signalement des points situés en dehors des intervalles de prédiction
- **Autoencodeur LSTM** : encodage des motifs temporels, erreur de reconstruction sur des fenêtres glissantes
- **Détection de points de rupture** : CUSUM, Bayesian Online Changepoint Detection (BOCD)

```python
# Simple sliding window approach
def detect_anomalies_timeseries(series, window=50, threshold=3):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    z_scores = (series - rolling_mean) / rolling_std
    return z_scores.abs() > threshold
```

## Métriques d'évaluation {#evaluation-metrics}

L'exactitude (accuracy) standard est trompeuse, car les anomalies sont rares (données déséquilibrées).

- **Précision / Rappel / F1** à différents seuils
- **AUROC** : aire sous la courbe ROC. Indépendante du seuil
- **AUPRC** : aire sous la courbe précision-rappel. Plus adaptée aux jeux de données déséquilibrés
- **Réglage du taux de contamination** : utiliser un jeu de validation contenant des anomalies connues pour fixer le seuil

## Pièges à éviter {#gotchas}

- **Le paramètre de contamination est critique** : une valeur trop élevée signale des points normaux comme anomalies, une valeur trop basse fait manquer de vraies anomalies. Si elle est inconnue, commencez par des méthodes non supervisées (Isolation Forest) et inspectez manuellement les points les mieux scorés pour l'estimer
- **La mise à l'échelle des variables compte** : les méthodes fondées sur les distances (LOF, One-Class SVM, Mahalanobis) sont sensibles à l'échelle des variables. Appliquez systématiquement StandardScaler ou RobustScaler avant l'ajustement. Isolation Forest est invariant à l'échelle
- **Dérive conceptuelle en production** : le comportement normal évolue dans le temps. Les modèles entraînés sur d'anciennes données signalent le nouveau comportement normal comme anormal. Réentraînez-les périodiquement ou utilisez des méthodes d'apprentissage en ligne (Isolation Forest en flux)

## Voir aussi {#see-also}

- [[unsupervised-learning]]
- [[time-series-analysis]]
- [[feature-engineering]]
- [[model-evaluation]]
