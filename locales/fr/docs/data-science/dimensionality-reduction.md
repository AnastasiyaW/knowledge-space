---
title: "Réduction de dimensionnalité"
category: concepts
tags: [data-science, pca, t-sne, umap, feature-selection, manifold-learning]
level: 3
source_sha256: 412a39bdbad3c8c5e643c175eb03333b39b002fa2602ad8c728fa815e8c34ebd
translation: machine
translated_at: '2026-10-24'
---
# Réduction de dimensionnalité {#dimensionality-reduction}

Réduire le nombre de variables tout en préservant l'information importante. Deux objectifs : la visualisation (projection en 2D/3D) et le prétraitement (supprimer le bruit, accélérer l'entraînement, lutter contre le fléau de la dimension). Deux approches : la sélection de variables (choisir un sous-ensemble) et l'extraction de variables (créer de nouvelles variables).

## PCA (Analyse en composantes principales) {#pca-principal-component-analysis}

Projection linéaire sur les directions de variance maximale.

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

**Quand l'utiliser** : prétraitement avant un apprentissage automatique, débruitage, suppression de la multicolinéarité, visualisation si les données sont à peu près linéaires.

### PCA incrémentale (pour les grands jeux de données) {#incremental-pca-for-large-datasets}

```python
from sklearn.decomposition import IncrementalPCA

ipca = IncrementalPCA(n_components=50, batch_size=1000)
for batch in data_loader:
    ipca.partial_fit(batch)
X_reduced = ipca.transform(X)
```

## t-SNE {#t-sne}

Non linéaire. Préserve la structure locale. Idéal pour la visualisation, pas pour le prétraitement.

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

**Perplexité** : contrôle le nombre effectif de voisins. Faible (5-10) = clusters serrés, élevée (30-50) = structure globale. Essayer plusieurs valeurs.

## UMAP {#umap}

Plus rapide que t-SNE, préserve mieux la structure globale, peut être utilisé pour le prétraitement (contrairement à t-SNE).

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

**n_neighbors** : faible (5-15) = structure locale, élevée (50-200) = structure globale. min_dist : faible = clusters plus serrés, élevée = points plus dispersés.

## Sélection de variables {#feature-selection}

### Méthodes de filtrage {#filter-methods}

Évaluer chaque variable indépendamment, sélectionner les k meilleures :

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

### Méthodes enveloppantes (wrapper) {#wrapper-methods}

Utiliser les performances du modèle pour évaluer des sous-ensembles de variables :

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

### Méthodes intégrées (embedded) {#embedded-methods}

Importance des variables fournie par le modèle lui-même :

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

## Autoencodeurs pour la réduction de dimensionnalité {#autoencoders-for-dimensionality-reduction}

Alternative non linéaire à la PCA :

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

## Pièges à éviter {#gotchas}

- **Les tailles et distances entre clusters dans un t-SNE n'ont pas de sens** : t-SNE déforme les distances pour préserver les voisinages locaux. Un grand cluster sur un graphique t-SNE ne sera pas forcément plus grand dans l'espace d'origine. Ne jamais interpréter les distances inter-clusters ni la taille des clusters. Utiliser t-SNE uniquement pour confirmer l'existence de clusters, pas pour les mesurer
- **PCA sur des données non standardisées = dominée par les variables à forte variance** : si une variable varie de 0 à 1000 et une autre de 0 à 1, la PCA retiendra la première quelle que soit son importance. Toujours appliquer StandardScaler avant la PCA. Exception : si les variables sont exprimées dans la même unité (par exemple, toutes des valeurs de pixels de 0 à 255)
- **La sélection de variables doit être effectuée à l'intérieur de la validation croisée** : sélectionner les variables sur l'ensemble complet puis faire la validation croisée introduit une fuite d'information depuis le pli de validation. Utiliser un Pipeline pour garantir que la sélection ne s'effectue que sur les données d'entraînement de chaque pli

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('selector', SelectKBest(f_classif, k=20)),
    ('model', RandomForestClassifier())
])
scores = cross_val_score(pipe, X, y, cv=5)  # correct: no leakage
```

## Voir aussi {#see-also}

- [[feature-engineering]]
- [[unsupervised-learning]]
- [[neural-networks]]
- [[knn-and-classical-ml]]
