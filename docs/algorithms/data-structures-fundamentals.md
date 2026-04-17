---
title: Data Structures Fundamentals - Arrays, Hash Tables, Linked Lists
category: concepts
tags: [misc, data-structures, arrays, hash-tables, linked-lists, stacks, queues, big-o]
---

# Data Structures Fundamentals - Arrays, Hash Tables, Linked Lists

Core data structure operations and complexity analysis - arrays, sorted arrays with binary search, hash tables, linked lists, stacks, and queues. Focus on operation costs and when to choose each structure.

## Key Facts

- Big O measures steps (hardware-independent), not time; ignores constants
- Arrays: O(1) read by index, O(N) insert/delete (shifting)
- Hash tables: O(1) average read/write/delete by key, O(N) search by value
- Linked lists: O(1) insert/delete at known position, O(N) read by index
- Binary search on sorted array: O(log N) - 1M elements = max 20 steps
- Hash table load factor ideal = 0.7 (7 elements per 10 cells)

## Patterns

### Array Operations

| Operation | Steps | Notes |
|-----------|-------|-------|
| Read by index | O(1) | Direct address calculation |
| Search (linear) | O(N) | Must check each element |
| Insert at end | O(1) | Place at next address |
| Insert at beginning | O(N) | Must shift elements right |
| Delete | O(N) | Must shift elements left |

**Sets (no duplicates)**: insert requires N-step search first, making insert O(N) even at end.

### Binary Search

```python
def binary_search(array, target):
    lo, hi = 0, len(array) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoids integer overflow
        if array[mid] == target: return mid
        elif array[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return None
```

| Elements | Linear search max | Binary search max |
|----------|------------------|-------------------|
| 100 | 100 | 7 |
| 10,000 | 10,000 | 14 |
| 1,000,000 | 1,000,000 | 20 |

### Hash Tables

Hash function converts key to array index. Collision handling via chaining (array of key-value pairs at each cell).

**Optimization pattern** - convert array to hash for O(1) lookups:
```ruby
hash = {}
array.each { |elem| hash[elem] = true }
# Now: hash[value] -> O(1) instead of O(N) scan
```

**Array subset check** - naive O(N*M), optimized O(N+M):
```javascript
function isSubset(array1, array2) {
  const larger = array1.length > array2.length ? array1 : array2;
  const smaller = array1.length > array2.length ? array2 : array1;
  const hashTable = {};
  for (const elem of larger) { hashTable[elem] = true; }
  for (const elem of smaller) {
    if (!hashTable[elem]) return false;
  }
  return true;
}
```

**Replace conditionals with hash lookup**:
```python
STATUS_CODES = {200: "OK", 301: "Moved Permanently", 404: "Not Found", 500: "Internal Server Error"}
def status_code_meaning(code):
    return STATUS_CODES.get(code)
```

### Linked Lists

| Operation | Linked List | Array |
|-----------|------------|-------|
| Read by index | O(N) | O(1) |
| Insert at known position | O(1) | O(N) |
| Insert at head | O(1) | O(N) |
| Delete at known position | O(1) | O(N) |
| Search | O(N) | O(N) |

Queue on doubly linked list: enqueue = insert_at_end O(1), dequeue = remove_from_front O(1). Better than array-backed queue.

### Stacks and Queues

**Stack (LIFO)**: push/pop from same end. Used for: function calls, undo, DFS.
**Queue (FIFO)**: enqueue at back, dequeue from front. Used for: BFS, task queues.

### Big O Reference

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array read, hash lookup |
| O(log N) | Logarithmic | Binary search, BST ops |
| O(N) | Linear | Linear search, traverse |
| O(N log N) | Linearithmic | Quicksort avg, mergesort |
| O(N^2) | Quadratic | Bubble/insertion/selection sort |
| O(2^N) | Exponential | Brute-force combinations |

**Important**: Big O ignores constants. O(N/2), O(2N), O(100N) all simplify to O(N). Constants matter within same category.

### Space Complexity

| Structure | Space |
|-----------|-------|
| Array of N items | O(N) |
| N x N matrix | O(N^2) |
| Recursion depth D | O(D) stack frames |
| Hash table N items | O(N) |

## Gotchas

- Hash table search is O(1) only when using the key; searching by value is O(N)
- Binary search requires sorted data - sort cost O(N log N) may not be worth it for single search
- Sorted array trade-off: faster search O(log N) but slower insertion O(N) for maintaining order
- Big O best/worst case: stated complexity is usually worst case; linear search is O(1) best, O(N) worst

## See Also

- [[trees-and-graphs]] - BST, heaps, tries, BFS, DFS, Dijkstra
- [[sorting-algorithms]] - detailed sort implementations and comparisons
- [[dynamic-programming]] - memoization, recursion patterns
- [[algorithms/problem-patterns]] - two-pointer, sliding window, interview techniques
