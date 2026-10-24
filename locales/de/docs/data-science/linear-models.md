---
title: "Lineare Modelle und Gradientenabstieg"
category: models
tags: [data-science, ml, linear-regression, logistic-regression, gradient-descent]
level: 4
source_sha256: 26cd757b1a6efb638051b0ab37320f73c911073f7ab2348aea5b90ea460be097
translation: machine
translated_at: '2026-10-24'
---
# Lineare Modelle und Gradientenabstieg {#linear-models-and-gradient-descent}

Lineare Modelle sind das Fundament des maschinellen Lernens. Sie sind einfach, interpretierbar und überraschend effektiv als Baselines. Das Verständnis von Gradientenabstieg ist essenziell – so lernen die meisten ML-Modelle.

## Lineare Regression {#linear-regression}

Vorhersage eines kontinuierlichen Zielwerts als gewichtete Summe der Merkmale: y = w0 + w1*x1 + w2*x2 + ... + wn*xn

**Matrixform**: y = Xw, wobei X eine Spalte mit Einsen für den Intercept enthält.

**Geschlossene Lösung (OLS)**: w = (X^T X)^(-1) X^T y

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(model.coef_, model.intercept_)
```

### Mit statsmodels (für Inferenz) {#with-statsmodels-for-inference}

```python
import statsmodels.api as sm
X_const = sm.add_constant(X)
model = sm.OLS(y, X_const).fit()
model.summary()  # coefficients, t-stats, p-values, R^2, confidence intervals
```

### Fünf OLS-Annahmen {#five-ols-assumptions}
1. Lineare Beziehung zwischen Merkmalen und Zielwert
2. Normalverteilte Fehler mit Erwartungswert null
3. Homoskedastizität (konstante Fehlervarianz)
4. Unabhängige Fehler
5. Korrekte Merkmalsspezifikation (keine fehlenden/redundanten Merkmale)

## Logistische Regression {#logistic-regression}

Binäre Klassifikation. Gibt eine Wahrscheinlichkeit über die Sigmoidfunktion aus: P(y=1|x) = 1 / (1 + exp(-w^T x))

**Verlust**: Binary Cross-Entropy = -sum[y_i * log(p_i) + (1-y_i) * log(1-p_i)]

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]  # P(class=1)
```

**Gradient**: d(Loss)/dw = X^T(p - y) – elegant, da die Ableitung der Sigmoidfunktion sigma'(z) = sigma(z)(1 - sigma(z)) ist.

## Gradientenabstieg {#gradient-descent}

Iterative Optimierung: w_neu = w_alt - lr * Gradient(Loss, w)

### Varianten {#variants}

| Variante | Gradient berechnet auf | Abwägung |
|---------|---------------------|----------|
| Batch GD | Gesamtem Datensatz | Stabil, aber langsam |
| Stochastic GD (SGD) | Einzelnem Sample | Schnell, aber verrauscht |
| Mini-Batch GD | Kleinem Batch (32–256) | Das Beste aus beiden |

### Lernrate {#learning-rate}

- Zu hoch: divergiert (Verlust oszilliert oder steigt)
- Zu niedrig: konvergiert sehr langsam
- Passend: stetige Abnahme des Verlusts

### Momentum {#momentum}

Beschleunigt in engen Tälern: v_t = beta * v_(t-1) + gradient; w -= lr * v_t

### Konvergenz {#convergence}

Für konvexe Funktionen (wie der Verlust der linearen Regression) konvergiert GD gegen das globale Minimum.
Für nicht-konvexe Funktionen (neuronale Netze) konvergiert er gegen ein lokales Minimum – in der Praxis oft ausreichend.

## Regularisierung {#regularization}

| Typ | Strafterm | sklearn-Klasse |
|------|---------|---------------|
| L2 (Ridge) | alpha * sum(w_j^2) | `Ridge(alpha=1.0)` |
| L1 (Lasso) | alpha * sum(\|w_j\|) | `Lasso(alpha=0.1)` |
| Elastic Net | alpha * [ratio * L1 + (1-ratio) * L2] | `ElasticNet(alpha=0.1, l1_ratio=0.5)` |

- alpha = 0: keine Regularisierung
- alpha -> inf: alle Koeffizienten -> 0 (Underfitting)
- alpha per Kreuzvalidierung wählen

## Ökonometrie vs. ML-Perspektive {#econometrics-vs-ml-perspective}

- **Ökonometrie**: Interpretierbarkeit, kausale Zusammenhänge, Signifikanz der Koeffizienten (p-Werte)
- **ML**: Vorhersagegenauigkeit, interessiert sich nicht für einzelne Koeffizienten
- Lineare Modelle dienen beiden: interpretierbar UND als prädiktive Baseline

## Muster {#patterns}

### Polynomiale Regression {#polynomial-regression}
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

### Auswahl der Regularisierung {#regularization-selection}
```python
from sklearn.linear_model import RidgeCV, LassoCV
ridge = RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0], cv=5)
ridge.fit(X_train, y_train)
print(f"Best alpha: {ridge.alpha_}")
```

## Stolpersteine {#gotchas}
- Lineare Regression benötigt für Gradientenabstieg eine Merkmalsskalierung (die geschlossene Lösung nicht, aber sklearn verwendet für Lasso/Elastic Net iterative Verfahren)
- Multikollinearität vergrößert die Varianz der Koeffizienten – Ridge verwenden oder korrelierte Merkmale entfernen
- Logistische Regression ist ein **lineares** Klassifikationsmodell – die Entscheidungsgrenze ist immer eine Hyperebene
- Lasso-Koeffizienten nicht als „Wichtigkeit“ interpretieren, wenn Merkmale korreliert sind – es wählt willkürlich eines aus
- R^2 kann negativ sein (Modell schlechter als die Vorhersage des Mittelwerts)

## Siehe auch {#see-also}
- [[feature-engineering]] – Vorverarbeitung ist für lineare Modelle entscheidend
- [[model-evaluation]] – Metriken für Regression und Klassifikation
- [[gradient-boosting]] – wenn lineare Modelle nicht ausreichen
- [[math-for-ml]] – Analysis-Grundlagen für Gradientenabstieg
