---
title: Graph Representation
category: data-structures
tags: [algorithms, graphs, adjacency-list, adjacency-matrix, data-structures]
---

# Graph Representation

Graphs can be represented as edge lists, adjacency lists, or adjacency matrices. The choice depends on graph density and which operations matter most. Adjacency lists are the default for sparse graphs; matrices for dense graphs needing O(1) edge checks.

## Key Facts

- **Edge list**: Store (src, dest) tuples. Finding neighbors is O(|E|) - rarely used alone
- **Adjacency list**: Map each vertex to its neighbors. Space O(|V| + |E|). Most common
- **Adjacency matrix**: n x n matrix. Space O(|V|^2). O(1) edge check but O(|V|) to list neighbors
- Graph with n vertices has at most n(n-1)/2 edges (undirected) or n(n-1) (directed)

## Core Terminology

| Term | Definition |
|------|-----------|
| Order | Number of vertices \|V\| |
| Size | Number of edges \|E\| |
| Degree | Number of edges at a vertex (in-degree + out-degree for directed) |
| Sparse | \|E\| << \|V\|^2 |
| Dense | \|E\| close to \|V\|^2 |
| DAG | Directed Acyclic Graph |
| Complete graph | Every pair connected. Size = \|V\|(\|V\|-1)/2 |
| Bipartite | Vertices split into two sets, edges only between sets |

## Graph Types

| Type | Definition |
|------|-----------|
| Simple graph | No self-loops, no multi-edges |
| Multigraph | Multiple edges between same pair allowed |
| Complete graph | Every pair connected |
| Bipartite | Two-set partition, edges between sets only |
| Regular graph | All vertices have same degree |

## Operation Complexity

| Operation | Adjacency List | Adjacency Matrix |
|-----------|---------------|-----------------|
| Space | O(\|V\| + \|E\|) | O(\|V\|^2) |
| Add vertex | O(1) | O(\|V\|^2) rebuild |
| Remove vertex | O(\|V\| + \|E\|) | O(\|V\|^2) |
| Add edge | O(1) | O(1) |
| Remove edge | O(degree(u)) | O(1) |
| Check edge | O(degree(u)) | O(1) |
| Get neighbors | O(degree(u)) | O(\|V\|) |

## Patterns

### Adjacency List Implementation

```python
class Graph:
    def __init__(self):
        self.adj_list = {}  # vertex -> list of neighbors

    def add_vertex(self, u):
        if u not in self.adj_list:
            self.adj_list[u] = []

    def add_edge(self, u, v):  # directed
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].append(v)

    def add_edge_undirected(self, u, v):
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)

    def add_edge_weighted(self, u, v, w):  # directed weighted
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].append((v, w))

    def remove_vertex(self, u):
        if u in self.adj_list:
            del self.adj_list[u]
            for v in self.adj_list:
                if u in self.adj_list[v]:
                    self.adj_list[v].remove(u)

    def check_edge(self, u, v):
        return u in self.adj_list and v in self.adj_list[u]

    def build(self, vertices, edges):
        for u in vertices:
            self.add_vertex(u)
        for u, v in edges:
            self.add_edge(u, v)
```

Use set instead of list for O(1) edge existence check at the cost of extra memory.

### Adjacency Matrix Implementation

```python
class GraphMatrix:
    def __init__(self):
        self.adj_mat = []

    def add_vertex(self):
        for row in self.adj_mat:
            row.append(0)
        n = len(self.adj_mat) + 1
        self.adj_mat.append([0] * n)

    def add_edge(self, u, v):
        self.adj_mat[u][v] = 1  # undirected: also self.adj_mat[v][u] = 1

    def edge_exists(self, u, v):
        return self.adj_mat[u][v] == 1

    def get_neighbors(self, u):
        return [v for v in range(len(self.adj_mat[u])) if self.adj_mat[u][v] == 1]
```

## Connectivity

| Concept | Definition |
|---------|-----------|
| Walk | Sequence of adjacent vertices, repeats allowed |
| Trail | Walk with no repeated edges |
| Path | Walk with no repeated vertices |
| Cycle | Closed path |
| Connected | Every pair reachable (undirected) |
| Strongly connected | Directed path between every ordered pair |
| Weakly connected | Connected when ignoring edge directions |

## Gotchas

- Choose adjacency list for sparse graphs (most real-world graphs)
- Choose adjacency matrix for dense graphs or when O(1) edge check is critical
- For non-integer vertex labels, use hash map to map labels to indices
- Removing a vertex from adjacency list requires scanning all lists: O(|V| + |E|)
- Matrix delete vertex: swap with last row/column then pop to avoid rebuild

## See Also

- [[graph-traversal-bfs-dfs]] - DFS and BFS on these representations
- [[shortest-path-algorithms]] - different algorithms suit different representations
- [[minimum-spanning-trees]] - Prim's with matrix O(|V|^2) vs with heap O(|E| log |V|)
