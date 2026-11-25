---
title: "Graphen-Traversierung: BFS und DFS"
category: algorithms
tags: [algorithms, graphs, bfs, dfs, traversal, shortest-path, grid]
level: 3
source_sha256: 88e0b3828287e1a74cc451919c2dc938e0069f1690862ba876369215bacea292
translation: machine
translated_at: '2026-10-24'
---
# Graphen-Traversierung: BFS und DFS {#graph-traversal-bfs-and-dfs}

BFS (Breadth-First Search) und DFS (Depth-First Search) sind die beiden grundlegenden Algorithmen zur Traversierung von Graphen. Beide besuchen jeden Knoten in O(|V| + |E|) Zeit, unterscheiden sich jedoch in der Reihenfolge, der Datenstruktur und den Anwendungsgebieten. BFS findet kürzeste Pfade in ungewichteten Graphen; DFS wird für Zykluserkennung, topologische Sortierung und die Bestimmung zusammenhängender Komponenten verwendet.

## Wichtige Fakten {#key-facts}

- **DFS**: Verwendet einen Stack (oder Rekursion). Geht zuerst in die Tiefe, bevor zurückgegangen wird. Speicher O(maximale Tiefe)
- **BFS**: Verwendet eine Queue. Durchläuft Ebene für Ebene. Speicher O(maximale Breite)
- Beide: O(|V| + |E|) Zeit mit Adjazenzliste, O(|V|^2) mit Adjazenzmatrix
- BFS garantiert den kürzesten Pfad in ungewichteten Graphen
- DFS bevorzugt für Zykluserkennung, topologische Sortierung und die Suche nach allen Pfaden

## Wahl zwischen DFS und BFS {#choosing-dfs-vs-bfs}

| Anwendungsfall | Wahl |
|----------|--------|
| Kürzester Pfad (ungewichtet) | BFS |
| Prüfung auf Zusammenhang | Beliebig |
| Zykluserkennung | DFS |
| Topologische Sortierung | DFS (oder BFS mit Kahns Algorithmus) |
| Suche nach allen Pfaden | DFS (mit Backtracking) |
| Level-Order- / Schichtprobleme | BFS |
| Sehr tiefer Graph | DFS (sofern die Tiefe handhabbar ist) |
| Sehr breiter Graph | DFS (die BFS-Queue wird sehr groß) |

## Muster {#patterns}

### Iterative DFS {#iterative-dfs}

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

### Rekursive DFS {#recursive-dfs}

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

### BFS {#bfs}

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

### DFS-Prüfung auf Pfadexistenz {#dfs-path-existence}

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

### BFS-Kürzester Pfad (ungewichtet) {#bfs-shortest-path-unweighted}

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

### Implizite Graphen: Schlüssel und Räume {#implicit-graph-keys-and-rooms}

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

### Multi-Source-BFS: Faule Orangen {#multi-source-bfs-rotten-oranges}

Alle faulen Orangen starten gleichzeitig. Jede BFS-Ebene = 1 Minute.

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

## Fallstricke {#gotchas}

- BFS: Knoten beim **Einreihen** als besucht markieren, nicht beim Herausnehmen - verhindert doppelte Verarbeitung
- Iterative DFS verarbeitet Knoten in einer anderen Reihenfolge als rekursive DFS (der Stack kehrt die Nachbarreihenfolge um)
- Rekursive DFS riskiert einen Stack-Überlauf bei tiefen Graphen (Python-Standardlimit: 1000)
- Gitterprobleme sind implizite Graphen - Nachbarn werden über Richtungen definiert, nicht über eine explizite Adjazenzliste
- Multi-Source-BFS: ALLE Quellen zum Zeitpunkt 0 einreihen, nicht eine nach der anderen

## Siehe auch {#see-also}

- [[graph-representation]] - Implementierungen von Adjazenzliste und -matrix
- [[shortest-path-algorithms]] - Kürzeste Pfade in gewichteten Graphen (Dijkstra, Bellman-Ford)
- [[topological-sort]] - Topologische Ordnung auf Basis von DFS und BFS
- [[trees-and-binary-trees]] - Baumtraversierung als Spezialfall der Graphentraversierung
