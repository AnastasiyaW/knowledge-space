---
title: "Analyse de séries temporelles"
category: techniques
tags: [data-science, time-series, forecasting, arima, seasonality, varma, garch, prophet]
level: 3
source_sha256: 255decfbb7abc0eddeb82ad6786b5c79cb5d7d1b0e4b8a3482e263d3171eda38
translation: machine
translated_at: '2026-10-24'
---
# Analyse de séries temporelles {#time-series-analysis}

Données ordonnées dans le temps. Elles demandent un traitement particulier, car les observations ne sont PAS indépendantes : les motifs temporels (tendance, saisonnalité, autocorrélation) doivent être modélisés explicitement.

## Composantes d'une série temporelle {#components-of-time-series}

- **Tendance** : direction à long terme (hausse, baisse, stable)
- **Saisonnalité** : motifs qui se répètent à intervalles fixes (quotidien, hebdomadaire, annuel)
- **Cyclique** : motifs qui se répètent à intervalles non fixes (cycles économiques)
- **Résidu/Bruit** : variations aléatoires restant après élimination de la tendance et de la saisonnalité

## Stationnarité {#stationarity}

Une série temporelle est stationnaire si ses propriétés statistiques (moyenne, variance) ne changent pas dans le temps. La plupart des modèles exigent la stationnarité.

**Tests :**
- **Test ADF** (Augmented Dickey-Fuller) : p < 0,05 -> stationnaire
- Visuel : tracer la série et vérifier que la moyenne et la variance sont constantes

**Rendre une série stationnaire :**
- **Différenciation** : y_diff = y_t - y_(t-1). Élimine une tendance linéaire
- **Transformation logarithmique** : stabilise la variance
- **Différenciation saisonnière** : y_t - y_(t-période)

## Modèles classiques {#classical-models}

### AR (AutoRegressive) {#ar-autoregressive}
y_t = c + phi_1 * y_(t-1) + ... + phi_p * y_(t-p) + erreur

Prédiction à partir des valeurs passées. L'ordre p correspond au nombre de retards (lags).

### MA (Moyenne mobile) {#ma-moving-average}
y_t = c + theta_1 * e_(t-1) + ... + theta_q * e_(t-q) + erreur

Prédiction à partir des erreurs passées. L'ordre q correspond au nombre de retards d'erreur.

### ARMA / ARIMA {#arma-arima}
- **ARMA(p,q)** : AR et MA combinés (exige la stationnarité)
- **ARIMA(p,d,q)** : d = ordre de différenciation. Gère les données non stationnaires
- **SARIMA(p,d,q)(P,D,Q,s)** : ajoute une composante saisonnière de période s

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(y_train, order=(2, 1, 1))  # AR=2, diff=1, MA=1
results = model.fit()
forecast = results.forecast(steps=30)
```

### Lissage exponentiel {#exponential-smoothing}

Moyenne pondérée des observations passées, avec des poids décroissant exponentiellement.

**SES** (Simple Exponential Smoothing) : ni tendance, ni saisonnalité. Équivalent à la moyenne mobile pondérée exponentiellement (EWMA). Un seul paramètre de lissage, alpha, contrôle le taux de décroissance.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing

# Simple Exponential Smoothing
ses_model = SimpleExpSmoothing(y_train).fit(smoothing_level=0.2)
forecast_ses = ses_model.forecast(12)

# Holt-Winters (trend + seasonality)
model = ExponentialSmoothing(y_train, trend='add', seasonal='mul', seasonal_periods=12)
results = model.fit()
forecast = results.forecast(12)
```

**Variantes** : SES (niveau seul) -> Holt (+ tendance) -> Holt-Winters (+ saisonnalité). Utiliser `seasonal='add'` pour une amplitude saisonnière constante, `seasonal='mul'` lorsque l'amplitude croît avec le niveau.

### VAR / VARMA (multivarié) {#var-varma-multivariate}

Modèles autorégressifs vectoriels : plusieurs séries temporelles corrélées sont prédites conjointement. Chaque série dépend de ses propres retards ET des retards de toutes les autres séries.

- Les paramètres sont des **matrices** (D x D) au lieu de scalaires, où D = nombre de séries temporelles
- **VAR(p)** : purement autorégressif, le plus couramment utilisé (l'estimation de VARMA est numériquement instable)
- **VARMA(p,q)** : ARMA vectoriel, ajoute une composante de moyenne mobile
- Format des données : T lignes x D colonnes (T pas de temps, D séries)

```python
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.api import VAR

# VAR model (recommended - simpler, more stable)
var_model = VAR(train_df[['series_1', 'series_2']])
results = var_model.fit(maxlags=4)
forecast = results.forecast(train_df[['series_1', 'series_2']].values[-4:], steps=12)

# VARMAX (supports exogenous variables)
model = VARMAX(train_scaled, order=(2, 1))
results = model.fit(disp=False, maxiter=500)
forecast = results.forecast(steps=n_test)
```

**Remarques pratiques** : toujours mettre à l'échelle les séries multivariées avant l'ajustement (unités et ordres de grandeur différents). Les ACF/PACF par série servent de guide approximatif, mais les termes croisés comptent : une recherche par grille sur (p,q) est l'approche pratique. Les jeux de données économétriques (PIB, taux d'intérêt, écarts de taux) constituent le cas d'usage classique de VARMA.

### GARCH (modélisation de la volatilité) {#garch-volatility-modeling}

GARCH modélise une variance variant dans le temps (regroupement de la volatilité). Indispensable pour les séries financières dont la variance n'est pas constante.

- **ARCH(q)** : la variance dépend des carrés des erreurs passées
- **GARCH(p,q)** : la variance dépend des carrés des erreurs passées ET des variances passées
- Le GARCH(1,1) standard est le modèle de référence

```python
from arch import arch_model

# Scale returns first - GARCH needs values between 1 and 1000
m, s = train_returns.mean(), train_returns.std()
train_scaled = (train_returns - m) / s

# GARCH(1,1)
model = arch_model(train_scaled, vol='GARCH', p=1, q=1)
result = model.fit(update_freq=5)
print(result.summary())

# ARCH(1) - simpler, variance depends only on past errors
arch1 = arch_model(train_scaled, vol='ARCH', p=1)
arch1_result = arch1.fit()

# Forecast variance
forecasts = result.forecast(horizon=5)
variance_forecast = forecasts.variance[-1:]
```

**Piège** : la bibliothèque `arch` émet un avertissement lorsque l'échelle des données d'entrée est trop petite. Toujours standardiser au préalable (soustraire la moyenne, diviser par l'écart type). Le paramètre `vol='ARCH'` doit être explicitement défini, car la valeur par défaut est GARCH.

### Prophet (Facebook/Meta) {#prophet-facebookmeta}

Modèle de séries temporelles décomposable : tendance + saisonnalité + jours fériés + régresseurs. Conçu pour la prévision business, avec une prise en charge automatique des motifs courants.

```python
from prophet import Prophet

# Data must have columns: 'ds' (datetime) and 'y' (values)
df_prophet = df[['date', 'value']].rename(columns={'date': 'ds', 'value': 'y'})

# Basic model
m = Prophet()
m.fit(df_prophet)

# Create future dates and predict
future = m.make_future_dataframe(periods=365)  # daily
forecast = m.predict(future)

# Multiplicative seasonality (for series where amplitude grows with level)
m = Prophet(seasonality_mode='multiplicative')

# Monthly data - specify freq
future = m.make_future_dataframe(periods=12, freq='MS')

# Add country holidays
m = Prophet()
m.add_country_holidays(country_name='US')
m.fit(df_prophet)

# Add custom regressor (exogenous variable)
m = Prophet()
m.add_regressor('promo')
m.fit(df_train)
# future df must also contain 'promo' column
```

**Paramètres clés** : `growth='linear'|'logistic'`, `changepoint_prior_scale` (flexibilité des changements de tendance, 0,05 par défaut), `seasonality_prior_scale` (intensité de la saisonnalité), `n_changepoints` (25 par défaut).

**Comportement automatique** : désactive la saisonnalité journalière pour les données quotidiennes, désactive les saisonnalités journalière et hebdomadaire pour les données mensuelles. Prophet affiche des messages signalant les composantes désactivées pendant l'ajustement.

### Marche aléatoire (Random Walk) {#random-walk}

Une marche aléatoire s'écrit : x_t = x_(t-1) + bruit. Chaque valeur = valeur précédente + pas aléatoire. Cas particulier d'ARIMA(0,1,0).

**Hypothèse de marche aléatoire** : les cours boursiers suivent une marche aléatoire, ce qui les rend fondamentalement imprévisibles. Conséquences :
- La meilleure prévision pour le cours de demain est le cours d'aujourd'hui
- Ce sont les **rendements** (différences de cours) qui sont imprévisibles, et non les cours eux-mêmes
- Utiliser les **rendements** (ou rendements logarithmiques) comme variables explicatives pour le ML, et non les cours bruts

**Problème d'extrapolation** : la plupart des modèles de ML (SVM, forêts aléatoires, réseaux de neurones) ne peuvent pas extrapoler au-delà de l'étendue des données d'entraînement. Si les cours d'entraînement se situent entre 100 et 200, le modèle ne peut pas prédire 250. C'est pourquoi les rendements (stationnaires, à étendue bornée) fonctionnent mieux que les cours bruts en ML.

### Auto ARIMA {#auto-arima}

Sélection automatique de l'ordre par recherche sur grille des combinaisons (p,d,q). Elle supprime l'interprétation manuelle des ACF/PACF en testant des modèles candidats et en retenant le meilleur selon l'AIC/BIC.

```python
from pmdarima import auto_arima

# Basic usage
model = auto_arima(y_train, seasonal=True, m=12,
                   stepwise=True, suppress_warnings=True,
                   trace=True)  # trace=True shows all models tested
print(model.summary())
forecast = model.predict(n_periods=12)
```

**Astuce de la transformation logarithmique** : si la série a une variance croissante (l'amplitude croît avec le niveau), appliquer une transformation logarithmique avant l'ajustement. Cela améliore souvent la précision avec le même ordre ARIMA :

```python
import numpy as np

df['log_values'] = np.log(df['values'])
model_log = auto_arima(df['log_values'][:train_end],
                       seasonal=True, m=12, trace=True,
                       suppress_warnings=True)
forecast_log = model_log.predict(n_periods=n_test)
forecast_original = np.exp(forecast_log)  # reverse the transform
```

**Arguments clés** :

- `trace=True` : affiche tous les modèles candidats et leurs scores AIC, utile pour comprendre la recherche
- `suppress_warnings=True` : supprime les avertissements de convergence émis par les candidats peu performants
- `m` : période saisonnière (12 pour les données mensuelles, 7 pour les données quotidiennes avec motif hebdomadaire, 52 pour les données hebdomadaires avec motif annuel)
- `stepwise=True` : recherche heuristique plus rapide (par défaut). Mettre `False` pour une recherche exhaustive sur grille (plus lente, parfois meilleure)
- `seasonal=True/False` : inclure ou non la composante ARIMA saisonnière (P,D,Q)

**pmdarima doit être installé séparément** : il n'est inclus ni dans les distributions Python standard, ni dans la plupart des environnements de notebooks cloud. L'installer avec `pip install pmdarima`.

## Ingénierie des variables pour les séries temporelles {#feature-engineering-for-time-series}

Pour les approches de ML (à base d'arbres, réseaux de neurones) :

```python
# Lag features
for lag in [1, 7, 14, 30]:
    df[f'lag_{lag}'] = df['value'].shift(lag)

# Rolling statistics
df['rolling_mean_7'] = df['value'].rolling(7).mean()
df['rolling_std_7'] = df['value'].rolling(7).std()

# Calendar features
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
```

## Validation pour les séries temporelles {#validation-for-time-series}

**Ne jamais utiliser une découpe aléatoire train/test** : l'ordre temporel compte. Utiliser une découpe temporelle.

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    # train on past, test on future
    X_train, X_test = X[train_idx], X[test_idx]
```

### Validation walk-forward {#walk-forward-validation}

La validation de séries temporelles la plus rigoureuse. Entraîner sur une fenêtre croissante, prévoir les h pas suivants, avancer la fenêtre, et recommencer. Cela simule un déploiement réel où le modèle est réentraîné périodiquement.

```python
from itertools import product

h = 12           # forecast horizon
n_steps = 10     # number of walk-forward steps

results = []
for i in range(n_steps):
    train_end = len(series) - h - n_steps + i + 1
    train = series[:train_end]
    test = series[train_end:train_end + h]

    model = ExponentialSmoothing(train, trend='add',
                                seasonal='mul', seasonal_periods=12,
                                use_boxcox=True).fit()
    pred = model.forecast(h)
    error = np.mean(np.abs(test - pred))
    results.append(error)

avg_mae = np.mean(results)
```

La combiner avec une recherche sur grille des paramètres du modèle (type de tendance, type de saisonnalité, Box-Cox) à l'aide de `itertools.product` pour trouver la meilleure configuration sur l'ensemble des fenêtres walk-forward.

**Piège** : le paramètre `use_boxcox` de statsmodels accepte `True`, `False` ou un flottant (valeur de lambda). La chaîne `'log'` apparaît dans certaines documentations mais provoque une erreur : utiliser `0` à la place (lambda=0 correspond à la transformation logarithmique).

## Pièges à éviter {#gotchas}
- Découpe aléatoire train/test = fuite de données (informations futures présentes dans l'entraînement)
- La stationnarité est requise pour ARIMA : toujours la tester en premier
- La période saisonnière doit être connue (connaissance métier ou graphique ACF)
- L'incertitude de prévision croît avec l'horizon : toujours fournir des intervalles de confiance
- Pour les très longues séries, les LSTM et les transformers peuvent surpasser ARIMA, mais nécessitent beaucoup plus de données
- **L'ajustement de VARMA est lent et instable** : pour la plupart des cas multivariés, utiliser VAR (sans partie MA) ou passer directement à des approches ML/DL
- **GARCH exige des entrées mises à l'échelle** : valeurs entre 1 et 1000, toujours standardiser au préalable
- **Prophet désactive automatiquement les saisonnalités de fréquence inférieure** : les données mensuelles ne peuvent pas capturer les motifs journaliers ou hebdomadaires, c'est attendu
- **Validation économétrie vs ML** : l'économétrie traditionnelle omet souvent les découpes train/test et prévoit au-delà des données disponibles. Toujours utiliser une évaluation hors échantillon rigoureuse
- **Prophet sur les cours boursiers** est une erreur courante : Prophet est conçu pour les indicateurs métier à forte saisonnalité (ventes, trafic), et non pour les instruments financiers qui suivent des marches aléatoires. Les cours boursiers n'ont pas les motifs saisonniers stables sur lesquels Prophet s'appuie, ce qui conduit à des prévisions très inexactes
- **Auto ARIMA sur les actions** donne de même de mauvais résultats. L'hypothèse de marche aléatoire implique que la meilleure prévision est « cours de demain = cours d'aujourd'hui » : tout modèle qui bat systématiquement cette référence sur des données hors échantillon doit être examiné de près pour détecter une fuite de données
- **ACF/PACF pour les séries multivariées** : les ACF/PACF par série ignorent les corrélations croisées ; à utiliser comme guide approximatif uniquement, puis faire une recherche sur grille de (p,q)
- **`use_boxcox='log'` de statsmodels ne fonctionne pas** : utiliser `0` (lambda=0 = transformation logarithmique) à la place

## Voir aussi {#see-also}
- [[rnn-sequences]] - apprentissage profond pour les séquences
- [[cnn-computer-vision]] - CNN appliqués à la classification de séries temporelles
- [[hypothesis-testing]] - test de la significativité d'une tendance
- [[pandas-eda]] - manipulation de séries temporelles avec pandas
- [[feature-engineering]] - création de variables temporelles
- [[model-evaluation]] - détails sur la validation walk-forward
- [[neural-networks]] - réseaux de neurones artificiels pour la prévision de séries temporelles
