---
title: Dynamic Programming
category: algorithms
tags: [dynamic-programming, memoization, tabulation, optimal-substructure, overlapping-subproblems]
---

# Dynamic Programming

## Key Facts

- **Dynamic programming (DP)** solves problems by breaking them into overlapping subproblems and storing results
- Two properties required: **optimal substructure** (optimal solution contains optimal sub-solutions) and **overlapping subproblems** (same subproblems recur)
- **Top-down (memoization)** - recursive with cache; easier to write, same complexity
- **Bottom-up (tabulation)** - iterative, fill table from base cases; no recursion overhead
- Transforms exponential brute-force into polynomial time by avoiding redundant computation
- Common patterns: 1D array, 2D grid, interval DP, knapsack, subsequence
- Related: [[recursion-and-backtracking]], [[graph-shortest-path]]

## Patterns

### Fibonacci (1D DP)

```python
# Brute force: O(2^n)
def fib_brute(n):
    if n <= 1: return n
    return fib_brute(n-1) + fib_brute(n-2)

# Memoization (top-down): O(n) time, O(n) space
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1: return n
    return fib_memo(n-1) + fib_memo(n-2)

# Tabulation (bottom-up): O(n) time, O(n) space
def fib_tab(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

# Space-optimized: O(n) time, O(1) space
def fib_opt(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### Minimum Cost Path in Grid (2D DP)

```python
def min_cost_path(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * m for _ in range(n)]

    dp[0][0] = matrix[0][0]

    # Fill first row
    for j in range(1, m):
        dp[0][j] = dp[0][j-1] + matrix[0][j]

    # Fill first column
    for i in range(1, n):
        dp[i][0] = dp[i-1][0] + matrix[i][0]

    # Fill rest
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + matrix[i][j]

    return dp[n-1][m-1]
# Time: O(n*m), Space: O(n*m) - vs brute force O(2^(n*m))
```

### 0/1 Knapsack

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]  # skip item i
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                    dp[i-1][w - weights[i-1]] + values[i-1])  # take item i
    return dp[n][capacity]
# Time: O(n * capacity), Space: O(n * capacity)
```

### Longest Common Subsequence (LCS)

```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
# Time: O(m*n), Space: O(m*n)
```

### Longest Increasing Subsequence (LIS)

```python
# O(n^2) DP
def lis(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# O(n log n) with binary search
import bisect
def lis_fast(nums):
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)
```

```java
// Java: coin change
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

## Gotchas

- **Greedy != DP** - greedy makes locally optimal choices (does not always give global optimum); DP explores all subproblems
- **Base cases** - forgetting or mis-defining base cases causes wrong results or index errors
- **Table dimensions** - dp table is often (n+1) x (m+1) to handle empty subsequence/zero capacity
- **Space optimization** - many 2D DP problems can be reduced to O(n) space by keeping only previous row
- **Memoization recursion depth** - Python's default limit is 1000; use `sys.setrecursionlimit()` or convert to bottom-up
- **State definition is everything** - clearly define what `dp[i]` or `dp[i][j]` represents before coding

## See Also

- [[recursion-and-backtracking]] - DP optimizes recursive solutions with overlapping subproblems
- [[graph-shortest-path]] - Floyd-Warshall is DP on graphs
- [[big-o-complexity-analysis]] - DP reduces exponential to polynomial
