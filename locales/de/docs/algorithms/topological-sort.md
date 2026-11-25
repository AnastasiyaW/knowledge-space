---
title: "Topologische Sortierung"
category: algorithms
tags: [algorithms, graphs, topological-sort, DAG, scheduling, kahn]
level: 3
source_sha256: b8c8b53c001f48b9d6894430ceae2714c9037957b5625e309325396b0a647510
translation: machine
translated_at: '2026-10-24'
---
# Topologische Sortierung {#topological-sort}

Eine topologische Ordnung eines DAG (Directed Acyclic Graph, gerichteter azyklischer Graph) ist eine lineare Anordnung der Knoten, sodass für jede Kante u -> v gilt: u steht vor v. Nur auf DAGs möglich - ein Zyklus erzeugt einen Widerspruch. Zwei Algorithmen: DFS-basiert (Umkehrung der Post-order) und Kahns Algorithmus (BFS mit Verfolgung des Eingangsgrads).

## Wichtige Fakten {#key-facts}

- Funktioniert nur auf DAGs - ein Zyklus bedeutet, dass keine gültige Ordnung existiert
- Nicht eindeutig - es können mehrere gültige Ordnungen existieren
- Beide Algorithmen: O(|V| + |E|) Zeit und Speicher
- Anwendungen: Studienvoraussetzungen, Aufgabenplanung, Build-Systeme, Reihenfolge beim Laden von Datenbanktabellen, kritischer Pfad

## Algorithmenvergleich {#algorithm-comparison}

| | DFS-basiert | Kahn (BFS) |
|-|-----------|---------------------|
| Ordnungserkennung | Post-order-DFS umgekehrt | Über den Eingangsgrad |
| Zyklenerkennung | Verfolgung von "im Stack" (graue Knoten) | Ausgabegröße < \|V\| |
| Mehrere gültige Ordnungen | Beliebige DFS-Reihenfolge | Steuerbar über Prioritätswarteschlange |
| Implementierung | Einfachere Rekursion | Explizite Verfolgung des Eingangsgrads |

## Muster {#patterns}

### DFS-basierte topologische Sortierung {#dfs-based-topological-sort}

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

Warum es funktioniert: Wenn wir Knoten u anhängen, sind alle von u erreichbaren Knoten bereits angehängt. Nach der Umkehrung steht u vor allen Knoten, auf die es zeigt.

### Kahns Algorithmus (BFS-basiert) {#kahns-algorithm-bfs-based}

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

### Kritischer Pfad (minimale Zeit für alle Aufgaben) {#critical-path-minimum-time-for-all-tasks}

Gegeben ist ein Aufgabengraph mit Dauern. Bestimme die minimale Fertigstellungszeit mithilfe einer topologischen Ordnung und dynamischer Programmierung.

```python
def critical_path(graph):
    order = topological_sort_kahn(graph)
    earliest = {v: 0 for v in graph.adj_list}
    for u in order:
        for v, weight in graph.adj_list[u]:
            earliest[v] = max(earliest[v], earliest[u] + weight)
    return max(earliest.values())  # minimum total time
```

Der kritische Pfad = längster Pfad durch den DAG = minimale Fertigstellungszeit.

### Kürzester Pfad im DAG {#shortest-path-in-dag}

In topologischer Reihenfolge verarbeiten und Kanten relaxieren. O(|V| + |E|), behandelt auch negative Gewichte.

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

## Fallstricke {#gotchas}

- Die DFS-basierte Variante erfordert die UMKEHRUNG der Post-order - wer sie vergisst, erhält die falsche Reihenfolge
- Zyklenerkennung bei Kahn: Hat die Ausgabe weniger Knoten als der Graph, existiert ein Zyklus
- Mehrere gültige Ordnungen sind möglich - nicht von einer bestimmten Ordnung ausgehen
- Nicht anwendbar auf ungerichtete Graphen oder Graphen mit Zyklen
- Die Kursplanung nutzt eine topologische Sortierung, benötigt aber eventuell zusätzlich Nebenbedingungen für parallel belegbare Kurse (separates Problem)

## Siehe auch {#see-also}

- [[graph-traversal-bfs-dfs]] - DFS- und BFS-Grundlagen, die hier verwendet werden
- [[shortest-path-algorithms]] - Kürzester Pfad im DAG als Anwendung
- [[graph-representation]] - Adjazenzliste für die topologische Sortierung
