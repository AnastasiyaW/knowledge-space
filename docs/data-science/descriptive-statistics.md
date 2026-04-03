---
title: Descriptive Statistics
category: concepts
tags: [data-science, statistics, eda, fundamentals]
---

# Descriptive Statistics

Quantitative summaries of data distributions. The foundation of EDA - always compute these before modeling. Understanding central tendency, spread, and shape tells you which models and preprocessing steps are appropriate.

## Measures of Central Tendency

- **Mean**: sum / count. Sensitive to outliers. `df['col'].mean()`
- **Median**: middle value when sorted. Robust to outliers. `df['col'].median()`
- **Mode**: most frequent value. Can be multimodal. `df['col'].mode()`

**Mean vs median reveals skewness:**
- Mean > median: right-skewed (few high values pull mean up) - e.g., income distributions
- Mean < median: left-skewed (few low values pull mean down) - e.g., exam scores
- Mean ~ median: roughly symmetric

## Measures of Spread

```python
import numpy as np
from scipy import stats

salary_range = df['income'].max() - df['income'].min()  # range
salary_var = df['income'].var()                          # variance
salary_std = df['income'].std()                          # standard deviation
iqr = df['income'].quantile(0.75) - df['income'].quantile(0.25)  # IQR
```

- **Range**: max - min. Simple but extremely sensitive to outliers
- **Variance**: average squared deviation from mean. Units are squared
- **Standard deviation**: sqrt(variance). Same units as data - easier to interpret
- **IQR** (Interquartile Range): Q3 - Q1. Robust spread measure used for outlier detection

## Measures of Shape

**Skewness** - asymmetry of distribution:
```python
skewness = stats.skew(df['income'])
# > 0: right-skewed (long right tail)
# < 0: left-skewed (long left tail)
# ~ 0: symmetric
```

**Kurtosis** - tail heaviness relative to normal:
```python
kurtosis = stats.kurtosis(df['income'])
# > 0 (leptokurtic): heavy tails, sharp peak - more extreme values
# < 0 (platykurtic): light tails, flat peak
# ~ 0 (mesokurtic): similar to normal
```

**Why shape matters**: guides preprocessing (log transform for skewed features), outlier detection (leptokurtic = more extremes), model selection (linear models assume roughly normal residuals).

## Measures of Position

```python
# Percentiles
p25, p50, p75 = np.percentile(df['income'], [25, 50, 75])

# Quartiles via describe()
df['income'].describe()
# count, mean, std, min, 25%, 50%, 75%, max
```

## Z-Scores

Z = (X - mu) / sigma. Number of standard deviations from the mean.

```python
z_scores = stats.zscore(df['income'])
# |z| > 2: unusual (5% of normal data)
# |z| > 3: extreme outlier (0.3% of normal data)
```

**68-95-99.7 rule** (empirical rule for normal distributions):
- ~68% of data within 1 std of mean
- ~95% within 2 std
- ~99.7% within 3 std

## Correlation

Measures strength and direction of relationship between two variables. Range: [-1, +1].

```python
# Pearson - linear relationships, assumes normality
pearson_r = df['income'].corr(df['experience'])

# Full correlation matrix
corr_matrix = df.corr()

# Spearman - monotonic (not just linear), rank-based, no normality assumption
spearman_r = df['income'].corr(df['experience'], method='spearman')

# Kendall - concordant/discordant pairs, robust to outliers, good for small samples
kendall_tau = df['income'].corr(df['experience'], method='kendall')
```

| Method | Measures | Assumptions | Use When |
|--------|----------|-------------|----------|
| Pearson | Linear relationship | Normality, homoscedasticity | Both continuous, roughly normal |
| Spearman | Monotonic relationship | None (rank-based) | Ordinal data, non-linear monotonic |
| Kendall | Concordance | None (rank-based) | Small samples, ordinal data |

**Correlation does NOT imply causation.** Ice cream sales correlate with drowning rates (confounding: hot weather).

## Sample vs Population

- **Population** (mu, sigma): entire set of interest. Rarely fully observable
- **Sample** (x_bar, s): subset used to estimate population parameters
- Larger sample = sample statistics closer to population parameters

## Gotchas
- Using mean on heavily skewed data without reporting median
- Pearson correlation = 0 does NOT mean no relationship (could be non-linear)
- Range is nearly useless for comparing distributions (dominated by single outliers)
- `df.describe()` only shows numeric columns by default - use `include='all'` or `include='object'`

## See Also
- [[probability-distributions]] - theoretical distributions underlying data
- [[pandas-eda]] - computing these statistics in pandas
- [[data-visualization]] - visualizing distributions
- [[hypothesis-testing]] - testing whether observed differences are significant
