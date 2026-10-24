---
title: "Arbres et graphes - ABR, tas, tries, parcours"
category: concepts
tags: [data-structures, trees, graphs, bst, heap, trie, bfs, dfs, dijkstra]
level: 3
source_sha256: 758cbcbafbe08018d3195ff2b6367346d59c3e7d9171d85ee6ca16d781bb6e4a
translation: machine
translated_at: '2026-10-24'
---
# Arbres et graphes - ABR, tas, tries, parcours {#trees-and-graphs-bst-heaps-tries-traversal}

Arbres binaires de recherche, tas et files de priorité, tries (arbres de préfixes), représentation des graphes et algorithmes de parcours (BFS, DFS, Dijkstra). Inclut l'analyse de complexité et les schémas d'implémentation.

## Points clés {#key-facts}

- ABR équilibré : recherche, insertion et suppression en O(log N) ; dégénère en O(N) si déséquilibré
- Tas : insertion O(log N), suppression de la racine O(log N), lecture du min/max O(1) ; ordre faible uniquement
- Trie : recherche/insertion en O(M) où M = longueur de la clé, indépendant du nombre de mots stockés
- BFS utilise une file (plus court chemin dans un graphe non pondéré) ; DFS utilise une pile/la récursion (exploration en profondeur)
- Complexité du parcours de graphe : O(V + E) pour BFS comme pour DFS
- Dijkstra trouve le chemin le moins coûteux depuis le départ vers tous les sommets ; O((V + E) log V) avec une file de priorité

## Schémas {#patterns}

### Arbre binaire de recherche {#binary-search-tree}

Règle : enfant gauche < parent < enfant droit (récursivement).

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

**Parcours infixe** : gauche -> racine -> droite = ordre trié. O(N).

**ABR vs tableau trié** : la recherche est en O(log N) dans les deux cas, mais l'insertion/suppression est en O(log N) contre O(N). L'ABR est préférable lorsque les données changent fréquemment.

### Tas / files de priorité {#heaps-priority-queues}

**Tas-max** : chaque nœud >= à ses enfants. La racine = maximum.
**Tas-min** : chaque nœud <= à ses enfants. La racine = minimum.

**Représentation par tableau** : nœud à l'indice `i` -> enfant gauche à `2i+1`, enfant droit à `2i+2`, parent à `(i-1)/2`.

**Insertion (« remontée »)** : ajouter à la fin, échanger avec le parent tant que la valeur est supérieure au parent.
**Suppression de la racine (« descente »)** : déplacer le dernier nœud à la racine, échanger avec le plus grand enfant tant que la valeur est inférieure à ses enfants.

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

### Tries (arbres de préfixes) {#tries-prefix-trees}

Chaque nœud est une table de hachage associant des caractères à des nœuds enfants. L'astérisque (`*`) marque la fin d'un mot complet.

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

À utiliser pour : l'autocomplétion, la correction automatique, le routage IP, la vérification orthographique.

### Représentation des graphes {#graph-representation}

```ruby
class GraphVertex
  attr_accessor :value, :adjacent_vertices
  def initialize(value)
    @value = value
    @adjacent_vertices = []
  end
end
```

Types : orienté, non orienté, pondéré.

### BFS (basé sur une file) {#bfs-queue-based}

Visite tous les voisins avant de descendre plus profondément. Trouve le plus court chemin dans un graphe non pondéré.

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

### DFS (basé sur une pile / la récursion) {#dfs-stackrecursion-based}

Descend le plus loin possible avant de revenir en arrière. Utilisé pour : tous les chemins, la détection de cycles, le tri topologique.

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

### Algorithme de Dijkstra {#dijkstras-algorithm}

Trouve le chemin le moins coûteux depuis le départ vers tous les sommets. Uniquement avec des poids non négatifs. Algorithme glouton.

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

## Pièges {#gotchas}

- Un ABR déséquilibré (données insérées dans l'ordre trié) devient une liste chaînée avec des opérations en O(N) ; utiliser des arbres auto-équilibrés (AVL, rouge-noir)
- La fonction de fenêtrage `LAST_VALUE` nécessite un cadre explicite `UNBOUNDED FOLLOWING` (le cadre par défaut s'arrête à la ligne courante)
- Dijkstra échoue sur des arêtes de poids négatif - utiliser Bellman-Ford à la place
- Le tas est faiblement ordonné (parent > enfants) et non entièrement trié - utile lorsque seuls le min/max comptent
- Le marqueur astérisque du trie est nécessaire lorsque des mots partagent un préfixe (par exemple « bat » et « batter »)

## Voir aussi {#see-also}

- [[data-structures-fundamentals]] - tableaux, tables de hachage, listes chaînées, Big O
- [[sorting-algorithms]] - implémentations de quicksort et du tri par insertion
- [[dynamic-programming]] - sous-problèmes qui se chevauchent sur les structures arborescentes
