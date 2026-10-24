---
title: "Rekursion und Grundlagen von Algorithmen"
category: concepts
tags: [python, recursion, algorithms, big-o, binary-search, sorting, memoization]
level: 2
source_sha256: 4a8afca92f73f42a0953416f3533fdbc9891a2366cbe47c4c729bb2daee22633
translation: machine
translated_at: '2026-10-24'
---
# Rekursion und Grundlagen von Algorithmen {#recursion-and-algorithm-basics}

Rekursion liegt vor, wenn eine Funktion sich selbst aufruft. Jede rekursive Funktion benötigt einen Basisfall (Abbruchbedingung) und einen rekursiven Fall (Annäherung an den Basisfall). Das Verständnis der Big-O-Notation hilft dabei, den passenden Algorithmus für die Datenmenge auszuwählen.

## Wichtige Fakten {#key-facts}

- Das Standard-Rekursionslimit von Python beträgt 1000 (`sys.getrecursionlimit()`)
- Python optimiert Tail-Rekursion **nicht** - für tiefe Rekursion auf Iteration umstellen
- `@lru_cache` macht aus der exponentiellen Fibonacci-Berechnung O(2^n) eine lineare O(n)-Berechnung
- Big O beschreibt, wie sich die Performance mit der Eingabegröße skaliert
- Pythons `sorted()` verwendet Timsort - ein hybrides O(n log n)-Verfahren aus Merge Sort und Insertion Sort

## Muster {#patterns}

### Klassische Rekursion {#classic-recursion}
```python
def factorial(n):
    if n <= 1:       # base case
        return 1
    return n * factorial(n - 1)  # recursive case

def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)  # exponential without memoization!
```

### Fibonacci mit Memoization {#memoized-fibonacci}
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

fib(100)  # instant, O(n)
```

### Binäre Suche (rekursiv) {#binary-search-recursive}
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

### Verschachtelte Liste abflachen {#flatten-nested-list}
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

### Baumdurchlauf {#tree-traversal}
```python
def tree_sum(node):
    if node is None: return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)
```

### Rekursion in Iteration umwandeln {#converting-recursion-to-iteration}
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

### Tail-Rekursion (Akkumulator-Muster) {#tail-recursion-accumulator-pattern}
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

## Big-O-Notation {#big-o-notation}

| Komplexität | Name | Beispiel |
|-----------|------|---------|
| O(1) | Konstant | Hash-Tabellen-Lookup, Dict-/Set-Zugriff |
| O(log n) | Logarithmisch | Binäre Suche |
| O(n) | Linear | Listendurchlauf, lineare Suche |
| O(n log n) | Linearithmisch | Effizientes Sortieren (Merge Sort, Timsort) |
| O(n^2) | Quadratisch | Verschachtelte Schleifen, Bubble Sort |
| O(2^n) | Exponentiell | Naive rekursive Fibonacci-Berechnung |

## Rekursion oder Iteration {#when-to-use-recursion-vs-iteration}

**Rekursion**: Baum- und Graphdurchläufe, Divide-and-Conquer (Merge Sort, Quicksort), natürlich rekursive Strukturen, begrenzte Tiefe.

**Iteration**: einfache Schleifen, Tiefe könnte ~500 überschreiten, Performance ist wichtig, iterative Lösung ist ebenso klar.

## Fallstricke {#gotchas}

- Fehlender Basisfall -> unendliche Rekursion -> `RecursionError`
- Naive Fibonacci-Berechnung berechnet dieselben Werte exponentiell neu - immer memoizen
- Das Rekursionslimit von Python (1000) ist absichtlich niedrig angesetzt - für tiefe Rekursion Iteration verwenden
- Veränderliche Argumente (Listen/Dicts), die über rekursive Aufrufe hinweg geteilt werden, verursachen Fehler
- `sys.setrecursionlimit(n)` existiert, weist aber auf ein Designproblem hin

## Siehe auch {#see-also}

- [[functions]] - Mechanik von Funktionsaufrufen
- [[iterators-and-generators]] - lazy Sequenzen als Alternative zur Iteration
- [[profiling-and-optimization]] - Messung der Algorithmus-Performance
