---
title: Topological Sort
category: algorithms
tags: [algorithms, graphs, topological-sort, DAG, scheduling, kahn]
---

# Topological Sort

A topological ordering of a DAG (Directed Acyclic Graph) is a linear ordering of vertices such that for every edge u -> v, u comes before v. Only possible on DAGs - a cycle creates a contradiction. Two algorithms: DFS-based (post-order reversal) and Kahn's (BFS with in-degree tracking).

## Key Facts

- Only works on DAGs - cycle means no valid ordering exists
- Not unique - multiple valid orderings may exist
- Both algorithms: O(|V| + |E|) time and space
- Applications: course prerequisites, task scheduling, build systems, database table loading order, critical path

## Algorithm Comparison

| | DFS-based | Kahn's (BFS) |
|-|-----------|---------------------|
| Order detection | Post-order DFS reversed | By in-degree |
| Cycle detection | Track "in stack" (gray nodes) | Output size < \|V\| |
| Multiple valid orderings | Any DFS order | Controllable via priority queue |
| Implementation | Simpler recursion | Explicit in-degree tracking |

## Patterns

### DFS-based Topological Sort

```python
def topological_sort_dfs(graph):
    visited = set()
    order = []

    def dfs(vertex):
        visited.add(vertex)
        for neighbor in graph.adj_list.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor)
        order.append(vertex)  # add AFTER all successors processed

    for vertex in graph.adj_list:
        if vertex not in visited:
            dfs(vertex)

    return order[::-1]  # reverse post-order
```

Why it works: when we append vertex u, all vertices reachable from u are already appended. After reversal, u precedes everything it points to.

### Kahn's Algorithm (BFS-based)

```python
from collections import deque

def topological_sort_kahn(graph):
    in_degree = {v: 0 for v in graph.adj_list}
    for u in graph.adj_list:
        for v in graph.adj_list[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    queue = deque([v for v in in_degree if in_degree[v] == 0])
    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor in graph.adj_list.get(vertex, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) < len(graph.adj_list):
        return None  # cycle detected
    return order
```

### Critical Path (Minimum Time for All Tasks)

Given task graph with durations, find minimum completion time using topological order + DP.

```python
def critical_path(graph):
    order = topological_sort_kahn(graph)
    earliest = {v: 0 for v in graph.adj_list}
    for u in order:
        for v, weight in graph.adj_list[u]:
            earliest[v] = max(earliest[v], earliest[u] + weight)
    return max(earliest.values())  # minimum total time
```

The critical path = longest path through the DAG = minimum completion time.

### Shortest Path in DAG

Process in topological order, relax edges. O(|V| + |E|), handles negative weights.

```python
def dag_shortest(graph, src):
    order = topological_sort_kahn(graph)
    dist = {v: float('inf') for v in graph.adj_list}
    dist[src] = 0
    for vertex in order:
        if dist[vertex] != float('inf'):
            for neighbor, weight in graph.adj_list[vertex]:
                if dist[vertex] + weight < dist[neighbor]:
                    dist[neighbor] = dist[vertex] + weight
    return dist
```

## Gotchas

- DFS-based requires post-order REVERSAL - forgetting to reverse gives wrong order
- Kahn's cycle detection: if output has fewer vertices than graph, a cycle exists
- Multiple valid orderings are possible - don't assume one specific ordering
- Not applicable to undirected graphs or graphs with cycles
- Course scheduling uses topological sort but may also need constraint on parallel courses (separate problem)

## See Also

- [[graph-traversal-bfs-dfs]] - DFS and BFS fundamentals used here
- [[shortest-path-algorithms]] - DAG shortest path as application
- [[graph-representation]] - adjacency list for topological sort
