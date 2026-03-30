---
title: Binary Trees and Traversal
category: data-structures
tags: [binary-tree, traversal, inorder, preorder, postorder, level-order, bfs, dfs, bst]
---

# Binary Trees and Traversal

## Key Facts

- **Binary tree** - each node has at most 2 children (left, right)
- **Binary Search Tree (BST)** - left subtree values < node < right subtree values
- BST operations: Search O(h), Insert O(h), Delete O(h), where h = tree height
- Balanced BST: h = O(log n); Degenerate (skewed): h = O(n)
- **Traversal orders**: inorder (L-Root-R), preorder (Root-L-R), postorder (L-R-Root), level-order (BFS)
- **Inorder traversal of BST produces sorted sequence**
- Self-balancing BSTs: [[binary-tree-traversal]], [[binary-tree-traversal]] guarantee O(log n) height
- Related: [[priority-queue-and-heap]], [[graph-bfs-dfs]]

## Patterns

### Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Recursive Traversals

```python
def inorder(root):
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root):
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

### Iterative Inorder (with Stack)

```python
def inorder_iterative(root):
    stack, result = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result
```

### Level-Order Traversal (BFS)

```python
from collections import deque

def level_order(root):
    if not root: return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

### Validate BST

```python
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    if root.val <= min_val or root.val >= max_val:
        return False
    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))
```

### Tree Height and Diameter

```python
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

def diameter(root):
    result = [0]
    def height(node):
        if not node: return 0
        l = height(node.left)
        r = height(node.right)
        result[0] = max(result[0], l + r)
        return 1 + max(l, r)
    height(root)
    return result[0]
```

```java
// Java: BST search
public TreeNode search(TreeNode root, int val) {
    if (root == null || root.val == val) return root;
    if (val < root.val) return search(root.left, val);
    return search(root.right, val);
}
```

## Gotchas

- **BST validation** - checking only parent vs direct children is insufficient; must check against entire subtree range (pass min/max bounds)
- **Inorder of BST = sorted** - useful property for validation and finding kth smallest
- **Height vs depth** - height is bottom-up (leaf=0), depth is top-down (root=0); different conventions exist
- **Space complexity of recursion** - O(h) where h is height; O(n) worst case for skewed tree
- **Null checks** - always handle `root is None` as base case
- **BST duplicates** - strict BST has no duplicates; some variants allow left <= node < right

## See Also

- [[graph-bfs-dfs]] - tree traversal is a special case of graph traversal
- [[priority-queue-and-heap]] - heap is a complete binary tree
- [[recursion-and-backtracking]] - tree problems are naturally recursive
