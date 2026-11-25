---
title: "Lineare Algebra für Data Science"
category: foundations
tags: [data-science, math, linear-algebra, matrices, eigenvalues]
level: 4
source_sha256: 91f241eea03317f7e49ae36a3a892bd0354653503b4984b49cc41be704b67eec
translation: machine
translated_at: '2026-10-24'
---
# Lineare Algebra für Data Science {#linear-algebra-for-data-science}

Vektoren, Matrizen und deren Operationen bilden das rechnerische Fundament des maschinellen Lernens. Jeder Datensatz ist eine Matrix, jede Vorhersage ist eine Matrixmultiplikation, und jede Dimensionsreduktion nutzt die Eigenzerlegung.

## Vektoren {#vectors}

Geordnetes Array von Zahlen. Repräsentiert einen Punkt oder eine Richtung im n-dimensionalen Raum.

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.dot(a, b)       # 32 (dot product)
np.linalg.norm(a)  # 3.74 (L2 norm)
np.cross(a, b)     # cross product (3D only)
```

**Operationen:**
- **Skalarprodukt**: a . b = sum(a_i * b_i) = |a| * |b| * cos(theta). Ist es 0, sind die Vektoren orthogonal
- **L2-Norm** (Euklidisch): ||a|| = sqrt(sum(a_i^2))
- **L1-Norm** (Manhattan): sum(|a_i|)

**Im ML**: Merkmalsvektoren, Gewichtsvektoren, Gradientenvektoren, Abstandsberechnung.

## Matrizen {#matrices}

Zweidimensionales Array, Form (m x n). Datensatz: Zeilen = Samples, Spalten = Merkmale.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B              # matrix multiplication
A.T                # transpose
np.linalg.inv(A)   # inverse
np.linalg.det(A)   # determinant
```

**Wichtige Eigenschaften:**
- AB != BA (nicht kommutativ)
- (AB)^T = B^T * A^T
- (AB)C = A(BC) (assoziativ)

**Spezielle Matrizen:**
- **Einheitsmatrix** (I): Diagonale aus 1en. AI = IA = A
- **Diagonalmatrix**: nur auf der Hauptdiagonale ungleich null
- **Symmetrisch**: A = A^T (Kovarianzmatrizen sind symmetrisch)
- **Orthogonal**: Q^T Q = I (Spalten sind orthonormal)

## Matrixinverse {#matrix-inverse}

A^(-1) existiert genau dann, wenn det(A) != 0 (regulär). A * A^(-1) = I.

```python
A_inv = np.linalg.inv(A)     # raises error if singular
A_pinv = np.linalg.pinv(A)   # pseudo-inverse (always exists)
np.linalg.solve(A, b)        # solve Ax=b (faster than inv(A) @ b)
```

**Singuläre Matrix** (det = 0): Spalten sind linear abhängig, keine eindeutige Lösung.

## Eigenwerte und Eigenvektoren {#eigenvalues-and-eigenvectors}

A * v = lambda * v. Der Vektor v bleibt in seiner Richtung erhalten und wird um lambda skaliert.

```python
eigenvalues, eigenvectors = np.linalg.eig(A)
```

**Im ML:**
- **PCA**: Eigenvektoren der Kovarianzmatrix = Hauptkomponenten; Eigenwerte = erklärte Varianz
- **Spektrales Clustering**: Eigenvektoren des Graph-Laplace-Operators
- **PageRank**: dominanter Eigenvektor der Adjazenzmatrix
- **Positiv definit** (alle Eigenwerte > 0): Hesse-Matrix an einem lokalen Minimum

## Singulärwertzerlegung (SVD) {#singular-value-decomposition-svd}

Jede Matrix A(m x n) = U * Sigma * V^T

```python
U, S, Vt = np.linalg.svd(A)
# U: left singular vectors (m x m)
# S: singular values (sorted descending)
# Vt: right singular vectors (n x n)
```

**Anwendungen:**
- Dimensionsreduktion (gekürzte SVD - die k größten behalten)
- Approximation durch Matrizen niedrigen Rangs
- Empfehlungssysteme (Matrixfaktorisierung)
- Bildkompression
- Berechnung der Pseudoinversen

## Lineare Gleichungssysteme {#systems-of-linear-equations}

Ax = b.
- Eindeutige Lösung: det(A) != 0 -> x = A^(-1)b
- Keine Lösung: inkonsistent (überbestimmt)
- Unendlich viele Lösungen: unterbestimmt

```python
x = np.linalg.solve(A, b)  # numerically stable
# NOT: np.linalg.inv(A) @ b (less stable, slower)
```

## Zentrale Konzepte für ML {#key-concepts-for-ml}

- **Lineare Unabhängigkeit**: Vektoren lassen sich nicht als Kombinationen anderer Vektoren darstellen
- **Rang**: maximale Anzahl linear unabhängiger Zeilen/Spalten
- **Rangsatz** (Rank-Nullity-Theorem): Rang + Nullität = Anzahl der Spalten
- **Positiv definit**: x^T A x > 0 für alle x != 0. Positiv definite Hesse-Matrix = lokales Minimum
- **Quadratische Form**: Q(x) = x^T A x. Klassifikation anhand der Vorzeichen der Eigenwerte

## Stolperfallen {#gotchas}
- Die Reihenfolge der Matrixmultiplikation ist wichtig: (100x3) @ (3x50) funktioniert, (3x50) @ (100x3) dagegen nicht
- `np.linalg.inv` sollte wenn möglich vermieden werden - `np.linalg.solve` ist schneller und numerisch stabiler
- Eigenwerte reeller, nicht symmetrischer Matrizen können komplexe Zahlen sein
- PCA erfordert zentrierte (mittelwertbereinigte) Daten vor der Eigenzerlegung
- Die Kovarianzmatrix ist immer symmetrisch positiv semidefinit

## Siehe auch {#see-also}
- [[math-for-ml]] - Begleitthema Analysis
- [[unsupervised-learning]] - Anwendungen von PCA und SVD
- [[numpy-fundamentals]] - Implementierung mit NumPy
- [[neural-networks]] - Gewichtsmatrizen, Transformationen
