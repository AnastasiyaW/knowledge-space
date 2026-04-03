---
title: Hypothesis Testing and A/B Testing
category: concepts
tags: [data-science, statistics, ab-testing, experimentation]
---

# Hypothesis Testing and A/B Testing

Statistical framework for making decisions from data. A/B testing applies these principles to controlled experiments. Critical skill for data scientists who need to distinguish real effects from noise.

## Hypothesis Testing Framework

1. **Formulate hypotheses**: H0 (null - no effect) and H1 (alternative - there is an effect)
2. **Choose significance level** alpha (typically 0.05)
3. **Compute test statistic** from data
4. **Calculate p-value** or compare to critical value
5. **Decision**: reject H0 if p-value < alpha

### Error Types

| | H0 True | H0 False |
|--|---------|----------|
| **Reject H0** | Type I (alpha) | Correct |
| **Fail to reject** | Correct | Type II (beta) |

- **Type I** (false positive): declaring effect when none exists. Controlled by alpha
- **Type II** (false negative): missing a real effect. Power = 1 - beta
- **p-value**: probability of observing data as extreme as ours, assuming H0 is true

### Common Tests

| Test | Use Case | Assumptions |
|------|----------|-------------|
| t-test (Student's) | Compare means of two groups | ~Normal, similar variance |
| Welch's t-test | Compare means, unequal variance | ~Normal |
| Mann-Whitney U | Compare distributions non-parametrically | Ordinal+ |
| z-test for proportions | Compare binary proportions | Large n |
| Chi-square | Test independence of categoricals | Expected count >= 5 |
| ANOVA | Compare means of 3+ groups | Normal, equal variance |

### Confidence Intervals

```python
from scipy import stats
import numpy as np

data = np.array([...])
confidence = 0.95
n = len(data)
mean = data.mean()
se = stats.sem(data)  # standard error
ci = stats.t.interval(confidence, df=n-1, loc=mean, scale=se)
```

For mean with known variance: x_bar +/- z_(alpha/2) * sigma / sqrt(n)
For mean with unknown variance: x_bar +/- t_(alpha/2, n-1) * s / sqrt(n)

## A/B Testing

Compare two versions (A=control, B=test) on independent user groups. Measure business metrics.

### Why Not Just Offline Metrics?

Offline model metrics (precision, NDCG) don't directly measure business impact. Companies care about: session length, clicks, conversions, retention, revenue. A/B tests connect model changes to real user behavior.

### Experimental Design

1. **Split users** into control/test groups (hash-based: `hash(user_id + salt) % 100`)
2. **Run for fixed period** (don't peek and stop early)
3. **Compare metrics** between groups
4. **Apply statistical tests** for significance

### Test Power

Power = probability of detecting a real effect. Influenced by:
- **Sample size**: more users = more power (main lever)
- **Effect size**: larger effects are easier to detect
- **Variance**: lower variance = more power (use CUPED)
- **Significance level**: higher alpha = more power but more false positives

### CUPED (Controlled-experiment Using Pre-Experiment Data)

Reduces metric variance by 20-30% using pre-experiment data.

```
Y_cuped = Y - theta * X
theta* = cov(Y, X) / Var(X)
Var(Y_cuped) = Var(Y) * (1 - rho^2(Y, X))
```

Higher correlation between pre- and during-experiment metric = more variance reduction.

### Measuring CTR

CTR = clicks / views. Problem: individual clicks aren't independent (same user generates multiple).

**Solutions:**
- **Per-user aggregation**: aggregate clicks per user, then t-test
- **Bootstrap**: resample users with replacement, compute CTR per sample
- **Bucketing**: hash users into ~100 buckets, compute CTR per bucket, t-test on buckets
- **Linearization**: LinearizedCTR = clicks - A * views (A = global CTR from control)

### Threats to Validity

- **Novelty effect**: new users overreact positively. Inflates results
- **Change aversion**: experienced users resist changes. Increases false negatives
- **Detection**: compare effect between new vs experienced users
- **SRM** (Sample Ratio Mismatch): groups aren't equal size - indicates broken randomization

### When A/B Tests Are Impossible

- **Two-sided marketplaces** (taxi, delivery): affecting one side impacts the other
- **Visible features**: users in different groups see each other's experience
- **Feature already live**: can't run reverse test

**Alternatives:**
- **Switchback testing**: alternate algorithms across geography x time slots
- **Synthetic control**: deploy everywhere, compare to predicted baseline from control regions
- **Difference-in-Differences**: compare treatment vs control before/after intervention
- **Propensity Score Matching**: match treatment units to similar control units

## Causal Inference Methods

| Method | Strength | When to Use |
|--------|----------|-------------|
| Randomized A/B | Gold standard | Full control over assignment |
| DiD | Moderate | Can't randomize, have before/after data |
| PSM | Moderate | Can't randomize, have covariates |
| Synthetic Control | Weak | Can't split at all, have control regions |

## Gotchas
- **Peeking problem**: checking results daily and stopping when significant inflates false positive rate. Use sequential testing (SPRT) if you must peek
- **Multiple comparisons**: testing 20 metrics at alpha=0.05 means ~1 will be "significant" by chance. Apply Bonferroni correction
- **P-hacking**: trying many analyses until one is significant. Pre-register analysis plan
- **Accuracy trap with A/B**: 1% increase in CTR can be worth millions - don't dismiss small but significant effects
- **Don't stockpile results**: seasonality means last quarter's results may not generalize

## See Also
- [[probability-distributions]] - underlying theory
- [[descriptive-statistics]] - summarizing data before testing
- [[bi-dashboards]] - presenting experiment results
- [[model-evaluation]] - offline metrics that complement A/B tests
