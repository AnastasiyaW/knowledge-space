---
title: Model Evaluation and Validation
category: techniques
tags: [data-science, ml, metrics, cross-validation, evaluation]
---

# Model Evaluation and Validation

Choosing the right metric and validation strategy is as important as choosing the model. Wrong metric = optimizing for the wrong thing. Wrong validation = overestimating performance.

## Regression Metrics

| Metric | Formula | When to Use |
|--------|---------|-------------|
| MAE | mean(\|actual - predicted\|) | Intuitive, in original units |
| MAPE | mean(\|actual - predicted\| / actual) | Need percentage error |
| MSE | mean((actual - predicted)^2) | Penalize large errors more |
| RMSE | sqrt(MSE) | Same units as target, penalizes large errors |
| R^2 | 1 - SS_res/SS_tot | Fraction of variance explained |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
```

**Gotcha**: MAPE breaks when actual values are near zero (division by zero). R^2 can be negative (model worse than predicting mean).

## Classification Metrics

### Confusion Matrix

| | Predicted 0 | Predicted 1 |
|--|------------|------------|
| **Actual 0** | TN | FP |
| **Actual 1** | FN | TP |

```python
from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_true, y_pred)
print(classification_report(y_true, y_pred))
```

### Key Metrics

| Metric | Formula | Optimize When |
|--------|---------|---------------|
| Precision | TP / (TP + FP) | FP costly (spam filter, fraud accusation) |
| Recall | TP / (TP + FN) | FN costly (disease detection, fraud detection) |
| F1 | 2*P*R / (P+R) | Balance precision/recall |
| Accuracy | (TP+TN) / total | **Avoid** with imbalanced classes |

### ROC AUC

Threshold-independent metric. Evaluates ranking quality of model scores.

```python
from sklearn.metrics import roc_auc_score, roc_curve

auc = roc_auc_score(y_true, scores)  # scores, not predictions!
fpr, tpr, thresholds = roc_curve(y_true, scores)

import matplotlib.pyplot as plt
plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.plot([0,1], [0,1], 'k--')  # random baseline
plt.xlabel('FPR'); plt.ylabel('TPR')
plt.legend()
```

**Interpretation**: probability that a random positive has higher score than a random negative. 0.5 = random, 1.0 = perfect.

### Precision-Recall Curve

Better than ROC for highly imbalanced data:

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

prec, rec, thresholds = precision_recall_curve(y_true, scores)
ap = average_precision_score(y_true, scores)
```

### Threshold Selection

Models output scores (probabilities). Converting to binary predictions requires choosing a threshold.

```python
# Business context determines threshold
threshold = 0.3  # lower = higher recall, lower precision
y_pred = (scores >= threshold).astype(int)
```

Higher threshold = fewer but more confident predictions (higher precision, lower recall).

## Ranking Metrics

| Metric | Description |
|--------|-------------|
| precision@k | Fraction of relevant items in top-k |
| mAP@k | Mean average precision across queries |
| nDCG@k | Position-weighted relevance: DCG = sum((2^y_i - 1) / log(i+1)) |

## Cross-Validation

Single train/test split depends on random seed. K-fold gives robust estimates.

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

# Simple K-fold
scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
print(f"Mean AUC: {scores.mean():.3f} +/- {scores.std():.3f}")

# Stratified (preserves class ratio) - use for classification
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='f1')

# Time series: use TimeSeriesSplit (no future leakage)
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
```

### Train / Validation / Test Split

```python
from sklearn.model_selection import train_test_split

# 60/20/20 split
train, test = train_test_split(df, test_size=0.2, random_state=42)
train, val = train_test_split(train, test_size=0.25, random_state=42)
# 0.25 of 0.8 = 0.2
```

- **Train**: fit model
- **Validation**: tune hyperparameters, select features
- **Test**: final evaluation ONCE (never tune on test)

## Bias-Variance Tradeoff

- **High bias** (underfitting): model too simple, misses patterns. Both train and val error high
- **High variance** (overfitting): model too complex, memorizes noise. Train error low, val error high
- **Diagnosing**: large gap between train and val performance = overfitting

**Solutions for overfitting**: regularization, simpler model, more data, early stopping, dropout, cross-validation.

## Gotchas
- **Accuracy trap**: with 99/1 class split, predicting all-zeros gives 99% accuracy
- **Data leakage**: preprocessing fit on full dataset (including test) inflates metrics
- **Test set contamination**: if you tune anything on test set, it's no longer unbiased
- **Class imbalance**: use F1, PR-AUC, or ROC AUC instead of accuracy
- **Metric selection**: optimize the metric that aligns with business goal, not the one that looks best
- **Overfitting to validation**: heavy hyperparameter tuning can overfit to validation set too

## See Also
- [[gradient-boosting]] - primary models to evaluate
- [[linear-models]] - simple baselines for comparison
- [[hypothesis-testing]] - statistical testing of model differences
- [[ds-workflow]] - evaluation in context of full project
