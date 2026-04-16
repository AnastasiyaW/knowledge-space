---
title: Complexity Analysis
category: concepts
tags: [algorithms, big-o, time-complexity, space-complexity, asymptotic-analysis]
---

# Complexity Analysis

Complexity analysis measures how algorithm resource usage (time or space) scales with input size n. It abstracts away hardware and language, focusing on asymptotic growth rates. The core notations are Big-O (upper bound), Big-Omega (lower bound), and Big-Theta (tight bound).

## Key Facts

- **Time complexity** = count of operations as function of n, classified by asymptotic growth
- **Space complexity** = auxiliary memory beyond input (convention: report auxiliary, not total)
- Drop constants: O(2n) = O(n), O(100n) = O(n)
- Keep only dominant term: O(n^2 + 100n + 12) = O(n^2)
- Multiple parameters possible: O(n * m) when inputs have different sizes
- **Hidden constant factors** matter in practice - two O(n) algorithms can differ by 100x

## Complexity Hierarchy

```text
O(1) < O(log n) < O(sqrt(n)) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)
```

| Class | Example |
|-------|---------|
| O(1) | Array index access, check even/odd with `n & 1` |
| O(log n) | Binary search, sum of digits, number of digits |
| O(sqrt(n)) | Loop `while i*i < n` |
| O(n) | Linear search, array min/max |
| O(n log n) | Merge sort, optimal comparison-based sorting |
| O(n^2) | Selection sort, brute-force two-sum, all pairs |
| O(n^3) | Naive matrix multiplication |
| O(2^n) | Recursive LCS without memoization |
| O(n!) | Generating all permutations |

## Notation

| Symbol | Meaning | Describes |
|--------|---------|-----------|
| O(f(n)) | Tight upper bound | Worst case (and below) |
| Omega(f(n)) | Tight lower bound | Best case (and above) |
| Theta(f(n)) | Exact bound | Both upper and lower |
| o(f(n)) | Strict upper bound | Grows strictly slower than f |
| omega(f(n)) | Strict lower bound | Grows strictly faster than f |

Best, average, and worst case are independent of Big-O/Omega/Theta - each case has its own T(n) which can be bounded separately.

## Patterns

### Counting Operations from Code

```python
# Single loop: O(n)
for elem in arr:
    process(elem)

# Nested loops: O(n^2)
for i in range(n):
    for j in range(n):
        process(i, j)

# Doubling step: i = 1, 2, 4, 8, ... n -> O(log n)
i = 1
while i < n:
    i *= 2

# Square root pattern: i*i < n -> O(sqrt(n))
i = 0
while i * i < n:
    i += 1

# Triangular loops: sum 0+1+2+...+(n-1) = n(n-1)/2 -> O(n^2)
for i in range(1, n + 1):
    for j in range(i):
        process(j)

# Inner loop depends on i^2: total = sum of i^2 = O(n^3)
for i in range(n):
    for j in range(i * i):
        process(j)

# Conditional inner loop at i == n//2 only: O(n) + O((n/2)^2) = O(n^2)
for i in range(n):
    if i == n // 2:
        for j in range(i * i):
            process(j)

# Conditional at constant i == 10: O(n) + O(100) = O(n)
for i in range(n):
    if i == 10:
        for j in range(i * i):
            process(j)
```

### Space Complexity Traps

```python
# String concatenation creates new string: O(len(s1) + len(s2))
result = str1 + str2

# Building prefixes: total space O(n^2)
prefixes = [s[0:i] for i in range(len(s))]

# Reference vs copy
copy = arr        # O(1) - same object, NOT a copy
copy = arr.copy() # O(n) - actual copy

# Fixed-size array is O(1) space
occurrences = [0] * 26  # constant regardless of input
```

### Multiple Parameters

```python
# O(n * m) where n = len(arr1), m = len(arr2)
def intersection(arr1, arr2):
    for elem in arr1:
        if elem in arr2:  # O(m) scan each time
            print(elem)

# O(min(n, m)) - loop terminates at shorter
def where_equal(str1, str2):
    i = 0
    while i < len(str1) and i < len(str2):
        if str1[i] == str2[i]:
            yield i
        i += 1
```

## Best, Average, Worst Case

- **Best case:** Most favorable input (e.g., element at index 0 for linear search)
- **Worst case:** Least favorable input (e.g., element not found)
- **Average case:** Expected cost over all possible inputs; requires probability assumptions
- A **randomized algorithm** uses internal randomness to convert worst-case to expected average

## Gotchas

- Two O(n) algorithms can have 100x runtime difference due to constants
- An O(n log n) algorithm with constant 13 can be slower than O(n^2) with constant 0.5 for n < 200
- O(n^2) vs O(m^2) are incomparable without knowing relationship between n and m
- Sum of digits of n has O(log n) complexity (n has floor(log10(n))+1 digits)
- `max(n, 10)` in loop condition: O(n) for large n, O(1) for n < 10
- `min(n, 10)` in loop condition: always O(1) regardless of n

## See Also

- [[amortized-analysis]] - average cost per operation over sequences
- [[complexity-classes]] - P, NP, NP-complete, NP-hard
- [[sorting-algorithms]] - complexity comparison of sorting methods
