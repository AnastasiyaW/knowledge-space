---
title: "Statistiques descriptives"
category: concepts
tags: [data-science, statistics, eda, fundamentals]
level: 3
source_sha256: c599a5c2ccb7f7478ce8b8464bb53c59aba3f7f45f3c0d9514131b6a8d023afd
translation: machine
translated_at: '2026-10-24'
---
# Statistiques descriptives {#descriptive-statistics}

Résumés quantitatifs des distributions de données. Le socle de l'EDA : toujours les calculer avant la modélisation. Comprendre la tendance centrale, la dispersion et la forme permet de savoir quels modèles et quelles étapes de prétraitement sont appropriés.

## Mesures de tendance centrale {#measures-of-central-tendency}

- **Moyenne** : somme / effectif. Sensible aux valeurs aberrantes. `df['col'].mean()`
- **Médiane** : valeur centrale une fois les données triées. Robuste aux valeurs aberrantes. `df['col'].median()`
- **Mode** : valeur la plus fréquente. Peut être multimodal. `df['col'].mode()`

**La comparaison moyenne/médiane révèle l'asymétrie :**
- Moyenne > médiane : asymétrie à droite (quelques valeurs élevées tirent la moyenne vers le haut), p. ex. distributions de revenus
- Moyenne < médiane : asymétrie à gauche (quelques valeurs faibles tirent la moyenne vers le bas), p. ex. notes d'examen
- Moyenne ≈ médiane : distribution à peu près symétrique

## Mesures de dispersion {#measures-of-spread}

```python
import numpy as np
from scipy import stats

salary_range = df['income'].max() - df['income'].min()  # range
salary_var = df['income'].var()                          # variance
salary_std = df['income'].std()                          # standard deviation
iqr = df['income'].quantile(0.75) - df['income'].quantile(0.25)  # IQR
```

- **Étendue** : max - min. Simple, mais extrêmement sensible aux valeurs aberrantes
- **Variance** : écart quadratique moyen à la moyenne. Unité au carré
- **Écart-type** : racine carrée de la variance. Même unité que les données, plus facile à interpréter
- **IQR** (intervalle interquartile) : Q3 - Q1. Mesure de dispersion robuste, utilisée pour la détection des valeurs aberrantes

## Mesures de forme {#measures-of-shape}

**Asymétrie (skewness)** - asymétrie de la distribution :
```python
skewness = stats.skew(df['income'])
# > 0: right-skewed (long right tail)
# < 0: left-skewed (long left tail)
# ~ 0: symmetric
```

**Aplatissement (kurtosis)** - épaisseur des queues de distribution par rapport à la loi normale :
```python
kurtosis = stats.kurtosis(df['income'])
# > 0 (leptokurtic): heavy tails, sharp peak - more extreme values
# < 0 (platykurtic): light tails, flat peak
# ~ 0 (mesokurtic): similar to normal
```

**Pourquoi la forme compte** : elle guide le prétraitement (transformation logarithmique pour les variables asymétriques), la détection des valeurs aberrantes (leptokurtique = plus de valeurs extrêmes) et le choix du modèle (les modèles linéaires supposent des résidus approximativement normaux).

## Mesures de position {#measures-of-position}

```python
# Percentiles
p25, p50, p75 = np.percentile(df['income'], [25, 50, 75])

# Quartiles via describe()
df['income'].describe()
# count, mean, std, min, 25%, 50%, 75%, max
```

## Scores z {#z-scores}

Z = (X - mu) / sigma. Nombre d'écarts-types par rapport à la moyenne.

```python
z_scores = stats.zscore(df['income'])
# |z| > 2: unusual (5% of normal data)
# |z| > 3: extreme outlier (0.3% of normal data)
```

**Règle 68-95-99,7** (règle empirique pour les lois normales) :
- ~68 % des données se situent à moins de 1 écart-type de la moyenne
- ~95 % à moins de 2 écarts-types
- ~99,7 % à moins de 3 écarts-types

## Corrélation {#correlation}

Mesure l'intensité et le sens de la relation entre deux variables. Intervalle : [-1, +1].

```python
# Pearson - linear relationships, assumes normality
pearson_r = df['income'].corr(df['experience'])

# Full correlation matrix
corr_matrix = df.corr()

# Spearman - monotonic (not just linear), rank-based, no normality assumption
spearman_r = df['income'].corr(df['experience'], method='spearman')

# Kendall - concordant/discordant pairs, robust to outliers, good for small samples
kendall_tau = df['income'].corr(df['experience'], method='kendall')
```

| Méthode | Mesure | Hypothèses | Quand l'utiliser |
|--------|----------|-------------|----------|
| Pearson | Relation linéaire | Normalité, homoscédasticité | Deux variables continues, à peu près normales |
| Spearman | Relation monotone | Aucune (basée sur les rangs) | Données ordinales, relation monotone non linéaire |
| Kendall | Concordance | Aucune (basée sur les rangs) | Petits échantillons, données ordinales |

**La corrélation n'implique pas la causalité.** Les ventes de glaces sont corrélées aux taux de noyade (facteur de confusion : la chaleur).

## Échantillon vs population {#sample-vs-population}

- **Population** (mu, sigma) : ensemble complet étudié. Rarement observable dans sa totalité
- **Échantillon** (x_bar, s) : sous-ensemble utilisé pour estimer les paramètres de la population
- Plus l'échantillon est grand, plus ses statistiques se rapprochent des paramètres de la population

## Pièges courants {#gotchas}
- Utiliser la moyenne sur des données fortement asymétriques sans indiquer la médiane
- Une corrélation de Pearson égale à 0 ne signifie PAS l'absence de relation (celle-ci peut être non linéaire)
- L'étendue est presque inutile pour comparer des distributions (dominée par quelques valeurs aberrantes)
- `df.describe()` n'affiche par défaut que les colonnes numériques : utiliser `include='all'` ou `include='object'`

## Voir aussi {#see-also}
- [[probability-distributions]] - distributions théoriques sous-jacentes aux données
- [[pandas-eda]] - calcul de ces statistiques avec pandas
- [[data-visualization]] - visualisation des distributions
- [[hypothesis-testing]] - test de la significativité des différences observées
