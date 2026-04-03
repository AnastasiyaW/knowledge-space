---
title: Eulerian and Hamiltonian Paths
category: algorithms
tags: [algorithms, graphs, eulerian, hamiltonian, hierholzer, backtracking]
---

# Eulerian and Hamiltonian Paths

Eulerian paths visit every EDGE exactly once; Hamiltonian paths visit every VERTEX exactly once. Eulerian problems are polynomial (simple degree conditions + Hierholzer's O(|E|) algorithm). Hamiltonian problems are NP-complete.

## Key Comparison

| | Eulerian | Hamiltonian |
|-|----------|-------------|
| What to traverse | Every edge exactly once | Every vertex exactly once |
| Complexity to find | O(\|E\|) - polynomial | NP-complete |
| Existence conditions | Simple degree conditions | No simple characterization |
| Algorithm | Hierholzer's | Backtracking O(n!), DP O(2^n * n^2) |

## Eulerian Trail/Circuit Conditions

### Undirected Graph

| Condition | Result |
|-----------|--------|
| All non-zero-degree vertices connected AND all even degree | Eulerian **circuit** |
| All non-zero-degree vertices connected AND exactly 2 odd-degree vertices | Eulerian **trail** (start/end at odd vertices) |
| More than 2 odd-degree vertices | No Eulerian trail |

### Directed Graph

| Condition | Result |
|-----------|--------|
| Strongly connected AND in-degree == out-degree for all | Eulerian **circuit** |
| Weakly connected AND exactly one vertex out-in=1 (start), one in-out=1 (end), rest balanced | Eulerian **trail** |

## Patterns

### Check Eulerian Circuit (Undirected)

```python
def has_eulerian_circuit(graph):
    non_isolated = [v for v in graph.adj_list if graph.adj_list[v]]
    if not non_isolated:
        return True
    # Check connectivity via DFS
    visited = set()
    stack = [non_isolated[0]]
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            for u in graph.adj_list[v]:
                stack.append(u)
    if any(v not in visited for v in non_isolated):
        return False
    # Check all degrees even
    return all(len(graph.adj_list[v]) % 2 == 0 for v in graph.adj_list)
```

### Hierholzer's Algorithm - O(|E|)

```python
def hierholzer(graph):
    start = next(v for v in graph.adj_list if graph.adj_list[v])
    adj = {v: list(neighbors) for v, neighbors in graph.adj_list.items()}
    stack = [start]
    circuit = []

    while stack:
        v = stack[-1]
        if adj[v]:
            u = adj[v].pop()
            adj[u].remove(v)  # remove reverse edge for undirected
            stack.append(u)
        else:
            circuit.append(stack.pop())

    return circuit[::-1]
```

### Reconstruct Itinerary (Directed Eulerian Path)

Given airline tickets, reconstruct lexicographic itinerary using all tickets exactly once.

```python
from collections import defaultdict

def find_itinerary(tickets):
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):  # reverse sort for efficient pop
        graph[src].append(dst)

    result = []
    stack = ["JFK"]
    while stack:
        while graph[stack[-1]]:
            stack.append(graph[stack[-1]].pop())
        result.append(stack.pop())

    return result[::-1]
```

### Hamiltonian Path - Backtracking O(n!)

```python
def hamiltonian_path(graph, path, visited):
    if len(path) == len(graph.adj_list):
        return path

    current = path[-1]
    for neighbor in graph.adj_list[current]:
        if neighbor not in visited:
            visited.add(neighbor)
            path.append(neighbor)
            result = hamiltonian_path(graph, path, visited)
            if result:
                return result
            path.pop()
            visited.remove(neighbor)
    return None

def find_hamiltonian(graph):
    for start in graph.adj_list:
        result = hamiltonian_path(graph, [start], {start})
        if result:
            return result
    return None
```

### Held-Karp DP for Hamiltonian - O(2^n * n^2)

Better than O(n!) for exact solution. See [[traveling-salesman-problem]] for bitmask DP implementation.

## Key Facts

- **Euler (1736)**: Seven Bridges of Konigsberg - first graph theory result
- **Ore's theorem**: If deg(u) + deg(v) >= n for all non-adjacent pairs, Hamiltonian cycle exists (sufficient, not necessary)
- Hierholzer's works by greedily following edges until stuck, then backtracking to find extensions
- Historical origin of graph theory: can you cross all 7 bridges exactly once?

## Gotchas

- Eulerian = edges, Hamiltonian = vertices - easy to confuse
- Hierholzer's for undirected graphs must remove edges in BOTH directions
- For Hamiltonian, no simple condition exists (unlike Eulerian) - must try or use DP
- Hamiltonian path vs cycle: path doesn't return to start, cycle does
- Euler trail with 2 odd-degree vertices: MUST start at one and end at the other

## See Also

- [[traveling-salesman-problem]] - Hamiltonian cycle with minimum weight
- [[graph-traversal-bfs-dfs]] - DFS used in Hierholzer's
- [[complexity-classes]] - Hamiltonian path is NP-complete
