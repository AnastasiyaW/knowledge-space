---
title: Trie (Prefix Tree)
category: data-structures
tags: [trie, prefix-tree, autocomplete, word-search, string-matching]
---

# Trie (Prefix Tree)

## Key Facts

- **Trie** - tree-like structure for storing strings; each edge represents a character
- Insert: O(m), Search: O(m), Prefix search: O(m) where m = word length
- Space: O(ALPHABET_SIZE * m * n) worst case, where n = number of words
- Each node has up to ALPHABET_SIZE children (26 for lowercase English)
- Applications: autocomplete, spell checker, IP routing, word search, prefix matching
- Advantage over [[hash-tables]]: prefix queries, lexicographic ordering, no hash collisions
- Related: [[arrays-and-strings]], [[recursion-and-backtracking]]

## Patterns

### Trie Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find_node(prefix) is not None

    def _find_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### Autocomplete (All Words with Prefix)

```python
def autocomplete(trie, prefix):
    node = trie._find_node(prefix)
    if not node:
        return []
    results = []
    def dfs(node, path):
        if node.is_end:
            results.append(prefix + ''.join(path))
        for char, child in node.children.items():
            path.append(char)
            dfs(child, path)
            path.pop()
    dfs(node, [])
    return results
```

### Word Search in Grid (Trie + Backtracking)

```python
def find_words(board, words):
    trie = Trie()
    for word in words:
        trie.insert(word)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(r, c, node, path):
        char = board[r][c]
        if char not in node.children:
            return
        node = node.children[char]
        path.append(char)
        if node.is_end:
            result.add(''.join(path))

        board[r][c] = '#'  # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, node, path)
        board[r][c] = char  # restore
        path.pop()

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, [])
    return list(result)
```

```java
// Java Trie
class Trie {
    private TrieNode root = new TrieNode();

    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }

    public void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null)
                node.children[idx] = new TrieNode();
            node = node.children[idx];
        }
        node.isEnd = true;
    }

    public boolean search(String word) {
        TrieNode node = findNode(word);
        return node != null && node.isEnd;
    }

    public boolean startsWith(String prefix) {
        return findNode(prefix) != null;
    }

    private TrieNode findNode(String s) {
        TrieNode node = root;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (node.children[idx] == null) return null;
            node = node.children[idx];
        }
        return node;
    }
}
```

## Gotchas

- **Space overhead** - trie can use more memory than hash set for short word lists; beneficial mainly for prefix queries
- **Array vs HashMap children** - array `[26]` is faster but wastes space for sparse alphabets; `dict` is more flexible
- **Delete is tricky** - must check if node has other children before removing; often not implemented
- **Case sensitivity** - normalize input (lowercase) before inserting
- **Not a balanced tree** - depth equals length of longest word; no balancing needed
- **Trie vs hash set** - hash set is better for exact lookup; trie is better for prefix operations and lexicographic ordering

## See Also

- [[hash-tables]] - alternative for exact string lookup
- [[recursion-and-backtracking]] - trie + backtracking for word search
- [[arrays-and-strings]] - string matching problems
