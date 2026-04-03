---
title: Probability Theory and Statistical Inference
category: foundations
tags: [data-science, math, probability, statistics, estimation, mle]
---

# Probability Theory and Statistical Inference

Rigorous probability foundations and statistical estimation methods. Bridges the gap between math theory and practical statistics used in ML.

## Probability Axioms

1. P(A) >= 0 for any event A
2. P(sample space) = 1
3. For mutually exclusive events: P(A1 or A2 or ...) = sum P(Ai)

## Key Theorems

### Law of Large Numbers (Weak)
Sample mean converges in probability to population mean as n -> inf. Justifies using sample statistics to estimate population parameters.

### Central Limit Theorem
For iid random variables with mean mu and variance sigma^2:
(X_bar - mu) / (sigma / sqrt(n)) -> N(0,1) as n -> inf

Regardless of original distribution. This is why normal distribution appears everywhere.

### Chebyshev's Inequality
P(|X - mu| >= k*sigma) <= 1/k^2 for ANY distribution.
- k=2: at most 25% of data beyond 2 sigma (empirical: ~5% for normal)
- k=3: at most 11% beyond 3 sigma (empirical: ~0.3% for normal)

## Statistical Estimation

### Point Estimation Properties
- **Unbiased**: E[theta_hat] = theta (on average, correct)
- **Consistent**: theta_hat -> theta as n -> inf (converges to truth)
- **Efficient**: achieves minimum variance (Cramer-Rao bound)
- **Sufficient**: captures all information about theta from the sample

### Maximum Likelihood Estimation (MLE)

Find parameters that maximize the likelihood of observed data.

L(theta) = product f(x_i | theta)

In practice, maximize log-likelihood: l(theta) = sum log f(x_i | theta)

**Properties**: MLE is asymptotically efficient, consistent, and normally distributed.

**Example (normal distribution)**: MLE for mu = sample mean, MLE for sigma^2 = sample variance (biased by n/(n-1)).

### Method of Moments
Equate sample moments to theoretical moments. Simpler than MLE but often less efficient.

## Hypothesis Testing (Theory)

### Framework
1. H0 (null) and H1 (alternative)
2. Choose alpha (significance level, typically 0.05)
3. Compute test statistic
4. Compare to critical value or compute p-value
5. Reject H0 if p-value < alpha

### Error Types
- **Type I** (alpha): reject true H0 (false positive)
- **Type II** (beta): fail to reject false H0 (false negative)
- **Power** = 1 - beta (probability of detecting real effect)

### Confidence Intervals
- Known variance: x_bar +/- z_(alpha/2) * sigma / sqrt(n)
- Unknown variance: x_bar +/- t_(alpha/2, n-1) * s / sqrt(n)

Student's t-distribution: heavier tails than normal. Used for small samples or unknown population variance.

## Convergence Types

From weakest to strongest:
1. **In distribution**: CDFs converge
2. **In probability**: P(|X_n - X| > epsilon) -> 0
3. **Almost surely**: P(lim X_n = X) = 1
4. **In mean (L^p)**: E[|X_n - X|^p] -> 0

## Asymptotic Analysis

- f = o(g): f grows strictly slower. lim f/g = 0
- f = O(g): f grows no faster (up to constant)
- f ~ g: asymptotically equivalent. lim f/g = 1
- Hierarchy: ln(n) << n^a << a^n << n! << n^n

## Conditional Expectation and Variance

- E[X] = E[E[X|Y]] (law of total expectation)
- Var(X) = E[Var(X|Y)] + Var(E[X|Y]) (law of total variance)

Useful in: Bayesian analysis, mixture models, hierarchical models.

## Gotchas
- MLE for variance is biased (divide by n, not n-1). Sample variance uses n-1 (Bessel's correction)
- CLT requires finite variance - fails for Cauchy and other heavy-tailed distributions
- p-value is NOT the probability that H0 is true. It's P(data | H0)
- Confidence interval: "95% of intervals constructed this way contain the true parameter" (frequentist interpretation)
- Statistical significance != practical significance. A tiny effect can be statistically significant with large n

## See Also
- [[probability-distributions]] - specific distributions
- [[hypothesis-testing]] - practical A/B testing
- [[descriptive-statistics]] - sample statistics
- [[math-for-ml]] - calculus for optimization
