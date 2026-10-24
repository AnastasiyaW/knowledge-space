---
title: "Netzwerkfluss"
category: algorithms
tags: [algorithms, graphs, max-flow, min-cut, ford-fulkerson, bipartite-matching]
level: 3
source_sha256: e555e86280fb68e52a0ffba1741ac83d35b6fa855e97e9971ab0deb5cdf1d757
translation: machine
translated_at: '2026-10-24'
---
# Netzwerkfluss {#network-flow}

Algorithmen für Netzwerkfluss finden den maximal möglichen Fluss von einer Quelle zu einer Senke in einem gerichteten gewichteten Graphen. Das Max-Flow-Min-Cut-Theorem verbindet den maximalen Fluss mit der minimalen Kapazität eines Schnitts. Zentrale Algorithmen sind Ford-Fulkerson, Edmonds-Karp und Dinic.

## Wichtige Fakten {#key-facts}

- **Max-Flow-Min-Cut-Theorem**: Maximaler Fluss = minimale Schnittkapazität
- **Flussbedingungen**: (1) Fluss <= Kapazität auf jeder Kante, (2) Flusserhaltung an jedem Knoten, der weder Quelle noch Senke ist
- **Residualgraph**: Vorwärtskanten mit verbleibender Kapazität + Rückwärtskanten zur Rücknahme von Fluss
- **Anwendungen**: Netzwerkbandbreite, bipartites Matching, Projektauswahl, Bildsegmentierung

## Vergleich der Algorithmen {#algorithm-comparison}

| Algorithmus | Komplexität | Geeignet für |
|-----------|-----------|---------|
| Ford-Fulkerson (DFS) | O(\|E\| * max_flow) | Ganzzahlige Kapazitäten, kleiner Fluss |
| Edmonds-Karp (BFS) | O(\|V\|\|E\|^2) | Allgemeine Verwendung, einfache Implementierung |
| Dinic | O(\|V\|^2\|E\|) | Dichte Graphen |
| Dinic (Einheitskapazität) | O(\|E\|*sqrt(\|V\|)) | Bipartites Matching |
| Push-Relabel | O(\|V\|^2*sqrt(\|E\|)) | Dichte Graphen in der Praxis |

## Muster {#patterns}

### Konzept des Residualgraphen {#residual-graph-concept}

```yaml
Original: u --(cap=8, flow=6)--> v
Residual: u --2--> v   (can send 2 more forward)
          v --6--> u   (can cancel 6 of current flow)
```

### Edmonds-Karp (BFS-basiertes Ford-Fulkerson) {#edmonds-karp-bfs-based-ford-fulkerson}

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

### Dinic-Algorithmus {#dinics-algorithm}

Verwendet blockierende Flüsse im geschichteten Graphen. BFS baut den Level-Graphen auf, DFS findet blockierende Flüsse.

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

### Bipartites Matching über maximalen Fluss {#bipartite-matching-via-max-flow}

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

Hopcroft-Karp löst bipartites Matching direkt in O(sqrt(|V|) * |E|).

## Fallstricke {#gotchas}

- Ford-Fulkerson terminiert möglicherweise nicht bei irrationalen Kapazitäten – für garantierte Terminierung Edmonds-Karp (BFS) verwenden
- Rückwärtskanten im Residualgraphen sind für die Korrektheit wesentlich – sie ermöglichen das "Rückgängigmachen" von Fluss
- Die Reduktion auf bipartites Matching erfordert Einheitskapazitäten auf allen Kanten
- Die Flusserhaltung gilt NICHT für Quelle und Senke
- Der minimale Schnitt lässt sich nach dem maximalen Fluss bestimmen: Knoten, die im Residualgraphen von der Quelle erreichbar sind, bilden S, der Rest bildet T

## Siehe auch {#see-also}

- [[graph-traversal-bfs-dfs]] - BFS wird in Edmonds-Karp und Dinic verwendet
- [[graph-coloring]] - Prüfung auf Bipartitheit hängt mit Matching zusammen
- [[shortest-path-algorithms]] - Flussnetzwerke teilen sich die Graphinfrastruktur
