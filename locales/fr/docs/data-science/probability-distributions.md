---
title: "Probabilités et distributions"
category: concepts
tags: [data-science, statistics, probability, distributions]
level: 3
source_sha256: 4403ad9a90aabc288cb47bda59120d51dab193fd7789e3a5f9c2dff1096bfb74
translation: machine
translated_at: '2026-10-24'
---
# Probabilités et distributions {#probability-and-distributions}

Théorie des probabilités fondamentale et distributions courantes utilisées tout au long de la data science et du ML. Comprendre les distributions est essentiel pour choisir des tests statistiques appropriés, construire des modèles génératifs et interpréter les résultats.

## Fondamentaux des probabilités {#probability-fundamentals}

**Probabilité** P(A) = mesure de la vraisemblance de l'événement A. Intervalle : [0, 1].

**Définition classique** : P(A) = nombre de cas favorables / nombre total de cas équiprobables.
**Définition fréquentiste** : P(A) = lim(N->inf) count(A) / N.

### Règles clés {#key-rules}

| Règle | Formule |
|------|---------|
| Complément | P(non A) = 1 - P(A) |
| Addition | P(A ou B) = P(A) + P(B) - P(A et B) |
| Incompatibilité | P(A ou B) = P(A) + P(B) |
| Indépendance | P(A et B) = P(A) * P(B) |
| Conditionnelle | P(A\|B) = P(A et B) / P(B) |

**Schéma « au moins un »** : P(au moins un) = 1 - P(aucun). Bien plus simple que le calcul direct.

### Théorème de Bayes {#bayes-theorem}

P(A|B) = P(B|A) * P(A) / P(B)

- P(A|B) : postérieure (ce que l'on cherche)
- P(B|A) : vraisemblance
- P(A) : a priori
- P(B) : évidence (marginale)

**Piège** : P(A|B) != P(B|A). P(maladie|test positif) n'est PAS P(test positif|maladie).

### Probabilité totale {#total-probability}

P(A) = somme_i P(A|B_i) * P(B_i) où {B_i} forme une partition de l'espace des événements.

## Variables aléatoires {#random-variables}

**Discrètes** : valeurs dénombrables (lancer de dé, nombre de clients). Décrites par une PMF.
**Continues** : toute valeur dans un intervalle (taille, température). Décrites par une PDF.

- **Espérance** : E(X) = somme(x_i * P(x_i)) ou intégrale(x * f(x) dx)
- **Variance** : Var(X) = E[(X - E[X])^2] = E[X^2] - (E[X])^2

## Distributions discrètes courantes {#common-discrete-distributions}

### Bernoulli {#bernoulli}
Essai unique de probabilité de succès p.
- E(X) = p, Var(X) = p(1-p)

### Binomiale {#binomial}
k succès sur n essais de Bernoulli indépendants.
- P(k) = C(n,k) * p^k * (1-p)^(n-k)
- E(X) = np, Var(X) = np(1-p)

### Poisson {#poisson}
Nombre d'événements dans un intervalle fixe avec un taux lambda.
- P(k) = (lambda^k / k!) * e^(-lambda)
- E(X) = Var(X) = lambda
- À utiliser pour : événements rares, données de comptage (appels/heure, accidents/mois)

## Distributions continues courantes {#common-continuous-distributions}

### Normale (gaussienne) {#normal-gaussian}
En forme de cloche, symétrique. Définie par mu (moyenne) et sigma (écart-type).
```python
from scipy import stats
norm = stats.norm(loc=0, scale=1)
norm.pdf(0)      # density at 0
norm.cdf(1.96)   # P(X <= 1.96) ~ 0.975
norm.ppf(0.95)   # 95th percentile ~ 1.645
```

**Théorème central limite** : la somme ou la moyenne d'un grand nombre de variables aléatoires indépendantes tend vers une loi normale, quelles que soient leurs distributions individuelles. C'est pourquoi la loi normale est si courante.

### Exponentielle {#exponential}
Temps entre événements indépendants à taux constant.
- Sans mémoire : P(X > s + t | X > s) = P(X > t)
- E(X) = 1/lambda, Var(X) = 1/lambda^2

### Uniforme {#uniform}
Toutes les issues équiprobables sur [a, b].
- E(X) = (a+b)/2, Var(X) = (b-a)^2/12

## Combinatoire {#combinatorics}

- **Permutations** (l'ordre compte) : P(n,k) = n! / (n-k)!
- **Combinaisons** (l'ordre ne compte pas) : C(n,k) = n! / (k!(n-k)!)
- **Avec répétition** : permutations = n^k, combinaisons = C(n+k-1, k)
- **Théorème du binôme** : (a+b)^n = somme C(n,k) * a^(n-k) * b^k

## Théorèmes clés {#key-theorems}

- **Loi des grands nombres** : la moyenne empirique converge vers la moyenne de la population lorsque n -> inf
- **Théorème central limite** : la moyenne échantillonnale centrée réduite -> N(0,1) lorsque n -> inf
- **Inégalité de Bienaymé-Tchebychev** : P(|X - mu| >= k*sigma) <= 1/k^2 (pour toute distribution)

## Simuler des distributions {#simulating-distributions}

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

## Pièges {#gotchas}
- Poisson n'est PAS simplement « binomiale avec n grand et p petit » : Poisson suppose un taux constant, la binomiale suppose un nombre fixe d'essais
- La loi normale n'est **pas** universelle : de nombreuses distributions réelles sont fortement asymétriques (revenus, tailles de fichiers)
- Le TCL requiert une variance finie : il échoue pour les distributions à queues lourdes (Cauchy)
- L'exponentielle est la **seule** loi continue sans mémoire

## Voir aussi {#see-also}
- [[descriptive-statistics]] - synthèses empiriques des données
- [[hypothesis-testing]] - utiliser les distributions pour l'inférence statistique
- [[bayesian-methods]] - le théorème de Bayes dans le contexte du ML
- [[math-for-ml]] - fondements de la théorie des probabilités
