---
title: "Flot dans les réseaux"
category: algorithms
tags: [algorithms, graphs, max-flow, min-cut, ford-fulkerson, bipartite-matching]
level: 3
source_sha256: e555e86280fb68e52a0ffba1741ac83d35b6fa855e97e9971ab0deb5cdf1d757
translation: machine
translated_at: '2026-10-24'
---
# Flot dans les réseaux {#network-flow}

Les algorithmes de flot dans les réseaux recherchent le flot maximal réalisable de la source vers le puits dans un graphe orienté pondéré. Le théorème flot maximal-coupe minimale relie le flot maximal à la capacité de la coupe minimale. Algorithmes principaux : Ford-Fulkerson, Edmonds-Karp et Dinic.

## Faits clés {#key-facts}

- **Théorème flot maximal-coupe minimale** : flot maximal = capacité de la coupe minimale
- **Contraintes de flot** : (1) flot <= capacité sur chaque arc, (2) conservation du flot en chaque sommet autre que la source et le puits
- **Graphe résiduel** : arcs directs avec capacité restante + arcs inverses permettant d'annuler du flot
- **Applications** : bande passante réseau, couplage biparti, sélection de projets, segmentation d'images

## Comparaison des algorithmes {#algorithm-comparison}

| Algorithme | Complexité | Usage recommandé |
|-----------|-----------|---------|
| Ford-Fulkerson (DFS) | O(\|E\| * flot_max) | Capacités entières, flot faible |
| Edmonds-Karp (BFS) | O(\|V\|\|E\|^2) | Usage général, implémentation simple |
| Dinic | O(\|V\|^2\|E\|) | Graphes denses |
| Dinic (capacité unitaire) | O(\|E\|*sqrt(\|V\|)) | Couplage biparti |
| Push-relabel | O(\|V\|^2*sqrt(\|E\|)) | Graphes denses en pratique |

## Schémas {#patterns}

### Concept de graphe résiduel {#residual-graph-concept}

```yaml
Original: u --(cap=8, flow=6)--> v
Residual: u --2--> v   (can send 2 more forward)
          v --6--> u   (can cancel 6 of current flow)
```

### Edmonds-Karp (Ford-Fulkerson basé sur BFS) {#edmonds-karp-bfs-based-ford-fulkerson}

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

### Algorithme de Dinic {#dinics-algorithm}

Utilise des flots bloquants dans un graphe en couches. Le BFS construit le graphe de niveaux, le DFS recherche les flots bloquants.

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

### Couplage biparti via flot maximal {#bipartite-matching-via-max-flow}

```bash
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

Hopcroft-Karp résout directement le couplage biparti en O(sqrt(|V|) * |E|).

## Pièges courants {#gotchas}

- Ford-Fulkerson peut ne pas se terminer avec des capacités irrationnelles : utiliser Edmonds-Karp (BFS) pour garantir la terminaison
- Les arcs inverses du graphe résiduel sont essentiels à la correction : ils permettent de « défaire » du flot
- La réduction au couplage biparti exige des capacités unitaires sur tous les arcs
- La conservation du flot ne s'applique PAS à la source et au puits
- La coupe minimale se trouve après le flot maximal : les sommets atteignables depuis la source dans le graphe résiduel forment S, les autres forment T

## Voir aussi {#see-also}

- [[graph-traversal-bfs-dfs]] - BFS utilisé dans Edmonds-Karp et Dinic
- [[graph-coloring]] - vérification de la bipartition, liée au couplage
- [[shortest-path-algorithms]] - les réseaux de flot partagent l'infrastructure des graphes
