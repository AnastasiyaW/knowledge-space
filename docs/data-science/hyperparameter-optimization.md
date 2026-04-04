---
title: Hyperparameter Optimization
category: tools
tags: [data-science, hyperparameter-tuning, optuna, grid-search, bayesian-optimization]
---

# Hyperparameter Optimization

Systematic search for the best model configuration. Hyperparameters control training behavior (learning rate, regularization, architecture) but cannot be learned from data. Proper tuning often matters more than algorithm choice.

## Search Strategies

### Grid Search

Exhaustive search over specified parameter grid. Simple but exponentially expensive.

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [3, 5, 7, 10],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 1.0],
}

grid = GridSearchCV(
    XGBClassifier(),
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)
grid.fit(X_train, y_train)
print(f"Best: {grid.best_score_:.3f} with {grid.best_params_}")
```

3 x 4 x 3 x 2 = 72 combinations x 5 folds = 360 fits. Scales badly.

### Random Search

Sample random combinations. Often finds good solutions faster than grid search because it explores more of each dimension.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

param_distributions = {
    'n_estimators': randint(50, 1000),
    'max_depth': randint(2, 15),
    'learning_rate': uniform(0.001, 0.3),
    'subsample': uniform(0.5, 0.5),
    'colsample_bytree': uniform(0.5, 0.5),
    'reg_alpha': uniform(0, 10),
    'reg_lambda': uniform(0, 10),
}

random_search = RandomizedSearchCV(
    XGBClassifier(),
    param_distributions,
    n_iter=100,        # 100 random combinations
    cv=5,
    scoring='f1',
    n_jobs=-1,
    random_state=42
)
random_search.fit(X_train, y_train)
```

### Bayesian Optimization (Optuna)

Uses past trial results to guide search toward promising regions. Most efficient for expensive evaluations.

```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 1000),
        'max_depth': trial.suggest_int('max_depth', 2, 12),
        'learning_rate': trial.suggest_float('learning_rate', 1e-3, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
    }

    model = XGBClassifier(**params, random_state=42, use_label_encoder=False)

    # Cross-validation
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=200, timeout=3600)

print(f"Best F1: {study.best_value:.4f}")
print(f"Best params: {study.best_params}")
```

### Optuna Advanced Features

```python
# Pruning: stop unpromising trials early
from optuna.pruners import MedianPruner

study = optuna.create_study(
    direction='maximize',
    pruner=MedianPruner(n_startup_trials=10, n_warmup_steps=5)
)

# Multi-objective optimization
def multi_objective(trial):
    # ... train model
    return f1_score, inference_time  # optimize both

study = optuna.create_study(directions=['maximize', 'minimize'])

# Visualization
optuna.visualization.plot_optimization_history(study)
optuna.visualization.plot_param_importances(study)
optuna.visualization.plot_parallel_coordinate(study)
```

## Neural Network Hyperparameters

Key parameters to tune for deep learning:

| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| Learning rate | 1e-5 to 1e-2 | Most important. Use log scale |
| Batch size | 16 to 512 | Larger = faster, noisier gradients |
| Weight decay | 1e-6 to 1e-2 | L2 regularization |
| Dropout | 0.0 to 0.5 | Per-layer, 0.1-0.3 typical |
| Hidden dim | 32 to 1024 | Powers of 2 preferred |
| Num layers | 1 to 8 | Diminishing returns |
| Warmup steps | 100 to 2000 | For transformers |

### Learning Rate Finder

```python
# PyTorch Lightning LR finder
trainer = pl.Trainer(auto_lr_find=True)
trainer.tune(model, datamodule)

# Manual: train for a few hundred steps with exponentially increasing LR
# Plot loss vs LR, pick LR where loss decreases fastest
```

## Practical Tips

**Search order** (most to least impactful):
1. Learning rate (always tune first)
2. Batch size / number of layers
3. Regularization (dropout, weight decay)
4. Architecture (hidden dims, num heads)
5. Optimizer-specific (momentum, beta1/beta2)

**Budget allocation**: spend 80% of budget on top 2-3 parameters. Fix the rest at reasonable defaults.

**Reproducibility**: always set random seeds, log all parameters including library versions.

```python
# Reproducible setup
import random
import numpy as np
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
```

## Gotchas

- **Overfitting the validation set**: if you run thousands of trials on the same validation fold, you effectively "train" on it. Use nested cross-validation: inner loop for HPO, outer loop for unbiased evaluation. Or hold out a final test set that is NEVER used during tuning
- **Log-scale for learning rate and regularization**: searching learning rate linearly between 0.001 and 0.1 wastes most trials near 0.1. Use `log=True` in Optuna or `loguniform` in sklearn. Same applies to weight decay, reg_alpha, reg_lambda
- **Early stopping interacts with n_estimators**: if using early stopping in gradient boosting, don't also tune n_estimators - they conflict. Set n_estimators high (10000) and let early stopping find the right number. Tune early_stopping_rounds instead

## See Also

- [[model-evaluation]]
- [[gradient-boosting]]
- [[ensemble-methods]]
- [[neural-networks]]
