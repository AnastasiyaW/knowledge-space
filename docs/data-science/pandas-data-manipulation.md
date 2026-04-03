---
title: Pandas Data Manipulation
category: tools
tags: [pandas, dataframe, data-wrangling, groupby, merge, python, eda]
---

# Pandas Data Manipulation

The core library for tabular data manipulation in Python. DataFrame is the central data structure -- a labeled 2D table with typed columns. Covers loading, cleaning, transforming, aggregating, and merging data. Prerequisite for [[feature-engineering]], [[descriptive-statistics]], and [[data-visualization]].

## Key Facts

- **DataFrame**: 2D labeled data structure; rows (index) x columns; each column = Series with a dtype
- **Series**: 1D labeled array; one column of a DataFrame
- **dtypes**: int64, float64, object (strings), category, datetime64, bool; check with `df.dtypes`
- **Index**: row labels; default 0..n-1; can be set to any column; enables fast lookup and alignment
- **Vectorized operations**: operate on entire columns at once; 10-100x faster than Python loops
- **GroupBy**: split-apply-combine pattern; `df.groupby('col').agg(...)` for aggregations
- **Merge/Join**: combine DataFrames; inner, left, right, outer; on keys; equivalent to SQL JOIN
- **Pivot/Melt**: reshape data; pivot (long -> wide), melt (wide -> long)
- **Method chaining**: `df.query(...).groupby(...).agg(...).reset_index()` -- functional, readable pipeline
- **Memory**: `category` dtype for low-cardinality strings saves 90%+ memory; `df.memory_usage(deep=True)`
- **Missing values**: NaN for float, pd.NA for nullable types; `df.isna()`, `df.fillna()`, `df.dropna()`
- For large datasets (>1GB): use `read_csv(..., chunksize=...)`, Parquet format, or polars library

## Patterns

```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data.csv', parse_dates=['date'], dtype={'category': 'category'})
df = pd.read_parquet('data.parquet')  # faster than CSV, preserves dtypes

# Quick inspection
df.head()
df.info()          # dtypes, non-null counts, memory usage
df.describe()      # statistics for numeric columns
df.shape           # (rows, cols)
df.dtypes
df.isna().sum()    # missing values per column

# Selecting data
df['col']                     # single column -> Series
df[['col1', 'col2']]          # multiple columns -> DataFrame
df.loc[0:5, 'col1':'col3']   # by label (inclusive both ends)
df.iloc[0:5, 0:3]            # by position (exclusive end)
df.query('age > 30 & salary > 50000')  # SQL-like filtering

# Filtering
mask = (df['age'] > 30) & (df['salary'] > 50000)
filtered = df[mask]
filtered = df[df['city'].isin(['Moscow', 'SPb'])]

# Adding/modifying columns
df['total'] = df['price'] * df['quantity']
df['log_price'] = np.log1p(df['price'])
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 65, 100], labels=['child', 'young', 'adult', 'senior'])

# apply for complex transformations
df['name_length'] = df['name'].apply(len)
# Prefer vectorized ops over apply when possible (faster)

# GroupBy aggregations
summary = df.groupby('category').agg(
    avg_price=('price', 'mean'),
    total_sales=('quantity', 'sum'),
    n_products=('product_id', 'nunique')
).reset_index()

# Multiple aggregations
df.groupby('category')['price'].agg(['mean', 'median', 'std', 'count'])

# Merge (SQL-like JOIN)
merged = pd.merge(orders, customers, on='customer_id', how='left')
# how: 'inner', 'left', 'right', 'outer'

# Pivot table
pivot = df.pivot_table(
    values='sales', index='region', columns='product',
    aggfunc='sum', fill_value=0
)

# Melt (wide -> long)
melted = pd.melt(df, id_vars=['id'], value_vars=['jan', 'feb', 'mar'],
                 var_name='month', value_name='sales')

# Handle missing values
df['col'].fillna(df['col'].median(), inplace=True)
df.dropna(subset=['important_col'], inplace=True)

# String operations
df['name_lower'] = df['name'].str.lower()
df['has_email'] = df['email'].str.contains('@', na=False)

# Date operations
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.day_name()

# Window functions
df['rolling_mean'] = df.groupby('product')['sales'].transform(
    lambda x: x.rolling(7, min_periods=1).mean()
)
df['rank'] = df.groupby('category')['sales'].rank(ascending=False)

# Optimize memory
for col in df.select_dtypes(['object']).columns:
    if df[col].nunique() < df.shape[0] * 0.5:
        df[col] = df[col].astype('category')
```

## Gotchas

- `df['col']` returns a view, not a copy; modifying it may trigger `SettingWithCopyWarning`; use `df.loc[:, 'col'] = ...` or `.copy()`
- `inplace=True` is deprecated in newer pandas; prefer reassignment: `df = df.dropna()`
- `pd.merge()` default is inner join; use `how='left'` explicitly to avoid silently dropping rows
- `groupby()` drops NaN groups by default; use `dropna=False` to include them
- `df.loc` uses inclusive slicing on both ends; `df.iloc` uses exclusive end (like Python lists)
- `apply()` is slow (Python loop underneath); use vectorized pandas/numpy operations whenever possible
- Chained indexing `df[condition]['col'] = val` does NOT modify original DataFrame; use `.loc` instead

## See Also

- [[descriptive-statistics]] - summary statistics computed with pandas
- [[data-visualization]] - plotting directly from pandas DataFrames
- [[feature-engineering]] - pandas transformations for ML feature creation
- [[hypothesis-testing]] - data preparation before statistical tests
- pandas docs: https://pandas.pydata.org/docs/reference/index.html
