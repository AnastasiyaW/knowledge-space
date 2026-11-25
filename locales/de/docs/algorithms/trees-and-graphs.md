---
title: "Bäume und Graphen – BST, Heaps, Tries, Traversierung"
category: concepts
tags: [data-structures, trees, graphs, bst, heap, trie, bfs, dfs, dijkstra]
level: 3
source_sha256: 758cbcbafbe08018d3195ff2b6367346d59c3e7d9171d85ee6ca16d781bb6e4a
translation: machine
translated_at: '2026-10-24'
---
# Bäume und Graphen – BST, Heaps, Tries, Traversierung {#trees-and-graphs-bst-heaps-tries-traversal}

Binäre Suchbäume, Heaps/Prioritätswarteschlangen, Tries (Präfixbäume), Graphdarstellung und Traversierungsalgorithmen (BFS, DFS, Dijkstra). Enthält Komplexitätsanalyse und Implementierungsmuster.

## Key Facts {#key-facts}

- Ausbalancierter BST: Suchen/Einfügen/Löschen jeweils O(log N); degradiert zu O(N), wenn unausbalanciert
- Heap: Einfügen O(log N), Wurzel löschen O(log N), Min/Max lesen O(1); nur schwache Ordnung
- Trie: Suchen/Einfügen O(M), wobei M = Schlüssellänge, unabhängig von der Anzahl gespeicherter Wörter
- BFS verwendet eine Queue (kürzester Pfad in ungewichtetem Graphen); DFS verwendet Stack/Rekursion (tiefe Exploration)
- Komplexität der Graphtraversierung: O(V + E) für BFS und DFS
- Dijkstra findet den günstigsten Pfad vom Start zu allen Knoten; O((V + E) log V) mit Prioritätswarteschlange

## Patterns {#patterns}

### Binary Search Tree {#binary-search-tree}

Regel: linkes Kind < Elternknoten < rechtes Kind (rekursiv).

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

**In-Order-Traversierung**: links -> Wurzel -> rechts = sortierte Reihenfolge. O(N).

**BST vs. sortiertes Array**: Suche jeweils O(log N), aber Einfügen/Löschen O(log N) vs. O(N). Der BST ist im Vorteil, wenn sich die Daten häufig ändern.

### Heaps / Prioritätswarteschlangen {#heaps-priority-queues}

**Max-Heap**: jeder Knoten >= seine Kinder. Wurzel = Maximum.
**Min-Heap**: jeder Knoten <= seine Kinder. Wurzel = Minimum.

**Array-Darstellung**: Knoten mit Index `i` -> linkes Kind bei `2i+1`, rechtes Kind bei `2i+2`, Elternknoten bei `(i-1)/2`.

**Einfügen ("Trickle up")**: am Ende anfügen, mit dem Elternknoten tauschen, solange der Wert größer als der Elternwert ist.
**Wurzel löschen ("Trickle down")**: letzten Knoten an die Wurzel verschieben, mit dem größeren Kind tauschen, solange der Wert kleiner als die Kinder ist.

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

### Tries (Präfixbäume) {#tries-prefix-trees}

Jeder Knoten ist eine Hashtabelle, die Zeichen auf Kindknoten abbildet. Ein Stern (`*`) markiert das Ende eines vollständigen Wortes.

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

Einsatz für: Autovervollständigung, Autokorrektur, IP-Routing, Rechtschreibprüfung.

### Graphdarstellung {#graph-representation}

```ruby
class GraphVertex
  attr_accessor :value, :adjacent_vertices
  def initialize(value)
    @value = value
    @adjacent_vertices = []
  end
end
```

Arten: gerichtet, ungerichtet, gewichtet.

### BFS (queuebasiert) {#bfs-queue-based}

Besucht alle Nachbarn, bevor tiefer gegangen wird. Findet den kürzesten Pfad in einem ungewichteten Graphen.

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

### DFS (stack-/rekursionsbasiert) {#dfs-stackrecursion-based}

Geht so tief wie möglich, bevor zurückgegangen wird. Einsatz für: alle Pfade, Zyklenerkennung, topologische Sortierung.

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

### Dijkstra-Algorithmus {#dijkstras-algorithm}

Findet den günstigsten Pfad vom Start zu allen Knoten. Nur nichtnegative Gewichte. Greedy-Algorithmus.

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

## Gotchas {#gotchas}

- Unausbalancierter BST (Daten in sortierter Reihenfolge eingefügt) wird zu einer verketteten Liste mit O(N)-Operationen; selbstbalancierende Bäume verwenden (AVL, Rot-Schwarz)
- Die Fensterfunktion `LAST_VALUE` erfordert einen expliziten Frame `UNBOUNDED FOLLOWING` (der Standard-Frame endet bei der aktuellen Zeile)
- Dijkstra schlägt bei negativen Kantengewichten fehl - stattdessen Bellman-Ford verwenden
- Der Heap ist schwach geordnet (Elternknoten > Kinder), nicht vollständig sortiert - nützlich, wenn nur Min/Max relevant ist
- Die Asterisk-Markierung im Trie ist nötig, wenn Wörter Präfixe teilen (z. B. "bat" und "batter")

## See Also {#see-also}

- [[data-structures-fundamentals]] - Arrays, Hashtabellen, verkettete Listen, Big O
- [[sorting-algorithms]] - Implementierungen von Quicksort und Insertion Sort
- [[dynamic-programming]] - überlappende Teilprobleme auf Baumstrukturen
