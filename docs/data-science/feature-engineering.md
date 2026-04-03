---
title: Feature Engineering and Preprocessing
category: techniques
tags: [data-science, feature-engineering, preprocessing, sklearn]
---

# Feature Engineering and Preprocessing

The art of transforming raw data into features that ML models can use effectively. Often the single most impactful step in a DS project - good features beat complex models.

## Feature Scaling

Linear models and neural networks are sensitive to feature scales. Tree-based models (CatBoost, Random Forest) are NOT.

### StandardScaler (Z-score)

Transforms to mean=0, std=1: z = (x - mean) / std

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # fit on train ONLY
X_test_scaled = scaler.transform(X_test)         # transform with train stats
```

### MinMaxScaler

Scales to [0, 1]: x_scaled = (x - x_min) / (x_max - x_min)

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)
```

**Critical rule**: fit scaler on training data ONLY, then transform both train and test. Fitting on test = data leakage.

## Categorical Encoding

### One-Hot Encoding
N categories -> N binary columns. Use for nominal (unordered) categories.
```python
pd.get_dummies(df['col'], drop_first=True)  # drop_first avoids multicollinearity

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(drop='first', sparse_output=False)
```

### Label Encoding
Maps categories to integers. Only for ordinal data (has natural order).
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['encoded'] = le.fit_transform(df['col'])
```

### Target Encoding
Replace category with mean of target for that category. CatBoost does this internally with regularization. High risk of data leakage without proper CV-based encoding.

## Missing Value Imputation

```python
from sklearn.impute import SimpleImputer

# Numerical: median is robust to outliers
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# Categorical: most frequent or constant
imputer_cat = SimpleImputer(strategy='most_frequent')
```

**Pro tip**: create binary indicator `is_missing` before imputing - missingness itself can be informative.

## Feature Selection

### Filter Methods (model-independent)
```python
from sklearn.feature_selection import VarianceThreshold, mutual_info_classif

# Remove near-constant features
sel = VarianceThreshold(threshold=0.01)
X_filtered = sel.fit_transform(X)

# Mutual information (captures non-linear relationships)
mi_scores = mutual_info_classif(X, y)
```

### Wrapper Methods (model-dependent)
```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

selector = RFE(LogisticRegression(), n_features_to_select=10)
X_selected = selector.fit_transform(X, y)
```

### Embedded Methods (built into model)
- **L1/Lasso**: pushes unimportant weights to exactly zero
- **Tree-based importance**: `model.feature_importances_` from Random Forest, CatBoost

## Regularization

Prevents overfitting by penalizing large coefficients.

| Type | Penalty | Effect | When to Use |
|------|---------|--------|-------------|
| L2 (Ridge) | sum(beta_j^2) | Shrinks all, never zero | Multicollinearity |
| L1 (Lasso) | sum(\|beta_j\|) | Pushes some to exactly 0 | Feature selection |
| Elastic Net | L1 + L2 | Combined | Groups of correlated features |

**Why L1 produces zeros**: L1 ball has corners on axes - optimal point frequently at a corner. L2 ball is smooth - tangent point almost never on an axis.

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
ridge = Ridge(alpha=1.0)    # alpha = regularization strength
lasso = Lasso(alpha=0.1)
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
```

## Sklearn Pipelines

Chain preprocessing + model. Prevents data leakage.

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

## Feature Engineering Techniques

- **Domain-based**: use domain knowledge (lat/lon -> distance, date -> day_of_week)
- **Interaction features**: x1 * x2 captures joint effects
- **Polynomial features**: x^2, x^3 for non-linear relationships
- **Aggregation features**: groupby statistics (mean, count, std) of related entities
- **Time-based**: day_of_week, month, hour, is_weekend, days_since_event
- **Text-based**: word count, TF-IDF features, n-grams

```python
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, interaction_only=False)
X_poly = poly.fit_transform(X)
```

## Non-linear Correlation Detection

```python
# phik - detects non-linear AND works with categoricals
import phik
corr_matrix = df.phik_matrix()
df.phik_matrix()['target'].sort_values(ascending=False)
```

Always verify phik findings with pivot tables. Phik shows WHERE to look, pivot tables confirm.

## Gotchas
- **Data leakage** via preprocessing: fit scaler/encoder on test data, or compute target encoding without CV
- **One-hot explosion**: 1000 categories = 1000 features. Use target encoding or embeddings instead
- **Label encoding for nominal**: gives false ordinal relationship (model thinks category 3 > category 1)
- **Polynomial features**: degree=3 with 100 features = millions of features. Use `interaction_only=True` or manually select
- **Feature importance from single tree model is unreliable** - use permutation importance or average over ensemble

## See Also
- [[pandas-eda]] - data exploration before engineering
- [[linear-models]] - models most affected by feature engineering
- [[gradient-boosting]] - models with built-in feature handling
- [[model-evaluation]] - evaluating impact of features on performance
