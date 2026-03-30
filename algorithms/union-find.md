---
title: Union-Find (Disjoint Set Union)
category: data-structures
tags: [union-find, disjoint-set, dsu, connected-components, path-compression, union-by-rank]
---

# Union-Find (Disjoint Set Union)

## Key Facts

- **Union-Find** (DSU) tracks elements partitioned into disjoint sets
- Two operations: **find(x)** - which set does x belong to; **union(x, y)** - merge sets containing x and y
- With **path compression** + **union by rank**: nearly O(1) amortized per operation (inverse Ackermann)
- Applications: connected components, cycle detection in undirected graphs, Kruskal's MST, network connectivity
- More efficient than BFS/DFS for dynamic connectivity queries (adding edges incrementally)
- Related: [[graph-representations]], [[graph-bfs-dfs]]

## Patterns

### Basic Union-Find with Path Compression and Union by Rank

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # already connected
        # Union by rank
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

### Number of Connected Components

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components
```

### Detect Cycle in Undirected Graph

```python
def has_cycle(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        if uf.connected(u, v):
            return True  # edge connects already-connected vertices
        uf.union(u, v)
    return False
```

### Kruskal's Minimum Spanning Tree

```python
def kruskal(n, edges):
    """edges: list of (weight, u, v), sorted by weight"""
    edges.sort()
    uf = UnionFind(n)
    mst = []
    total_weight = 0
    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight
            if len(mst) == n - 1:
                break
    return total_weight, mst
```

```java
// Java Union-Find
class UnionFind {
    int[] parent, rank;
    int components;

    UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        components = n;
        for (int i = 0; i < n; i++) parent[i] = i;
    }

    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);
        return parent[x];
    }

    boolean union(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return false;
        if (rank[rx] < rank[ry]) { int t = rx; rx = ry; ry = t; }
        parent[ry] = rx;
        if (rank[rx] == rank[ry]) rank[rx]++;
        components--;
        return true;
    }
}
```

## Gotchas

- **Path compression is critical** - without it, find() degrades to O(n) in worst case (degenerate tree)
- **Union by rank/size prevents skewed trees** - always attach smaller tree under larger one
- **Not suitable for disconnecting** - union-find supports merging sets but NOT splitting them
- **1-indexed vs 0-indexed** - adjust parent array size accordingly
- **Return value of union()** - returning `False` when already connected is useful for cycle detection
- **Union-Find vs BFS/DFS** - UF is better for incremental connectivity; BFS/DFS is better for path-finding

## See Also

- [[graph-bfs-dfs]] - alternative for static connected components
- [[graph-representations]] - edge list format works well with Kruskal's
- [[greedy-algorithms]] - Kruskal's MST is a greedy algorithm using UF
