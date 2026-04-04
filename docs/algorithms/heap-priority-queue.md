---
title: Heap and Priority Queue
category: concepts
tags: [data-structure, heap, priority-queue, sorting]
---

# Heap and Priority Queue

Binary heap: complete binary tree satisfying heap property. Min-heap: parent <= children. Max-heap: parent >= children. Foundation for priority queues, heapsort, and graph algorithms.

## Key Facts

- Complete binary tree stored as array: parent at `i`, children at `2i+1`, `2i+2`
- Parent index: `(i-1)//2`
- Insert: O(log N) - add at end, bubble up
- Extract min/max: O(log N) - swap root with last, bubble down
- Peek min/max: O(1)
- Build heap from array: O(N) - not O(N log N)
- Heapsort: O(N log N) in-place, not stable
- Python `heapq` is min-heap only; negate values for max-heap

## Implementation

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

## Python heapq Usage

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

## Patterns

### Top-K Elements

```python
def top_k_frequent(nums, k):
    from collections import Counter
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### Merge K Sorted Lists

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

### Running Median (Two Heaps)

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

## Complexity

| Operation | Time |
|-----------|------|
| Insert | O(log N) |
| Extract min/max | O(log N) |
| Peek | O(1) |
| Build heap | O(N) |
| Heapsort | O(N log N) |
| Find k-th largest | O(N + K log N) |

## Gotchas

- **Issue:** Python `heapq` only supports min-heap -> **Fix:** Negate values for max-heap behavior. For objects, wrap in tuple `(-priority, item)`.
- **Issue:** Using `heapq.nlargest(k, arr)` when `k` is close to `len(arr)` -> **Fix:** For `k > len(arr)/2`, sort and slice is faster. `nlargest` is O(N + K log N), sort is O(N log N).
- **Issue:** Trying to update priority of existing element in heapq -> **Fix:** Python heapq has no decrease-key. Use lazy deletion: mark old entry as removed, push new entry. Or use `sortedcontainers.SortedList`.

## See Also

- [[sorting-algorithms]] - heapsort
- [[shortest-path-algorithms]] - Dijkstra uses min-heap
- [[minimum-spanning-trees]] - Prim uses min-heap
