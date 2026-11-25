---
title: "Pandas und explorative Datenanalyse"
category: tools
tags: [data-science, pandas, eda, python]
level: 3
source_sha256: 5f70d0d26cbec7c980d30f66918da4c09153be0caa14ec3a6361dad77353e6ae
translation: machine
translated_at: '2026-10-24'
---
# Pandas und explorative Datenanalyse {#pandas-and-exploratory-data-analysis}

Pandas ist das wichtigste Werkzeug für die Bearbeitung tabellarischer Daten in Python. EDA ist der systematische Prozess, Daten vor der Modellierung zu verstehen. Dieser Eintrag behandelt die pandas-API und den EDA-Workflow.

## Daten laden {#loading-data}

```python
import pandas as pd

df = pd.read_csv('data.csv')
df = pd.read_csv('file.csv', encoding='cp1251')  # Cyrillic
df = pd.read_excel('file.xlsx', sheet_name='Sheet1')
df = pd.read_parquet('file.parquet')  # fastest for large data
df = pd.read_sql('SELECT * FROM table', connection)
```

Konvention: Das zentrale DataFrame wird `df` genannt - allgemein üblich und leicht zum Kopieren und Einfügen.

## DataFrame-Inspektion {#dataframe-inspection}

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

## Spaltenoperationen {#column-operations}

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

Hinweis: `inplace=True` ist veraltet. Verwende immer eine Neuzuweisung.

## Filtern {#filtering}

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

**Behebung von SettingWithCopyWarning**: Beim Speichern eines gefilterten Ausschnitts immer `.copy()` verwenden:
```python
filtered = df[df['city'] == 'NYC'].copy()
```

## Fehlende Werte {#missing-values}

```python
df.isna().sum()               # count per column
df.isna().mean()              # fraction per column (preferred over percentages)

df['col'].fillna(df['col'].median())   # numeric: median
df['col'].fillna('Unknown')            # categorical: explicit value
df.dropna(subset=['critical_col'])     # drop rows where critical col is null
```

**Gotcha**: `groupby` und `value_counts` ignorieren NaN standardmäßig stillschweigend. Verwende daher immer `dropna=False`:
```python
df['gender'].value_counts(dropna=False)
df.groupby('gender', dropna=False)['target'].agg(['count', 'mean'])
```

## GroupBy (zentrales Analysewerkzeug) {#groupby-core-analysis-tool}

Das wichtigste Mittel, um Zusammenhänge zwischen Features und Zielvariable zu finden.

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

### Binning kontinuierlicher Werte für GroupBy {#binning-continuous-for-groupby}

```python
df['group'] = pd.cut(df['col'], bins=5)          # equal-width
df['group'] = pd.qcut(df['col'], q=5)            # equal-count (quantile)
df['group'] = pd.cut(df['col'], bins=[0, 10, 50, 100, float('inf')])  # custom
```

### Pivot-Tabellen {#pivot-tables}

```python
# Two-dimensional aggregation (great for heatmaps)
t = df.pivot_table(index='education', columns='gender',
                   values='target', aggfunc=['count', 'mean'])

# Flatten MultiIndex columns
t.columns = ['_'.join(col).strip() for col in t.columns.values]
t = t.reset_index()
```

## Sortieren und Ranking {#sorting-and-ranking}

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

**Gotcha**: Prüfe nach einem Left Join immer auf neue NaN-Werte - sie zeigen Schlüssel in df1 an, die in df2 nicht gefunden wurden.

## String-Operationen {#string-operations}

```python
df['text'].str.lower()
df['text'].str.contains('pattern')
df['text'].str.split('_')
df['text'].str.len()
```

## Kategorien neu gruppieren {#category-re-grouping}

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

**Zeilen niemals mit Python-Schleifen iterieren** - verwende vektorisierte Operationen oder `apply()`.

## EDA-Workflow {#eda-workflow}

1. **Überblick**: `df.shape`, `df.info()`, `df.describe()`
2. **Fehlende Werte**: `df.isna().mean()` - pro Spalte entscheiden, ob gelöscht oder imputiert wird
3. **Verteilung der Zielvariable**: Histogramm/Countplot - Balance prüfen
4. **Verteilung der Features**: Histogramme für numerische, `value_counts()` für kategoriale Features
5. **Korrelationen**: Heatmap von `df.corr()`, stärkste Korrelationen mit der Zielvariable
6. **Feature vs. Zielvariable**: groupby + agg, Box-Plots nach Zielklasse
7. **Ausreißererkennung**: Box-Plots, z-Scores, IQR-Methode
8. **Paarweise Beziehungen**: Pairplot für eine kleine Feature-Menge

## Gotchas {#gotchas}
- `df['col'].value_counts()` ignoriert NaN standardmäßig - verwende immer `dropna=False`
- `print(df)` in Jupyter zerstört die HTML-Formatierung - schreibe einfach `df`
- Spaltennamen niemals manuell tippen - aus der Ausgabe kopieren
- `inplace=True` ist veraltet und verwirrend - immer neu zuweisen
- Kleine Gruppen (N < 30) in groupby liefern unzuverlässige Statistiken

## Siehe auch {#see-also}
- [[data-visualization]] - Plotten von pandas-Daten
- [[feature-engineering]] - Transformation von Features für ML
- [[numpy-fundamentals]] - Array-Operationen, auf denen pandas aufbaut
- [[descriptive-statistics]] - statistische Kennzahlen, die in der EDA berechnet werden
