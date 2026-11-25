---
title: "Gradient Boosting et modèles à base d'arbres"
category: models
tags: [data-science, ml, catboost, xgboost, lightgbm, random-forest, ensemble]
level: 3
source_sha256: 25e8afc890bca06615fe52b8c41315a4daf40e507fb8a084e3cb1df06665b1d2
translation: machine
translated_at: '2026-10-24'
---
# Gradient Boosting et modèles à base d'arbres {#gradient-boosting-and-tree-based-models}

Le gradient boosting est l'algorithme dominant pour les données tabulaires. CatBoost, LightGBM et XGBoost sont des implémentations de la même idée. Les modèles à base d'arbres gèrent les types de données mixtes, les relations non linéaires et les interactions sans ingénierie de features manuelle.

## Arbres de décision {#decision-trees}

Brique de base. Découpe récursivement les données sur des seuils de features afin de minimiser l'impureté.

**Critères de découpage :**
- **Impureté de Gini** : sum(p_i * (1 - p_i)). Mesure la probabilité de mauvaise classification
- **Entropie** : -sum(p_i * log(p_i)). Mesure de désordre issue de la théorie de l'information
- **MSE** (régression) : variance au sein de chaque découpage

**Avantages** : interprétables, gèrent les types mixtes, pas de mise à l'échelle nécessaire.
**Inconvénients** : forte variance, sujets au surapprentissage, instables (de petites variations des données -> un arbre différent).

## Random Forest {#random-forest}

Ensemble d'arbres de décision. Chaque arbre est entraîné sur un échantillon bootstrap avec un sous-ensemble aléatoire de features.

```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train, y_train)
rf.feature_importances_  # built-in importance scores
```

- **Bagging** réduit la variance en moyennant des prédictions décorrélées
- Importance des features : diminution de l'impureté lors des découpages sur une feature
- Embarrassingly parallel - chaque arbre s'entraîne indépendamment

## Gradient Boosting {#gradient-boosting}

Construction séquentielle d'arbres, chacun corrigeant les erreurs des précédents.

**Idée** : ajuster un arbre aux résidus (erreurs) du modèle courant, puis l'ajouter avec un faible learning rate.

### CatBoost {#catboost}

Meilleures performances par défaut. Gère nativement les variables catégorielles.

```python
from catboost import CatBoostRegressor, CatBoostClassifier

model = CatBoostRegressor(cat_features=['transmission', 'fuel_type'])
model.fit(
    train[features], train[target],
    eval_set=(val[features], val[target]),
    verbose=100
)

# Predictions
y_pred = model.predict(test[features])

# Classification: get probabilities
model = CatBoostClassifier(cat_features=cat_features)
model.fit(train[features], train[target],
          eval_set=(val[features], val[target]))
scores = model.predict_proba(test[features])[:, 1]

# Feature importance
model.get_feature_importance(prettified=True)
```

**Un jeu de validation est obligatoire** : CatBoost s'entraîne itérativement. Sans validation, il mémorise les données d'entraînement. L'early stopping s'arrête au minimum de l'erreur de validation.

### Validation croisée avec CatBoost {#catboost-cross-validation}

```python
from catboost import cv, Pool

cv_data = cv(
    pool=Pool(X, y, cat_features=cat_features),
    params={'loss_function': 'Logloss', 'eval_metric': 'AUC'},
    fold_count=5, shuffle=True, stratified=True,
    partition_random_seed=42, verbose=False
)
best_iter = cv_data['test-AUC-mean'].idxmax()
```

**Workflow** : CV pour trouver le nombre optimal d'itérations -> entraîner le modèle final sur train+val complet avec ce nombre -> évaluer sur le test.

### XGBoost {#xgboost}

```python
import xgboost as xgb
model = xgb.XGBClassifier(
    n_estimators=500, max_depth=6, learning_rate=0.1,
    subsample=0.8, colsample_bytree=0.8,
    early_stopping_rounds=50, eval_metric='auc'
)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=50)
```

### LightGBM {#lightgbm}

Le plus rapide pour les grands jeux de données. Croissance par feuille (leaf-wise) plutôt que par niveau (level-wise).

```python
import lightgbm as lgb
model = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=31)
model.fit(X_train, y_train, eval_set=[(X_val, y_val)],
          callbacks=[lgb.early_stopping(50)])
```

## Hyperparamètres clés {#key-hyperparameters}

| Paramètre | Effet | Plage typique |
|-----------|-------|---------------|
| n_estimators / iterations | Nombre d'arbres | 100-5000 |
| learning_rate | Taille du pas par arbre | 0.01-0.3 |
| max_depth | Profondeur de l'arbre | 3-10 |
| subsample | Fraction de lignes par arbre | 0.5-1.0 |
| colsample_bytree | Fraction de features par arbre | 0.5-1.0 |
| min_child_weight | Nombre minimal d'échantillons par feuille | 1-100 |
| reg_lambda (L2) | Régularisation L2 | 0-10 |
| reg_alpha (L1) | Régularisation L1 | 0-10 |

**Règle empirique** : learning_rate plus faible + plus d'estimateurs = meilleur résultat mais plus lent. Commencer avec les valeurs par défaut, régler d'abord learning_rate et max_depth.

## Gestion des classes déséquilibrées {#handling-imbalanced-classes}

```python
# CatBoost
model = CatBoostClassifier(scale_pos_weight=neg_count/pos_count)

# XGBoost
model = xgb.XGBClassifier(scale_pos_weight=neg_count/pos_count)

# Or: tune threshold on validation set
```

## Comparaison {#comparison}

| Aspect | CatBoost | XGBoost | LightGBM | Random Forest |
|--------|----------|---------|----------|---------------|
| Performance par défaut | Meilleure | Bonne | Bonne | Bonne |
| Gestion des catégorielles | Native | Encodage manuel | Native | Encodage manuel |
| Vitesse | Modérée | Modérée | La plus rapide | Rapide (parallèle) |
| Risque de surapprentissage | Faible | Modéré | Modéré | Faible |
| Support GPU | Oui | Oui | Oui | Non |

## Pièges à éviter {#gotchas}
- **Ne pas utiliser l'accuracy** sur des jeux de données déséquilibrés : un modèle prédisant toujours 0 obtient 80 % d'accuracy avec une répartition 80/20
- CatBoost sans eval_set surapprend silencieusement : toujours fournir une validation
- L'importance des features varie selon les exécutions et les méthodes : utiliser la permutation importance pour plus de fiabilité
- XGBoost nécessite un encodage one-hot manuel pour les catégorielles (sauf avec `enable_categorical=True`)
- Commencer simple (valeurs par défaut) avant le réglage des hyperparamètres : le réglage ne compense pas de mauvaises features

## Voir aussi {#see-also}
- [[model-evaluation]] - métriques pour comparer les modèles
- [[feature-engineering]] - moins critique pour les arbres mais toujours utile
- [[linear-models]] - alternative plus simple, utile comme baseline
- [[neural-networks]] - lorsque les modèles tabulaires ne suffisent pas
