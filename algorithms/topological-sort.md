---
title: Topological Sort
category: algorithms
tags: [topological-sort, dag, directed-acyclic-graph, kahn, dependency-resolution]
---

# Topological Sort

## Key Facts

- **Topological sort** - linear ordering of vertices in a [[topological-sort]] (DAG) such that for every edge (u, v), u comes before v
- Only possible on DAGs - if graph has a cycle, topological sort is impossible
- Multiple valid orderings may exist
- Applications: build systems (Makefile), task scheduling, course prerequisites, dependency resolution
- Two approaches: **DFS-based** (reverse post-order) and **Kahn's algorithm** (BFS with in-degree)
- Time: O(V + E), Space: O(V)
- Related: [[graph-bfs-dfs]], [[graph-representations]]

## Patterns

### Kahn's Algorithm (BFS / In-Degree)

```python
from collections import deque, defaultdict

def topological_sort_kahn(n, edges):
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != n:
        return []  # cycle detected - not a DAG
    return order
```

### DFS-Based (Reverse Post-Order)

```python
def topological_sort_dfs(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    visited = set()
    stack = []
    has_cycle = [False]

    def dfs(node, in_progress):
        if node in in_progress:
            has_cycle[0] = True
            return
        if node in visited:
            return
        in_progress.add(node)
        for neighbor in graph[node]:
            dfs(neighbor, in_progress)
        in_progress.remove(node)
        visited.add(node)
        stack.append(node)

    for i in range(n):
        if i not in visited:
            dfs(i, set())

    if has_cycle[0]:
        return []
    return stack[::-1]
```

### Course Schedule (Classic Problem)

```python
def can_finish(num_courses, prerequisites):
    """Return True if all courses can be finished (no cycle)."""
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return count == num_courses
```

```java
// Java Kahn's algorithm
public int[] topologicalSort(int n, int[][] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    int[] inDegree = new int[n];
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (int[] e : edges) {
        graph.get(e[0]).add(e[1]);
        inDegree[e[1]]++;
    }
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < n; i++)
        if (inDegree[i] == 0) queue.offer(i);
    int[] order = new int[n];
    int idx = 0;
    while (!queue.isEmpty()) {
        int node = queue.poll();
        order[idx++] = node;
        for (int nb : graph.get(node))
            if (--inDegree[nb] == 0) queue.offer(nb);
    }
    return idx == n ? order : new int[0];
}
```

## Gotchas

- **Cycle detection** - if topological sort produces fewer than V vertices, the graph has a cycle
- **Not unique** - DAGs with multiple sources can produce different valid orderings
- **Direction matters** - edges represent "must come before" relationship; reversing direction changes meaning
- **DFS coloring for cycles** - use three states (unvisited/in-progress/visited) to detect back edges in directed graphs
- **Kahn's vs DFS** - Kahn's naturally detects cycles (count != V); DFS requires explicit cycle tracking

## See Also

- [[graph-bfs-dfs]] - underlying traversal strategies
- [[graph-representations]] - adjacency list for DAGs
- [[dynamic-programming]] - DP on DAGs often follows topological order
