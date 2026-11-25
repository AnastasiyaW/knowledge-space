---
title: "Feature Engineering und Preprocessing"
category: techniques
tags: [data-science, feature-engineering, preprocessing, sklearn]
level: 3
source_sha256: 0b9264a73f73fed21cef65b6d9d301b06ef27131778f93b5175ef0581918c5e4
translation: machine
translated_at: '2026-10-24'
---
# Feature Engineering und Preprocessing {#feature-engineering-and-preprocessing}

Die Kunst, Rohdaten in Merkmale zu transformieren, die ML-Modelle effektiv nutzen können. Oft der einflussreichste Schritt in einem DS-Projekt – gute Features schlagen komplexe Modelle.

## Feature Scaling {#feature-scaling}

Lineare Modelle und neuronale Netze sind empfindlich gegenüber Feature-Skalierungen. Baumbasierte Modelle (CatBoost, Random Forest) sind das NICHT.

### StandardScaler (Z-Score) {#standardscaler-z-score}

Transformiert auf Mittelwert=0, Standardabweichung=1: z = (x - Mittelwert) / Standardabweichung

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # fit on train ONLY
X_test_scaled = scaler.transform(X_test)         # transform with train stats
```

### MinMaxScaler {#minmaxscaler}

Skaliert auf [0, 1]: x_scaled = (x - x_min) / (x_max - x_min)

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)
```

**Kritische Regel**: Scaler nur auf den Trainingsdaten fitten, dann sowohl Trainings- als auch Testdaten transformieren. Fitten auf den Testdaten = Data Leakage.

## Kategorische Kodierung {#categorical-encoding}

### One-Hot Encoding {#one-hot-encoding}
N Kategorien -> N binäre Spalten. Für nominale (ungeordnete) Kategorien verwenden.
```python
pd.get_dummies(df['col'], drop_first=True)  # drop_first avoids multicollinearity

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(drop='first', sparse_output=False)
```

### Label Encoding {#label-encoding}
Ordnet Kategorien ganzzahlige Werte zu. Nur für ordinale Daten (mit natürlicher Reihenfolge) verwenden.
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['encoded'] = le.fit_transform(df['col'])
```

### Target Encoding {#target-encoding}
Ersetzt die Kategorie durch den Mittelwert des Targets für diese Kategorie. CatBoost macht das intern mit Regularisierung. Ohne korrekte CV-basierte Kodierung besteht ein hohes Risiko für Data Leakage.

## Imputation fehlender Werte {#missing-value-imputation}

```python
from sklearn.impute import SimpleImputer

# Numerical: median is robust to outliers
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# Categorical: most frequent or constant
imputer_cat = SimpleImputer(strategy='most_frequent')
```

**Pro-Tipp**: Vor der Imputation einen binären Indikator `is_missing` anlegen – die Fehlstelle selbst kann informativ sein.

## Feature Selection {#feature-selection}

### Filter-Methoden (modellunabhängig) {#filter-methods-model-independent}
```python
from sklearn.feature_selection import VarianceThreshold, mutual_info_classif

# Remove near-constant features
sel = VarianceThreshold(threshold=0.01)
X_filtered = sel.fit_transform(X)

# Mutual information (captures non-linear relationships)
mi_scores = mutual_info_classif(X, y)
```

### Wrapper-Methoden (modellabhängig) {#wrapper-methods-model-dependent}
```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

selector = RFE(LogisticRegression(), n_features_to_select=10)
X_selected = selector.fit_transform(X, y)
```

### Eingebettete Methoden (im Modell integriert) {#embedded-methods-built-into-model}
- **L1/Lasso**: drückt unwichtige Gewichte auf exakt null
- **Baumbasierte Wichtigkeit**: `model.feature_importances_` aus Random Forest, CatBoost

## Regularisierung {#regularization}

Verhindert Overfitting, indem große Koeffizienten bestraft werden.

| Typ | Strafterm | Wirkung | Wann verwenden |
|------|---------|--------|-------------|
| L2 (Ridge) | sum(beta_j^2) | Verkleinert alle, nie null | Multikollinearität |
| L1 (Lasso) | sum(\|beta_j\|) | Drückt einige auf exakt 0 | Feature Selection |
| Elastic Net | L1 + L2 | Kombiniert | Gruppen korrelierter Features |

**Warum L1 Nullen erzeugt**: Die L1-Kugel hat Ecken auf den Achsen – das Optimum liegt häufig an einer Ecke. Die L2-Kugel ist glatt – der Berührpunkt liegt fast nie auf einer Achse.

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
ridge = Ridge(alpha=1.0)    # alpha = regularization strength
lasso = Lasso(alpha=0.1)
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
```

## Sklearn Pipelines {#sklearn-pipelines}

Preprocessing und Modell verketten. Verhindert Data Leakage.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_cols),
    ('cat', OneHotEncoder(drop='first'), categorical_cols)
])

pipe = Pipeline([
    ('preprocess', preprocessor),
    ('model', LogisticRegression())
])
pipe.fit(X_train, y_train)
predictions = pipe.predict(X_test)
```

## Feature-Engineering-Techniken {#feature-engineering-techniques}

- **Domänenbasiert**: Domänenwissen nutzen (lat/lon -> Distanz, Datum -> Wochentag)
- **Interaktions-Features**: x1 * x2 erfasst gemeinsame Effekte
- **Polynomiale Features**: x^2, x^3 für nichtlineare Zusammenhänge
- **Aggregations-Features**: groupby-Statistiken (Mittelwert, Anzahl, Std) verwandter Entitäten
- **Zeitbasiert**: day_of_week, month, hour, is_weekend, days_since_event
- **Textbasiert**: Wortanzahl, TF-IDF-Features, n-Gramme

```python
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, interaction_only=False)
X_poly = poly.fit_transform(X)
```

## Erkennung nichtlinearer Korrelationen {#non-linear-correlation-detection}

```python
# phik - detects non-linear AND works with categoricals
import phik
corr_matrix = df.phik_matrix()
df.phik_matrix()['target'].sort_values(ascending=False)
```

Ergebnisse von phik immer mit Pivot-Tabellen überprüfen. Phik zeigt, WO man suchen sollte, Pivot-Tabellen bestätigen es.

## Stolperfallen {#gotchas}
- **Data Leakage** durch Preprocessing: Scaler/Encoder auf Testdaten fitten oder Target Encoding ohne CV berechnen
- **One-Hot-Explosion**: 1000 Kategorien = 1000 Features. Stattdessen Target Encoding oder Embeddings verwenden
- **Label Encoding für Nominaldaten**: erzeugt eine falsche Ordnungsbeziehung (das Modell hält Kategorie 3 für größer als Kategorie 1)
- **Polynomiale Features**: degree=3 bei 100 Features = Millionen Features. `interaction_only=True` verwenden oder manuell auswählen
- **Feature Importance aus einem einzelnen Baummodell ist unzuverlässig** – Permutation Importance verwenden oder über ein Ensemble mitteln

## Siehe auch {#see-also}
- [[pandas-eda]] - Datenexploration vor dem Feature Engineering
- [[linear-models]] - Modelle, die am stärksten von Feature Engineering abhängen
- [[gradient-boosting]] - Modelle mit eingebauter Feature-Behandlung
- [[model-evaluation]] - Bewertung des Einflusses von Features auf die Performance
