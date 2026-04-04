---
title: Handling Imbalanced Data
category: concepts
tags: [data-science, class-imbalance, smote, oversampling, undersampling]
---

# Handling Imbalanced Data

When one class dominates the dataset (e.g., 99% negative, 1% positive), standard classifiers become biased toward the majority class. Fraud detection, medical diagnosis, defect detection - all suffer from this. A model predicting "always negative" gets 99% accuracy but is useless.

## Measuring the Problem

```python
import pandas as pd

# Check imbalance ratio
print(y.value_counts(normalize=True))
# 0    0.985
# 1    0.015  <- severe imbalance

imbalance_ratio = y.value_counts()[0] / y.value_counts()[1]
# > 10:1 = moderate, > 100:1 = severe
```

**Key rule**: never use accuracy as the metric for imbalanced problems. Use precision, recall, F1, AUROC, or AUPRC instead.

## Data-Level Methods

### Random Oversampling / Undersampling

```python
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

# Oversample minority to match majority
ros = RandomOverSampler(random_state=42)
X_res, y_res = ros.fit_resample(X_train, y_train)

# Undersample majority to match minority
rus = RandomUnderSampler(random_state=42)
X_res, y_res = rus.fit_resample(X_train, y_train)
```

- Oversampling: risk of overfitting (duplicated minority samples)
- Undersampling: loses information from majority class

### SMOTE (Synthetic Minority Oversampling)

Creates synthetic samples by interpolating between existing minority points and their k-nearest neighbors.

```python
from imblearn.over_sampling import SMOTE, BorderlineSMOTE, ADASYN

# Basic SMOTE
smote = SMOTE(sampling_strategy='auto', k_neighbors=5, random_state=42)
X_res, y_res = smote.fit_resample(X_train, y_train)

# Borderline-SMOTE: only synthesize near decision boundary
bl_smote = BorderlineSMOTE(kind='borderline-1', random_state=42)

# ADASYN: adaptively generate more samples in harder regions
adasyn = ADASYN(random_state=42)
```

### SMOTE + Tomek Links (Combined)

Oversample minority then clean noisy majority samples near the boundary:

```python
from imblearn.combine import SMOTETomek

smt = SMOTETomek(random_state=42)
X_res, y_res = smt.fit_resample(X_train, y_train)
```

## Algorithm-Level Methods

### Class Weights

Most classifiers support `class_weight` parameter. Penalizes misclassification of minority class more heavily.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Automatic weight inversely proportional to class frequency
rf = RandomForestClassifier(class_weight='balanced', random_state=42)

# Manual weights
lr = LogisticRegression(class_weight={0: 1, 1: 50})

# CatBoost / XGBoost
import xgboost as xgb
model = xgb.XGBClassifier(scale_pos_weight=imbalance_ratio)
```

### Focal Loss

Down-weights easy (well-classified) examples, focuses on hard ones:

```python
import torch
import torch.nn.functional as F

def focal_loss(logits, targets, alpha=0.25, gamma=2.0):
    bce = F.binary_cross_entropy_with_logits(logits, targets, reduction='none')
    pt = torch.exp(-bce)  # probability of correct class
    loss = alpha * (1 - pt) ** gamma * bce
    return loss.mean()
```

gamma=0 is standard cross-entropy. gamma=2 is typical starting point.

### Cost-Sensitive Learning

Assign different misclassification costs. False negative (missing fraud) may cost 1000x more than false positive (flagging legitimate transaction).

```python
# Custom scoring with business costs
def business_cost(y_true, y_pred):
    fn_cost = 1000  # missed fraud
    fp_cost = 10    # false alarm
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    return fn * fn_cost + fp * fp_cost
```

## Threshold Tuning

Default threshold 0.5 is almost never optimal for imbalanced data.

```python
from sklearn.metrics import precision_recall_curve

probas = model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, probas)

# Find threshold for target recall (e.g., catch 90% of fraud)
target_recall = 0.90
idx = np.argmin(np.abs(recalls - target_recall))
optimal_threshold = thresholds[idx]

y_pred = (probas >= optimal_threshold).astype(int)
```

## Evaluation Strategy

- **Stratified K-Fold**: preserves class distribution in each fold
- **AUPRC over AUROC**: AUPRC is more informative when positive class is rare
- **Confusion matrix**: always inspect raw TP/FP/TN/FN counts

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import average_precision_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
ap_scores = []
for train_idx, val_idx in skf.split(X, y):
    model.fit(X[train_idx], y[train_idx])
    probas = model.predict_proba(X[val_idx])[:, 1]
    ap_scores.append(average_precision_score(y[val_idx], probas))
```

## Gotchas

- **Never SMOTE the test set**: apply resampling only to training data inside the cross-validation loop. SMOTE on full data before splitting causes data leakage - synthetic test points are interpolations of training points, giving inflated metrics
- **SMOTE on high-dimensional sparse data fails**: SMOTE interpolates in feature space - for text (TF-IDF) or one-hot encoded categoricals, interpolated points are meaningless. Use class weights or random oversampling instead
- **Imbalance ratio changes in production**: if training data has 1% fraud but production sees 0.01%, threshold and class weights need recalibration. Monitor class distribution in incoming data

## See Also

- [[model-evaluation]]
- [[feature-engineering]]
- [[gradient-boosting]]
