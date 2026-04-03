---
title: Clustering and Unsupervised Learning
category: ml-algorithms
tags: [clustering, kmeans, dbscan, hierarchical, unsupervised, sklearn]
---

# Clustering and Unsupervised Learning

Find structure in unlabeled data. Clustering groups similar data points; density estimation models data distribution. Used for customer segmentation, anomaly detection, topic discovery, and as a preprocessing step for [[feature-engineering]].

## Key Facts

- **K-Means**: partition data into k clusters by minimizing within-cluster sum of squares; requires specifying k
- **K-Means++**: smart initialization that spreads initial centroids apart; default in sklearn
- **Elbow method**: plot inertia (within-cluster SSE) vs. k; look for "elbow" where improvement slows
- **Silhouette score**: measures how similar a point is to its own cluster vs. nearest neighbor cluster; range [-1, 1]; higher is better
- **DBSCAN**: density-based; finds arbitrary-shaped clusters; marks low-density points as noise; parameters: eps (radius), min_samples
- **Hierarchical clustering**: builds a tree (dendrogram); agglomerative (bottom-up) or divisive (top-down); no need to pre-specify k
- **Gaussian Mixture Models (GMM)**: soft clustering; each cluster is a Gaussian distribution; uses EM algorithm; BIC/AIC for model selection
- K-Means assumes spherical, equal-size clusters; fails on elongated or varying-density clusters
- DBSCAN does not require k but is sensitive to eps; use k-distance plot to estimate eps
- Always scale features before clustering -- distances are scale-dependent; see [[linear-algebra]]
- [[dimensionality-reduction]] (PCA, t-SNE) is commonly used to visualize clusters in 2D

## Patterns

```python
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np

# Scale features first
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means
kmeans = KMeans(n_clusters=3, init='k-means++', n_init=10, random_state=42)
labels = kmeans.fit_predict(X_scaled)
centroids = kmeans.cluster_centers_
inertia = kmeans.inertia_  # within-cluster SSE

# Elbow method
inertias = []
K_range = range(2, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
# Plot K_range vs inertias, look for elbow

# Silhouette score
sil_score = silhouette_score(X_scaled, labels)
# Good: > 0.5; Reasonable: 0.25-0.5; Poor: < 0.25

# DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
labels_db = dbscan.fit_predict(X_scaled)
n_clusters = len(set(labels_db)) - (1 if -1 in labels_db else 0)
n_noise = (labels_db == -1).sum()

# Estimate eps with k-distance plot
from sklearn.neighbors import NearestNeighbors
nn = NearestNeighbors(n_neighbors=5)
nn.fit(X_scaled)
distances, _ = nn.kneighbors(X_scaled)
# Sort and plot distances[:, -1] -- look for "knee"

# Hierarchical clustering
from scipy.cluster.hierarchy import dendrogram, linkage
Z = linkage(X_scaled, method='ward')
# dendrogram(Z)  # visualize

agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
labels_agg = agg.fit_predict(X_scaled)

# Gaussian Mixture Model (soft clustering)
gmm = GaussianMixture(n_components=3, random_state=42)
labels_gmm = gmm.fit_predict(X_scaled)
proba = gmm.predict_proba(X_scaled)  # soft assignments
bic = gmm.bic(X_scaled)  # lower BIC = better model
```

## Gotchas

- K-Means result depends on initialization; always use `n_init=10` (default) and `init='k-means++'`
- K-Means with `n_clusters` too high will always decrease inertia; it does not mean better clustering
- DBSCAN labels noise as -1; silhouette_score breaks if you include noise points -- filter them first
- Hierarchical clustering with `linkage='ward'` only works with Euclidean distance
- GMM with too many components overfits; use BIC (lower is better) to select n_components
- Clustering results are not deterministic across runs for K-Means; set `random_state` for reproducibility

## See Also

- [[dimensionality-reduction]] - PCA/t-SNE for visualizing clusters
- [[feature-engineering]] - cluster labels as new features for supervised models
- [[model-evaluation-metrics]] - silhouette, Calinski-Harabasz, Davies-Bouldin for cluster quality
- sklearn clustering: https://scikit-learn.org/stable/modules/clustering.html
