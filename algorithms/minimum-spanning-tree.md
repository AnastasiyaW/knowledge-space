---
title: Minimum Spanning Tree
category: algorithms
tags: [mst, kruskal, prim, spanning-tree, weighted-graph, greedy]
---

# Minimum Spanning Tree

## Key Facts

- **Spanning tree** of a connected undirected graph includes all vertices with exactly V-1 edges
- **Minimum spanning tree (MST)** has minimum total edge weight among all spanning trees
- **Kruskal's algorithm** - sort edges by weight, greedily add if no cycle (uses [[union-find]]); O(E log E)
- **Prim's algorithm** - grow MST from a start vertex using [[priority-queue-and-heap]]; O((V+E) log V) with binary heap
- Both are greedy algorithms; both produce optimal MST
- Kruskal's is better for sparse graphs; Prim's is better for dense graphs
- MST is unique if all edge weights are distinct
- Related: [[union-find]], [[priority-queue-and-heap]], [[greedy-algorithms]]

## Patterns

### Kruskal's Algorithm

```python
def kruskal(n, edges):
    """edges: list of (u, v, weight)"""
    edges.sort(key=lambda e: e[2])
    uf = UnionFind(n)
    mst = []
    total = 0
    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == n - 1:
                break
    return total, mst
# Time: O(E log E) for sorting + O(E * alpha(V)) for union-find
```

### Prim's Algorithm

```python
import heapq

def prim(graph, n):
    """graph: adjacency list {node: [(neighbor, weight), ...]}"""
    visited = set()
    heap = [(0, 0)]  # (weight, node), start from node 0
    total = 0
    mst = []

    while heap and len(visited) < n:
        weight, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        total += weight
        for v, w in graph[u]:
            if v not in visited:
                heapq.heappush(heap, (w, v))
    return total
# Time: O((V + E) log V)
```

```java
// Java Prim's
public int primMST(List<List<int[]>> graph, int n) {
    boolean[] visited = new boolean[n];
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[1] - b[1]);
    pq.offer(new int[]{0, 0}); // {node, weight}
    int total = 0, count = 0;

    while (!pq.isEmpty() && count < n) {
        int[] curr = pq.poll();
        int u = curr[0], w = curr[1];
        if (visited[u]) continue;
        visited[u] = true;
        total += w;
        count++;
        for (int[] edge : graph.get(u)) {
            if (!visited[edge[0]])
                pq.offer(new int[]{edge[0], edge[1]});
        }
    }
    return total;
}
```

## Gotchas

- **Graph must be connected** - if disconnected, MST does not exist (result is minimum spanning forest)
- **Kruskal needs union-find** - without it, cycle detection is O(V) per edge, making total O(V*E)
- **Prim with adjacency matrix** - O(V^2) without heap; useful for dense graphs
- **Negative edge weights are fine** - both algorithms handle negative weights correctly (unlike Dijkstra)
- **MST does not give shortest paths** - MST minimizes total weight; shortest path tree minimizes distance from source
- **Equal weight edges** - MST may not be unique if edge weights are not distinct

## See Also

- [[union-find]] - required for Kruskal's algorithm
- [[priority-queue-and-heap]] - required for Prim's algorithm
- [[graph-shortest-path]] - different optimization goal from MST
