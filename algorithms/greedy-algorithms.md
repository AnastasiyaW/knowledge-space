---
title: Greedy Algorithms
category: algorithms
tags: [greedy, interval-scheduling, activity-selection, huffman, fractional-knapsack]
---

# Greedy Algorithms

## Key Facts

- **Greedy algorithm** makes the locally optimal choice at each step, hoping to find a global optimum
- Works when problem has **greedy choice property** (local optimal leads to global optimal) and **optimal substructure**
- Greedy does NOT always produce optimal solutions - must prove correctness for each problem
- Typically simpler and faster than DP, but applicable to fewer problems
- Classic greedy problems: interval scheduling, Huffman coding, fractional knapsack, minimum spanning tree
- Greedy vs DP: greedy makes one choice per step; DP considers all choices
- Related: [[dynamic-programming]], [[sorting-algorithms]]

## Patterns

### Activity Selection / Interval Scheduling

```python
def max_non_overlapping(intervals):
    """Maximum number of non-overlapping intervals."""
    intervals.sort(key=lambda x: x[1])  # sort by end time
    count = 0
    last_end = float('-inf')
    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end
    return count
```

### Minimum Number of Platforms / Meeting Rooms

```python
def min_meeting_rooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))   # meeting starts
        events.append((end, -1))    # meeting ends
    events.sort()
    max_rooms = current = 0
    for _, delta in events:
        current += delta
        max_rooms = max(max_rooms, current)
    return max_rooms
```

### Jump Game

```python
def can_jump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True

def min_jumps(nums):
    jumps = current_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
    return jumps
```

### Fractional Knapsack

```python
def fractional_knapsack(weights, values, capacity):
    items = sorted(zip(values, weights),
                   key=lambda x: x[0]/x[1], reverse=True)
    total = 0
    for value, weight in items:
        if capacity >= weight:
            total += value
            capacity -= weight
        else:
            total += value * (capacity / weight)
            break
    return total
# Greedy works for fractional; does NOT work for 0/1 knapsack
```

### Assign Cookies

```python
def assign_cookies(greed, cookies):
    greed.sort()
    cookies.sort()
    child = cookie = 0
    while child < len(greed) and cookie < len(cookies):
        if cookies[cookie] >= greed[child]:
            child += 1
        cookie += 1
    return child
```

```java
// Java: interval scheduling
public int maxNonOverlapping(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);
    int count = 0, lastEnd = Integer.MIN_VALUE;
    for (int[] interval : intervals) {
        if (interval[0] >= lastEnd) {
            count++;
            lastEnd = interval[1];
        }
    }
    return count;
}
```

## Gotchas

- **Greedy is not always correct** - 0/1 knapsack, shortest path with negative weights, coin change (arbitrary denominations) all require DP
- **Proof of correctness** - always verify greedy choice property; exchange argument or induction
- **Sort criteria matter** - interval scheduling sorts by END time (not start time); wrong sort = wrong answer
- **Greedy works for coin change ONLY with standard denominations** (1, 5, 10, 25) - fails for arbitrary coin sets
- **Fractional vs 0/1 knapsack** - greedy works for fractional (can take partial items); fails for 0/1 (must take whole items)
- **Local != global** - the classic DP minimum cost path example shows greedy taking locally cheapest but globally suboptimal path

## See Also

- [[dynamic-programming]] - use when greedy fails due to overlapping subproblems
- [[sorting-algorithms]] - greedy often requires sorted input
- [[graph-shortest-path]] - Dijkstra is a greedy algorithm
