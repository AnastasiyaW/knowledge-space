---
title: "Arbres couvrants de poids minimal"
category: algorithms
tags: [algorithms, graphs, MST, prim, kruskal, union-find, greedy]
level: 3
source_sha256: ea609d9e206f44d6c4f78dcc35b4ad835800f12b6b0deabf6d98fd7b41f0b8b4
translation: machine
translated_at: '2026-10-24'
---
# Arbres couvrants de poids minimal {#minimum-spanning-trees}

Un arbre couvrant de poids minimal (MST) d'un graphe non orienté, pondéré et connexe est un arbre couvrant dont la somme des poids des arêtes est minimale. Deux algorithmes classiques : celui de Prim (faire croître l'arbre de manière gloutonne) et celui de Kruskal (fusionner les composantes par l'arête la moins coûteuse). Les deux sont gloutons et reposent sur la propriété de coupe.

## Points clés {#key-facts}

- Arbre couvrant : sous-graphe contenant les |V| sommets, connexe, acyclique, comportant exactement |V|-1 arêtes
- Le MST n'est PAS unique si plusieurs arêtes ont le même poids
- **Propriété de coupe** : pour toute coupe, l'arête de poids minimal traversant la coupe appartient à au moins un MST
- Pour trouver N'IMPORTE QUEL arbre couvrant : exécuter un BFS/DFS et conserver les arêtes de l'arbre
- Prim : O(|E| log |V|) avec un tas binaire, O(|V|^2) avec une matrice
- Kruskal : O(|E| log |E|) = O(|E| log |V|), dominé par le tri

## Prim contre Kruskal {#prims-vs-kruskals}

| | Prim | Kruskal |
|-|--------|----------|
| Structure de données | File de priorité | Union-Find + arêtes triées |
| Idéal pour | Graphes denses | Graphes creux |
| Approche | Fait croître un arbre unique | Fusionne des composantes |
| Graphe dense | O(\|V\|^2) avec matrice | O(\|E\| log \|V\|) = O(\|V\|^2 log \|V\|) |
| Graphe creux | O(\|E\| log \|V\|) | O(\|E\| log \|V\|) ~ O(\|V\| log \|V\|) |

## Schémas {#patterns}

### Algorithme de Prim {#prims-algorithm}

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

### Algorithme de Kruskal {#kruskals-algorithm}

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

### Coût minimal pour relier des points {#min-cost-to-connect-points}

Étant donnés n points, les relier tous avec une distance totale minimale. Il s'agit d'un MST sur un graphe complet.

- Construire les O(n^2) arêtes avec leurs distances
- Pour les graphes complets (denses), Prim avec une matrice en O(n^2) est plus simple

## Pièges {#gotchas}

- Le MST ne concerne que les graphes NON ORIENTÉS. Pour les graphes orientés, utiliser une arborescence couvrante de poids minimal (algorithme d'Edmonds)
- MST != arbre des plus courts chemins. L'arbre des plus courts chemins de Dijkstra minimise les chemins individuels, le MST minimise le poids total
- Prim ne peut pas détecter les graphes déconnectés (il ne trouve que le MST de la composante de départ)
- Kruskal peut détecter un graphe déconnecté : si le MST comporte moins de |V|-1 arêtes, le graphe est déconnecté
- Un arrêt anticipé de Kruskal dès que |V|-1 arêtes sont trouvées évite des itérations inutiles

## Voir aussi {#see-also}

- [[union-find]] - structure de données d'ensembles disjoints utilisée par Kruskal
- [[shortest-path-algorithms]] - MST contre arbre des plus courts chemins
- [[graph-representation]] - la complexité de Prim dépend de la représentation
- [[graph-traversal-bfs-dfs]] - BFS/DFS trouve un arbre couvrant quelconque
