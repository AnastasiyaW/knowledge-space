---
title: Arrays and Strings
category: data-structures
tags: [array, string, two-pointers, sliding-window, prefix-sum, anagram]
---

# Arrays and Strings

## Key Facts

- **Array** - contiguous block of memory with O(1) random access by index
- **Dynamic array** (Python `list`, Java `ArrayList`) - auto-resizes, amortized O(1) append, O(n) insert/delete at arbitrary position
- **String** - immutable in Python/Java; concatenation in a loop is O(n^2) - use `join()` or `StringBuilder`
- Access: O(1), Search: O(n), Insert/Delete at end: O(1) amortized, Insert/Delete at index: O(n)
- Related: [[hash-tables]], [[sorting-algorithms]]

## Patterns

### Two Pointers

```python
# Two pointers: check if sorted array has a pair summing to target
def two_sum_sorted(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        s = arr[lo] + arr[hi]
        if s == target: return [lo, hi]
        elif s < target: lo += 1
        else: hi -= 1
    return []

# Reverse a string in-place
def reverse_string(s: list):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        s[lo], s[hi] = s[hi], s[lo]
        lo += 1
        hi -= 1
```

### Sliding Window

```python
# Maximum sum subarray of size k - O(n)
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

# Longest substring without repeating characters
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

### Prefix Sum

```python
# Range sum query in O(1) after O(n) preprocessing
def build_prefix_sum(arr):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

### Frequency Counting / Anagram Check

```python
from collections import Counter

# Valid anagram - O(n) time, O(n) space
def is_anagram(s1, s2):
    return Counter(s1) == Counter(s2)

# Manual approach with array (lowercase letters only)
def is_anagram_array(s1, s2):
    if len(s1) != len(s2):
        return False
    freq = [0] * 26
    for c in s1:
        freq[ord(c) - ord('a')] += 1
    for c in s2:
        freq[ord(c) - ord('a')] -= 1
    return all(f == 0 for f in freq)
```

```java
// Two pointers: remove duplicates from sorted array in-place
public int removeDuplicates(int[] nums) {
    if (nums.length == 0) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.length; fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}
```

## Gotchas

- **String concatenation in loops** - `s += c` in Python/Java creates a new string each time: O(n^2). Use `"".join(parts)` or `StringBuilder`
- **Off-by-one errors in sliding window** - be precise about whether window is `[left, right]` inclusive or `[left, right)` exclusive
- **Sorted vs unsorted** - two pointers on sorted arrays is O(n); on unsorted, use a hash set for O(n) or sort first for O(n log n)
- **Python slicing creates copies** - `arr[i:j]` is O(j-i), not O(1)
- **Negative indices in Python** - `arr[-1]` is valid but can mask bugs in pointer arithmetic

## See Also

- [[hash-tables]] - O(1) lookup for frequency/existence problems
- [[sorting-algorithms]] - often a prerequisite for two-pointer approaches
- [[linked-lists]] - compare access patterns with arrays
