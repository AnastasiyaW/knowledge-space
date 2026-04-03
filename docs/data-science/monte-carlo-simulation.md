---
title: Monte Carlo Simulation
category: techniques
tags: [data-science, simulation, monte-carlo, finance, risk]
---

# Monte Carlo Simulation

Estimate outcomes by running thousands of random experiments. When analytical solutions are intractable, simulate. Widely used in finance, risk analysis, and portfolio optimization.

## Core Idea

1. Define a model with random inputs
2. Run many simulations (1000+)
3. Aggregate results for probability estimates

## Stock Price Simulation

Geometric Brownian Motion (GBM):

```python
import numpy as np

def simulate_prices(S0, mu, sigma, days, n_sims):
    """
    S0: initial price, mu: expected daily return
    sigma: daily volatility, days: trading days
    """
    prices = np.zeros((days, n_sims))
    prices[0] = S0
    for t in range(1, days):
        Z = np.random.standard_normal(n_sims)
        prices[t] = prices[t-1] * np.exp(
            (mu - 0.5*sigma**2) + sigma*Z
        )
    return prices

# Historical volatility
returns = df['price'].pct_change().dropna()
volatility = returns.std()
annualized_vol = volatility * np.sqrt(252)  # 252 trading days
```

## Portfolio Optimization

```python
n_sims = 10000
n_assets = len(tickers)
results = np.zeros((3, n_sims))  # return, std, sharpe

for i in range(n_sims):
    weights = np.random.random(n_assets)
    weights /= weights.sum()

    port_return = weights @ daily_returns.mean() * 252
    port_std = np.sqrt(weights @ cov_matrix @ weights) * np.sqrt(252)
    sharpe = port_return / port_std

    results[0, i] = port_return
    results[1, i] = port_std
    results[2, i] = sharpe

# Best Sharpe ratio portfolio
best_idx = results[2].argmax()
```

## Risk Metrics

### Value at Risk (VaR)
Maximum expected loss at given confidence level.

```python
# Historical VaR (95% confidence)
var_95 = np.percentile(returns, 5)  # 5th percentile

# Parametric VaR
var_95 = returns.mean() - 1.645 * returns.std()
```

### Sharpe Ratio
Risk-adjusted return: (return - risk_free_rate) / std_dev

```python
sharpe = (returns.mean() - risk_free_rate) / returns.std()
annualized_sharpe = sharpe * np.sqrt(252)
```

## Practical Tips

- More simulations = more stable estimates. Use 10,000+ for serious analysis
- Vectorize with NumPy - never use Python loops for simulation
- Always set random seed for reproducibility
- Visualize: scatter plot of risk vs return colored by Sharpe ratio
- Business days: 20/month, 252/year in finance

## Applications Beyond Finance

- Sports prediction (simulate tournaments)
- Project timeline estimation (simulate task durations)
- A/B test power analysis
- Bayesian inference (MCMC)
- Physics simulations

## See Also
- [[probability-distributions]] - distributions used in simulation
- [[numpy-fundamentals]] - vectorized random generation
- [[descriptive-statistics]] - analyzing simulation results
