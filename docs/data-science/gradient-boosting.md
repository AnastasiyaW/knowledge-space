---
title: Gradient Boosting and Tree-Based Models
category: models
tags: [data-science, ml, catboost, xgboost, lightgbm, random-forest, ensemble]
---

# Gradient Boosting and Tree-Based Models

Gradient boosting is the dominant algorithm for tabular data. CatBoost, LightGBM, and XGBoost are implementations of the same idea. Tree-based models handle mixed data types, non-linear relationships, and interactions without manual feature engineering.

## Decision Trees

Base building block. Recursively split data on feature thresholds to minimize impurity.

**Splitting criteria:**
- **Gini impurity**: sum(p_i * (1 - p_i)). Measures probability of misclassification
- **Entropy**: -sum(p_i * log(p_i)). Information theory measure of disorder
- **MSE** (regression): variance within each split

**Pros**: interpretable, handles mixed types, no scaling needed.
**Cons**: high variance, prone to overfitting, unstable (small data changes -> different tree).

## Random Forest

Ensemble of decision trees. Each tree trained on bootstrap sample with random feature subset.

```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train, y_train)
rf.feature_importances_  # built-in importance scores
```

- **Bagging** reduces variance by averaging decorrelated predictions
- Feature importance: decrease in impurity when splitting on feature
- Embarrassingly parallel - each tree trains independently

## Gradient Boosting

Sequentially build trees, each correcting errors of previous ones.

**Idea**: fit tree to residuals (errors) of current model, add it with a small learning rate.

### CatBoost

Best out-of-box performance. Handles categoricals natively.

```python
from catboost import CatBoostRegressor, CatBoostClassifier

model = CatBoostRegressor(cat_features=['transmission', 'fuel_type'])
model.fit(
    train[features], train[target],
    eval_set=(val[features], val[target]),
    verbose=100
)

# Predictions
y_pred = model.predict(test[features])

# Classification: get probabilities
model = CatBoostClassifier(cat_features=cat_features)
model.fit(train[features], train[target],
          eval_set=(val[features], val[target]))
scores = model.predict_proba(test[features])[:, 1]

# Feature importance
model.get_feature_importance(prettified=True)
```

**Validation set is mandatory**: CatBoost trains iteratively. Without validation, it memorizes training data. Early stopping halts at validation error minimum.

### CatBoost Cross-Validation

```python
from catboost import cv, Pool

cv_data = cv(
    pool=Pool(X, y, cat_features=cat_features),
    params={'loss_function': 'Logloss', 'eval_metric': 'AUC'},
    fold_count=5, shuffle=True, stratified=True,
    partition_random_seed=42, verbose=False
)
best_iter = cv_data['test-AUC-mean'].idxmax()
```

**Workflow**: CV to find optimal iterations -> train final model on full train+val with that count -> evaluate on test.

### XGBoost

```python
import xgboost as xgb
model = xgb.XGBClassifier(
    n_estimators=500, max_depth=6, learning_rate=0.1,
    subsample=0.8, colsample_bytree=0.8,
    early_stopping_rounds=50, eval_metric='auc'
)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=50)
```

### LightGBM

Fastest for large datasets. Leaf-wise growth (vs level-wise).

```python
import lightgbm as lgb
model = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=31)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)],
          callbacks=[lgb.early_stopping(50)])
```

## Key Hyperparameters

| Parameter | Effect | Typical Range |
|-----------|--------|---------------|
| n_estimators / iterations | Number of trees | 100-5000 |
| learning_rate | Step size per tree | 0.01-0.3 |
| max_depth | Tree depth | 3-10 |
| subsample | Fraction of rows per tree | 0.5-1.0 |
| colsample_bytree | Fraction of features per tree | 0.5-1.0 |
| min_child_weight | Minimum samples in leaf | 1-100 |
| reg_lambda (L2) | L2 regularization | 0-10 |
| reg_alpha (L1) | L1 regularization | 0-10 |

**Rule of thumb**: lower learning_rate + more estimators = better but slower. Start with defaults, tune learning_rate and max_depth first.

## Handling Imbalanced Classes

```python
# CatBoost
model = CatBoostClassifier(scale_pos_weight=neg_count/pos_count)

# XGBoost
model = xgb.XGBClassifier(scale_pos_weight=neg_count/pos_count)

# Or: tune threshold on validation set
```

## Comparison

| Aspect | CatBoost | XGBoost | LightGBM | Random Forest |
|--------|----------|---------|----------|---------------|
| Default performance | Best | Good | Good | Good |
| Categorical handling | Native | Manual encoding | Native | Manual encoding |
| Speed | Moderate | Moderate | Fastest | Fast (parallel) |
| Overfitting risk | Low | Moderate | Moderate | Low |
| GPU support | Yes | Yes | Yes | No |

## Gotchas
- **Don't use accuracy** on imbalanced datasets - a model predicting all-zeros gets 80% accuracy with 80/20 split
- CatBoost with no eval_set will overfit silently - always provide validation
- Feature importance varies across runs and methods - use permutation importance for reliability
- XGBoost requires manual one-hot encoding for categoricals (unless using `enable_categorical=True`)
- Start simple (defaults) before hyperparameter tuning - tuning doesn't compensate for bad features

## See Also
- [[model-evaluation]] - metrics for model comparison
- [[feature-engineering]] - less critical for trees but still valuable
- [[linear-models]] - simpler alternative, useful baseline
- [[neural-networks]] - when tabular models aren't enough
