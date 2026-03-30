---
title: Sorting Algorithms
category: algorithms
tags: [sorting, merge-sort, quick-sort, heap-sort, bubble-sort, insertion-sort, counting-sort, radix-sort]
---

# Sorting Algorithms

## Key Facts

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) | O(1) | No |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| Radix Sort | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Yes |

- **Comparison-based** sorts cannot be faster than O(n log n) in the worst case
- **Stable** sort preserves relative order of equal elements
- Python uses **Timsort** (hybrid merge+insertion sort), Java uses **dual-pivot quicksort** for primitives
- Related: [[binary-search]], [[priority-queue-and-heap]]

## Patterns

### Merge Sort - Divide and Conquer

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
# Time: O(n log n), Space: O(n)
```

### Quick Sort

```python
import random

def quick_sort(arr, lo=0, hi=None):
    if hi is None:
        hi = len(arr) - 1
    if lo < hi:
        pivot_idx = partition(arr, lo, hi)
        quick_sort(arr, lo, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, hi)

def partition(arr, lo, hi):
    pivot_idx = random.randint(lo, hi)  # randomized pivot
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i
# Average: O(n log n), Worst: O(n^2) with bad pivot
```

### Counting Sort (Non-comparison)

```python
def counting_sort(arr, max_val):
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    result = []
    for val, cnt in enumerate(count):
        result.extend([val] * cnt)
    return result
# Time: O(n + k), Space: O(k), where k = range of values
```

### Bubble Sort (Educational)

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break  # early termination if already sorted
# Best: O(n) with early termination, Worst: O(n^2)
```

```java
// Java: Arrays.sort uses dual-pivot quicksort for int[]
import java.util.Arrays;
Arrays.sort(arr);  // in-place, O(n log n) average

// Custom comparator for objects
Arrays.sort(arr, (a, b) -> a.compareTo(b));
```

## Gotchas

- **Quick sort worst case** - O(n^2) when pivot is always min/max; use randomized pivot or median-of-three
- **Merge sort for linked lists** - O(log n) space instead of O(n), because merge is in-place without auxiliary array
- **Stability matters** - when sorting objects by multiple keys (e.g., sort by name then by age), stable sort preserves first key order
- **Counting/Radix sort** - only for integers or fixed-length keys; not comparison-based
- **Python sorted() vs .sort()** - `sorted()` returns new list, `.sort()` modifies in-place; both are Timsort O(n log n)
- **In-place vs not** - quick sort is in-place O(log n) stack; merge sort needs O(n) extra space for arrays

## See Also

- [[binary-search]] - requires sorted input
- [[priority-queue-and-heap]] - heap sort uses heap data structure
- [[big-o-complexity-analysis]] - comparison of sort complexities
