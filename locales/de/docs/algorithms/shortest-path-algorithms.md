---
title: "Algorithmen für kürzeste Pfade"
category: algorithms
tags: [algorithms, graphs, dijkstra, bellman-ford, floyd-warshall, shortest-path, weighted-graph]
level: 3
source_sha256: 9fab3eb23210cfcca83a906e1435f68c0328fb5580a53a27e3731b7dc5248ddd
translation: machine
translated_at: '2026-10-24'
---
# Algorithmen für kürzeste Pfade {#shortest-path-algorithms}

Algorithmen zur Suche kürzester Pfade in gewichteten Graphen: BFS (ungewichtet), Dijkstra (nicht-negative Gewichte), Bellman-Ford (behandelt negative Kanten), Floyd-Warshall (alle Paare), DAG-Relaxierung und Johnson-Algorithmus.

## Auswahl des Algorithmus {#algorithm-selection}

| Bedingung | Algorithmus | Komplexität |
|-----------|----------|-----------|
| Ungewichtet | BFS | O(\|V\| + \|E\|) |
| Nicht-negative Gewichte, eine Quelle | Dijkstra | O((\|V\|+\|E\|) log \|V\|) |
| Negative Kanten, eine Quelle | Bellman-Ford | O(\|V\|\|E\|) |
| DAG, beliebige Gewichte, eine Quelle | Topologische DP | O(\|V\| + \|E\|) |
| Alle Paare, keine negativen Kanten | Dijkstra von jedem Knoten | O(\|V\|(\|V\|+\|E\|) log \|V\|) |
| Alle Paare, negative Kanten, dicht | Floyd-Warshall | O(\|V\|^3) |
| Alle Paare, negative Kanten, dünn | Johnson | O(\|V\|^2 log \|V\| + \|V\|\|E\|) |
| Dichter Graph, keine neg. Kanten | Dijkstra mit Matrix | O(\|V\|^2) |

## Wichtige Fakten {#key-facts}

- **Zyklus mit negativem Gewicht**: Wenn er von der Quelle aus erreichbar ist, existiert kein wohldefinierter kürzester Pfad
- Dijkstra scheitert bei negativen Kanten – die Greedy-Annahme bricht
- Floyd-Warshall erkennt negative Zyklen: dist[i][i] < 0 nach der Ausführung
- Der kürzeste Pfad in einem DAG ist der schnellste Einquellen-Algorithmus, wenn der Graph azyklisch ist

## Muster {#patterns}

### BFS – ungewichtet: O(|V| + |E|) {#bfs-unweighted-ov-e}

```python
from collections import deque

def bfs_shortest(graph, src):
    dist = {src: 0}
    queue = deque([src])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.adj_list[vertex]:
            if neighbor not in dist:
                dist[neighbor] = dist[vertex] + 1
                queue.append(neighbor)
    return dist
```

### Dijkstra – nicht-negative Gewichte {#dijkstra-non-negative-weights}

```python
import heapq

def dijkstra(graph, src):
    dist = {v: float('inf') for v in graph.adj_list}
    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, vertex = heapq.heappop(heap)
        if d > dist[vertex]:
            continue  # stale entry
        for neighbor, weight in graph.adj_list[vertex]:
            new_dist = dist[vertex] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist
```

**Warum Greedy funktioniert:** Wenn Knoten u entnommen wird, ist dist[u] optimal. Jeder andere Pfad müsste über einen Knoten mit größerer Distanz führen (alle Gewichte >= 0).

**Komplexitätsvarianten:**
- Binärer Heap: O((|V| + |E|) log |V|)
- Fibonacci-Heap: O(|E| + |V| log |V|)
- Adjazenzmatrix, ohne Heap: O(|V|^2) – besser für dichte Graphen

### Bellman-Ford – behandelt negative Kanten {#bellman-ford-handles-negative-edges}

```python
def bellman_ford(graph, src):
    dist = {v: float('inf') for v in graph.vertices}
    dist[src] = 0

    for _ in range(len(graph.vertices) - 1):
        for u, v, w in graph.edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Negative cycle detection
    for u, v, w in graph.edges:
        if dist[u] + w < dist[v]:
            return None  # negative cycle
    return dist
```

**Warum |V|-1 Iterationen:** Ein kürzester Pfad hat höchstens |V|-1 Kanten (keine wiederholten Knoten). Iteration k liefert den kürzesten Pfad mit höchstens k Kanten.

### Floyd-Warshall – alle Paare: O(|V|^3) {#floyd-warshall-all-pairs-ov3}

```python
def floyd_warshall(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):       # intermediate vertex
        for i in range(n):   # source
            for j in range(n):  # destination
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
```

### Kürzester Pfad in einem DAG – O(|V| + |E|) {#dag-shortest-path-ov-e}

Knoten in topologischer Reihenfolge verarbeiten. Negative Gewichte werden behandelt.

```python
def dag_shortest_path(graph, src):
    order = topological_sort(graph)
    dist = {v: float('inf') for v in graph.adj_list}
    dist[src] = 0

    for vertex in order:
        if dist[vertex] != float('inf'):
            for neighbor, weight in graph.adj_list[vertex]:
                if dist[vertex] + weight < dist[neighbor]:
                    dist[neighbor] = dist[vertex] + weight
    return dist
```

### Johnson-Algorithmus – alle Paare mit negativen Kanten {#johnsons-algorithm-all-pairs-with-negative-edges}

1. Neuen Knoten s mit Kanten vom Gewicht 0 zu allen Knoten hinzufügen
2. Bellman-Ford von s ausführen, um die Potentialfunktion h[v] zu erhalten
3. Neu gewichten: w'(u,v) = w(u,v) + h[u] - h[v] >= 0
4. Dijkstra von jedem Knoten auf dem neu gewichteten Graphen ausführen
5. Distanzen zurückrechnen: dist(u,v) = dist'(u,v) - h[u] + h[v]

Für dünne Graphen besser als Floyd-Warshall.

## Fallstricke {#gotchas}

- Dijkstras `if d > dist[vertex]: continue` ist für die Korrektheit bei verzögertem Löschen (veraltete Heap-Einträge) entscheidend
- Erkennung negativer Zyklen bei Bellman-Ford: Wenn NACH |V|-1 Durchläufen noch eine Kante relaxiert werden kann, existiert ein Zyklus
- Die Schleifenreihenfolge bei Floyd-Warshall muss k (Zwischenknoten) außen, dann i, dann j sein
- Der kürzeste Pfad in einem DAG erfordert zuerst eine topologische Sortierung – bei zyklischen Graphen schlägt er fehl
- Für Abfragen eines einzelnen Paares berechnen alle diese Algorithmen trotzdem die Einquellen-Lösung (keine bekannte allgemeine Methode ist schneller)

## Siehe auch {#see-also}

- [[graph-traversal-bfs-dfs]] – BFS für ungewichtete kürzeste Pfade
- [[topological-sort]] – erforderlich für den kürzesten Pfad in einem DAG
- [[graph-representation]] – Komplexität hängt von der Darstellung ab
- [[minimum-spanning-trees]] – verwandte Graphoptimierung (MST ≠ Baum kürzester Pfade)
