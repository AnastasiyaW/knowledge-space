---
title: Linear Algebra for ML
category: math-foundations
tags: [linear-algebra, vectors, matrices, eigenvalues, svd, numpy]
---

# Linear Algebra for ML

Vectors, matrices, and their operations form the computational backbone of every ML algorithm. Data is represented as matrices, model parameters as vectors, transformations as matrix multiplications. Understanding linear algebra is prerequisite for grasping gradient descent, PCA, neural network layers, and image processing kernels.

## Key Facts

- A **vector** is an ordered array of numbers; in ML context, a feature vector describes one data sample
- A **matrix** is a 2D array; a dataset with N samples and M features is an (N x M) matrix
- **Dot product** of two vectors: sum of element-wise products; measures similarity (cosine similarity derives from it)
- **Matrix multiplication** (A @ B): inner dimensions must match; result shape is (rows_A, cols_B)
- **Transpose** flips rows and columns: shape (N, M) becomes (M, N)
- **Inverse** A^(-1) exists only for square, non-singular matrices; A @ A^(-1) = I (identity)
- **Determinant** = 0 means matrix is singular (no inverse, linearly dependent columns)
- **Eigenvalues/eigenvectors**: Av = lambda * v; directions that only get scaled under transformation A
- **SVD** (Singular Value Decomposition): any matrix M = U * Sigma * V^T; foundation of [[dimensionality-reduction]] (PCA) and recommender systems
- **Rank** of a matrix = number of linearly independent rows/columns; determines if a system of equations has a unique solution
- [[convolutional-neural-networks]] use matrix operations (convolution = cross-correlation with a kernel matrix)

## Patterns

```python
import numpy as np

# Vectors and dot product
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
dot = np.dot(a, b)          # 32
dot_alt = a @ b              # same

# Matrix creation and multiplication
X = np.random.randn(100, 5)  # 100 samples, 5 features
W = np.random.randn(5, 3)    # weight matrix
output = X @ W                # (100, 3)

# Transpose
X_T = X.T                    # (5, 100)

# Inverse (square matrices only)
A = np.array([[1, 2], [3, 4]])
A_inv = np.linalg.inv(A)
identity = A @ A_inv          # ~eye(2)

# Determinant
det = np.linalg.det(A)        # -2.0

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# SVD
U, sigma, Vt = np.linalg.svd(X, full_matrices=False)
# Reconstruct: X_approx = U @ np.diag(sigma) @ Vt

# Cosine similarity
from numpy.linalg import norm
cos_sim = np.dot(a, b) / (norm(a) * norm(b))

# Solve linear system Ax = b
b_vec = np.array([5, 6])
x = np.linalg.solve(A, b_vec)

# Frobenius norm (matrix "magnitude")
frob = np.linalg.norm(X, 'fro')
```

## Gotchas

- `np.dot` on 2D arrays does matrix multiplication, NOT element-wise; use `*` for element-wise
- Matrix inverse is numerically unstable; prefer `np.linalg.solve(A, b)` over `np.linalg.inv(A) @ b`
- Eigenvalue decomposition only works on square matrices; use SVD for rectangular ones
- Broadcasting in NumPy silently reshapes arrays -- shape (3,) + shape (3,1) gives (3,3), not (3,)
- In ML, data matrix convention: rows = samples, columns = features (sklearn expects this)

## See Also

- [[dimensionality-reduction]] - PCA uses eigendecomposition of the covariance matrix
- [[neural-network-fundamentals]] - forward pass = chain of matrix multiplications + activations
- [[gradient-descent-and-optimization]] - gradient is a vector, Hessian is a matrix
- NumPy linalg docs: https://numpy.org/doc/stable/reference/routines.linalg.html
