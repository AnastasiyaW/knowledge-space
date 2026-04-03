---
title: Linear Models and Gradient Descent
category: models
tags: [data-science, ml, linear-regression, logistic-regression, gradient-descent]
---

# Linear Models and Gradient Descent

Linear models are the foundation of ML. Simple, interpretable, and surprisingly effective as baselines. Understanding gradient descent is essential - it's how most ML models learn.

## Linear Regression

Predict continuous target as weighted sum of features: y = w0 + w1*x1 + w2*x2 + ... + wn*xn

**Matrix form**: y = Xw where X includes a column of 1s for intercept.

**Closed-form solution (OLS)**: w = (X^T X)^(-1) X^T y

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(model.coef_, model.intercept_)
```

### With statsmodels (for inference)

```python
import statsmodels.api as sm
X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()
model.summary()  # coefficients, t-stats, p-values, R^2, confidence intervals
```

### Five OLS Assumptions
1. Linear relationship between features and target
2. Normally distributed errors with zero mean
3. Homoscedasticity (constant error variance)
4. Independent errors
5. Correct feature specification (no missing/redundant features)

## Logistic Regression

Binary classification. Outputs probability via sigmoid: P(y=1|x) = 1 / (1 + exp(-w^T x))

**Loss**: Binary Cross-Entropy = -sum[y_i * log(p_i) + (1-y_i) * log(1-p_i)]

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]  # P(class=1)
```

**Gradient**: d(Loss)/dw = X^T(p - y) - elegant because sigmoid derivative sigma'(z) = sigma(z)(1 - sigma(z)).

## Gradient Descent

Iterative optimization: w_new = w_old - lr * gradient(Loss, w)

### Variants

| Variant | Gradient Computed On | Tradeoff |
|---------|---------------------|----------|
| Batch GD | Full dataset | Stable but slow |
| Stochastic GD (SGD) | Single sample | Fast but noisy |
| Mini-batch GD | Small batch (32-256) | Best of both |

### Learning Rate

- Too high: diverges (loss oscillates or increases)
- Too low: converges very slowly
- Just right: smooth decrease in loss

### Momentum

Accelerates through narrow valleys: v_t = beta * v_(t-1) + gradient; w -= lr * v_t

### Convergence

For convex functions (like linear regression loss): GD converges to global minimum.
For non-convex (neural networks): converges to local minimum - often sufficient in practice.

## Regularization

| Type | Penalty | sklearn Class |
|------|---------|---------------|
| L2 (Ridge) | alpha * sum(w_j^2) | `Ridge(alpha=1.0)` |
| L1 (Lasso) | alpha * sum(\|w_j\|) | `Lasso(alpha=0.1)` |
| Elastic Net | alpha * [ratio * L1 + (1-ratio) * L2] | `ElasticNet(alpha=0.1, l1_ratio=0.5)` |

- alpha = 0: no regularization
- alpha -> inf: all coefficients -> 0 (underfitting)
- Choose alpha via cross-validation

## Econometrics vs ML Perspective

- **Econometrics**: interpretability, causal relationships, coefficient significance (p-values)
- **ML**: prediction accuracy, doesn't care about individual coefficients
- Linear models serve both: interpretable AND predictive baseline

## Patterns

### Polynomial Regression
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('scaler', StandardScaler()),
    ('model', Ridge(alpha=1.0))
])
pipe.fit(X_train, y_train)
```

### Regularization Selection
```python
from sklearn.linear_model import RidgeCV, LassoCV
ridge = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0], cv=5)
ridge.fit(X_train, y_train)
print(f"Best alpha: {ridge.alpha_}")
```

## Gotchas
- Linear regression requires feature scaling for gradient descent (closed-form doesn't need it, but sklearn uses iterative methods for Lasso/Elastic Net)
- Multicollinearity inflates coefficient variance - use Ridge or drop correlated features
- Logistic regression is a **linear** classifier - decision boundary is always a hyperplane
- Don't interpret Lasso coefficients as "importance" when features are correlated - it arbitrarily picks one
- R^2 can be negative (model worse than predicting mean)

## See Also
- [[feature-engineering]] - preprocessing critical for linear models
- [[model-evaluation]] - metrics for regression and classification
- [[gradient-boosting]] - when linear models aren't enough
- [[math-for-ml]] - calculus foundations for gradient descent
