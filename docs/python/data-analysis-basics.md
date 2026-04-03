---
title: Data Analysis Basics (Pandas and Matplotlib)
category: concepts
tags: [python, pandas, matplotlib, seaborn, dataframe, visualization, data-science]
---

# Data Analysis Basics (Pandas and Matplotlib)

Pandas provides tabular data structures (DataFrame, Series) for data manipulation and analysis. Matplotlib and Seaborn handle visualization. Together with NumPy, they form the foundation of Python's data science ecosystem.

## Key Facts

- DataFrame is a 2D labeled table (like a spreadsheet); Series is a 1D labeled array (column)
- Pandas is for data that fits in memory; PySpark for distributed large-scale data
- `pd.concat()` for stacking DataFrames; `pd.merge()` for SQL-style joins
- Matplotlib has two APIs: pyplot (MATLAB-style) and OOP (fig, ax - more control)
- Seaborn wraps Matplotlib with better defaults and statistical plotting
- Miller's rule: plots with >8 categories become unreadable - use a table instead

## Patterns

### Pandas Core Operations
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

### Concat and Merge
```python
# Vertical stack
pd.concat([df1, df2])
pd.concat([df1, df2], join='inner')  # common columns only

# SQL-style join
pd.merge(employees, departments, on='dept_id')
pd.merge(left, right, left_on='id', right_on='emp_id', how='left')
```

### Matplotlib
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

### Common Plot Types
```python
plt.plot(x, y)                    # line
plt.scatter(x, y, c=colors)      # scatter
plt.bar(categories, values)       # bar
plt.hist(data, bins=30)           # histogram
plt.contourf(X, Y, Z, cmap='RdGy')  # contour
```

### Seaborn
```python
import seaborn as sns

sns.pairplot(df)                          # all variables against each other
sns.heatmap(df.corr(), annot=True)        # correlation matrix
sns.boxplot(x='category', y='value', data=df)
```

### NumPy Basics
```python
import numpy as np

arr = np.array([1, 2, 3])
zeros = np.zeros((3, 4))        # 3x4 matrix of zeros
rand = np.random.random((2, 3)) # 2x3 random matrix
np.random.seed(42)              # reproducibility
```

## Visualization Best Practices

- **Trends over time** -> line chart
- **Comparisons** -> bar chart
- **Distributions** -> histogram or box plot
- **Relationships** -> scatter plot
- **Proportions** -> pie chart (use sparingly)
- **3D on 2D** -> contour or heatmap
- Max ~8 categories per chart; beyond that, use a table

## Gotchas

- Pandas `concat` with repeated `append` has quadratic complexity - collect all DataFrames, then concat once
- `pd.merge()` auto-detects join column from common names; specify `on=` to be explicit
- Matplotlib pyplot state API is convenient but hard to manage for complex figures - prefer OOP style
- For large datasets, Matplotlib is slow - use `datashader` or Plotly/Bokeh with WebGL

## See Also

- [[data-structures]] - Python built-in collections
- [[file-io]] - reading CSV, JSON data files
- [[data-science/index]] - advanced data science topics
