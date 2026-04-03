---
title: NumPy Fundamentals
category: tools
tags: [data-science, numpy, python, arrays]
---

# NumPy Fundamentals

NumPy is the numerical computing foundation underlying pandas, scikit-learn, and PyTorch. Its ndarray enables vectorized operations that are 10-100x faster than Python loops.

## Array Basics

```python
import numpy as np

# Creation
a = np.array([1, 2, 3])              # from list
b = np.zeros((3, 4))                  # 3x4 of zeros
c = np.ones((2, 3))                   # 2x3 of ones
d = np.eye(3)                          # 3x3 identity
e = np.arange(0, 10, 0.5)            # evenly spaced (start, stop, step)
f = np.linspace(0, 1, 100)           # 100 points between 0 and 1
g = np.random.uniform(size=10)        # uniform [0, 1)
h = np.random.normal(0, 1, (3, 4))   # normal, shape 3x4
```

## Element-wise Operations

Unlike Python lists, NumPy operates element-wise:
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a + b    # [5, 7, 9]  (not concatenation!)
a * b    # [4, 10, 18]
a ** 2   # [1, 4, 9]
a > 2    # [False, False, True]
```

## Matrix Operations

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B                   # matrix multiplication
np.dot(A, B)            # equivalent
A.T                     # transpose
np.linalg.inv(A)        # inverse
np.linalg.det(A)        # determinant
np.linalg.eig(A)        # eigenvalues, eigenvectors
np.linalg.svd(A)        # SVD
np.linalg.solve(A, b)   # solve Ax=b (preferred over inv)
np.linalg.norm(a)       # L2 norm
```

## Aggregations

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

a.sum()           # 21 (all elements)
a.sum(axis=0)     # [5, 7, 9] (column sums)
a.sum(axis=1)     # [6, 15] (row sums)
a.mean(axis=0)    # column means
a.std()           # standard deviation
a.min(), a.max()
np.cumsum(a, axis=0)  # cumulative sum along columns
```

## Indexing and Slicing

```python
a = np.array([10, 20, 30, 40, 50])
a[0]        # 10
a[-1]       # 50
a[1:3]      # [20, 30]
a[::2]      # [10, 30, 50] (every other)

# Boolean indexing
a[a > 25]   # [30, 40, 50]

# 2D
A = np.array([[1,2,3],[4,5,6]])
A[0, :]     # first row
A[:, 1]     # second column
A[A > 3]    # [4, 5, 6]
```

## Broadcasting

NumPy automatically expands dimensions for operations on different-shaped arrays:
```python
A = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2, 3)
b = np.array([10, 20, 30])             # shape (3,)
A + b   # [[11, 22, 33], [14, 25, 36]]  - b broadcast to each row
```

Rules: dimensions compared from right to left. Compatible if equal or one of them is 1.

## Random Number Generation

```python
np.random.seed(42)                    # reproducibility
np.random.uniform(0, 1, size=10)      # uniform
np.random.normal(0, 1, size=10)       # normal
np.random.randint(0, 100, size=10)    # integers
np.random.choice([1,2,3], size=5)     # sample with replacement
np.random.shuffle(arr)                 # in-place shuffle
```

## Reshaping

```python
a = np.arange(12)
a.reshape(3, 4)       # 3x4 matrix
a.reshape(-1, 4)      # infer rows: (3, 4)
a.flatten()            # back to 1D
a.ravel()              # 1D view (no copy if possible)
np.expand_dims(a, 0)  # add dimension: (1, 12)
np.squeeze(a)          # remove dimensions of size 1
```

## Performance

- Vectorized operations are 10-100x faster than Python loops
- Avoid `for` loops over array elements
- Use boolean indexing instead of `if` inside loops
- Pandas uses NumPy under the hood - rarely need NumPy directly in typical EDA work

## Gotchas
- `a * b` is element-wise, NOT matrix multiplication. Use `a @ b` or `np.dot(a, b)`
- NumPy arrays are mutable - `b = a` creates a reference, not a copy. Use `b = a.copy()`
- Integer division: `np.array([1, 2, 3]) / 2` returns floats. Use `//` for integer division
- Broadcasting can silently produce wrong results if shapes are unintentionally compatible

## See Also
- [[pandas-eda]] - pandas built on numpy
- [[math-linear-algebra]] - theory behind matrix operations
- [[neural-networks]] - tensor operations in deep learning
