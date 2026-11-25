---
title: "Principes fondamentaux de la programmation dynamique"
category: concepts
tags: [algorithms, dynamic-programming, memoization, tabulation, optimization]
level: 2
source_sha256: 169db07a934f0bb1a9a7d117b19cf6208b89fb1970b793f8019ad7732815a7a8
translation: machine
translated_at: '2026-10-24'
---
# Principes fondamentaux de la programmation dynamique {#dynamic-programming-fundamentals}

La programmation dynamique (DP) résout des problèmes en les décomposant en sous-problèmes qui se chevauchent et en stockant les résultats pour éviter les recalculs. Elle s'applique lorsqu'un problème possède une sous-structure optimale (une solution optimale à partir de sous-solutions optimales) et des sous-problèmes qui se chevauchent (les mêmes sous-problèmes résolus de façon répétée dans une récursion naïve).

## Points clés {#key-facts}

- **Top-down (memoization)** : récursif + cache, ne calcule que les sous-problèmes nécessaires
- **Bottom-up (tabulation)** : itératif, remplit la table à partir des cas de base, sans surcoût de récursion
- La DP réduit une récursion exponentielle à un coût polynomial grâce au cache - typiquement de O(2^n) à O(n*m) ou O(n^2)
- Commencer par la memoization pour valider la logique, puis convertir en tabulation pour les performances
- Une optimisation de l'espace est souvent possible en ne conservant que les 1 à 2 dernières lignes ou valeurs

## Top-Down vs Bottom-Up {#top-down-vs-bottom-up}

| | Top-Down (Memoization) | Bottom-Up (Tabulation) |
|-|----------------------|----------------------|
| Implémentation | Récursive - naturelle à partir de la récurrence | Itérative - nécessite de déterminer l'ordre de remplissage |
| Sous-problèmes calculés | Uniquement ceux nécessaires | Tous les sous-problèmes |
| Surcoût | Pile d'appels, recherche dans un dictionnaire | Accès à un tableau (plus rapide) |
| Dépassement de pile | Risque en cas de récursion profonde | Aucun risque |
| Optimisation de l'espace | Plus difficile | Plus simple (ligne par ligne) |

## Patterns {#patterns}

### Identifier la récurrence DP {#identifying-dp-recurrence}

1. Définir ce que représente `dp[state]` (être précis sur son sens)
2. Écrire les cas de base
3. Écrire la récurrence : `dp[state] = f(dp[smaller_states])`
4. Identifier l'ordre de parcours pour que les dépendances soient résolues avant utilisation
5. Retourner l'état cible

### Exemple guide : chemin de coût minimal dans une matrice {#running-example-min-cost-path-in-matrix}

Se déplacer uniquement vers la droite ou vers le bas, du coin supérieur gauche au coin inférieur droit, en minimisant le coût total.

**Récursion naïve - O(2^(n+m)) :**

```python
def min_cost(matrix, i=0, j=0):
    n, m = len(matrix), len(matrix[0])
    if i == n or j == m:
        return float('inf')
    if i == n - 1 and j == m - 1:
        return matrix[i][j]
    return matrix[i][j] + min(min_cost(matrix, i + 1, j),
                               min_cost(matrix, i, j + 1))
```

**Top-Down (Memoization) - O(n*m) :**

```python
def min_cost(matrix, i=0, j=0, memo=None):
    if memo is None:
        memo = {}
    if (i, j) in memo:
        return memo[(i, j)]
    n, m = len(matrix), len(matrix[0])
    if i == n or j == m:
        return float('inf')
    if i == n - 1 and j == m - 1:
        return matrix[i][j]
    memo[(i, j)] = matrix[i][j] + min(
        min_cost(matrix, i + 1, j, memo),
        min_cost(matrix, i, j + 1, memo)
    )
    return memo[(i, j)]
```

**Bottom-Up (Tabulation) - O(n*m) :**

```python
def min_cost(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * m for _ in range(n)]
    dp[n - 1][m - 1] = matrix[n - 1][m - 1]

    for j in range(m - 2, -1, -1):  # last row
        dp[n - 1][j] = matrix[n - 1][j] + dp[n - 1][j + 1]
    for i in range(n - 2, -1, -1):  # last column
        dp[i][m - 1] = matrix[i][m - 1] + dp[i + 1][m - 1]
    for i in range(n - 2, -1, -1):  # rest
        for j in range(m - 2, -1, -1):
            dp[i][j] = matrix[i][j] + min(dp[i + 1][j], dp[i][j + 1])

    return dp[0][0]
```

### Compter les chemins dans une grille {#counting-paths-in-grid}

```python
def count_paths(n, m):
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        dp[i][0] = 1
    for j in range(m):
        dp[0][j] = 1
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[n - 1][m - 1]
```

Formule mathématique : C(n+m-2, n-1) - choisir quelles étapes sont vers le bas.

## Pièges {#gotchas}

- Un algorithme glouton échoue souvent là où la DP réussit - toujours se diriger vers le voisin le moins coûteux peut manquer l'optimum global
- Le top-down avec des dictionnaires Python peut être lent pour de grands espaces d'états - la tabulation avec des tableaux est plus rapide
- La limite de récursion de Python (1000 par défaut) peut faire planter une DP top-down sur de grandes entrées - utiliser `sys.setrecursionlimit` ou passer en bottom-up
- Piège des arguments par défaut mutables : utiliser `None` comme valeur par défaut et initialiser à l'intérieur de la fonction
- L'optimisation de l'espace (ne conserver que la dernière ligne) empêche de reconstruire le chemin de solution effectif

## Voir aussi {#see-also}

- [[dp-sequence-problems]] - LCS, distance d'édition, LIS, word break
- [[dp-optimization-problems]] - sac à dos, rendu de monnaie, house robber
- [[dp-grid-problems]] - chemin dans une matrice, carré maximal, gold mine
- [[complexity-analysis]] - comprendre la réduction de complexité en DP
