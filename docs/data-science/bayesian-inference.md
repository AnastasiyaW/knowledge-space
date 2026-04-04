---
title: Bayesian Inference for ML
category: concepts
tags: [data-science, bayesian, probabilistic-programming, pymc, uncertainty, mcmc]
---

# Bayesian Inference for ML

Bayesian approach treats model parameters as probability distributions, not point estimates. Instead of "the coefficient is 0.5", you get "the coefficient is 0.5 +/- 0.1 with 95% probability". Critical for uncertainty quantification, small datasets, and decision-making under risk.

## Bayes Theorem

P(theta|data) = P(data|theta) * P(theta) / P(data)

- **Prior P(theta)**: what you believe before seeing data
- **Likelihood P(data|theta)**: how likely the data is given parameters
- **Posterior P(theta|data)**: updated beliefs after seeing data
- **Evidence P(data)**: normalizing constant (often intractable)

## Bayesian vs Frequentist

| Aspect | Frequentist | Bayesian |
|--------|-------------|----------|
| Parameters | Fixed, unknown | Random variables |
| Uncertainty | Confidence intervals | Credible intervals |
| Prior knowledge | Not used | Encoded as prior |
| Small data | Unreliable | Regularized by prior |
| Computation | Fast (MLE) | Slower (MCMC/VI) |
| Interpretation | Long-run frequency | Probability of hypothesis |

## Probabilistic Programming with PyMC

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

## MCMC (Markov Chain Monte Carlo)

Sampling algorithm to approximate posterior when analytic solution is impossible.

**NUTS (No-U-Turn Sampler)**: default in PyMC, Stan. Adapts step size automatically. Gold standard for continuous parameters.

**Diagnostics**:
- **R-hat (Gelman-Rubin)**: should be < 1.01. Measures chain convergence
- **Effective sample size (ESS)**: should be > 400. Accounts for autocorrelation
- **Divergences**: NUTS-specific. Divergences = bad geometry, reparameterize model

```python
# Check diagnostics
az.summary(trace)  # includes r_hat and ess columns
az.plot_trace(trace)  # visual: chains should mix well (look like fuzzy caterpillars)
```

## Variational Inference (VI)

Faster alternative to MCMC. Approximates posterior with simpler distribution. Less accurate but scales to large data.

```python
with model:
    # Mean-field variational inference
    approx = pm.fit(method='advi', n=30000)
    trace_vi = approx.sample(2000)
```

## Bayesian Neural Networks

Replace point-weight networks with distributions over weights. Capture epistemic uncertainty.

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

## Bayesian A/B Testing

Superior to frequentist hypothesis testing for business decisions:

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

## Conjugate Priors

When prior and posterior are same distribution family, update is analytic (no MCMC needed):

| Likelihood | Conjugate Prior | Posterior |
|------------|----------------|-----------|
| Bernoulli | Beta | Beta |
| Poisson | Gamma | Gamma |
| Normal (known var) | Normal | Normal |
| Multinomial | Dirichlet | Dirichlet |

## Gotchas

- **Prior sensitivity with small data**: with < 100 samples, the prior dominates. Always do prior predictive checks (`pm.sample_prior_predictive()`) to verify priors generate plausible data ranges. Garbage priors = garbage posteriors regardless of data
- **MCMC divergences are not warnings - they are errors**: divergent transitions mean the sampler failed to explore the posterior correctly. Results are unreliable. Reparameterize (non-centered parameterization), increase `target_accept` to 0.95, or simplify model
- **VI underestimates uncertainty**: variational inference uses simpler distributions (usually Gaussian) to approximate the true posterior. It consistently underestimates the width of credible intervals. Use MCMC when accurate uncertainty quantification matters

## See Also

- [[bayesian-methods]]
- [[probability-distributions]]
- [[hypothesis-testing]]
- [[model-evaluation]]
