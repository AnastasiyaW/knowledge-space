---
title: "Minimale Spannbäume"
category: algorithms
tags: [algorithms, graphs, MST, prim, kruskal, union-find, greedy]
level: 3
source_sha256: ea609d9e206f44d6c4f78dcc35b4ad835800f12b6b0deabf6d98fd7b41f0b8b4
translation: machine
translated_at: '2026-10-24'
---
# Minimale Spannbäume {#minimum-spanning-trees}

Ein minimaler Spannbaum (MST) eines gewichteten, ungerichteten, zusammenhängenden Graphen ist ein Spannbaum mit minimalem Gesamtgewicht der Kanten. Es gibt zwei klassische Algorithmen: Prims (den Baum gierig wachsen lassen) und Kruskals (Komponenten über die günstigste Kante verschmelzen). Beide sind gierig (greedy) und stützen sich auf die Schnitt-Eigenschaft (Cut Property).

## Wichtige Fakten {#key-facts}

- Spannbaum: Teilgraph, der alle |V| Knoten enthält, zusammenhängend und azyklisch ist und genau |V|-1 Kanten besitzt
- Der MST ist NICHT eindeutig, wenn mehrere Kanten dasselbe Gewicht haben
- **Schnitt-Eigenschaft**: Für jeden Schnitt liegt die Kante mit minimalem Gewicht unter den schneidenden Kanten in einem MST
- Einen BELIEBIGEN Spannbaum findet man, indem man BFS/DFS ausführt und die Baumkanten behält
- Prim: O(|E| log |V|) mit binärem Heap, O(|V|^2) mit Matrix
- Kruskal: O(|E| log |E|) = O(|E| log |V|), dominiert durch das Sortieren

## Prim vs. Kruskal {#prims-vs-kruskals}

| | Prim | Kruskal |
|-|--------|----------|
| Datenstruktur | Prioritätswarteschlange | Union-Find + sortierte Kanten |
| Am besten geeignet für | Dichte Graphen | Dünne Graphen |
| Vorgehen | Wächst einen einzelnen Baum | Verschmilzt Komponenten |
| Dichter Graph | O(\|V\|^2) mit Matrix | O(\|E\| log \|V\|) = O(\|V\|^2 log \|V\|) |
| Dünner Graph | O(\|E\| log \|V\|) | O(\|E\| log \|V\|) ~ O(\|V\| log \|V\|) |

## Muster {#patterns}

### Prim-Algorithmus {#prims-algorithm}

```python
import heapq

def prim(graph, start):
    visited = set()
    heap = [(0, start, None)]  # (weight, vertex, parent)
    mst_edges = []
    mst_cost = 0

    while heap and len(visited) < len(graph.adj_list):
        weight, vertex, parent = heapq.heappop(heap)
        if vertex in visited:
            continue
        visited.add(vertex)
        if parent is not None:
            mst_edges.append((parent, vertex, weight))
            mst_cost += weight
        for neighbor, w in graph.adj_list[vertex]:
            if neighbor not in visited:
                heapq.heappush(heap, (w, neighbor, vertex))

    return mst_edges, mst_cost
```

### Kruskal-Algorithmus {#kruskals-algorithm}

```python
def kruskal(vertices, edges):
    edges.sort(key=lambda e: e[2])  # sort by weight
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False  # same component = cycle
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    mst_edges = []
    mst_cost = 0
    for u, v, w in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            mst_cost += w
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges, mst_cost
```

### Minimale Kosten zum Verbinden von Punkten {#min-cost-to-connect-points}

Gegeben sind n Punkte; verbinde alle mit minimaler Gesamtdistanz. Dies ist ein MST auf dem vollständigen Graphen.

- Erzeuge alle O(n^2) Kanten mit den Distanzen
- Für vollständige (dichte) Graphen ist Prim mit O(n^2)-Matrix einfacher

## Fallstricke {#gotchas}

- Der MST gilt nur für UNGERICHTETE Graphen. Für gerichtete Graphen verwendet man eine minimale spannende Arboreszenz (Edmonds-Algorithmus)
- MST != Baum kürzester Wege: Dijkstras SPT minimiert einzelne Pfade, der MST minimiert das Gesamtgewicht
- Prim kann nicht erkennen, dass ein Graph nicht zusammenhängend ist (er findet nur den MST der Startkomponente)
- Kruskal kann einen nicht zusammenhängenden Graphen erkennen: Hat der MST weniger als |V|-1 Kanten, ist der Graph nicht zusammenhängend
- Ein frühzeitiger Abbruch bei Kruskal, sobald |V|-1 Kanten gefunden wurden, spart unnötige Iterationen

## Siehe auch {#see-also}

- [[union-find]] - Datenstruktur für disjunkte Mengen, die Kruskal verwendet
- [[shortest-path-algorithms]] - MST vs. Baum kürzester Wege
- [[graph-representation]] - Die Komplexität von Prim hängt von der Repräsentation ab
- [[graph-traversal-bfs-dfs]] - BFS/DFS findet einen beliebigen Spannbaum
