---
title: Mathematical Logic
category: foundations
tags: [data-science, math, logic, propositional, sets, proofs]
---

# Mathematical Logic

Formal reasoning systems underlying computer science and mathematical proofs. Propositional logic, first-order logic, proof techniques, and algorithm theory.

## Propositional Logic

### Connectives

| Connective | Symbol | True When |
|-----------|--------|-----------|
| Negation | ~P | P is false |
| Conjunction | P & Q | Both true |
| Disjunction | P v Q | At least one true |
| Exclusive OR | P XOR Q | Exactly one true |
| Implication | P -> Q | P false, or both true |
| Equivalence | P <-> Q | Same truth value |

### Key Properties
- **Tautology**: always true regardless of variable values. Example: P v ~P
- **Contradiction**: always false. Example: P & ~P
- **Logical equivalence**: same truth table
- **De Morgan's laws**: ~(P & Q) = ~P v ~Q, ~(P v Q) = ~P & ~Q
- **Contrapositive**: P -> Q equivalent to ~Q -> ~P
- For n variables: 2^n rows in truth table

### Implication Gotcha
P -> Q is true when P is false (vacuous truth). "If pigs fly, then I'm the king" is logically true.

## First-Order Logic

Extends propositional logic with:
- **Variables** over a domain
- **Quantifiers**: "for all" (universal) and "there exists" (existential)
- **Predicates**: P(x), R(x, y)
- **Functions**: f(x)

**Negation of quantifiers:**
- ~(forall x, P(x)) = exists x, ~P(x)
- ~(exists x, P(x)) = forall x, ~P(x)

## Proof Techniques

| Method | Approach |
|--------|----------|
| Direct | Assume premises, derive conclusion |
| Contradiction | Assume negation of conclusion, derive contradiction |
| Contrapositive | Prove ~Q -> ~P instead of P -> Q |
| Induction | Base case + inductive step (P(n) -> P(n+1)) |
| Counterexample | Disprove universal statement with one example |

### Mathematical Induction
1. **Base case**: prove P(1) (or P(0))
2. **Inductive step**: assume P(k) true, prove P(k+1)
3. **Conclusion**: P(n) true for all n >= base

## Algorithm Theory

### Computability
- **Turing machine**: abstract model of computation
- **Church-Turing thesis**: anything computable can be computed by a Turing machine
- **Halting problem**: no algorithm can determine if any program halts (undecidable)
- **Decidable**: there exists an algorithm that always halts with correct answer

### Complexity
- **P**: solvable in polynomial time
- **NP**: verifiable in polynomial time
- **NP-complete**: hardest problems in NP (if one is in P, all NP is in P)
- **P vs NP**: open millennium problem

## Axiomatic Systems

- **Axioms**: statements accepted without proof
- **Theorems**: statements proved from axioms
- **Consistency**: no contradictions derivable
- **Completeness**: every true statement is provable (Godel: impossible for sufficiently powerful systems)

## Relevance to DS
- Boolean logic underpins pandas filtering: `df[(cond1) & (cond2)]`
- SQL WHERE clauses are propositional logic
- Decision trees are conjunctions of predicates
- Computational complexity determines algorithm scalability

## See Also
- [[math-precalculus]] - sets and combinatorics
- [[python-for-ds]] - boolean operations in Python
- [[sql-for-data-science]] - SQL WHERE as logic
