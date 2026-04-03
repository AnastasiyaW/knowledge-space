---
title: "Graph Traversal: BFS and DFS"
category: algorithms
tags: [algorithms, graphs, bfs, dfs, traversal, shortest-path, grid]
---

# Graph Traversal: BFS and DFS

BFS (Breadth-First Search) and DFS (Depth-First Search) are the two fundamental graph traversal algorithms. Both visit every vertex in O(|V| + |E|) time but differ in order, data structure, and applications. BFS finds shortest paths in unweighted graphs; DFS is used for cycle detection, topological sort, and connected components.

## Key Facts

- **DFS**: Uses stack (or recursion). Goes deep before backtracking. Space O(max depth)
- **BFS**: Uses queue. Explores level by level. Space O(max breadth)
- Both: O(|V| + |E|) time with adjacency list, O(|V|^2) with adjacency matrix
- BFS guarantees shortest path in unweighted graphs
- DFS preferred for cycle detection, topological sort, finding all paths

## Choosing DFS vs BFS

| Use Case | Choose |
|----------|--------|
| Shortest path (unweighted) | BFS |
| Checking connectivity | Either |
| Cycle detection | DFS |
| Topological sort | DFS (or BFS with Kahn's) |
| Finding all paths | DFS (with backtracking) |
| Level-order / layer problems | BFS |
| Very deep graph | DFS (if depth manageable) |
| Very wide graph | DFS (BFS queue gets huge) |

## Patterns

### Iterative DFS

```python
def dfs(graph, start):
    visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            print(vertex)  # process
            for neighbor in graph.adj_list[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)
```

### Recursive DFS

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start)  # process
    for neighbor in graph.adj_list[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

### BFS

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)  # mark when enqueuing, not dequeuing
    while queue:
        vertex = queue.popleft()
        print(vertex)
        for neighbor in graph.adj_list[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### DFS Path Existence

```python
def has_path(graph, src, dest):
    visited = set()
    stack = [src]
    while stack:
        vertex = stack.pop()
        if vertex == dest:
            return True
        if vertex not in visited:
            visited.add(vertex)
            for neighbor in graph.adj_list[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)
    return False
```

### BFS Shortest Path (Unweighted)

```python
from collections import deque

def shortest_path(graph, src, dest):
    visited = {src}
    queue = deque([(src, [src])])
    while queue:
        vertex, path = queue.popleft()
        if vertex == dest:
            return path
        for neighbor in graph.adj_list[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None
```

### Implicit Graph: Keys and Rooms

```python
def can_visit_all_rooms(rooms):
    visited = set()
    stack = [0]
    while stack:
        room = stack.pop()
        if room not in visited:
            visited.add(room)
            for key in rooms[room]:
                if key not in visited:
                    stack.append(key)
    return len(visited) == len(rooms)
```

### Multi-Source BFS: Rotten Oranges

All rotten oranges start simultaneously. Each BFS level = 1 minute.

```python
from collections import deque

def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    max_time = 0
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        pass  # directions used in loop below
    while queue:
        r, c, time = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                max_time = max(max_time, time + 1)
                queue.append((nr, nc, time + 1))
    return max_time if fresh == 0 else -1
```

## Gotchas

- BFS: mark visited when **enqueuing**, not when dequeuing - prevents duplicate processing
- Iterative DFS processes vertices in different order than recursive DFS (stack reverses neighbor order)
- Recursive DFS risks stack overflow on deep graphs (Python default limit: 1000)
- Grid problems are implicit graphs - neighbors defined by directions, not explicit adjacency list
- Multi-source BFS: enqueue ALL sources at time 0, not one at a time

## See Also

- [[graph-representation]] - adjacency list and matrix implementations
- [[shortest-path-algorithms]] - weighted graph shortest paths (Dijkstra, Bellman-Ford)
- [[topological-sort]] - DFS and BFS-based topological ordering
- [[trees-and-binary-trees]] - tree traversals as special case of graph traversal
