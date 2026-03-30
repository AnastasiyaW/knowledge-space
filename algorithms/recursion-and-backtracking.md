---
title: Recursion and Backtracking
category: algorithms
tags: [recursion, backtracking, permutations, combinations, subsets, n-queens]
---

# Recursion and Backtracking

## Key Facts

- **Recursion** - function calls itself; requires base case (termination) and recursive case (reduction)
- **Backtracking** - systematic exploration of all candidates; prune invalid paths early
- Every recursive algorithm can be converted to iterative with an explicit stack
- Recursive call stack uses O(depth) space
- Backtracking generates solutions incrementally, abandoning a candidate as soon as it violates constraints
- Common patterns: subsets, permutations, combinations, N-Queens, Sudoku solver, maze paths
- Related: [[dynamic-programming]], [[binary-tree-traversal]]

## Patterns

### Subsets (Power Set)

```python
def subsets(nums):
    result = []
    def backtrack(start, current):
        result.append(current[:])  # copy
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()  # backtrack
    backtrack(0, [])
    return result
# 2^n subsets, O(n * 2^n) total
```

### Permutations

```python
def permutations(nums):
    result = []
    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()
    backtrack([], nums)
    return result
# n! permutations
```

### Combinations (n choose k)

```python
def combinations(n, k):
    result = []
    def backtrack(start, current):
        if len(current) == k:
            result.append(current[:])
            return
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
            current.pop()
    backtrack(1, [])
    return result
```

### N-Queens

```python
def solve_n_queens(n):
    result = []
    board = [['.' ] * n for _ in range(n)]

    def is_safe(row, col):
        for i in range(row):
            if board[i][col] == 'Q':
                return False
            if col - (row - i) >= 0 and board[i][col - (row - i)] == 'Q':
                return False
            if col + (row - i) < n and board[i][col + (row - i)] == 'Q':
                return False
        return True

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'

    backtrack(0)
    return result
```

### General Backtracking Template

```python
def backtrack(candidates, state, result):
    if is_solution(state):
        result.append(state.copy())
        return
    for candidate in candidates:
        if is_valid(candidate, state):
            state.add(candidate)       # choose
            backtrack(candidates, state, result)  # explore
            state.remove(candidate)    # un-choose (backtrack)
```

```java
// Java: generate all subsets
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    result.add(new ArrayList<>(current));
    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

## Gotchas

- **Copy the state** - `result.append(current[:])` not `result.append(current)` - lists are mutable references
- **Stack overflow** - deep recursion exceeds Python's default 1000 frame limit; use `sys.setrecursionlimit` or iterative approach
- **Pruning is essential** - without early termination, backtracking degenerates to brute force
- **Avoid duplicates** - sort input first, skip `nums[i] == nums[i-1]` when generating subsets/combinations without repeats
- **Base case** - forgetting base case causes infinite recursion; always define termination condition first
- **Mutable default arguments** - never use `def f(result=[])` in Python; use `None` and create inside function

## See Also

- [[dynamic-programming]] - when backtracking has overlapping subproblems, add memoization
- [[binary-tree-traversal]] - tree recursion patterns
- [[graph-bfs-dfs]] - DFS is recursive graph traversal
