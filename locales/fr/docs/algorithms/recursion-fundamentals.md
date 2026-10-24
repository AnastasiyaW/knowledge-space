---
title: "Principes fondamentaux de la récursivité"
category: concepts
tags: [recursion, call-stack, divide-and-conquer, memoization]
level: 2
source_sha256: 852141ddf0932264067198d8f7055fc94ef73b6b00990cba7159f1cd7d73d256
translation: machine
translated_at: '2026-10-24'
---
# Principes fondamentaux de la récursivité {#recursion-fundamentals}

Fonction qui s'appelle elle-même pour résoudre des instances plus petites du même problème. Fondement de la méthode diviser pour régner, de la programmation dynamique (DP), du backtracking et du parcours d'arbres et de graphes.

## Points clés {#key-facts}

- Toute récursion nécessite : un cas de base + un cas récursif
- La pile d'appels stocke les variables locales et l'adresse de retour pour chaque appel
- Profondeur de pile = profondeur de récursion. Limite par défaut de Python : 1000 (`sys.setrecursionlimit()`)
- Récursion terminale : l'appel récursif est la dernière opération. Python n'optimise PAS les appels terminaux
- Toute récursion peut être convertie en itération à l'aide d'une pile explicite
- Complexité temporelle : résoudre la relation de récurrence (théorème maître pour la méthode diviser pour régner)

## Structure {#structure}

```python
def recursive_function(problem):
    # Base case - termination condition
    if is_trivial(problem):
        return trivial_solution

    # Recursive case - break into smaller subproblems
    smaller = reduce(problem)
    sub_result = recursive_function(smaller)

    # Combine
    return combine(sub_result)
```

## Motifs {#patterns}

### Récursion linéaire {#linear-recursion}

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
# T(n) = T(n-1) + O(1) -> O(n)
```

### Récursion binaire (diviser pour régner) {#binary-recursion-divide-and-conquer}

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
# T(n) = 2T(n/2) + O(n) -> O(n log n)
```

### Récursion en arbre (branches multiples) {#tree-recursion-multiple-branches}

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
# T(n) = T(n-1) + T(n-2) -> O(2^n) without memoization
```

### De la récursion à l'itération {#recursion-to-iteration}

```python
# Recursive DFS
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# Iterative DFS (explicit stack)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

### Mémoïsation (mise en cache des sous-problèmes qui se chevauchent) {#memoization-caching-overlapping-subproblems}

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
# O(2^n) -> O(n) with memoization
```

### Mémoïsation manuelle {#manual-memoization}

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

## Théorème maître (récurrences de diviser pour régner) {#master-theorem-divide-and-conquer-recurrences}

Pour `T(n) = aT(n/b) + O(n^d)` :

| Condition | Complexité |
|-----------|-----------|
| d > log_b(a) | O(n^d) |
| d = log_b(a) | O(n^d * log n) |
| d < log_b(a) | O(n^(log_b(a))) |

Exemples :
- Recherche dichotomique : T(n) = T(n/2) + O(1) -> a=1, b=2, d=0 -> O(log n)
- Tri fusion : T(n) = 2T(n/2) + O(n) -> a=2, b=2, d=1 -> O(n log n)
- Multiplication de Karatsuba : T(n) = 3T(n/2) + O(n) -> O(n^1.585)

## Compromis entre récursion et itération {#recursion-vs-iteration-trade-offs}

| Aspect | Récursion | Itération |
|--------|-----------|-----------|
| Lisibilité | Souvent plus claire pour les arbres et les graphes | Plus claire pour les problèmes linéaires |
| Utilisation de la pile | O(profondeur) pour la pile d'appels | O(1) ou pile explicite |
| Performance | Surcoût des appels de fonction | Généralement plus rapide |
| Dépassement de pile | Risque à partir d'une profondeur de 1000 | Aucun risque |
| Gestion de l'état | Implicite via la pile d'appels | Variables explicites |

## Pièges {#gotchas}

- **Problème :** Dépassement de pile dû à une récursion profonde en Python (limite par défaut 1000) -> **Correctif :** Utiliser `sys.setrecursionlimit(N)` avec précaution, ou convertir en version itérative avec une pile explicite. Pour la DP, privilégier la tabulation ascendante (bottom-up).
- **Problème :** Temps exponentiel dû au recalcul de sous-problèmes qui se chevauchent -> **Correctif :** Ajouter une mémoïsation (`@lru_cache` ou dictionnaire manuel). Si les sous-problèmes se chevauchent, une récursion sans mémoïsation est un bogue.
- **Problème :** Les arguments par défaut mutables utilisés comme dictionnaire de mémoïsation persistent entre les appels -> **Correctif :** Utiliser le motif `memo=None` avec `if memo is None: memo = {}` dans le corps de la fonction.

## Voir aussi {#see-also}

- [[dynamic-programming-fundamentals]] - récursion + mémoïsation = DP descendante (top-down)
- [[backtracking]] - récursion avec élagage
- [[graph-traversal-bfs-dfs]] - le DFS est un parcours récursif de graphe
- [[complexity-analysis]] - relations de récurrence pour la complexité récursive
