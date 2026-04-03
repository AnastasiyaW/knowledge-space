---
title: Union-Find (Disjoint Set Union)
category: data-structures
tags: [algorithms, data-structures, union-find, disjoint-set, connected-components]
---

# Union-Find (Disjoint Set Union)

Union-Find maintains a collection of disjoint sets with near-constant-time operations for merging sets and finding which set an element belongs to. Essential for Kruskal's MST, connected components, and cycle detection.

## Key Facts

- **find(x)**: Find root/representative of set containing x
- **union(x, y)**: Merge sets containing x and y
- With path compression + union by rank: O(alpha(n)) amortized per operation
- alpha(n) = inverse Ackermann function, effectively O(1) for all practical n (alpha(n) <= 4 for n < 10^80)
- Space: O(n)

## Patterns

### Implementation

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already same set
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

### Iterative Find with Path Halving

```python
def find(self, x):
    while self.parent[x] != x:
        self.parent[x] = self.parent[self.parent[x]]  # path halving
        x = self.parent[x]
    return x
```

Path halving (iterative) is simpler and has same asymptotic performance as full path compression (recursive).

### Cycle Detection in Undirected Graph

```python
def has_cycle(vertices, edges):
    uf = UnionFind(len(vertices))
    for u, v in edges:
        if not uf.union(u, v):
            return True  # u and v already connected = cycle
    return False
```

### Count Connected Components

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return len(set(uf.find(i) for i in range(n)))
```

## Optimization Techniques

| Technique | Effect |
|-----------|--------|
| Path compression | Flattens tree during find - all nodes point to root |
| Union by rank | Attaches shorter tree under taller - limits height to O(log n) |
| Both combined | Amortized O(alpha(n)) per operation |
| Neither | O(n) worst case per operation (degenerate chain) |

## Gotchas

- Without path compression, find can be O(n) on a degenerate chain
- Union by rank alone gives O(log n) per find
- `union` returns False when elements are already in same set - useful for cycle detection
- The rank is an upper bound on height, not exact height (path compression doesn't update rank)
- For sparse graphs, Union-Find is more efficient than DFS/BFS for connectivity queries on dynamic graphs (edges added over time)

## See Also

- [[minimum-spanning-trees]] - Kruskal's algorithm uses Union-Find
- [[graph-representation]] - Union-Find as alternative for dynamic connectivity
- [[graph-traversal-bfs-dfs]] - alternative for static connectivity queries
