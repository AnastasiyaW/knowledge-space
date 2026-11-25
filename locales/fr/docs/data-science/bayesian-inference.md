---
title: "Inférence bayésienne pour le ML"
category: concepts
tags: [data-science, bayesian, probabilistic-programming, pymc, uncertainty, mcmc]
level: 3
source_sha256: 2b648158fb9be1aa6f41eb7f92c96c2626ad43191fb8ce74f3a8d528d3440b93
translation: machine
translated_at: '2026-10-24'
---
# Inférence bayésienne pour le ML {#bayesian-inference-for-ml}

L'approche bayésienne traite les paramètres du modèle comme des distributions de probabilité, et non comme des estimations ponctuelles. Au lieu de « le coefficient vaut 0,5 », on obtient « le coefficient vaut 0,5 +/- 0,1 avec une probabilité de 95 % ». Cette approche est essentielle pour la quantification de l'incertitude, les petits jeux de données et la prise de décision en situation de risque.

## Théorème de Bayes {#bayes-theorem}

P(theta|data) = P(data|theta) * P(theta) / P(data)

- **Prior P(theta)** : ce que l'on croit avant d'observer les données
- **Vraisemblance P(data|theta)** : la probabilité des données étant donnés les paramètres
- **Postérieure P(theta|data)** : les croyances mises à jour après observation des données
- **Évidence P(data)** : constante de normalisation (souvent intraitable)

## Bayésien vs fréquentiste {#bayesian-vs-frequentist}

| Aspect | Fréquentiste | Bayésien |
|--------|-------------|----------|
| Paramètres | Fixes, inconnus | Variables aléatoires |
| Incertitude | Intervalles de confiance | Intervalles de crédibilité |
| Connaissance a priori | Non utilisée | Encodée sous forme de prior |
| Petites données | Peu fiable | Régularisée par le prior |
| Calcul | Rapide (MLE) | Plus lent (MCMC/VI) |
| Interprétation | Fréquence à long terme | Probabilité d'une hypothèse |

## Programmation probabiliste avec PyMC {#probabilistic-programming-with-pymc}

```python
import pymc as pm
import arviz as az

# Bayesian Linear Regression
with pm.Model() as model:
    # Priors
    alpha = pm.Normal("alpha", mu=0, sigma=10)
    beta = pm.Normal("beta", mu=0, sigma=10, shape=X.shape[1])
    sigma = pm.HalfNormal("sigma", sigma=1)

    # Likelihood
    mu = alpha + pm.math.dot(X, beta)
    y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)

    # Inference (MCMC sampling)
    trace = pm.sample(2000, tune=1000, cores=4, return_inferencedata=True)

# Analyze posterior
az.summary(trace, var_names=["alpha", "beta", "sigma"])
az.plot_posterior(trace, var_names=["beta"])
az.plot_trace(trace)
```

## MCMC (Markov Chain Monte Carlo) {#mcmc-markov-chain-monte-carlo}

Algorithme d'échantillonnage permettant d'approximer la postérieure lorsqu'une solution analytique est impossible.

**NUTS (No-U-Turn Sampler)** : méthode par défaut dans PyMC et Stan. Elle adapte automatiquement la taille du pas. C'est la référence pour les paramètres continus.

**Diagnostics** :
- **R-hat (Gelman-Rubin)** : doit être inférieur à 1,01. Mesure la convergence des chaînes
- **Taille d'échantillon effective (ESS)** : doit être supérieure à 400. Tient compte de l'autocorrélation
- **Divergences** : spécifiques à NUTS. Des divergences signalent une mauvaise géométrie ; il faut reparamétrer le modèle

```python
# Check diagnostics
az.summary(trace)  # includes r_hat and ess columns
az.plot_trace(trace)  # visual: chains should mix well (look like fuzzy caterpillars)
```

## Inférence variationnelle (VI) {#variational-inference-vi}

Alternative plus rapide au MCMC. Elle approxime la postérieure par une distribution plus simple. Moins précise, mais adaptée aux grands volumes de données.

```python
with model:
    # Mean-field variational inference
    approx = pm.fit(method='advi', n=30000)
    trace_vi = approx.sample(2000)
```

## Réseaux de neurones bayésiens {#bayesian-neural-networks}

Les poids ponctuels sont remplacés par des distributions sur les poids. Ce modèle capture l'incertitude épistémique.

```python
import torch
import torch.nn as nn

class BayesianLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight_mu = nn.Parameter(torch.randn(out_features, in_features) * 0.1)
        self.weight_log_sigma = nn.Parameter(torch.full((out_features, in_features), -3.0))

    def forward(self, x):
        weight_sigma = torch.exp(self.weight_log_sigma)
        weight = self.weight_mu + weight_sigma * torch.randn_like(self.weight_mu)
        return x @ weight.T

# MC Dropout as cheap Bayesian approximation
class MCDropoutModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout=0.1):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim)
        )

    def predict_with_uncertainty(self, x, n_samples=100):
        self.train()  # keep dropout ON
        preds = torch.stack([self.layers(x) for _ in range(n_samples)])
        return preds.mean(0), preds.std(0)  # mean prediction + uncertainty
```

## Test A/B bayésien {#bayesian-ab-testing}

Plus adapté que le test d'hypothèse fréquentiste pour les décisions métier :

```python
with pm.Model() as ab_model:
    # Priors for conversion rates
    p_A = pm.Beta("p_A", alpha=1, beta=1)  # uninformative prior
    p_B = pm.Beta("p_B", alpha=1, beta=1)

    # Observed data
    obs_A = pm.Binomial("obs_A", n=n_visitors_A, p=p_A, observed=conversions_A)
    obs_B = pm.Binomial("obs_B", n=n_visitors_B, p=p_B, observed=conversions_B)

    # Derived: probability B is better
    diff = pm.Deterministic("diff", p_B - p_A)

    trace = pm.sample(5000, return_inferencedata=True)

# P(B > A)
p_b_better = (trace.posterior["diff"] > 0).mean().item()
print(f"Probability B is better: {p_b_better:.1%}")
```

## Priors conjugués {#conjugate-priors}

Lorsque le prior et la postérieure appartiennent à la même famille de distributions, la mise à jour est analytique (aucun MCMC n'est nécessaire) :

| Vraisemblance | Prior conjugué | Postérieure |
|---------------|----------------|-------------|
| Bernoulli | Bêta | Bêta |
| Poisson | Gamma | Gamma |
| Normale (variance connue) | Normale | Normale |
| Multinomiale | Dirichlet | Dirichlet |

## Pièges à éviter {#gotchas}

- **Sensibilité au prior avec peu de données** : avec moins de 100 échantillons, le prior domine. Effectuez toujours des vérifications prédictives a priori (`pm.sample_prior_predictive()`) pour vous assurer que les priors génèrent des plages de données plausibles. Des priors incorrects donnent des postérieures incorrectes, quelles que soient les données
- **Les divergences MCMC ne sont pas des avertissements, ce sont des erreurs** : des transitions divergentes signifient que l'échantillonneur n'a pas exploré correctement la postérieure. Les résultats ne sont pas fiables. Reparamétrez le modèle (paramétrisation non centrée), augmentez `target_accept` à 0,95, ou simplifiez le modèle
- **La VI sous-estime l'incertitude** : l'inférence variationnelle utilise des distributions plus simples (généralement gaussiennes) pour approximer la vraie postérieure. Elle sous-estime systématiquement la largeur des intervalles de crédibilité. Utilisez le MCMC lorsqu'une quantification précise de l'incertitude est importante

## Voir aussi {#see-also}

- [[bayesian-methods]]
- [[probability-distributions]]
- [[hypothesis-testing]]
- [[model-evaluation]]
