---
title: "Tas et file de priorité"
category: concepts
tags: [data-structure, heap, priority-queue, sorting]
level: 3
source_sha256: a066d0feb3986c1429b5d130096dbb0f8e0191a936080e26819e90b0e2713f89
translation: machine
translated_at: '2026-10-24'
---
# Tas et file de priorité {#heap-and-priority-queue}

Tas binaire : arbre binaire complet satisfaisant la propriété de tas. Min-tas : parent <= enfants. Max-tas : parent >= enfants. Base des files de priorité, du tri par tas et des algorithmes sur les graphes.

## Points clés {#key-facts}

- Arbre binaire complet stocké sous forme de tableau : parent à `i`, enfants à `2i+1`, `2i+2`
- Index du parent : `(i-1)//2`
- Insertion : O(log N) - ajout en fin, remontée (bubble up)
- Extraction min/max : O(log N) - échange de la racine avec le dernier élément, descente (bubble down)
- Lecture min/max : O(1)
- Construction du tas à partir d'un tableau : O(N) - et non O(N log N)
- Tri par tas : O(N log N) en place, non stable
- `heapq` de Python ne gère que le min-tas ; pour un max-tas, il faut inverser les valeurs (négation)

## Implémentation {#implementation}

```python
class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, val):
        self.data.append(val)
        self._bubble_up(len(self.data) - 1)

    def pop(self):
        if len(self.data) == 1:
            return self.data.pop()
        root = self.data[0]
        self.data[0] = self.data.pop()
        self._bubble_down(0)
        return root

    def _bubble_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.data[i] < self.data[parent]:
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                i = parent
            else:
                break

    def _bubble_down(self, i):
        n = len(self.data)
        while True:
            smallest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self.data[left] < self.data[smallest]:
                smallest = left
            if right < n and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == i:
                break
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            i = smallest
```

## Utilisation de heapq en Python {#python-heapq-usage}

```python
import heapq

# Min-heap
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
smallest = heapq.heappop(heap)  # 1

# Max-heap (negate values)
max_heap = []
heapq.heappush(max_heap, -5)
largest = -heapq.heappop(max_heap)  # 5

# Build heap from list - O(N)
arr = [5, 1, 8, 3, 2]
heapq.heapify(arr)

# K largest elements - O(N log K)
k_largest = heapq.nlargest(3, arr)

# K smallest elements
k_smallest = heapq.nsmallest(3, arr)

# Merge sorted iterables
merged = list(heapq.merge([1, 3, 5], [2, 4, 6]))
```

## Patrons {#patterns}

### Les K éléments les plus grands {#top-k-elements}

```python
def top_k_frequent(nums, k):
    from collections import Counter
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### Fusion de K listes triées {#merge-k-sorted-lists}

```python
def merge_k_sorted(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    return result
```

### Médiane glissante (deux tas) {#running-median-two-heaps}

```python
class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negated)
        self.hi = []  # min-heap

    def add(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def median(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2
```

## Complexité {#complexity}

| Opération | Temps |
|-----------|------|
| Insertion | O(log N) |
| Extraction min/max | O(log N) |
| Lecture | O(1) |
| Construction du tas | O(N) |
| Tri par tas | O(N log N) |
| Recherche du k-ième plus grand | O(N + K log N) |

## Pièges courants {#gotchas}

- **Problème :** `heapq` de Python ne supporte que le min-tas -> **Solution :** inverser les valeurs pour obtenir le comportement de max-tas. Pour des objets, encapsuler dans un tuple `(-priority, item)`.
- **Problème :** utiliser `heapq.nlargest(k, arr)` lorsque `k` est proche de `len(arr)` -> **Solution :** pour `k > len(arr)/2`, trier puis découper est plus rapide. `nlargest` est en O(N + K log N), le tri en O(N log N).
- **Problème :** tenter de mettre à jour la priorité d'un élément existant dans heapq -> **Solution :** heapq de Python n'offre pas de decrease-key. Utiliser la suppression paresseuse : marquer l'ancienne entrée comme supprimée et insérer la nouvelle. Ou utiliser `sortedcontainers.SortedList`.

## Voir aussi {#see-also}

- [[sorting-algorithms]] - tri par tas
- [[shortest-path-algorithms]] - Dijkstra utilise un min-tas
- [[minimum-spanning-trees]] - Prim utilise un min-tas
