---
title: Financial Data Science
category: applications
tags: [data-science, finance, portfolio, derivatives, risk]
---

# Financial Data Science

Applying data science methods to financial markets. Covers portfolio theory, risk metrics, derivatives basics, and quantitative analysis patterns.

## Portfolio Theory

### Key Metrics
- **Expected return**: weighted average of asset returns
- **Portfolio volatility**: sqrt(w^T * Cov * w) where w = weight vector
- **Sharpe ratio**: (return - risk_free_rate) / volatility
- **Beta**: sensitivity to market movements

### Efficient Frontier
Set of portfolios maximizing return for given risk level. Found via Monte Carlo simulation or quadratic programming.

```python
# Monte Carlo portfolio optimization
port_return = weights @ daily_returns.mean() * 252
port_vol = np.sqrt(weights @ cov_matrix @ weights) * np.sqrt(252)
sharpe = port_return / port_vol
```

## Financial Derivatives

### Options
- **Call**: right to buy at strike price. Payoff = max(0, spot - strike)
- **Put**: right to sell at strike price. Payoff = max(0, strike - spot)
- **Premium**: price paid for the option

### Forwards/Futures
Lock price for future delivery. Mark-to-market: daily P&L based on spot vs contract price.

## Risk Metrics

### Value at Risk (VaR)
Maximum expected loss at confidence level over time period.

```python
# Historical VaR (95%)
var_95 = np.percentile(returns, 5)

# Parametric VaR
var_95 = returns.mean() - 1.645 * returns.std()
```

### Volatility
Standard deviation of returns. THE fundamental risk measure in finance.

```python
daily_vol = returns.std()
annualized_vol = daily_vol * np.sqrt(252)
```

**68-95-99.7 rule** applied to returns: 95% of daily returns within +/- 2*sigma.

## Financial Constants
- Trading days per year: 252
- Trading days per month: ~20
- Trading days per quarter: ~60
- Annualization factor: sqrt(252) for volatility

## Asset-Backed Securities (ABS)

**Securitization**: convert illiquid assets (mortgages, loans) into tradable bonds.
- **SPV** (Special Purpose Vehicle): legally separate entity holding asset pool
- **Tranching**: redistribute cash flows into bonds with different risk/return profiles
- **Senior tranche**: first to be paid, lowest risk (AAA rating)
- **Equity tranche**: residual after all other tranches paid, highest risk/return

## Key Financial Ratios

| Category | Metrics |
|----------|---------|
| Profitability | EBIT, EBITDA, net margin |
| Liquidity | Current ratio, quick ratio |
| Solvency | Debt/equity, interest coverage |
| Valuation | P/E, EV/EBITDA, P/B |
| Cash flow | FCF, operating cash flow |

**Free Cash Flow (FCF)**: most important metric for cash generation capacity. Accounts for working capital changes and CapEx.

## Gotchas
- Financial returns are NOT normally distributed - heavy tails (kurtosis > 0)
- Past performance does not predict future returns
- Correlation between assets changes during crises (correlation goes to 1)
- VaR underestimates tail risk - use CVaR (expected shortfall) for extreme scenarios
- Always use log returns for multi-period analysis, simple returns for single period

## See Also
- [[monte-carlo-simulation]] - simulation techniques for finance
- [[probability-distributions]] - distribution theory
- [[time-series-analysis]] - financial time series
- [[descriptive-statistics]] - analyzing return distributions
