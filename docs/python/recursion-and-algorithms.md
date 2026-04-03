---
title: Recursion and Algorithm Basics
category: concepts
tags: [python, recursion, algorithms, big-o, binary-search, sorting, memoization]
---

# Recursion and Algorithm Basics

Recursion is when a function calls itself. Every recursive function needs a base case (stop condition) and a recursive case (moving toward the base). Understanding Big O notation helps choose the right algorithm for the data size.

## Key Facts

- Python's default recursion limit is 1000 (`sys.getrecursionlimit()`)
- Python does NOT optimize tail recursion - convert to iteration for deep recursion
- `@lru_cache` turns exponential Fibonacci O(2^n) into linear O(n)
- Big O describes how performance scales with input size
- Python's `sorted()` uses Timsort - O(n log n) hybrid of merge sort and insertion sort

## Patterns

### Classic Recursion
```python
def factorial(n):
    if n <= 1:       # base case
        return 1
    return n * factorial(n - 1)  # recursive case

def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)  # exponential without memoization!
```

### Memoized Fibonacci
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

fib(100)  # instant, O(n)
```

### Binary Search (Recursive)
```python
def binary_search(arr, target, low=0, high=None):
    if high is None: high = len(arr) - 1
    if low > high: return -1
    mid = (low + high) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)
```

### Flatten Nested List
```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
```

### Tree Traversal
```python
def tree_sum(node):
    if node is None: return 0
    return node.value + tree_sum(node.left) + tree_sum(node.right)
```

### Converting Recursion to Iteration
```python
# Recursive DFS
def dfs(node):
    if node is None: return
    print(node.value)
    dfs(node.left)
    dfs(node.right)

# Iterative DFS with explicit stack
def dfs_iterative(root):
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None: continue
        print(node.value)
        stack.append(node.right)
        stack.append(node.left)
```

### Tail Recursion (Accumulator Pattern)
```python
# Not tail recursive (multiplication after recursive call)
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)

# Tail recursive (but Python doesn't optimize it)
def factorial(n, acc=1):
    if n <= 1: return acc
    return factorial(n - 1, acc * n)

# Iterative (best for Python)
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

## Big O Notation

| Complexity | Name | Example |
|-----------|------|---------|
| O(1) | Constant | Hash table lookup, dict/set access |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | List iteration, linear search |
| O(n log n) | Linearithmic | Efficient sorting (merge, Timsort) |
| O(n^2) | Quadratic | Nested loops, bubble sort |
| O(2^n) | Exponential | Naive recursive Fibonacci |

## When to Use Recursion vs Iteration

**Recursion**: tree/graph traversal, divide-and-conquer (merge sort, quicksort), naturally recursive structures, bounded depth.

**Iteration**: simple loops, depth could exceed ~500, performance matters, iterative solution equally clear.

## Gotchas

- Missing base case -> infinite recursion -> `RecursionError`
- Naive Fibonacci recalculates same values exponentially - always memoize
- Python recursion limit (1000) is intentionally low - use iteration for deep recursion
- Modifying mutable arguments (lists/dicts) shared across recursive calls causes bugs
- `sys.setrecursionlimit(n)` exists but signals a design problem

## See Also

- [[functions]] - function call mechanics
- [[iterators-and-generators]] - lazy sequences as iteration alternative
- [[profiling-and-optimization]] - measuring algorithm performance
