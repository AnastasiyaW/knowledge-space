---
title: Data Visualization
category: tools
tags: [data-science, visualization, matplotlib, seaborn, plotly]
---

# Data Visualization

Visualization is both an analysis tool (EDA) and a communication tool (dashboards, reports). Python offers matplotlib for foundations, seaborn for statistical plots, and plotly for interactivity.

## Matplotlib

Foundation plotting library. Everything else builds on top.

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

**Dark theme**: `plt.style.use('dark_background')`

### Plot Types

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

## Seaborn

High-level interface. Better defaults, statistical plots, automatic legends.

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

## Plotly (Interactive)

```python
import plotly.express as px

fig = px.scatter(df, x='feat1', y='feat2', color='target',
                 hover_data=['name'], title='Interactive Scatter')
fig.show()

fig = px.histogram(df, x='column', nbins=30, color='category')
fig.show()
```

## Choosing the Right Chart

| Data Type | Chart Type |
|-----------|-----------|
| One continuous variable | Histogram, KDE, box plot |
| Two continuous variables | Scatter plot, regression plot |
| Categorical vs continuous | Box plot, violin plot, bar plot |
| Categorical vs categorical | Stacked bar, heatmap |
| Time series | Line plot |
| Correlation matrix | Heatmap |
| High-dimensional overview | Pair plot, t-SNE/PCA scatter |

## EDA Visualization Workflow

1. **Missing values**: heatmap of nulls, bar chart of null percentages
2. **Target distribution**: histogram/countplot
3. **Feature distributions**: histograms (numeric), countplots (categorical)
4. **Correlations**: heatmap of correlation matrix
5. **Feature vs target**: groupby bar plots, box plots by target class
6. **Outliers**: box plots, scatter plots with z-score coloring
7. **Pair relationships**: pairplot for top features

## Design Principles

- **Title and axis labels**: always include with appropriate font sizes
- **Legend**: include when multiple series
- **Color**: sequential for continuous, qualitative for categories; consider colorblind-safe palettes
- **Grid lines**: subtle, help read values
- **Aspect ratio**: choose to avoid distortion

## Gotchas
- Pie charts with > 5 categories are unreadable - use bar charts instead
- 3D plots add confusion without clarity - stick to 2D
- Red-green color schemes fail for ~8% of males (colorblind)
- Missing axis labels or title makes plots useless for communication
- Too many series on one plot = visual noise

## See Also
- [[pandas-eda]] - data manipulation before visualization
- [[descriptive-statistics]] - what to visualize
- [[bi-dashboards]] - business intelligence visualization tools
