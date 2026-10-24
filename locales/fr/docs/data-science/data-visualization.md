---
title: "Visualisation de données"
category: tools
tags: [data-science, visualization, matplotlib, seaborn, plotly]
level: 3
source_sha256: 4287f605b8f48889e29334915b348158361f36c2896424f72369d14f2aa6cc01
translation: machine
translated_at: '2026-10-24'
---
# Visualisation de données {#data-visualization}

La visualisation est à la fois un outil d'analyse (EDA) et un outil de communication (tableaux de bord, rapports). Python propose matplotlib comme base, seaborn pour les graphiques statistiques et plotly pour l'interactivité.

## Matplotlib {#matplotlib}

Bibliothèque de tracé de base. Tout le reste s'appuie sur elle.

```python
import matplotlib.pyplot as plt

# Basic line plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='line1', color='blue', linewidth=2)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('My Plot')
plt.legend()
plt.grid(True)
plt.show()

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y)
axes[0, 0].set_title('Plot 1')
axes[0, 1].scatter(x, y)
plt.tight_layout()
plt.show()
```

**Thème sombre** : `plt.style.use('dark_background')`

### Types de graphiques {#plot-types}

```python
# Histogram - distribution of continuous variable
df['column'].hist(bins=30)

# Bar plot - counts/values per category
df['category'].value_counts().plot(kind='bar')

# Scatter - relationship between two continuous
plt.scatter(df['x'], df['y'], c=df['label'], alpha=0.5)

# Box plot - distribution with quartiles and outliers
df.boxplot(column='value', by='category')
```

## Seaborn {#seaborn}

Interface de haut niveau. Meilleures valeurs par défaut, graphiques statistiques, légendes automatiques.

```python
import seaborn as sns

# Correlation heatmap
sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm')

# Distribution
sns.histplot(df['col'], kde=True)     # histogram + density curve
sns.kdeplot(df['col'])                 # density only

# Categorical
sns.boxplot(x='category', y='value', data=df)
sns.violinplot(x='category', y='value', data=df)
sns.countplot(x='category', data=df)
sns.barplot(x='category', y='value', data=df)  # mean + CI

# Regression
sns.regplot(x='feat1', y='feat2', data=df)

# Pair plot - all pairwise relationships
sns.pairplot(df, hue='target')

# FacetGrid - multiple plots split by category
g = sns.FacetGrid(df, col='category', col_wrap=3)
g.map(plt.hist, 'value')
```

## Plotly (interactif) {#plotly-interactive}

```python
import plotly.express as px

fig = px.scatter(df, x='feat1', y='feat2', color='target',
                 hover_data=['name'], title='Interactive Scatter')
fig.show()

fig = px.histogram(df, x='column', nbins=30, color='category')
fig.show()
```

## Choisir le bon graphique {#choosing-the-right-chart}

| Type de données | Type de graphique |
|-----------|-----------|
| Une variable continue | Histogramme, KDE, boîte à moustaches |
| Deux variables continues | Nuage de points, graphique de régression |
| Catégorielle vs continue | Boîte à moustaches, diagramme en violon, diagramme en barres |
| Catégorielle vs catégorielle | Barres empilées, heatmap |
| Série temporelle | Courbe |
| Matrice de corrélation | Heatmap |
| Vue d'ensemble en grande dimension | Pair plot, nuage de points t-SNE/PCA |

## Workflow de visualisation EDA {#eda-visualization-workflow}

1. **Valeurs manquantes** : heatmap des valeurs nulles, diagramme en barres des pourcentages de nulls
2. **Distribution de la cible** : histogramme/countplot
3. **Distributions des variables** : histogrammes (numériques), countplots (catégorielles)
4. **Corrélations** : heatmap de la matrice de corrélation
5. **Variable vs cible** : diagrammes en barres groupés, boîtes à moustaches par classe cible
6. **Valeurs aberrantes** : boîtes à moustaches, nuages de points colorés par z-score
7. **Relations entre paires** : pairplot pour les variables les plus importantes

## Principes de conception {#design-principles}

- **Titre et étiquettes d'axes** : toujours les inclure, avec des tailles de police adaptées
- **Légende** : à inclure lorsqu'il y a plusieurs séries
- **Couleur** : séquentielle pour le continu, qualitative pour les catégories ; privilégier des palettes adaptées au daltonisme
- **Lignes de grille** : discrètes, pour faciliter la lecture des valeurs
- **Rapport d'aspect** : à choisir pour éviter les déformations

## Pièges à éviter {#gotchas}
- Les diagrammes circulaires avec plus de 5 catégories sont illisibles - utiliser plutôt des diagrammes en barres
- Les graphiques 3D ajoutent de la confusion sans gain de clarté - s'en tenir à la 2D
- Les schémas rouge-vert sont problématiques pour environ 8 % des hommes (daltonisme)
- L'absence d'étiquettes d'axes ou de titre rend les graphiques inutilisables pour la communication
- Trop de séries sur un même graphique = bruit visuel

## Voir aussi {#see-also}
- [[pandas-eda]] - manipulation des données avant visualisation
- [[descriptive-statistics]] - ce qu'il faut visualiser
- [[bi-dashboards]] - outils de visualisation de business intelligence
