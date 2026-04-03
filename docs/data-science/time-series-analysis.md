---
title: Time Series Analysis
category: techniques
tags: [data-science, time-series, forecasting, arima, seasonality]
---

# Time Series Analysis

Data ordered by time. Special handling required because observations are NOT independent - temporal patterns (trend, seasonality, autocorrelation) must be modeled explicitly.

## Components of Time Series

- **Trend**: long-term direction (up, down, flat)
- **Seasonality**: repeating patterns at fixed intervals (daily, weekly, yearly)
- **Cyclical**: repeating patterns at non-fixed intervals (business cycles)
- **Residual/Noise**: random variation after removing trend and seasonality

## Stationarity

A time series is stationary if its statistical properties (mean, variance) don't change over time. Most models require stationarity.

**Tests:**
- **ADF test** (Augmented Dickey-Fuller): p < 0.05 -> stationary
- Visual: plot and check for constant mean/variance

**Making stationary:**
- **Differencing**: y_diff = y_t - y_(t-1). Removes linear trend
- **Log transform**: stabilizes variance
- **Seasonal differencing**: y_t - y_(t-period)

## Classical Models

### AR (AutoRegressive)
y_t = c + phi_1 * y_(t-1) + ... + phi_p * y_(t-p) + error

Predict from past values. Order p = number of lags.

### MA (Moving Average)
y_t = c + theta_1 * e_(t-1) + ... + theta_q * e_(t-q) + error

Predict from past errors. Order q = number of error lags.

### ARMA / ARIMA
- **ARMA(p,q)**: AR + MA combined (requires stationarity)
- **ARIMA(p,d,q)**: d = differencing order. Handles non-stationary data
- **SARIMA(p,d,q)(P,D,Q,s)**: + seasonal component with period s

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(y_train, order=(2, 1, 1))  # AR=2, diff=1, MA=1
results = model.fit()
forecast = results.forecast(steps=30)
```

### Exponential Smoothing

Weighted average of past observations with exponentially decreasing weights.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(y_train, trend='add', seasonal='mul', seasonal_periods=12)
results = model.fit()
forecast = results.forecast(12)
```

## Feature Engineering for Time Series

For ML approaches (tree-based, neural networks):

```python
# Lag features
for lag in [1, 7, 14, 30]:
    df[f'lag_{lag}'] = df['value'].shift(lag)

# Rolling statistics
df['rolling_mean_7'] = df['value'].rolling(7).mean()
df['rolling_std_7'] = df['value'].rolling(7).std()

# Calendar features
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
```

## Validation for Time Series

**Never use random train/test split** - temporal order matters. Use time-based split.

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    # train on past, test on future
    X_train, X_test = X[train_idx], X[test_idx]
```

## Gotchas
- Random train/test split = data leakage (future information in training)
- Stationarity is required for ARIMA - always test first
- Seasonal period must be known (domain knowledge or ACF plot)
- Forecasting uncertainty grows with horizon - always provide confidence intervals
- For very long series, LSTMs/transformers can outperform ARIMA, but require much more data

## See Also
- [[rnn-sequences]] - deep learning for sequences
- [[hypothesis-testing]] - testing trend significance
- [[pandas-eda]] - time series manipulation in pandas
- [[feature-engineering]] - time-based feature creation
