---
title: Sliding Window Technique
category: patterns
tags: [arrays, strings, subarray, optimization]
---

# Sliding Window Technique

Maintain a window (contiguous subarray/substring) that slides across input, expanding and shrinking to satisfy constraints. Reduces brute-force O(N*K) to O(N).

## Key Facts

- Two variants: fixed-size window and variable-size window
- Uses two pointers (left, right) defining window boundaries
- Right pointer expands window; left pointer shrinks it
- Avoids recomputation by incrementally updating window state
- Applicable when problem asks about contiguous subarrays/substrings
- Time: O(N) - each element enters and leaves window at most once

## Fixed-Size Window

```python
def max_sum_subarray(arr, k):
    """Maximum sum of subarray of size k."""
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

## Variable-Size Window Template

```python
def variable_window(arr):
    left = 0
    window_state = {}  # track what's in window
    result = 0

    for right in range(len(arr)):
        # Expand: add arr[right] to window state
        update_state(window_state, arr[right])

        # Shrink: while window violates constraint
        while not valid(window_state):
            remove_state(window_state, arr[left])
            left += 1

        # Update result
        result = max(result, right - left + 1)
    return result
```

## Patterns

### Longest Substring Without Repeating Characters

```python
def length_of_longest_substring(s):
    seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

### Minimum Window Substring

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = 0
    start, end = 0, float('inf')

    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1

        while missing == 0:
            if right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1

    return s[start:end + 1] if end != float('inf') else ""
```

### Maximum of All Subarrays of Size K (Monotonic Deque)

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # stores indices, front = max
    result = []

    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Maintain decreasing order
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

### Subarray Sum Equals K (Prefix Sum + HashMap)

```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}

    for num in nums:
        prefix_sum += num
        count += seen.get(prefix_sum - k, 0)
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    return count
```

## When to Use

| Signal | Technique |
|--------|-----------|
| "subarray of size k" | Fixed window |
| "longest/shortest subarray with condition" | Variable window |
| "all subarrays that satisfy..." | Variable window + counting |
| Contiguous elements | Sliding window candidate |
| Non-contiguous elements | NOT sliding window |

## Gotchas

- **Issue:** Using sliding window on problems requiring non-contiguous elements -> **Fix:** Sliding window only works for contiguous subarrays/substrings. Use DP or two-pointer for non-contiguous.
- **Issue:** Not handling the shrink condition correctly, causing infinite loop -> **Fix:** Ensure left pointer always advances in the shrink loop. Window state must be monotonically updated.
- **Issue:** Off-by-one in fixed window (first window computation) -> **Fix:** Initialize first window separately, then slide from index k.

## See Also

- [[two-pointer-technique]] - related but pointers can move independently
- [[searching-algorithms]] - binary search can combine with sliding window
- [[complexity-analysis]] - sliding window achieves O(N) amortized
