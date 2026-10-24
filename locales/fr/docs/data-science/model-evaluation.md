---
title: "Évaluation et validation des modèles"
category: techniques
tags: [data-science, ml, metrics, cross-validation, evaluation]
level: 3
source_sha256: 01a49cc78ad24adadf7d30fa113abd9ee7b4097740526b185591c6ac788f8784
translation: machine
translated_at: '2026-10-24'
---
# Évaluation et validation des modèles {#model-evaluation-and-validation}

Choisir la bonne métrique et la bonne stratégie de validation est aussi important que choisir le modèle. Mauvaise métrique = optimisation de la mauvaise chose. Mauvaise validation = surestimation des performances.

## Métriques de régression {#regression-metrics}

| Métrique | Formule | Quand l'utiliser |
|--------|---------|-------------|
| MAE | mean(\|actual - predicted\|) | Intuitive, dans les unités d'origine |
| MAPE | mean(\|actual - predicted\| / actual) | Besoin d'une erreur en pourcentage |
| MSE | mean((actual - predicted)^2) | Pénalise davantage les grandes erreurs |
| RMSE | sqrt(MSE) | Mêmes unités que la cible, pénalise les grandes erreurs |
| R^2 | 1 - SS_res/SS_tot | Fraction de la variance expliquée |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
```

**Piège** : la MAPE ne fonctionne plus lorsque les valeurs réelles sont proches de zéro (division par zéro). Le R^2 peut être négatif (modèle moins bon que la prédiction de la moyenne).

## Métriques de classification {#classification-metrics}

### Matrice de confusion {#confusion-matrix}

| | Prédit 0 | Prédit 1 |
|--|------------|------------|
| **Réel 0** | TN | FP |
| **Réel 1** | FN | TP |

```python
from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_true, y_pred)
print(classification_report(y_true, y_pred))
```

### Métriques clés {#key-metrics}

| Métrique | Formule | À optimiser lorsque |
|--------|---------|---------------|
| Precision | TP / (TP + FP) | Les FP sont coûteux (filtre anti-spam, accusation de fraude) |
| Recall | TP / (TP + FN) | Les FN sont coûteux (détection de maladie, détection de fraude) |
| F1 | 2*P*R / (P+R) | Équilibre entre precision et recall |
| Accuracy | (TP+TN) / total | **À éviter** avec des classes déséquilibrées |

### ROC AUC {#roc-auc}

Métrique indépendante du seuil. Évalue la qualité de classement des scores du modèle.

```python
from sklearn.metrics import roc_auc_score, roc_curve

auc = roc_auc_score(y_true, scores)  # scores, not predictions!
fpr, tpr, thresholds = roc_curve(y_true, scores)

import matplotlib.pyplot as plt
plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.plot([0,1], [0,1], 'k--')  # random baseline
plt.xlabel('FPR'); plt.ylabel('TPR')
plt.legend()
```

**Interprétation** : probabilité qu'un positif tiré au hasard ait un score supérieur à celui d'un négatif tiré au hasard. 0,5 = aléatoire, 1,0 = parfait.

### Courbe precision-recall {#precision-recall-curve}

Plus adaptée que la ROC pour des données très déséquilibrées :

```python
from sklearn.metrics import precision_recall_curve, average_precision_score

prec, rec, thresholds = precision_recall_curve(y_true, scores)
ap = average_precision_score(y_true, scores)
```

### Choix du seuil {#threshold-selection}

Les modèles produisent des scores (probabilités). Pour les convertir en prédictions binaires, il faut choisir un seuil.

```python
# Business context determines threshold
threshold = 0.3  # lower = higher recall, lower precision
y_pred = (scores >= threshold).astype(int)
```

Seuil plus élevé = prédictions moins nombreuses mais plus confiantes (precision plus élevée, recall plus faible).

## Métriques de classement (ranking) {#ranking-metrics}

| Métrique | Description |
|--------|-------------|
| precision@k | Fraction d'éléments pertinents dans le top-k |
| mAP@k | Precision moyenne (mean average precision) sur l'ensemble des requêtes |
| nDCG@k | Pertinence pondérée par la position : DCG = sum((2^y_i - 1) / log(i+1)) |

## Validation croisée {#cross-validation}

Une découpe unique train/test dépend de la graine aléatoire. La validation K-fold fournit des estimations plus robustes.

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

# Simple K-fold
scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
print(f"Mean AUC: {scores.mean():.3f} +/- {scores.std():.3f}")

# Stratified (preserves class ratio) - use for classification
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='f1')

# Time series: use TimeSeriesSplit (no future leakage)
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
```

### Découpage train / validation / test {#train-validation-test-split}

```python
from sklearn.model_selection import train_test_split

# 60/20/20 split
train, test = train_test_split(df, test_size=0.2, random_state=42)
train, val = train_test_split(train, test_size=0.25, random_state=42)
# 0.25 of 0.8 = 0.2
```

- **Train** : entraînement du modèle
- **Validation** : réglage des hyperparamètres, sélection des variables
- **Test** : évaluation finale, UNE SEULE FOIS (ne jamais régler le modèle sur le test)

## Compromis biais-variance {#bias-variance-tradeoff}

- **Biais élevé** (sous-apprentissage) : modèle trop simple, ne capture pas les motifs. Erreurs en entraînement et en validation élevées
- **Variance élevée** (surapprentissage) : modèle trop complexe, mémorise le bruit. Erreur d'entraînement faible, erreur de validation élevée
- **Diagnostic** : un écart important entre les performances en entraînement et en validation = surapprentissage

**Solutions contre le surapprentissage** : régularisation, modèle plus simple, davantage de données, arrêt anticipé (early stopping), dropout, validation croisée.

## Pièges {#gotchas}

- **Piège de l'accuracy** : avec une répartition de classes 99/1, prédire uniquement des zéros donne 99 % d'accuracy
- **Fuite de données (data leakage)** : un prétraitement ajusté sur l'ensemble complet (y compris le test) gonfle les métriques
- **Contamination du jeu de test** : si vous réglez quoi que ce soit sur le jeu de test, il n'est plus non biaisé
- **Déséquilibre des classes** : utiliser F1, PR-AUC ou ROC AUC plutôt que l'accuracy
- **Choix de la métrique** : optimiser la métrique qui correspond à l'objectif métier, et non celle qui paraît la meilleure
- **Surapprentissage sur la validation** : un réglage intensif des hyperparamètres peut aussi sur-ajuster le jeu de validation

## Voir aussi {#see-also}
- [[gradient-boosting]] - modèles principaux à évaluer
- [[linear-models]] - baselines simples pour comparaison
- [[hypothesis-testing]] - tests statistiques des écarts entre modèles
- [[ds-workflow]] - évaluation dans le contexte global du projet
