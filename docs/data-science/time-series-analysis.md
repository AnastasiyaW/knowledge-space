---
title: Time Series Analysis
category: techniques
tags: [data-science, time-series, forecasting, arima, seasonality, varma, garch, prophet]
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

**SES** (Simple Exponential Smoothing): no trend, no seasonality. Equivalent to EWMA (exponentially weighted moving average). Single smoothing parameter alpha controls decay rate.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing

# Simple Exponential Smoothing
ses_model = SimpleExpSmoothing(y_train).fit(smoothing_level=0.2)
forecast_ses = ses_model.forecast(12)

# Holt-Winters (trend + seasonality)
model = ExponentialSmoothing(y_train, trend='add', seasonal='mul', seasonal_periods=12)
results = model.fit()
forecast = results.forecast(12)
```

**Variants**: SES (level only) -> Holt (+ trend) -> Holt-Winters (+ seasonality). Use `seasonal='add'` for constant seasonal amplitude, `seasonal='mul'` when amplitude grows with level.

### VAR / VARMA (Multivariate)

Vector autoregressive models: multiple correlated time series predicted jointly. Each series depends on its own lags AND lags of all other series.

- Parameters are **matrices** (D x D) instead of scalars, where D = number of time series
- **VAR(p)**: purely autoregressive, most commonly used (VARMA estimation is numerically unstable)
- **VARMA(p,q)**: vector ARMA, adds moving average component
- Data format: T rows x D columns (T time steps, D series)

```python
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.api import VAR

# VAR model (recommended - simpler, more stable)
var_model = VAR(train_df[['series_1', 'series_2']])
results = var_model.fit(maxlags=4)
forecast = results.forecast(train_df[['series_1', 'series_2']].values[-4:], steps=12)

# VARMAX (supports exogenous variables)
model = VARMAX(train_scaled, order=(2, 1))
results = model.fit(disp=False, maxiter=500)
forecast = results.forecast(steps=n_test)
```

**Practical notes**: Always scale multivariate series before fitting (different units/magnitudes). Use ACF/PACF per series as rough guide, but cross-terms matter - grid search over (p,q) is the practical approach. Econometrics datasets (GDP, interest rates, term spreads) are the classic VARMA use case.

### GARCH (Volatility Modeling)

GARCH models time-varying variance (volatility clustering). Essential for financial time series where variance is not constant.

- **ARCH(q)**: variance depends on past squared errors
- **GARCH(p,q)**: variance depends on past squared errors AND past variances
- Standard GARCH(1,1) is the workhorse model

```python
from arch import arch_model

# Scale returns first - GARCH needs values between 1 and 1000
m, s = train_returns.mean(), train_returns.std()
train_scaled = (train_returns - m) / s

# GARCH(1,1)
model = arch_model(train_scaled, vol='GARCH', p=1, q=1)
result = model.fit(update_freq=5)
print(result.summary())

# ARCH(1) - simpler, variance depends only on past errors
arch1 = arch_model(train_scaled, vol='ARCH', p=1)
arch1_result = arch1.fit()

# Forecast variance
forecasts = result.forecast(horizon=5)
variance_forecast = forecasts.variance[-1:]
```

**Gotcha**: The `arch` library warns when input scale is too small. Always standardize first (subtract mean, divide by std). The `vol='ARCH'` parameter must be set explicitly since default is GARCH.

### Prophet (Facebook/Meta)

Decomposable time series model: trend + seasonality + holidays + regressors. Designed for business forecasting with automatic handling of common patterns.

```python
from prophet import Prophet

# Data must have columns: 'ds' (datetime) and 'y' (values)
df_prophet = df[['date', 'value']].rename(columns={'date': 'ds', 'value': 'y'})

# Basic model
m = Prophet()
m.fit(df_prophet)

# Create future dates and predict
future = m.make_future_dataframe(periods=365)  # daily
forecast = m.predict(future)

# Multiplicative seasonality (for series where amplitude grows with level)
m = Prophet(seasonality_mode='multiplicative')

# Monthly data - specify freq
future = m.make_future_dataframe(periods=12, freq='MS')

# Add country holidays
m = Prophet()
m.add_country_holidays(country_name='US')
m.fit(df_prophet)

# Add custom regressor (exogenous variable)
m = Prophet()
m.add_regressor('promo')
m.fit(df_train)
# future df must also contain 'promo' column
```

**Key parameters**: `growth='linear'|'logistic'`, `changepoint_prior_scale` (flexibility of trend changes, default 0.05), `seasonality_prior_scale` (strength of seasonality), `n_changepoints` (default 25).

**Automatic behavior**: disables daily seasonality for daily data, disables daily+weekly for monthly data. Prophet prints messages about disabled components during fit.

### Random Walk

A random walk is: x_t = x_(t-1) + noise. Each value = previous value + random step. Special case of ARIMA(0,1,0).

**Random Walk Hypothesis**: stock prices follow a random walk, making them fundamentally unpredictable. Implications:
- Best forecast for tomorrow's price = today's price
- Returns (price differences) are unpredictable, not prices themselves
- Use **returns** (or log returns) as features for ML, not raw prices

**Extrapolation problem**: most ML models (SVM, random forest, neural nets) cannot extrapolate beyond training data range. If training prices are 100-200, model cannot predict 250. This is why returns (stationary, bounded range) work better than raw prices for ML.

### Auto ARIMA

Automated order selection via grid search over (p,d,q) combinations. Eliminates manual ACF/PACF interpretation by testing candidate models and selecting the best by AIC/BIC.

```python
from pmdarima import auto_arima

# Basic usage
model = auto_arima(y_train, seasonal=True, m=12,
                   stepwise=True, suppress_warnings=True,
                   trace=True)  # trace=True shows all models tested
print(model.summary())
forecast = model.predict(n_periods=12)
```

**Log transform trick**: if the series has increasing variance (amplitude grows with level), apply log transform before fitting. This often improves accuracy with the same ARIMA order:

```python
import numpy as np

df['log_values'] = np.log(df['values'])
model_log = auto_arima(df['log_values'][:train_end],
                       seasonal=True, m=12, trace=True,
                       suppress_warnings=True)
forecast_log = model_log.predict(n_periods=n_test)
forecast_original = np.exp(forecast_log)  # reverse the transform
```

**Key arguments**:

- `trace=True`: prints all candidate models and their AIC scores - useful for understanding the search
- `suppress_warnings=True`: silences convergence warnings from weak candidates
- `m`: seasonal period (12 for monthly, 7 for daily with weekly pattern, 52 for weekly with yearly)
- `stepwise=True`: faster heuristic search (default). Set `False` for exhaustive grid search (slower, occasionally better)
- `seasonal=True/False`: whether to include seasonal ARIMA component (P,D,Q)

**pmdarima must be installed separately** - it is not included in standard Python distributions or most cloud notebook environments. Install via `pip install pmdarima`.

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

### Walk-Forward Validation

Most rigorous time series validation. Train on expanding window, forecast next h steps, slide forward, repeat. Simulates real-world deployment where model is periodically retrained.

```python
from itertools import product

h = 12           # forecast horizon
n_steps = 10     # number of walk-forward steps

results = []
for i in range(n_steps):
    train_end = len(series) - h - n_steps + i + 1
    train = series[:train_end]
    test = series[train_end:train_end + h]

    model = ExponentialSmoothing(train, trend='add',
                                seasonal='mul', seasonal_periods=12,
                                use_boxcox=True).fit()
    pred = model.forecast(h)
    error = np.mean(np.abs(test - pred))
    results.append(error)

avg_mae = np.mean(results)
```

Combine with grid search over model parameters (trend type, seasonality type, Box-Cox) using `itertools.product` to find best configuration across all walk-forward windows.

**Gotcha**: statsmodels `use_boxcox` parameter accepts `True`, `False`, or a float (lambda value). The string `'log'` appears in some docs but raises an error - use `0` instead (lambda=0 is the log transform).

## Gotchas
- Random train/test split = data leakage (future information in training)
- Stationarity is required for ARIMA - always test first
- Seasonal period must be known (domain knowledge or ACF plot)
- Forecasting uncertainty grows with horizon - always provide confidence intervals
- For very long series, LSTMs/transformers can outperform ARIMA, but require much more data
- **VARMA fitting is slow and unstable** - for most multivariate cases, use VAR (no MA part) or go directly to ML/DL approaches
- **GARCH requires scaled input** - values between 1-1000, always standardize first
- **Prophet disables sub-frequency seasonality automatically** - monthly data cannot capture daily/weekly patterns, this is expected
- **Econometrics vs ML validation** - traditional econometrics often skips train/test splits and forecasts beyond available data. Always use proper out-of-sample evaluation
- **Prophet on stock prices** is a common mistake - Prophet is designed for business metrics with strong seasonality (sales, traffic), not for financial instruments that follow random walks. Stock prices lack the stable seasonal patterns Prophet relies on, leading to wildly inaccurate forecasts
- **Auto ARIMA on stocks** similarly produces poor results. The random walk hypothesis means the best forecast is "tomorrow's price = today's price" - any model that beats this consistently on out-of-sample data should be scrutinized for data leakage
- **ACF/PACF for multivariate series** - per-series ACF/PACF ignores cross-correlations; use as rough guide only, then grid search over (p,q)
- **statsmodels `use_boxcox='log'` is broken** - use `0` (lambda=0 = log transform) instead

## See Also
- [[rnn-sequences]] - deep learning for sequences
- [[cnn-computer-vision]] - CNNs applied to time series classification
- [[hypothesis-testing]] - testing trend significance
- [[pandas-eda]] - time series manipulation in pandas
- [[feature-engineering]] - time-based feature creation
- [[model-evaluation]] - walk-forward validation details
- [[neural-networks]] - ANNs for time series forecasting
