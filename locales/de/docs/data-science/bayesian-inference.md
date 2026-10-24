---
title: "Bayes'sche Inferenz für ML"
category: concepts
tags: [data-science, bayesian, probabilistic-programming, pymc, uncertainty, mcmc]
level: 3
source_sha256: 2b648158fb9be1aa6f41eb7f92c96c2626ad43191fb8ce74f3a8d528d3440b93
translation: machine
translated_at: '2026-10-24'
---
# Bayes'sche Inferenz für ML {#bayesian-inference-for-ml}

Der Bayes'sche Ansatz behandelt Modellparameter als Wahrscheinlichkeitsverteilungen und nicht als Punktschätzungen. Statt „der Koeffizient ist 0,5“ erhält man „der Koeffizient ist 0,5 +/- 0,1 mit 95 % Wahrscheinlichkeit“. Dieser Ansatz ist entscheidend für die Quantifizierung von Unsicherheit, kleine Datensätze und Entscheidungsfindung unter Risiko.

## Satz von Bayes {#bayes-theorem}

P(theta|data) = P(data|theta) * P(theta) / P(data)

- **Prior P(theta)**: was man vor der Beobachtung der Daten glaubt
- **Likelihood P(data|theta)**: wie wahrscheinlich die Daten bei gegebenen Parametern sind
- **Posterior P(theta|data)**: aktualisierte Überzeugungen nach Beobachtung der Daten
- **Evidenz P(data)**: Normierungskonstante (oft nicht analytisch berechenbar)

## Bayes'sch vs. frequentistisch {#bayesian-vs-frequentist}

| Aspekt | Frequentistisch | Bayes'sch |
|--------|-----------------|-----------|
| Parameter | Fest, unbekannt | Zufallsvariablen |
| Unsicherheit | Konfidenzintervalle | Glaubwürdigkeitsintervalle |
| Vorwissen | Nicht verwendet | Als Prior kodiert |
| Kleine Datenmengen | Unzuverlässig | Durch Prior regularisiert |
| Berechnung | Schnell (MLE) | Langsamer (MCMC/VI) |
| Interpretation | Langfristige Häufigkeit | Wahrscheinlichkeit einer Hypothese |

## Probabilistische Programmierung mit PyMC {#probabilistic-programming-with-pymc}

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

## MCMC (Markov-Chain-Monte-Carlo) {#mcmc-markov-chain-monte-carlo}

Sampling-Algorithmus zur Approximation des Posteriors, wenn keine analytische Lösung möglich ist.

**NUTS (No-U-Turn Sampler)**: Standard in PyMC und Stan. Passt die Schrittweite automatisch an. Goldstandard für kontinuierliche Parameter.

**Diagnose**:
- **R-hat (Gelman-Rubin)**: sollte < 1,01 sein. Misst die Konvergenz der Ketten
- **Effektive Stichprobengröße (ESS)**: sollte > 400 sein. Berücksichtigt Autokorrelation
- **Divergenzen**: NUTS-spezifisch. Divergenzen = ungünstige Geometrie, Modell umparametrisieren

```python
# Check diagnostics
az.summary(trace)  # includes r_hat and ess columns
az.plot_trace(trace)  # visual: chains should mix well (look like fuzzy caterpillars)
```

## Variational Inference (VI) {#variational-inference-vi}

Schnellere Alternative zu MCMC. Approximiert den Posterior durch eine einfachere Verteilung. Weniger genau, skaliert aber auf große Datenmengen.

```python
with model:
    # Mean-field variational inference
    approx = pm.fit(method='advi', n=30000)
    trace_vi = approx.sample(2000)
```

## Bayes'sche neuronale Netze {#bayesian-neural-networks}

Ersetzen Netze mit Punktgewichten durch Verteilungen über die Gewichte. Erfassen epistemische Unsicherheit.

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

## Bayes'sches A/B-Testing {#bayesian-ab-testing}

Für geschäftliche Entscheidungen dem frequentistischen Hypothesentest überlegen:

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

## Konjugierte Priors {#conjugate-priors}

Wenn Prior und Posterior derselben Verteilungsfamilie angehören, ist das Update analytisch (kein MCMC nötig):

| Likelihood | Konjugierter Prior | Posterior |
|------------|--------------------|-----------|
| Bernoulli | Beta | Beta |
| Poisson | Gamma | Gamma |
| Normal (bekannte Varianz) | Normal | Normal |
| Multinomial | Dirichlet | Dirichlet |

## Fallstricke {#gotchas}

- **Prior-Sensitivität bei kleinen Datenmengen**: Bei weniger als 100 Stichproben dominiert der Prior. Immer Prior-Predictive-Checks durchführen (`pm.sample_prior_predictive()`), um zu prüfen, ob die Priors plausible Datenbereiche erzeugen. Schlechte Priors führen unabhängig von den Daten zu schlechten Posteriors
- **MCMC-Divergenzen sind keine Warnungen, sondern Fehler**: Divergente Übergänge bedeuten, dass der Sampler den Posterior nicht korrekt erkundet hat. Die Ergebnisse sind unzuverlässig. Umparametrisieren (nicht-zentrierte Parametrisierung), `target_accept` auf 0,95 erhöhen oder das Modell vereinfachen
- **VI unterschätzt die Unsicherheit**: Variational Inference verwendet einfachere Verteilungen (meist Gaußsche), um den wahren Posterior zu approximieren. Dadurch wird die Breite der Glaubwürdigkeitsintervalle systematisch unterschätzt. Bei Bedarf an präziser Unsicherheitsquantifizierung MCMC verwenden

## Siehe auch {#see-also}

- [[bayesian-methods]]
- [[probability-distributions]]
- [[hypothesis-testing]]
- [[model-evaluation]]
