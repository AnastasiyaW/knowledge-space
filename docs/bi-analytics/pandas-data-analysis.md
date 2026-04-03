---
title: pandas Data Analysis
category: tools
tags: [bi-analytics, python, pandas, dataframe, data-cleaning, groupby, analysis]
---

# pandas Data Analysis

pandas is the core Python library for tabular data manipulation and analysis. For BI analysts, it bridges the gap between SQL-based querying and the flexibility of Python for data cleaning, transformation, and exploratory analysis.

## Key Facts

- Two core structures: Series (1D labeled array) and DataFrame (2D labeled table)
- pandas operations map directly to SQL: groupby = GROUP BY, merge = JOIN, concat = UNION
- Vectorized operations are dramatically faster than `.iterrows()` loops
- Use `.copy()` when modifying filtered DataFrames to avoid SettingWithCopyWarning
- matplotlib/seaborn = quick exploratory analysis; for production dashboards use Tableau/Power BI

## Patterns

### Loading Data

```python
import pandas as pd

df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', sep=';', encoding='utf-8',
                  parse_dates=['date_col'])
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

import sqlalchemy
engine = sqlalchemy.create_engine('postgresql://user:pass@host/db')
df = pd.read_sql("SELECT * FROM orders WHERE date >= '2024-01-01'",
                  engine)
```

### Exploration

```python
df.shape            # (rows, columns)
df.dtypes           # column data types
df.info()           # summary: dtypes + non-null counts
df.describe()       # statistics for numeric columns
df.head(5)          # first 5 rows
df.sample(10)       # 10 random rows
df.nunique()        # unique value count per column
df['col'].value_counts()  # frequency table
```

### Selection and Filtering

```python
# Columns
df['sales']                  # Series
df[['name', 'sales']]       # DataFrame

# Rows by label
df.loc[df['age'] > 25]      # boolean indexing

# Rows by position
df.iloc[0:5]                 # rows 0-4
df.iloc[:, 0:2]              # all rows, first 2 columns

# Boolean filtering
filtered = df[(df['age'] > 25) & (df['sales'] > 1000)]
subset = df[df['city'].isin(['Moscow', 'SPb'])]
```

### Data Cleaning

```python
# Missing values
df.isnull().sum()
df.dropna(subset=['sales'])
df['sales'].fillna(df['sales'].mean(), inplace=True)

# Duplicates
df.duplicated().sum()
df.drop_duplicates(subset=['user_id'])

# Type conversion
df['date'] = pd.to_datetime(df['date'])
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['user_id'] = df['user_id'].astype(str)

# String cleaning
df['name'] = df['name'].str.strip().str.lower()
```

### Aggregation (groupby)

```python
# Single aggregation
df.groupby('city')['sales'].sum()

# Multiple aggregations (named)
agg = df.groupby('city').agg(
    order_count=('order_id', 'count'),
    total_sales=('sales', 'sum'),
    avg_order=('sales', 'mean'),
    unique_customers=('customer_id', 'nunique')
)

# Transform (keeps original row count)
df['city_avg'] = df.groupby('city')['sales'].transform('mean')
df['pct_of_city'] = df['sales'] / \
    df.groupby('city')['sales'].transform('sum')
```

### Pivot Tables

```python
pivot = pd.pivot_table(
    df, values='sales', index='city',
    columns='category', aggfunc='sum', fill_value=0
)

ct_pct = pd.crosstab(df['city'], df['category'],
                      normalize='index')  # row percentages
```

### Merging (SQL JOINs)

```python
pd.merge(df1, df2, on='user_id', how='left')    # LEFT JOIN
pd.merge(df1, df2, on='user_id', how='inner')   # INNER JOIN
pd.merge(df1, df2, left_on='id', right_on='uid') # different names
pd.concat([df1, df2], ignore_index=True)          # UNION
```

### Date Operations

```python
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday
df['days_since'] = (pd.Timestamp.today() - df['date']).dt.days
```

### Quick Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

df['sales'].hist(bins=30)
df.groupby('city')['sales'].sum().plot(kind='bar')
sns.boxplot(x='category', y='sales', data=df)
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
```

### Apply and Lambda

```python
df['tier'] = df['sales'].apply(
    lambda x: 'high' if x > 1000 else 'low'
)
df['score'] = df.apply(
    lambda row: row['sales'] * 0.1 + row['tenure'] * 5,
    axis=1
)
```

## Gotchas

- **NULL handling in averages**: averaging over NaN may be misleading - use `.fillna()` or `.dropna()` intentionally
- **Copy vs view**: `df[condition]` returns a view; use `.copy()` to modify: `subset = df[df['x']>0].copy()`
- **dtypes after merge**: integer columns become float if NULLs introduced by LEFT JOIN
- **Index reset**: after `.sort_values()` and `.head()`, use `.reset_index(drop=True)` for clean index
- **Performance**: use categorical dtype for low-cardinality strings; `pd.read_csv(usecols=[...])` to load only needed columns
- Always check `.shape`, `.isnull().sum()`, `.duplicated().sum()` after merges

## See Also

- [[sql-for-analytics]] - SQL equivalents of pandas operations
- [[python-for-analytics]] - Python basics and NumPy
- [[web-marketing-analytics]] - data sources for pandas analysis
