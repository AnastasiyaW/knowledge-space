---
title: Classification Algorithms
category: ml-algorithms
tags: [classification, logistic-regression, svm, knn, naive-bayes, sklearn, supervised-learning]
---

# Classification Algorithms

Predict a discrete label (class) for an input sample. Logistic regression, SVM, KNN, and Naive Bayes are foundational classifiers. Understanding their decision boundaries, assumptions, and trade-offs is essential before moving to [[ensemble-methods]] or [[neural-network-fundamentals]].

## Key Facts

- **Logistic regression**: linear model + sigmoid activation; outputs P(y=1|x); decision boundary is a hyperplane
- **Sigmoid function**: sigma(z) = 1 / (1 + e^(-z)); maps any real number to (0, 1)
- **Softmax**: multi-class extension of sigmoid; outputs probability vector summing to 1
- **SVM** (Support Vector Machine): finds maximum-margin hyperplane; support vectors are closest points to boundary
- **Kernel trick**: SVM maps data to higher dimensions implicitly; RBF kernel for non-linear boundaries
- **KNN** (K-Nearest Neighbors): no training phase; classifies by majority vote of k closest neighbors; distance-based
- **Naive Bayes**: applies Bayes' theorem with "naive" conditional independence assumption; fast, works well with text
- **Decision boundary**: logistic regression = linear; SVM + RBF kernel = non-linear; KNN = irregular, data-dependent
- **Multiclass strategies**: One-vs-Rest (OvR) trains C binary classifiers; One-vs-One (OvO) trains C*(C-1)/2 pairs
- For imbalanced classes: use `class_weight='balanced'`, SMOTE oversampling, or adjust threshold
- Compare classifiers using [[model-evaluation-metrics]] beyond accuracy (precision, recall, F1)

## Patterns

```python
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20,
                           n_informative=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features (critical for SVM and KNN)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# Logistic Regression
lr = LogisticRegression(max_iter=1000, C=1.0)  # C = inverse regularization
lr.fit(X_train_s, y_train)
print(classification_report(y_test, lr.predict(X_test_s)))
# Probability output
proba = lr.predict_proba(X_test_s)  # shape (n_samples, n_classes)

# SVM with RBF kernel
svm = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True)
svm.fit(X_train_s, y_train)

# KNN
knn = KNeighborsClassifier(n_neighbors=5, weights='distance', metric='euclidean')
knn.fit(X_train_s, y_train)

# Naive Bayes
nb = GaussianNB()
nb.fit(X_train, y_train)  # no scaling needed for NB

# Handling imbalanced classes
lr_balanced = LogisticRegression(class_weight='balanced', max_iter=1000)
lr_balanced.fit(X_train_s, y_train)

# Custom threshold (instead of default 0.5)
proba = lr.predict_proba(X_test_s)[:, 1]
custom_preds = (proba >= 0.3).astype(int)  # lower threshold -> more positives

# Multiclass: sklearn uses OvR by default for LogisticRegression
from sklearn.datasets import make_classification
X_multi, y_multi = make_classification(n_classes=4, n_informative=10,
                                        n_samples=1000, random_state=42)
lr_multi = LogisticRegression(multi_class='multinomial', max_iter=1000)
lr_multi.fit(X_multi, y_multi)
```

## Gotchas

- SVM and KNN are very sensitive to feature scale; ALWAYS standardize first
- KNN with k=1 memorizes training data (overfits); large k smooths but may underfit; use odd k for binary to avoid ties
- Logistic regression `C` parameter: SMALL C = MORE regularization (inverse of alpha in Ridge)
- SVM's `probability=True` uses Platt scaling (slow, approximate); avoid if you only need hard predictions
- Naive Bayes assumes feature independence -- violated for correlated features but often still works in practice
- Default sklearn metric is accuracy, which is misleading for imbalanced datasets

## See Also

- [[ensemble-methods]] - Random Forest, XGBoost build on decision trees for stronger classification
- [[model-evaluation-metrics]] - precision, recall, F1, ROC-AUC for classifier evaluation
- [[regression-models]] - logistic regression is a classification model despite the name
- [[feature-engineering]] - feature quality directly impacts classifier performance
- sklearn classifiers: https://scikit-learn.org/stable/supervised_learning.html
