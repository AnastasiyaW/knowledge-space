---
title: Algorithms & Data Structures - Map of Content
category: index
tags: [moc, algorithms, data-structures, index]
---

# Algorithms & Data Structures

## Fundamentals

- [[big-o-complexity-analysis]] - asymptotic notation, time/space analysis, common complexity classes
- [[divide-and-conquer]] - split-solve-combine pattern, master theorem, fast exponentiation

## Data Structures

- [[arrays-and-strings]] - two pointers, sliding window, prefix sum, frequency counting
- [[linked-lists]] - singly/doubly linked, fast-slow pointers, reversal, merge sort on lists
- [[stacks-and-queues]] - LIFO/FIFO, monotonic stack, min stack, queue from two stacks
- [[hash-tables]] - hash maps/sets, collision resolution, two-sum pattern, frequency counter
- [[binary-tree-traversal]] - BST, inorder/preorder/postorder, level-order, validation
- [[priority-queue-and-heap]] - binary heap, min/max heap, heapify, top-K problems
- [[trie]] - prefix tree, autocomplete, word search in grids
- [[union-find]] - disjoint set union, path compression, union by rank, Kruskal's MST

## Algorithm Techniques

- [[binary-search]] - sorted array search, first/last position, search on answer, rotated array
- [[sorting-algorithms]] - merge/quick/heap/counting sort, stability, complexity comparison
- [[recursion-and-backtracking]] - subsets, permutations, combinations, N-Queens, general template
- [[dynamic-programming]] - memoization vs tabulation, grid DP, knapsack, LCS, LIS
- [[greedy-algorithms]] - interval scheduling, jump game, fractional knapsack, correctness proofs

## Graph Algorithms

- [[graph-representations]] - adjacency list vs matrix, weighted/directed, edge list
- [[graph-bfs-dfs]] - breadth-first, depth-first, connected components, cycle detection, flood fill
- [[graph-shortest-path]] - Dijkstra, Bellman-Ford, Floyd-Warshall
- [[topological-sort]] - Kahn's algorithm (BFS), DFS-based, cycle detection in DAGs
- [[minimum-spanning-tree]] - Kruskal's (union-find), Prim's (priority queue)
- [[bit-manipulation]] - bitwise operations, XOR tricks, bitmask DP, popcount

## Quick Complexity Reference

| Operation | Array | Linked List | Hash Table | BST (balanced) | Heap |
|-----------|-------|-------------|------------|----------------|------|
| Access | O(1) | O(n) | - | O(log n) | - |
| Search | O(n) | O(n) | O(1) avg | O(log n) | O(n) |
| Insert | O(n) | O(1)* | O(1) avg | O(log n) | O(log n) |
| Delete | O(n) | O(1)* | O(1) avg | O(log n) | O(log n) |
| Min/Max | O(n) | O(n) | O(n) | O(log n) | O(1) peek |

*with reference to node

## Algorithm Selection Guide

| Problem Type | Technique | Example |
|-------------|-----------|---------|
| Search sorted data | Binary search | First/last position |
| Shortest path (unweighted) | BFS | Grid shortest path |
| Shortest path (weighted) | Dijkstra | Network routing |
| Optimal substructure + overlap | Dynamic programming | Knapsack, LCS |
| Locally optimal = globally optimal | Greedy | Interval scheduling |
| Explore all possibilities | Backtracking | N-Queens, Sudoku |
| Dynamic connectivity | Union-Find | Connected components |
| Prefix queries on strings | Trie | Autocomplete |
| Ordering with dependencies | Topological sort | Build systems |
| Next greater/smaller element | Monotonic stack | Stock span |
