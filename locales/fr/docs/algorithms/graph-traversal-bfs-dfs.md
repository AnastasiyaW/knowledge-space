---
title: "Parcours de graphes : BFS et DFS"
category: algorithms
tags: [algorithms, graphs, bfs, dfs, traversal, shortest-path, grid]
level: 3
source_sha256: 88e0b3828287e1a74cc451919c2dc938e0069f1690862ba876369215bacea292
translation: machine
translated_at: '2026-10-24'
---
# Parcours de graphes : BFS et DFS {#graph-traversal-bfs-and-dfs}

BFS (Breadth-First Search, parcours en largeur) et DFS (Depth-First Search, parcours en profondeur) sont les deux algorithmes fondamentaux de parcours de graphes. Tous deux visitent chaque sommet en temps O(|V| + |E|), mais ils diffèrent par l'ordre de visite, la structure de données utilisée et leurs applications. BFS trouve les plus courts chemins dans les graphes non pondérés ; DFS est utilisé pour la détection de cycles, le tri topologique et les composantes connexes.

## Points clés {#key-facts}

- **DFS** : utilise une pile (ou la récursion). Descend en profondeur avant de revenir en arrière. Espace O(profondeur max)
- **BFS** : utilise une file. Explore niveau par niveau. Espace O(largeur max)
- Dans les deux cas : O(|V| + |E|) en temps avec une liste d'adjacence, O(|V|^2) avec une matrice d'adjacence
- BFS garantit le plus court chemin dans les graphes non pondérés
- DFS est préféré pour la détection de cycles, le tri topologique et la recherche de tous les chemins

## Choisir entre DFS et BFS {#choosing-dfs-vs-bfs}

| Cas d'usage | Choix |
|----------|--------|
| Plus court chemin (non pondéré) | BFS |
| Vérification de la connexité | Indifférent |
| Détection de cycles | DFS |
| Tri topologique | DFS (ou BFS avec l'algorithme de Kahn) |
| Recherche de tous les chemins | DFS (avec retour arrière) |
| Problèmes par niveaux / couches | BFS |
| Graphe très profond | DFS (si la profondeur reste maîtrisable) |
| Graphe très large | DFS (la file BFS devient énorme) |

## Motifs {#patterns}

### DFS itératif {#iterative-dfs}

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

### DFS récursif {#recursive-dfs}

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

### Existence d'un chemin par DFS {#dfs-path-existence}

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

### Plus court chemin par BFS (non pondéré) {#bfs-shortest-path-unweighted}

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

### Graphe implicite : Keys and Rooms {#implicit-graph-keys-and-rooms}

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

### BFS multi-sources : oranges pourries {#multi-source-bfs-rotten-oranges}

Toutes les oranges pourries commencent simultanément. Chaque niveau du BFS = 1 minute.

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

## Pièges {#gotchas}

- BFS : marquer comme visité lors de l'**enfilage**, et non lors du défilage, ce qui évite les traitements en double
- Le DFS itératif traite les sommets dans un ordre différent du DFS récursif (la pile inverse l'ordre des voisins)
- Le DFS récursif risque un dépassement de pile sur les graphes profonds (limite par défaut de Python : 1000)
- Les problèmes sur grille sont des graphes implicites : les voisins sont définis par des directions, et non par une liste d'adjacence explicite
- BFS multi-sources : enfiler TOUTES les sources au temps 0, et non une à une

## Voir aussi {#see-also}

- [[graph-representation]] - implémentations par liste et matrice d'adjacence
- [[shortest-path-algorithms]] - plus courts chemins dans les graphes pondérés (Dijkstra, Bellman-Ford)
- [[topological-sort]] - ordonnancement topologique par DFS et par BFS
- [[trees-and-binary-trees]] - parcours d'arbres comme cas particulier du parcours de graphes
