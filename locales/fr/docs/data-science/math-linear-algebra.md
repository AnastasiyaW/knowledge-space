---
title: "Algèbre linéaire pour la science des données"
category: foundations
tags: [data-science, math, linear-algebra, matrices, eigenvalues]
level: 4
source_sha256: 91f241eea03317f7e49ae36a3a892bd0354653503b4984b49cc41be704b67eec
translation: machine
translated_at: '2026-10-24'
---
# Algèbre linéaire pour la science des données {#linear-algebra-for-data-science}

Les vecteurs, les matrices et leurs opérations constituent l'épine dorsale computationnelle du ML. Chaque jeu de données est une matrice, chaque prédiction est une multiplication matricielle, chaque réduction de dimensionnalité utilise une décomposition en éléments propres.

## Vecteurs {#vectors}

Tableau ordonné de nombres. Représente un point ou une direction dans un espace à n dimensions.

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.dot(a, b)       # 32 (dot product)
np.linalg.norm(a)  # 3.74 (L2 norm)
np.cross(a, b)     # cross product (3D only)
```

**Opérations :**
- **Produit scalaire** : a . b = sum(a_i * b_i) = |a| * |b| * cos(theta). Si 0, les vecteurs sont orthogonaux
- **Norme L2** (euclidienne) : ||a|| = sqrt(sum(a_i^2))
- **Norme L1** (de Manhattan) : sum(|a_i|)

**En ML** : vecteurs de caractéristiques, vecteurs de poids, vecteurs de gradient, calcul de distances.

## Matrices {#matrices}

Tableau 2D, de forme (m x n). Jeu de données : lignes = échantillons, colonnes = caractéristiques.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B              # matrix multiplication
A.T                # transpose
np.linalg.inv(A)   # inverse
np.linalg.det(A)   # determinant
```

**Propriétés clés :**
- AB != BA (non commutative)
- (AB)^T = B^T * A^T
- (AB)C = A(BC) (associative)

**Matrices particulières :**
- **Identité** (I) : diagonale de 1. AI = IA = A
- **Diagonale** : non nulle uniquement sur la diagonale principale
- **Symétrique** : A = A^T (les matrices de covariance sont symétriques)
- **Orthogonale** : Q^T Q = I (les colonnes sont orthonormées)

## Inverse d'une matrice {#matrix-inverse}

A^(-1) existe si et seulement si det(A) != 0 (non singulière). A * A^(-1) = I.

```python
A_inv = np.linalg.inv(A)     # raises error if singular
A_pinv = np.linalg.pinv(A)   # pseudo-inverse (always exists)
np.linalg.solve(A, b)        # solve Ax=b (faster than inv(A) @ b)
```

**Matrice singulière** (det = 0) : les colonnes sont linéairement dépendantes, pas de solution unique.

## Valeurs propres et vecteurs propres {#eigenvalues-and-eigenvectors}

A * v = lambda * v. Le vecteur v conserve sa direction et est multiplié par lambda.

```python
eigenvalues, eigenvectors = np.linalg.eig(A)
```

**En ML :**
- **PCA** : les vecteurs propres de la matrice de covariance = composantes principales ; les valeurs propres = variance expliquée
- **Clustering spectral** : vecteurs propres du laplacien du graphe
- **PageRank** : vecteur propre dominant de la matrice d'adjacence
- **Définie positive** (toutes les valeurs propres > 0) : Hessienne en un minimum local

## Décomposition en valeurs singulières (SVD) {#singular-value-decomposition-svd}

Toute matrice A(m x n) = U * Sigma * V^T

```python
U, S, Vt = np.linalg.svd(A)
# U: left singular vectors (m x m)
# S: singular values (sorted descending)
# Vt: right singular vectors (n x n)
```

**Applications :**
- Réduction de dimensionnalité (SVD tronquée - conserver les k premières)
- Approximation de matrices de rang faible
- Systèmes de recommandation (factorisation matricielle)
- Compression d'images
- Calcul de la pseudo-inverse

## Systèmes d'équations linéaires {#systems-of-linear-equations}

Ax = b.
- Solution unique : det(A) != 0 -> x = A^(-1)b
- Pas de solution : incohérent (sur-déterminé)
- Solutions infinies : sous-déterminé

```python
x = np.linalg.solve(A, b)  # numerically stable
# NOT: np.linalg.inv(A) @ b (less stable, slower)
```

## Concepts clés pour le ML {#key-concepts-for-ml}

- **Indépendance linéaire** : les vecteurs ne peuvent pas s'exprimer comme combinaisons d'autres vecteurs
- **Rang** : nombre maximal de lignes/colonnes linéairement indépendantes
- **Théorème du rang** : rang + nullité = nombre de colonnes
- **Définie positive** : x^T A x > 0 pour tout x != 0. Hessienne définie positive = minimum local
- **Forme quadratique** : Q(x) = x^T A x. Classification selon le signe des valeurs propres

## Pièges courants {#gotchas}
- L'ordre de multiplication des matrices compte : (100x3) @ (3x50) fonctionne, mais (3x50) @ (100x3) ne fonctionne pas
- `np.linalg.inv` doit être évitée lorsque c'est possible : `np.linalg.solve` est plus rapide et plus stable
- Les valeurs propres de matrices réelles non symétriques peuvent être des nombres complexes
- La PCA nécessite des données centrées (moyenne soustraite) avant la décomposition en éléments propres
- La matrice de covariance est toujours symétrique semi-définie positive

## Voir aussi {#see-also}
- [[math-for-ml]] - compagnon du calcul différentiel
- [[unsupervised-learning]] - applications de la PCA et de la SVD
- [[numpy-fundamentals]] - implémentation avec numpy
- [[neural-networks]] - matrices de poids, transformations
