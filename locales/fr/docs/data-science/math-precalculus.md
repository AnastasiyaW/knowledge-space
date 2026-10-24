---
title: "Fondations du pré-calcul"
category: foundations
tags: [data-science, math, algebra, functions, sets]
level: 2
source_sha256: cfc7fccf46941d83e30a97a100c43ce6e2812aecb97209f9f3a5d1bbdffe3eb4
translation: machine
translated_at: '2026-10-24'
---
# Fondations du pré-calcul {#pre-calculus-foundations}

Systèmes de nombres, équations, fonctions et théorie élémentaire des ensembles - les prérequis avant d'aborder le calcul, les probabilités et l'algèbre linéaire.

## Systèmes de nombres {#number-systems}

N (entiers naturels) subset Z (entiers relatifs) subset Q (rationnels) subset R (réels) subset C (complexes)

- **Rationnels** : fractions p/q. Le développement décimal est fini ou périodique
- **Irrationnels** : sqrt(2), pi, e. Développement non fini et non périodique
- **Théorème fondamental** : tout entier > 1 possède une décomposition unique en facteurs premiers

## Équations {#equations}

### Quadratique : ax^2 + bx + c = 0 {#quadratic-ax2-bx-c-0}
- Discriminant D = b^2 - 4ac
- D > 0 : deux racines réelles, D = 0 : une racine, D < 0 : aucune racine réelle
- x = (-b +/- sqrt(D)) / (2a)
- Relations de Viète : x1 + x2 = -b/a, x1 * x2 = c/a

### Systèmes {#systems}
- **Substitution** : résoudre une équation pour une variable, puis substituer
- **Élimination** : additionner ou soustraire les équations
- Types : unique (droites sécantes), aucune solution (droites parallèles), infinité (droites confondues)

## Inéquations {#inequalities}

- Lors d'une multiplication ou division par un négatif : **inverser le sens** de l'inégalité
- **Méthode des intervalles** pour une fraction rationnelle : trouver les zéros, étudier le signe sur chaque intervalle
- Quadratique : trouver les racines, utiliser le sens de la parabole

## Fonctions élémentaires {#elementary-functions}

| Fonction | Domaine | Propriété clé |
|----------|---------|---------------|
| Linéaire : y = kx + b | R | Taux de variation constant |
| Quadratique : y = ax^2 + bx + c | R | Sommet en x = -b/(2a) |
| Exponentielle : y = a^x | R | Toujours positive, monotone |
| Logarithmique : y = log_a(x) | x > 0 | Réciproque de l'exponentielle |
| Trigonométrique : sin, cos | R | Période 2*pi, image [-1, 1] |

**Propriétés du logarithme** : log(ab) = log(a) + log(b), log(a^n) = n*log(a), log_a(x) = ln(x)/ln(a)

**Identités clés** : sin^2 + cos^2 = 1, e^(i*theta) = cos(theta) + i*sin(theta)

### Transformations de graphes {#graph-transformations}
- f(x) + c : translation vers le haut
- f(x - c) : translation vers la droite
- c*f(x) : étirement vertical
- f(cx) : compression horizontale

## Ensembles {#sets}

- **Union** A cup B : dans A OU dans B
- **Intersection** A cap B : dans A ET dans B
- **Différence** A \ B : dans A mais pas dans B
- **Lois de De Morgan** : (A cup B)^c = A^c cap B^c
- **Principe d'inclusion-exclusion** : |A cup B| = |A| + |B| - |A cap B|
- **Ensemble des parties** : |P(A)| = 2^|A|

## Combinatoire {#combinatorics}

- **Arrangements** (l'ordre compte) : P(n,k) = n!/(n-k)!
- **Combinaisons** (l'ordre ne compte pas) : C(n,k) = n!/(k!(n-k)!)
- **Théorème binomial** : (a+b)^n = somme C(n,k) * a^(n-k) * b^k
- **Principe des tiroirs** : n objets dans m boîtes, n > m -> au moins une boîte en contient plus d'un

## Suites {#sequences}

- **Arithmétique** : a_n = a_1 + (n-1)d, S_n = n(a_1+a_n)/2
- **Géométrique** : a_n = a_1 * r^(n-1), somme infinie (|r|<1) : S = a_1/(1-r)
- **Intérêts composés** : A = P(1+r)^n

## Voir aussi {#see-also}
- [[math-for-ml]] - le calcul s'appuie sur ces fondements
- [[math-linear-algebra]] - vecteurs et matrices
- [[probability-distributions]] - les probabilités utilisent la combinatoire
