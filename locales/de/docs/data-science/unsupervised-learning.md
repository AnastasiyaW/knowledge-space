---
title: "Unüberwachtes Lernen"
category: models
tags: [data-science, ml, clustering, dimensionality-reduction, pca, kmeans]
level: 3
source_sha256: 442eb80e63a7cd26036f2227e388db548815963636ca1213e8f5c70fc1d98d05
translation: machine
translated_at: '2026-10-24'
---
# Unüberwachtes Lernen {#unsupervised-learning}

Lernen aus unmarkierten Daten. Zwei Hauptaufgaben: Clustering (ähnliche Elemente gruppieren) und Dimensionsreduktion (Merkmale komprimieren). Unverzichtbar für explorative Analysen, Segmentierung und Preprocessing.

## Clustering {#clustering}

### K-Means {#k-means}
Daten in k Cluster partitionieren, indem die Abstände innerhalb der Cluster minimiert werden.

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)
centroids = kmeans.cluster_centers_
```

**Algorithmus**: 1) Zufällige initiale Centroids -> 2) Punkte dem nächstgelegenen Centroid zuweisen -> 3) Centroids als Mittelwerte der Cluster aktualisieren -> 4) Wiederholen bis zur Konvergenz.

**Wahl von k**: Ellbogenmethode (Inertia gegen k auftragen, den „Ellbogen“ wählen), Silhouette-Score.

**Einschränkungen**: Setzt kugelförmige Cluster ähnlicher Größe voraus, ist empfindlich gegenüber der Initialisierung und erfordert die vorherige Angabe von k.

### DBSCAN (Dichtebasiert) {#dbscan-density-based}

Gruppiert Punkte in dichten Regionen. Findet Cluster beliebiger Form. Erkennt Rauschen.

```python
from sklearn.cluster import DBSCAN

db = DBSCAN(eps=1.0, min_samples=20)
labels = db.fit_predict(X)
# label = -1 means noise point
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
```

- **eps**: Radius der Nachbarschaft
- **min_samples**: Mindestanzahl an Punkten für einen Kernpunkt
- Punkttypen: Kernpunkt (dichte Nachbarschaft), Randpunkt (in der Nachbarschaft eines Kernpunkts), Rauschen (-1)
- Keine Angabe der Clusteranzahl nötig
- Probleme bei unterschiedlicher Dichte

### Hierarchisches Clustering {#hierarchical-clustering}

Baum aus Clustern aufbauen, durch Zusammenführen (agglomerativ) oder Aufteilen (divisiv).

```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

hc = AgglomerativeClustering(n_clusters=5, linkage='ward')
labels = hc.fit_predict(X)

# Dendrogram to choose k
Z = linkage(X, method='ward')
dendrogram(Z)
```

**Linkage-Methoden**: single (minimaler Abstand), complete (maximaler Abstand), average, ward (Minimierung der Varianz).

### Clustering-Metriken {#clustering-metrics}

| Metrik | Bereich | Verwendung |
|--------|---------|------------|
| Silhouette | [-1, 1] | Höher = besser getrennte Cluster |
| Inertia | [0, inf) | Niedriger = kompaktere Cluster (bei K-Means) |
| Calinski-Harabasz | [0, inf) | Höher = besser definierte Cluster |
| Adjusted Rand Index | [-1, 1] | Vergleich mit Ground Truth, sofern verfügbar |

```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, labels)
```

## Dimensionsreduktion {#dimensionality-reduction}

### PCA (Hauptkomponentenanalyse) {#pca-principal-component-analysis}

Richtungen maximaler Varianz finden. Daten auf die obersten k Komponenten projizieren.

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

**Mathematik**: Eigenvektoren der Kovarianzmatrix = Hauptkomponenten. Eigenwerte = erklärte Varianz je Komponente.

**Anwendungsfälle**: Visualisierung (2D-Projektion), Rauschreduktion, Preprocessing für Modelle, Merkmalskompression.

### t-SNE {#t-sne}

Nichtlineare Dimensionsreduktion, ausschließlich zur **Visualisierung**.

```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_2d = tsne.fit_transform(X)
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, alpha=0.5)
```

**Stolperfalle**: t-SNE ist stochastisch und ohne Seed nicht deterministisch; die Abstände zwischen Clustern sind NICHT aussagekräftig. Nur zur Visualisierung verwenden, niemals als Features für nachgelagerte Modelle.

### UMAP {#umap}

Schneller als t-SNE, erhält mehr globale Struktur.

```python
import umap
reducer = umap.UMAP(n_components=2, random_state=42)
X_2d = reducer.fit_transform(X)
```

### SVD (Singulärwertzerlegung) {#svd-singular-value-decomposition}

Jede Matrix A = U * Sigma * V^T. Truncated SVD behält die obersten k Singulärwerte.

```python
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=50)
X_reduced = svd.fit_transform(X_sparse)  # works with sparse matrices (TF-IDF)
```

**Anwendungen**: Matrixapproximation, Empfehlungssysteme, Text (Latent Semantic Analysis).

## Anwendungen {#applications}

- **Kundensegmentierung**: K-Means/DBSCAN auf Verhaltensmerkmalen
- **Anomalieerkennung**: Punkte, die weit von allen Clusterzentren entfernt liegen
- **Topic Modeling**: Clustering von Dokumenten im TF-IDF- oder Embedding-Raum
- **Merkmalskompression**: PCA vor dem Training, um Modelle zu beschleunigen
- **Visualisierung**: t-SNE/UMAP zum Verständnis hochdimensionaler Daten

## Stolperfallen {#gotchas}
- K-Means erfordert Feature-Skalierung (verwendet den euklidischen Abstand)
- PCA erfordert standardisierte Merkmale (andernfalls dominieren Merkmale mit hoher Varianz)
- t-SNE mit unterschiedlichen Perplexity-Werten kann sehr unterschiedliche Darstellungen erzeugen – immer mehrere ausprobieren
- Clustering ist subjektiv – es gibt keine „richtige“ Anzahl von Clustern
- Der eps-Wert von DBSCAN ist skalenabhängig – Features zuerst normalisieren

## Siehe auch {#see-also}
- [[feature-engineering]] - PCA als Preprocessing-Schritt
- [[neural-networks]] - Autoencoder für nichtlineare Dimensionsreduktion
- [[math-linear-algebra]] - Eigenwerte und Theorie der SVD
- [[model-evaluation]] - Metriken zur Bewertung von Clustering
