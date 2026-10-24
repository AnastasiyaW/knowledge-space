---
title: "Méthodes d'ensemble"
category: concepts
tags: [data-science, ensemble, bagging, boosting, stacking, voting]
level: 3
source_sha256: 904c045fc2b890bfc9a72bda7b443b90344d9c7e92129e6689086ef0659cb0a6
translation: machine
translated_at: '2026-10-24'
---
# Méthodes d'ensemble {#ensemble-methods}

Combiner plusieurs modèles pour produire de meilleures prédictions que n'importe quel modèle isolé. Trois grandes stratégies : le bagging (parallèle, réduit la variance), le boosting (séquentiel, réduit le biais) et le stacking (apprendre comment combiner).

## Bagging (Bootstrap Aggregating) {#bagging-bootstrap-aggregating}

Entraîner plusieurs modèles sur des échantillons bootstrap (échantillonnage aléatoire avec remise), puis agréger les prédictions par vote (classification) ou par moyenne (régression).

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

**Random Forest** est du bagging auquel on ajoute un sous-ensemble aléatoire de variables à chaque division. C'est la méthode de bagging la plus performante.

**Pourquoi ça fonctionne** : le bagging réduit la variance en moyennant des prédictions décorrélées. Chaque modèle voit des données différentes et commet des erreurs différentes. Les erreurs se compensent lors de l'agrégation.

## Boosting {#boosting}

Entraîner séquentiellement des apprenants faibles, chacun se concentrant sur les erreurs des précédents.

### AdaBoost {#adaboost}

Augmente le poids des échantillons mal classés :

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

### Gradient Boosting (XGBoost / LightGBM / CatBoost) {#gradient-boosting-xgboost-lightgbm-catboost}

Ajuste un nouvel arbre sur les résidus (gradient de la fonction de perte). Voir [[gradient-boosting]] pour une comparaison détaillée.

### Principaux paramètres du boosting {#key-boosting-parameters}

| Paramètre | Effet | Plage typique |
|-----------|--------|---------------|
| n_estimators | Nombre d'arbres | 100-10000 |
| learning_rate | Réduction par arbre | 0.01-0.3 |
| max_depth | Complexité de l'arbre | 3-10 |
| subsample | Ratio d'échantillonnage des lignes | 0.5-1.0 |
| colsample_bytree | Échantillonnage des variables | 0.5-1.0 |
| reg_alpha (L1) | Parcimonie | 0-10 |
| reg_lambda (L2) | Lissage | 0-10 |

**Règle empirique** : un taux d'apprentissage plus faible combiné à davantage d'arbres donne de meilleurs résultats, mais un entraînement plus lent. Utiliser l'arrêt anticipé (early stopping).

## Stacking {#stacking}

Entraîner un méta-apprenant sur les prédictions des modèles de base :

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

**Stacking multi-niveaux** : modèles de base -> méta-apprenant de niveau 1 -> méta-apprenant de niveau 2. Les gains deviennent marginaux au-delà de 2 niveaux. Populaire dans Kaggle, mais rarement justifié par sa complexité en production.

## Voting {#voting}

Combinaison simple de modèles diversifiés :

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

## Blending {#blending}

Plus simple que le stacking : on utilise un ensemble de validation (holdout) à la place de la validation croisée :

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

## Diversité des modèles {#model-diversity}

Les ensembles fonctionnent au mieux lorsque les modèles de base commettent des **erreurs différentes** :

- **Algorithmes différents** : arbre + linéaire + réseau de neurones
- **Variables différentes** : sous-ensembles, prétraitements différents
- **Hyperparamètres différents** : arbres peu profonds et profonds
- **Données d'entraînement différentes** : bootstrap, fenêtres temporelles différentes

La corrélation entre les erreurs des modèles est l'ennemi des ensembles. Deux modèles ayant chacun 80 % de précision mais des erreurs non corrélées donnent un ensemble à environ 96 %. Deux modèles corrélés à 80 % restent à environ 80 %.

## Pièges à éviter {#gotchas}

- **Le stacking sans validation croisée fuit** : si vous entraînez les modèles de base sur toutes les données d'entraînement puis utilisez ces mêmes prédictions pour entraîner le méta-apprenant, les prédictions des modèles de base sur les données d'entraînement sont surapprises. Utilisez toujours des prédictions out-of-fold pour l'ensemble d'entraînement du méta-apprenant
- **Rendements décroissants** : passer de 1 à 3-5 modèles diversifiés apporte le gain le plus important. Ajouter le 50e modèle n'aide presque pas. En production, la complexité de maintenance de nombreux modèles dépasse souvent le gain marginal de précision. Commencez par 3 modèles diversifiés
- **Le boosting sur-apprend avec des labels bruités** : le boosting se concentre sur les exemples difficiles ; si ceux-ci sont mal étiquetés, il mémorise le bruit. Utilisez l'arrêt anticipé et validez sur un holdout propre. Si le bruit d'étiquetage est connu, privilégiez le bagging ou utilisez le lissage des labels (label smoothing)

## Voir aussi {#see-also}

- [[gradient-boosting]]
- [[model-evaluation]]
- [[hyperparameter-optimization]]
