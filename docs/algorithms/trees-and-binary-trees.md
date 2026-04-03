---
title: Trees and Binary Trees
category: data-structures
tags: [algorithms, data-structures, trees, binary-tree, traversal, BST]
---

# Trees and Binary Trees

A tree is an undirected, connected, acyclic graph. Trees with n vertices have exactly n-1 edges. Binary trees (each node has at most 2 children) support four traversal orders: inorder, preorder, postorder, and level-order (BFS). Trees are fundamental to search, sorting, and hierarchical data.

## Key Facts

- Tree with n vertices has exactly n-1 edges
- Not a tree if: disconnected (even if acyclic) or contains a cycle (even if connected)
- A **forest** is an acyclic graph (each connected component is a tree)
- **Binary tree traversals**: inorder (L-Root-R), preorder (Root-L-R), postorder (L-R-Root), level-order (BFS)
- Inorder traversal of a BST gives sorted order

## Terminology

| Term | Definition |
|------|-----------|
| Root | Top vertex, no parent |
| Parent | Vertex directly above |
| Child | Vertex directly below |
| Leaf | No children (degree 1 undirected, out-degree 0 rooted) |
| Depth | Distance from root (root = depth 0) |
| Height | Maximum depth in tree |
| Subtree | A vertex and all its descendants |

## Patterns

### Binary Tree Node

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Inorder Traversal (Left - Root - Right)

For BST: gives sorted order.

```python
def inorder(root):
    if root:
        inorder(root.left)
        print(root.val)
        inorder(root.right)
```

### Preorder Traversal (Root - Left - Right)

Used to copy/serialize a tree.

```python
def preorder(root):
    if root:
        print(root.val)
        preorder(root.left)
        preorder(root.right)
```

### Postorder Traversal (Left - Right - Root)

Used to delete tree, compute subtree sizes.

```python
def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.val)
```

### Level-Order Traversal (BFS)

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

### Graph to Rooted Tree Conversion

```python
def build_tree(adj_list, root, parent=None):
    node = TreeNode(root)
    for child in adj_list[root]:
        if child != parent:
            node.children.append(build_tree(adj_list, child, root))
    return node
```

### Nodes at Distance K

Convert binary tree to undirected graph, then BFS from target for k steps.

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

### Spanning Tree

A spanning tree of a connected graph includes all vertices, is connected, acyclic, has |V|-1 edges. Find one by running BFS/DFS and keeping only tree edges.

## Gotchas

- Any undirected connected acyclic graph can be rooted at ANY vertex
- Tree traversal order matters: inorder only gives sorted output on BSTs
- Level-order (BFS) requires a queue, not recursion (though recursive level-order exists, it's less natural)
- "Distance K" problems on trees often require converting to undirected graph first
- Depth vs Height: depth is top-down (root=0), height is bottom-up (leaf=0)

## See Also

- [[graph-traversal-bfs-dfs]] - tree traversals are special cases of graph traversal
- [[minimum-spanning-trees]] - MST of weighted graphs
- [[graph-representation]] - trees as graph special cases
