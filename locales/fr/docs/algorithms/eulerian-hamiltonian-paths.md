---
title: "Chemins eulériens et hamiltoniens"
category: algorithms
tags: [algorithms, graphs, eulerian, hamiltonian, hierholzer, backtracking]
level: 3
source_sha256: afae69f79b115a380b6aef5ce649481c59df124b741de243bd5d7a4ef5a618d7
translation: machine
translated_at: '2026-10-24'
---
# Chemins eulériens et hamiltoniens {#eulerian-and-hamiltonian-paths}

Les chemins eulériens parcourent chaque ARÊTE exactement une fois ; les chemins hamiltoniens parcourent chaque SOMMET exactement une fois. Les problèmes eulériens sont polynomiaux (conditions simples sur les degrés + algorithme de Hierholzer en O(|E|)). Les problèmes hamiltoniens sont NP-complets.

## Comparaison essentielle {#key-comparison}

| | Eulérien | Hamiltonien |
|-|----------|-------------|
| Ce qu'on parcourt | Chaque arête exactement une fois | Chaque sommet exactement une fois |
| Complexité de recherche | O(\|E\|) - polynomial | NP-complet |
| Conditions d'existence | Conditions simples sur les degrés | Pas de caractérisation simple |
| Algorithme | Hierholzer | Backtracking O(n!), DP O(2^n * n^2) |

## Conditions de chemin/circuit eulérien {#eulerian-trailcircuit-conditions}

### Graphe non orienté {#undirected-graph}

| Condition | Résultat |
|-----------|----------|
| Tous les sommets de degré non nul connexes ET tous de degré pair | Circuit eulérien **circuit** |
| Tous les sommets de degré non nul connexes ET exactement 2 sommets de degré impair | Chemin eulérien **chemin** (début/fin aux sommets impairs) |
| Plus de 2 sommets de degré impair | Pas de chemin eulérien |

### Graphe orienté {#directed-graph}

| Condition | Résultat |
|-----------|----------|
| Fortement connexe ET degré entrant == degré sortant pour tous | Circuit eulérien **circuit** |
| Faiblement connexe ET exactement un sommet avec sortant-entrant=1 (début), un avec entrant-sortant=1 (fin), les autres équilibrés | Chemin eulérien **chemin** |

## Schémas {#patterns}

### Vérifier un circuit eulérien (non orienté) {#check-eulerian-circuit-undirected}

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

### Algorithme de Hierholzer - O(|E|) {#hierholzers-algorithm-oe}

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

### Reconstituer un itinéraire (chemin eulérien orienté) {#reconstruct-itinerary-directed-eulerian-path}

Étant donné des billets d'avion, reconstituer l'itinéraire lexicographiquement minimal utilisant chaque billet exactement une fois.

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

### Chemin hamiltonien - Backtracking en O(n!) {#hamiltonian-path-backtracking-on}

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

### DP de Held-Karp pour le hamiltonien - O(2^n * n^2) {#held-karp-dp-for-hamiltonian-o2n-n2}

Meilleur que O(n!) pour une solution exacte. Voir [[traveling-salesman-problem]] pour l'implémentation de la DP par masque binaire.

## Faits clés {#key-facts}

- **Euler (1736)** : les sept ponts de Königsberg - premier résultat de la théorie des graphes
- **Théorème d'Ore** : si deg(u) + deg(v) >= n pour toute paire de sommets non adjacents, il existe un cycle hamiltonien (condition suffisante, non nécessaire)
- L'algorithme de Hierholzer suit glouton les arêtes jusqu'à être bloqué, puis revient en arrière pour trouver des extensions
- Origine historique de la théorie des graphes : peut-on traverser les 7 ponts exactement une fois ?

## Pièges {#gotchas}

- Eulérien = arêtes, hamiltonien = sommets : facile à confondre
- Pour les graphes non orientés, Hierholzer doit retirer les arêtes dans LES DEUX sens
- Pour le hamiltonien, il n'existe pas de condition simple (contrairement à l'eulérien) : il faut essayer ou utiliser la DP
- Chemin hamiltonien vs cycle : le chemin ne revient pas au départ, le cycle si
- Chemin eulérien avec 2 sommets de degré impair : il DOIT commencer à l'un et finir à l'autre

## Voir aussi {#see-also}

- [[traveling-salesman-problem]] - Cycle hamiltonien de poids minimal
- [[graph-traversal-bfs-dfs]] - DFS utilisé dans Hierholzer
- [[complexity-classes]] - Le chemin hamiltonien est NP-complet
