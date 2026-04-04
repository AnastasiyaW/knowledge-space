---
title: Greedy Algorithms
category: patterns
tags: [optimization, greedy-choice, scheduling, interval]
---

# Greedy Algorithms

Build solutions incrementally by making the locally optimal choice at each step. No backtracking - once a choice is made, it is never reconsidered.

## Key Facts

- Makes locally optimal choice at each decision point
- Does NOT always produce globally optimal solutions
- Requires proof of correctness (greedy choice property + optimal substructure)
- Typically O(N log N) due to sorting step
- Much faster than DP or backtracking when applicable
- Exchange argument: prove that swapping a non-greedy choice with a greedy one never worsens solution

## When Greedy Works

Must satisfy both:
1. **Greedy choice property**: a globally optimal solution can be arrived at by making locally optimal choices
2. **Optimal substructure**: an optimal solution contains optimal solutions to subproblems

## Classic Problems

### Activity Selection (Interval Scheduling)

```python
def max_activities(intervals):
    # Sort by end time
    intervals.sort(key=lambda x: x[1])
    count = 1
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= last_end:
            count += 1
            last_end = end
    return count
```

### Fractional Knapsack

```python
def fractional_knapsack(capacity, items):
    # items: [(value, weight), ...]
    # Sort by value/weight ratio descending
    items.sort(key=lambda x: x[0] / x[1], reverse=True)
    total_value = 0

    for value, weight in items:
        if capacity >= weight:
            total_value += value
            capacity -= weight
        else:
            total_value += value * (capacity / weight)
            break
    return total_value
```

### Huffman Coding

```python
import heapq

def huffman(frequencies):
    heap = [[freq, [char, ""]] for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heap[0][1:], key=lambda p: (len(p[1]), p))
```

### Coin Change (Greedy - only works for certain denominations)

```python
def coin_change_greedy(coins, amount):
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1
```

### Job Scheduling with Deadlines

```python
def job_scheduling(jobs):
    # jobs: [(profit, deadline), ...]
    jobs.sort(key=lambda x: x[0], reverse=True)
    max_deadline = max(j[1] for j in jobs)
    slots = [False] * (max_deadline + 1)
    total_profit = 0

    for profit, deadline in jobs:
        for t in range(deadline, 0, -1):
            if not slots[t]:
                slots[t] = True
                total_profit += profit
                break
    return total_profit
```

## Greedy vs DP Comparison

| Aspect | Greedy | DP |
|--------|--------|-----|
| Choices | One best local choice | All choices evaluated |
| Subproblems | Solved once | Solved and memoized |
| Direction | Top-down only | Top-down or bottom-up |
| Speed | Usually O(N log N) | Usually O(N*W) or O(N^2) |
| Correctness | Needs proof | Always correct for well-formed recurrence |

## Gotchas

- **Issue:** Greedy coin change fails for arbitrary denominations (e.g., coins=[1,3,4], amount=6: greedy gives 4+1+1=3 coins, optimal is 3+3=2 coins) -> **Fix:** Use DP for general coin change.
- **Issue:** Applying greedy without proving correctness -> **Fix:** Always verify greedy choice property. If in doubt, use DP or backtracking.
- **Issue:** 0/1 Knapsack is NOT solvable by greedy (only fractional knapsack is) -> **Fix:** Use DP for 0/1 Knapsack.

## See Also

- [[dynamic-programming-fundamentals]] - when greedy fails, DP is the fallback
- [[minimum-spanning-trees]] - Kruskal and Prim are greedy algorithms
- [[shortest-path-algorithms]] - Dijkstra is a greedy algorithm
