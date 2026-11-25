---
title: "Optimisation des hyperparamètres"
category: tools
tags: [data-science, hyperparameter-tuning, optuna, grid-search, bayesian-optimization]
level: 4
source_sha256: 90f189613fd19ddbc12b968feb59adf4b2af2e458fde8dc0442494cb924d2667
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des hyperparamètres {#hyperparameter-optimization}

Recherche systématique de la meilleure configuration de modèle. Les hyperparamètres contrôlent le comportement de l'entraînement (taux d'apprentissage, régularisation, architecture) mais ne peuvent pas être appris à partir des données. Un bon réglage compte souvent davantage que le choix de l'algorithme.

## Stratégies de recherche {#search-strategies}

### Recherche par grille {#grid-search}

Recherche exhaustive sur une grille de paramètres spécifiée. Simple, mais d'un coût exponentiel.

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

3 x 4 x 3 x 2 = 72 combinaisons x 5 plis = 360 ajustements. Passe mal à l'échelle.

### Recherche aléatoire {#random-search}

Échantillonne des combinaisons aléatoires. Elle trouve souvent de bonnes solutions plus vite que la recherche par grille, car elle explore davantage chaque dimension.

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

### Optimisation bayésienne (Optuna) {#bayesian-optimization-optuna}

Utilise les résultats des essais passés pour orienter la recherche vers les régions prometteuses. C'est la méthode la plus efficace lorsque les évaluations sont coûteuses.

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

### Fonctionnalités avancées d'Optuna {#optuna-advanced-features}

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

## Hyperparamètres des réseaux de neurones {#neural-network-hyperparameters}

Paramètres clés à régler pour l'apprentissage profond :

| Paramètre | Plage typique | Remarques |
|-----------|--------------|-------|
| Taux d'apprentissage | 1e-5 à 1e-2 | Le plus important. Utiliser une échelle logarithmique |
| Taille de lot | 16 à 512 | Plus grand = plus rapide, gradients plus bruités |
| Weight decay | 1e-6 à 1e-2 | Régularisation L2 |
| Dropout | 0.0 à 0.5 | Par couche, 0.1-0.3 typique |
| Dimension cachée | 32 à 1024 | Puissances de 2 préférées |
| Nombre de couches | 1 à 8 | Rendements décroissants |
| Pas de warmup | 100 à 2000 | Pour les transformers |

### Recherche du taux d'apprentissage (LR finder) {#learning-rate-finder}

```python
# PyTorch Lightning LR finder
trainer = pl.Trainer(auto_lr_find=True)
trainer.tune(model, datamodule)

# Manual: train for a few hundred steps with exponentially increasing LR
# Plot loss vs LR, pick LR where loss decreases fastest
```

## Conseils pratiques {#practical-tips}

**Ordre de recherche** (du plus au moins impactant) :
1. Taux d'apprentissage (toujours régler en premier)
2. Taille de lot / nombre de couches
3. Régularisation (dropout, weight decay)
4. Architecture (dimensions cachées, nombre de têtes)
5. Spécifique à l'optimiseur (momentum, beta1/beta2)

**Allocation du budget** : consacrer 80 % du budget aux 2 ou 3 paramètres les plus importants. Fixer le reste à des valeurs par défaut raisonnables.

**Reproductibilité** : toujours fixer les graines aléatoires, consigner tous les paramètres, y compris les versions des bibliothèques.

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

## Pièges à éviter {#gotchas}

- **Surapprentissage du jeu de validation** : si vous lancez des milliers d'essais sur le même pli de validation, vous vous retrouvez en pratique à « entraîner » sur ce jeu. Utilisez une validation croisée imbriquée : boucle interne pour l'optimisation des hyperparamètres, boucle externe pour une évaluation sans biais. Ou réservez un jeu de test final qui n'est JAMAIS utilisé pendant le réglage
- **Échelle logarithmique pour le taux d'apprentissage et la régularisation** : rechercher le taux d'apprentissage linéairement entre 0.001 et 0.1 gaspille la plupart des essais près de 0.1. Utilisez `log=True` dans Optuna ou `loguniform` dans sklearn. Cela s'applique aussi au weight decay, reg_alpha et reg_lambda
- **L'arrêt anticipé interagit avec n_estimators** : si vous utilisez l'arrêt anticipé en boosting de gradient, ne réglez pas aussi n_estimators, car les deux entrent en conflit. Fixez n_estimators à une valeur élevée (10000) et laissez l'arrêt anticipé trouver le bon nombre. Réglez plutôt early_stopping_rounds

## Voir aussi {#see-also}

- [[model-evaluation]]
- [[gradient-boosting]]
- [[ensemble-methods]]
- [[neural-networks]]
