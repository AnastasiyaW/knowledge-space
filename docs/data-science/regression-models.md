---
title: Regression Models
category: ml-algorithms
tags: [regression, linear-regression, polynomial, regularization, sklearn, supervised-learning]
---

# Regression Models

Predict a continuous numerical target from input features. Linear regression is the simplest model and the conceptual foundation for understanding [[neural-network-fundamentals]]. Regularized variants (Ridge, Lasso, ElasticNet) handle multicollinearity and [[feature-engineering]] selection.

## Key Facts

- **Linear regression**: y = w0 + w1*x1 + w2*x2 + ... + wn*xn; minimizes MSE (Mean Squared Error)
- **OLS** (Ordinary Least Squares): closed-form solution w = (X^T X)^(-1) X^T y; requires invertible X^T X
- **Assumptions**: linearity, independence of errors, homoscedasticity (constant error variance), normally distributed residuals
- **R-squared** (coefficient of determination): proportion of variance explained; 0 to 1 for good models, can be negative for bad ones
- **Adjusted R-squared**: penalizes for number of features; use when comparing models with different feature counts
- **Ridge (L2)**: adds lambda * sum(w^2) penalty; shrinks coefficients toward zero but never exactly zero
- **Lasso (L1)**: adds lambda * sum(|w|) penalty; can set coefficients exactly to zero -> feature selection
- **ElasticNet**: combines L1 and L2; l1_ratio controls balance; best when features are correlated
- **Polynomial regression**: add x^2, x^3, ... features to capture non-linear relationships; high degree -> [[cross-validation-and-model-selection]] to avoid overfitting
- **Multicollinearity**: highly correlated features make coefficients unstable; detect with VIF (Variance Inflation Factor) > 5-10
- Gradient-based fitting via [[gradient-descent-and-optimization]] scales better than OLS for large datasets

## Patterns

```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

X = np.random.randn(200, 5)
y = 3*X[:, 0] + 2*X[:, 1] - X[:, 2] + np.random.randn(200) * 0.5

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Basic linear regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print(f"R2: {r2_score(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
print(f"Coefficients: {lr.coef_}")

# Ridge regression (L2 regularization)
ridge = Ridge(alpha=1.0)  # alpha = regularization strength
ridge.fit(X_train, y_train)

# Lasso regression (L1 - feature selection)
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
# Features with coef_ == 0 are effectively removed

# ElasticNet (L1 + L2)
enet = ElasticNet(alpha=0.1, l1_ratio=0.5)
enet.fit(X_train, y_train)

# Polynomial regression pipeline
poly_pipeline = Pipeline([
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('scaler', StandardScaler()),
    ('ridge', Ridge(alpha=1.0))
])
poly_pipeline.fit(X_train, y_train)

# Check multicollinearity (VIF)
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = [variance_inflation_factor(X_train, i) for i in range(X_train.shape[1])]
# VIF > 5-10 indicates problematic collinearity

# Residual analysis
residuals = y_test - y_pred
# Should be: normally distributed, no pattern vs predicted values
```

## Gotchas

- Always scale features before Ridge/Lasso/ElasticNet -- regularization penalizes large coefficients, scale affects magnitude
- Lasso with `alpha` too large sets ALL coefficients to zero; use cross-validation to find optimal alpha
- R-squared can be misleading on non-linear data; always plot residuals
- Linear regression with categorical features requires encoding (OneHotEncoder or similar)
- `sklearn.LinearRegression` has no regularization; for regularized version use Ridge/Lasso with very small alpha, not LinearRegression

## See Also

- [[classification-algorithms]] - logistic regression adapts linear regression for classification
- [[loss-functions-and-regularization]] - detailed L1/L2/ElasticNet mechanics
- [[feature-engineering]] - feature transformations improve linear model performance
- [[cross-validation-and-model-selection]] - finding optimal regularization strength
- sklearn linear models: https://scikit-learn.org/stable/modules/linear_model.html
