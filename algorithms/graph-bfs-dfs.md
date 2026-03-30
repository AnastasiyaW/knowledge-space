---
title: Graph BFS and DFS
category: algorithms
tags: [bfs, dfs, graph-traversal, breadth-first, depth-first, connected-components, flood-fill]
---

# Graph BFS and DFS

## Key Facts

- **BFS (Breadth-First Search)** - explores level by level using a queue; finds shortest path in unweighted graphs
- **DFS (Depth-First Search)** - explores as deep as possible using stack/recursion; useful for cycle detection, topological sort
- Both visit every vertex and edge once: Time O(V + E), Space O(V)
- BFS guarantees shortest path (fewest edges) in unweighted graphs
- DFS can be implemented recursively (implicit stack) or iteratively (explicit stack)
- Applications: connected components, cycle detection, [[topological-sort]], flood fill, bipartite check
- Related: [[graph-representations]], [[graph-shortest-path]]

## Patterns

### BFS - Level-Order Traversal

```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
```

### BFS - Shortest Path (Unweighted)

```python
from collections import deque

def shortest_path(graph, start, end):
    visited = set([start])
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return []  # no path

# Alternative: track parent to reconstruct path
def shortest_path_distance(graph, start, end):
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1
```

### DFS - Recursive

```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

### DFS - Iterative

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    return order
```

### Connected Components

```python
def count_components(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    components = 0
    for i in range(n):
        if i not in visited:
            components += 1
            # BFS or DFS from i
            stack = [i]
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                for neighbor in graph[node]:
                    stack.append(neighbor)
    return components
```

### Cycle Detection (Undirected)

```python
def has_cycle(graph, n):
    visited = set()
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # back edge = cycle
        return False

    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True
    return False
```

### Grid BFS (Flood Fill / Islands)

```python
from collections import deque

def num_islands(grid):
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                queue = deque([(r, c)])
                grid[r][c] = '0'
                while queue:
                    row, col = queue.popleft()
                    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))
    return count
```

```java
// Java BFS
public void bfs(List<List<Integer>> graph, int start) {
    boolean[] visited = new boolean[graph.size()];
    Queue<Integer> queue = new LinkedList<>();
    visited[start] = true;
    queue.offer(start);
    while (!queue.isEmpty()) {
        int node = queue.poll();
        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                queue.offer(neighbor);
            }
        }
    }
}
```

## Gotchas

- **Mark visited BEFORE enqueuing (BFS)** - not after dequeuing; prevents duplicate entries in queue
- **DFS recursion depth** - Python default recursion limit is 1000; use `sys.setrecursionlimit()` or iterative DFS
- **BFS for shortest path only in unweighted graphs** - for weighted graphs, use [[graph-shortest-path]]
- **Cycle detection differs for directed vs undirected** - undirected: back edge to non-parent; directed: need coloring (white/gray/black)
- **Grid directions** - use `[(0,1),(0,-1),(1,0),(-1,0)]` for 4-directional; add diagonals for 8-directional
- **Disconnected graphs** - must start BFS/DFS from every unvisited vertex to cover all components

## See Also

- [[graph-representations]] - how to store graphs
- [[topological-sort]] - DFS-based ordering for DAGs
- [[graph-shortest-path]] - BFS for unweighted, Dijkstra for weighted
