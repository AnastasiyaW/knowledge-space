---
title: "Classes de complexité : P, NP, NP-complet"
category: concepts
tags: [algorithms, complexity-theory, P, NP, NP-complete, NP-hard, reductions]
level: 2
source_sha256: db9d509f35ebb5f29a067aa20a4e580604f24aae9beae6911afe9b22ed70ba7c
translation: machine
translated_at: '2026-10-24'
---
# Classes de complexité : P, NP, NP-complet {#complexity-classes-p-np-np-complete}

Les classes de complexité regroupent les problèmes de décision selon les ressources de calcul nécessaires pour les résoudre ou les vérifier. La question P vs NP, c'est-à-dire savoir si tout problème dont la solution peut être vérifiée rapidement peut aussi être résolu rapidement, est l'un des problèmes ouverts les plus importants de l'informatique.

## Points clés {#key-facts}

- **P** : problèmes de décision résolubles en temps polynomial. Exemples : test de palindrome, plus court chemin, tri
- **NP** : problèmes de décision pour lesquels une réponse OUI peut être **vérifiée** en temps polynomial. Exemple : étant donnée une partition, vérifier en O(n) que les deux moitiés ont la même somme
- **NP-complet** : problèmes les plus difficiles de NP, vers lesquels tout problème de NP se réduit en temps polynomial. Exemples : chemin hamiltonien, 3-SAT
- **NP-difficile** : au moins aussi difficile que NP-complet, mais pas nécessairement dans NP (il peut ne pas s'agir de problèmes de décision). Exemples : problème de l'arrêt, version optimisation du TSP
- Tous les problèmes de P sont dans NP (un problème résoluble en temps polynomial est aussi vérifiable)
- P ≠ NP est largement admis mais non démontré (problème du prix du millénaire, 1 M$)

## Hiérarchie des classes {#class-hierarchy}

```text
NP-hard
  |-- NP-complete  <-- hardest problems IN NP
  |-- (problems not in NP, e.g., halting problem)
NP
  |-- NP-complete
  |-- P  (assuming P != NP)
```

## Schémas {#patterns}

### Réduction {#reduction}

Transformer le problème A en problème B de sorte que la résolution de B permette de résoudre A. Si B est dans P et que A se réduit à B en temps polynomial, alors A est dans P.

Pour prouver qu'un problème X est NP-complet :
1. Montrer que X est dans NP (solution vérifiable en temps polynomial)
2. Montrer qu'un problème NP-complet connu se réduit à X en temps polynomial

### Problèmes NP-complets courants {#common-np-complete-problems}

| Problème | Description |
|---------|-------------|
| 3-SAT | Satisfiabilité d'une formule booléenne en 3-CNF |
| Chemin/Cycle hamiltonien | Visiter chaque sommet exactement une fois |
| Coloration de graphe (k >= 3) | Colorier les sommets avec k couleurs, sans sommets adjacents de même couleur |
| Somme de sous-ensemble | Existe-t-il un sous-ensemble dont la somme vaut la cible ? |
| Voyageur de commerce (décision) | Existe-t-il un circuit de coût <= k ? |
| Partition | Répartir un tableau en deux moitiés de même somme |

### Implications pratiques {#practical-implications}

- Si votre problème est NP-difficile, ne cherchez pas d'algorithme exact polynomial
- Utilisez des algorithmes d'approximation (par exemple Christofides pour le TSP : 1,5 fois l'optimal)
- Utilisez des heuristiques (glouton, recherche locale, algorithmes génétiques)
- Les solutions exactes ne sont envisageables que pour de petites entrées (programmation dynamique en temps exponentiel, par exemple Held-Karp en O(2^n * n^2))

## Pièges {#gotchas}

- NP ne signifie PAS « non polynomial » : cela signifie « polynomial non déterministe »
- Les problèmes NP-difficiles peuvent ne pas être dans NP du tout (variantes d'optimisation de problèmes de décision)
- La 2-coloration est polynomiale, mais la 3-coloration est NP-complète
- La somme de sous-ensemble est NP-complète mais admet une solution DP pseudo-polynomiale en O(n*S) (polynomiale en la valeur de S, et non en la taille de sa représentation binaire)
- Qu'un problème soit NP-complet ne signifie pas qu'il est toujours difficile : de nombreuses instances sont faciles, seul le pire cas est difficile

## Voir aussi {#see-also}

- [[complexity-analysis]] - fondements de l'analyse asymptotique
- [[traveling-salesman-problem]] - problème d'optimisation NP-difficile classique
- [[graph-coloring]] - NP-complet pour k >= 3
- [[dp-optimization-problems]] - solutions pseudo-polynomiales pour les problèmes NP-complets
