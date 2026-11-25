---
title: "Grundlagen der Rekursion"
category: concepts
tags: [recursion, call-stack, divide-and-conquer, memoization]
level: 2
source_sha256: 852141ddf0932264067198d8f7055fc94ef73b6b00990cba7159f1cd7d73d256
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen der Rekursion {#recursion-fundamentals}

Funktion, die sich selbst aufruft, um kleinere Instanzen desselben Problems zu lösen. Grundlage für Divide-and-Conquer, DP, Backtracking sowie Baum- und Graph-Traversierung.

## Wichtige Fakten {#key-facts}

- Jede Rekursion benötigt: Basisfall + rekursiver Fall
- Der Call Stack speichert lokale Variablen und die Rücksprungadresse für jeden Aufruf
- Stacktiefe = Rekursionstiefe. Standardlimit in Python: 1000 (`sys.setrecursionlimit()`)
- Tail-Rekursion: Der rekursive Aufruf ist die letzte Operation. Python optimiert Tail-Calls NICHT
- Jede Rekursion lässt sich mithilfe eines expliziten Stacks in Iteration umwandeln
- Zeitkomplexität: Rekurrenzrelation lösen (Master Theorem für Divide-and-Conquer)

## Struktur {#structure}

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

## Muster {#patterns}

### Lineare Rekursion {#linear-recursion}

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
# T(n) = T(n-1) + O(1) -> O(n)
```

### Binäre Rekursion (Divide and Conquer) {#binary-recursion-divide-and-conquer}

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

### Baumrekursion (mehrere Zweige) {#tree-recursion-multiple-branches}

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
# T(n) = T(n-1) + T(n-2) -> O(2^n) without memoization
```

### Rekursion in Iteration umwandeln {#recursion-to-iteration}

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

### Memoization (Zwischenspeichern überlappender Teilprobleme) {#memoization-caching-overlapping-subproblems}

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
# O(2^n) -> O(n) with memoization
```

### Manuelle Memoization {#manual-memoization}

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

## Master Theorem (Rekurrenzen für Divide and Conquer) {#master-theorem-divide-and-conquer-recurrences}

Für `T(n) = aT(n/b) + O(n^d)`:

| Bedingung | Komplexität |
|-----------|-----------|
| d > log_b(a) | O(n^d) |
| d = log_b(a) | O(n^d * log n) |
| d < log_b(a) | O(n^(log_b(a))) |

Beispiele:
- Binäre Suche: T(n) = T(n/2) + O(1) -> a=1, b=2, d=0 -> O(log n)
- Merge Sort: T(n) = 2T(n/2) + O(n) -> a=2, b=2, d=1 -> O(n log n)
- Karatsuba-Multiplikation: T(n) = 3T(n/2) + O(n) -> O(n^1.585)

## Abwägungen zwischen Rekursion und Iteration {#recursion-vs-iteration-trade-offs}

| Aspekt | Rekursion | Iteration |
|--------|-----------|-----------|
| Lesbarkeit | Oft klarer bei Bäumen/Graphen | Klarer bei linearen Problemen |
| Stack-Nutzung | O(Tiefe) Call Stack | O(1) oder expliziter Stack |
| Performance | Overhead durch Funktionsaufrufe | Im Allgemeinen schneller |
| Stack Overflow | Risiko ab Tiefe > 1000 | Kein Risiko |
| Zustandsverwaltung | Implizit über den Call Stack | Explizite Variablen |

## Fallstricke {#gotchas}

- **Problem:** Stack Overflow durch tiefe Rekursion in Python (Standardlimit 1000) -> **Lösung:** `sys.setrecursionlimit(N)` mit Bedacht verwenden oder mithilfe eines expliziten Stacks iterativ umschreiben. Bei DP ist bottom-up-Tabellierung vorzuziehen.
- **Problem:** Exponentielle Laufzeit durch wiederholte Berechnung überlappender Teilprobleme -> **Lösung:** Memoization hinzufügen (`@lru_cache` oder manuelles dict). Wenn sich Teilprobleme überlappen, ist Rekursion ohne Memoization ein Fehler.
- **Problem:** Veränderliche Standardargumente als Memo-dict bleiben über Aufrufe hinweg erhalten -> **Lösung:** Das Muster `memo=None` mit `if memo is None: memo = {}` im Funktionskörper verwenden.

## Siehe auch {#see-also}

- [[dynamic-programming-fundamentals]] - Rekursion + Memoization = Top-down-DP
- [[backtracking]] - Rekursion mit Pruning
- [[graph-traversal-bfs-dfs]] - DFS ist rekursive Graph-Traversierung
- [[complexity-analysis]] - Rekurrenzrelationen für rekursive Komplexität
