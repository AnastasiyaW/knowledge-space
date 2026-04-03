---
title: Dimensionality Reduction
category: ml-algorithms
tags: [pca, tsne, umap, dimensionality-reduction, feature-selection, sklearn]
---

# Dimensionality Reduction

Reduce the number of features while preserving meaningful structure. PCA finds directions of maximum variance; t-SNE and UMAP create low-dimensional visualizations. Essential for handling the curse of dimensionality, speeding up training, and visualizing [[clustering-and-unsupervised]] results.

## Key Facts

- **Curse of dimensionality**: as dimensions grow, data becomes sparse; distances become less meaningful; models need exponentially more data
- **PCA** (Principal Component Analysis): linear projection onto directions of maximum variance; uses [[linear-algebra]] eigendecomposition of covariance matrix
- **Explained variance ratio**: fraction of total variance captured by each component; cumulative sum tells you how many components to keep (e.g., 95% threshold)
- **t-SNE**: non-linear; preserves local neighborhoods; for visualization only (2D/3D); NOT for downstream ML
- **UMAP**: faster than t-SNE, preserves more global structure; can be used as a feature transformation (not just visualization)
- **Feature selection** vs. **feature extraction**: selection keeps original features (filter, wrapper, embedded methods); extraction creates new features (PCA, autoencoders)
- PCA components are linear combinations of original features; lose interpretability
- Always standardize data before PCA -- it is based on variance, and scale affects variance
- For sparse data (text TF-IDF), use **TruncatedSVD** instead of PCA (no centering needed)
- **Kernel PCA**: non-linear PCA using kernel trick; RBF kernel for non-linear manifolds
- Typical pipeline: StandardScaler -> PCA -> downstream model (classifier/clusterer)

## Patterns

```python
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import numpy as np

# Standardize first (critical for PCA)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA - find optimal number of components
pca_full = PCA()
pca_full.fit(X_scaled)
cumulative_var = np.cumsum(pca_full.explained_variance_ratio_)
n_components_95 = np.argmax(cumulative_var >= 0.95) + 1
print(f"Components for 95% variance: {n_components_95}")

# PCA - reduce dimensions
pca = PCA(n_components=n_components_95)
X_pca = pca.fit_transform(X_scaled)
print(f"Shape: {X.shape} -> {X_pca.shape}")
print(f"Explained variance: {pca.explained_variance_ratio_.sum():.4f}")

# PCA for visualization (2D)
pca_2d = PCA(n_components=2)
X_2d = pca_2d.fit_transform(X_scaled)
# plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels)

# t-SNE for visualization
tsne = TSNE(
    n_components=2,
    perplexity=30,       # 5-50; smaller = more local structure
    learning_rate='auto',
    n_iter=1000,
    random_state=42
)
X_tsne = tsne.fit_transform(X_scaled)
# NOTE: t-SNE has no .transform() method -- cannot apply to new data

# UMAP (install: pip install umap-learn)
# import umap
# reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1)
# X_umap = reducer.fit_transform(X_scaled)
# X_new_umap = reducer.transform(X_new_scaled)  # can transform new data

# TruncatedSVD for sparse data (e.g., TF-IDF)
from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf = TfidfVectorizer(max_features=10000)
# X_sparse = tfidf.fit_transform(texts)
# svd = TruncatedSVD(n_components=100)
# X_reduced = svd.fit_transform(X_sparse)

# PCA in sklearn pipeline
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=0.95)),  # keep 95% variance
    ('clf', LogisticRegression(max_iter=1000))
])
pipe.fit(X_train, y_train)
```

## Gotchas

- t-SNE is stochastic and non-parametric -- different runs give different results; distances between clusters are NOT meaningful
- t-SNE `perplexity` changes output dramatically; try multiple values (5, 15, 30, 50)
- PCA on unscaled data: first component will just capture the feature with largest range, not most informative direction
- PCA with `n_components=0.95` (float) means "keep components until 95% variance explained" -- convenient shortcut
- t-SNE/UMAP for visualization only; do NOT use t-SNE output as features for a classifier
- PCA `.transform()` uses learned components to transform new data; t-SNE cannot do this

## See Also

- [[linear-algebra]] - PCA = eigendecomposition of covariance matrix, or SVD of data matrix
- [[clustering-and-unsupervised]] - visualize clusters in reduced dimensions
- [[feature-engineering]] - PCA as feature extraction; compare with manual feature selection
- sklearn decomposition: https://scikit-learn.org/stable/modules/decomposition.html
