---
title: Divide and Conquer
category: algorithms
tags: [divide-and-conquer, merge-sort, quick-sort, binary-search, master-theorem]
---

# Divide and Conquer

## Key Facts

- **Divide and Conquer** - break problem into smaller subproblems, solve recursively, combine results
- Three steps: **Divide** (split), **Conquer** (solve subproblems), **Combine** (merge results)
- **Master Theorem** for recurrence T(n) = a*T(n/b) + O(n^d):
  - If d < log_b(a): T(n) = O(n^(log_b a))
  - If d = log_b(a): T(n) = O(n^d * log n)
  - If d > log_b(a): T(n) = O(n^d)
- Key examples: [[sorting-algorithms]] O(n log n), [[binary-search]] O(log n), [[sorting-algorithms]] O(n log n) average
- Differs from DP: D&C subproblems are independent (no overlap); DP subproblems overlap
- Related: [[sorting-algorithms]], [[binary-search]], [[recursion-and-backtracking]]

## Patterns

### Maximum Subarray (Divide and Conquer)

```python
def max_subarray_dc(nums, lo, hi):
    if lo == hi:
        return nums[lo]

    mid = (lo + hi) // 2
    left_max = max_subarray_dc(nums, lo, mid)
    right_max = max_subarray_dc(nums, mid + 1, hi)

    # Max crossing subarray
    left_sum = float('-inf')
    total = 0
    for i in range(mid, lo - 1, -1):
        total += nums[i]
        left_sum = max(left_sum, total)
    right_sum = float('-inf')
    total = 0
    for i in range(mid + 1, hi + 1):
        total += nums[i]
        right_sum = max(right_sum, total)

    return max(left_max, right_max, left_sum + right_sum)
# T(n) = 2T(n/2) + O(n) -> O(n log n)
# Note: Kadane's algorithm is O(n) and simpler
```

### Power Function (Fast Exponentiation)

```python
def power(base, exp):
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = power(base, exp // 2)
        return half * half
    else:
        return base * power(base, exp - 1)
# O(log n) multiplications instead of O(n)
```

### Merge Sort (Classic D&C)

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])      # Divide
    right = merge_sort(arr[mid:])     # Divide
    return merge(left, right)          # Combine
# T(n) = 2T(n/2) + O(n) -> O(n log n)
```

### Count Inversions

```python
def count_inversions(arr):
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    merged = []
    inversions = left_inv + right_inv
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i  # all remaining left > right[j]
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions
# O(n log n) - counting inversions in merge step
```

```java
// Java: fast power
public long power(long base, long exp, long mod) {
    long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp % 2 == 1)
            result = result * base % mod;
        exp /= 2;
        base = base * base % mod;
    }
    return result;
}
```

## Gotchas

- **D&C vs DP** - if subproblems overlap, use DP (memoize); if independent, use D&C
- **Master theorem limitations** - only applies to recurrences of the form T(n) = aT(n/b) + f(n); not all recurrences fit
- **Merge step is the key** - the combine step is where the real work happens (merge in merge sort, cross sum in max subarray)
- **Stack depth** - D&C with halving gives O(log n) recursion depth; safe for large inputs
- **Constant factors** - D&C solutions often have higher constant factors than iterative alternatives
- **Kadane's beats D&C** - for maximum subarray, Kadane's is O(n) vs D&C O(n log n); D&C is educational

## See Also

- [[sorting-algorithms]] - merge sort and quick sort are D&C
- [[binary-search]] - simplest D&C: divide by half
- [[dynamic-programming]] - use when D&C subproblems overlap
