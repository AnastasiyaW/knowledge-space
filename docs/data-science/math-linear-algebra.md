---
title: Linear Algebra for Data Science
category: foundations
tags: [data-science, math, linear-algebra, matrices, eigenvalues]
---

# Linear Algebra for Data Science

Vectors, matrices, and their operations form the computational backbone of ML. Every dataset is a matrix, every prediction is a matrix multiplication, every dimensionality reduction uses eigendecomposition.

## Vectors

Ordered array of numbers. Represents a point or direction in n-dimensional space.

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.dot(a, b)       # 32 (dot product)
np.linalg.norm(a)  # 3.74 (L2 norm)
np.cross(a, b)     # cross product (3D only)
```

**Operations:**
- **Dot product**: a . b = sum(a_i * b_i) = |a| * |b| * cos(theta). If 0, vectors are orthogonal
- **L2 norm** (Euclidean): ||a|| = sqrt(sum(a_i^2))
- **L1 norm** (Manhattan): sum(|a_i|)

**In ML**: feature vectors, weight vectors, gradient vectors, distance computation.

## Matrices

2D array, shape (m x n). Dataset: rows = samples, columns = features.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B              # matrix multiplication
A.T                # transpose
np.linalg.inv(A)   # inverse
np.linalg.det(A)   # determinant
```

**Key properties:**
- AB != BA (not commutative)
- (AB)^T = B^T * A^T
- (AB)C = A(BC) (associative)

**Special matrices:**
- **Identity** (I): diagonal of 1s. AI = IA = A
- **Diagonal**: non-zero only on main diagonal
- **Symmetric**: A = A^T (covariance matrices are symmetric)
- **Orthogonal**: Q^T Q = I (columns are orthonormal)

## Matrix Inverse

A^(-1) exists iff det(A) != 0 (non-singular). A * A^(-1) = I.

```python
A_inv = np.linalg.inv(A)     # raises error if singular
A_pinv = np.linalg.pinv(A)   # pseudo-inverse (always exists)
np.linalg.solve(A, b)        # solve Ax=b (faster than inv(A) @ b)
```

**Singular matrix** (det = 0): columns are linearly dependent, no unique solution.

## Eigenvalues and Eigenvectors

A * v = lambda * v. Vector v preserved in direction, scaled by lambda.

```python
eigenvalues, eigenvectors = np.linalg.eig(A)
```

**In ML:**
- **PCA**: eigenvectors of covariance matrix = principal components; eigenvalues = variance explained
- **Spectral clustering**: eigenvectors of graph Laplacian
- **PageRank**: dominant eigenvector of adjacency matrix
- **Positive definite** (all eigenvalues > 0): Hessian at local minimum

## Singular Value Decomposition (SVD)

Any matrix A(m x n) = U * Sigma * V^T

```python
U, S, Vt = np.linalg.svd(A)
# U: left singular vectors (m x m)
# S: singular values (sorted descending)
# Vt: right singular vectors (n x n)
```

**Applications:**
- Dimensionality reduction (truncated SVD - keep top k)
- Low-rank matrix approximation
- Recommendation systems (matrix factorization)
- Image compression
- Pseudoinverse computation

## Systems of Linear Equations

Ax = b.
- Unique solution: det(A) != 0 -> x = A^(-1)b
- No solution: inconsistent (overdetermined)
- Infinite solutions: underdetermined

```python
x = np.linalg.solve(A, b)  # numerically stable
# NOT: np.linalg.inv(A) @ b (less stable, slower)
```

## Key Concepts for ML

- **Linear independence**: vectors can't be expressed as combinations of others
- **Rank**: max number of linearly independent rows/columns
- **Rank-nullity theorem**: rank + nullity = number of columns
- **Positive definite**: x^T A x > 0 for all x != 0. Hessian positive definite = local minimum
- **Quadratic form**: Q(x) = x^T A x. Classification by eigenvalue signs

## Gotchas
- Matrix multiplication order matters: (100x3) @ (3x50) works, but (3x50) @ (100x3) doesn't
- `np.linalg.inv` should be avoided when possible - `np.linalg.solve` is faster and more stable
- Eigenvalues of real non-symmetric matrices can be complex numbers
- PCA requires centered (mean-subtracted) data before eigendecomposition
- Covariance matrix is always symmetric positive semi-definite

## See Also
- [[math-for-ml]] - calculus companion
- [[unsupervised-learning]] - PCA, SVD applications
- [[numpy-fundamentals]] - numpy implementation
- [[neural-networks]] - weight matrices, transformations
