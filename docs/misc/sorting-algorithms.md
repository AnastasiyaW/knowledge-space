---
title: Sorting Algorithms - Bubble, Selection, Insertion, Quicksort
category: concepts
tags: [misc, algorithms, sorting, quicksort, complexity]
---

# Sorting Algorithms - Bubble, Selection, Insertion, Quicksort

Comparison of fundamental sorting algorithms with implementations, complexity analysis, and practical trade-offs. Includes quickselect for finding kth element without full sort.

## Key Facts

- Quicksort O(N log N) average is used in most standard library sort functions
- Insertion sort O(N) on nearly sorted data makes it ideal for small/mostly-sorted arrays
- Selection sort does fewer swaps than bubble sort (at most N-1) but same O(N^2) comparisons
- Quicksort worst case O(N^2) occurs on already-sorted arrays with naive pivot selection
- Quickselect finds kth smallest/largest in O(N) average without full sort

## Patterns

### Bubble Sort - O(N^2)

Each pass: compare adjacent pairs, swap if out of order. Largest unsorted element "bubbles" to end.

```python
def bubble_sort(list):
    unsorted_until_index = len(list) - 1
    sorted = False
    while not sorted:
        sorted = True
        for i in range(unsorted_until_index):
            if list[i] > list[i+1]:
                list[i], list[i+1] = list[i+1], list[i]
                sorted = False
        unsorted_until_index -= 1
    return list
```

### Selection Sort - O(N^2)

Each pass: find minimum in unsorted portion, swap to front. ~N^2/2 comparisons, at most N-1 swaps.

```javascript
function selectionSort(array) {
  for (let i = 0; i < array.length - 1; i++) {
    let lowestNumberIndex = i;
    for (let j = i + 1; j < array.length; j++) {
      if (array[j] < array[lowestNumberIndex]) {
        lowestNumberIndex = j;
      }
    }
    if (lowestNumberIndex != i) {
      let temp = array[i];
      array[i] = array[lowestNumberIndex];
      array[lowestNumberIndex] = temp;
    }
  }
  return array;
}
```

### Insertion Sort

| Case | Complexity |
|------|-----------|
| Best (nearly sorted) | O(N) |
| Average | O(N^2) |
| Worst (reverse sorted) | O(N^2) |

Maintain sorted left portion. For each new element, shift right until correct position found.

### Quicksort - O(N log N) average

Partitioning: pick pivot, arrange elements so left < pivot < right. Recursively sort subarrays.

```ruby
class SortableArray
  def partition!(left_index, right_index)
    pivot_index = right_index
    pivot = @array[pivot_index]
    right_index -= 1
    loop do
      left_index += 1 while @array[left_index] < pivot
      right_index -= 1 while @array[right_index] > pivot
      break if left_index >= right_index
      @array[left_index], @array[right_index] = @array[right_index], @array[left_index]
    end
    @array[left_index], @array[pivot_index] = @array[pivot_index], @array[left_index]
    left_index
  end

  def quicksort!(left_index, right_index)
    return if right_index - left_index <= 0
    pivot_index = partition!(left_index, right_index)
    quicksort!(left_index, pivot_index - 1)
    quicksort!(pivot_index + 1, right_index)
  end
end
```

**Why O(N log N)**: log N partition rounds x N comparisons per round.
**Worst case O(N^2)**: pivot always lands at edge (already sorted). Fix: random pivot or median-of-three.

### Quickselect - O(N) average

Find kth smallest/largest without full sort. After each partition, pivot is in final position. Only recurse into the half containing target index.

### Comparison

| Algorithm | Best | Average | Worst | Swaps |
|-----------|------|---------|-------|-------|
| Bubble Sort | O(N) | O(N^2) | O(N^2) | Many |
| Selection Sort | O(N^2) | O(N^2) | O(N^2) | <= N-1 |
| Insertion Sort | O(N) | O(N^2) | O(N^2) | Moderate |
| Quicksort | O(N log N) | O(N log N) | O(N^2) | Moderate |

## Gotchas

- Quicksort is not stable (equal elements may change relative order); use mergesort if stability required
- Already-sorted input is quicksort's worst case with rightmost pivot selection
- Insertion sort's O(N) best case makes it the practical choice for small subarrays (often used as base case in quicksort)
- Selection sort's advantage is minimal write operations - useful when writes are expensive

## See Also

- [[data-structures-fundamentals]] - Big O analysis, arrays
- [[trees-and-graphs]] - heap sort via priority queue
- [[algorithm-problem-patterns]] - when to sort as preprocessing step
