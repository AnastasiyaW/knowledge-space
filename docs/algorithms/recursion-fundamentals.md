---
title: Recursion Fundamentals
category: concepts
tags: [recursion, call-stack, divide-and-conquer, memoization]
---

# Recursion Fundamentals

Function that calls itself to solve smaller instances of the same problem. Foundation for divide-and-conquer, DP, backtracking, and tree/graph traversal.

## Key Facts

- Every recursion needs: base case + recursive case
- Call stack stores local variables and return address for each call
- Stack depth = recursion depth. Python default limit: 1000 (`sys.setrecursionlimit()`)
- Tail recursion: recursive call is last operation. Python does NOT optimize tail calls
- Any recursion can be converted to iteration using explicit stack
- Time complexity: solve recurrence relation (Master Theorem for divide-and-conquer)

## Structure

```python
def recursive_function(problem):
    # Base case - termination condition
    if is_trivial(problem):
        return trivial_solution

    # Recursive case - break into smaller subproblems
    smaller = reduce(problem)
    sub_result = recursive_function(smaller)

    # Combine
    return combine(sub_result)
```

## Patterns

### Linear Recursion

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
# T(n) = T(n-1) + O(1) -> O(n)
```

### Binary Recursion (Divide and Conquer)

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
# T(n) = 2T(n/2) + O(n) -> O(n log n)
```

### Tree Recursion (Multiple Branches)

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
# T(n) = T(n-1) + T(n-2) -> O(2^n) without memoization
```

### Recursion to Iteration

```python
# Recursive DFS
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# Iterative DFS (explicit stack)
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
```

### Memoization (Caching Overlapping Subproblems)

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
# O(2^n) -> O(n) with memoization
```

### Manual Memoization

```python
def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

## Master Theorem (Divide and Conquer Recurrences)

For `T(n) = aT(n/b) + O(n^d)`:

| Condition | Complexity |
|-----------|-----------|
| d > log_b(a) | O(n^d) |
| d = log_b(a) | O(n^d * log n) |
| d < log_b(a) | O(n^(log_b(a))) |

Examples:
- Binary search: T(n) = T(n/2) + O(1) -> a=1, b=2, d=0 -> O(log n)
- Merge sort: T(n) = 2T(n/2) + O(n) -> a=2, b=2, d=1 -> O(n log n)
- Karatsuba multiply: T(n) = 3T(n/2) + O(n) -> O(n^1.585)

## Recursion vs Iteration Trade-offs

| Aspect | Recursion | Iteration |
|--------|-----------|-----------|
| Readability | Often cleaner for trees/graphs | Cleaner for linear problems |
| Stack usage | O(depth) call stack | O(1) or explicit stack |
| Performance | Function call overhead | Generally faster |
| Stack overflow | Risk at depth > 1000 | No risk |
| State management | Implicit via call stack | Explicit variables |

## Gotchas

- **Issue:** Stack overflow from deep recursion in Python (default limit 1000) -> **Fix:** Use `sys.setrecursionlimit(N)` cautiously, or convert to iterative with explicit stack. For DP, prefer bottom-up tabulation.
- **Issue:** Exponential time from recomputing overlapping subproblems -> **Fix:** Add memoization (`@lru_cache` or manual dict). If subproblems overlap, recursion without memoization is a bug.
- **Issue:** Mutable default arguments as memo dict persist across calls -> **Fix:** Use `memo=None` pattern with `if memo is None: memo = {}` inside function body.

## See Also

- [[dynamic-programming-fundamentals]] - recursion + memoization = top-down DP
- [[backtracking]] - recursion with pruning
- [[graph-traversal-bfs-dfs]] - DFS is recursive graph traversal
- [[complexity-analysis]] - recurrence relations for recursive complexity
