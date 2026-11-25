---
title: "Récursivité et bases des algorithmes"
category: concepts
tags: [python, recursion, algorithms, big-o, binary-search, sorting, memoization]
level: 2
source_sha256: 4a8afca92f73f42a0953416f3533fdbc9891a2366cbe47c4c729bb2daee22633
translation: machine
translated_at: '2026-10-24'
---
# Récursivité et bases des algorithmes {#recursion-and-algorithm-basics}

La récursivité consiste pour une fonction à s'appeler elle-même. Toute fonction récursive nécessite un cas de base (condition d'arrêt) et un cas récursif (qui rapproche du cas de base). Comprendre la notation Big O aide à choisir le bon algorithme selon la taille des données.

## Faits essentiels {#key-facts}

- La limite de récursion par défaut de Python est 1000 (`sys.getrecursionlimit()`)
- Python n'optimise PAS la récursion terminale - convertissez en itération pour une récursion profonde
- `@lru_cache` transforme le Fibonacci exponentiel O(2^n) en linéaire O(n)
- Big O décrit comment les performances évoluent en fonction de la taille de l'entrée
- La fonction `sorted()` de Python utilise Timsort - O(n log n), hybride entre tri fusion et tri par insertion

## Motifs {#patterns}

### Récursivité classique {#classic-recursion}
```python
def factorial(n):
    if n <= 1:       # base case
        return 1
    return n * factorial(n - 1)  # recursive case

def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)  # exponential without memoization!
```

### Fibonacci avec mémoïsation {#memoized-fibonacci}
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

fib(100)  # instant, O(n)
```

### Recherche dichotomique (récursive) {#binary-search-recursive}
```python
def binary_search(arr, target, low=0, high=None):
    if high is None: high = len(arr) - 1
    if low > high: return -1
    mid = (low + high) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)
```

### Aplatir une liste imbriquée {#flatten-nested-list}
```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
```

### Parcours d'arbre {#tree-traversal}
```python
def tree_sum(node):
    if node is None: return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)
```

### Convertir une récursion en itération {#converting-recursion-to-iteration}
```python
# Recursive DFS
def dfs(node):
    if node is None: return
    print(node.value)
    dfs(node.left)
    dfs(node.right)

# Iterative DFS with explicit stack
def dfs_iterative(root):
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None: continue
        print(node.value)
        stack.append(node.right)
        stack.append(node.left)
```

### Récursion terminale (motif à accumulateur) {#tail-recursion-accumulator-pattern}
```python
# Not tail recursive (multiplication after recursive call)
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

# Tail recursive (but Python doesn't optimize it)
def factorial(n, acc=1):
    if n <= 1: return acc
    return factorial(n - 1, acc * n)

# Iterative (best for Python)
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

## Notation Big O {#big-o-notation}

| Complexité | Nom | Exemple |
|-----------|------|---------|
| O(1) | Constante | Recherche dans une table de hachage, accès dict/set |
| O(log n) | Logarithmique | Recherche dichotomique |
| O(n) | Linéaire | Parcours de liste, recherche linéaire |
| O(n log n) | Linéarithmique | Tri efficace (fusion, Timsort) |
| O(n^2) | Quadratique | Boucles imbriquées, tri à bulles |
| O(2^n) | Exponentielle | Fibonacci récursif naïf |

## Quand utiliser la récursion ou l'itération {#when-to-use-recursion-vs-iteration}

**Récursion** : parcours d'arbres ou de graphes, diviser pour régner (tri fusion, tri rapide), structures naturellement récursives, profondeur bornée.

**Itération** : boucles simples, profondeur pouvant dépasser environ 500, performances critiques, solution itérative aussi claire.

## Pièges à éviter {#gotchas}

- Cas de base manquant -> récursion infinie -> `RecursionError`
- Le Fibonacci naïf recalcule les mêmes valeurs de façon exponentielle - mémoïsez toujours
- La limite de récursion de Python (1000) est volontairement basse - utilisez l'itération pour une récursion profonde
- Modifier des arguments mutables (listes/dicts) partagés entre appels récursifs provoque des bugs
- `sys.setrecursionlimit(n)` existe mais signale un problème de conception

## Voir aussi {#see-also}

- [[functions]] - mécanique des appels de fonctions
- [[iterators-and-generators]] - séquences paresseuses comme alternative à l'itération
- [[profiling-and-optimization]] - mesurer les performances des algorithmes
