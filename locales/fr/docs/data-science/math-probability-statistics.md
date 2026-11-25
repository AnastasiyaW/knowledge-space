---
title: "Théorie des probabilités et inférence statistique"
category: foundations
tags: [data-science, math, probability, statistics, estimation, mle]
level: 4
source_sha256: 08eafc9585ce02b38613df2e15e24d75277e3f148e5453270d88e74b6bf821ca
translation: machine
translated_at: '2026-10-24'
---
# Théorie des probabilités et inférence statistique {#probability-theory-and-statistical-inference}

Fondements rigoureux des probabilités et méthodes d'estimation statistique. Fait le lien entre la théorie mathématique et les statistiques pratiques utilisées en ML.

## Axiomes des probabilités {#probability-axioms}

1. P(A) >= 0 pour tout événement A
2. P(espace des échantillons) = 1
3. Pour des événements mutuellement exclusifs : P(A1 ou A2 ou ...) = somme des P(Ai)

## Théorèmes clés {#key-theorems}

### Loi des grands nombres (faible) {#law-of-large-numbers-weak}
La moyenne empirique converge en probabilité vers la moyenne de la population lorsque n -> inf. Elle justifie l'utilisation des statistiques empiriques pour estimer les paramètres de la population.

### Théorème central limite {#central-limit-theorem}
Pour des variables aléatoires i.i.d. de moyenne mu et de variance sigma^2 :
(X_bar - mu) / (sigma / sqrt(n)) -> N(0,1) lorsque n -> inf

Quelle que soit la distribution d'origine. C'est pourquoi la loi normale apparaît partout.

### Inégalité de Bienaymé-Tchebychev {#chebyshevs-inequality}
P(|X - mu| >= k*sigma) <= 1/k^2 pour N'IMPORTE QUELLE distribution.
- k=2 : au plus 25 % des données au-delà de 2 sigma (empiriquement : environ 5 % pour une loi normale)
- k=3 : au plus 11 % au-delà de 3 sigma (empiriquement : environ 0,3 % pour une loi normale)

## Estimation statistique {#statistical-estimation}

### Propriétés des estimateurs ponctuels {#point-estimation-properties}
- **Sans biais** : E[theta_hat] = theta (en moyenne, correct)
- **Convergent** : theta_hat -> theta lorsque n -> inf (converge vers la vraie valeur)
- **Efficace** : atteint la variance minimale (borne de Cramér-Rao)
- **Exhaustif** : capture toute l'information sur theta contenue dans l'échantillon

### Estimation par maximum de vraisemblance (MLE) {#maximum-likelihood-estimation-mle}

Trouver les paramètres qui maximisent la vraisemblance des données observées.

L(theta) = produit des f(x_i | theta)

En pratique, on maximise la log-vraisemblance : l(theta) = somme des log f(x_i | theta)

**Propriétés** : le MLE est asymptotiquement efficace, convergent et asymptotiquement normal.

**Exemple (loi normale)** : le MLE de mu est la moyenne empirique, et le MLE de sigma^2 est la variance empirique (biaisée d'un facteur n/(n-1)).

### Méthode des moments {#method-of-moments}
Égaliser les moments empiriques aux moments théoriques. Plus simple que le MLE, mais souvent moins efficace.

## Test d'hypothèses (théorie) {#hypothesis-testing-theory}

### Cadre {#framework}
1. H0 (hypothèse nulle) et H1 (hypothèse alternative)
2. Choisir alpha (seuil de significativité, typiquement 0,05)
3. Calculer la statistique de test
4. Comparer à la valeur critique ou calculer la p-valeur
5. Rejeter H0 si la p-valeur < alpha

### Types d'erreurs {#error-types}
- **Erreur de type I** (alpha) : rejeter une H0 vraie (faux positif)
- **Erreur de type II** (beta) : ne pas rejeter une H0 fausse (faux négatif)
- **Puissance** = 1 - beta (probabilité de détecter un effet réel)

### Intervalles de confiance {#confidence-intervals}
- Variance connue : x_bar +/- z_(alpha/2) * sigma / sqrt(n)
- Variance inconnue : x_bar +/- t_(alpha/2, n-1) * s / sqrt(n)

La loi de Student présente des queues plus lourdes que la loi normale. Elle est utilisée pour les petits échantillons ou lorsque la variance de la population est inconnue.

## Types de convergence {#convergence-types}

Du plus faible au plus fort :
1. **En loi** : les fonctions de répartition convergent
2. **En probabilité** : P(|X_n - X| > epsilon) -> 0
3. **Presque sûrement** : P(lim X_n = X) = 1
4. **En moyenne (L^p)** : E[|X_n - X|^p] -> 0

## Analyse asymptotique {#asymptotic-analysis}

- f = o(g) : f croît strictement plus lentement. lim f/g = 0
- f = O(g) : f ne croît pas plus vite (à une constante près)
- f ~ g : équivalence asymptotique. lim f/g = 1
- Hiérarchie : ln(n) << n^a << a^n << n! << n^n

## Espérance et variance conditionnelles {#conditional-expectation-and-variance}

- E[X] = E[E[X|Y]] (loi de l'espérance totale)
- Var(X) = E[Var(X|Y)] + Var(E[X|Y]) (loi de la variance totale)

Utile dans : l'analyse bayésienne, les modèles de mélange, les modèles hiérarchiques.

## Pièges courants {#gotchas}
- Le MLE de la variance est biaisé (division par n, et non par n-1). La variance empirique non biaisée utilise n-1 (correction de Bessel)
- Le TCL nécessite une variance finie : il ne s'applique pas à la loi de Cauchy ni aux autres distributions à queues lourdes
- La p-valeur n'est PAS la probabilité que H0 soit vraie. Elle vaut P(données | H0)
- Intervalle de confiance : « 95 % des intervalles construits de cette manière contiennent le vrai paramètre » (interprétation fréquentiste)
- Significativité statistique != significativité pratique. Un effet minime peut être statistiquement significatif avec un grand n

## Voir aussi {#see-also}
- [[probability-distributions]] - distributions spécifiques
- [[hypothesis-testing]] - tests A/B en pratique
- [[descriptive-statistics]] - statistiques empiriques
- [[math-for-ml]] - calcul différentiel pour l'optimisation
