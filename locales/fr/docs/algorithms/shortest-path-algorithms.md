---
title: "Algorithmes de plus court chemin"
category: algorithms
tags: [algorithms, graphs, dijkstra, bellman-ford, floyd-warshall, shortest-path, weighted-graph]
level: 3
source_sha256: 9fab3eb23210cfcca83a906e1435f68c0328fb5580a53a27e3731b7dc5248ddd
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes de plus court chemin {#shortest-path-algorithms}

Algorithmes de recherche de plus courts chemins dans les graphes pondérés : BFS (non pondéré), Dijkstra (poids non négatifs), Bellman-Ford (gère les arêtes négatives), Floyd-Warshall (toutes paires), relaxation sur DAG, et l'algorithme de Johnson.

## Sélection de l'algorithme {#algorithm-selection}

| Condition | Algorithme | Complexité |
|-----------|----------|-----------|
| Non pondéré | BFS | O(\|V\| + \|E\|) |
| Poids non négatifs, source unique | Dijkstra | O((\|V\|+\|E\|) log \|V\|) |
| Arêtes négatives, source unique | Bellman-Ford | O(\|V\|\|E\|) |
| DAG, poids quelconques, source unique | DP topologique | O(\|V\| + \|E\|) |
| Toutes paires, pas d'arêtes négatives | Dijkstra depuis chaque sommet | O(\|V\|(\|V\|+\|E\|) log \|V\|) |
| Toutes paires, arêtes négatives, graphe dense | Floyd-Warshall | O(\|V\|^3) |
| Toutes paires, arêtes négatives, graphe creux | Johnson | O(\|V\|^2 log \|V\| + \|V\|\|E\|) |
| Graphe dense, pas d'arêtes négatives | Dijkstra avec matrice | O(\|V\|^2) |

## Points clés {#key-facts}

- **Cycle de poids négatif** : s'il est atteignable depuis la source, aucun plus court chemin bien défini n'existe
- Dijkstra ÉCHOUE en présence d'arêtes négatives : l'hypothèse gloutonne ne tient plus
- Floyd-Warshall détecte les cycles négatifs : dist[i][i] < 0 après exécution
- Le plus court chemin sur DAG est l'algorithme mono-source le plus rapide lorsque le graphe est acyclique

## Schémas {#patterns}

### BFS - Non pondéré : O(|V| + |E|) {#bfs-unweighted-ov-e}

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

### Dijkstra - Poids non négatifs {#dijkstra-non-negative-weights}

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

**Pourquoi l'approche gloutonne fonctionne :** lorsque le sommet u est extrait, dist[u] est optimal. Tout autre chemin passerait par un sommet à distance plus grande (tous les poids sont >= 0).

**Variantes de complexité :**
- Tas binaire : O((|V| + |E|) log |V|)
- Tas de Fibonacci : O(|E| + |V| log |V|)
- Matrice d'adjacence, sans tas : O(|V|^2) - préférable pour les graphes denses

### Bellman-Ford - Gère les arêtes négatives {#bellman-ford-handles-negative-edges}

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

**Pourquoi |V|-1 itérations :** un plus court chemin comporte au plus |V|-1 arêtes (aucun sommet répété). L'itération k donne le plus court chemin utilisant au plus k arêtes.

### Floyd-Warshall - Toutes paires : O(|V|^3) {#floyd-warshall-all-pairs-ov3}

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

### Plus court chemin sur DAG - O(|V| + |E|) {#dag-shortest-path-ov-e}

Parcourir les sommets dans l'ordre topologique. Gère les poids négatifs.

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

### Algorithme de Johnson - Toutes paires avec arêtes négatives {#johnsons-algorithm-all-pairs-with-negative-edges}

1. Ajouter un nouveau sommet s avec des arêtes de poids 0 vers tous les sommets
2. Exécuter Bellman-Ford depuis s pour obtenir la fonction potentiel h[v]
3. Repondérer : w'(u,v) = w(u,v) + h[u] - h[v] >= 0
4. Exécuter Dijkstra depuis chaque sommet sur le graphe repondéré
5. Restaurer les distances : dist(u,v) = dist'(u,v) - h[u] + h[v]

Préférable à Floyd-Warshall pour les graphes creux.

## Pièges {#gotchas}

- La condition `if d > dist[vertex]: continue` de Dijkstra est essentielle à la correction avec suppression paresseuse (entrées obsolètes dans le tas)
- Détection de cycle négatif avec Bellman-Ford : si UNE arête est encore relâchable après |V|-1 tours, un cycle existe
- Dans Floyd-Warshall, la boucle externe doit être celle sur k (sommet intermédiaire), puis i, puis j
- Le plus court chemin sur DAG nécessite d'abord un tri topologique - échoue sur les graphes cycliques
- Pour les requêtes sur une seule paire, tous ces algorithmes calculent tout de même la source unique (aucune méthode générale connue plus rapide)

## Voir aussi {#see-also}

- [[graph-traversal-bfs-dfs]] - BFS pour les plus courts chemins non pondérés
- [[topological-sort]] - nécessaire pour le plus court chemin sur DAG
- [[graph-representation]] - la complexité dépend de la représentation
- [[minimum-spanning-trees]] - optimisation de graphe apparentée (l'ABM n'est pas un arbre de plus court chemin)
