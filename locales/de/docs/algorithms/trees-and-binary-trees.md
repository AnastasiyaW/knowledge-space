---
title: "Bäume und Binärbäume"
category: data-structures
tags: [algorithms, data-structures, trees, binary-tree, traversal, BST]
level: 3
source_sha256: 61540834e7b25425599a9120f9e7fd5d8b0bbcd4abd24a8cc7a360ec5d91e33b
translation: machine
translated_at: '2026-10-24'
---
# Bäume und Binärbäume {#trees-and-binary-trees}

Ein Baum ist ein ungerichteter, zusammenhängender, azyklischer Graph. Bäume mit n Knoten haben genau n-1 Kanten. Binärbäume (jeder Knoten hat höchstens 2 Kinder) unterstützen vier Traversierungsreihenfolgen: Inorder, Preorder, Postorder und Level-Order (BFS). Bäume sind grundlegend für Suche, Sortierung und hierarchische Daten.

## Wichtige Fakten {#key-facts}

- Ein Baum mit n Knoten hat genau n-1 Kanten
- Kein Baum, wenn er nicht zusammenhängend ist (auch wenn er azyklisch ist) oder einen Zyklus enthält (auch wenn er zusammenhängend ist)
- Ein **Wald** ist ein azyklischer Graph (jede Zusammenhangskomponente ist ein Baum)
- **Binärbaum-Traversierungen**: Inorder (L-Wurzel-R), Preorder (Wurzel-L-R), Postorder (L-R-Wurzel), Level-Order (BFS)
- Die Inorder-Traversierung eines BST liefert die sortierte Reihenfolge

## Terminologie {#terminology}

| Begriff | Definition |
|------|-----------|
| Wurzel | Oberster Knoten, ohne Elternknoten |
| Elternknoten | Knoten direkt darüber |
| Kind | Knoten direkt darunter |
| Blatt | Keine Kinder (Grad 1 im ungerichteten Fall, Ausgangsgrad 0 im Wurzelbaum) |
| Tiefe | Abstand zur Wurzel (Wurzel = Tiefe 0) |
| Höhe | Maximale Tiefe im Baum |
| Teilbaum | Ein Knoten und alle seine Nachfahren |

## Muster {#patterns}

### Binärbaum-Knoten {#binary-tree-node}

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Inorder-Traversierung (Links - Wurzel - Rechts) {#inorder-traversal-left-root-right}

Für BST: liefert die sortierte Reihenfolge.

```python
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)
```

### Preorder-Traversierung (Wurzel - Links - Rechts) {#preorder-traversal-root-left-right}

Wird zum Kopieren/Serialisieren eines Baums verwendet.

```python
def preorder(root):
    if root:
        print(root.val)
        preorder(root.left)
        preorder(root.right)
```

### Postorder-Traversierung (Links - Rechts - Wurzel) {#postorder-traversal-left-right-root}

Wird zum Löschen eines Baums und zur Berechnung von Teilbaumgrößen verwendet.

```python
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val)
```

### Level-Order-Traversierung (BFS) {#level-order-traversal-bfs}

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

### Umwandlung eines Graphen in einen Wurzelbaum {#graph-to-rooted-tree-conversion}

```python
def build_tree(adj_list, root, parent=None):
    node = TreeNode(root)
    for child in adj_list[root]:
        if child != parent:
            node.children.append(build_tree(adj_list, child, root))
    return node
```

### Knoten in Distanz K {#nodes-at-distance-k}

Binärbaum in einen ungerichteten Graphen umwandeln, dann von dem Zielknoten aus k Schritte mit BFS durchlaufen.

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

### Spannbaum {#spanning-tree}

Ein Spannbaum eines zusammenhängenden Graphen enthält alle Knoten, ist zusammenhängend, azyklisch und hat |V|-1 Kanten. Man findet ihn, indem man BFS/DFS ausführt und nur die Baumkanten behält.

## Fallstricke {#gotchas}

- Jeder ungerichtete, zusammenhängende, azyklische Graph kann an JEDEM Knoten als Wurzel gewählt werden
- Die Reihenfolge der Traversierung ist wichtig: Inorder liefert nur bei BSTs sortierte Ausgaben
- Level-Order (BFS) benötigt eine Warteschlange, keine Rekursion (es gibt zwar eine rekursive Variante, sie ist aber weniger natürlich)
- Probleme mit "Distanz K" auf Bäumen erfordern oft zuerst die Umwandlung in einen ungerichteten Graphen
- Tiefe vs. Höhe: Die Tiefe wird von oben gezählt (Wurzel = 0), die Höhe von unten (Blatt = 0)

## Siehe auch {#see-also}

- [[graph-traversal-bfs-dfs]] - Baumtraversierungen sind Spezialfälle der Graphentraversierung
- [[minimum-spanning-trees]] - MST gewichteter Graphen
- [[graph-representation]] - Bäume als Spezialfälle von Graphen
