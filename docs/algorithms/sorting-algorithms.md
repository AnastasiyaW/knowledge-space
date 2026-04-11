---
title: Sorting Algorithms
category: algorithms
tags: [algorithms, sorting, comparison-sort, merge-sort, quick-sort, radix-sort]
---

# Sorting Algorithms

Comprehensive reference for sorting algorithms covering comparison-based sorts (insertion, bubble, selection, merge, quick, heap), non-comparison sorts (counting, radix, bucket), and their properties. The theoretical lower bound for comparison-based sorting is Omega(n log n).

## Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable | In-place |
|-----------|------|---------|-------|-------|--------|----------|
| Insertion sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| Bubble sort | O(n) | O(n^2) | O(n^2) | O(1) | Yes | Yes |
| Selection sort | O(n^2) | O(n^2) | O(n^2) | O(1) | No | Yes |
| Heap sort | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Yes |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No |
| Quick sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | No | Yes |
| Counting sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes | No |
| Radix sort | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Yes | No |
| Bucket sort | O(n+k) | O(n+k) | O(n^2) | O(n+k) | Yes | No |

## Classification Properties

| Property | Definition |
|----------|-----------|
| **Stable** | Equal elements maintain original relative order |
| **In-place** | Uses O(1) auxiliary space |
| **Adaptive** | Faster on nearly-sorted input |
| **Online** | Can process input sequentially |
| **Comparison-based** | Uses only element comparisons to determine order |

## Key Facts

- **Lower bound for comparison sorts**: Omega(n log n) - proof via decision tree (n! leaves, tree height >= log2(n!) = Omega(n log n))
- **Non-comparison sorts** break this barrier using key structure (counting, radix, bucket)
- Python's `sorted()` and `.sort()` use **Timsort** (hybrid merge+insertion): O(n log n) worst, O(n) best, stable, adaptive

## Patterns

### Insertion Sort

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
```

Best for: small arrays, nearly-sorted data, online sorting. O(n) best case on sorted input.

### Selection Sort

```python
def selection_sort(arr):
    for i in range(len(arr)):
        pos_min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[pos_min]:
                pos_min = j
        arr[i], arr[pos_min] = arr[pos_min], arr[i]
```

Always O(n^2) regardless of input order. Not adaptive, not stable.

### Merge Sort

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

Recurrence: T(n) = 2T(n/2) + O(n) -> O(n log n). Recursion tree has log2(n) levels, each doing O(n) merge work. Stable but requires O(n) extra space.

### Quick Sort

```python
def quick_sort(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
```

O(n^2) worst case when pivot always worst (sorted array + always pick first/last). O(n log n) average. In practice faster than merge sort due to cache locality and small constants. Worst case rare with random or median-of-three pivot.

### Counting Sort

For integers in range [0, k). Time O(n + k), space O(k). Useful when k = O(n).

### Radix Sort

Sort by digits LSD to MSD using counting sort as subroutine. Time O(d(n+k)) where d = digits, k = digit range. For fixed-width integers: O(n).

### Python Built-in Sorting

```python
sorted(strs)                          # lexicographic
sorted(strs, key=len)                 # by length
sorted(strs, key=lambda s: s.count('c'))  # by custom criterion
sorted(products, key=lambda p: p['price'])  # by dict field
```

## Gotchas

- Quicksort worst case O(n^2) on already-sorted arrays with naive pivot (first/last element)
- Selection sort is NOT stable - long-range swaps displace equal elements
- Bubble sort with early termination flag becomes adaptive (O(n) on sorted input)
- Shell sort (gap-based insertion sort) achieves O(n log^2 n) with Hibbard gaps
- Counting sort requires non-negative integers in known range
- Bucket sort degrades to O(n^2) if all elements land in same bucket

## See Also

- [[complexity-analysis]] - understanding O-notation
- [[searching-algorithms]] - binary search requires sorted input
- [[functions]] - sorted() and sort() details
