---
title: Searching Algorithms
category: algorithms
tags: [algorithms, search, binary-search, linear-search, kmp, string-matching]
---

# Searching Algorithms

Covers linear search, binary search, and KMP string matching. Linear search is O(n) for unsorted data, binary search is O(log n) for sorted data, and KMP achieves O(n+m) string pattern matching by avoiding redundant comparisons.

## Key Facts

- **Linear search**: O(n) time, O(1) space - works on any data, any predicate
- **Binary search**: O(log n) time, O(1) space - requires sorted array
- **KMP**: O(n+m) time, O(m) space - pattern matching without backtracking in text
- For a single query on unsorted data, linear search beats sort-then-binary-search (O(n) vs O(n log n))
- For many queries on same data, sort once O(n log n) then binary search each O(log n)

## Patterns

### Linear Search

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

Works with any predicate - not just equality:

```python
# First element greater than num
def search_greater(arr, num):
    for i in range(len(arr)):
        if arr[i] > num:
            return i
    return -1

# String containing character
def search_contains(arr, ch):
    for i in range(len(arr)):
        if ch in arr[i]:
            return i
    return -1
```

### Binary Search

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Why O(log n): starting with n elements, after k iterations at most ceil(n/2^k) remain. Stop when 1 element: n/2^k = 1 -> k = log2(n).

### When to Choose

```python
def search(arr, target):
    if is_sorted(arr):
        return binary_search(arr, target)
    else:
        return linear_search(arr, target)
```

### KMP String Search - O(n+m)

Naive string search is O(n*m) because it restarts pattern matching from scratch on mismatch. KMP uses an LPS (Longest Proper Prefix which is also Suffix) array to skip known-matched characters.

**LPS Array Construction - O(m):**

```python
def get_lps_arr(pattern):
    lps = [0] * len(pattern)
    length = 0  # length of previous longest prefix-suffix
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]  # fall back without moving i
        else:
            lps[i] = 0
            i += 1
    return lps
```

Example: `"aabaaab"` -> `[0, 1, 0, 1, 2, 2, 3]`

**KMP Search - O(n):**

```python
def kmp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    if m == n:
        return 0 if text == pattern else -1
    lps = get_lps_arr(pattern)
    i, j = 0, 0  # text pointer, pattern pointer
    while i < n and j < m:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j > 0:
            j = lps[j - 1]  # don't advance i
        else:
            i += 1
    return i - j if j == m else -1
```

**Why it works:** `i` never moves backward. On mismatch at position j, `lps[j-1]` tells how many characters are already matched (prefix = suffix of what we've seen). Total: O(n) for search + O(m) for LPS = O(n+m).

## Gotchas

- Binary search requires sorted input - applying it to unsorted data gives wrong results
- Binary search `mid = (left + right) // 2` can overflow in languages with fixed-size integers; use `mid = left + (right - left) // 2` instead (not an issue in Python)
- KMP's LPS construction: when mismatch occurs, fall back to `lps[length-1]`, NOT reset to 0
- For single search on unsorted data, sorting first (O(n log n)) is wasteful vs linear search (O(n))
- Naive string search worst case: text="aaa...a", pattern="aaa...ab" -> O(n*m)

## See Also

- [[sorting-algorithms]] - binary search requires sorted input
- [[two-pointer-technique]] - search patterns on sorted arrays
- [[complexity-analysis]] - understanding O(log n) derivation
