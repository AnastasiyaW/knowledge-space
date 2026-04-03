---
title: Probability and Distributions
category: concepts
tags: [data-science, statistics, probability, distributions]
---

# Probability and Distributions

Core probability theory and common distributions used throughout data science and ML. Understanding distributions is essential for choosing appropriate statistical tests, building generative models, and interpreting results.

## Probability Fundamentals

**Probability** P(A) = measure of how likely event A is. Range: [0, 1].

**Classical definition**: P(A) = favorable outcomes / total equally likely outcomes.
**Frequentist definition**: P(A) = lim(N->inf) count(A) / N.

### Key Rules

| Rule | Formula |
|------|---------|
| Complement | P(not A) = 1 - P(A) |
| Addition | P(A or B) = P(A) + P(B) - P(A and B) |
| Mutually exclusive | P(A or B) = P(A) + P(B) |
| Independence | P(A and B) = P(A) * P(B) |
| Conditional | P(A\|B) = P(A and B) / P(B) |

**"At least one" pattern**: P(at least one) = 1 - P(none). Much easier than direct computation.

### Bayes' Theorem

P(A|B) = P(B|A) * P(A) / P(B)

- P(A|B): posterior (what we want)
- P(B|A): likelihood
- P(A): prior
- P(B): evidence (marginal)

**Gotcha**: P(A|B) != P(B|A). P(disease|positive test) is NOT P(positive test|disease).

### Total Probability

P(A) = sum_i P(A|B_i) * P(B_i) where {B_i} partitions the sample space.

## Random Variables

**Discrete**: countable values (die roll, number of customers). Described by PMF.
**Continuous**: any value in a range (height, temperature). Described by PDF.

- **Expected value**: E(X) = sum(x_i * P(x_i)) or integral(x * f(x) dx)
- **Variance**: Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2

## Common Discrete Distributions

### Bernoulli
Single trial with success probability p.
- E(X) = p, Var(X) = p(1-p)

### Binomial
k successes in n independent Bernoulli trials.
- P(k) = C(n,k) * p^k * (1-p)^(n-k)
- E(X) = np, Var(X) = np(1-p)

### Poisson
Number of events in fixed interval with rate lambda.
- P(k) = (lambda^k / k!) * e^(-lambda)
- E(X) = Var(X) = lambda
- Use for: rare events, count data (calls/hour, accidents/month)

## Common Continuous Distributions

### Normal (Gaussian)
Bell-shaped, symmetric. Defined by mu (mean) and sigma (std dev).
```python
from scipy import stats
norm = stats.norm(loc=0, scale=1)
norm.pdf(0)      # density at 0
norm.cdf(1.96)   # P(X <= 1.96) ~ 0.975
norm.ppf(0.95)   # 95th percentile ~ 1.645
```

**Central Limit Theorem**: sum/average of many independent random variables tends to normal regardless of their individual distributions. This is why the normal distribution is so common.

### Exponential
Time between independent events at constant rate.
- Memoryless: P(X > s + t | X > s) = P(X > t)
- E(X) = 1/lambda, Var(X) = 1/lambda^2

### Uniform
All outcomes equally likely over [a, b].
- E(X) = (a+b)/2, Var(X) = (b-a)^2/12

## Combinatorics

- **Permutations** (order matters): P(n,k) = n! / (n-k)!
- **Combinations** (order doesn't matter): C(n,k) = n! / (k!(n-k)!)
- **With repetition**: permutations = n^k, combinations = C(n+k-1, k)
- **Binomial theorem**: (a+b)^n = sum C(n,k) * a^(n-k) * b^k

## Key Theorems

- **Law of Large Numbers**: sample mean converges to population mean as n -> inf
- **Central Limit Theorem**: standardized sample mean -> N(0,1) as n -> inf
- **Chebyshev's inequality**: P(|X - mu| >= k*sigma) <= 1/k^2 (for any distribution)

## Simulating Distributions

```python
import numpy as np

# Inverse CDF method: if U ~ Uniform(0,1), then F^{-1}(U) has CDF F
# Exponential: X = -ln(U) / lambda
u = np.random.uniform(size=10000)
x_exp = -np.log(u) / 2.0  # Exp(lambda=2)

# Box-Muller for normal:
u1, u2 = np.random.uniform(size=10000), np.random.uniform(size=10000)
z = np.sqrt(-2*np.log(u1)) * np.cos(2*np.pi*u2)  # N(0,1)

# Direct numpy:
np.random.normal(0, 1, 10000)     # normal
np.random.poisson(5, 10000)       # poisson
np.random.binomial(10, 0.3, 10000) # binomial
```

## Gotchas
- Poisson is NOT just "binomial with large n, small p" - Poisson assumes constant rate, binomial assumes fixed trials
- Normal distribution is **not** universal - many real-world distributions are heavily skewed (income, file sizes)
- CLT requires finite variance - fails for heavy-tailed distributions (Cauchy)
- Exponential is the **only** continuous memoryless distribution

## See Also
- [[descriptive-statistics]] - empirical summaries of data
- [[hypothesis-testing]] - using distributions for statistical inference
- [[bayesian-methods]] - Bayes' theorem in ML context
- [[math-for-ml]] - probability theory foundations
