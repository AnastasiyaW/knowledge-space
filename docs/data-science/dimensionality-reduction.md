---
title: Dimensionality Reduction
category: concepts
tags: [data-science, pca, t-sne, umap, feature-selection, manifold-learning]
---

# Dimensionality Reduction

Reducing number of features while preserving important information. Two purposes: visualization (project to 2D/3D) and preprocessing (remove noise, speed up training, fight curse of dimensionality). Two approaches: feature selection (pick subset) and feature extraction (create new features).

## PCA (Principal Component Analysis)

Linear projection onto directions of maximum variance.

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Always scale before PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit PCA
pca = PCA(n_components=0.95)  # keep 95% of variance
X_pca = pca.fit_transform(X_scaled)

print(f"Reduced from {X.shape[1]} to {X_pca.shape[1]} features")
print(f"Explained variance per component: {pca.explained_variance_ratio_}")

# Scree plot to choose n_components
import matplotlib.pyplot as plt
cumvar = pca.explained_variance_ratio_.cumsum()
plt.plot(range(1, len(cumvar)+1), cumvar)
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance')
plt.axhline(y=0.95, color='r', linestyle='--')
```

**When to use**: preprocessing before ML, denoising, multicollinearity removal, visualization if data is roughly linear.

### Incremental PCA (for large datasets)

```python
from sklearn.decomposition import IncrementalPCA

ipca = IncrementalPCA(n_components=50, batch_size=1000)
for batch in data_loader:
    ipca.partial_fit(batch)
X_reduced = ipca.transform(X)
```

## t-SNE

Non-linear. Preserves local structure. Best for visualization, not preprocessing.

```python
from sklearn.manifold import TSNE

tsne = TSNE(
    n_components=2,
    perplexity=30,       # 5-50, controls neighborhood size
    learning_rate='auto',
    n_iter=1000,
    random_state=42
)
X_2d = tsne.fit_transform(X_scaled)

plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap='tab10', s=5, alpha=0.7)
```

**Perplexity**: controls effective number of neighbors. Low (5-10) = tight clusters, high (30-50) = global structure. Try multiple values.

## UMAP

Faster than t-SNE, preserves more global structure, can be used for preprocessing (unlike t-SNE).

```python
import umap

reducer = umap.UMAP(
    n_components=2,
    n_neighbors=15,       # local vs global balance
    min_dist=0.1,         # how tight clusters are (0.0 = very tight)
    metric='euclidean',
    random_state=42
)
X_2d = reducer.fit_transform(X_scaled)

# UMAP can transform new data (t-SNE cannot)
X_new_2d = reducer.transform(X_new)
```

**n_neighbors**: low (5-15) = local structure, high (50-200) = global structure. min_dist: low = tighter clusters, high = spread out.

## Feature Selection

### Filter Methods

Score features independently, select top-k:

```python
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

# ANOVA F-test (for classification)
selector = SelectKBest(f_classif, k=20)
X_selected = selector.fit_transform(X, y)
selected_features = X.columns[selector.get_support()]

# Mutual information (captures non-linear relationships)
mi_selector = SelectKBest(mutual_info_classif, k=20)
X_mi = mi_selector.fit_transform(X, y)

# Variance threshold (remove near-constant features)
from sklearn.feature_selection import VarianceThreshold
vt = VarianceThreshold(threshold=0.01)
X_filtered = vt.fit_transform(X)
```

### Wrapper Methods

Use model performance to evaluate feature subsets:

```python
from sklearn.feature_selection import RFE

# Recursive Feature Elimination
rfe = RFE(
    estimator=RandomForestClassifier(n_estimators=100),
    n_features_to_select=15,
    step=5  # remove 5 features per iteration
)
rfe.fit(X_train, y_train)
selected = X.columns[rfe.support_]
rankings = rfe.ranking_  # 1 = selected
```

### Embedded Methods

Feature importance from the model itself:

```python
# Tree-based importance
model = XGBClassifier()
model.fit(X_train, y_train)
importances = model.feature_importances_

# Permutation importance (model-agnostic, more reliable)
from sklearn.inspection import permutation_importance

perm_imp = permutation_importance(model, X_val, y_val, n_repeats=10)
sorted_idx = perm_imp.importances_mean.argsort()[::-1]

# L1 regularization (Lasso) for linear models
from sklearn.linear_model import LassoCV
lasso = LassoCV(cv=5).fit(X_scaled, y)
selected = X.columns[lasso.coef_ != 0]
```

## Autoencoders for Dimensionality Reduction

Non-linear alternative to PCA:

```python
import torch.nn as nn

class DimensionReducer(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, input_dim)
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z), z

# Use encoder output as reduced features
model.eval()
_, X_reduced = model(X_tensor)
```

## Gotchas

- **t-SNE cluster sizes and distances are meaningless**: t-SNE distorts distances to preserve local neighborhoods. A large cluster in t-SNE plot may not be larger in original space. Never interpret inter-cluster distances or cluster sizes. Use t-SNE only to confirm clusters exist, not to measure them
- **PCA on unscaled data = dominated by high-variance features**: if one feature ranges 0-1000 and another 0-1, PCA will pick the high-variance one regardless of importance. Always StandardScaler before PCA. Exception: if features are in same units (e.g., all pixel values 0-255)
- **Feature selection must happen inside cross-validation**: selecting features on full dataset then doing CV leaks information from validation fold. Use Pipeline to ensure selection happens only on training data each fold

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('selector', SelectKBest(f_classif, k=20)),
    ('model', RandomForestClassifier())
])
scores = cross_val_score(pipe, X, y, cv=5)  # correct: no leakage
```

## See Also

- [[feature-engineering]]
- [[unsupervised-learning]]
- [[neural-networks]]
- [[pca-and-classical-ml]]
