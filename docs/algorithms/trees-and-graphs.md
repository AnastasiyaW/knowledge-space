---
title: Trees and Graphs - BST, Heaps, Tries, Traversal
category: concepts
tags: [data-structures, trees, graphs, bst, heap, trie, bfs, dfs, dijkstra]
---

# Trees and Graphs - BST, Heaps, Tries, Traversal

Binary search trees, heaps/priority queues, tries (prefix trees), graph representation, and traversal algorithms (BFS, DFS, Dijkstra). Includes complexity analysis and implementation patterns.

## Key Facts

- Balanced BST: search/insert/delete all O(log N); degrades to O(N) if unbalanced
- Heap: insert O(log N), delete-root O(log N), read-min/max O(1); weak ordering only
- Trie: search/insert O(M) where M = key length, independent of stored word count
- BFS uses queue (shortest path in unweighted graph); DFS uses stack/recursion (deep exploration)
- Graph traversal complexity: O(V + E) for both BFS and DFS
- Dijkstra finds cheapest path from start to all vertices; O((V + E) log V) with priority queue

## Patterns

### Binary Search Tree

Rule: left child < parent < right child (recursively).

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.value = val
        self.leftChild = left
        self.rightChild = right

def search(search_value, node):
    if node is None or node.value == search_value:
        return node
    elif search_value < node.value:
        return search(search_value, node.leftChild)
    else:
        return search(search_value, node.rightChild)
```

**In-order traversal**: left -> root -> right = sorted order. O(N).

**BST vs sorted array**: search same O(log N), but insert/delete O(log N) vs O(N). BST wins when data changes frequently.

### Heaps / Priority Queues

**Max-heap**: every node >= its children. Root = maximum.
**Min-heap**: every node <= its children. Root = minimum.

**Array representation**: node at index `i` -> left child at `2i+1`, right child at `2i+2`, parent at `(i-1)/2`.

**Insert ("trickle up")**: add at end, swap with parent while value > parent.
**Delete root ("trickle down")**: move last node to root, swap with larger child while value < children.

```python
import heapq
heap = []
heapq.heappush(heap, (priority, item))
priority, item = heapq.heappop(heap)   # min-heap by default

# Max-heap: negate priorities
heapq.heappush(heap, (-priority, item))

# k largest / k smallest
heapq.nlargest(k, iterable, key=fn)
heapq.nsmallest(k, iterable, key=fn)
```

### Tries (Prefix Trees)

Each node is a hash table mapping characters to child nodes. Asterisk (`*`) marks end of complete word.

```python
class TrieNode:
    def __init__(self):
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.children["*"] = None  # end-of-word marker

    def autocomplete(self, prefix):
        current_node = self.search(prefix)
        return [] if current_node is None else self.collect_all_words(current_node, prefix)
```

Use for: autocomplete, autocorrect, IP routing, spell checking.

### Graph Representation

```ruby
class GraphVertex
  attr_accessor :value, :adjacent_vertices
  def initialize(value)
    @value = value
    @adjacent_vertices = []
  end
end
```

Types: directed, undirected, weighted.

### BFS (Queue-based)

Visits all neighbors before going deeper. Finds shortest path in unweighted graph.

```ruby
def bfs(starting_vertex)
  visited = {}
  queue = Queue.new
  visited[starting_vertex.value] = true
  queue.enqueue(starting_vertex)
  while queue.read
    current = queue.dequeue
    current.adjacent_vertices.each do |adj|
      unless visited[adj.value]
        visited[adj.value] = true
        queue.enqueue(adj)
      end
    end
  end
end
```

### DFS (Stack/Recursion-based)

Goes as deep as possible before backtracking. Used for: all paths, cycle detection, topological sort.

```ruby
def dfs(vertex, visited = {})
  visited[vertex.value] = true
  vertex.adjacent_vertices.each do |adj|
    unless visited[adj.value]
      dfs(adj, visited)
    end
  end
end
```

### Dijkstra's Algorithm

Finds cheapest path from start to all vertices. Non-negative weights only. Greedy algorithm.

```python
def dijkstra(start, finish, graph):
    cheapest_prices = {start: 0}
    cheapest_previous = {}
    unvisited = set(graph.keys())
    current = start

    while current != finish:
        unvisited.remove(current)
        for neighbor, weight in graph[current].items():
            price = cheapest_prices[current] + weight
            if neighbor not in cheapest_prices or price < cheapest_prices[neighbor]:
                cheapest_prices[neighbor] = price
                cheapest_previous[neighbor] = current
        current = min((v for v in unvisited if v in cheapest_prices),
                      key=lambda v: cheapest_prices[v])

    # Reconstruct path
    path = []
    node = finish
    while node != start:
        path.insert(0, node)
        node = cheapest_previous[node]
    path.insert(0, start)
    return path, cheapest_prices[finish]
```

## Gotchas

- Unbalanced BST (data inserted in sorted order) becomes a linked list with O(N) operations; use self-balancing trees (AVL, Red-Black)
- `LAST_VALUE` window function requires explicit `UNBOUNDED FOLLOWING` frame (default frame ends at current row)
- Dijkstra fails on negative edge weights - use Bellman-Ford instead
- Heap is weakly ordered (parent > children) not fully sorted - useful when only min/max matters
- Trie asterisk marker is needed when words share prefixes (e.g., "bat" and "batter")

## See Also

- [[data-structures-fundamentals]] - arrays, hash tables, linked lists, Big O
- [[sorting-algorithms]] - quicksort, insertion sort implementations
- [[dynamic-programming]] - overlapping subproblems on tree structures
