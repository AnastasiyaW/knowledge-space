---
title: "Bases de l'analyse de données (Pandas et Matplotlib)"
category: concepts
tags: [python, pandas, matplotlib, seaborn, dataframe, visualization, data-science]
level: 2
source_sha256: dff48c246080eb6f7a845acc87ded101fd9978f63fc81b9f00c90c0539d4bbe4
translation: machine
translated_at: '2026-10-24'
---
# Bases de l'analyse de données (Pandas et Matplotlib) {#data-analysis-basics-pandas-and-matplotlib}

Pandas fournit des structures de données tabulaires (DataFrame, Series) pour la manipulation et l'analyse de données. Matplotlib et Seaborn assurent la visualisation. Avec NumPy, ils constituent le socle de l'écosystème data science de Python.

## Points clés {#key-facts}

- DataFrame est un tableau 2D étiqueté (comparable à une feuille de calcul) ; Series est un tableau 1D étiqueté (une colonne)
- Pandas convient aux données qui tiennent en mémoire ; PySpark est adapté aux volumes de données importants et distribués
- `pd.concat()` pour empiler des DataFrames ; `pd.merge()` pour les jointures de type SQL
- Matplotlib propose deux APIs : pyplot (style MATLAB) et orientée objet (fig, ax, plus de contrôle)
- Seaborn enveloppe Matplotlib avec de meilleures valeurs par défaut et des graphiques statistiques
- Règle de Miller : au-delà de 8 catégories, un graphique devient illisible ; utiliser un tableau à la place

## Motifs {#patterns}

### Opérations de base avec Pandas {#pandas-core-operations}
```python
import pandas as pd

# Create
df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]})

# Select
df['name']               # column -> Series
df[['name', 'age']]      # multiple columns -> DataFrame
df.loc[0]                # row by label
df.iloc[0]               # row by position
df[df['age'] > 25]       # boolean filter

# Aggregate
df.groupby('dept').mean()
df.describe()            # summary statistics

# Clean
df.fillna(0)             # replace NaN
df.dropna()              # remove NaN rows
df.drop_duplicates()     # remove duplicate rows
df.astype({'age': int})  # type conversion
```

### Concat et Merge {#concat-and-merge}
```python
# Vertical stack
pd.concat([df1, df2])
pd.concat([df1, df2], join='inner')  # common columns only

# SQL-style join
pd.merge(employees, departments, on='dept_id')
pd.merge(left, right, left_on='id', right_on='emp_id', how='left')
```

### Matplotlib {#matplotlib}
```python
import matplotlib.pyplot as plt
import numpy as np

# OOP style (recommended)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, label='data')
ax.set_title('Title')
ax.set_xlabel('X')
ax.legend()
plt.savefig('plot.png', dpi=150, bbox_inches='tight')

# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y)
axes[0, 1].scatter(x, y)
axes[1, 0].bar(categories, values)
axes[1, 1].hist(data, bins=30)
```

### Types de graphiques courants {#common-plot-types}
```python
plt.plot(x, y)                    # line
plt.scatter(x, y, c=colors)      # scatter
plt.bar(categories, values)       # bar
plt.hist(data, bins=30)           # histogram
plt.contourf(X, Y, Z, cmap='RdGy')  # contour
```

### Seaborn {#seaborn}
```python
import seaborn as sns

sns.pairplot(df)                          # all variables against each other
sns.heatmap(df.corr(), annot=True)        # correlation matrix
sns.boxplot(x='category', y='value', data=df)
```

### Bases de NumPy {#numpy-basics}
```python
import numpy as np

arr = np.array([1, 2, 3])
zeros = np.zeros((3, 4))        # 3x4 matrix of zeros
rand = np.random.random((2, 3)) # 2x3 random matrix
np.random.seed(42)              # reproducibility
```

## Bonnes pratiques de visualisation {#visualization-best-practices}

- **Tendances dans le temps** -> graphique en courbes
- **Comparaisons** -> diagramme en barres
- **Distributions** -> histogramme ou boîte à moustaches
- **Relations** -> nuage de points
- **Proportions** -> diagramme circulaire (à utiliser avec parcimonie)
- **3D sur 2D** -> carte de contours ou heatmap
- Maximum ~8 catégories par graphique ; au-delà, utiliser un tableau

## Pièges {#gotchas}

- Un `concat` de Pandas combiné à des `append` répétés a une complexité quadratique : collecter tous les DataFrames, puis effectuer un seul `concat`
- `pd.merge()` détecte automatiquement la colonne de jointure à partir des noms communs ; spécifier `on=` pour être explicite
- L'API pyplot à états de Matplotlib est pratique mais difficile à gérer pour les figures complexes ; privilégier le style orienté objet
- Pour les grands jeux de données, Matplotlib est lent : utiliser `datashader` ou Plotly/Bokeh avec WebGL

## Voir aussi {#see-also}

- [[data-structures]] - Collections intégrées de Python
- [[file-io]] - Lecture de fichiers de données CSV et JSON
- [[data-science/index]] - Sujets avancés de data science
