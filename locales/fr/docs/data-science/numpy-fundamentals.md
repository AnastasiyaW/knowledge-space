---
title: "Fondamentaux de NumPy"
category: tools
tags: [data-science, numpy, python, arrays]
level: 2
source_sha256: 976f3246da850e9df87b7a12383d34f68339d09ee646e234bdb04617e5d4003b
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de NumPy {#numpy-fundamentals}

NumPy est la fondation de calcul numérique sur laquelle reposent pandas, scikit-learn et PyTorch. Son ndarray permet des opérations vectorisées 10 à 100 fois plus rapides que les boucles Python.

## Bases des tableaux {#array-basics}

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

## Opérations élément par élément {#element-wise-operations}

Contrairement aux listes Python, NumPy opère élément par élément :
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a + b    # [5, 7, 9]  (not concatenation!)
a * b    # [4, 10, 18]
a ** 2   # [1, 4, 9]
a > 2    # [False, False, True]
```

## Opérations matricielles {#matrix-operations}

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

## Agrégations {#aggregations}

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

## Indexation et découpage {#indexing-and-slicing}

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

## Broadcasting {#broadcasting}

NumPy étend automatiquement les dimensions pour les opérations sur des tableaux de formes différentes :
```python
A = np.array([[1, 2, 3], [4, 5, 6]])  # shape (2, 3)
b = np.array([10, 20, 30])             # shape (3,)
A + b   # [[11, 22, 33], [14, 25, 36]]  - b broadcast to each row
```

Règles : les dimensions sont comparées de droite à gauche. Elles sont compatibles si elles sont égales ou si l'une d'elles vaut 1.

## Génération de nombres aléatoires {#random-number-generation}

```python
np.random.seed(42)                    # reproducibility
np.random.uniform(0, 1, size=10)      # uniform
np.random.normal(0, 1, size=10)       # normal
np.random.randint(0, 100, size=10)    # integers
np.random.choice([1,2,3], size=5)     # sample with replacement
np.random.shuffle(arr)                 # in-place shuffle
```

## Remodelage {#reshaping}

```python
a = np.arange(12)
a.reshape(3, 4)       # 3x4 matrix
a.reshape(-1, 4)      # infer rows: (3, 4)
a.flatten()            # back to 1D
a.ravel()              # 1D view (no copy if possible)
np.expand_dims(a, 0)  # add dimension: (1, 12)
np.squeeze(a)          # remove dimensions of size 1
```

## Performance {#performance}

- Les opérations vectorisées sont 10 à 100 fois plus rapides que les boucles Python
- Éviter les boucles `for` sur les éléments d'un tableau
- Utiliser l'indexation booléenne au lieu d'un `if` à l'intérieur des boucles
- Pandas utilise NumPy en arrière-plan : il est rare d'avoir besoin de NumPy directement dans une analyse exploratoire typique

## Pièges courants {#gotchas}
- `a * b` est un produit élément par élément, PAS un produit matriciel. Utiliser `a @ b` ou `np.dot(a, b)`
- Les tableaux NumPy sont mutables : `b = a` crée une référence, et non une copie. Utiliser `b = a.copy()`
- Division entière : `np.array([1, 2, 3]) / 2` renvoie des flottants. Utiliser `//` pour la division entière
- Le broadcasting peut produire silencieusement des résultats erronés si les formes sont compatibles par accident

## Voir aussi {#see-also}
- [[pandas-eda]] - pandas, construit sur numpy
- [[math-linear-algebra]] - théorie derrière les opérations matricielles
- [[neural-networks]] - opérations sur les tenseurs en apprentissage profond
