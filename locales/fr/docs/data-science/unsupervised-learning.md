---
title: "Apprentissage non supervisé"
category: models
tags: [data-science, ml, clustering, dimensionality-reduction, pca, kmeans]
level: 3
source_sha256: 442eb80e63a7cd26036f2227e388db548815963636ca1213e8f5c70fc1d98d05
translation: machine
translated_at: '2026-10-24'
---
# Apprentissage non supervisé {#unsupervised-learning}

Apprentissage à partir de données non étiquetées. Deux tâches principales : le clustering (regrouper des éléments similaires) et la réduction de dimensionnalité (compresser les caractéristiques). Essentiel pour l'analyse exploratoire, la segmentation et le prétraitement.

## Clustering {#clustering}

### K-Means {#k-means}
Partitionne les données en k clusters en minimisant les distances intra-cluster.

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)
centroids = kmeans.cluster_centers_
```

**Algorithme** : 1) Centroïdes initiaux aléatoires → 2) Affecter chaque point au centroïde le plus proche → 3) Mettre à jour les centroïdes en tant que moyennes des clusters → 4) Répéter jusqu'à convergence.

**Choix de k** : méthode du coude (tracer l'inertie en fonction de k et choisir le « coude »), score de silhouette.

**Limites** : suppose des clusters sphériques de taille similaire, sensible à l'initialisation, nécessite de spécifier k à l'avance.

### DBSCAN (basé sur la densité) {#dbscan-density-based}

Regroupe les points situés dans des régions denses. Détecte des clusters de forme arbitraire. Identifie le bruit.

```python
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=1.0, min_samples=20)
labels = db.fit_predict(X)
# label = -1 means noise point
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
```

- **eps** : rayon du voisinage
- **min_samples** : nombre minimal de points pour un point cœur
- Types de points : cœur (voisinage dense), frontière (dans le voisinage d'un point cœur), bruit (-1)
- Pas besoin de spécifier le nombre de clusters
- Peine à gérer les densités variables

### Clustering hiérarchique {#hierarchical-clustering}

Construit un arbre de clusters par fusion (agglomératif) ou par division (divisif).

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

hc = AgglomerativeClustering(n_clusters=5, linkage='ward')
labels = hc.fit_predict(X)

# Dendrogram to choose k
Z = linkage(X, method='ward')
dendrogram(Z)
```

**Méthodes de liaison** : single (distance minimale), complete (distance maximale), average, ward (minimisation de la variance).

### Métriques de clustering {#clustering-metrics}

| Métrique | Plage | Usage |
|----------|-------|-------|
| Silhouette | [-1, 1] | Plus élevé = clusters mieux séparés |
| Inertie | [0, inf) | Plus faible = clusters plus compacts (dans k-means) |
| Calinski-Harabasz | [0, inf) | Plus élevé = clusters mieux définis |
| Adjusted Rand Index | [-1, 1] | Comparaison à la vérité terrain si disponible |

```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, labels)
```

## Réduction de dimensionnalité {#dimensionality-reduction}

### PCA (Analyse en composantes principales) {#pca-principal-component-analysis}

Trouve les directions de variance maximale. Projette les données sur les k premières composantes.

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

**Mathématiques** : les vecteurs propres de la matrice de covariance sont les composantes principales. Les valeurs propres correspondent à la variance expliquée par chaque composante.

**Cas d'usage** : visualisation (projection 2D), réduction du bruit, prétraitement pour les modèles, compression des caractéristiques.

### t-SNE {#t-sne}

Réduction de dimensionnalité non linéaire, destinée **uniquement à la visualisation**.

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_2d = tsne.fit_transform(X)
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, alpha=0.5)
```

**Piège** : t-SNE est stochastique, non déterministe sans graine fixée, et les distances entre clusters ne sont PAS significatives. À utiliser uniquement pour la visualisation, jamais comme caractéristiques pour des modèles en aval.

### UMAP {#umap}

Plus rapide que t-SNE, préserve mieux la structure globale.

```python
import umap
reducer = umap.UMAP(n_components=2, random_state=42)
X_2d = reducer.fit_transform(X)
```

### SVD (décomposition en valeurs singulières) {#svd-singular-value-decomposition}

Toute matrice A = U * Sigma * V^T. La SVD tronquée conserve les k plus grandes valeurs singulières.

```python
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=50)
X_reduced = svd.fit_transform(X_sparse)  # works with sparse matrices (TF-IDF)
```

**Applications** : approximation matricielle, systèmes de recommandation, texte (analyse sémantique latente).

## Applications {#applications}

- **Segmentation de clientèle** : K-Means/DBSCAN sur des caractéristiques comportementales
- **Détection d'anomalies** : points éloignés de tout centre de cluster
- **Modélisation de thèmes** : clustering de documents dans un espace TF-IDF ou d'embeddings
- **Compression des caractéristiques** : PCA avant l'entraînement pour accélérer les modèles
- **Visualisation** : t-SNE/UMAP pour comprendre des données de grande dimension

## Pièges courants {#gotchas}
- K-Means nécessite une mise à l'échelle des caractéristiques (il utilise la distance euclidienne)
- PCA nécessite des caractéristiques standardisées (sinon elle est dominée par les caractéristiques à forte variance)
- t-SNE avec des valeurs de perplexité différentes peut produire des graphiques très différents : toujours en essayer plusieurs
- Le clustering est subjectif : il n'existe pas de nombre « correct » de clusters
- Le paramètre eps de DBSCAN dépend de l'échelle : normaliser les caractéristiques au préalable

## Voir aussi {#see-also}
- [[feature-engineering]] - PCA comme étape de prétraitement
- [[neural-networks]] - autoencodeurs pour la réduction de dimensionnalité non linéaire
- [[math-linear-algebra]] - théorie des valeurs propres et de la SVD
- [[model-evaluation]] - métriques d'évaluation du clustering
