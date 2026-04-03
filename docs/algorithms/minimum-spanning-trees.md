---
title: Minimum Spanning Trees
category: algorithms
tags: [algorithms, graphs, MST, prim, kruskal, union-find, greedy]
---

# Minimum Spanning Trees

A minimum spanning tree (MST) of a weighted undirected connected graph is a spanning tree with minimum total edge weight. Two classic algorithms: Prim's (grow tree greedily) and Kruskal's (merge components by cheapest edge). Both are greedy and rely on the cut property.

## Key Facts

- Spanning tree: subgraph including all |V| vertices, connected, acyclic, exactly |V|-1 edges
- MST is NOT unique if multiple edges have same weight
- **Cut property**: For any cut, the minimum-weight crossing edge is in some MST
- Finding ANY spanning tree: run BFS/DFS, keep tree edges
- Prim's: O(|E| log |V|) with binary heap, O(|V|^2) with matrix
- Kruskal's: O(|E| log |E|) = O(|E| log |V|) dominated by sorting

## Prim's vs Kruskal's

| | Prim's | Kruskal's |
|-|--------|----------|
| Data structure | Priority queue | Union-Find + sorted edges |
| Best for | Dense graphs | Sparse graphs |
| Approach | Grows single tree | Merges components |
| Dense graph | O(\|V\|^2) with matrix | O(\|E\| log \|V\|) = O(\|V\|^2 log \|V\|) |
| Sparse graph | O(\|E\| log \|V\|) | O(\|E\| log \|V\|) ~ O(\|V\| log \|V\|) |

## Patterns

### Prim's Algorithm

```python
import heapq

def prim(graph, start):
    visited = set()
    heap = [(0, start, None)]  # (weight, vertex, parent)
    mst_edges = []
    mst_cost = 0

    while heap and len(visited) < len(graph.adj_list):
        weight, vertex, parent = heapq.heappop(heap)
        if vertex in visited:
            continue
        visited.add(vertex)
        if parent is not None:
            mst_edges.append((parent, vertex, weight))
            mst_cost += weight
        for neighbor, w in graph.adj_list[vertex]:
            if neighbor not in visited:
                heapq.heappush(heap, (w, neighbor, vertex))

    return mst_edges, mst_cost
```

### Kruskal's Algorithm

```python
def kruskal(vertices, edges):
    edges.sort(key=lambda e: e[2])  # sort by weight
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False  # same component = cycle
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    mst_edges = []
    mst_cost = 0
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            mst_cost += w
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges, mst_cost
```

### Min Cost to Connect Points

Given n points, connect all with minimum total distance. This is MST on complete graph.

- Build all O(n^2) edges with distances
- For complete (dense) graphs, Prim's with O(n^2) matrix is simpler

## Gotchas

- MST is for UNDIRECTED graphs only. For directed graphs, use minimum spanning arborescence (Edmonds' algorithm)
- MST != shortest path tree. Dijkstra's SPT minimizes individual paths, MST minimizes total weight
- Prim's can't detect disconnected graphs (only finds MST of starting component)
- Kruskal's can detect disconnected graph: if MST has fewer than |V|-1 edges, graph is disconnected
- Early termination in Kruskal's when |V|-1 edges found saves unnecessary iterations

## See Also

- [[union-find]] - disjoint set data structure used by Kruskal's
- [[shortest-path-algorithms]] - MST vs shortest path tree
- [[graph-representation]] - Prim's complexity depends on representation
- [[graph-traversal-bfs-dfs]] - BFS/DFS finds any spanning tree
