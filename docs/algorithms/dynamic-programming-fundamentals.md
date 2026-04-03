---
title: Dynamic Programming Fundamentals
category: concepts
tags: [algorithms, dynamic-programming, memoization, tabulation, optimization]
---

# Dynamic Programming Fundamentals

Dynamic programming (DP) solves problems by breaking them into overlapping subproblems and storing results to avoid recomputation. It applies when a problem has optimal substructure (optimal solution from optimal sub-solutions) and overlapping subproblems (same subproblems solved repeatedly in naive recursion).

## Key Facts

- **Top-down (memoization)**: Recursive + cache, computes only needed subproblems
- **Bottom-up (tabulation)**: Iterative, fills table from base cases, no recursion overhead
- DP reduces exponential recursion to polynomial by caching - typically from O(2^n) to O(n*m) or O(n^2)
- Start with memoization to validate logic, then convert to tabulation for performance
- Space optimization often possible by keeping only the last 1-2 rows/values

## Top-Down vs Bottom-Up

| | Top-Down (Memoization) | Bottom-Up (Tabulation) |
|-|----------------------|----------------------|
| Implementation | Recursive - natural from recurrence | Iterative - requires figuring out fill order |
| Subproblems computed | Only needed ones | All subproblems |
| Overhead | Call stack, dictionary lookup | Array access (faster) |
| Stack overflow | Risk for deep recursion | No risk |
| Space optimization | Harder | Easier (row-by-row) |

## Patterns

### Identifying DP Recurrence

1. Define what `dp[state]` represents (be precise about what it means)
2. Write base cases
3. Write recurrence: `dp[state] = f(dp[smaller_states])`
4. Identify traversal order so dependencies are resolved before use
5. Return target state

### Running Example: Min Cost Path in Matrix

Move only right or down from top-left to bottom-right, minimizing total cost.

**Naive Recursive - O(2^(n+m)):**

```python
def min_cost(matrix, i=0, j=0):
    n, m = len(matrix), len(matrix[0])
    if i == n or j == m:
        return float('inf')
    if i == n - 1 and j == m - 1:
        return matrix[i][j]
    return matrix[i][j] + min(min_cost(matrix, i + 1, j),
                               min_cost(matrix, i, j + 1))
```

**Top-Down (Memoization) - O(n*m):**

```python
def min_cost(matrix, i=0, j=0, memo=None):
    if memo is None:
        memo = {}
    if (i, j) in memo:
        return memo[(i, j)]
    n, m = len(matrix), len(matrix[0])
    if i == n or j == m:
        return float('inf')
    if i == n - 1 and j == m - 1:
        return matrix[i][j]
    memo[(i, j)] = matrix[i][j] + min(
        min_cost(matrix, i + 1, j, memo),
        min_cost(matrix, i, j + 1, memo)
    )
    return memo[(i, j)]
```

**Bottom-Up (Tabulation) - O(n*m):**

```python
def min_cost(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * m for _ in range(n)]
    dp[n - 1][m - 1] = matrix[n - 1][m - 1]

    for j in range(m - 2, -1, -1):  # last row
        dp[n - 1][j] = matrix[n - 1][j] + dp[n - 1][j + 1]
    for i in range(n - 2, -1, -1):  # last column
        dp[i][m - 1] = matrix[i][m - 1] + dp[i + 1][m - 1]
    for i in range(n - 2, -1, -1):  # rest
        for j in range(m - 2, -1, -1):
            dp[i][j] = matrix[i][j] + min(dp[i + 1][j], dp[i][j + 1])

    return dp[0][0]
```

### Counting Paths in Grid

```python
def count_paths(n, m):
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        dp[i][0] = 1
    for j in range(m):
        dp[0][j] = 1
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[n - 1][m - 1]
```

Mathematical formula: C(n+m-2, n-1) - choose which steps are downward.

## Gotchas

- Greedy often fails where DP succeeds - always moving to cheapest neighbor can miss global optimum
- Top-down with Python dicts can be slow for large state spaces - tabulation with arrays is faster
- Python recursion limit (default 1000) can crash top-down DP on large inputs - use `sys.setrecursionlimit` or convert to bottom-up
- Mutable default arguments trap: use `None` default + initialize inside function
- Space optimization (keeping only last row) prevents reconstructing the actual solution path

## See Also

- [[dp-sequence-problems]] - LCS, edit distance, LIS, word break
- [[dp-optimization-problems]] - knapsack, coin change, house robber
- [[dp-grid-problems]] - matrix path, maximal square, gold mine
- [[complexity-analysis]] - understanding DP complexity reduction
