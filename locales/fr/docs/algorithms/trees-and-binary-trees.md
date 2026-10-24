---
title: "Arbres et arbres binaires"
category: data-structures
tags: [algorithms, data-structures, trees, binary-tree, traversal, BST]
level: 3
source_sha256: 61540834e7b25425599a9120f9e7fd5d8b0bbcd4abd24a8cc7a360ec5d91e33b
translation: machine
translated_at: '2026-10-24'
---
# Arbres et arbres binaires {#trees-and-binary-trees}

Un arbre est un graphe non orienté, connexe et acyclique. Un arbre à n sommets possède exactement n-1 arêtes. Les arbres binaires (chaque nœud a au plus 2 enfants) supportent quatre ordres de parcours : infixe, préfixe, postfixe et parcours par niveaux (BFS). Les arbres sont fondamentaux pour la recherche, le tri et les données hiérarchiques.

## Points clés {#key-facts}

- Un arbre à n sommets possède exactement n-1 arêtes
- Ce n'est pas un arbre si : il est déconnecté (même s'il est acyclique) ou s'il contient un cycle (même s'il est connexe)
- Une **forêt** est un graphe acyclique (chaque composante connexe est un arbre)
- **Parcours d'arbres binaires** : infixe (G-Racine-D), préfixe (Racine-G-D), postfixe (G-D-Racine), parcours par niveaux (BFS)
- Le parcours infixe d'un ABR donne l'ordre trié

## Terminologie {#terminology}

| Terme | Définition |
|------|-----------|
| Racine | Sommet du haut, sans parent |
| Parent | Sommet directement au-dessus |
| Enfant | Sommet directement en dessous |
| Feuille | Sans enfant (degré 1 en non orienté, demi-degré sortant 0 en arbre enraciné) |
| Profondeur | Distance à la racine (racine = profondeur 0) |
| Hauteur | Profondeur maximale de l'arbre |
| Sous-arbre | Un sommet et tous ses descendants |

## Motifs {#patterns}

### Nœud d'arbre binaire {#binary-tree-node}

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Parcours infixe (Gauche - Racine - Droite) {#inorder-traversal-left-root-right}

Pour un ABR : donne l'ordre trié.

```python
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)
```

### Parcours préfixe (Racine - Gauche - Droite) {#preorder-traversal-root-left-right}

Utilisé pour copier ou sérialiser un arbre.

```python
def preorder(root):
    if root:
        print(root.val)
        preorder(root.left)
        preorder(root.right)
```

### Parcours postfixe (Gauche - Droite - Racine) {#postorder-traversal-left-right-root}

Utilisé pour supprimer un arbre, calculer la taille des sous-arbres.

```python
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val)
```

### Parcours par niveaux (BFS) {#level-order-traversal-bfs}

```python
from collections import deque

def level_order(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
```

### Conversion d'un graphe en arbre enraciné {#graph-to-rooted-tree-conversion}

```python
def build_tree(adj_list, root, parent=None):
    node = TreeNode(root)
    for child in adj_list[root]:
        if child != parent:
            node.children.append(build_tree(adj_list, child, root))
    return node
```

### Nœuds à distance K {#nodes-at-distance-k}

Convertir l'arbre binaire en graphe non orienté, puis effectuer un BFS depuis la cible sur k étapes.

```python
from collections import defaultdict, deque

def distance_k(root, target, k):
    graph = defaultdict(list)
    def build(node, parent):
        if node:
            if parent:
                graph[node.val].append(parent.val)
                graph[parent.val].append(node.val)
            build(node.left, node)
            build(node.right, node)
    build(root, None)

    visited = {target.val}
    queue = deque([(target.val, 0)])
    result = []
    while queue:
        node, dist = queue.popleft()
        if dist == k:
            result.append(node)
        elif dist < k:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
    return result
```

### Arbre couvrant {#spanning-tree}

Un arbre couvrant d'un graphe connexe contient tous les sommets, est connexe, acyclique et possède |V|-1 arêtes. On en obtient un en exécutant un BFS ou un DFS et en ne conservant que les arêtes de l'arbre.

## Pièges {#gotchas}

- Tout graphe non orienté, connexe et acyclique peut être enraciné en N'IMPORTE QUEL sommet
- L'ordre de parcours compte : le parcours infixe ne donne un résultat trié que sur les ABR
- Le parcours par niveaux (BFS) nécessite une file, et non la récursivité (bien qu'un parcours récursif par niveaux existe, il est moins naturel)
- Les problèmes de « distance K » sur les arbres nécessitent souvent de convertir d'abord en graphe non orienté
- Profondeur et hauteur : la profondeur se mesure du haut vers le bas (racine = 0), la hauteur du bas vers le haut (feuille = 0)

## Voir aussi {#see-also}

- [[graph-traversal-bfs-dfs]] - les parcours d'arbres sont des cas particuliers du parcours de graphe
- [[minimum-spanning-trees]] - arbre couvrant minimal des graphes pondérés
- [[graph-representation]] - les arbres comme cas particuliers de graphes
