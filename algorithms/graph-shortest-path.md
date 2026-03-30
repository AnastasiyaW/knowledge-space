---
title: Graph Shortest Path Algorithms
category: algorithms
tags: [dijkstra, bellman-ford, shortest-path, weighted-graph, single-source]
---

# Graph Shortest Path Algorithms

## Key Facts

| Algorithm | Time | Space | Negative Weights | Use Case |
|-----------|------|-------|-----------------|----------|
| BFS | O(V + E) | O(V) | No | Unweighted graphs |
| Dijkstra | O((V+E) log V) | O(V) | No | Non-negative weighted |
| Bellman-Ford | O(V * E) | O(V) | Yes | Negative weights, cycle detection |
| Floyd-Warshall | O(V^3) | O(V^2) | Yes | All-pairs shortest path |

- **Dijkstra** - greedy algorithm using [[priority-queue-and-heap]]; processes closest unvisited vertex first
- **Bellman-Ford** - relaxes all edges V-1 times; detects negative cycles on Vth iteration
- **Floyd-Warshall** - dynamic programming for all-pairs; uses intermediate vertices
- Dijkstra fails with negative edge weights (greedy assumption violated)
- Related: [[graph-bfs-dfs]], [[priority-queue-and-heap]], [[dynamic-programming]]

## Patterns

### Dijkstra's Algorithm

```python
import heapq

def dijkstra(graph, start):
    """graph: adjacency list {node: [(neighbor, weight), ...]}"""
    dist = {start: 0}
    heap = [(0, start)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')):
            continue  # skip stale entries
        for v, weight in graph[u]:
            new_dist = d + weight
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
    return dist

# Reconstruct path
def dijkstra_with_path(graph, start, end):
    dist = {start: 0}
    parent = {start: None}
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if u == end:
            break
        if d > dist.get(u, float('inf')):
            continue
        for v, weight in graph[u]:
            new_dist = d + weight
            if new_dist < dist.get(v, float('inf')):
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(heap, (new_dist, v))

    # Reconstruct path
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent.get(node)
    return path[::-1], dist.get(end, float('inf'))
```

### Bellman-Ford

```python
def bellman_ford(n, edges, start):
    """edges: list of (u, v, weight)"""
    dist = [float('inf')] * n
    dist[start] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            raise ValueError("Negative cycle detected")

    return dist
```

### Floyd-Warshall (All-Pairs)

```python
def floyd_warshall(n, edges):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

```java
// Java Dijkstra with PriorityQueue
public int[] dijkstra(List<List<int[]>> graph, int start) {
    int n = graph.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;

    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{start, 0});

    while (!pq.isEmpty()) {
        int[] curr = pq.poll();
        int u = curr[0], d = curr[1];
        if (d > dist[u]) continue;
        for (int[] edge : graph.get(u)) {
            int v = edge[0], w = edge[1];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.offer(new int[]{v, dist[v]});
            }
        }
    }
    return dist;
}
```

## Gotchas

- **Dijkstra with negative weights** - greedy assumption fails; node can be reached cheaper through negative edge later
- **Stale heap entries** - since Python's heapq does not support decrease-key, skip entries where `d > dist[u]`
- **Bellman-Ford runs V-1 times** - longest shortest path has at most V-1 edges
- **Floyd-Warshall** - loop order must be k (intermediate) as outer loop, not i or j
- **Dense vs sparse** - Dijkstra with binary heap is O((V+E) log V); with Fibonacci heap is O(E + V log V) but rarely used in practice
- **0-indexed vs 1-indexed** - verify vertex numbering when translating problem input to graph

## See Also

- [[graph-bfs-dfs]] - BFS for unweighted shortest path
- [[priority-queue-and-heap]] - core data structure for Dijkstra
- [[dynamic-programming]] - Floyd-Warshall uses DP approach
