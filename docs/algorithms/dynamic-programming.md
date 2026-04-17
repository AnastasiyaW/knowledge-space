---
title: Dynamic Programming and Recursion
category: concepts
tags: [misc, algorithms, dynamic-programming, recursion, memoization]
---

# Dynamic Programming and Recursion

Recursion fundamentals, memoization (top-down), bottom-up tabulation, and recognizing DP opportunities. Core technique for optimization problems with overlapping subproblems.

## Key Facts

- Recursion needs three ingredients: base case, recursive call (moves toward base case), return value propagation
- Fibonacci without memoization: O(2^N); with memoization: O(N)
- Bottom-up (iterative) is usually more memory-efficient than top-down (memoized recursion)
- DP applies when there are overlapping subproblems - the recursive call tree has duplicate branches
- Memoization trades O(N) space for dramatic time savings
- Stack overflow occurs when recursion depth exceeds call stack memory

## Patterns

### Recursion Fundamentals

```python
def factorial(n):
    return 1 if n == 1 else n * factorial(n - 1)
```

**When to use recursion**: problems with unknown or variable depth (file system traversal, tree operations, fractal structures).

```ruby
# Directory traversal - unknown depth handled naturally
def find_directories(directory)
  Dir.foreach(directory) do |filename|
    if File.directory?("#{directory}/#{filename}") && filename != "." && filename != ".."
      puts "#{directory}/#{filename}"
      find_directories("#{directory}/#{filename}")
    end
  end
end
```

**Writing recursive functions**: identify single-step action, pass additional parameters to track state, last line is the recursive call.

```python
def double_array(array, index=0):
    if index >= len(array): return
    array[index] *= 2
    double_array(array, index + 1)
```

### Memoization (Top-Down)

Cache results of expensive recursive calls:

```python
def fib(n, memo={}):
    if n <= 1: return n
    if n not in memo:
        memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
```

### Bottom-Up Tabulation

Iterate from small subproblems to large, store results in table:

```python
def fib_bottom_up(n):
    if n <= 1: return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i-1] + table[i-2]
    return table[n]
```

### DP Problem-Solving Framework

1. **Identify overlapping subproblems** - same computation repeated with different parameters
2. **Define state**: dp[i] = "best solution for problem of size i"
3. **Recurrence**: dp[i] = f(dp[i-1], dp[i-2], ...)
4. **Base cases**: smallest subproblems with known answers
5. **Build direction**: bottom-up (iterative) or top-down (memoized)

### Preprocessing Optimization

Example - find largest sub-square in matrix where all border cells are filled:

Naive: O(N^5). Better with preprocessing: O(N^3).

```python
# Preprocess consecutive filled cells in each direction
zeros_right = [[0]*n for _ in range(n)]
zeros_below = [[0]*n for _ in range(n)]
for i in range(n-1, -1, -1):
    for j in range(n-1, -1, -1):
        if matrix[i][j] == 1:
            zeros_right[i][j] = 1 + (zeros_right[i][j+1] if j+1 < n else 0)
            zeros_below[i][j] = 1 + (zeros_below[i+1][j] if i+1 < n else 0)
```

Now checking a border candidate is O(1) per side instead of O(N).

## Gotchas

- Python default mutable argument (`memo={}`) persists across calls - useful for memoization but a common bug in other contexts
- Recursion depth limit in Python: default ~1000 (`sys.setrecursionlimit()` to change, but prefer iterative for deep recursion)
- Bottom-up often allows space optimization (e.g., Fibonacci only needs prev two values, not full table)
- Not all recursive problems benefit from DP - only those with overlapping subproblems (not divide-and-conquer like mergesort)

## See Also

- [[data-structures-fundamentals]] - recursion on arrays, Big O analysis
- [[trees-and-graphs]] - recursive tree traversal, DFS
- [[algorithms/problem-patterns]] - sliding window, two-pointer, interview techniques
