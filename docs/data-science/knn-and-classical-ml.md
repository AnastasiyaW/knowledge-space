---
title: KNN and Classical ML Algorithms
category: models
tags: [data-science, ml, knn, svm, naive-bayes, decision-tree]
---

# KNN and Classical ML Algorithms

Classical ML algorithms beyond linear models and gradient boosting. Important for understanding the algorithm landscape and choosing appropriate tools.

## K-Nearest Neighbors (KNN)

Classify by majority vote of k nearest neighbors. No training phase - predictions computed at query time.

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
```

**Distance metrics:**
- Euclidean: ||x-y||_2 = sqrt(sum((x_i - y_i)^2))
- Manhattan: ||x-y||_1 = sum(|x_i - y_i|)
- Minkowski: ||x-y||_p (generalization)

**Choosing k:**
- k too small: overfitting (sensitive to noise)
- k too large: underfitting (too smooth)
- Use cross-validation to select

**Curse of dimensionality**: in high dimensions, all points become roughly equidistant. Requires dimensionality reduction (PCA) or feature selection.

**Pros**: simple, no assumptions about data distribution, works for multi-class.
**Cons**: slow at prediction time (O(n) per query), requires feature scaling, fails in high dimensions.

## Support Vector Machines (SVM)

Find the hyperplane that maximizes margin between classes.

```python
from sklearn.svm import SVC, SVR

svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train, y_train)
```

**Kernel trick**: project data to higher dimensions where it becomes linearly separable.
- Linear: no transformation
- RBF (Gaussian): creates smooth decision boundaries
- Polynomial: degree-based non-linearity

**C parameter**: trade-off between margin width and classification errors. High C = narrow margin, fewer errors on training data.

**Pros**: effective in high dimensions, works well with clear margin of separation.
**Cons**: slow for large datasets, doesn't scale well beyond ~10K samples, no probability output by default.

## Decision Trees (Standalone)

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=10)
dt.fit(X_train, y_train)

# Visualization
import matplotlib.pyplot as plt
plt.figure(figsize=(20, 10))
plot_tree(dt, feature_names=features, class_names=['No', 'Yes'], filled=True)
plt.show()
```

**Splitting criteria**: Gini impurity = sum(p_i * (1 - p_i)), Entropy = -sum(p_i * log(p_i))

**Pros**: interpretable (can visualize), handles mixed types, no scaling needed.
**Cons**: high variance (unstable), prone to overfitting. Use Random Forest or gradient boosting instead.

## Algorithm Selection Guide

| Situation | Recommended |
|-----------|-------------|
| Tabular, any size | Gradient boosting (CatBoost) |
| Small data, need interpretability | Logistic regression, Decision tree |
| Text classification, small data | Naive Bayes, TF-IDF + LogReg |
| High-dimensional sparse data | SVM, Logistic with L1 |
| Need probabilities | Logistic regression, CatBoost |
| Images/text/audio | Deep learning |
| Baseline | Mean/mode prediction, then LogReg |

## Gotchas
- KNN requires standardized features (Euclidean distance is scale-dependent)
- SVM is essentially deprecated for tabular data - gradient boosting dominates
- Single decision tree should never be used alone - always use ensemble (RF, GB)
- Always compare to a simple baseline before using complex models
- "No free lunch" theorem: no algorithm is best for ALL problems

## See Also
- [[gradient-boosting]] - dominant approach for tabular data
- [[linear-models]] - logistic regression as baseline
- [[unsupervised-learning]] - KNN for anomaly detection
- [[feature-engineering]] - preprocessing for distance-based models
