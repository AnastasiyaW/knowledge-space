---
title: Descriptive Statistics
category: statistics
tags: [statistics, mean, median, variance, correlation, eda, outliers]
---

# Descriptive Statistics

Numerical summaries that describe the center, spread, and shape of a dataset. Always the first step in any data analysis pipeline before modeling. Central to [[feature-engineering]] decisions and [[data-visualization]].

## Key Facts

- **Measures of central tendency**: mean (sensitive to outliers), median (robust), mode (most frequent)
- **Measures of spread**: variance, std deviation, range, IQR (interquartile range = Q3 - Q1)
- **Skewness**: asymmetry of distribution; positive = right tail longer; negative = left tail longer
- **Kurtosis**: tail heaviness; high kurtosis = heavy tails, more outliers
- **Percentiles/quantiles**: Q1 (25th), Q2 (50th = median), Q3 (75th); boxplots visualize these
- **Correlation**: Pearson (linear relationship, -1 to +1), Spearman (monotonic, rank-based), Kendall (ordinal)
- **Covariance**: unstandardized correlation; hard to interpret without normalization
- **Outliers**: common rule: below Q1 - 1.5*IQR or above Q3 + 1.5*IQR; or z-score > 3
- Correlation does NOT imply causation
- **Standard error** = std / sqrt(n); measures precision of sample mean estimate
- For [[regression-models]], always check distribution of residuals and target variable

## Patterns

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'age': [25, 30, 35, 40, 45, 200],  # 200 is outlier
    'salary': [30000, 45000, 55000, 60000, 70000, 500000]
})

# Central tendency
df['age'].mean()      # 62.5 (skewed by outlier)
df['age'].median()    # 37.5 (robust)
df['age'].mode()      # all unique -> all values

# Spread
df['age'].std()       # std deviation (ddof=1 by default in pandas)
df['age'].var()       # variance
df['age'].quantile([0.25, 0.5, 0.75])  # quartiles

# Full summary
df.describe()  # count, mean, std, min, 25%, 50%, 75%, max

# Correlation matrix
df.corr(method='pearson')    # default
df.corr(method='spearman')   # rank-based, robust to outliers

# Skewness and kurtosis
df['salary'].skew()    # positive = right-skewed
df['salary'].kurtosis()

# Detect outliers with IQR
Q1 = df['salary'].quantile(0.25)
Q3 = df['salary'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['salary'] < Q1 - 1.5 * IQR) | (df['salary'] > Q3 + 1.5 * IQR)]

# Z-score outlier detection
from scipy.stats import zscore
df['z_salary'] = zscore(df['salary'])
outliers_z = df[df['z_salary'].abs() > 3]

# Grouped statistics
# df.groupby('category')['value'].agg(['mean', 'median', 'std', 'count'])
```

## Gotchas

- `pandas.std()` uses ddof=1 (sample std), `numpy.std()` uses ddof=0 (population std) by default -- they give different results
- Pearson correlation only captures LINEAR relationships; use Spearman for monotonic non-linear
- Mean of percentages != percentage of totals (Simpson's paradox)
- Always visualize before trusting summary statistics -- Anscombe's quartet has identical stats but wildly different patterns
- Correlation matrix on one-hot encoded features is misleading

## See Also

- [[data-visualization]] - always plot distributions alongside computing statistics
- [[feature-engineering]] - statistics guide feature transformations (log for skewed data)
- [[hypothesis-testing]] - formal comparison of group statistics
- pandas describe docs: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html
