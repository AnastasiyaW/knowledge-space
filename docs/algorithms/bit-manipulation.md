---
title: Bit Manipulation
category: concepts
tags: [bitwise, binary, optimization, low-level]
---

# Bit Manipulation

Operations on individual bits of integers. Critical for optimization, cryptography, networking, and competitive programming.

## Key Facts

- Bitwise AND (`&`): both bits 1 -> 1
- Bitwise OR (`|`): either bit 1 -> 1
- Bitwise XOR (`^`): bits differ -> 1
- Bitwise NOT (`~`): flip all bits (two's complement: `~x = -x - 1`)
- Left shift (`<<`): multiply by 2^n
- Right shift (`>>`): divide by 2^n (arithmetic shift preserves sign)
- Python integers have arbitrary precision - no overflow

## Essential Tricks

```python
# Check if n-th bit is set
(x >> n) & 1

# Set n-th bit
x | (1 << n)

# Clear n-th bit
x & ~(1 << n)

# Toggle n-th bit
x ^ (1 << n)

# Check if power of 2
x > 0 and (x & (x - 1)) == 0

# Count set bits (Brian Kernighan)
def count_bits(n):
    count = 0
    while n:
        n &= n - 1  # clears lowest set bit
        count += 1
    return count

# Lowest set bit
x & (-x)

# Clear lowest set bit
x & (x - 1)

# Check if even/odd
x & 1  # 0 = even, 1 = odd

# Swap without temp
a ^= b; b ^= a; a ^= b

# Two's complement negation
-x == ~x + 1
```

## Patterns

### Single Number (XOR)

```python
def single_number(nums):
    """Every element appears twice except one. Find it."""
    result = 0
    for n in nums:
        result ^= n
    return result
# XOR properties: a ^ a = 0, a ^ 0 = a, commutative + associative
```

### Missing Number

```python
def missing_number(nums):
    """Array [0..n] with one missing."""
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)

# XOR approach
def missing_number_xor(nums):
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```

### Power Set via Bitmask

```python
def subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    return result
```

### Counting Bits for All Numbers 0..N

```python
def count_bits_array(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### Bitmask DP (Traveling Salesman)

```python
def tsp(dist):
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])

    full = (1 << n) - 1
    return min(dp[full][u] + dist[u][0] for u in range(n))
```

## Common Bit Patterns

| Operation | Expression | Result |
|-----------|-----------|--------|
| Is power of 2 | `n & (n-1) == 0` | True if power of 2 |
| Rightmost set bit | `n & (-n)` | Isolates lowest 1 |
| Turn off rightmost 1 | `n & (n-1)` | Clears lowest 1 |
| All 1s of length k | `(1 << k) - 1` | Binary: 0..01..1 |
| Is n-th bit set | `(x >> n) & 1` | 0 or 1 |

## Gotchas

- **Issue:** Python `~x` returns `-(x+1)` due to arbitrary precision integers (no fixed-width) -> **Fix:** For fixed-width behavior, mask with `~x & 0xFFFFFFFF` for 32-bit.
- **Issue:** Signed right shift extends sign bit, unsigned right shift does not -> **Fix:** Python only has arithmetic (signed) right shift. For unsigned behavior on negative numbers, convert to unsigned first: `(x & 0xFFFFFFFF) >> n`.
- **Issue:** Bitmask DP memory explosion for large N -> **Fix:** Bitmask DP is practical only for N <= 20-25 (2^N states). For larger N, use other approaches.

## See Also

- [[complexity-analysis]] - bit manipulation often achieves O(1) or O(log N) per operation
- [[dynamic-programming-fundamentals]] - bitmask DP combines bits with DP
- [[traveling-salesman-problem]] - classic bitmask DP application
