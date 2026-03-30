---
title: Binary Search
category: algorithms
tags: [binary-search, divide-and-conquer, sorted-array, search, logarithmic]
---

# Binary Search

## Key Facts

- Searches a **sorted** array by repeatedly halving the search space
- Time: O(log n), Space: O(1) iterative / O(log n) recursive
- Prerequisite: input must be sorted (or have a monotonic property)
- Can find: exact match, first/last occurrence, insertion point, boundary condition
- Variants: find first position, find last position, search in rotated array, find peak element
- Python: `bisect.bisect_left()`, `bisect.bisect_right()` from `bisect` module
- Java: `Arrays.binarySearch()`, `Collections.binarySearch()`
- Related: [[sorting-algorithms]], [[binary-tree-traversal]]

## Patterns

### Classic Binary Search

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoid overflow
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1  # not found
```

### First and Last Position of Target

```python
def find_first(arr, target):
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid
            hi = mid - 1  # keep searching left
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result

def find_last(arr, target):
    lo, hi = 0, len(arr) - 1
    result = -1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            result = mid
            lo = mid + 1  # keep searching right
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return result
```

### Binary Search on Answer (Parametric Search)

```python
# Find minimum value that satisfies condition
def binary_search_on_answer(lo, hi, condition):
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if condition(mid):
            hi = mid  # mid might be the answer
        else:
            lo = mid + 1
    return lo
```

### Search in Rotated Sorted Array

```python
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

```java
// Java: using Arrays.binarySearch
import java.util.Arrays;

int idx = Arrays.binarySearch(arr, target);
// returns negative value if not found: -(insertion_point) - 1

// Manual implementation
public int binarySearch(int[] arr, int target) {
    int lo = 0, hi = arr.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

## Gotchas

- **Integer overflow** - use `lo + (hi - lo) // 2` instead of `(lo + hi) // 2` (matters in Java/C++)
- **Off-by-one in loop condition** - `lo <= hi` for exact match; `lo < hi` for boundary/minimization
- **Inclusive vs exclusive bounds** - be consistent: `[lo, hi]` uses `lo <= hi`; `[lo, hi)` uses `lo < hi`
- **Not just for sorted arrays** - binary search works on any monotonic predicate (e.g., "can we achieve X in time T?")
- **Early exit conditions** - add checks for edge cases (target < arr[0] or target > arr[-1]) before the loop
- **Rotated array** - must determine which half is sorted before comparing with target

## See Also

- [[sorting-algorithms]] - binary search requires sorted input
- [[binary-tree-traversal]] - tree structure based on binary search principle
- [[big-o-complexity-analysis]] - O(log n) from repeated halving
