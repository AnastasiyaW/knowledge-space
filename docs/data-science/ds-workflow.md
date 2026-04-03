---
title: Data Science Workflow and Best Practices
category: practices
tags: [data-science, workflow, methodology, best-practices]
---

# Data Science Workflow and Best Practices

End-to-end project methodology. The difference between a toy model and a production-ready solution is process discipline.

## Project Workflow

### 1. Problem Definition
- Understand business goal (not just ML goal)
- Define success metric (both ML metric AND business metric)
- Determine if ML is even needed - sometimes simple rules suffice

### 2. Data Collection
- SQL queries from databases
- API calls, CSV/Excel from stakeholders
- Feature stores / data warehouses
- Web scraping (with permission)

### 3. EDA (Exploratory Data Analysis)
- Shape, dtypes, `describe()`
- Missing values (percentage per column)
- Target distribution (balanced? skewed?)
- Univariate: histograms (numeric), value_counts (categorical)
- Bivariate: correlation matrix, groupby + target mean
- Outliers: box plots, z-scores, IQR method

### 4. Preprocessing
- Handle missing values (impute or drop)
- Handle outliers (cap, remove, or keep)
- Encode categoricals
- Scale numerical features
- Create train/validation/test splits
- Feature engineering

### 5. Modeling
- Start with simple baseline (mean prediction, logistic regression)
- Try multiple model families (linear, tree-based, ensemble)
- Use cross-validation for reliable estimates
- Track experiments

### 6. Evaluation
- Compare against baseline
- Check for overfitting (train vs val gap)
- Error analysis: what does the model get wrong?
- Feature importance
- Final evaluation on held-out test set ONCE

### 7. Deployment
- Export model (pickle, ONNX, model.save())
- Create prediction API (Flask, FastAPI)
- Set up monitoring (data drift, model degradation)
- A/B test in production

## Common Pitfalls

### Data Leakage
Information from the future or test set leaking into training. **Most dangerous mistake.**

- **Target leakage**: feature derived from or correlated with target
- **Train-test leakage**: preprocessing fit on full dataset including test
- **Temporal leakage**: using future data to predict past

**Prevention**: always split BEFORE any preprocessing. Use sklearn Pipelines.

### Overfitting
Model memorizes training data, fails on new data.
- **Symptoms**: large gap between train and val performance
- **Solutions**: regularization, simpler model, more data, early stopping, dropout, CV

### Class Imbalance
One class vastly outnumbers others (99% negative, 1% positive).
- **Problem**: model predicts majority class and gets high accuracy
- **Solutions**: class weights, SMOTE/oversampling, undersampling, F1/PR-AUC metrics

### Selection Bias
- **Survivorship bias**: only seeing successful examples
- **Sampling bias**: non-random data collection

## Reproducibility

```python
import numpy as np
import random
import torch

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

# sklearn
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=SEED)
```

**Checklist:**
- Pin library versions in requirements.txt
- Document data sources and preprocessing steps
- Save trained models and parameters
- Version control (git) for code
- Record experiment results

## Communication

- **Start with business impact**, not the model
- Show metrics business understands (revenue, cost savings)
- Explain limitations and edge cases
- Use visualizations (confusion matrix heatmap, feature importance)
- Provide confidence intervals, not just point estimates

## Gotchas
- Spending weeks on modeling when the problem is bad data quality
- Optimizing the wrong metric (high accuracy on imbalanced data)
- Not comparing to a simple baseline first
- Deploying without monitoring - models degrade silently
- Ignoring domain experts who understand the data better than any algorithm

## See Also
- [[model-evaluation]] - metrics and validation strategies
- [[feature-engineering]] - the highest-ROI step
- [[pandas-eda]] - practical EDA implementation
- [[hypothesis-testing]] - A/B testing deployed models
