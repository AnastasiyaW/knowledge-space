---
title: "Graph-Darstellung"
category: data-structures
tags: [algorithms, graphs, adjacency-list, adjacency-matrix, data-structures]
level: 3
source_sha256: a7b335f9ec39416e0a8bc4e0cfa2230c9715b875fa0bf05e231117937ea8b982
translation: machine
translated_at: '2026-10-24'
---
# Graph-Darstellung {#graph-representation}

Graphen lassen sich als Kantenlisten, Adjazenzlisten oder Adjazenzmatrizen darstellen. Die Wahl hängt von der Dichte des Graphen und davon ab, welche Operationen am wichtigsten sind. Adjazenzlisten sind der Standard für dünn besetzte Graphen; Matrizen eignen sich für dicht besetzte Graphen, die O(1)-Kantenprüfungen benötigen.

## Wichtige Fakten {#key-facts}

- **Kantenliste**: Speichert (src, dest)-Tupel. Das Finden von Nachbarn kostet O(|E|) – wird selten allein verwendet
- **Adjazenzliste**: Ordnet jedem Knoten seine Nachbarn zu. Speicherbedarf O(|V| + |E|). Am häufigsten verwendet
- **Adjazenzmatrix**: n x n-Matrix. Speicherbedarf O(|V|^2). O(1) für Kantenprüfung, aber O(|V|) zum Auflisten der Nachbarn
- Ein Graph mit n Knoten hat höchstens n(n-1)/2 Kanten (ungerichtet) bzw. n(n-1) (gerichtet)

## Zentrale Terminologie {#core-terminology}

| Begriff | Definition |
|---------|-----------|
| Ordnung | Anzahl der Knoten \|V\| |
| Größe | Anzahl der Kanten \|E\| |
| Grad | Anzahl der Kanten an einem Knoten (Eingangsgrad + Ausgangsgrad bei gerichteten Graphen) |
| Dünn besetzt | \|E\| << \|V\|^2 |
| Dicht besetzt | \|E\| nahe \|V\|^2 |
| DAG | Gerichteter azyklischer Graph (Directed Acyclic Graph) |
| Vollständiger Graph | Jedes Knotenpaar ist verbunden. Größe = \|V\|(\|V\|-1)/2 |
| Bipartit | Knoten sind in zwei Mengen aufgeteilt, Kanten nur zwischen den Mengen |

## Graphtypen {#graph-types}

| Typ | Definition |
|-----|-----------|
| Einfacher Graph | Keine Schleifen, keine Mehrfachkanten |
| Multigraph | Mehrere Kanten zwischen demselben Knotenpaar erlaubt |
| Vollständiger Graph | Jedes Knotenpaar ist verbunden |
| Bipartit | Zweiteilung in Mengen, Kanten nur zwischen den Mengen |
| Regulärer Graph | Alle Knoten haben denselben Grad |

## Komplexität der Operationen {#operation-complexity}

| Operation | Adjazenzliste | Adjazenzmatrix |
|-----------|---------------|-----------------|
| Speicher | O(\|V\| + \|E\|) | O(\|V\|^2) |
| Knoten hinzufügen | O(1) | O(\|V\|^2) Neuaufbau |
| Knoten entfernen | O(\|V\| + \|E\|) | O(\|V\|^2) |
| Kante hinzufügen | O(1) | O(1) |
| Kante entfernen | O(degree(u)) | O(1) |
| Kante prüfen | O(degree(u)) | O(1) |
| Nachbarn abrufen | O(degree(u)) | O(\|V\|) |

## Muster {#patterns}

### Implementierung der Adjazenzliste {#adjacency-list-implementation}

```python
class Graph:
    def __init__(self):
        self.adj_list = {}  # vertex -> list of neighbors

    def add_vertex(self, u):
        if u not in self.adj_list:
            self.adj_list[u] = []

    def add_edge(self, u, v):  # directed
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].append(v)

    def add_edge_undirected(self, u, v):
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)

    def add_edge_weighted(self, u, v, w):  # directed weighted
        if u in self.adj_list and v in self.adj_list:
            self.adj_list[u].append((v, w))

    def remove_vertex(self, u):
        if u in self.adj_list:
            del self.adj_list[u]
            for v in self.adj_list:
                if u in self.adj_list[v]:
                    self.adj_list[v].remove(u)

    def check_edge(self, u, v):
        return u in self.adj_list and v in self.adj_list[u]

    def build(self, vertices, edges):
        for u in vertices:
            self.add_vertex(u)
        for u, v in edges:
            self.add_edge(u, v)
```

Verwende set statt list für eine O(1)-Prüfung, ob eine Kante existiert, auf Kosten von zusätzlichem Speicher.

### Implementierung der Adjazenzmatrix {#adjacency-matrix-implementation}

```python
class GraphMatrix:
    def __init__(self):
        self.adj_mat = []

    def add_vertex(self):
        for row in self.adj_mat:
            row.append(0)
        n = len(self.adj_mat) + 1
        self.adj_mat.append([0] * n)

    def add_edge(self, u, v):
        self.adj_mat[u][v] = 1  # undirected: also self.adj_mat[v][u] = 1

    def edge_exists(self, u, v):
        return self.adj_mat[u][v] == 1

    def get_neighbors(self, u):
        return [v for v in range(len(self.adj_mat[u])) if self.adj_mat[u][v] == 1]
```

## Zusammenhang {#connectivity}

| Konzept | Definition |
|---------|-----------|
| Walk | Folge benachbarter Knoten, Wiederholungen erlaubt |
| Trail | Walk ohne wiederholte Kanten |
| Path | Walk ohne wiederholte Knoten |
| Zyklus | Geschlossener Pfad |
| Zusammenhängend | Jedes Knotenpaar ist erreichbar (ungerichtet) |
| Stark zusammenhängend | Gerichteter Pfad zwischen jedem geordneten Knotenpaar |
| Schwach zusammenhängend | Zusammenhängend, wenn Kantenrichtungen ignoriert werden |

## Fallstricke {#gotchas}

- Wähle Adjazenzlisten für dünn besetzte Graphen (die meisten realen Graphen)
- Wähle Adjazenzmatrizen für dicht besetzte Graphen oder wenn die O(1)-Kantenprüfung entscheidend ist
- Für nicht-ganzzahlige Knotenbezeichnungen verwende eine Hash-Map, um Bezeichnungen auf Indizes abzubilden
- Das Entfernen eines Knotens aus einer Adjazenzliste erfordert das Durchsuchen aller Listen: O(|V| + |E|)
- Matrix-Knoten löschen: Mit der letzten Zeile/Spalte tauschen und dann entfernen (pop), um einen Neuaufbau zu vermeiden

## Siehe auch {#see-also}

- [[graph-traversal-bfs-dfs]] - DFS und BFS auf diesen Darstellungen
- [[shortest-path-algorithms]] - verschiedene Algorithmen eignen sich für verschiedene Darstellungen
- [[minimum-spanning-trees]] - Prim mit Matrix O(|V|^2) vs. mit Heap O(|E| log |V|)
