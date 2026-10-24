---
title: "Dimensionalitätsreduktion"
category: concepts
tags: [data-science, pca, t-sne, umap, feature-selection, manifold-learning]
level: 3
source_sha256: 412a39bdbad3c8c5e643c175eb03333b39b002fa2602ad8c728fa815e8c34ebd
translation: machine
translated_at: '2026-10-24'
---
# Dimensionalitätsreduktion {#dimensionality-reduction}

Reduzierung der Anzahl von Merkmalen unter Erhaltung wichtiger Informationen. Zwei Zwecke: Visualisierung (Projektion auf 2D/3D) und Vorverarbeitung (Rauschen entfernen, Training beschleunigen, dem Fluch der Dimensionalität entgegenwirken). Zwei Ansätze: Merkmalsauswahl (Auswahl einer Teilmenge) und Merkmalsextraktion (Erzeugung neuer Merkmale).

## PCA (Hauptkomponentenanalyse) {#pca-principal-component-analysis}

Lineare Projektion auf die Richtungen maximaler Varianz.

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

**Wann verwenden**: Vorverarbeitung vor dem maschinellen Lernen, Entrauschung, Entfernung von Multikollinearität, Visualisierung, wenn die Daten näherungsweise linear sind.

### Inkrementelle PCA (für große Datensätze) {#incremental-pca-for-large-datasets}

```python
from sklearn.decomposition import IncrementalPCA

ipca = IncrementalPCA(n_components=50, batch_size=1000)
for batch in data_loader:
    ipca.partial_fit(batch)
X_reduced = ipca.transform(X)
```

## t-SNE {#t-sne}

Nichtlinear. Erhält die lokale Struktur. Am besten zur Visualisierung geeignet, nicht zur Vorverarbeitung.

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

**Perplexity**: steuert die effektive Anzahl der Nachbarn. Niedrig (5-10) = enge Cluster, hoch (30-50) = globale Struktur. Mehrere Werte ausprobieren.

## UMAP {#umap}

Schneller als t-SNE, erhält mehr globale Struktur und kann zur Vorverarbeitung verwendet werden (anders als t-SNE).

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

**n_neighbors**: niedrig (5-15) = lokale Struktur, hoch (50-200) = globale Struktur. min_dist: niedrig = engere Cluster, hoch = stärker verteilt.

## Merkmalsauswahl {#feature-selection}

### Filtermethoden {#filter-methods}

Merkmale unabhängig voneinander bewerten und die besten k auswählen:

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

### Wrapper-Methoden {#wrapper-methods}

Die Modellleistung dient zur Bewertung von Merkmalsteilmengen:

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

### Eingebettete Methoden {#embedded-methods}

Merkmalswichtigkeit aus dem Modell selbst:

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

## Autoencoder zur Dimensionalitätsreduktion {#autoencoders-for-dimensionality-reduction}

Nichtlineare Alternative zur PCA:

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

## Fallstricke {#gotchas}

- **Cluster-Größen und -Abstände in t-SNE sind bedeutungslos**: t-SNE verzerrt Abstände, um lokale Nachbarschaften zu erhalten. Ein großer Cluster im t-SNE-Diagramm muss im Originalraum nicht größer sein. Abstände zwischen Clustern oder Cluster-Größen niemals interpretieren. t-SNE nur verwenden, um die Existenz von Clustern zu bestätigen, nicht um sie zu messen
- **PCA auf unskalierten Daten = dominiert von Merkmalen mit hoher Varianz**: Wenn ein Merkmal Werte von 0 bis 1000 und ein anderes von 0 bis 1 annimmt, wählt PCA unabhängig von der Bedeutung das Merkmal mit hoher Varianz. Vor PCA immer StandardScaler anwenden. Ausnahme: Wenn alle Merkmale in denselben Einheiten vorliegen (z. B. alle Pixelwerte 0-255)
- **Merkmalsauswahl muss innerhalb der Kreuzvalidierung erfolgen**: Wird die Auswahl auf dem gesamten Datensatz durchgeführt und danach die Kreuzvalidierung, fließen Informationen aus dem Validierungsfold ein. Mit einer Pipeline sicherstellen, dass die Auswahl in jedem Fold nur auf den Trainingsdaten erfolgt

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('selector', SelectKBest(f_classif, k=20)),
    ('model', RandomForestClassifier())
])
scores = cross_val_score(pipe, X, y, cv=5)  # correct: no leakage
```

## Siehe auch {#see-also}

- [[feature-engineering]]
- [[unsupervised-learning]]
- [[neural-networks]]
- [[knn-and-classical-ml]]
