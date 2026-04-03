---
title: Network Flow
category: algorithms
tags: [algorithms, graphs, max-flow, min-cut, ford-fulkerson, bipartite-matching]
---

# Network Flow

Network flow algorithms find the maximum feasible flow from source to sink in a directed weighted graph. The max-flow min-cut theorem connects maximum flow to the minimum capacity cut. Key algorithms: Ford-Fulkerson, Edmonds-Karp, and Dinic's.

## Key Facts

- **Max-Flow Min-Cut Theorem**: Maximum flow = minimum cut capacity
- **Flow constraints**: (1) flow <= capacity on each edge, (2) flow conservation at each non-source/sink vertex
- **Residual graph**: forward edges with remaining capacity + backward edges for flow cancellation
- **Applications**: network bandwidth, bipartite matching, project selection, image segmentation

## Algorithm Comparison

| Algorithm | Complexity | Best for |
|-----------|-----------|---------|
| Ford-Fulkerson (DFS) | O(\|E\| * max_flow) | Integer capacities, small flow |
| Edmonds-Karp (BFS) | O(\|V\|\|E\|^2) | General use, simple implementation |
| Dinic's | O(\|V\|^2\|E\|) | Dense graphs |
| Dinic's (unit capacity) | O(\|E\|*sqrt(\|V\|)) | Bipartite matching |
| Push-relabel | O(\|V\|^2*sqrt(\|E\|)) | Dense graphs in practice |

## Patterns

### Residual Graph Concept

```
Original: u --(cap=8, flow=6)--> v
Residual: u --2--> v   (can send 2 more forward)
          v --6--> u   (can cancel 6 of current flow)
```

### Edmonds-Karp (BFS-based Ford-Fulkerson)

```python
from collections import deque

def edmonds_karp(capacity, source, sink):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]

    def bfs():
        visited = [-1] * n
        visited[source] = source
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in range(n):
                if visited[v] == -1 and capacity[u][v] - flow[u][v] > 0:
                    visited[v] = u
                    if v == sink:
                        return visited
                    queue.append(v)
        return None

    max_flow = 0
    while True:
        parent = bfs()
        if parent is None:
            break
        # Find bottleneck
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
            v = u
        # Update flow
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
        max_flow += path_flow

    return max_flow
```

### Dinic's Algorithm

Uses blocking flows in layered graph. BFS builds level graph, DFS finds blocking flows.

```python
from collections import deque

def dinic(graph, source, sink):
    n = len(graph)

    def bfs_level(level):
        level[:] = [-1] * n
        level[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v, cap, rev in graph[u]:
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level[sink] >= 0

    def dfs_blocking(u, pushed, level, iter_):
        if u == sink:
            return pushed
        while iter_[u] < len(graph[u]):
            v, cap, rev = graph[u][iter_[u]]
            if cap > 0 and level[v] == level[u] + 1:
                d = dfs_blocking(v, min(pushed, cap), level, iter_)
                if d > 0:
                    graph[u][iter_[u]][1] -= d
                    graph[v][rev][1] += d
                    return d
            iter_[u] += 1
        return 0

    level = [0] * n
    max_flow = 0
    while bfs_level(level):
        iter_ = [0] * n
        while True:
            f = dfs_blocking(source, float('inf'), level, iter_)
            if f == 0:
                break
            max_flow += f
    return max_flow
```

### Bipartite Matching via Max Flow

```
Network construction:
- Source s --> each left vertex (capacity 1)
- Left vertex --> connected right vertices (capacity 1)
- Right vertex --> sink t (capacity 1)

max_flow = maximum matching size
```

```python
def max_bipartite_matching(left_nodes, right_nodes, edges):
    n = 2 + len(left_nodes) + len(right_nodes)
    source, sink = 0, n - 1
    capacity = [[0] * n for _ in range(n)]

    for i, _ in enumerate(left_nodes):
        capacity[source][i + 1] = 1
    left_idx = {v: i + 1 for i, v in enumerate(left_nodes)}
    right_idx = {v: i + len(left_nodes) + 1 for i, v in enumerate(right_nodes)}
    for l, r in edges:
        capacity[left_idx[l]][right_idx[r]] = 1
    for i, _ in enumerate(right_nodes):
        capacity[i + len(left_nodes) + 1][sink] = 1

    return edmonds_karp(capacity, source, sink)
```

Hopcroft-Karp solves bipartite matching directly in O(sqrt(|V|) * |E|).

## Gotchas

- Ford-Fulkerson may not terminate with irrational capacities - use Edmonds-Karp (BFS) for guaranteed termination
- Backward edges in residual graph are essential for correctness - they allow "undoing" flow
- Bipartite matching reduction requires unit capacities on all edges
- Flow conservation does NOT apply to source and sink vertices
- Min-cut can be found after max-flow: vertices reachable from source in residual graph = S, rest = T

## See Also

- [[graph-traversal-bfs-dfs]] - BFS used in Edmonds-Karp and Dinic's
- [[graph-coloring]] - bipartite checking related to matching
- [[shortest-path-algorithms]] - flow networks share graph infrastructure
