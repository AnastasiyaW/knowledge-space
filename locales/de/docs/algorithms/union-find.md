---
title: "Union-Find (Disjunkte Mengen-Vereinigung)"
category: data-structures
tags: [algorithms, data-structures, union-find, disjoint-set, connected-components]
level: 3
source_sha256: 570aee2abeae5c2b7602c1b43e8da8d81d568945c49e595b32e78a2b8e5512c3
translation: machine
translated_at: '2026-10-24'
---
# Union-Find (Disjunkte Mengen-Vereinigung) {#union-find-disjoint-set-union}

Union-Find verwaltet eine Sammlung disjunkter Mengen mit nahezu konstanter Laufzeit für das Zusammenführen von Mengen und für die Ermittlung der Menge, zu der ein Element gehört. Unverzichtbar für Kruskals MST, zusammenhängende Komponenten und Zykluserkennung.

## Key Facts {#key-facts}

- **find(x)**: Ermittelt Wurzel/Repräsentanten der Menge, die x enthält
- **union(x, y)**: Führt die Mengen zusammen, die x und y enthalten
- Mit Pfadkompression + Union by Rank: O(alpha(n)) amortisiert pro Operation
- alpha(n) = inverse Ackermann-Funktion, für alle praktischen n effektiv O(1) (alpha(n) <= 4 für n < 10^80)
- Speicher: O(n)

## Patterns {#patterns}

### Implementation {#implementation}

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already same set
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
```

### Iterative Find with Path Halving {#iterative-find-with-path-halving}

```python
def find(self, x):
    while self.parent[x] != x:
        self.parent[x] = self.parent[self.parent[x]]  # path halving
        x = self.parent[x]
    return x
```

Path Halving (iterativ) ist einfacher und hat dieselbe asymptotische Laufzeit wie die vollständige Pfadkompression (rekursiv).

### Cycle Detection in Undirected Graph {#cycle-detection-in-undirected-graph}

```python
def has_cycle(vertices, edges):
    uf = UnionFind(len(vertices))
    for u, v in edges:
        if not uf.union(u, v):
            return True  # u and v already connected = cycle
    return False
```

### Count Connected Components {#count-connected-components}

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return len(set(uf.find(i) for i in range(n)))
```

## Optimization Techniques {#optimization-techniques}

| Technik | Wirkung |
|-----------|--------|
| Pfadkompression | Flacht den Baum während find ab – alle Knoten zeigen auf die Wurzel |
| Union by Rank | Hängt den kürzeren Baum unter den höheren – begrenzt die Höhe auf O(log n) |
| Beides kombiniert | Amortisiert O(alpha(n)) pro Operation |
| Keines von beiden | O(n) im schlechtesten Fall pro Operation (entarteter Pfad) |

## Gotchas {#gotchas}

- Ohne Pfadkompression kann find auf einer entarteten Kette O(n) benötigen
- Union by Rank allein ergibt O(log n) pro find
- `union` gibt False zurück, wenn die Elemente bereits in derselben Menge liegen – nützlich für die Zykluserkennung
- Der Rank ist eine obere Schranke für die Höhe, nicht die exakte Höhe (Pfadkompression aktualisiert den Rank nicht)
- Für dünn besetzte Graphen ist Union-Find bei Konnektivitätsabfragen auf dynamischen Graphen (Kanten werden im Laufe der Zeit hinzugefügt) effizienter als DFS/BFS

## See Also {#see-also}

- [[minimum-spanning-trees]] - Kruskals Algorithmus verwendet Union-Find
- [[graph-representation]] - Union-Find als Alternative für dynamische Konnektivität
- [[graph-traversal-bfs-dfs]] - Alternative für statische Konnektivitätsabfragen
