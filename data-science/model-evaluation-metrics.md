---
title: Model Evaluation Metrics
category: ml-fundamentals
tags: [metrics, accuracy, precision, recall, f1, roc-auc, rmse, confusion-matrix, sklearn]
---

# Model Evaluation Metrics

Quantify model performance to compare approaches, tune hyperparameters, and decide if a model is production-ready. Different metrics suit different problems: accuracy for balanced classes, F1 for imbalanced, RMSE for regression, ROC-AUC for ranking quality. Closely tied to [[cross-validation-and-model-selection]].

## Key Facts

### Classification Metrics
- **Accuracy**: (TP + TN) / total; misleading for imbalanced classes (99% accuracy on 1% positive class by predicting all negative)
- **Precision**: TP / (TP + FP); "of predicted positives, how many are correct"; minimize false positives (spam filter)
- **Recall (Sensitivity)**: TP / (TP + FN); "of actual positives, how many found"; minimize false negatives (disease detection)
- **F1 score**: harmonic mean of precision and recall; 2*P*R / (P+R); balanced when both matter equally
- **F-beta**: weighted F1; beta > 1 weights recall more; beta < 1 weights precision more
- **ROC curve**: TPR (recall) vs FPR at all thresholds; **AUC** = area under ROC; 0.5 = random, 1.0 = perfect
- **PR curve** (Precision-Recall): better than ROC for imbalanced datasets; AUC-PR is more informative when positives are rare
- **Confusion matrix**: 2x2 (binary) or NxN (multiclass) table of actual vs. predicted; basis for all classification metrics
- **Log loss** (cross-entropy): measures probability calibration; lower is better; penalizes confident wrong predictions heavily

### Regression Metrics
- **MSE** (Mean Squared Error): average of squared differences; penalizes large errors more
- **RMSE**: sqrt(MSE); same units as target; most commonly reported
- **MAE** (Mean Absolute Error): average of absolute differences; robust to outliers
- **R-squared**: 1 - (SS_res / SS_tot); proportion of variance explained; can be negative for bad models
- **MAPE** (Mean Absolute Percentage Error): percentage-based; problematic when actual values are near zero

## Patterns

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve, average_precision_score,
    confusion_matrix, classification_report, log_loss,
    mean_squared_error, mean_absolute_error, r2_score
)
import numpy as np

# Classification metrics
y_true = np.array([0, 0, 1, 1, 1, 0, 1, 0, 1, 1])
y_pred = np.array([0, 1, 1, 1, 0, 0, 1, 0, 0, 1])
y_prob = np.array([0.1, 0.6, 0.9, 0.8, 0.3, 0.2, 0.7, 0.1, 0.4, 0.85])

print(f"Accuracy:  {accuracy_score(y_true, y_pred):.4f}")
print(f"Precision: {precision_score(y_true, y_pred):.4f}")
print(f"Recall:    {recall_score(y_true, y_pred):.4f}")
print(f"F1:        {f1_score(y_true, y_pred):.4f}")
print(f"ROC AUC:   {roc_auc_score(y_true, y_prob):.4f}")
print(f"Log loss:  {log_loss(y_true, y_prob):.4f}")

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)
# [[TN, FP], [FN, TP]]

# Full classification report
print(classification_report(y_true, y_pred))

# ROC curve points for plotting
fpr, tpr, thresholds = roc_curve(y_true, y_prob)

# Precision-Recall curve
prec, rec, thresholds_pr = precision_recall_curve(y_true, y_prob)
ap = average_precision_score(y_true, y_prob)  # AUC-PR

# Multiclass metrics
# precision_score(y_true, y_pred, average='macro')   # unweighted mean per class
# precision_score(y_true, y_pred, average='weighted') # weighted by support
# precision_score(y_true, y_pred, average='micro')    # global TP / (TP + FP)

# Regression metrics
y_true_r = np.array([3.0, 5.5, 2.1, 7.8, 4.3])
y_pred_r = np.array([2.8, 5.0, 2.5, 7.2, 4.8])
print(f"RMSE: {np.sqrt(mean_squared_error(y_true_r, y_pred_r)):.4f}")
print(f"MAE:  {mean_absolute_error(y_true_r, y_pred_r):.4f}")
print(f"R2:   {r2_score(y_true_r, y_pred_r):.4f}")

# Custom scoring for cross-validation
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(rf, X, y, cv=5, scoring='f1')
# Available scoring strings: 'accuracy', 'f1', 'precision', 'recall',
# 'roc_auc', 'neg_mean_squared_error', 'r2', etc.
```

## Gotchas

- `sklearn.metrics.mean_squared_error` returns MSE, not RMSE; wrap with `np.sqrt()` or use `squared=False`
- `roc_auc_score` needs probability scores, not binary predictions; use `model.predict_proba()[:, 1]`
- For multiclass ROC AUC, pass `multi_class='ovr'` or `'ovo'` and use probability matrix
- Accuracy is the WRONG default metric for imbalanced datasets; a model predicting all zeros gets high accuracy
- Cross-validation `scoring='neg_mean_squared_error'` is negative because sklearn maximizes scores; take `-score` for actual MSE
- F1 is undefined when precision and recall are both 0; sklearn returns 0.0 with a warning

## See Also

- [[cross-validation-and-model-selection]] - use metrics within CV to compare models fairly
- [[classification-algorithms]] - each classifier type has different metric strengths
- [[loss-functions-and-regularization]] - loss function during training vs. evaluation metric at test time
- [[hypothesis-testing]] - statistical significance of metric differences
- sklearn metrics: https://scikit-learn.org/stable/modules/model_evaluation.html
