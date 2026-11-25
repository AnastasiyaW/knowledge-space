---
title: "Coloration de graphes"
category: algorithms
tags: [algorithms, graphs, coloring, chromatic-number, bipartite, NP-complete, scheduling]
level: 3
source_sha256: fbfa493a5a6d1e2d8519a98000058314e61e0b47353877c1bfb4d5bb3cf80bac
translation: machine
translated_at: '2026-10-24'
---
# Coloration de graphes {#graph-coloring}

La coloration de graphes attribue des couleurs aux sommets de manière à ce que deux sommets adjacents ne partagent jamais la même couleur. Le nombre chromatique chi(G) est le nombre minimal de couleurs nécessaires. La 2-coloration (bipartition) est polynomiale ; la k-coloration pour k >= 3 est NP-complète.

## Faits essentiels {#key-facts}

- **Nombre chromatique chi(G)** : nombre minimal de couleurs pour une coloration valide
- **2-colorable** si et seulement si biparti si et seulement si pas de cycle de longueur impaire - vérifiable en O(|V| + |E|)
- **k-colorable (k >= 3)** : NP-complet
- La coloration gloutonne utilise au plus Delta+1 couleurs (Delta = degré maximal)
- **Théorème de Brooks** : chi(G) <= Delta pour les graphes connexes qui ne sont ni complets ni des cycles impairs
- **Théorème de Vizing** (coloration d'arêtes) : chi'(G) vaut Delta ou Delta+1

## Applications {#applications}

- **Ordonnancement de ressources** : tâches qui se chevauchent représentées par des arêtes, couleurs = ressources (nombre minimal de voitures, de salles, etc.)
- **Allocation de registres** dans les compilateurs
- **Attribution de fréquences** dans les réseaux sans fil
- **Planification d'examens** : les examens en conflit nécessitent des créneaux horaires différents
- **Sudoku** : 9-coloration du graphe de contraintes (81 sommets, arêtes pour une même ligne/colonne/case)

## Schémas {#patterns}

### Vérification de bipartition (2-coloration) - O(|V| + |E|) {#bipartite-check-2-coloring-ov-e}

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

### Coloration gloutonne {#greedy-coloring}

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

Le résultat dépend de l'ordre des sommets. Elle ne garantit PAS le nombre chromatique.

### Heuristique de Welsh-Powell {#welsh-powell-heuristic}

Trier les sommets par degré décroissant avant la coloration gloutonne. Produit souvent de bons résultats (sans être optimaux).

```python
def welsh_powell(graph):
    order = sorted(graph.adj_list,
                   key=lambda v: len(graph.adj_list[v]), reverse=True)
    return greedy_coloring(graph, order)
```

### k-coloration exacte (retour sur trace) {#exact-k-coloring-backtracking}

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

## Concepts associés {#related-concepts}

| Concept | Définition |
|---------|-----------|
| Clique | Sous-ensemble de sommets deux à deux adjacents |
| Ensemble indépendant | Sous-ensemble sans deux sommets adjacents |
| Nombre de clique omega(G) | Taille de la plus grande clique. omega(G) <= chi(G) |
| Graphe parfait | omega(G) = chi(G). Inclut les graphes bipartis et les graphes cordaux |
| Coloration d'arêtes | Colorer les arêtes, deux arêtes partageant un sommet ne reçoivent pas la même couleur |

## Pièges à éviter {#gotchas}

- Le graphe complet K_n nécessite exactement n couleurs
- Cycle pair : chi = 2 ; cycle impair : chi = 3
- Le résultat de la coloration gloutonne dépend entièrement de l'ordre de traitement des sommets
- La vérification de bipartition gère les graphes non connexes : il faut démarrer depuis chaque sommet non coloré
- La coloration d'arêtes diffère de la coloration de sommets : le théorème de Vizing la borne

## Voir aussi {#see-also}

- [[network-flow]] - le couplage biparti est lié à la coloration bipartie
- [[eulerian-hamiltonian-paths]] - les cycles impairs apparaissent dans les deux contextes
- [[complexity-classes]] - la k-coloration (k >= 3) est NP-complète
