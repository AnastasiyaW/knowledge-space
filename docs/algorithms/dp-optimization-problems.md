---
title: "DP: Optimization Problems"
category: algorithms
tags: [algorithms, dynamic-programming, knapsack, coin-change, subset-sum, optimization]
---

# DP: Optimization Problems

Classic DP optimization problems: House Robber, Coin Change, 0-1 Knapsack, Subset Sum, Rod Cutting, Minimum Ticket Cost, and Matrix Chain Multiplication. These share the pattern of choosing to include or exclude items/actions to optimize an objective.

## Key Facts

- **House Robber**: O(n) time, O(1) space (only need previous two values)
- **Coin Change**: O(amount * |coins|) time, O(amount) space
- **0-1 Knapsack**: O(n*W) time, reducible to O(W) space with backward iteration
- **Subset Sum**: O(n*target) time, O(target) space - boolean variant of knapsack
- **Matrix Chain**: O(n^3) time, O(n^2) space - interval DP
- Knapsack and subset sum are NP-complete but have pseudo-polynomial DP solutions

## Patterns

### House Robber - O(n) time, O(1) space

Rob max total without robbing adjacent houses. At each house: rob it (skip next) or skip.

```python
def rob(arr):
    n = len(arr)
    if n == 1:
        return arr[0]
    before_prev = arr[0]
    prev = max(arr[0], arr[1])
    for i in range(2, n):
        curr = max(prev, arr[i] + before_prev)
        before_prev = prev
        prev = curr
    return prev
```

Example: `[4, 8, 12, 1, 2, 10, 3, 6, 8]` -> dp: `[4, 8, 16, 16, 18, 26, 26, 32, 34]` -> answer 34

### Coin Change (Minimum Coins)

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for amt in range(1, amount + 1):
        for coin in coins:
            if coin <= amt and dp[amt - coin] + 1 < dp[amt]:
                dp[amt] = dp[amt - coin] + 1
    return dp[amount] if dp[amount] != float('inf') else -1
```

### 0-1 Knapsack

n items with weight/value, capacity W. Each item used at most once.

```python
def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]  # don't take
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               values[i - 1] + dp[i - 1][w - weights[i - 1]])
    return dp[n][W]
```

**Space-optimized to O(W)** by iterating weights backwards:

```python
def knapsack_opt(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):  # backward!
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]
```

### Subset Sum

Can we select a subset summing to target? Boolean variant of knapsack.

```python
def subset_sum(arr, target):
    dp = [False] * (target + 1)
    dp[0] = True
    for x in arr:
        for s in range(target, x - 1, -1):  # backward to use each item once
            dp[s] = dp[s] or dp[s - x]
    return dp[target]
```

### Rod Cutting

Given rod of length n and price for each length, maximize revenue.

```python
def rod_cutting(prices, n):
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            dp[length] = max(dp[length], prices[cut - 1] + dp[length - cut])
    return dp[n]
```

### Minimum Ticket Cost

Travel days and ticket prices (1-day, 7-day, 30-day passes).

```python
def min_cost_tickets(days, costs):
    day_set = set(days)
    max_day = max(days)
    dp = [0] * (max_day + 1)
    for d in range(1, max_day + 1):
        if d not in day_set:
            dp[d] = dp[d - 1]
        else:
            dp[d] = min(
                dp[d - 1] + costs[0],
                dp[max(0, d - 7)] + costs[1],
                dp[max(0, d - 30)] + costs[2]
            )
    return dp[max_day]
```

### Matrix Chain Multiplication - O(n^3)

Optimal parenthesization to minimize multiplication cost.

```python
def matrix_chain(dims):
    n = len(dims)
    cost = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float('inf')
            for k in range(i, j):
                c = (cost[i][k] + cost[k + 1][j] +
                     dims[i][0] * dims[k][1] * dims[j][1])
                cost[i][j] = min(cost[i][j], c)
    return cost[0][n - 1]
```

### Gold Mine - O(n*m)

Start from any cell in column 0, move to adjacent cells in next column. Maximize gold.

```python
def gold(mine):
    n, m = len(mine), len(mine[0])
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        dp[i][m - 1] = mine[i][m - 1]
    for j in range(m - 2, -1, -1):
        for i in range(n):
            best = dp[i][j + 1]
            if i > 0:
                best = max(best, dp[i - 1][j + 1])
            if i < n - 1:
                best = max(best, dp[i + 1][j + 1])
            dp[i][j] = mine[i][j] + best
    return max(dp[i][0] for i in range(n))
```

## Gotchas

- **Backward iteration** in subset sum/knapsack prevents reusing items (0-1 constraint). Forward iteration = unbounded knapsack
- Coin change returns -1 if amount unreachable (check for infinity)
- Matrix chain: interval DP fills by increasing interval length, not row-by-row
- Rod cutting is unbounded (same length can be cut multiple times) - forward iteration is correct here
- House robber O(1) space: only need `before_prev` and `prev`, not full dp array

## See Also

- [[dynamic-programming-fundamentals]] - DP concepts and approach
- [[dp-grid-problems]] - grid-based DP problems
- [[dp-sequence-problems]] - string and sequence DP
- [[complexity-classes]] - knapsack and subset sum are NP-complete with pseudo-polynomial solutions
