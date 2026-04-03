---
title: Pandas and Exploratory Data Analysis
category: tools
tags: [data-science, pandas, eda, python]
---

# Pandas and Exploratory Data Analysis

Pandas is the primary tool for tabular data manipulation in Python. EDA is the systematic process of understanding data before modeling. This entry covers the pandas API and the EDA workflow.

## Loading Data

```python
import pandas as pd

df = pd.read_csv('data.csv')
df = pd.read_csv('file.csv', encoding='cp1251')  # Cyrillic
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
df = pd.read_parquet('file.parquet')  # fastest for large data
df = pd.read_sql('SELECT * FROM table', connection)
```

Convention: name main DataFrame `df` - universal, easy copy-paste.

## DataFrame Inspection

```python
df.head(10)          # first N rows
df.tail(5)           # last N rows
df.shape             # (rows, cols)
df.columns           # column names
df.dtypes            # data types
df.info()            # types + non-null counts
df.describe()        # numeric summary (mean, std, quartiles)
df.describe(include='object')  # categorical summary
df.nunique()         # unique values per column
len(df)              # row count
```

## Column Operations

```python
# Select
df['city']                       # Series
df[['city']]                     # DataFrame (single col)
df[['city', 'price']]            # multiple - double brackets required

# Add
df['new_col'] = 1                         # constant
df['ratio'] = df['a'] / df['b']           # computed
df.assign(temp=99)                        # non-mutating, returns new df

# Remove
df = df.drop('city', axis=1)              # axis=1 = column
df = df[['col1', 'col2']]                 # select only needed

# Rename
df = df.rename(columns={'old': 'new'})
```

Note: `inplace=True` is deprecated. Always use reassignment.

## Filtering

```python
# Single condition
df[df['price'] > 100]

# Multiple conditions (each in parentheses)
df[(df['city'] == 'NYC') & (df['price'] > 100)]
df[(df['city'] == 'NYC') | (df['city'] == 'LA')]

# Query syntax (equivalent, often cleaner)
df.query("city == 'NYC' and price > 100")

# Between
df[df['col'].between(q1, q2)]

# Quantile-based outlier removal
q05, q95 = df['col'].quantile(0.05), df['col'].quantile(0.95)
df_trimmed = df[df['col'].between(q05, q95)]
```

**SettingWithCopyWarning fix**: always `.copy()` when saving filtered slice:
```python
filtered = df[df['city'] == 'NYC'].copy()
```

## Missing Values

```python
df.isna().sum()               # count per column
df.isna().mean()              # fraction per column (preferred over percentages)

df['col'].fillna(df['col'].median())   # numeric: median
df['col'].fillna('Unknown')            # categorical: explicit value
df.dropna(subset=['critical_col'])     # drop rows where critical col is null
```

**Gotcha**: `groupby` and `value_counts` silently ignore NaN by default. Always use `dropna=False`:
```python
df['gender'].value_counts(dropna=False)
df.groupby('gender', dropna=False)['target'].agg(['count', 'mean'])
```

## GroupBy (Core Analysis Tool)

Primary way to find feature-target relationships.

```python
# Basic
df.groupby('gender')['target'].mean()

# With counts (always include for context!)
df.groupby('gender', dropna=False)['target'].agg(['count', 'mean'])

# Multiple aggregations
df.groupby('col').agg({'target': 'mean', 'salary': ['mean', 'median', 'std']})

# Checksum validation - ALWAYS verify
grouped = df.groupby('gender', dropna=False)['target'].agg(['count', 'mean'])
assert grouped['count'].sum() == len(df)
```

### Binning Continuous for GroupBy

```python
df['group'] = pd.cut(df['col'], bins=5)          # equal-width
df['group'] = pd.qcut(df['col'], q=5)            # equal-count (quantile)
df['group'] = pd.cut(df['col'], bins=[0, 10, 50, 100, float('inf')])  # custom
```

### Pivot Tables

```python
# Two-dimensional aggregation (great for heatmaps)
t = df.pivot_table(index='education', columns='gender',
                   values='target', aggfunc=['count', 'mean'])

# Flatten MultiIndex columns
t.columns = ['_'.join(col).strip() for col in t.columns.values]
t = t.reset_index()
```

## Sorting and Ranking

```python
df.sort_values('price', ascending=False)
df.sort_values(['col1', 'col2'], ascending=[True, False])
df['rank'] = df['score'].rank(ascending=False)
```

## Merge / Join

```python
result = df1.merge(df2, on='key', how='left')    # left/right/inner/outer
result = df1.merge(df2, left_on='col1', right_on='col2', how='inner')

# Concatenate vertically
full = pd.concat([train, val])
```

**Gotcha**: after left join, always check for new NaN - indicates keys in df1 not found in df2.

## String Operations

```python
df['text'].str.lower()
df['text'].str.contains('pattern')
df['text'].str.split('_')
df['text'].str.len()
```

## Category Re-grouping

```python
# Method 1: apply()
def education_group(x):
    if x in ['High School', 'Primary']:
        return 'School'
    return x
df['edu_group'] = df['education'].apply(education_group)

# Method 2: replace() - unmapped stay as-is
df['col'].replace({'Primary': 'School', 'High School': 'School'})

# Method 3: map() - unmapped become NaN
df['col'].map({'Primary': 'School', 'High School': 'School'})
```

**Never iterate rows with Python loops** - use vectorized operations or `apply()`.

## EDA Workflow

1. **Overview**: `df.shape`, `df.info()`, `df.describe()`
2. **Missing values**: `df.isna().mean()` - decide drop/impute per column
3. **Target distribution**: histogram/countplot - check balance
4. **Feature distributions**: histograms for numeric, `value_counts()` for categorical
5. **Correlations**: `df.corr()` heatmap, top correlations with target
6. **Feature vs target**: groupby + agg, box plots by target class
7. **Outlier detection**: box plots, z-scores, IQR method
8. **Pair relationships**: pairplot for small feature set

## Gotchas
- `df['col'].value_counts()` ignores NaN by default - always use `dropna=False`
- `print(df)` in Jupyter destroys HTML formatting - just write `df`
- Never type column names manually - copy from output
- `inplace=True` is deprecated and confusing - always reassign
- Small groups (N < 30) in groupby produce unreliable statistics

## See Also
- [[data-visualization]] - plotting pandas data
- [[feature-engineering]] - transforming features for ML
- [[numpy-fundamentals]] - array operations underlying pandas
- [[descriptive-statistics]] - statistical measures computed in EDA
