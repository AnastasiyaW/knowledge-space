---
title: Graph Representations
category: data-structures
tags: [graph, adjacency-list, adjacency-matrix, directed, undirected, weighted]
---

# Graph Representations

## Key Facts

- **Graph** G = (V, E) consists of vertices (nodes) V and edges E connecting them
- **Directed graph** (digraph) - edges have direction (u -> v)
- **Undirected graph** - edges are bidirectional (u -- v)
- **Weighted graph** - edges have associated costs/weights
- **Adjacency list** - each vertex stores list of neighbors; Space O(V + E); preferred for sparse graphs
- **Adjacency matrix** - V x V matrix; `matrix[i][j]` = edge weight or 1/0; Space O(V^2); preferred for dense graphs
- **Degree** - number of edges incident to a vertex; in-degree / out-degree for directed graphs
- **Sparse graph**: E ~ O(V); **Dense graph**: E ~ O(V^2)
- Related: [[graph-bfs-dfs]], [[graph-shortest-path]]

## Patterns

### Adjacency List (Most Common)

```python
from collections import defaultdict

# Unweighted undirected graph
graph = defaultdict(list)
edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # remove for directed

# Weighted graph
weighted_graph = defaultdict(list)
weighted_edges = [(0, 1, 5), (0, 2, 3), (1, 3, 2)]
for u, v, w in weighted_edges:
    weighted_graph[u].append((v, w))
    weighted_graph[v].append((u, w))
```

### Adjacency Matrix

```python
# Unweighted graph with n vertices
n = 4
matrix = [[0] * n for _ in range(n)]
edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
for u, v in edges:
    matrix[u][v] = 1
    matrix[v][u] = 1  # remove for directed

# Check if edge exists: O(1)
has_edge = matrix[0][1] == 1
```

### Edge List

```python
# Simple list of edges - useful for Kruskal's, Bellman-Ford
edges = [(0, 1, 5), (0, 2, 3), (1, 3, 2)]  # (from, to, weight)
edges.sort(key=lambda e: e[2])  # sort by weight for Kruskal's
```

### Build Graph from Input

```python
# Common pattern: n nodes, m edges
def build_graph(n, edges, directed=False):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph

# With weights
def build_weighted_graph(n, edges, directed=False):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        if not directed:
            graph[v].append((u, w))
    return graph
```

```java
// Java adjacency list
import java.util.*;

List<List<Integer>> graph = new ArrayList<>();
for (int i = 0; i < n; i++) {
    graph.add(new ArrayList<>());
}
// Add edge
graph.get(u).add(v);
graph.get(v).add(u); // undirected

// Weighted: List<List<int[]>> where int[] = {neighbor, weight}
```

### Comparison Table

| Operation | Adjacency List | Adjacency Matrix |
|-----------|---------------|-----------------|
| Space | O(V + E) | O(V^2) |
| Add edge | O(1) | O(1) |
| Remove edge | O(E) | O(1) |
| Check edge | O(degree) | O(1) |
| Get neighbors | O(degree) | O(V) |
| Best for | Sparse graphs | Dense graphs |

## Gotchas

- **Self-loops** - edge from vertex to itself; may need explicit handling
- **Parallel edges** - multiple edges between same pair; adjacency list naturally supports, matrix does not
- **0-indexed vs 1-indexed** - problem input often uses 1-indexed vertices; adjust when building graph
- **Directed vs undirected** - forgetting to add both directions for undirected graphs is a common bug
- **defaultdict vs fixed-size list** - `defaultdict(list)` handles unknown vertex count; fixed-size list is faster for known n
- **Matrix space** - O(V^2) is prohibitive for large graphs (10^5+ vertices); always use adjacency list

## See Also

- [[graph-bfs-dfs]] - traversal algorithms on graphs
- [[graph-shortest-path]] - Dijkstra, Bellman-Ford
- [[topological-sort]] - ordering for DAGs
