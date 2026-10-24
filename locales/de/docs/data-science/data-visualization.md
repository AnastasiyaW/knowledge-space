---
title: "Datenvisualisierung"
category: tools
tags: [data-science, visualization, matplotlib, seaborn, plotly]
level: 3
source_sha256: 4287f605b8f48889e29334915b348158361f36c2896424f72369d14f2aa6cc01
translation: machine
translated_at: '2026-10-24'
---
# Datenvisualisierung {#data-visualization}

Visualisierung ist sowohl ein Analysewerkzeug (EDA) als auch ein Kommunikationswerkzeug (Dashboards, Berichte). Python bietet matplotlib als Grundlage, seaborn für statistische Diagramme und plotly für Interaktivität.

## Matplotlib {#matplotlib}

Grundlegende Plotting-Bibliothek. Alles andere baut darauf auf.

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

**Dunkles Design**: `plt.style.use('dark_background')`

### Diagrammtypen {#plot-types}

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

High-Level-Schnittstelle. Bessere Standardeinstellungen, statistische Diagramme, automatische Legenden.

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

## Plotly (interaktiv) {#plotly-interactive}

```python
import plotly.express as px

fig = px.scatter(df, x='feat1', y='feat2', color='target',
                 hover_data=['name'], title='Interactive Scatter')
fig.show()

fig = px.histogram(df, x='column', nbins=30, color='category')
fig.show()
```

## Die richtige Diagrammart wählen {#choosing-the-right-chart}

| Datentyp | Diagrammtyp |
|-----------|-----------|
| Eine kontinuierliche Variable | Histogramm, KDE, Boxplot |
| Zwei kontinuierliche Variablen | Streudiagramm, Regressionsdiagramm |
| Kategorisch vs. kontinuierlich | Boxplot, Violinplot, Balkendiagramm |
| Kategorisch vs. kategorisch | Gestapeltes Balkendiagramm, Heatmap |
| Zeitreihen | Liniendiagramm |
| Korrelationsmatrix | Heatmap |
| Hochdimensionale Übersicht | Pairplot, t-SNE/PCA-Streudiagramm |

## EDA-Visualisierungsworkflow {#eda-visualization-workflow}

1. **Fehlende Werte**: Heatmap der Nullwerte, Balkendiagramm der Anteile fehlender Werte
2. **Zielverteilung**: Histogramm/Countplot
3. **Merkmalsverteilungen**: Histogramme (numerisch), Countplots (kategorisch)
4. **Korrelationen**: Heatmap der Korrelationsmatrix
5. **Merkmal vs. Ziel**: gruppierte Balkendiagramme, Boxplots nach Zielklasse
6. **Ausreißer**: Boxplots, Streudiagramme mit z-Score-Färbung
7. **Paarbeziehungen**: Pairplot für die wichtigsten Merkmale

## Gestaltungsprinzipien {#design-principles}

- **Titel und Achsenbeschriftungen**: immer mit passenden Schriftgrößen angeben
- **Legende**: bei mehreren Datenreihen angeben
- **Farbe**: sequenziell für kontinuierliche Daten, qualitativ für Kategorien; farbenblindheitsfreundliche Paletten erwägen
- **Gitternetzlinien**: dezent, damit Werte gut abgelesen werden können
- **Seitenverhältnis**: so wählen, dass keine Verzerrung entsteht

## Stolperfallen {#gotchas}
- Kreisdiagramme mit mehr als 5 Kategorien sind kaum lesbar - stattdessen Balkendiagramme verwenden
- 3D-Diagramme erzeugen Verwirrung statt Klarheit - bei 2D bleiben
- Rot-Grün-Farbschemata sind für etwa 8 % der Männer (Farbenblindheit) problematisch
- Fehlende Achsenbeschriftungen oder Titel machen Diagramme für die Kommunikation unbrauchbar
- Zu viele Datenreihen in einem Diagramm = visuelles Rauschen

## Siehe auch {#see-also}
- [[pandas-eda]] - Datenaufbereitung vor der Visualisierung
- [[descriptive-statistics]] - was visualisiert werden sollte
- [[bi-dashboards]] - Business-Intelligence-Werkzeuge zur Visualisierung
