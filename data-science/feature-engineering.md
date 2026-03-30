---
title: Feature Engineering
category: ml-fundamentals
tags: [feature-engineering, encoding, scaling, transformation, missing-values, sklearn, pandas]
---

# Feature Engineering

Transform raw data into features that make ML models work better. The most impactful activity in applied ML -- often more important than algorithm choice. Covers encoding, scaling, handling missing values, creating interaction features, and temporal features. Works hand-in-hand with [[pandas-data-manipulation]].

## Key Facts

- **Numerical scaling**: StandardScaler (zero mean, unit variance), MinMaxScaler (0-1 range), RobustScaler (uses IQR, robust to outliers)
- **Log transform**: reduces right skew; apply to features with long tails (income, prices, counts); use `np.log1p()` for zero-safe
- **Categorical encoding**: OneHotEncoder (creates binary columns per category), OrdinalEncoder (integer labels for ordinal data), TargetEncoder (mean target per category)
- **High-cardinality categoricals**: target encoding or frequency encoding; one-hot creates too many columns
- **Missing values**: SimpleImputer (mean/median/mode), KNNImputer, or indicator column + imputation; NEVER drop rows blindly on large datasets
- **Polynomial features**: PolynomialFeatures creates x^2, x*y interactions; use with [[regression-models]]
- **Binning**: discretize continuous features into buckets; useful for non-linear relationships with linear models
- **Date/time features**: extract year, month, day_of_week, hour, is_weekend, days_since_event
- **Text features**: TF-IDF, CountVectorizer, character n-grams; for deep models: embeddings
- **Feature selection**: filter (correlation, mutual info), wrapper (recursive feature elimination), embedded (Lasso, tree importance)
- Fit transformers on train data ONLY, then `.transform()` on test -- prevents [[cross-validation-and-model-selection]] leakage
- sklearn `Pipeline` + `ColumnTransformer` = best practice for reproducible preprocessing

## Patterns

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    OneHotEncoder, OrdinalEncoder, LabelEncoder,
    PolynomialFeatures
)
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, mutual_info_classif

# Identify feature types
numeric_features = ['age', 'income', 'score']
categorical_features = ['city', 'gender']

# Full preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ]), numeric_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ]), categorical_features)
    ]
)

# Full pipeline with model
from sklearn.ensemble import RandomForestClassifier
full_pipe = Pipeline([
    ('preprocess', preprocessor),
    ('clf', RandomForestClassifier(n_estimators=100))
])
full_pipe.fit(X_train, y_train)

# Log transform for skewed features
df['log_income'] = np.log1p(df['income'])  # log(1 + x), handles zeros

# Date features
df['date'] = pd.to_datetime(df['date_str'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['days_since_start'] = (df['date'] - df['date'].min()).dt.days

# Target encoding (careful of leakage -- use within CV)
from sklearn.preprocessing import TargetEncoder
te = TargetEncoder(smooth=5.0)
# te.fit(X_train[['city']], y_train)

# Feature selection with mutual information
selector = SelectKBest(mutual_info_classif, k=10)
X_selected = selector.fit_transform(X_train, y_train)
selected_mask = selector.get_support()

# Recursive Feature Elimination
from sklearn.feature_selection import RFECV
rfecv = RFECV(estimator=RandomForestClassifier(n_estimators=50),
              step=1, cv=5, scoring='f1')
rfecv.fit(X_train, y_train)
print(f"Optimal features: {rfecv.n_features_}")

# Interaction features
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_interactions = poly.fit_transform(X_train[['feat1', 'feat2']])
```

## Gotchas

- ALWAYS fit scaler/encoder on training data only; `fit_transform(X_train)` then `transform(X_test)` -- fitting on test leaks information
- OneHotEncoder creates k columns for k categories; set `drop='first'` to avoid multicollinearity with linear models
- `LabelEncoder` is for target variable only, NOT for features; use `OrdinalEncoder` for features
- Mean imputation destroys variance; median is more robust; consider KNNImputer for better estimates
- Log transform fails on negative values; use `np.log1p()` for zeros, but negative values need different treatment (e.g., shift)
- Target encoding on full data causes massive leakage; always compute target statistics within cross-validation folds
- `ColumnTransformer` reorders columns; use `remainder='passthrough'` to keep unspecified columns

## See Also

- [[pandas-data-manipulation]] - data wrangling operations that precede feature engineering
- [[regression-models]] - linear models benefit most from feature engineering
- [[ensemble-methods]] - tree models are less sensitive to scaling but benefit from good features
- [[cross-validation-and-model-selection]] - prevent leakage in feature engineering
- sklearn preprocessing: https://scikit-learn.org/stable/modules/preprocessing.html
