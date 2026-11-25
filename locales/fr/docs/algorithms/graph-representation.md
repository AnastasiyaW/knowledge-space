---
title: "Représentation des graphes"
category: data-structures
tags: [algorithms, graphs, adjacency-list, adjacency-matrix, data-structures]
level: 3
source_sha256: a7b335f9ec39416e0a8bc4e0cfa2230c9715b875fa0bf05e231117937ea8b982
translation: machine
translated_at: '2026-10-24'
---
# Représentation des graphes {#graph-representation}

Les graphes peuvent être représentés par des listes d'arêtes, des listes d'adjacence ou des matrices d'adjacence. Le choix dépend de la densité du graphe et des opérations les plus importantes. Les listes d'adjacence sont le choix par défaut pour les graphes creux ; les matrices conviennent aux graphes denses qui nécessitent des vérifications d'arêtes en O(1).

## Faits essentiels {#key-facts}

- **Liste d'arêtes** : Stocker des tuples (src, dest). Trouver les voisins est en O(|E|), ce qui la rend rarement utilisée seule
- **Liste d'adjacence** : Associer chaque sommet à ses voisins. Espace en O(|V| + |E|). C'est la plus courante
- **Matrice d'adjacence** : Matrice n x n. Espace en O(|V|^2). Vérification d'une arête en O(1), mais lister les voisins en O(|V|)
- Un graphe à n sommets possède au plus n(n-1)/2 arêtes (non orienté) ou n(n-1) arêtes (orienté)

## Terminologie de base {#core-terminology}

| Terme | Définition |
|------|-----------|
| Ordre | Nombre de sommets \|V\| |
| Taille | Nombre d'arêtes \|E\| |
| Degré | Nombre d'arêtes incidentes à un sommet (degré entrant + degré sortant pour un graphe orienté) |
| Creux | \|E\| << \|V\|^2 |
| Dense | \|E\| proche de \|V\|^2 |
| DAG | Graphe orienté acyclique (Directed Acyclic Graph) |
| Graphe complet | Chaque paire de sommets est reliée. Taille = \|V\|(\|V\|-1)/2 |
| Biparti | Sommets répartis en deux ensembles, arêtes uniquement entre les ensembles |

## Types de graphes {#graph-types}

| Type | Définition |
|------|-----------|
| Graphe simple | Sans boucles ni arêtes multiples |
| Multigraphe | Plusieurs arêtes autorisées entre une même paire de sommets |
| Graphe complet | Chaque paire de sommets est reliée |
| Biparti | Partition en deux ensembles, arêtes uniquement entre les ensembles |
| Graphe régulier | Tous les sommets ont le même degré |

## Complexité des opérations {#operation-complexity}

| Opération | Liste d'adjacence | Matrice d'adjacence |
|-----------|---------------|-----------------|
| Espace | O(\|V\| + \|E\|) | O(\|V\|^2) |
| Ajouter un sommet | O(1) | O(\|V\|^2) reconstruction |
| Supprimer un sommet | O(\|V\| + \|E\|) | O(\|V\|^2) |
| Ajouter une arête | O(1) | O(1) |
| Supprimer une arête | O(degree(u)) | O(1) |
| Vérifier une arête | O(degree(u)) | O(1) |
| Obtenir les voisins | O(degree(u)) | O(\|V\|) |

## Modèles {#patterns}

### Implémentation par liste d'adjacence {#adjacency-list-implementation}

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

Utiliser un set au lieu d'une liste pour vérifier l'existence d'une arête en O(1), au prix d'une mémoire supplémentaire.

### Implémentation par matrice d'adjacence {#adjacency-matrix-implementation}

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

## Connectivité {#connectivity}

| Concept | Définition |
|---------|-----------|
| Marche | Séquence de sommets adjacents, les répétitions sont autorisées |
| Piste | Marche sans arête répétée |
| Chemin | Marche sans sommet répété |
| Cycle | Chemin fermé |
| Connexe | Chaque paire de sommets est atteignable (non orienté) |
| Fortement connexe | Chemin orienté entre chaque couple ordonné de sommets |
| Faiblement connexe | Connexe en ignorant le sens des arêtes |

## Pièges à éviter {#gotchas}

- Choisir une liste d'adjacence pour les graphes creux (la plupart des graphes réels)
- Choisir une matrice d'adjacence pour les graphes denses ou lorsque la vérification d'arête en O(1) est critique
- Pour des étiquettes de sommets qui ne sont pas des entiers, utiliser une table de hachage pour associer les étiquettes à des indices
- Supprimer un sommet d'une liste d'adjacence impose de parcourir toutes les listes : O(|V| + |E|)
- Supprimer un sommet d'une matrice : échanger avec la dernière ligne et la dernière colonne, puis retirer l'élément, pour éviter une reconstruction

## Voir aussi {#see-also}

- [[graph-traversal-bfs-dfs]] - DFS et BFS sur ces représentations
- [[shortest-path-algorithms]] - différents algorithmes conviennent à différentes représentations
- [[minimum-spanning-trees]] - Prim avec matrice en O(|V|^2) contre Prim avec tas en O(|E| log |V|)
