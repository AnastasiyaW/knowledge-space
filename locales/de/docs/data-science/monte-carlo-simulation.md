---
title: "Monte-Carlo-Simulation"
category: techniques
tags: [data-science, simulation, monte-carlo, finance, risk]
level: 3
source_sha256: 9e154cf98988cabff835e3af4e2bbc77d0e1486fb4e2b5bd4093a71a0ede526b
translation: machine
translated_at: '2026-10-24'
---
# Monte-Carlo-Simulation {#monte-carlo-simulation}

Ergebnisse durch die Durchführung von Tausenden von Zufallsexperimenten abschätzen. Wenn analytische Lösungen nicht handhabbar sind, wird simuliert. Weit verbreitet in Finanzwesen, Risikoanalyse und Portfoliooptimierung.

## Grundidee {#core-idea}

1. Ein Modell mit zufälligen Eingaben definieren
2. Viele Simulationen durchführen (1000+)
3. Ergebnisse für Wahrscheinlichkeitsschätzungen aggregieren

## Simulation von Aktienkursen {#stock-price-simulation}

Geometrische Brownsche Bewegung (GBM):

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

## Portfoliooptimierung {#portfolio-optimization}

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

## Risikokennzahlen {#risk-metrics}

### Value at Risk (VaR) {#value-at-risk-var}
Maximal erwarteter Verlust bei gegebenem Konfidenzniveau.

```python
# Historical VaR (95% confidence)
var_95 = np.percentile(returns, 5)  # 5th percentile

# Parametric VaR
var_95 = returns.mean() - 1.645 * returns.std()
```

### Sharpe-Ratio {#sharpe-ratio}
Risikoadjustierte Rendite: (Rendite - risikofreier_Zins) / Standardabweichung

```python
sharpe = (returns.mean() - risk_free_rate) / returns.std()
annualized_sharpe = sharpe * np.sqrt(252)
```

## Praktische Tipps {#practical-tips}

- Mehr Simulationen = stabilere Schätzungen. Für ernsthafte Analysen 10.000+ verwenden
- Mit NumPy vektorisieren – niemals Python-Schleifen für Simulationen verwenden
- Immer einen Zufallsseed setzen, um Reproduzierbarkeit zu gewährleisten
- Visualisieren: Streudiagramm von Risiko vs. Rendite, eingefärbt nach Sharpe-Ratio
- Handelstage: 20/Monat, 252/Jahr im Finanzwesen

## Anwendungen jenseits der Finanzwelt {#applications-beyond-finance}

- Sportprognosen (Turniere simulieren)
- Schätzung von Projektzeitplänen (Aufgabendauern simulieren)
- Power-Analyse für A/B-Tests
- Bayessche Inferenz (MCMC)
- Physikalische Simulationen

## Siehe auch {#see-also}
- [[probability-distributions]] - in Simulationen verwendete Verteilungen
- [[numpy-fundamentals]] - vektorisierte Zufallszahlenerzeugung
- [[descriptive-statistics]] - Analyse der Simulationsergebnisse
