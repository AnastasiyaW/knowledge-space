---
title: "Pandas et analyse exploratoire de données"
category: tools
tags: [data-science, pandas, eda, python]
level: 3
source_sha256: 5f70d0d26cbec7c980d30f66918da4c09153be0caa14ec3a6361dad77353e6ae
translation: machine
translated_at: '2026-10-24'
---
# Pandas et analyse exploratoire de données {#pandas-and-exploratory-data-analysis}

Pandas est l'outil principal de manipulation de données tabulaires en Python. L'EDA est le processus systématique de compréhension des données avant la modélisation. Cette entrée couvre l'API pandas et le workflow d'EDA.

## Chargement des données {#loading-data}

```python
import pandas as pd

df = pd.read_csv('data.csv')
df = pd.read_csv('file.csv', encoding='cp1251')  # Cyrillic
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
df = pd.read_parquet('file.parquet')  # fastest for large data
df = pd.read_sql('SELECT * FROM table', connection)
```

Convention : nommer le DataFrame principal `df`, universel et facile à copier-coller.

## Inspection du DataFrame {#dataframe-inspection}

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

## Opérations sur les colonnes {#column-operations}

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

Note : `inplace=True` est déprécié. Toujours utiliser la réaffectation.

## Filtrage {#filtering}

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

**Correctif pour SettingWithCopyWarning** : toujours utiliser `.copy()` lors de l'enregistrement d'une tranche filtrée :
```python
filtered = df[df['city'] == 'NYC'].copy()
```

## Valeurs manquantes {#missing-values}

```python
df.isna().sum()               # count per column
df.isna().mean()              # fraction per column (preferred over percentages)

df['col'].fillna(df['col'].median())   # numeric: median
df['col'].fillna('Unknown')            # categorical: explicit value
df.dropna(subset=['critical_col'])     # drop rows where critical col is null
```

**Piège** : `groupby` et `value_counts` ignorent silencieusement les NaN par défaut. Toujours utiliser `dropna=False` :
```python
df['gender'].value_counts(dropna=False)
df.groupby('gender', dropna=False)['target'].agg(['count', 'mean'])
```

## GroupBy (outil d'analyse central) {#groupby-core-analysis-tool}

Moyen principal pour identifier les relations entre variables explicatives et cible.

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

### Discrétisation de variables continues pour GroupBy {#binning-continuous-for-groupby}

```python
df['group'] = pd.cut(df['col'], bins=5)          # equal-width
df['group'] = pd.qcut(df['col'], q=5)            # equal-count (quantile)
df['group'] = pd.cut(df['col'], bins=[0, 10, 50, 100, float('inf')])  # custom
```

### Tableaux croisés dynamiques {#pivot-tables}

```python
# Two-dimensional aggregation (great for heatmaps)
t = df.pivot_table(index='education', columns='gender',
                   values='target', aggfunc=['count', 'mean'])

# Flatten MultiIndex columns
t.columns = ['_'.join(col).strip() for col in t.columns.values]
t = t.reset_index()
```

## Tri et classement {#sorting-and-ranking}

```python
df.sort_values('price', ascending=False)
df.sort_values(['col1', 'col2'], ascending=[True, False])
df['rank'] = df['score'].rank(ascending=False)
```

## Merge / Join {#merge-join}

```python
result = df1.merge(df2, on='key', how='left')    # left/right/inner/outer
result = df1.merge(df2, left_on='col1', right_on='col2', how='inner')

# Concatenate vertically
full = pd.concat([train, val])
```

**Piège** : après un left join, toujours vérifier la présence de nouveaux NaN, ce qui indique des clés de df1 absentes de df2.

## Opérations sur les chaînes de caractères {#string-operations}

```python
df['text'].str.lower()
df['text'].str.contains('pattern')
df['text'].str.split('_')
df['text'].str.len()
```

## Regroupement des catégories {#category-re-grouping}

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

**Ne jamais itérer sur les lignes avec des boucles Python** : utiliser des opérations vectorisées ou `apply()`.

## Workflow d'EDA {#eda-workflow}

1. **Vue d'ensemble** : `df.shape`, `df.info()`, `df.describe()`
2. **Valeurs manquantes** : `df.isna().mean()`, décider pour chaque colonne de supprimer ou d'imputer
3. **Distribution de la cible** : histogramme ou countplot, vérifier l'équilibre des classes
4. **Distributions des variables** : histogrammes pour le numérique, `value_counts()` pour le catégoriel
5. **Corrélations** : heatmap de `df.corr()`, corrélations les plus fortes avec la cible
6. **Variable vs cible** : groupby + agg, box plots par classe cible
7. **Détection des valeurs aberrantes** : box plots, z-scores, méthode IQR
8. **Relations entre paires** : pairplot pour un petit ensemble de variables

## Pièges {#gotchas}

- `df['col'].value_counts()` ignore les NaN par défaut : toujours utiliser `dropna=False`
- `print(df)` dans Jupyter casse le formatage HTML : écrire simplement `df`
- Ne jamais saisir manuellement les noms de colonnes : les copier depuis la sortie
- `inplace=True` est déprécié et source de confusion : toujours réaffecter
- Les petits groupes (N < 30) dans un groupby produisent des statistiques peu fiables

## Voir aussi {#see-also}
- [[data-visualization]] - tracer des données pandas
- [[feature-engineering]] - transformer les variables pour le ML
- [[numpy-fundamentals]] - opérations sur les tableaux qui sous-tendent pandas
- [[descriptive-statistics]] - mesures statistiques calculées lors de l'EDA
