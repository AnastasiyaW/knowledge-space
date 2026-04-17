---
title: Ensemble Methods
category: concepts
tags: [data-science, ensemble, bagging, boosting, stacking, voting]
---

# Ensemble Methods

Combining multiple models to produce better predictions than any single model. Three main strategies: bagging (parallel, reduce variance), boosting (sequential, reduce bias), stacking (learn how to combine).

## Bagging (Bootstrap Aggregating)

Train multiple models on bootstrap samples (random sampling with replacement), aggregate predictions by voting (classification) or averaging (regression).

```python
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bagging = BaggingClassifier(
    estimator=DecisionTreeClassifier(max_depth=None),
    n_estimators=50,
    max_samples=0.8,    # 80% of data per base model
    max_features=0.8,   # 80% of features per base model
    bootstrap=True,
    oob_score=True,     # out-of-bag estimate (free validation)
    random_state=42
)
bagging.fit(X_train, y_train)
print(f"OOB score: {bagging.oob_score_:.3f}")
```

**Random Forest** is bagging + random feature subsets at each split. The most successful bagging method.

**Why it works**: reduces variance by averaging decorrelated predictions. Each model sees different data, makes different errors. Errors cancel out in aggregation.

## Boosting

Sequentially train weak learners, each focusing on mistakes of previous ones.

### AdaBoost

Increases weight of misclassified samples:

```python
from sklearn.ensemble import AdaBoostClassifier

ada = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),  # stumps
    n_estimators=200,
    learning_rate=0.1,
    random_state=42
)
ada.fit(X_train, y_train)
```

### Gradient Boosting (XGBoost / LightGBM / CatBoost)

Fits new tree to residuals (gradient of loss function). See [[gradient-boosting]] for detailed comparison.

### Key Boosting Parameters

| Parameter | Effect | Typical Range |
|-----------|--------|---------------|
| n_estimators | Number of trees | 100-10000 |
| learning_rate | Shrinkage per tree | 0.01-0.3 |
| max_depth | Tree complexity | 3-10 |
| subsample | Row sampling ratio | 0.5-1.0 |
| colsample_bytree | Feature sampling | 0.5-1.0 |
| reg_alpha (L1) | Sparsity | 0-10 |
| reg_lambda (L2) | Smoothing | 0-10 |

**Rule of thumb**: lower learning rate + more trees = better but slower. Use early stopping.

## Stacking

Train a meta-learner on predictions of base models:

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

stack = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('xgb', XGBClassifier(n_estimators=200)),
        ('svm', SVC(probability=True))],
    final_estimator=LogisticRegression(),
    cv=5,  # use cross-val predictions to prevent leakage
    stack_method='predict_proba'  # use probabilities not hard labels
)
stack.fit(X_train, y_train)
```

**Multi-level stacking**: base models -> level-1 meta-learner -> level-2 meta-learner. Diminishing returns after 2 levels. Popular in Kaggle but rarely worth complexity in production.

## Voting

Simple combination of diverse models:

```python
from sklearn.ensemble import VotingClassifier

# Hard voting: majority vote
hard_vote = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression()),
        ('rf', RandomForestClassifier()),
        ('svm', SVC())
    ],
    voting='hard'
)

# Soft voting: average probabilities (usually better)
soft_vote = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression()),
        ('rf', RandomForestClassifier()),
        ('svm', SVC(probability=True))
    ],
    voting='soft',
    weights=[1, 2, 1]  # weight better models higher
)
```

## Blending

Simpler than stacking - use holdout set instead of cross-validation:

```python
# Split: train -> base_train + blend_set
X_base, X_blend, y_base, y_blend = train_test_split(
    X_train, y_train, test_size=0.3, random_state=42
)

# Train base models on base_train
models = [rf.fit(X_base, y_base), xgb.fit(X_base, y_base)]

# Generate blend features
blend_features = np.column_stack([
    m.predict_proba(X_blend)[:, 1] for m in models
])

# Train meta-model on blend_set
meta = LogisticRegression()
meta.fit(blend_features, y_blend)
```

## Model Diversity

Ensembles work best when base models make **different errors**:

- **Different algorithms**: tree + linear + neural net
- **Different features**: subsets, different preprocessing
- **Different hyperparameters**: shallow + deep trees
- **Different training data**: bootstrap, different time windows

Correlation between model errors is the enemy of ensembles. Two models with 80% accuracy but uncorrelated errors ensemble to ~96%. Two correlated 80% models stay at ~80%.

## Gotchas

- **Stacking without cross-validation leaks**: if you train base models on all training data and then use those same predictions to train the meta-learner, base model predictions on training data are overfit. Always use out-of-fold predictions for the meta-learner training set
- **Diminishing returns**: going from 1 model to 3-5 diverse models gives biggest improvement. Adding model 50 barely helps. In production, the complexity of maintaining many models often outweighs the marginal accuracy gain. Start with 3 diverse models
- **Boosting overfits with noisy labels**: boosting focuses on hard examples - if those are mislabeled, it memorizes noise. Use early stopping and validate on clean holdout. If label noise is known, prefer bagging or use label smoothing

## See Also

- [[gradient-boosting]]
- [[model-evaluation]]
- [[hyperparameter-optimization]]
