---
title: "pandas-Datenanalyse"
category: tools
tags: [bi-analytics, python, pandas, dataframe, data-cleaning, groupby, analysis]
level: 3
source_sha256: 1508bd2c3f6d29a02be3f864892924ed238f28d797f0d1832f47888a7ee0338d
translation: machine
translated_at: '2026-10-24'
---
# pandas-Datenanalyse {#pandas-data-analysis}

pandas ist die zentrale Python-Bibliothek für die Manipulation und Analyse tabellarischer Daten. Für BI-Analysten schließt sie die Lücke zwischen SQL-basierten Abfragen und der Flexibilität von Python für Datenbereinigung, Transformation und explorative Analyse.

## Key Facts {#key-facts}

- Zwei Kernstrukturen: Series (eindimensionales, beschriftetes Array) und DataFrame (zweidimensionale, beschriftete Tabelle)
- pandas-Operationen entsprechen direkt SQL: groupby = GROUP BY, merge = JOIN, concat = UNION
- Vektorisierte Operationen sind deutlich schneller als `.iterrows()`-Schleifen
- Verwende `.copy()` beim Ändern gefilterter DataFrames, um SettingWithCopyWarning zu vermeiden
- matplotlib/seaborn = schnelle explorative Analyse; für produktive Dashboards Tableau/Power BI verwenden

## Patterns {#patterns}

### Loading Data {#loading-data}

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

### Exploration {#exploration}

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

### Selection and Filtering {#selection-and-filtering}

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

### Data Cleaning {#data-cleaning}

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

### Aggregation (groupby) {#aggregation-groupby}

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

### Pivot Tables {#pivot-tables}

```python
pivot = pd.pivot_table(
    df, values='sales', index='city',
    columns='category', aggfunc='sum', fill_value=0
)

ct_pct = pd.crosstab(df['city'], df['category'],
                      normalize='index')  # row percentages
```

### Merging (SQL JOINs) {#merging-sql-joins}

```python
pd.merge(df1, df2, on='user_id', how='left')    # LEFT JOIN
pd.merge(df1, df2, on='user_id', how='inner')   # INNER JOIN
pd.merge(df1, df2, left_on='id', right_on='uid') # different names
pd.concat([df1, df2], ignore_index=True)          # UNION
```

### Date Operations {#date-operations}

```python
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday
df['days_since'] = (pd.Timestamp.today() - df['date']).dt.days
```

### Quick Visualization {#quick-visualization}

```python
import matplotlib.pyplot as plt
import seaborn as sns

df['sales'].hist(bins=30)
df.groupby('city')['sales'].sum().plot(kind='bar')
sns.boxplot(x='category', y='sales', data=df)
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
```

### Apply and Lambda {#apply-and-lambda}

```python
df['tier'] = df['sales'].apply(
    lambda x: 'high' if x > 1000 else 'low'
)
df['score'] = df.apply(
    lambda row: row['sales'] * 0.1 + row['tenure'] * 5,
    axis=1
)
```

## Gotchas {#gotchas}

- **NULL-Behandlung bei Durchschnittswerten**: Die Mittelwertbildung über NaN kann irreführend sein – verwende `.fillna()` oder `.dropna()` bewusst
- **Kopie vs. View**: `df[condition]` liefert einen View; zum Ändern `.copy()` verwenden: `subset = df[df['x']>0].copy()`
- **dtypes nach einem Merge**: Ganzzahlspalten werden zu float, wenn durch LEFT JOIN NULLs entstehen
- **Index zurücksetzen**: Nach `.sort_values()` und `.head()` `.reset_index(drop=True)` für einen sauberen Index verwenden
- **Performance**: Für Strings mit niedriger Kardinalität den Datentyp categorical verwenden; `pd.read_csv(usecols=[...])` lädt nur die benötigten Spalten
- Nach Merges immer `.shape`, `.isnull().sum()` und `.duplicated().sum()` prüfen

## See Also {#see-also}

- [[sql-for-analytics]] - SQL-Entsprechungen der pandas-Operationen
- [[python-for-analytics]] - Python-Grundlagen und NumPy
- [[web-marketing-analytics]] - Datenquellen für die pandas-Analyse
