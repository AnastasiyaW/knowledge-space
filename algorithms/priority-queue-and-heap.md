---
title: Priority Queue and Heap
category: data-structures
tags: [priority-queue, heap, binary-heap, min-heap, max-heap, heapify]
---

# Priority Queue and Heap

## Key Facts

- **Priority queue** - abstract data type where elements are dequeued by priority, not insertion order
- **Binary heap** - canonical implementation of priority queue; complete binary tree satisfying heap property
- **Min-heap** - parent <= children (root is minimum); **Max-heap** - parent >= children (root is maximum)
- Operations: Insert O(log n), Extract-min/max O(log n), Peek O(1), Build heap O(n)
- **Heapify** (build heap from array) - O(n) using bottom-up sift-down, not O(n log n)
- Stored as array: parent at `i`, left child at `2i+1`, right child at `2i+2`, parent at `(i-1)//2`
- Python: `heapq` module (min-heap only); Java: `PriorityQueue` (min-heap by default)
- Used in: [[graph-shortest-path]], Prim's MST, Huffman coding, heap sort, top-K problems
- Related: [[binary-tree-traversal]], [[sorting-algorithms]]

## Patterns

### Python heapq (Min-Heap)

```python
import heapq

# Basic operations
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
smallest = heapq.heappop(heap)  # 1
peek = heap[0]  # next smallest without removing

# Build heap from list - O(n)
nums = [5, 1, 3, 8, 2]
heapq.heapify(nums)  # in-place

# Top K smallest
top_3 = heapq.nsmallest(3, nums)

# Top K largest
top_3_large = heapq.nlargest(3, nums)
```

### Max-Heap via Negation (Python)

```python
import heapq

# Python only has min-heap; negate values for max-heap
max_heap = []
for val in [5, 1, 3, 8, 2]:
    heapq.heappush(max_heap, -val)

largest = -heapq.heappop(max_heap)  # 8
```

### Heap with Custom Priority (Tuples)

```python
import heapq

# Priority queue with (priority, item) tuples
tasks = []
heapq.heappush(tasks, (2, "low priority"))
heapq.heappush(tasks, (1, "high priority"))
heapq.heappush(tasks, (3, "lowest priority"))
priority, task = heapq.heappop(tasks)  # (1, "high priority")
```

### Top K Frequent Elements

```python
from collections import Counter
import heapq

def top_k_frequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

# Alternative: maintain heap of size k - O(n log k)
def top_k_frequent_heap(nums, k):
    count = Counter(nums)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for freq, num in heap]
```

### Kth Largest Element

```python
import heapq

def find_kth_largest(nums, k):
    # Min-heap of size k - O(n log k)
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]
```

```java
// Java PriorityQueue (min-heap by default)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5);
minHeap.offer(1);
int smallest = minHeap.poll();  // 1

// Max-heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());

// Custom comparator
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
```

## Gotchas

- **Python heapq is min-heap only** - negate values or use tuple `(-priority, value)` for max-heap behavior
- **heapq does not support decrease-key** - for Dijkstra, add duplicate entries and skip stale ones
- **Heap is NOT sorted** - only the root is guaranteed to be min/max; siblings have no order guarantee
- **Build heap is O(n), not O(n log n)** - bottom-up sift-down is more efficient than n insertions
- **heapq.heapreplace vs heappushpop** - `heapreplace` pops first then pushes; `heappushpop` pushes first then pops
- **Tuple comparison** - `(1, "b") < (1, "a")` is False in Python; if priorities are equal, items must be comparable or use a counter

## See Also

- [[graph-shortest-path]] - Dijkstra uses priority queue
- [[sorting-algorithms]] - heap sort uses heap
- [[binary-tree-traversal]] - heap is stored as complete binary tree
