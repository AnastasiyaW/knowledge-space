---
title: "Simulation de Monte-Carlo"
category: techniques
tags: [data-science, simulation, monte-carlo, finance, risk]
level: 3
source_sha256: 9e154cf98988cabff835e3af4e2bbc77d0e1486fb4e2b5bd4093a71a0ede526b
translation: machine
translated_at: '2026-10-24'
---
# Simulation de Monte-Carlo {#monte-carlo-simulation}

Estimer des résultats en exécutant des milliers d'expériences aléatoires. Lorsque les solutions analytiques sont intraitables, on simule. Largement utilisée en finance, en analyse de risque et en optimisation de portefeuille.

## Idée centrale {#core-idea}

1. Définir un modèle avec des entrées aléatoires
2. Exécuter de nombreuses simulations (1000+)
3. Agréger les résultats pour estimer des probabilités

## Simulation du cours d'une action {#stock-price-simulation}

Mouvement brownien géométrique (GBM) :

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

## Optimisation de portefeuille {#portfolio-optimization}

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

## Mesures de risque {#risk-metrics}

### Value at Risk (VaR) {#value-at-risk-var}
Perte maximale attendue à un niveau de confiance donné.

```python
# Historical VaR (95% confidence)
var_95 = np.percentile(returns, 5)  # 5th percentile

# Parametric VaR
var_95 = returns.mean() - 1.645 * returns.std()
```

### Ratio de Sharpe {#sharpe-ratio}
Rendement ajusté du risque : (rendement - taux sans risque) / écart-type

```python
sharpe = (returns.mean() - risk_free_rate) / returns.std()
annualized_sharpe = sharpe * np.sqrt(252)
```

## Conseils pratiques {#practical-tips}

- Plus de simulations = estimations plus stables. Utilisez 10 000+ pour une analyse sérieuse
- Vectorisez avec NumPy : n'utilisez jamais de boucles Python pour la simulation
- Fixez toujours la graine aléatoire (random seed) pour la reproductibilité
- Visualisez : nuage de points risque/rendement coloré par le ratio de Sharpe
- Jours ouvrés : 20 par mois, 252 par an en finance

## Applications au-delà de la finance {#applications-beyond-finance}

- Prédiction sportive (simuler des tournois)
- Estimation de calendriers de projet (simuler la durée des tâches)
- Analyse de puissance des tests A/B
- Inférence bayésienne (MCMC)
- Simulations en physique

## Voir aussi {#see-also}
- [[probability-distributions]] - distributions utilisées en simulation
- [[numpy-fundamentals]] - génération aléatoire vectorisée
- [[descriptive-statistics]] - analyse des résultats de simulation
