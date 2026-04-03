---
title: "DP: Grid and Combinatorics Problems"
category: algorithms
tags: [algorithms, dynamic-programming, grid, matrix, partition, combinatorics]
---

# DP: Grid and Combinatorics Problems

Grid-based and combinatorial DP problems: Partition Problem, Maximal Square, Count Sorted Vowel Strings, and counting patterns. These combine subset selection with geometric or counting constraints.

## Key Facts

- **Partition Problem**: Reduce to subset sum with target = total/2. O(n * sum) time
- **Maximal Square**: dp[i][j] = 1 + min(left, above, diagonal). O(nm) time
- **Count Sorted Vowel Strings**: Stars and bars = C(n+4, 4), or DP with prefix sums
- Partition problem is NP-complete but has pseudo-polynomial DP solution

## Patterns

### Partition Problem

Split array into two subsets with equal sum. Reduces to: does any subset sum to total/2?

```python
def partition(arr):
    s = sum(arr)
    if s % 2 == 1:
        return False  # odd sum impossible
    target = s // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in arr:
        for t in range(target, x - 1, -1):  # backward: use each item once
            dp[t] = dp[t] or dp[t - x]
    return dp[target]
```

**Why iterate backwards:** Ensures each element is used at most once. Forward iteration would allow reusing the same element (unbounded variant).

### Maximal Square of Ones - O(nm)

Find area of largest square submatrix containing only 1s.

**Recurrence:**
```
if matrix[i][j] == 0: dp[i][j] = 0
else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```

Why min of three: to form a square of side k at (i,j), we need squares of side k-1 above, to the left, and diagonally. The bottleneck is the smallest.

```python
def maximal_square(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * m for _ in range(n)]
    max_side = 0
    for j in range(m):
        dp[0][j] = matrix[0][j]
    for i in range(n):
        dp[i][0] = matrix[i][0]
    for i in range(1, n):
        for j in range(1, m):
            if matrix[i][j] == 0:
                dp[i][j] = 0
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
            max_side = max(max_side, dp[i][j])
    return max_side ** 2  # area
```

### Count Sorted Vowel Strings

Count strings of length n using vowels a,e,i,o,u in non-decreasing order.

```python
def count_vowel_strings(n):
    dp = [1] * 5  # length 1: one string per vowel
    for _ in range(1, n):
        new_dp = [0] * 5
        for v in range(5):
            new_dp[v] = sum(dp[:v + 1])  # can use same or earlier vowel
        dp = new_dp
    return sum(dp)
```

Mathematical shortcut: C(n+4, 4) (stars and bars).

### General Combinatorics DP Patterns

**Counting paths in DAG:**
```python
dp[v] = sum(dp[u] for all u with edge u -> v)
```

**Counting bit strings with constraints:**
```python
dp[i][last] = count of valid strings of length i ending with `last`
```

**Counting partitions of n into k parts:**
```python
dp[n][k] = dp[n-1][k-1] + dp[n-k][k]
```

## Gotchas

- Partition: total sum must be even, otherwise immediately return False
- Maximal square: don't forget base cases (first row and first column copied directly)
- Maximal square returns area (side^2), not side length
- Space optimization to O(m) with two-row trick is possible for both grid problems
- Memoization version of partition uses state (index, remaining_sum), not (index, sum1, sum2)

## See Also

- [[dp-optimization-problems]] - subset sum, knapsack (closely related to partition)
- [[dynamic-programming-fundamentals]] - DP approach and top-down vs bottom-up
- [[dp-sequence-problems]] - string-based DP patterns
