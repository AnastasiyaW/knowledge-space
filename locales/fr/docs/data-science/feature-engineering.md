---
title: "Feature engineering et prétraitement"
category: techniques
tags: [data-science, feature-engineering, preprocessing, sklearn]
level: 3
source_sha256: 0b9264a73f73fed21cef65b6d9d301b06ef27131778f93b5175ef0581918c5e4
translation: machine
translated_at: '2026-10-24'
---
# Feature Engineering et prétraitement {#feature-engineering-and-preprocessing}

L'art de transformer les données brutes en features exploitables efficacement par les modèles de ML. Souvent l'étape la plus déterminante d'un projet de data science : de bonnes features valent mieux que des modèles complexes.

## Mise à l'échelle des features {#feature-scaling}

Les modèles linéaires et les réseaux de neurones sont sensibles à l'échelle des features. Ce n'est PAS le cas des modèles à base d'arbres (CatBoost, Random Forest).

### StandardScaler (score Z) {#standardscaler-z-score}

Transforme les données vers moyenne=0, écart-type=1 : z = (x - moyenne) / écart-type

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # fit on train ONLY
X_test_scaled = scaler.transform(X_test)         # transform with train stats
```

### MinMaxScaler {#minmaxscaler}

Ramène les valeurs dans [0, 1] : x_scaled = (x - x_min) / (x_max - x_min)

```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)
```

**Règle critique** : ajuster le scaler (fit) uniquement sur les données d'entraînement, puis transformer à la fois l'entraînement et le test. Ajuster sur le test = fuite de données (data leakage).

## Encodage des variables catégorielles {#categorical-encoding}

### One-Hot Encoding {#one-hot-encoding}
N catégories -> N colonnes binaires. À utiliser pour les catégories nominales (non ordonnées).
```python
pd.get_dummies(df['col'], drop_first=True)  # drop_first avoids multicollinearity

from sklearn.preprocessing import OneHotEncoder
ohe = OneHotEncoder(drop='first', sparse_output=False)
```

### Label Encoding {#label-encoding}
Associe chaque catégorie à un entier. À réserver aux données ordinales (ayant un ordre naturel).
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['encoded'] = le.fit_transform(df['col'])
```

### Target Encoding {#target-encoding}
Remplace la catégorie par la moyenne de la cible pour cette catégorie. CatBoost le fait en interne, avec régularisation. Risque élevé de fuite de données sans encodage basé sur une validation croisée (CV) correctement conçue.

## Imputation des valeurs manquantes {#missing-value-imputation}

```python
from sklearn.impute import SimpleImputer

# Numerical: median is robust to outliers
imputer = SimpleImputer(strategy='median')
X_imputed = imputer.fit_transform(X)

# Categorical: most frequent or constant
imputer_cat = SimpleImputer(strategy='most_frequent')
```

**Astuce** : créer un indicateur binaire `is_missing` avant l'imputation, car l'absence de valeur peut elle-même être informative.

## Sélection de features {#feature-selection}

### Méthodes de filtrage (indépendantes du modèle) {#filter-methods-model-independent}
```python
from sklearn.feature_selection import VarianceThreshold, mutual_info_classif

# Remove near-constant features
sel = VarianceThreshold(threshold=0.01)
X_filtered = sel.fit_transform(X)

# Mutual information (captures non-linear relationships)
mi_scores = mutual_info_classif(X, y)
```

### Méthodes wrapper (dépendantes du modèle) {#wrapper-methods-model-dependent}
```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

selector = RFE(LogisticRegression(), n_features_to_select=10)
X_selected = selector.fit_transform(X, y)
```

### Méthodes embarquées (intégrées au modèle) {#embedded-methods-built-into-model}
- **L1/Lasso** : ramène à exactement zéro les poids peu importants
- **Importance basée sur les arbres** : `model.feature_importances_` de Random Forest, CatBoost

## Régularisation {#regularization}

Prévient le surapprentissage en pénalisant les coefficients de grande valeur.

| Type | Pénalité | Effet | Quand l'utiliser |
|------|----------|-------|------------------|
| L2 (Ridge) | sum(beta_j^2) | Réduit tous les coefficients, sans jamais les annuler | Multicolinéarité |
| L1 (Lasso) | sum(\|beta_j\|) | Ramène certains coefficients à exactement 0 | Sélection de features |
| Elastic Net | L1 + L2 | Combinaison des deux | Groupes de features corrélées |

**Pourquoi L1 produit des zéros** : la boule L1 a des pointes situées sur les axes, si bien que l'optimum se trouve souvent sur une pointe. La boule L2 est lisse : le point de tangence ne se situe presque jamais sur un axe.

```python
from sklearn.linear_model import Ridge, Lasso, ElasticNet
ridge = Ridge(alpha=1.0)    # alpha = regularization strength
lasso = Lasso(alpha=0.1)
elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)
```

## Pipelines sklearn {#sklearn-pipelines}

Enchaîne le prétraitement et le modèle. Prévient la fuite de données.

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_cols),
    ('cat', OneHotEncoder(drop='first'), categorical_cols)
])

pipe = Pipeline([
    ('preprocess', preprocessor),
    ('model', LogisticRegression())
])
pipe.fit(X_train, y_train)
predictions = pipe.predict(X_test)
```

## Techniques de feature engineering {#feature-engineering-techniques}

- **Basées sur le domaine** : exploiter la connaissance métier (lat/lon -> distance, date -> jour_de_semaine)
- **Features d'interaction** : x1 * x2 capture les effets conjoints
- **Features polynomiales** : x^2, x^3 pour les relations non linéaires
- **Features d'agrégation** : statistiques de groupe (moyenne, count, écart-type) sur des entités liées
- **Temporelles** : jour_de_semaine, mois, heure, is_weekend, jours_depuis_événement
- **Textuelles** : nombre de mots, features TF-IDF, n-grammes

```python
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, interaction_only=False)
X_poly = poly.fit_transform(X)
```

## Détection de corrélations non linéaires {#non-linear-correlation-detection}

```python
# phik - detects non-linear AND works with categoricals
import phik
corr_matrix = df.phik_matrix()
df.phik_matrix()['target'].sort_values(ascending=False)
```

Toujours vérifier les résultats de phik avec des tableaux croisés dynamiques. Phik indique OÙ regarder, les tableaux croisés confirment.

## Pièges courants {#gotchas}
- **Fuite de données** via le prétraitement : ajuster le scaler/encodeur sur les données de test, ou calculer le target encoding sans validation croisée
- **Explosion du one-hot** : 1000 catégories = 1000 features. Préférer le target encoding ou les embeddings
- **Label encoding sur des données nominales** : crée une fausse relation d'ordre (le modèle considère que la catégorie 3 > catégorie 1)
- **Features polynomiales** : degré 3 avec 100 features = des millions de features. Utiliser `interaction_only=True` ou sélectionner manuellement
- **L'importance des features issue d'un seul arbre est peu fiable** : utiliser l'importance par permutation ou une moyenne sur un ensemble de modèles

## Voir aussi {#see-also}
- [[pandas-eda]] - exploration des données avant le feature engineering
- [[linear-models]] - modèles les plus affectés par le feature engineering
- [[gradient-boosting]] - modèles gérant nativement les features
- [[model-evaluation]] - évaluation de l'impact des features sur les performances
