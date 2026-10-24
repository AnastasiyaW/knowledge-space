---
title: "Problem des Handlungsreisenden (TSP)"
category: algorithms
tags: [algorithms, graphs, TSP, NP-hard, approximation, optimization, bitmask-dp]
level: 3
source_sha256: 072ddc74b5aef3cc89604d7ed095c847783a657b464d05aefb509b1711730205
translation: machine
translated_at: '2026-10-24'
---
# Problem des Handlungsreisenden (TSP) {#traveling-salesman-problem-tsp}

Finde die kürzeste Route, die jede Stadt genau einmal besucht und zum Ausgangspunkt zurückkehrt. NP-schwer – es ist kein polynomialer exakter Algorithmus bekannt. Praktische Ansätze reichen von Brute Force (n <= 10) über DP (n <= 20) bis zu Heuristiken (n > 20).

## Wichtige Fakten {#key-facts}

- **Brute Force**: O(n!) – alle Permutationen durchprobieren
- **Held-Karp-DP**: O(2^n * n^2) Zeit, O(2^n * n) Speicher – Bitmask-DP
- **Nearest-Neighbor-Heuristik**: O(n^2), typischerweise 20–25 % über dem Optimum
- **Christofides**: O(n^3), garantiert <= 1,5-faches des Optimums für metrisches TSP
- **2-Opt-Lokalsuche**: verbessert iterativ durch Umkehren von Teilstrecken
- TSP != kürzester Weg: es müssen ALLE Städte besucht werden, nicht nur der Weg von A nach B

## TSP-Varianten {#tsp-variants}

| Variante | Definition |
|---------|-----------|
| Symmetrisch | dist(A,B) = dist(B,A), ungerichtet |
| Asymmetrisch | Gerichtet, Distanzen können je nach Richtung verschieden sein |
| Metrisch | Symmetrisch + Dreiecksungleichung |
| Mit Dreiecksungleichung | dist(A,C) <= dist(A,B) + dist(B,C) |

## Praktische Hinweise {#practical-guidance}

| n | Ansatz |
|---|---------|
| <= 10 | Brute Force O(n!) |
| <= 20 | Held-Karp-DP O(2^n * n^2) |
| <= 100 | Nearest Neighbor + 2-Opt |
| > 100 | Christofides, LKH oder Metaheuristiken |

## Muster {#patterns}

### Brute Force – O(n!) {#brute-force-on}

```python
from itertools import permutations

def tsp_brute_force(dist, start=0):
    cities = [i for i in range(len(dist)) if i != start]
    min_cost = float('inf')
    best_route = None
    for perm in permutations(cities):
        route = [start] + list(perm) + [start]
        cost = sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))
        if cost < min_cost:
            min_cost = cost
            best_route = route
    return best_route, min_cost
```

### Held-Karp-DP – O(2^n * n^2) {#held-karp-dp-o2n-n2}

Bitmask-DP. Zustand: dp[S][v] = minimale Kosten, um alle Städte in der Bitmaske S zu besuchen und bei Stadt v zu enden.

```python
def tsp_dp(dist):
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0, visited = {0}

    for S in range(1 << n):
        for v in range(n):
            if dp[S][v] == INF or not (S >> v & 1):
                continue
            for u in range(n):
                if S >> u & 1:
                    continue  # already visited
                new_S = S | (1 << u)
                dp[new_S][u] = min(dp[new_S][u], dp[S][v] + dist[v][u])

    full = (1 << n) - 1
    return min(dp[full][v] + dist[v][0] for v in range(1, n))
```

Für n=20: ca. 20 Mio. Zustände – machbar. Für n=30: nicht praktikabel.

### Nearest-Neighbor-Heuristik – O(n^2) {#nearest-neighbor-heuristic-on2}

```python
def nearest_neighbor(dist, start=0):
    n = len(dist)
    visited = [False] * n
    route = [start]
    visited[start] = True
    current = start

    for _ in range(n - 1):
        nearest = min(
            (j for j in range(n) if not visited[j]),
            key=lambda j: dist[current][j]
        )
        route.append(nearest)
        visited[nearest] = True
        current = nearest

    route.append(start)
    return route
```

### 2-Opt-Lokalsuche {#2-opt-local-search}

```python
def two_opt(route, dist):
    improved = True
    while improved:
        improved = False
        n = len(route) - 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                if tour_length(new_route, dist) < tour_length(route, dist):
                    route = new_route
                    improved = True
    return route
```

### Christofides-Algorithmus (Konzept) {#christofides-algorithm-concept}

Für metrisches TSP (Dreiecksungleichung) garantiert 1,5-faches des Optimums:
1. Minimalen Spannbaum (MST) bestimmen
2. Minimum-Gewicht-perfektes Matching auf den Knoten mit ungradem Grad finden
3. MST und Matching zu einem eulerschen Graphen kombinieren
4. Eulerkreis finden
5. Mehrfach besuchte Knoten abkürzen

## Verwandte Probleme {#related-problems}

- **Kürzeste Superstring**: kürzeste Zeichenkette, die alle gegebenen Zeichenketten als Teilzeichenketten enthält. Äquivalent zum TSP auf dem Überlappungsgraphen. NP-schwer.

## Fallstricke {#gotchas}

- TSP lässt sich nicht in unabhängige Teilprobleme mit kürzesten Wegen zerlegen
- Nearest Neighbor kann sehr schlechte Routen mit „Backtracking“-Mustern erzeugen
- 2-Opt konvergiert zu einem LOKALEN Minimum – mehrere zufällige Neustarts verbessern die Ergebnisse
- Christofides funktioniert nur mit Dreiecksungleichung (metrisches TSP)
- Bitmask-DP benötigt eine ganzzahlige Bitmaske – Python unterstützt beliebig große Ints, aber der Speicher ist die Grenze

## Siehe auch {#see-also}

- [[eulerian-hamiltonian-paths]] – TSP = minimal gewichteter Hamiltonkreis
- [[minimum-spanning-trees]] – MST wird in der Christofides-Approximation verwendet
- [[complexity-classes]] – TSP ist NP-schwer
- [[dp-optimization-problems]] – Bitmask-DP-Technik
