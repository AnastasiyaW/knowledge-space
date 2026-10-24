---
title: "Grundlagen der Datenanalyse (Pandas und Matplotlib)"
category: concepts
tags: [python, pandas, matplotlib, seaborn, dataframe, visualization, data-science]
level: 2
source_sha256: dff48c246080eb6f7a845acc87ded101fd9978f63fc81b9f00c90c0539d4bbe4
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen der Datenanalyse (Pandas und Matplotlib) {#data-analysis-basics-pandas-and-matplotlib}

Pandas stellt tabellarische Datenstrukturen (DataFrame, Series) für Datenmanipulation und -analyse bereit. Matplotlib und Seaborn übernehmen die Visualisierung. Zusammen mit NumPy bilden sie das Fundament des Data-Science-Ökosystems von Python.

## Wichtige Fakten {#key-facts}

- DataFrame ist eine zweidimensionale, beschriftete Tabelle (vergleichbar mit einer Tabellenkalkulation); Series ist ein eindimensionales, beschriftetes Array (Spalte)
- Pandas eignet sich für Daten, die in den Arbeitsspeicher passen; für verteilte Daten im großen Maßstab PySpark
- `pd.concat()` zum Aneinanderreihen von DataFrames; `pd.merge()` für Joins im SQL-Stil
- Matplotlib bietet zwei APIs: pyplot (im Stil von MATLAB) und OOP (fig, ax – mehr Kontrolle)
- Seaborn baut auf Matplotlib auf, bietet bessere Standardeinstellungen und statistische Diagramme
- Millers Regel: Diagramme mit mehr als 8 Kategorien werden unleserlich – stattdessen eine Tabelle verwenden

## Muster {#patterns}

### Pandas-Kernoperationen {#pandas-core-operations}
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

### Concat und Merge {#concat-and-merge}
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

### Gängige Diagrammtypen {#common-plot-types}
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

### NumPy-Grundlagen {#numpy-basics}
```python
import numpy as np

arr = np.array([1, 2, 3])
zeros = np.zeros((3, 4))        # 3x4 matrix of zeros
rand = np.random.random((2, 3)) # 2x3 random matrix
np.random.seed(42)              # reproducibility
```

## Best Practices für Visualisierung {#visualization-best-practices}

- **Trends über die Zeit** -> Liniendiagramm
- **Vergleiche** -> Balkendiagramm
- **Verteilungen** -> Histogramm oder Box-Plot
- **Zusammenhänge** -> Streudiagramm
- **Anteile** -> Kreisdiagramm (sparsam verwenden)
- **3D auf 2D** -> Konturdiagramm oder Heatmap
- Maximal etwa 8 Kategorien pro Diagramm; darüber hinaus eine Tabelle verwenden

## Fallstricke {#gotchas}

- Pandas `concat` mit wiederholtem `append` hat quadratische Komplexität – alle DataFrames sammeln und dann einmal mit `concat` zusammenführen
- `pd.merge()` erkennt die Join-Spalte automatisch anhand gemeinsamer Namen; `on=` explizit angeben
- Die zustandsbasierte pyplot-API von Matplotlib ist bequem, bei komplexen Abbildungen aber schwer zu verwalten – OOP-Stil bevorzugen
- Bei großen Datensätzen ist Matplotlib langsam – `datashader` oder Plotly/Bokeh mit WebGL verwenden

## Siehe auch {#see-also}

- [[data-structures]] - Eingebaute Python-Sammlungen
- [[file-io]] - Lesen von CSV- und JSON-Datendateien
- [[data-science/index]] - Fortgeschrittene Themen der Data Science
