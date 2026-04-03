---
title: Shortest Path Algorithms
category: algorithms
tags: [algorithms, graphs, dijkstra, bellman-ford, floyd-warshall, shortest-path, weighted-graph]
---

# Shortest Path Algorithms

Algorithms for finding shortest paths in weighted graphs: BFS (unweighted), Dijkstra (non-negative weights), Bellman-Ford (handles negative edges), Floyd-Warshall (all-pairs), DAG relaxation, and Johnson's algorithm.

## Algorithm Selection

| Condition | Algorithm | Complexity |
|-----------|----------|-----------|
| Unweighted | BFS | O(\|V\| + \|E\|) |
| Non-negative weights, single source | Dijkstra | O((\|V\|+\|E\|) log \|V\|) |
| Negative edges, single source | Bellman-Ford | O(\|V\|\|E\|) |
| DAG, any weights, single source | Topological DP | O(\|V\| + \|E\|) |
| All-pairs, no negative edges | Dijkstra from each vertex | O(\|V\|(\|V\|+\|E\|) log \|V\|) |
| All-pairs, negative edges, dense | Floyd-Warshall | O(\|V\|^3) |
| All-pairs, negative edges, sparse | Johnson's | O(\|V\|^2 log \|V\| + \|V\|\|E\|) |
| Dense graph, no neg edges | Dijkstra with matrix | O(\|V\|^2) |

## Key Facts

- **Negative-weight cycle**: If reachable from source, no well-defined shortest path exists
- Dijkstra FAILS on negative edges - greedy assumption breaks
- Floyd-Warshall detects negative cycles: dist[i][i] < 0 after running
- DAG shortest path is the fastest single-source algorithm when graph is acyclic

## Patterns

### BFS - Unweighted: O(|V| + |E|)

```python
from collections import deque

def bfs_shortest(graph, src):
    dist = {src: 0}
    queue = deque([src])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.adj_list[vertex]:
            if neighbor not in dist:
                dist[neighbor] = dist[vertex] + 1
                queue.append(neighbor)
    return dist
```

### Dijkstra - Non-Negative Weights

```python
import heapq

def dijkstra(graph, src):
    dist = {v: float('inf') for v in graph.adj_list}
    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, vertex = heapq.heappop(heap)
        if d > dist[vertex]:
            continue  # stale entry
        for neighbor, weight in graph.adj_list[vertex]:
            new_dist = dist[vertex] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist
```

**Why greedy works:** When vertex u is popped, dist[u] is optimal. Any other path would go through a vertex with larger distance (all weights >= 0).

**Complexity variants:**
- Binary heap: O((|V| + |E|) log |V|)
- Fibonacci heap: O(|E| + |V| log |V|)
- Adjacency matrix, no heap: O(|V|^2) - better for dense graphs

### Bellman-Ford - Handles Negative Edges

```python
def bellman_ford(graph, src):
    dist = {v: float('inf') for v in graph.vertices}
    dist[src] = 0

    for _ in range(len(graph.vertices) - 1):
        for u, v, w in graph.edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Negative cycle detection
    for u, v, w in graph.edges:
        if dist[u] + w < dist[v]:
            return None  # negative cycle
    return dist
```

**Why |V|-1 iterations:** Shortest path has at most |V|-1 edges (no repeated vertices). Iteration k gives shortest path using at most k edges.

### Floyd-Warshall - All-Pairs: O(|V|^3)

```python
def floyd_warshall(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):       # intermediate vertex
        for i in range(n):   # source
            for j in range(n):  # destination
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

### DAG Shortest Path - O(|V| + |E|)

Process vertices in topological order. Handles negative weights.

```python
def dag_shortest_path(graph, src):
    order = topological_sort(graph)
    dist = {v: float('inf') for v in graph.adj_list}
    dist[src] = 0

    for vertex in order:
        if dist[vertex] != float('inf'):
            for neighbor, weight in graph.adj_list[vertex]:
                if dist[vertex] + weight < dist[neighbor]:
                    dist[neighbor] = dist[vertex] + weight
    return dist
```

### Johnson's Algorithm - All-Pairs with Negative Edges

1. Add new vertex s with 0-weight edges to all vertices
2. Run Bellman-Ford from s to get potential function h[v]
3. Reweight: w'(u,v) = w(u,v) + h[u] - h[v] >= 0
4. Run Dijkstra from every vertex on reweighted graph
5. Adjust distances back: dist(u,v) = dist'(u,v) - h[u] + h[v]

Better than Floyd-Warshall for sparse graphs.

## Gotchas

- Dijkstra's `if d > dist[vertex]: continue` is critical for correctness with lazy deletion (stale heap entries)
- Bellman-Ford negative cycle detection: if ANY edge still relaxes after |V|-1 rounds, a cycle exists
- Floyd-Warshall loop order must be k (intermediate) outermost, then i, then j
- DAG shortest path requires topological sort first - fails on cyclic graphs
- For single-pair queries, all these algorithms still compute single-source (no known faster general method)

## See Also

- [[graph-traversal-bfs-dfs]] - BFS for unweighted shortest paths
- [[topological-sort]] - required for DAG shortest path
- [[graph-representation]] - complexity depends on representation
- [[minimum-spanning-trees]] - related graph optimization (MST != shortest path tree)
