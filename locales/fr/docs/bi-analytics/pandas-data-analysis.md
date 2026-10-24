---
title: "Analyse de données avec pandas"
category: tools
tags: [bi-analytics, python, pandas, dataframe, data-cleaning, groupby, analysis]
level: 3
source_sha256: 1508bd2c3f6d29a02be3f864892924ed238f28d797f0d1832f47888a7ee0338d
translation: machine
translated_at: '2026-10-24'
---
# Analyse de données avec pandas {#pandas-data-analysis}

pandas est la bibliothèque Python de référence pour la manipulation et l'analyse de données tabulaires. Pour les analystes BI, elle fait le lien entre les requêtes SQL et la souplesse de Python pour le nettoyage de données, les transformations et l'analyse exploratoire.

## Points clés {#key-facts}

- Deux structures principales : Series (tableau 1D étiqueté) et DataFrame (tableau 2D étiqueté)
- Les opérations pandas correspondent directement à SQL : groupby = GROUP BY, merge = JOIN, concat = UNION
- Les opérations vectorisées sont nettement plus rapides que les boucles `.iterrows()`
- Utilisez `.copy()` lorsque vous modifiez des DataFrames filtrés afin d'éviter SettingWithCopyWarning
- matplotlib/seaborn = analyse exploratoire rapide ; pour les tableaux de bord de production, utilisez Tableau/Power BI

## Modèles d'usage {#patterns}

### Chargement des données {#loading-data}

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

### Sélection et filtrage {#selection-and-filtering}

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

### Nettoyage des données {#data-cleaning}

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

### Agrégation (groupby) {#aggregation-groupby}

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

### Tableaux croisés dynamiques {#pivot-tables}

```python
pivot = pd.pivot_table(
    df, values='sales', index='city',
    columns='category', aggfunc='sum', fill_value=0
)

ct_pct = pd.crosstab(df['city'], df['category'],
                      normalize='index')  # row percentages
```

### Fusion (équivalent des JOIN SQL) {#merging-sql-joins}

```python
pd.merge(df1, df2, on='user_id', how='left')    # LEFT JOIN
pd.merge(df1, df2, on='user_id', how='inner')   # INNER JOIN
pd.merge(df1, df2, left_on='id', right_on='uid') # different names
pd.concat([df1, df2], ignore_index=True)          # UNION
```

### Opérations sur les dates {#date-operations}

```python
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday
df['days_since'] = (pd.Timestamp.today() - df['date']).dt.days
```

### Visualisation rapide {#quick-visualization}

```python
import matplotlib.pyplot as plt
import seaborn as sns

df['sales'].hist(bins=30)
df.groupby('city')['sales'].sum().plot(kind='bar')
sns.boxplot(x='category', y='sales', data=df)
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
```

### Apply et lambda {#apply-and-lambda}

```python
df['tier'] = df['sales'].apply(
    lambda x: 'high' if x > 1000 else 'low'
)
df['score'] = df.apply(
    lambda row: row['sales'] * 0.1 + row['tenure'] * 5,
    axis=1
)
```

## Pièges à éviter {#gotchas}

- **Gestion des NULL dans les moyennes** : calculer une moyenne en présence de NaN peut être trompeur ; utilisez `.fillna()` ou `.dropna()` de manière délibérée
- **Copie ou vue** : `df[condition]` renvoie une vue ; utilisez `.copy()` pour la modifier : `subset = df[df['x']>0].copy()`
- **Types de données après une fusion** : les colonnes entières deviennent des flottants si un LEFT JOIN introduit des NULL
- **Réinitialisation de l'index** : après `.sort_values()` et `.head()`, utilisez `.reset_index(drop=True)` pour obtenir un index propre
- **Performances** : utilisez le type categorical pour les chaînes à faible cardinalité ; `pd.read_csv(usecols=[...])` pour ne charger que les colonnes nécessaires
- Vérifiez systématiquement `.shape`, `.isnull().sum()` et `.duplicated().sum()` après les fusions

## Voir aussi {#see-also}

- [[sql-for-analytics]] - équivalents SQL des opérations pandas
- [[python-for-analytics]] - bases de Python et NumPy
- [[web-marketing-analytics]] - sources de données pour l'analyse avec pandas
