---
title: "Graphenfärbung"
category: algorithms
tags: [algorithms, graphs, coloring, chromatic-number, bipartite, NP-complete, scheduling]
level: 3
source_sha256: fbfa493a5a6d1e2d8519a98000058314e61e0b47353877c1bfb4d5bb3cf80bac
translation: machine
translated_at: '2026-10-24'
---
# Graphenfärbung {#graph-coloring}

Graphenfärbung weist Knoten Farben so zu, dass keine zwei benachbarten Knoten dieselbe Farbe haben. Die chromatische Zahl chi(G) ist die minimale Anzahl der benötigten Farben. 2-Färbung (Bipartitheit) ist polynomiell lösbar; k-Färbung für k >= 3 ist NP-vollständig.

## Kernfakten {#key-facts}

- **Chromatische Zahl chi(G)**: minimale Anzahl Farben für eine gültige Färbung
- **2-färbbar** genau dann, wenn bipartit, genau dann, wenn kein Kreis ungerader Länge existiert – prüfbar in O(|V| + |E|)
- **k-färbbar (k >= 3)**: NP-vollständig
- Die Greedy-Färbung verwendet höchstens Delta+1 Farben (Delta = maximaler Grad)
- **Satz von Brooks**: chi(G) <= Delta für zusammenhängende Graphen, die weder vollständig noch ungerade Kreise sind
- **Satz von Vizing** (Kantenfärbung): chi'(G) ist entweder Delta oder Delta+1

## Anwendungen {#applications}

- **Ressourcenplanung**: sich überschneidende Aufgaben als Kanten, Farben = Ressourcen (z. B. minimale Anzahl Fahrzeuge, Räume usw.)
- **Registerallokation** in Compilern
- **Frequenzzuweisung** in drahtlosen Netzen
- **Prüfungsplanung**: kollidierende Prüfungen benötigen verschiedene Zeitfenster
- **Sudoku**: 9-Färbung des Nebenbedingungsgraphen (81 Knoten, Kanten für gleiche Zeile/Spalte/Box)

## Muster {#patterns}

### Bipartitheitsprüfung (2-Färbung) - O(|V| + |E|) {#bipartite-check-2-coloring-ov-e}

```python
from collections import deque

def is_bipartite(graph):
    color = {}
    for start in graph.adj_list:
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph.adj_list[vertex]:
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]  # alternate
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False  # odd cycle found
    return True
```

### Greedy-Färbung {#greedy-coloring}

```python
def greedy_coloring(graph, order=None):
    if order is None:
        order = list(graph.adj_list.keys())
    colors = {}
    for vertex in order:
        neighbor_colors = {colors[n] for n in graph.adj_list[vertex] if n in colors}
        color = 0
        while color in neighbor_colors:
            color += 1
        colors[vertex] = color
    return colors, max(colors.values()) + 1
```

Das Ergebnis hängt von der Knotenreihenfolge ab. Die chromatische Zahl wird NICHT garantiert.

### Welsh-Powell-Heuristik {#welsh-powell-heuristic}

Knoten vor der Greedy-Färbung nach absteigendem Grad sortieren. Liefert oft gute (nicht optimale) Ergebnisse.

```python
def welsh_powell(graph):
    order = sorted(graph.adj_list,
                   key=lambda v: len(graph.adj_list[v]), reverse=True)
    return greedy_coloring(graph, order)
```

### Exakte k-Färbung (Backtracking) {#exact-k-coloring-backtracking}

```python
def color_graph(graph, k):
    colors = {}

    def backtrack(vertex_list, idx):
        if idx == len(vertex_list):
            return True
        vertex = vertex_list[idx]
        for color in range(k):
            neighbor_colors = {colors.get(n) for n in graph.adj_list[vertex]}
            if color not in neighbor_colors:
                colors[vertex] = color
                if backtrack(vertex_list, idx + 1):
                    return True
                del colors[vertex]
        return False

    vertices = list(graph.adj_list.keys())
    if backtrack(vertices, 0):
        return colors
    return None  # not k-colorable
```

## Verwandte Konzepte {#related-concepts}

| Konzept | Definition |
|---------|-----------|
| Clique | Teilmenge paarweise benachbarter Knoten |
| Unabhängige Menge | Teilmenge ohne zwei benachbarte Knoten |
| Cliquenzahl omega(G) | Größe der größten Clique. omega(G) <= chi(G) |
| Perfekter Graph | omega(G) = chi(G). Umfasst bipartite Graphen und chordale Graphen |
| Kantenfärbung | Kanten färben, wobei keine zwei Kanten mit gemeinsamem Knoten dieselbe Farbe haben |

## Stolperfallen {#gotchas}

- Der vollständige Graph K_n benötigt genau n Farben
- Gerader Kreis: chi = 2; ungerader Kreis: chi = 3
- Das Ergebnis der Greedy-Färbung hängt vollständig von der Reihenfolge der Knotenverarbeitung ab
- Die Bipartitheitsprüfung behandelt unzusammenhängende Graphen: man muss von jedem ungefärbten Knoten aus starten
- Kantenfärbung unterscheidet sich von Knotenfärbung: Der Satz von Vizing schränkt sie ein

## Siehe auch {#see-also}

- [[network-flow]] - bipartites Matching, verwandt mit bipartiter Färbung
- [[eulerian-hamiltonian-paths]] - ungerade Kreise treten in beiden Kontexten auf
- [[complexity-classes]] - k-Färbung (k >= 3) ist NP-vollständig
