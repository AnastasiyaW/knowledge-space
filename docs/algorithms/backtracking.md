---
title: Backtracking
category: patterns
tags: [recursion, search, constraint-satisfaction, pruning]
---

# Backtracking

Systematic exploration of solution space by building candidates incrementally and abandoning ("backtracking") branches that violate constraints. Combines DFS with pruning.

## Key Facts

- Explores state space tree depth-first
- Prunes branches that cannot lead to valid solutions (constraint check)
- Time complexity often exponential, but pruning reduces practical runtime significantly
- Foundation for solving NP-complete problems (subset sum, graph coloring, N-queens, Sudoku)
- Always returns to the last decision point and tries the next option
- Can find one solution, all solutions, or the optimal solution depending on implementation

## Core Template

```python
def backtrack(state, choices):
    if is_solution(state):
        process_solution(state)
        return

    for choice in choices:
        if is_valid(state, choice):
            make_choice(state, choice)
            backtrack(state, remaining_choices(choices, choice))
            undo_choice(state, choice)  # backtrack
```

## Patterns

### N-Queens

```python
def solve_n_queens(n):
    results = []

    def backtrack(row, cols, diag1, diag2, board):
        if row == n:
            results.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            board[row][col] = "Q"
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            backtrack(row + 1, cols, diag1, diag2, board)
            board[row][col] = "."
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    board = [["." for _ in range(n)] for _ in range(n)]
    backtrack(0, set(), set(), set(), board)
    return results
```

### Sudoku Solver (Graph Coloring Approach)

```python
def solve_sudoku(grid):
    def get_candidates(r, c):
        used = set()
        used.update(grid[r])  # row
        used.update(grid[i][c] for i in range(9))  # col
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                used.add(grid[i][j])
        return [n for n in range(1, 10) if n not in used]

    def solve():
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for num in get_candidates(r, c):
                        grid[r][c] = num
                        if solve():
                            return True
                        grid[r][c] = 0
                    return False
        return True

    solve()
    return grid
```

### Subset Sum

```python
def subset_sum(nums, target):
    result = []

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:
                break  # prune (requires sorted input)
            current.append(nums[i])
            backtrack(i + 1, current, remaining - nums[i])
            current.pop()

    nums.sort()
    backtrack(0, [], target)
    return result
```

### Permutations

```python
def permutations(nums):
    result = []

    def backtrack(first):
        if first == len(nums):
            result.append(nums[:])
            return
        for i in range(first, len(nums)):
            nums[first], nums[i] = nums[i], nums[first]
            backtrack(first + 1)
            nums[first], nums[i] = nums[i], nums[first]

    backtrack(0)
    return result
```

## Complexity

| Problem | Time | Space |
|---------|------|-------|
| N-Queens | O(N!) | O(N) |
| Sudoku | O(9^(empty cells)) | O(1) |
| Subset Sum | O(2^N) | O(N) |
| Permutations | O(N!) | O(N) |
| Graph Coloring | O(k^N) | O(N) |

## Optimization Techniques

- **Constraint propagation**: reduce domain before recursing (e.g., arc consistency in Sudoku)
- **Variable ordering**: choose the most constrained variable first (MRV heuristic)
- **Value ordering**: try the least constraining value first
- **Symmetry breaking**: avoid exploring equivalent configurations
- **Early termination**: stop when first valid solution found (if only one needed)

## Gotchas

- **Issue:** Forgetting to undo state changes after recursive call -> **Fix:** Always pair `make_choice` with `undo_choice`. Use immutable data structures or explicit undo.
- **Issue:** Exponential blowup from insufficient pruning -> **Fix:** Add constraint checks as early as possible. Sort input arrays for numeric pruning.
- **Issue:** Duplicate solutions when input contains duplicates -> **Fix:** Sort input and skip `nums[i] == nums[i-1]` at same recursion level.

## See Also

- [[dynamic-programming-fundamentals]] - when subproblems overlap, DP beats backtracking
- [[graph-coloring]] - classic backtracking application
- [[graph-traversal-bfs-dfs]] - backtracking is DFS with pruning
