---
title: Unsupervised Learning
category: models
tags: [data-science, ml, clustering, dimensionality-reduction, pca, kmeans]
---

# Unsupervised Learning

Learning from unlabeled data. Two main tasks: clustering (group similar items) and dimensionality reduction (compress features). Essential for exploratory analysis, segmentation, and preprocessing.

## Clustering

### K-Means
Partition data into k clusters by minimizing within-cluster distances.

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)
centroids = kmeans.cluster_centers_
```

**Algorithm**: 1) Random initial centroids -> 2) Assign points to nearest centroid -> 3) Update centroids as cluster means -> 4) Repeat until convergence.

**Choosing k**: Elbow method (plot inertia vs k, pick "elbow"), Silhouette score.

**Limitations**: assumes spherical clusters of similar size, sensitive to initialization, needs k specified upfront.

### DBSCAN (Density-Based)

Groups points in dense regions. Finds clusters of arbitrary shape. Identifies noise.

```python
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=1.0, min_samples=20)
labels = db.fit_predict(X)
# label = -1 means noise point
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
```

- **eps**: neighborhood radius
- **min_samples**: minimum points for core point
- Point types: core (dense neighborhood), border (in core's neighborhood), noise (-1)
- No need to specify number of clusters
- Struggles with varying density

### Hierarchical Clustering

Build tree of clusters by merging (agglomerative) or splitting (divisive).

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

hc = AgglomerativeClustering(n_clusters=5, linkage='ward')
labels = hc.fit_predict(X)

# Dendrogram to choose k
Z = linkage(X, method='ward')
dendrogram(Z)
```

**Linkage methods**: single (min distance), complete (max), average, ward (minimize variance).

### Clustering Metrics

| Metric | Range | Use |
|--------|-------|-----|
| Silhouette | [-1, 1] | Higher = better separated clusters |
| Inertia | [0, inf) | Lower = tighter clusters (within k-means) |
| Calinski-Harabasz | [0, inf) | Higher = better defined clusters |
| Adjusted Rand Index | [-1, 1] | Compare to ground truth if available |

```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, labels)
```

## Dimensionality Reduction

### PCA (Principal Component Analysis)

Find directions of maximum variance. Project data onto top k components.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X_scaled)  # ALWAYS scale first!

# Explained variance ratio
print(pca.explained_variance_ratio_)
# e.g., [0.72, 0.15] = first two components explain 87% of variance

# Choose n_components to explain 95% of variance
pca = PCA(n_components=0.95)
X_reduced = pca.fit_transform(X_scaled)
print(f"Components needed: {pca.n_components_}")
```

**Math**: eigenvectors of covariance matrix = principal components. Eigenvalues = variance explained per component.

**Use cases**: visualization (2D projection), noise reduction, preprocessing for models, feature compression.

### t-SNE

Non-linear dimensionality reduction for **visualization only**.

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_2d = tsne.fit_transform(X)
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, alpha=0.5)
```

**Gotcha**: t-SNE is stochastic, non-deterministic without seed, and distances between clusters are NOT meaningful. Only use for visualization, never as features for downstream models.

### UMAP

Faster than t-SNE, preserves more global structure.

```python
import umap
reducer = umap.UMAP(n_components=2, random_state=42)
X_2d = reducer.fit_transform(X)
```

### SVD (Singular Value Decomposition)

Any matrix A = U * Sigma * V^T. Truncated SVD keeps top k singular values.

```python
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=50)
X_reduced = svd.fit_transform(X_sparse)  # works with sparse matrices (TF-IDF)
```

**Applications**: matrix approximation, recommendation systems, text (Latent Semantic Analysis).

## Applications

- **Customer segmentation**: K-Means/DBSCAN on behavioral features
- **Anomaly detection**: points far from any cluster center
- **Topic modeling**: clustering documents in TF-IDF or embedding space
- **Feature compression**: PCA before training to speed up models
- **Visualization**: t-SNE/UMAP to understand high-dimensional data

## Gotchas
- K-Means requires feature scaling (uses Euclidean distance)
- PCA requires standardized features (otherwise dominated by high-variance features)
- t-SNE with different perplexity values can produce very different plots - always try multiple
- Clustering is subjective - no "correct" number of clusters
- DBSCAN eps is scale-dependent - normalize features first

## See Also
- [[feature-engineering]] - PCA as preprocessing step
- [[neural-networks]] - autoencoders for non-linear dimensionality reduction
- [[math-linear-algebra]] - eigenvalues and SVD theory
- [[model-evaluation]] - clustering evaluation metrics
