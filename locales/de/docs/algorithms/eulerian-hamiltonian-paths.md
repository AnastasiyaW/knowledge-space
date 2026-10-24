---
title: "Eulersche und Hamiltonsche Pfade"
category: algorithms
tags: [algorithms, graphs, eulerian, hamiltonian, hierholzer, backtracking]
level: 3
source_sha256: afae69f79b115a380b6aef5ce649481c59df124b741de243bd5d7a4ef5a618d7
translation: machine
translated_at: '2026-10-24'
---
# Eulersche und Hamiltonsche Pfade {#eulerian-and-hamiltonian-paths}

Eulersche Pfade besuchen jede KANTE genau einmal; Hamiltonsche Pfade besuchen jeden KNOTEN genau einmal. Eulersche Probleme sind polynomiell lösbar (einfache Gradbedingungen + Hierholzers Algorithmus mit O(|E|)). Hamiltonsche Probleme sind NP-vollständig.

## Vergleich im Überblick {#key-comparison}

| | Eulersch | Hamiltonsch |
|-|----------|-------------|
| Was durchlaufen wird | Jede Kante genau einmal | Jeden Knoten genau einmal |
| Komplexität der Suche | O(\|E\|) - polynomiell | NP-vollständig |
| Existenzbedingungen | Einfache Gradbedingungen | Keine einfache Charakterisierung |
| Algorithmus | Hierholzer | Backtracking O(n!), DP O(2^n * n^2) |

## Bedingungen für eulersche Wege/Kreise {#eulerian-trailcircuit-conditions}

### Ungerichteter Graph {#undirected-graph}

| Bedingung | Ergebnis |
|-----------|----------|
| Alle Knoten mit Grad ungleich null sind zusammenhängend UND alle Grade gerade | Eulerscher **Kreis** |
| Alle Knoten mit Grad ungleich null sind zusammenhängend UND genau 2 Knoten mit ungeradem Grad | Eulerscher **Weg** (Start/Ende an den Knoten mit ungeradem Grad) |
| Mehr als 2 Knoten mit ungeradem Grad | Kein eulerscher Weg |

### Gerichteter Graph {#directed-graph}

| Bedingung | Ergebnis |
|-----------|----------|
| Stark zusammenhängend UND Eingangsgrad == Ausgangsgrad für alle Knoten | Eulerscher **Kreis** |
| Schwach zusammenhängend UND genau ein Knoten mit Ausgang-Eingang=1 (Start), einer mit Eingang-Ausgang=1 (Ende), alle übrigen ausgeglichen | Eulerscher **Weg** |

## Muster {#patterns}

### Eulerschen Kreis prüfen (ungerichtet) {#check-eulerian-circuit-undirected}

```python
def has_eulerian_circuit(graph):
    non_isolated = [v for v in graph.adj_list if graph.adj_list[v]]
    if not non_isolated:
        return True
    # Check connectivity via DFS
    visited = set()
    stack = [non_isolated[0]]
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            for u in graph.adj_list[v]:
                stack.append(u)
    if any(v not in visited for v in non_isolated):
        return False
    # Check all degrees even
    return all(len(graph.adj_list[v]) % 2 == 0 for v in graph.adj_list)
```

### Hierholzers Algorithmus - O(|E|) {#hierholzers-algorithm-oe}

```python
def hierholzer(graph):
    start = next(v for v in graph.adj_list if graph.adj_list[v])
    adj = {v: list(neighbors) for v, neighbors in graph.adj_list.items()}
    stack = [start]
    circuit = []

    while stack:
        v = stack[-1]
        if adj[v]:
            u = adj[v].pop()
            adj[u].remove(v)  # remove reverse edge for undirected
            stack.append(u)
        else:
            circuit.append(stack.pop())

    return circuit[::-1]
```

### Reiseroute rekonstruieren (gerichteter eulerscher Pfad) {#reconstruct-itinerary-directed-eulerian-path}

Gegeben sind Flugtickets; rekonstruiere die lexikographisch kleinste Reiseroute, die alle Tickets genau einmal verwendet.

```python
from collections import defaultdict

def find_itinerary(tickets):
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):  # reverse sort for efficient pop
        graph[src].append(dst)

    result = []
    stack = ["JFK"]
    while stack:
        while graph[stack[-1]]:
            stack.append(graph[stack[-1]].pop())
        result.append(stack.pop())

    return result[::-1]
```

### Hamiltonscher Pfad - Backtracking O(n!) {#hamiltonian-path-backtracking-on}

```python
def hamiltonian_path(graph, path, visited):
    if len(path) == len(graph.adj_list):
        return path

    current = path[-1]
    for neighbor in graph.adj_list[current]:
        if neighbor not in visited:
            visited.add(neighbor)
            path.append(neighbor)
            result = hamiltonian_path(graph, path, visited)
            if result:
                return result
            path.pop()
            visited.remove(neighbor)
    return None

def find_hamiltonian(graph):
    for start in graph.adj_list:
        result = hamiltonian_path(graph, [start], {start})
        if result:
            return result
    return None
```

### Held-Karp-DP für Hamiltonsche Pfade - O(2^n * n^2) {#held-karp-dp-for-hamiltonian-o2n-n2}

Für eine exakte Lösung besser als O(n!). Die Bitmask-DP-Implementierung findet sich unter [[traveling-salesman-problem]].

## Wichtige Fakten {#key-facts}

- **Euler (1736)**: Das Königsberger Brückenproblem - das erste Resultat der Graphentheorie
- **Satz von Ore**: Gilt deg(u) + deg(v) >= n für alle nicht benachbarten Knotenpaare, existiert ein Hamiltonscher Kreis (hinreichend, aber nicht notwendig)
- Hierholzers Verfahren folgt Kanten gierig, bis es nicht weitergeht, und bildet dann per Backtracking Erweiterungen
- Historischer Ursprung der Graphentheorie: Lässt sich über alle 7 Brücken genau einmal gehen?

## Fallstricke {#gotchas}

- Eulersch = Kanten, Hamiltonsch = Knoten - leicht zu verwechseln
- Hierholzers Algorithmus muss bei ungerichteten Graphen Kanten in BEIDE Richtungen entfernen
- Für Hamiltonsche Pfade gibt es keine einfache Bedingung (anders als bei eulerschen) - man muss suchen oder DP verwenden
- Hamiltonscher Pfad vs. Kreis: Ein Pfad kehrt nicht zum Start zurück, ein Kreis schon
- Eulerscher Weg mit 2 Knoten ungeraden Grades: MUSS an einem davon beginnen und am anderen enden

## Siehe auch {#see-also}

- [[traveling-salesman-problem]] - Hamiltonscher Kreis mit minimalem Gewicht
- [[graph-traversal-bfs-dfs]] - DFS wird in Hierholzers Algorithmus verwendet
- [[complexity-classes]] - Hamiltonscher Pfad ist NP-vollständig
