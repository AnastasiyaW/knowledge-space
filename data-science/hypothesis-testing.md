---
title: Hypothesis Testing
category: statistics
tags: [hypothesis-testing, p-value, t-test, chi-square, ab-testing, confidence-interval]
---

# Hypothesis Testing

A formal framework for making decisions from data. Define a null hypothesis (H0), collect data, compute a test statistic, and decide whether the evidence is strong enough to reject H0. Used extensively in A/B testing, feature selection, and validating [[model-evaluation-metrics]].

## Key Facts

- **H0 (null hypothesis)**: default assumption (e.g., "no difference between groups")
- **H1 (alternative hypothesis)**: what you want to prove (e.g., "treatment group is different")
- **p-value**: probability of observing data at least as extreme as measured, assuming H0 is true
- **Significance level (alpha)**: threshold for rejection; typically 0.05; reject H0 if p < alpha
- **Type I error (false positive)**: rejecting H0 when it is true; probability = alpha
- **Type II error (false negative)**: failing to reject H0 when H1 is true; probability = beta
- **Power** = 1 - beta; probability of correctly detecting a real effect; aim for >= 0.8
- **t-test**: compares means; one-sample, two-sample (independent), paired; assumes normality or large n
- **Chi-squared test**: tests independence of categorical variables or goodness-of-fit
- **Mann-Whitney U**: non-parametric alternative to independent t-test (no normality assumption)
- **ANOVA**: extension of t-test to 3+ groups; F-statistic
- **Confidence interval**: range that contains the true parameter with (1-alpha) probability
- **Multiple comparisons problem**: testing many hypotheses inflates false positive rate; use Bonferroni correction (alpha / n_tests) or Benjamini-Hochberg (FDR)

## Patterns

```python
from scipy import stats
import numpy as np

# Two-sample independent t-test
group_a = np.random.normal(100, 15, size=50)
group_b = np.random.normal(105, 15, size=50)
t_stat, p_value = stats.ttest_ind(group_a, group_b)
# p < 0.05 => reject H0, means are significantly different

# Paired t-test (before/after measurements)
before = np.array([85, 90, 78, 92, 88])
after = np.array([90, 95, 82, 96, 91])
t_stat, p_value = stats.ttest_rel(before, after)

# Chi-squared test for independence
# contingency table: rows = groups, cols = outcomes
observed = np.array([[50, 30], [40, 80]])
chi2, p_value, dof, expected = stats.chi2_contingency(observed)

# Mann-Whitney U (non-parametric)
u_stat, p_value = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')

# One-way ANOVA (3+ groups)
g1 = np.random.normal(10, 2, 30)
g2 = np.random.normal(11, 2, 30)
g3 = np.random.normal(10.5, 2, 30)
f_stat, p_value = stats.f_oneway(g1, g2, g3)

# Confidence interval for mean
sample = np.random.normal(50, 10, 100)
ci = stats.t.interval(
    confidence=0.95,
    df=len(sample) - 1,
    loc=np.mean(sample),
    scale=stats.sem(sample)
)

# Bonferroni correction for multiple comparisons
from statsmodels.stats.multitest import multipletests
p_values = [0.01, 0.04, 0.03, 0.20]
reject, corrected_p, _, _ = multipletests(p_values, method='bonferroni')

# A/B test: conversion rates
# Group A: 500 visitors, 50 conversions; Group B: 500, 65 conversions
from statsmodels.stats.proportion import proportions_ztest
count = np.array([50, 65])
nobs = np.array([500, 500])
z_stat, p_value = proportions_ztest(count, nobs)
```

## Gotchas

- p-value is NOT the probability that H0 is true; it is P(data | H0)
- Statistical significance != practical significance; a tiny effect can be "significant" with large n
- t-test assumes equal variances by default; use `equal_var=False` (Welch's t-test) when unsure
- Multiple A/B tests without correction will produce false positives: 20 tests at alpha=0.05 -> expect 1 false positive
- Never peek at p-values during data collection and stop early ("p-hacking"); decide sample size before starting

## See Also

- [[probability-distributions]] - test statistics follow known distributions (t, chi2, F)
- [[descriptive-statistics]] - summarize data before testing
- [[model-evaluation-metrics]] - statistical tests validate model performance differences
- statsmodels docs: https://www.statsmodels.org/stable/stats.html
