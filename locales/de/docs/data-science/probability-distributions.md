---
title: "Wahrscheinlichkeit und Verteilungen"
category: concepts
tags: [data-science, statistics, probability, distributions]
level: 3
source_sha256: 4403ad9a90aabc288cb47bda59120d51dab193fd7789e3a5f9c2dff1096bfb74
translation: machine
translated_at: '2026-10-24'
---
# Wahrscheinlichkeit und Verteilungen {#probability-and-distributions}

Grundlagen der Wahrscheinlichkeitstheorie und gängige Verteilungen, die in Data Science und ML durchgängig verwendet werden. Das Verständnis von Verteilungen ist unerlässlich für die Auswahl geeigneter statistischer Tests, den Aufbau generativer Modelle und die Interpretation von Ergebnissen.

## Grundlagen der Wahrscheinlichkeit {#probability-fundamentals}

**Wahrscheinlichkeit** P(A) = Maß dafür, wie wahrscheinlich das Ereignis A ist. Wertebereich: [0, 1].

**Klassische Definition**: P(A) = günstige Ergebnisse / Anzahl aller gleich wahrscheinlichen Ergebnisse.
**Frequentistische Definition**: P(A) = lim(N->inf) count(A) / N.

### Zentrale Regeln {#key-rules}

| Regel | Formel |
|------|---------|
| Komplement | P(nicht A) = 1 - P(A) |
| Addition | P(A oder B) = P(A) + P(B) - P(A und B) |
| Disjunkte Ereignisse | P(A oder B) = P(A) + P(B) |
| Unabhängigkeit | P(A und B) = P(A) * P(B) |
| Bedingt | P(A\|B) = P(A und B) / P(B) |

**Muster „Mindestens eins“**: P(mindestens eins) = 1 - P(keins). Deutlich einfacher als die direkte Berechnung.

### Satz von Bayes {#bayes-theorem}

P(A|B) = P(B|A) * P(A) / P(B)

- P(A|B): Posterior (das, was wir suchen)
- P(B|A): Likelihood
- P(A): Prior
- P(B): Evidenz (Randwahrscheinlichkeit)

**Fallstrick**: P(A|B) != P(B|A). P(Krankheit|positiver Test) ist NICHT P(positiver Test|Krankheit).

### Totale Wahrscheinlichkeit {#total-probability}

P(A) = sum_i P(A|B_i) * P(B_i), wobei {B_i} eine Zerlegung des Ergebnisraums bildet.

## Zufallsvariablen {#random-variables}

**Diskret**: abzählbare Werte (Würfelwurf, Anzahl der Kunden). Beschrieben durch die PMF.
**Stetig**: beliebige Werte innerhalb eines Bereichs (Körpergröße, Temperatur). Beschrieben durch die PDF.

- **Erwartungswert**: E(X) = sum(x_i * P(x_i)) oder integral(x * f(x) dx)
- **Varianz**: Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2

## Gängige diskrete Verteilungen {#common-discrete-distributions}

### Bernoulli {#bernoulli}
Einzelner Versuch mit Erfolgswahrscheinlichkeit p.
- E(X) = p, Var(X) = p(1-p)

### Binomialverteilung {#binomial}
k Erfolge in n unabhängigen Bernoulli-Versuchen.
- P(k) = C(n,k) * p^k * (1-p)^(n-k)
- E(X) = np, Var(X) = np(1-p)

### Poisson-Verteilung {#poisson}
Anzahl der Ereignisse in einem festen Intervall mit der Rate lambda.
- P(k) = (lambda^k / k!) * e^(-lambda)
- E(X) = Var(X) = lambda
- Verwendung für: seltene Ereignisse, Zähldaten (Anrufe pro Stunde, Unfälle pro Monat)

## Gängige stetige Verteilungen {#common-continuous-distributions}

### Normalverteilung (Gauß) {#normal-gaussian}
Glockenförmig, symmetrisch. Definiert durch mu (Mittelwert) und sigma (Standardabweichung).
```python
from scipy import stats
norm = stats.norm(loc=0, scale=1)
norm.pdf(0)      # density at 0
norm.cdf(1.96)   # P(X <= 1.96) ~ 0.975
norm.ppf(0.95)   # 95th percentile ~ 1.645
```

**Zentraler Grenzwertsatz**: Summe bzw. Mittelwert vieler unabhängiger Zufallsvariablen nähert sich unabhängig von deren einzelnen Verteilungen einer Normalverteilung an. Deshalb ist die Normalverteilung so verbreitet.

### Exponentialverteilung {#exponential}
Zeit zwischen unabhängigen Ereignissen mit konstanter Rate.
- Gedächtnislos: P(X > s + t | X > s) = P(X > t)
- E(X) = 1/lambda, Var(X) = 1/lambda^2

### Gleichverteilung {#uniform}
Alle Ergebnisse im Intervall [a, b] sind gleich wahrscheinlich.
- E(X) = (a+b)/2, Var(X) = (b-a)^2/12

## Kombinatorik {#combinatorics}

- **Permutationen** (Reihenfolge zählt): P(n,k) = n! / (n-k)!
- **Kombinationen** (Reihenfolge zählt nicht): C(n,k) = n! / (k!(n-k)!)
- **Mit Wiederholung**: Permutationen = n^k, Kombinationen = C(n+k-1, k)
- **Binomischer Lehrsatz**: (a+b)^n = sum C(n,k) * a^(n-k) * b^k

## Zentrale Sätze {#key-theorems}

- **Gesetz der großen Zahlen**: Der Stichprobenmittelwert konvergiert für n -> inf gegen den Populationsmittelwert
- **Zentraler Grenzwertsatz**: Der standardisierte Stichprobenmittelwert strebt für n -> inf gegen N(0,1)
- **Tschebyscheff-Ungleichung**: P(|X - mu| >= k*sigma) <= 1/k^2 (für beliebige Verteilungen)

## Verteilungen simulieren {#simulating-distributions}

```python
import numpy as np

# Inverse CDF method: if U ~ Uniform(0,1), then F^{-1}(U) has CDF F
# Exponential: X = -ln(U) / lambda
u = np.random.uniform(size=10000)
x_exp = -np.log(u) / 2.0  # Exp(lambda=2)

# Box-Muller for normal:
u1, u2 = np.random.uniform(size=10000), np.random.uniform(size=10000)
z = np.sqrt(-2*np.log(u1)) * np.cos(2*np.pi*u2)  # N(0,1)

# Direct numpy:
np.random.normal(0, 1, 10000)     # normal
np.random.poisson(5, 10000)       # poisson
np.random.binomial(10, 0.3, 10000) # binomial
```

## Fallstricke {#gotchas}
- Die Poisson-Verteilung ist NICHT einfach „Binomialverteilung mit großem n und kleinem p“ – Poisson setzt eine konstante Rate voraus, die Binomialverteilung feste Versuchszahlen
- Die Normalverteilung ist **nicht** universell – viele reale Verteilungen sind stark schief (Einkommen, Dateigrößen)
- Der ZGWS setzt endliche Varianz voraus – er gilt nicht für schwerschwänzige Verteilungen (Cauchy)
- Die Exponentialverteilung ist die **einzige** stetige gedächtnislose Verteilung

## Siehe auch {#see-also}
- [[descriptive-statistics]] - empirische Zusammenfassungen von Daten
- [[hypothesis-testing]] - Verteilungen für statistische Inferenz nutzen
- [[bayesian-methods]] - Satz von Bayes im ML-Kontext
- [[math-for-ml]] - Grundlagen der Wahrscheinlichkeitstheorie
