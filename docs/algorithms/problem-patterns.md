---
title: Algorithm Problem-Solving Patterns
category: concepts
tags: [algorithms, interview, two-pointer, sliding-window, binary-search, problem-solving]
---

# Algorithm Problem-Solving Patterns

Systematic approach to algorithm problems - the 7-step interview process, common patterns (two-pointer, sliding window), optimization techniques, and data structure selection guidelines.

## Key Facts

- BUD optimization: identify Bottlenecks, Unnecessary work, Duplicate work
- Hash maps solve any "have I seen this?" or "lookup by key" problem in O(1)
- Heaps solve k-th largest/smallest, merge k sorted lists, scheduling problems
- Two-pointer works on sorted arrays or when searching for pairs
- Sliding window works for contiguous subarray/substring problems
- Bottom-up DP is usually more efficient than top-down memoized recursion

## Patterns

### The 7-Step Process

1. **Listen carefully** - identify unique constraints (sorted? tree vs graph? memory limits?)
2. **Draw an example** - specific, large enough, not a special case
3. **State brute force** - even O(N^3); shows understanding
4. **Optimize** - BUD: Bottlenecks, Unnecessary work, Duplicate work
5. **Walk through** - verify algorithm with example before coding
6. **Code** - modular, real code (not pseudocode)
7. **Test** - edge cases: empty, single element, duplicates, negatives

### Two-Pointer

```python
left, right = 0, len(arr) - 1
while left < right:
    if condition: left += 1
    else: right -= 1
```

Use for: pair finding in sorted arrays, palindrome checking, partition problems.

### Sliding Window

```python
start = 0
for end in range(len(s)):
    # expand window
    while window_invalid:
        # shrink from start
        start += 1
    best = max(best, end - start + 1)
```

Use for: longest/shortest substring with constraint, maximum sum subarray of size k.

### Binary Search Template

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = lo + (hi - lo) // 2  # avoids integer overflow
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
```

Use for: sorted data, search space reduction, finding boundaries.

### Data Structure Selection Guide

| Problem type | Data structure | Lookup |
|-------------|---------------|--------|
| "Have I seen this?" | Hash map | O(1) avg |
| k-th largest/smallest | Heap | O(log N) |
| Range queries, predecessor | BST / sorted structure | O(log N) |
| Connected components | Union-Find | O(alpha(N)) |
| Shortest path (unweighted) | BFS with queue | O(V + E) |
| Shortest path (weighted) | Dijkstra with heap | O((V+E) log V) |

### Optimization Techniques

**Space/time tradeoffs**:
- Hash tables for O(1) lookup instead of O(N) scan
- Preprocessing/sorting to enable binary search
- Memoization to avoid repeated subproblem computation

**Dynamic programming**:
- Identify overlapping subproblems
- Define state: dp[i] = "best solution for problem of size i"
- Recurrence: dp[i] = f(dp[i-1], dp[i-2], ...)

### Clean Code for Algorithms

- **Meaningful names**: `leftPointer` not `l`, `currentMax` not `cm`
- **Function length**: if it doesn't fit on screen, split it
- **Single responsibility**: separate parsing, logic, and output
- **No magic numbers**: `MAX_SIZE = 1000` not just `1000`
- **Comments explain WHY**: not what (that should be readable), but why this approach

## Gotchas

- `lo + (hi - lo) // 2` avoids integer overflow; `(lo + hi) // 2` can overflow in languages with fixed-width integers
- Off-by-one errors in binary search: `lo <= hi` vs `lo < hi` depends on whether endpoints are inclusive
- Sliding window only works for problems where shrinking the window from the left is always valid
- Two-pointer on unsorted data requires sorting first - factor in O(N log N) cost
- Always handle edge cases explicitly: empty input, single element, all duplicates

## See Also

- [[data-structures-fundamentals]] - arrays, hash tables, Big O analysis
- [[trees-and-graphs]] - graph traversal algorithms
- [[sorting-algorithms]] - sort as preprocessing step
- [[dynamic-programming]] - memoization and tabulation
