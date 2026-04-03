---
title: Ensemble Methods
category: ml-algorithms
tags: [ensemble, random-forest, gradient-boosting, xgboost, bagging, stacking, sklearn]
---

# Ensemble Methods

Combine multiple weak learners into a strong predictor. Bagging (Random Forest) reduces variance; boosting (XGBoost, LightGBM) reduces bias. Ensembles consistently win structured/tabular data competitions and remain the default choice before trying [[neural-network-fundamentals]] on tabular data.

## Key Facts

- **Bagging** (Bootstrap Aggregating): train models on random subsets of data with replacement; average predictions
- **Random Forest**: bagging of decision trees + random feature subsets at each split; reduces correlation between trees
- **Boosting**: train models sequentially, each correcting errors of previous; additive model
- **Gradient Boosting**: each new tree fits the negative gradient of the loss function (residuals for MSE)
- **XGBoost**: optimized gradient boosting with L1/L2 regularization, column sampling, missing value handling
- **LightGBM**: histogram-based splitting (faster), leaf-wise growth (vs. level-wise), handles categoricals natively
- **CatBoost**: handles categorical features with ordered target encoding; less prone to overfitting on small data
- **Stacking**: train a meta-model on predictions of base models; use out-of-fold predictions to avoid leakage
- **Feature importance**: Random Forest uses impurity decrease or permutation importance; boosting uses split gain
- Key hyperparameters: `n_estimators` (number of trees), `max_depth`, `learning_rate` (boosting), `min_samples_leaf`
- Random Forest: more trees = better (no overfitting from more trees); boosting: too many trees -> overfitting
- For tabular data, gradient boosting > neural networks in most benchmarks (as of 2024 research)

## Patterns

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

# Random Forest
rf = RandomForestClassifier(
    n_estimators=200,       # more trees = better, diminishing returns after ~200
    max_depth=None,         # None = fully grown trees
    min_samples_leaf=5,     # regularization
    max_features='sqrt',    # sqrt(n_features) at each split (default for classification)
    n_jobs=-1,              # use all CPU cores
    random_state=42
)
rf.fit(X_train, y_train)

# Feature importance
importances = rf.feature_importances_
sorted_idx = np.argsort(importances)[::-1]

# XGBoost
from xgboost import XGBClassifier
xgb = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,      # aka eta; smaller = more trees needed but better generalization
    subsample=0.8,          # row sampling
    colsample_bytree=0.8,   # column sampling
    reg_alpha=0.01,         # L1 regularization
    reg_lambda=1.0,         # L2 regularization
    eval_metric='logloss',
    early_stopping_rounds=20,
    random_state=42
)
xgb.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

# LightGBM
from lightgbm import LGBMClassifier
lgbm = LGBMClassifier(
    n_estimators=300,
    num_leaves=31,          # leaf-wise growth; max leaves per tree
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    verbose=-1
)
lgbm.fit(X_train, y_train)

# Stacking ensemble
from sklearn.linear_model import LogisticRegression
stacking = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('xgb', XGBClassifier(n_estimators=100, eval_metric='logloss')),
    ],
    final_estimator=LogisticRegression(),
    cv=5  # out-of-fold predictions for meta-learner
)
stacking.fit(X_train, y_train)

# Cross-validated performance comparison
for name, model in [('RF', rf), ('XGB', xgb), ('LGBM', lgbm)]:
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    print(f"{name}: {scores.mean():.4f} +/- {scores.std():.4f}")
```

## Gotchas

- Random Forest `max_features='sqrt'` for classification, `'auto'` (all features) for regression by default
- XGBoost `early_stopping_rounds` requires `eval_set`; without it, no early stopping happens
- LightGBM `num_leaves` > 2^max_depth causes overfitting; keep num_leaves <= 2^max_depth
- Feature importance from tree models is biased toward high-cardinality features; use permutation importance for reliable ranking
- Stacking: MUST use cross-validated predictions for meta-learner training to prevent data leakage
- Gradient boosting with `learning_rate=1.0` often overfits; start with 0.01-0.1 and increase n_estimators

## See Also

- [[classification-algorithms]] - base classifiers that ensembles improve upon
- [[cross-validation-and-model-selection]] - hyperparameter tuning for ensemble models
- [[feature-engineering]] - ensembles handle raw features better but still benefit from engineering
- [[model-evaluation-metrics]] - comparing ensemble vs. single model performance
- XGBoost docs: https://xgboost.readthedocs.io/en/stable/
- LightGBM docs: https://lightgbm.readthedocs.io/en/stable/
