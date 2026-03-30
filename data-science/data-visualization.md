---
title: Data Visualization
category: tools
tags: [visualization, matplotlib, seaborn, plotly, eda, charts, python]
---

# Data Visualization

Communicate patterns, distributions, and relationships through charts. Essential for EDA (exploratory data analysis), model diagnostics, and presenting results. Matplotlib is the foundation; Seaborn adds statistical plots; Plotly provides interactivity. Always visualize data before modeling -- see [[descriptive-statistics]].

## Key Facts

- **Matplotlib**: low-level, highly customizable; `plt.figure()` + `plt.plot()` + `plt.show()` pattern; two APIs: pyplot (procedural) and OOP (fig, ax)
- **Seaborn**: built on matplotlib; statistical plots with less code; works directly with [[pandas-data-manipulation]] DataFrames
- **Plotly**: interactive charts; hover tooltips, zoom, pan; `plotly.express` for quick plots
- **Distribution plots**: histogram, KDE (kernel density estimate), box plot, violin plot
- **Relationship plots**: scatter plot, line plot, heatmap (correlation matrix), pair plot
- **Comparison plots**: bar chart, grouped bar, stacked bar
- **Composition plots**: pie chart (avoid in most cases), stacked area
- **Best practices**: label axes, title, legend; use color consistently; avoid 3D charts; minimize chart junk
- **Pair plot**: scatterplot matrix of all feature pairs; quick way to spot relationships and outliers
- **Correlation heatmap**: visualize `df.corr()` to identify multicollinearity and feature relationships
- For ML: learning curves, confusion matrix heatmap, ROC curve, feature importance bar chart
- Color: use colorblind-friendly palettes; sequential for continuous, diverging for centered data, qualitative for categories

## Patterns

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Set style
sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# --- Distribution ---
# Histogram + KDE
fig, ax = plt.subplots()
sns.histplot(df['price'], kde=True, bins=30, ax=ax)
ax.set_title('Price Distribution')
ax.set_xlabel('Price ($)')

# Box plot (detect outliers)
sns.boxplot(data=df, x='category', y='price')

# Violin plot (distribution + density)
sns.violinplot(data=df, x='category', y='price')

# --- Relationships ---
# Scatter plot
sns.scatterplot(data=df, x='age', y='salary', hue='department', alpha=0.7)

# Correlation heatmap
corr = df.select_dtypes('number').corr()
sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, fmt='.2f',
            mask=np.triu(np.ones_like(corr, dtype=bool)))

# Pair plot (all pairwise relationships)
sns.pairplot(df[['feat1', 'feat2', 'feat3', 'target']], hue='target', diag_kind='kde')

# --- ML Diagnostics ---
# Confusion matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
cm = confusion_matrix(y_true, y_pred)
ConfusionMatrixDisplay(cm, display_labels=['Negative', 'Positive']).plot(cmap='Blues')

# ROC curve
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(y_true, y_prob)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.3f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('FPR'); plt.ylabel('TPR'); plt.legend()

# Feature importance
importances = model.feature_importances_
sorted_idx = np.argsort(importances)
plt.barh(range(len(sorted_idx)), importances[sorted_idx])
plt.yticks(range(len(sorted_idx)), np.array(feature_names)[sorted_idx])
plt.xlabel('Importance')

# Learning curve
from sklearn.model_selection import learning_curve
train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)
)
plt.plot(train_sizes, train_scores.mean(axis=1), label='Train')
plt.plot(train_sizes, val_scores.mean(axis=1), label='Validation')
plt.xlabel('Training Set Size'); plt.ylabel('Score'); plt.legend()

# --- Subplots ---
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.histplot(df['col1'], ax=axes[0, 0])
sns.boxplot(data=df, y='col2', ax=axes[0, 1])
sns.scatterplot(data=df, x='col1', y='col2', ax=axes[1, 0])
sns.heatmap(corr, ax=axes[1, 1])
plt.tight_layout()

# Save figure
plt.savefig('plot.png', dpi=150, bbox_inches='tight')

# Plotly interactive
import plotly.express as px
fig = px.scatter(df, x='age', y='salary', color='department',
                 hover_data=['name'], title='Age vs Salary')
fig.show()
```

## Gotchas

- `plt.show()` clears the figure; call `plt.savefig()` BEFORE `plt.show()` or the saved file will be blank
- Seaborn `hue` parameter automatically splits data and adds legend; matplotlib requires manual loop
- Matplotlib OOP API (`fig, ax = plt.subplots()`) is preferred over pyplot for complex plots; easier to manage multiple subplots
- Heatmap `annot=True` with many cells creates clutter; for large correlation matrices, mask half with `mask=np.triu()`
- Pie charts are almost never the right choice; bar charts are easier to read for comparisons
- Seaborn functions return matplotlib Axes; you can further customize with matplotlib calls on the same ax

## See Also

- [[descriptive-statistics]] - compute summary stats before visualizing
- [[pandas-data-manipulation]] - data preparation for plotting
- [[model-evaluation-metrics]] - confusion matrix, ROC curve visualization
- [[cross-validation-and-model-selection]] - learning curve plots
- seaborn gallery: https://seaborn.pydata.org/examples/index.html
- matplotlib docs: https://matplotlib.org/stable/gallery/index.html
