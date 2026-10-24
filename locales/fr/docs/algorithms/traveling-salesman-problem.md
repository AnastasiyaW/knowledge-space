---
title: "Problème du voyageur de commerce (TSP)"
category: algorithms
tags: [algorithms, graphs, TSP, NP-hard, approximation, optimization, bitmask-dp]
level: 3
source_sha256: 072ddc74b5aef3cc89604d7ed095c847783a657b464d05aefb509b1711730205
translation: machine
translated_at: '2026-10-24'
---
# Problème du voyageur de commerce (TSP) {#traveling-salesman-problem-tsp}

Trouver le trajet le plus court visitant chaque ville exactement une fois et revenant à l'origine. NP-difficile - aucun algorithme exact polynomial connu. Les approches pratiques vont de la force brute (n <= 10) à la programmation dynamique (n <= 20) jusqu'aux heuristiques (n > 20).

## Faits clés {#key-facts}

- **Force brute** : O(n!) - essayer toutes les permutations
- **DP de Held-Karp** : O(2^n * n^2) en temps, O(2^n * n) en espace - DP sur masques de bits
- **Heuristique du plus proche voisin** : O(n^2), généralement 20 à 25 % au-dessus de l'optimum
- **Christofides** : O(n^3), garanti <= 1,5 fois l'optimum pour le TSP métrique
- **Recherche locale 2-opt** : amélioration itérative par inversion de segments
- TSP != plus court chemin : il faut visiter TOUTES les villes, pas seulement aller de A à B

## Variantes du TSP {#tsp-variants}

| Variante | Définition |
|---------|-----------|
| Symétrique | dist(A,B) = dist(B,A), non orienté |
| Asymétrique | Orienté, les distances peuvent différer selon le sens |
| Métrique | Symétrique + inégalité triangulaire |
| Avec inégalité triangulaire | dist(A,C) <= dist(A,B) + dist(B,C) |

## Recommandations pratiques {#practical-guidance}

| n | Approche |
|---|---------|
| <= 10 | Force brute O(n!) |
| <= 20 | DP de Held-Karp O(2^n * n^2) |
| <= 100 | Plus proche voisin + 2-opt |
| > 100 | Christofides, LKH ou métaheuristiques |

## Schémas {#patterns}

### Force brute - O(n!) {#brute-force-on}

```python
from itertools import permutations

def tsp_brute_force(dist, start=0):
    cities = [i for i in range(len(dist)) if i != start]
    min_cost = float('inf')
    best_route = None
    for perm in permutations(cities):
        route = [start] + list(perm) + [start]
        cost = sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))
        if cost < min_cost:
            min_cost = cost
            best_route = route
    return best_route, min_cost
```

### DP de Held-Karp - O(2^n * n^2) {#held-karp-dp-o2n-n2}

DP sur masques de bits. État : dp[S][v] = coût minimal pour visiter toutes les villes du masque S, en terminant à la ville v.

```python
def tsp_dp(dist):
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0, visited = {0}

    for S in range(1 << n):
        for v in range(n):
            if dp[S][v] == INF or not (S >> v & 1):
                continue
            for u in range(n):
                if S >> u & 1:
                    continue  # already visited
                new_S = S | (1 << u)
                dp[new_S][u] = min(dp[new_S][u], dp[S][v] + dist[v][u])

    full = (1 << n) - 1
    return min(dp[full][v] + dist[v][0] for v in range(1, n))
```

Pour n=20 : environ 20 M d'états - faisable. Pour n=30 : irréaliste.

### Heuristique du plus proche voisin - O(n^2) {#nearest-neighbor-heuristic-on2}

```python
def nearest_neighbor(dist, start=0):
    n = len(dist)
    visited = [False] * n
    route = [start]
    visited[start] = True
    current = start

    for _ in range(n - 1):
        nearest = min(
            (j for j in range(n) if not visited[j]),
            key=lambda j: dist[current][j]
        )
        route.append(nearest)
        visited[nearest] = True
        current = nearest

    route.append(start)
    return route
```

### Recherche locale 2-opt {#2-opt-local-search}

```python
def two_opt(route, dist):
    improved = True
    while improved:
        improved = False
        n = len(route) - 1
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                if tour_length(new_route, dist) < tour_length(route, dist):
                    route = new_route
                    improved = True
    return route
```

### Algorithme de Christofides (concept) {#christofides-algorithm-concept}

Pour le TSP métrique (inégalité triangulaire), garanti à 1,5 fois l'optimum :
1. Trouver l'arbre couvrant de poids minimal (MST)
2. Trouver un couplage parfait de poids minimal sur les sommets de degré impair
3. Combiner MST + couplage -> graphe eulérien
4. Trouver un circuit eulérien
5. Raccourcir les sommets répétés

## Problèmes connexes {#related-problems}

- **Superchaîne la plus courte** : chaîne la plus courte contenant toutes les chaînes données comme sous-chaînes. Équivalent au TSP sur le graphe de recouvrement. NP-difficile.

## Pièges à éviter {#gotchas}

- Le TSP ne peut pas être décomposé en sous-problèmes indépendants de plus court chemin
- Le plus proche voisin peut produire des trajets très médiocres avec des motifs de « retour en arrière »
- Le 2-opt converge vers un minimum LOCAL - plusieurs redémarrages aléatoires améliorent les résultats
- Christofides ne fonctionne qu'avec l'inégalité triangulaire (TSP métrique)
- La DP sur masques de bits nécessite un entier de masque - Python gère des entiers de taille arbitraire, mais la mémoire est la limite

## Voir aussi {#see-also}

- [[eulerian-hamiltonian-paths]] - TSP = cycle hamiltonien de poids minimal
- [[minimum-spanning-trees]] - MST utilisé dans l'approximation de Christofides
- [[complexity-classes]] - le TSP est NP-difficile
- [[dp-optimization-problems]] - technique de DP sur masques de bits
