---
title: Amortized Analysis
category: concepts
tags: [algorithms, complexity, amortized, dynamic-array]
---

# Amortized Analysis

Amortized analysis computes the average cost per operation over a sequence of operations, providing a guaranteed bound regardless of input. Unlike average-case analysis (which depends on input distribution), amortized cost applies to all possible operation sequences.

## Key Facts

- Amortized cost = total cost of n operations / n
- NOT dependent on input probability - guaranteed bound over all sequences
- Individual operations may be expensive, but the average is cheap
- Most common example: dynamic array (Python list) append

## Patterns

### Dynamic Array (Python list) Insertion

When the array is full, double capacity and copy all elements. Resize happens at sizes 1, 2, 4, 8, 16, 32, ...

```text
Cost of n insertions without resize: n
Cost of resize operations: 1 + 2 + 4 + 8 + ... + n = 2n - 1

Total cost of n insertions = n + (2n - 1) ~ 3n
Amortized cost per insertion = 3n / n = O(1)
```

Even though a single resize costs O(n), it happens so rarely that the amortized cost per `append()` is O(1).

### Key Distinction

| Concept | Depends on | Guarantee |
|---------|-----------|-----------|
| Worst case | Single worst input | Per-operation |
| Average case | Input probability distribution | Expected over random inputs |
| Amortized | Sequence of operations | Average per operation, any sequence |

## Gotchas

- Amortized O(1) does NOT mean every operation is O(1) - individual operations can be O(n)
- Not useful for real-time systems where every single operation must be fast
- The guarantee is over the entire sequence, not per-operation
- Python `list.append()` is amortized O(1) but a single append can trigger O(n) copy

## See Also

- [[complexity-analysis]] - fundamental complexity concepts
- [[data-structures]] - Python list internals
