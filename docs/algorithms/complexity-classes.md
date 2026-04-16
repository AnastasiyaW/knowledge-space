---
title: "Complexity Classes: P, NP, NP-Complete"
category: concepts
tags: [algorithms, complexity-theory, P, NP, NP-complete, NP-hard, reductions]
---

# Complexity Classes: P, NP, NP-Complete

Complexity classes categorize decision problems by the computational resources needed to solve or verify them. The P vs NP question - whether every problem whose solution can be quickly verified can also be quickly solved - is one of the most important open problems in computer science.

## Key Facts

- **P**: Decision problems solvable in polynomial time. Examples: palindrome check, shortest path, sorting
- **NP**: Decision problems where a YES answer can be **verified** in polynomial time. Example: given a partition, verify both halves sum equally in O(n)
- **NP-complete**: Hardest problems in NP - every NP problem reduces to them in polynomial time. Example: Hamiltonian path, 3-SAT
- **NP-hard**: At least as hard as NP-complete, but not necessarily in NP (may not be decision problems). Example: halting problem, TSP optimization
- All P problems are in NP (if solvable in poly-time, also verifiable)
- P != NP is widely assumed but unproven (Millennium Prize Problem, $1M reward)

## Class Hierarchy

```text
NP-hard
  |-- NP-complete  <-- hardest problems IN NP
  |-- (problems not in NP, e.g., halting problem)
NP
  |-- NP-complete
  |-- P  (assuming P != NP)
```

## Patterns

### Reduction

Transform problem A into problem B so that solving B solves A. If B is in P and A reduces to B in polynomial time, then A is in P.

To prove a problem X is NP-complete:
1. Show X is in NP (solution verifiable in poly-time)
2. Show a known NP-complete problem reduces to X in poly-time

### Common NP-Complete Problems

| Problem | Description |
|---------|-------------|
| 3-SAT | Satisfiability of boolean formula in 3-CNF |
| Hamiltonian Path/Cycle | Visit every vertex exactly once |
| Graph Coloring (k >= 3) | Color vertices with k colors, no adjacent same |
| Subset Sum | Does a subset sum to target? |
| Traveling Salesman (decision) | Is there a tour of cost <= k? |
| Partition | Split array into two equal-sum halves |

### Practical Implications

- If your problem is NP-hard, don't look for polynomial exact algorithms
- Use approximation algorithms (e.g., Christofides for TSP: 1.5x optimal)
- Use heuristics (greedy, local search, genetic algorithms)
- Exact solutions feasible only for small inputs (DP with exponential time, e.g., Held-Karp O(2^n * n^2))

## Gotchas

- NP does NOT mean "not polynomial" - it means "non-deterministic polynomial"
- NP-hard problems may not be in NP at all (optimization variants of decision problems)
- 2-colorability is polynomial, but 3-colorability is NP-complete
- Subset sum is NP-complete but has pseudo-polynomial O(n*S) DP solution (polynomial in value of S, not bit-length)
- A problem being NP-complete doesn't mean it's always hard - many instances are easy, only worst case is hard

## See Also

- [[complexity-analysis]] - asymptotic analysis fundamentals
- [[traveling-salesman-problem]] - classic NP-hard optimization
- [[graph-coloring]] - NP-complete for k >= 3
- [[dp-optimization-problems]] - pseudo-polynomial solutions for NP-complete problems
