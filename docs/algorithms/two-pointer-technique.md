---
title: Two-Pointer Technique
category: patterns
tags: [algorithms, two-pointers, sorted-array, optimization, space-time-tradeoff]
---

# Two-Pointer Technique

The two-pointer technique uses two indices to traverse data structures (typically arrays), reducing time complexity by exploiting sorted order or other structural properties. Common in problems involving pairs, subarrays, and subsequences.

## Key Facts

- Typically reduces O(n^2) brute force to O(n) or O(n log n)
- Requires sorted array for convergent pointer approach
- Two variants: convergent (left/right moving inward) and parallel (both moving forward)
- Often part of the space-time tradeoff: O(n^2) time O(1) space -> O(n) time O(n) space (hash) or O(n log n) time O(1) space (sort + two pointers)

## Patterns

### Two-Sum with Sort + Two Pointers - O(n log n)

```python
def find_pair(arr, k):
    arr = sorted(arr)
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == k:
            return True
        elif s < k:
            left += 1   # need larger sum
        else:
            right -= 1  # need smaller sum
    return False
```

Why it works: when sum is too small, only incrementing left can increase it; when too large, only decrementing right can decrease it. No pair is missed because arr[left+1] >= arr[left] and arr[right-1] <= arr[right].

### Two-Sum with Hash Set - O(n)

```python
def find_pair(arr, k):
    visited = set()
    for elem in arr:
        if (k - elem) in visited:
            return True
        visited.add(elem)
    return False
```

### Subsequence Check - O(n+m)

```python
def is_subsequence(text, pattern):
    ptr_t, ptr_p = 0, 0
    while ptr_t < len(text) and ptr_p < len(pattern):
        if text[ptr_t] == pattern[ptr_p]:
            ptr_p += 1
        ptr_t += 1
    return ptr_p == len(pattern)
```

### Trade-off Summary for Two-Sum

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force (all pairs) | O(n^2) | O(1) | No preprocessing |
| Sort + two pointers | O(n log n) | O(1) extra | Modifies/copies array |
| Hash set | O(n) | O(n) | Fastest, uses extra memory |

## Gotchas

- Sort + two pointers loses original indices (if you need them, store (value, index) pairs)
- Hash set approach handles duplicates differently - check if complement was already seen
- For sorted arrays, two pointers is preferred over hash set (O(1) space)
- The technique doesn't work on unsorted arrays without sorting first (for convergent variant)

## See Also

- [[searching-algorithms]] - binary search as another sorted-array technique
- [[sorting-algorithms]] - sorting as preprocessing step
- [[dp-sequence-problems]] - more advanced sequence techniques
