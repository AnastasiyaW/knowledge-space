---
title: Probability Distributions
category: math-foundations
tags: [probability, distributions, normal, binomial, poisson, bayes, statistics]
---

# Probability Distributions

A probability distribution describes how likely each possible outcome is. Discrete distributions assign probabilities to countable outcomes; continuous distributions use probability density functions (PDF). Understanding distributions is essential for [[hypothesis-testing]], generative models, and [[loss-functions-and-regularization]].

## Key Facts

- **PMF** (Probability Mass Function): for discrete variables; P(X = x)
- **PDF** (Probability Density Function): for continuous variables; P(a <= X <= b) = integral of f(x) from a to b
- **CDF** (Cumulative Distribution Function): P(X <= x); works for both discrete and continuous
- **Expected value** E[X] = sum(x * P(x)) or integral(x * f(x)); the "average" outcome
- **Variance** Var(X) = E[(X - mu)^2]; measures spread; **std dev** = sqrt(variance)
- **Bernoulli**: single binary trial; P(X=1) = p; mean = p, var = p(1-p)
- **Binomial**: n independent Bernoulli trials; P(X=k) = C(n,k) * p^k * (1-p)^(n-k)
- **Poisson**: count of events in fixed interval; P(X=k) = (lambda^k * e^(-lambda)) / k!; mean = var = lambda
- **Normal (Gaussian)**: bell curve; defined by mu and sigma; 68-95-99.7 rule; [[regression-models]] assume normal residuals
- **Uniform**: all outcomes equally likely; U(a, b) has mean = (a+b)/2
- **Exponential**: time between Poisson events; memoryless property
- **Bayes' theorem**: P(A|B) = P(B|A) * P(A) / P(B); foundation of Bayesian inference and Naive Bayes classifier
- **Central Limit Theorem (CLT)**: sample means approach Normal distribution as n grows, regardless of population distribution
- **Law of Large Numbers**: sample mean converges to population mean as n increases

## Patterns

```python
import numpy as np
from scipy import stats

# Normal distribution
mu, sigma = 0, 1
norm_dist = stats.norm(loc=mu, scale=sigma)
norm_dist.pdf(0)        # 0.3989 (density at x=0)
norm_dist.cdf(1.96)     # ~0.975 (P(X <= 1.96))
norm_dist.ppf(0.975)    # ~1.96 (inverse CDF / quantile)
samples = norm_dist.rvs(size=1000)  # random samples

# Binomial: 10 coin flips, P(heads) = 0.5
binom_dist = stats.binom(n=10, p=0.5)
binom_dist.pmf(5)       # P(X=5) = 0.2461
binom_dist.mean()       # 5.0

# Poisson: average 3 events per hour
pois_dist = stats.poisson(mu=3)
pois_dist.pmf(5)        # P(X=5) = 0.1008

# Bayes' theorem manual
# P(disease | positive_test) = P(pos|disease)*P(disease) / P(pos)
p_disease = 0.001
p_pos_given_disease = 0.99
p_pos_given_healthy = 0.05
p_pos = p_pos_given_disease * p_disease + p_pos_given_healthy * (1 - p_disease)
p_disease_given_pos = p_pos_given_disease * p_disease / p_pos  # ~0.0194

# Check if data is normally distributed
from scipy.stats import shapiro
stat, p_value = shapiro(samples)
# p > 0.05: fail to reject H0 (data looks normal)

# Q-Q plot for visual normality check
import matplotlib.pyplot as plt
stats.probplot(samples, dist="norm", plot=plt)
```

## Gotchas

- PDF value can exceed 1 (it is density, not probability); only CDF values are in [0, 1]
- Normal distribution goes to +/- infinity; no real data is perfectly normal
- CLT requires independent samples and finite variance; does NOT apply to Cauchy distribution
- Bayes' theorem with low base rate: even with 99% accurate test, P(disease | positive) can be very low
- `scipy.stats.norm(scale=sigma)` uses std dev, not variance -- don't accidentally pass variance

## See Also

- [[hypothesis-testing]] - uses distributions to compute p-values and critical regions
- [[descriptive-statistics]] - mean, variance, skewness describe distribution shape
- [[generative-models]] - GANs and VAEs learn to generate samples from data distributions
- scipy.stats docs: https://docs.scipy.org/doc/scipy/reference/stats.html
