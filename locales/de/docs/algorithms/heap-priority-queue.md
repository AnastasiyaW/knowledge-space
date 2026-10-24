---
title: "Heap und Prioritätswarteschlange"
category: concepts
tags: [data-structure, heap, priority-queue, sorting]
level: 3
source_sha256: a066d0feb3986c1429b5d130096dbb0f8e0191a936080e26819e90b0e2713f89
translation: machine
translated_at: '2026-10-24'
---
: I need to output the document in German with placeholders kept. Let me translate carefully.

---
title: Heap und Prioritätswarteschlange
category: concepts
tags: [data-structure, heap, priority-queue, sorting]
---

# Heap und Prioritätswarteschlange {#heap-and-priority-queue}

Binärer Heap: vollständiger Binärbaum, der die Heap-Eigenschaft erfüllt. Min-Heap: Elternknoten <= Kindknoten. Max-Heap: Elternknoten >= Kindknoten. Grundlage für Prioritätswarteschlangen, Heapsort und Graphalgorithmen.

## Wichtige Fakten {#key-facts}

- Vollständiger Binärbaum als Array gespeichert: Elternknoten bei `i`, Kindknoten bei `2i+1`, `2i+2`
- Index des Elternknotens: `(i-1)//2`
- Einfügen: O(log N) - am Ende anhängen, nach oben sickern lassen
- Minimum/Maximum entfernen: O(log N) - Wurzel mit letztem Element tauschen, nach unten sickern lassen
- Minimum/Maximum betrachten: O(1)
- Heap aus Array aufbauen: O(N) - nicht O(N log N)
- Heapsort: O(N log N) in-place, nicht stabil
- Python `heapq` ist nur ein Min-Heap; für einen Max-Heap Werte negieren

## Implementierung {#implementation}

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

## Verwendung von Python heapq {#python-heapq-usage}

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

## Muster {#patterns}

### Top-K-Elemente {#top-k-elements}

```python
def top_k_frequent(nums, k):
    from collections import Counter
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### K sortierte Listen zusammenführen {#merge-k-sorted-lists}

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

### Laufender Median (zwei Heaps) {#running-median-two-heaps}

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

## Komplexität {#complexity}

| Operation | Zeit |
|-----------|------|
| Einfügen | O(log N) |
| Minimum/Maximum entfernen | O(log N) |
| Betrachten | O(1) |
| Heap aufbauen | O(N) |
| Heapsort | O(N log N) |
| k-größtes Element finden | O(N + K log N) |

## Fallstricke {#gotchas}

- **Problem:** Python `heapq` unterstützt nur Min-Heaps -> **Lösung:** Werte für Max-Heap-Verhalten negieren. Bei Objekten in ein Tupel `(-priority, item)` verpacken.
- **Problem:** `heapq.nlargest(k, arr)` verwenden, wenn `k` nahe bei `len(arr)` liegt -> **Lösung:** Für `k > len(arr)/2` ist Sortieren und Slicing schneller. `nlargest` ist O(N + K log N), Sortieren ist O(N log N).
- **Problem:** Priorität eines bestehenden Elements in heapq aktualisieren -> **Lösung:** Python heapq bietet kein Decrease-Key. Lazy Deletion verwenden: alten Eintrag als entfernt markieren und neuen Eintrag einfügen. Alternativ `sortedcontainers.SortedList` verwenden.

## Siehe auch {#see-also}

- [[sorting-algorithms]] - Heapsort
- [[shortest-path-algorithms]] - Dijkstra verwendet Min-Heap
- [[minimum-spanning-trees]] - Prim verwendet Min-Heap
