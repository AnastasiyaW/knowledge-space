---
title: Pre-Calculus Foundations
category: foundations
tags: [data-science, math, algebra, functions, sets]
---

# Pre-Calculus Foundations

Number systems, equations, functions, and basic set theory - the prerequisites before diving into calculus, probability, and linear algebra.

## Number Systems

N (naturals) subset Z (integers) subset Q (rationals) subset R (reals) subset C (complex)

- **Rationals**: fractions p/q. Decimal terminates or repeats
- **Irrationals**: sqrt(2), pi, e. Non-terminating, non-repeating
- **Fundamental theorem**: every integer > 1 has unique prime factorization

## Equations

### Quadratic: ax^2 + bx + c = 0
- Discriminant D = b^2 - 4ac
- D > 0: two real roots, D = 0: one root, D < 0: no real roots
- x = (-b +/- sqrt(D)) / (2a)
- Vieta's: x1 + x2 = -b/a, x1 * x2 = c/a

### Systems
- **Substitution**: solve one for one variable, substitute
- **Elimination**: add/subtract equations
- Types: unique (intersecting), none (parallel), infinite (coincident)

## Inequalities

- When multiplying/dividing by negative: **flip sign**
- **Method of Intervals** for rational: find zeros, check sign per interval
- Quadratic: find roots, use parabola direction

## Elementary Functions

| Function | Domain | Key Property |
|----------|--------|-------------|
| Linear: y = kx + b | R | Constant rate of change |
| Quadratic: y = ax^2 + bx + c | R | Vertex at x = -b/(2a) |
| Exponential: y = a^x | R | Always positive, monotone |
| Logarithmic: y = log_a(x) | x > 0 | Inverse of exponential |
| Trigonometric: sin, cos | R | Period 2*pi, range [-1, 1] |

**Log properties**: log(ab) = log(a) + log(b), log(a^n) = n*log(a), log_a(x) = ln(x)/ln(a)

**Key identities**: sin^2 + cos^2 = 1, e^(i*theta) = cos(theta) + i*sin(theta)

### Graph Transformations
- f(x) + c: shift up
- f(x - c): shift right
- c*f(x): vertical stretch
- f(cx): horizontal compression

## Sets

- **Union** A cup B: in A OR B
- **Intersection** A cap B: in A AND B
- **Difference** A \ B: in A but not B
- **De Morgan**: (A cup B)^c = A^c cap B^c
- **Inclusion-exclusion**: |A cup B| = |A| + |B| - |A cap B|
- **Power set**: |P(A)| = 2^|A|

## Combinatorics

- **Permutations** (order matters): P(n,k) = n!/(n-k)!
- **Combinations** (order doesn't): C(n,k) = n!/(k!(n-k)!)
- **Binomial theorem**: (a+b)^n = sum C(n,k) * a^(n-k) * b^k
- **Pigeonhole principle**: n items into m containers, n > m -> at least one has > 1

## Sequences

- **Arithmetic**: a_n = a_1 + (n-1)d, S_n = n(a_1+a_n)/2
- **Geometric**: a_n = a_1 * r^(n-1), infinite sum (|r|<1): S = a_1/(1-r)
- **Compound interest**: A = P(1+r)^n

## See Also
- [[math-for-ml]] - calculus builds on these foundations
- [[math-linear-algebra]] - vectors and matrices
- [[probability-distributions]] - probability uses combinatorics
