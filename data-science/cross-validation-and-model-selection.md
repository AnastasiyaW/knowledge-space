---
title: Cross-Validation and Model Selection
category: ml-fundamentals
tags: [cross-validation, hyperparameter-tuning, grid-search, overfitting, underfitting, sklearn]
---

# Cross-Validation and Model Selection

Systematically evaluate and compare models, tune hyperparameters, and detect overfitting. Cross-validation provides reliable performance estimates by training and testing on different data splits. Proper CV prevents information leakage and ensures [[model-evaluation-metrics]] are trustworthy.

## Key Facts

- **Train/test split**: holdout 20-30% for testing; simple but high variance with small datasets
- **K-Fold CV**: split data into k folds; train on k-1, test on 1; repeat k times; average scores; k=5 or k=10 is typical
- **Stratified K-Fold**: maintains class proportions in each fold; use for classification (especially imbalanced)
- **Leave-One-Out (LOO)**: k = n; maximum use of data; expensive; high variance
- **Time Series Split**: expanding window; train on past, test on future; never look ahead
- **Overfitting**: model memorizes training data, performs poorly on new data; high train score, low test score
- **Underfitting**: model too simple to capture patterns; low train AND test score
- **Bias-variance tradeoff**: simple model = high bias, low variance; complex model = low bias, high variance; goal is the sweet spot
- **Grid Search**: exhaustive search over hyperparameter combinations; exponential cost
- **Random Search**: sample random combinations; often finds good params faster than grid search
- **Bayesian optimization**: Optuna, scikit-optimize; models objective function to search efficiently
- **Nested CV**: outer loop for model evaluation, inner loop for hyperparameter tuning; unbiased estimate
- Data leakage: fitting transformers on full data before splitting inflates metrics

## Patterns

```python
from sklearn.model_selection import (
    train_test_split, cross_val_score, StratifiedKFold,
    GridSearchCV, RandomizedSearchCV, TimeSeriesSplit
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Basic train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# K-Fold cross-validation
scores = cross_val_score(
    RandomForestClassifier(n_estimators=100),
    X, y, cv=5, scoring='f1'
)
print(f"F1: {scores.mean():.4f} +/- {scores.std():.4f}")

# Stratified K-Fold (explicit)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(X, y):
    X_train_fold, X_val_fold = X[train_idx], X[val_idx]
    y_train_fold, y_val_fold = y[train_idx], y[val_idx]

# Grid Search with Pipeline (prevents leakage)
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(random_state=42))
])
param_grid = {
    'clf__n_estimators': [100, 200, 300],
    'clf__max_depth': [5, 10, None],
    'clf__min_samples_leaf': [1, 5, 10]
}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)
print(f"Best params: {grid.best_params_}")
print(f"Best CV F1:  {grid.best_score_:.4f}")
print(f"Test F1:     {grid.score(X_test, y_test):.4f}")

# Random Search (faster for large param spaces)
from scipy.stats import randint, uniform
param_distributions = {
    'clf__n_estimators': randint(50, 500),
    'clf__max_depth': randint(3, 20),
    'clf__min_samples_leaf': randint(1, 20)
}
random_search = RandomizedSearchCV(
    pipe, param_distributions, n_iter=50, cv=5,
    scoring='f1', n_jobs=-1, random_state=42
)
random_search.fit(X_train, y_train)

# Optuna (Bayesian optimization)
# import optuna
# def objective(trial):
#     n_est = trial.suggest_int('n_estimators', 50, 500)
#     depth = trial.suggest_int('max_depth', 3, 20)
#     model = RandomForestClassifier(n_estimators=n_est, max_depth=depth)
#     score = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
#     return score.mean()
# study = optuna.create_study(direction='maximize')
# study.optimize(objective, n_trials=100)

# Time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X_time):
    pass  # train_idx always before test_idx

# Learning curve (detect overfit/underfit)
from sklearn.model_selection import learning_curve
train_sizes, train_scores, val_scores = learning_curve(
    pipe, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10), scoring='f1'
)
# Plot: if train >> val -> overfitting; if both low -> underfitting
```

## Gotchas

- NEVER use test set for hyperparameter tuning; use validation set or inner CV
- `GridSearchCV` with `refit=True` (default) refits best model on entire training set after search
- `cross_val_score` returns scores per fold; report `mean +/- std`, not just mean
- Preprocessing MUST be inside the Pipeline for CV to prevent leakage; fitting scaler on full data before split leaks test statistics
- Random search with 60 iterations has 95% chance of finding a combination in the top 5% of the search space (Bergstra & Bengio, 2012)
- For time series: NEVER shuffle data; use `TimeSeriesSplit` or manual expanding window

## See Also

- [[model-evaluation-metrics]] - which scoring metric to optimize during search
- [[feature-engineering]] - feature transformations must be inside CV pipeline
- [[ensemble-methods]] - hyperparameter tuning is especially important for boosting methods
- [[regression-models]] - finding optimal regularization strength (alpha/C)
- sklearn model selection: https://scikit-learn.org/stable/model_selection.html
