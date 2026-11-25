---
title: "Tri topologique"
category: algorithms
tags: [algorithms, graphs, topological-sort, DAG, scheduling, kahn]
level: 3
source_sha256: b8c8b53c001f48b9d6894430ceae2714c9037957b5625e309325396b0a647510
translation: machine
translated_at: '2026-10-24'
---
# Tri topologique {#topological-sort}

Un ordre topologique d'un DAG (graphe orienté acyclique, *Directed Acyclic Graph*) est un ordonnancement linéaire des sommets tel que, pour chaque arête u -> v, u apparaît avant v. Ce n'est possible que sur les DAG : un cycle crée une contradiction. Deux algorithmes existent : l'approche basée sur le DFS (inversion du parcours en post-ordre) et celui de Kahn (BFS avec suivi des degrés entrants).

## Points clés {#key-facts}

- Ne fonctionne que sur les DAG : la présence d'un cycle signifie qu'aucun ordre valide n'existe
- Non unique : plusieurs ordres valides peuvent exister
- Les deux algorithmes : O(|V| + |E|) en temps et en espace
- Applications : prérequis de cours, ordonnancement de tâches, systèmes de build, ordre de chargement des tables de base de données, chemin critique

## Comparaison des algorithmes {#algorithm-comparison}

| | DFS | Kahn (BFS) |
|-|-----------|---------------------|
| Détection de l'ordre | DFS en post-ordre, inversé | Par degré entrant |
| Détection de cycle | Suivi des nœuds « dans la pile » (nœuds gris) | Taille de la sortie < \|V\| |
| Plusieurs ordres valides | Tout ordre de DFS | Contrôlable via une file de priorité |
| Implémentation | Récursion plus simple | Suivi explicite des degrés entrants |

## Modèles {#patterns}

### Tri topologique basé sur le DFS {#dfs-based-topological-sort}

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

Pourquoi cela fonctionne : lorsque l'on ajoute le sommet u, tous les sommets accessibles depuis u ont déjà été ajoutés. Après inversion, u précède tout ce vers quoi il pointe.

### Algorithme de Kahn (basé sur le BFS) {#kahns-algorithm-bfs-based}

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

### Chemin critique (temps minimal pour l'ensemble des tâches) {#critical-path-minimum-time-for-all-tasks}

Étant donné un graphe de tâches avec leurs durées, on trouve le temps d'achèvement minimal à l'aide d'un ordre topologique et de la programmation dynamique.

```python
def critical_path(graph):
    order = topological_sort_kahn(graph)
    earliest = {v: 0 for v in graph.adj_list}
    for u in order:
        for v, weight in graph.adj_list[u]:
            earliest[v] = max(earliest[v], earliest[u] + weight)
    return max(earliest.values())  # minimum total time
```

Le chemin critique correspond au plus long chemin dans le DAG, c'est-à-dire au temps d'achèvement minimal.

### Plus court chemin dans un DAG {#shortest-path-in-dag}

On parcourt les sommets dans l'ordre topologique et on relâche les arêtes. Complexité O(|V| + |E|), gère les poids négatifs.

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

## Pièges {#gotchas}

- L'approche basée sur le DFS nécessite d'INVERSER le post-ordre : oublier cette inversion donne un ordre incorrect
- Détection de cycle avec Kahn : si la sortie contient moins de sommets que le graphe, il existe un cycle
- Plusieurs ordres valides sont possibles : ne pas supposer un ordre particulier
- Non applicable aux graphes non orientés ni aux graphes contenant des cycles
- L'ordonnancement de cours utilise le tri topologique mais peut aussi nécessiter une contrainte sur les cours suivis en parallèle (problème distinct)

## Voir aussi {#see-also}

- [[graph-traversal-bfs-dfs]] - fondamentaux du DFS et du BFS utilisés ici
- [[shortest-path-algorithms]] - plus court chemin dans un DAG comme application
- [[graph-representation]] - liste d'adjacence pour le tri topologique
