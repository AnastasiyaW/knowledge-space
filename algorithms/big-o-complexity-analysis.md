---
title: Big-O and Complexity Analysis
category: fundamentals
tags: [big-o, time-complexity, space-complexity, asymptotic-analysis, algorithm-analysis]
---

# Big-O and Complexity Analysis

## Key Facts

- **Big-O notation** describes the upper bound of an algorithm's growth rate as input size approaches infinity
- Measures how runtime/space scales with input size `n`, ignoring constants and lower-order terms
- Common complexities (fastest to slowest): O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!)
- **Time complexity** - number of operations as a function of input size
- **Space complexity** - memory used as a function of input size (includes call stack for recursion)
- **Amortized analysis** - average cost per operation over a sequence (e.g., [[arrays-and-strings]] resize is O(1) amortized)
- Best/Average/Worst case are separate from Big-O/Omega/Theta notation
- Related: [[big-o-complexity-analysis]], [[divide-and-conquer]]

## Patterns

### Common Complexity Classes

```python
# O(1) - Constant: array access, hash table lookup
def get_first(arr):
    return arr[0]

# O(log n) - Logarithmic: binary search, balanced BST operations
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

# O(n) - Linear: single pass, linear search
def find_max(arr):
    return max(arr)

# O(n log n) - Linearithmic: efficient sorting (merge sort, heap sort)
# O(n^2) - Quadratic: nested loops, bubble sort, insertion sort
# O(2^n) - Exponential: recursive subsets, brute-force combinations
# O(n!) - Factorial: permutations
```

### Identifying Complexity from Code Structure

```python
# Single loop over n elements -> O(n)
for i in range(n): ...

# Nested loops -> O(n^2)
for i in range(n):
    for j in range(n): ...

# Loop with halving -> O(log n)
while n > 1:
    n //= 2

# Loop * halving -> O(n log n)
for i in range(n):
    j = n
    while j > 1:
        j //= 2

# Recursive with two branches -> O(2^n)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

```java
// Space complexity: recursive calls consume stack
// O(n) space for linear recursion
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1); // n stack frames
}

// O(log n) space for divide-and-conquer with halving
void mergeSort(int[] arr, int lo, int hi) {
    if (lo >= hi) return;
    int mid = (lo + hi) / 2;
    mergeSort(arr, lo, mid);
    mergeSort(arr, mid + 1, hi);
    merge(arr, lo, mid, hi);
}
```

## Gotchas

- **Hash table operations are O(1) average, O(n) worst case** - hash collisions can degrade to linear scan
- **String comparison is O(k)** where k is string length, not O(1) - affects overall complexity of string-based algorithms
- **Space complexity includes the call stack** - recursive merge sort uses O(n) extra for merge + O(log n) for stack = O(n)
- **Amortized != average** - amortized is guaranteed over sequences; average depends on input distribution
- **Drop constants only for Big-O** - in practice, O(n) with constant 1000 is slower than O(n log n) with constant 2 for small n
- **log base does not matter in Big-O** - log_2(n) and log_10(n) differ by a constant factor

## See Also

- [[sorting-algorithms]] - comparative analysis of sort complexities
- [[recursion-and-backtracking]] - recursive space complexity
- [[dynamic-programming]] - optimizing exponential to polynomial
