---
title: "Modèles linéaires et descente de gradient"
category: models
tags: [data-science, ml, linear-regression, logistic-regression, gradient-descent]
level: 4
source_sha256: 26cd757b1a6efb638051b0ab37320f73c911073f7ab2348aea5b90ea460be097
translation: machine
translated_at: '2026-10-24'
---
# Modèles linéaires et descente de gradient {#linear-models-and-gradient-descent}

Les modèles linéaires sont la base du ML. Simples, interprétables et étonnamment efficaces comme baselines. Comprendre la descente de gradient est essentiel : c'est ainsi que la plupart des modèles de ML apprennent.

## Régression linéaire {#linear-regression}

Prédire une cible continue comme une somme pondérée des features : y = w0 + w1*x1 + w2*x2 + ... + wn*xn

**Forme matricielle** : y = Xw où X inclut une colonne de 1 pour l'ordonnée à l'origine.

**Solution fermée (OLS)** : w = (X^T X)^(-1) X^T y

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(model.coef_, model.intercept_)
```

### Avec statsmodels (pour l'inférence) {#with-statsmodels-for-inference}

```python
import statsmodels.api as sm
X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()
model.summary()  # coefficients, t-stats, p-values, R^2, confidence intervals
```

### Les cinq hypothèses de l'OLS {#five-ols-assumptions}
1. Relation linéaire entre les features et la cible
2. Erreurs distribuées normalement, de moyenne nulle
3. Homoscédasticité (variance des erreurs constante)
4. Erreurs indépendantes
5. Spécification correcte des features (pas de features manquantes ou redondantes)

## Régression logistique {#logistic-regression}

Classification binaire. Produit une probabilité via la sigmoïde : P(y=1|x) = 1 / (1 + exp(-w^T x))

**Perte** : entropie croisée binaire = -sum[y_i * log(p_i) + (1-y_i) * log(1-p_i)]

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]  # P(class=1)
```

**Gradient** : d(Perte)/dw = X^T(p - y) - élégant car la dérivée de la sigmoïde sigma'(z) = sigma(z)(1 - sigma(z)).

## Descente de gradient {#gradient-descent}

Optimisation itérative : w_new = w_old - lr * gradient(Perte, w)

### Variantes {#variants}

| Variante | Gradient calculé sur | Compromis |
|---------|---------------------|----------|
| GD par lots (batch) | Jeu de données complet | Stable mais lent |
| Descente de gradient stochastique (SGD) | Un seul échantillon | Rapide mais bruité |
| GD par mini-lots | Petit lot (32-256) | Le meilleur des deux |

### Taux d'apprentissage {#learning-rate}

- Trop élevé : diverge (la perte oscille ou augmente)
- Trop faible : converge très lentement
- Bien réglé : décroissance régulière de la perte

### Momentum {#momentum}

Accélère dans les vallées étroites : v_t = beta * v_(t-1) + gradient ; w -= lr * v_t

### Convergence {#convergence}

Pour les fonctions convexes (comme la perte de la régression linéaire) : la GD converge vers le minimum global.
Pour les fonctions non convexes (réseaux de neurones) : elle converge vers un minimum local, souvent suffisant en pratique.

## Régularisation {#regularization}

| Type | Pénalité | Classe sklearn |
|------|---------|---------------|
| L2 (Ridge) | alpha * sum(w_j^2) | `Ridge(alpha=1.0)` |
| L1 (Lasso) | alpha * sum(\|w_j\|) | `Lasso(alpha=0.1)` |
| Elastic Net | alpha * [ratio * L1 + (1-ratio) * L2] | `ElasticNet(alpha=0.1, l1_ratio=0.5)` |

- alpha = 0 : pas de régularisation
- alpha -> inf : tous les coefficients -> 0 (sous-apprentissage)
- Choisir alpha par validation croisée

## Perspective économétrie vs ML {#econometrics-vs-ml-perspective}

- **Économétrie** : interprétabilité, relations causales, significativité des coefficients (p-values)
- **ML** : précision de la prédiction, ne se soucie pas des coefficients individuels
- Les modèles linéaires servent les deux : interprétables ET baseline prédictive

## Patrons {#patterns}

### Régression polynomiale {#polynomial-regression}
```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('scaler', StandardScaler()),
    ('model', Ridge(alpha=1.0))
])
pipe.fit(X_train, y_train)
```

### Sélection de la régularisation {#regularization-selection}
```python
from sklearn.linear_model import RidgeCV, LassoCV
ridge = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0], cv=5)
ridge.fit(X_train, y_train)
print(f"Best alpha: {ridge.alpha_}")
```

## Pièges {#gotchas}
- La régression linéaire nécessite une mise à l'échelle des features pour la descente de gradient (la forme fermée n'en a pas besoin, mais sklearn utilise des méthodes itératives pour Lasso/Elastic Net)
- La multicolinéarité gonfle la variance des coefficients : utiliser Ridge ou supprimer les features corrélées
- La régression logistique est un classifieur **linéaire** : la frontière de décision est toujours un hyperplan
- Ne pas interpréter les coefficients du Lasso comme une « importance » quand les features sont corrélées : il en choisit une arbitrairement
- Le R^2 peut être négatif (modèle pire que la prédiction de la moyenne)

## Voir aussi {#see-also}
- [[feature-engineering]] - prétraitement critique pour les modèles linéaires
- [[model-evaluation]] - métriques pour la régression et la classification
- [[gradient-boosting]] - quand les modèles linéaires ne suffisent pas
- [[math-for-ml]] - fondements de calcul différentiel pour la descente de gradient
