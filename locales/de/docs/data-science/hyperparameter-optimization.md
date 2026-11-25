---
title: "Hyperparameter-Optimierung"
category: tools
tags: [data-science, hyperparameter-tuning, optuna, grid-search, bayesian-optimization]
level: 4
source_sha256: 90f189613fd19ddbc12b968feb59adf4b2af2e458fde8dc0442494cb924d2667
translation: machine
translated_at: '2026-10-24'
---
# Hyperparameter-Optimierung {#hyperparameter-optimization}

Systematische Suche nach der besten Modellkonfiguration. Hyperparameter steuern das Trainingsverhalten (Lernrate, Regularisierung, Architektur), können aber nicht aus den Daten gelernt werden. Sorgfältiges Tuning ist oft wichtiger als die Wahl des Algorithmus.

## Suchstrategien {#search-strategies}

### Grid Search {#grid-search}

Erschöpfende Suche über ein vorgegebenes Parameterraster. Einfach, aber exponentiell aufwendig.

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

3 x 4 x 3 x 2 = 72 Kombinationen x 5 Folds = 360 Fits. Skaliert schlecht.

### Random Search {#random-search}

Zufällige Kombinationen werden gezogen. Findet oft schneller gute Lösungen als Grid Search, da jede Dimension stärker abgedeckt wird.

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

### Bayesian Optimization (Optuna) {#bayesian-optimization-optuna}

Nutzt die Ergebnisse bisheriger Trials, um die Suche in vielversprechende Bereiche zu lenken. Am effizientesten bei teuren Evaluierungen.

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

### Erweiterte Optuna-Funktionen {#optuna-advanced-features}

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

## Hyperparameter neuronaler Netze {#neural-network-hyperparameters}

Wichtige Parameter für das Tuning von Deep Learning:

| Parameter | Typischer Bereich | Hinweise |
|-----------|--------------|-------|
| Lernrate | 1e-5 bis 1e-2 | Am wichtigsten. Logarithmische Skala verwenden |
| Batch-Größe | 16 bis 512 | Größer = schneller, aber verrauschtere Gradienten |
| Weight Decay | 1e-6 bis 1e-2 | L2-Regularisierung |
| Dropout | 0.0 bis 0.5 | Pro Schicht, typischerweise 0.1–0.3 |
| Hidden Dim | 32 bis 1024 | Zweierpotenzen bevorzugt |
| Anzahl Schichten | 1 bis 8 | Abnehmender Nutzen |
| Warmup-Schritte | 100 bis 2000 | Für Transformer |

### Learning-Rate-Finder {#learning-rate-finder}

```python
# PyTorch Lightning LR finder
trainer = pl.Trainer(auto_lr_find=True)
trainer.tune(model, datamodule)

# Manual: train for a few hundred steps with exponentially increasing LR
# Plot loss vs LR, pick LR where loss decreases fastest
```

## Praktische Tipps {#practical-tips}

**Suchreihenfolge** (von am wirkungsvollsten bis am wenigsten):
1. Lernrate (immer zuerst tunen)
2. Batch-Größe / Anzahl der Schichten
3. Regularisierung (Dropout, Weight Decay)
4. Architektur (Hidden Dims, Anzahl Heads)
5. Optimiererspezifisch (Momentum, beta1/beta2)

**Budgetverteilung**: 80 % des Budgets auf die 2–3 wichtigsten Parameter verwenden. Die übrigen auf sinnvollen Standardwerten festhalten.

**Reproduzierbarkeit**: Immer Random Seeds setzen und alle Parameter inklusive Bibliotheksversionen protokollieren.

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

## Fallstricke {#gotchas}

- **Überanpassung an das Validierungsset**: Werden Tausende Trials auf demselben Validierungsfold ausgeführt, wird faktisch auf diesem "trainiert". Nested Cross-Validation verwenden: innere Schleife für HPO, äußere Schleife für eine unverzerrte Evaluierung. Alternativ ein finales Testset zurückhalten, das während des Tunings NIE verwendet wird
- **Logarithmische Skala für Lernrate und Regularisierung**: Wird die Lernrate linear zwischen 0.001 und 0.1 durchsucht, landen die meisten Trials nahe 0.1. `log=True` in Optuna oder `loguniform` in sklearn verwenden. Dasselbe gilt für Weight Decay, reg_alpha und reg_lambda
- **Early Stopping und n_estimators interagieren**: Wird Early Stopping bei Gradient Boosting verwendet, sollte n_estimators nicht zusätzlich getunt werden, da sich beides widerspricht. n_estimators hoch ansetzen (10000) und Early Stopping die passende Anzahl finden lassen. Stattdessen early_stopping_rounds tunen

## Siehe auch {#see-also}

- [[model-evaluation]]
- [[gradient-boosting]]
- [[ensemble-methods]]
- [[neural-networks]]
