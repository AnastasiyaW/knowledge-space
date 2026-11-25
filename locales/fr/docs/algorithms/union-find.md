---
title: "Union-Find (ensembles disjoints)"
category: data-structures
tags: [algorithms, data-structures, union-find, disjoint-set, connected-components]
level: 3
source_sha256: 570aee2abeae5c2b7602c1b43e8da8d81d568945c49e595b32e78a2b8e5512c3
translation: machine
translated_at: '2026-10-24'
---
# Union-Find (ensembles disjoints) {#union-find-disjoint-set-union}

Union-Find maintient une collection d'ensembles disjoints, avec des opérations quasi à temps constant pour fusionner des ensembles et déterminer à quel ensemble appartient un élément. Indispensable pour l'algorithme de Kruskal (arbre couvrant de poids minimal), le calcul des composantes connexes et la détection de cycles.

## Points clés {#key-facts}

- **find(x)** : trouve la racine (représentant) de l'ensemble contenant x
- **union(x, y)** : fusionne les ensembles contenant x et y
- Avec compression de chemin + union par rang : O(alpha(n)) amorti par opération
- alpha(n) = fonction inverse d'Ackermann, effectivement O(1) pour toute valeur pratique de n (alpha(n) <= 4 pour n < 10^80)
- Espace : O(n)

## Motifs {#patterns}

### Implémentation {#implementation}

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

### Find itératif avec division de chemin {#iterative-find-with-path-halving}

```python
def find(self, x):
    while self.parent[x] != x:
        self.parent[x] = self.parent[self.parent[x]]  # path halving
        x = self.parent[x]
    return x
```

La division de chemin (itérative) est plus simple et présente les mêmes performances asymptotiques que la compression de chemin complète (récursive).

### Détection de cycle dans un graphe non orienté {#cycle-detection-in-undirected-graph}

```python
def has_cycle(vertices, edges):
    uf = UnionFind(len(vertices))
    for u, v in edges:
        if not uf.union(u, v):
            return True  # u and v already connected = cycle
    return False
```

### Comptage des composantes connexes {#count-connected-components}

```python
def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return len(set(uf.find(i) for i in range(n)))
```

## Techniques d'optimisation {#optimization-techniques}

| Technique | Effet |
|-----------|--------|
| Compression de chemin | Aplatit l'arbre pendant le find : tous les nœuds pointent vers la racine |
| Union par rang | Rattache l'arbre le moins haut sous le plus haut : limite la hauteur à O(log n) |
| Les deux combinées | O(alpha(n)) amorti par opération |
| Aucune des deux | O(n) au pire par opération (chaîne dégénérée) |

## Pièges {#gotchas}

- Sans compression de chemin, find peut coûter O(n) sur une chaîne dégénérée
- L'union par rang seul donne O(log n) par find
- `union` renvoie False lorsque les éléments sont déjà dans le même ensemble : utile pour la détection de cycles
- Le rang est une borne supérieure de la hauteur, et non la hauteur exacte (la compression de chemin ne met pas le rang à jour)
- Pour les graphes peu denses, Union-Find est plus efficace que DFS/BFS pour les requêtes de connectivité sur des graphes dynamiques (arêtes ajoutées au fil du temps)

## Voir aussi {#see-also}

- [[minimum-spanning-trees]] - l'algorithme de Kruskal utilise Union-Find
- [[graph-representation]] - Union-Find comme alternative pour la connectivité dynamique
- [[graph-traversal-bfs-dfs]] - alternative pour les requêtes de connectivité statiques
