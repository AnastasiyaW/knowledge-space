---
title: Traveling Salesman Problem (TSP)
category: algorithms
tags: [algorithms, graphs, TSP, NP-hard, approximation, optimization, bitmask-dp]
---

# Traveling Salesman Problem (TSP)

Find the shortest route visiting every city exactly once and returning to origin. NP-hard - no known polynomial exact algorithm. Practical approaches range from brute force (n <= 10) to DP (n <= 20) to heuristics (n > 20).

## Key Facts

- **Brute force**: O(n!) - try all permutations
- **Held-Karp DP**: O(2^n * n^2) time, O(2^n * n) space - bitmask DP
- **Nearest Neighbor heuristic**: O(n^2), typically 20-25% above optimal
- **Christofides**: O(n^3), guaranteed <= 1.5x optimal for metric TSP
- **2-opt local search**: iteratively improves by reversing segments
- TSP != shortest path: must visit ALL cities, not just get from A to B

## TSP Variants

| Variant | Definition |
|---------|-----------|
| Symmetric | dist(A,B) = dist(B,A), undirected |
| Asymmetric | Directed, distances can differ by direction |
| Metric | Symmetric + triangle inequality |
| With triangle inequality | dist(A,C) <= dist(A,B) + dist(B,C) |

## Practical Guidance

| n | Approach |
|---|---------|
| <= 10 | Brute force O(n!) |
| <= 20 | Held-Karp DP O(2^n * n^2) |
| <= 100 | Nearest neighbor + 2-opt |
| > 100 | Christofides, LKH, or metaheuristics |

## Patterns

### Brute Force - O(n!)

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

### Held-Karp DP - O(2^n * n^2)

Bitmask DP. State: dp[S][v] = min cost to visit all cities in bitmask S, ending at city v.

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

For n=20: ~20M states - feasible. For n=30: impractical.

### Nearest Neighbor Heuristic - O(n^2)

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

### 2-Opt Local Search

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

### Christofides Algorithm (Concept)

For metric TSP (triangle inequality), guaranteed 1.5x optimal:
1. Find MST
2. Find minimum-weight perfect matching on odd-degree vertices
3. Combine MST + matching -> Eulerian graph
4. Find Eulerian circuit
5. Shortcut repeated vertices

## Related Problems

- **Shortest Superstring**: shortest string containing all given strings as substrings. Equivalent to TSP on overlap graph. NP-hard.

## Gotchas

- TSP cannot be decomposed into independent shortest-path subproblems
- Nearest neighbor can create very poor routes with "backtracking" patterns
- 2-opt converges to LOCAL minimum - multiple random restarts improve results
- Christofides only works with triangle inequality (metric TSP)
- Bitmask DP requires integer bitmask - Python handles arbitrary-size ints but memory is the limit

## See Also

- [[eulerian-hamiltonian-paths]] - TSP = minimum-weight Hamiltonian cycle
- [[minimum-spanning-trees]] - MST used in Christofides approximation
- [[complexity-classes]] - TSP is NP-hard
- [[dp-optimization-problems]] - bitmask DP technique
