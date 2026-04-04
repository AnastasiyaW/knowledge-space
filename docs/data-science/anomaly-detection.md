---
title: Anomaly Detection
category: concepts
tags: [data-science, anomaly-detection, outlier-detection, isolation-forest, autoencoder]
---

# Anomaly Detection

Identifying data points that deviate significantly from normal behavior. Critical for fraud detection, system monitoring, manufacturing QA, and cybersecurity. Three types: point anomalies (single outlier), contextual (anomalous in context), collective (group of points anomalous together).

## Statistical Methods

### Z-Score / IQR

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

- Z-score assumes normal distribution. Fails on skewed data
- IQR more robust but misses anomalies in multimodal distributions
- Grubbs test for single outlier in univariate normal data

### Mahalanobis Distance

Multivariate extension - accounts for correlations between features:

```python
from scipy.spatial.distance import mahalanobis

mean = np.mean(X, axis=0)
cov = np.cov(X.T)
cov_inv = np.linalg.inv(cov)

distances = [mahalanobis(x, mean, cov_inv) for x in X]
threshold = np.percentile(distances, 97.5)  # chi-squared distribution
```

## Machine Learning Methods

### Isolation Forest

Random forest variant. Anomalies are easier to isolate (shorter path length in random trees).

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

**How it works**: randomly select feature, randomly select split value. Anomalies need fewer splits to isolate. Average path length across all trees is the anomaly score.

### Local Outlier Factor (LOF)

Density-based. Compares local density of a point to its neighbors. Points in low-density regions relative to neighbors are anomalies.

```python
from sklearn.neighbors import LocalOutlierFactor

lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
predictions = lof.fit_predict(X)  # -1 = anomaly
scores = lof.negative_outlier_factor_  # more negative = more anomalous
```

### One-Class SVM

Learns boundary around normal data in kernel space:

```python
from sklearn.svm import OneClassSVM

oc_svm = OneClassSVM(kernel='rbf', gamma='auto', nu=0.05)
oc_svm.fit(X_train)  # train on normal data only
predictions = oc_svm.predict(X_test)
```

## Deep Learning Methods

### Autoencoder-Based Detection

Train autoencoder on normal data. High reconstruction error = anomaly.

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

### Variational Autoencoder (VAE)

Better calibrated anomaly scores via probabilistic reconstruction:
- Anomaly score = reconstruction probability (not just error)
- KL divergence term regularizes latent space
- More robust threshold selection

## Time Series Anomaly Detection

- **Seasonal decomposition + residual monitoring**: STL decompose, flag residuals > threshold
- **Prophet anomaly detection**: fit Prophet model, flag points outside prediction intervals
- **LSTM autoencoder**: encode temporal patterns, reconstruction error on sliding windows
- **Change point detection**: CUSUM, Bayesian Online Changepoint Detection (BOCD)

```python
# Simple sliding window approach
def detect_anomalies_timeseries(series, window=50, threshold=3):
    rolling_mean = series.rolling(window).mean()
    rolling_std = series.rolling(window).std()
    z_scores = (series - rolling_mean) / rolling_std
    return z_scores.abs() > threshold
```

## Evaluation Metrics

Standard accuracy is misleading because anomalies are rare (imbalanced).

- **Precision/Recall/F1** at different thresholds
- **AUROC**: area under ROC curve. Threshold-independent
- **AUPRC**: area under precision-recall curve. Better for imbalanced datasets
- **Contamination tuning**: use validation set with known anomalies to set threshold

## Gotchas

- **Contamination parameter is critical**: setting contamination too high flags normal points as anomalies, too low misses real anomalies. If unknown, start with unsupervised methods (Isolation Forest) and manually inspect top-scoring points to estimate
- **Feature scaling matters**: distance-based methods (LOF, One-Class SVM, Mahalanobis) are sensitive to feature scales. Always StandardScaler or RobustScaler before fitting. Isolation Forest is scale-invariant
- **Concept drift in production**: normal behavior changes over time. Models trained on old data flag new-normal as anomalous. Retrain periodically or use online learning methods (streaming Isolation Forest)

## See Also

- [[unsupervised-learning]]
- [[time-series-analysis]]
- [[feature-engineering]]
- [[model-evaluation]]
