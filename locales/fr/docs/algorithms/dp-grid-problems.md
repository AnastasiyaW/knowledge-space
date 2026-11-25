---
title: "DP : problèmes de grille et de combinatoire"
category: algorithms
tags: [algorithms, dynamic-programming, grid, matrix, partition, combinatorics]
level: 3
source_sha256: 33bc4326a61186df21d5dc1869b38ebfbd6af0e02df04828518f284fe8165e83
translation: machine
translated_at: '2026-10-24'
---
# DP : problèmes de grille et de combinatoire {#dp-grid-and-combinatorics-problems}

Problèmes de programmation dynamique sur grille et en combinatoire : problème de partition, carré maximal, comptage de chaînes de voyelles triées et comptage de motifs. Ces problèmes combinent la sélection de sous-ensembles avec des contraintes géométriques ou de comptage.

## Points clés {#key-facts}

- **Problème de partition** : se ramène à la somme de sous-ensembles avec cible = total/2. Temps O(n * sum)
- **Carré maximal** : dp[i][j] = 1 + min(gauche, dessus, diagonale). Temps O(nm)
- **Comptage de chaînes de voyelles triées** : étoiles et barres = C(n+4, 4), ou DP avec sommes préfixes
- Le problème de partition est NP-complet mais admet une solution DP pseudo-polynomiale

## Motifs {#patterns}

### Problème de partition {#partition-problem}

Diviser un tableau en deux sous-ensembles de même somme. Cela revient à se demander si un sous-ensemble a pour somme total/2.

```python
def partition(arr):
    s = sum(arr)
    if s % 2 == 1:
        return False  # odd sum impossible
    target = s // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in arr:
        for t in range(target, x - 1, -1):  # backward: use each item once
            dp[t] = dp[t] or dp[t - x]
    return dp[target]
```

**Pourquoi itérer à rebours :** cela garantit que chaque élément est utilisé au plus une fois. Une itération en sens direct permettrait de réutiliser le même élément (variante illimitée).

### Carré maximal de uns - O(nm) {#maximal-square-of-ones-onm}

Trouver l'aire du plus grand sous-carré de la matrice ne contenant que des 1.

**Relation de récurrence :**
```yaml
if matrix[i][j] == 0: dp[i][j] = 0
else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```

Pourquoi le minimum des trois : pour former un carré de côté k en (i,j), il faut des carrés de côté k-1 au-dessus, à gauche et en diagonale. Le facteur limitant est le plus petit d'entre eux.

```python
def maximal_square(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * m for _ in range(n)]
    max_side = 0
    for j in range(m):
        dp[0][j] = matrix[0][j]
    for i in range(n):
        dp[i][0] = matrix[i][0]
    for i in range(1, n):
        for j in range(1, m):
            if matrix[i][j] == 0:
                dp[i][j] = 0
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
            max_side = max(max_side, dp[i][j])
    return max_side ** 2  # area
```

### Comptage de chaînes de voyelles triées {#count-sorted-vowel-strings}

Compter les chaînes de longueur n formées des voyelles a, e, i, o, u dans un ordre non décroissant.

```python
def count_vowel_strings(n):
    dp = [1] * 5  # length 1: one string per vowel
    for _ in range(1, n):
        new_dp = [0] * 5
        for v in range(5):
            new_dp[v] = sum(dp[:v + 1])  # can use same or earlier vowel
        dp = new_dp
    return sum(dp)
```

Raccourci mathématique : C(n+4, 4) (étoiles et barres).

### Motifs généraux de DP en combinatoire {#general-combinatorics-dp-patterns}

**Comptage de chemins dans un DAG :**
```python
dp[v] = sum(dp[u] for all u with edge u -> v)
```

**Comptage de chaînes de bits avec contraintes :**
```python
dp[i][last] = count of valid strings of length i ending with `last`
```

**Comptage des partitions de n en k parties :**
```python
dp[n][k] = dp[n-1][k-1] + dp[n-k][k]
```

## Pièges à éviter {#gotchas}

- Partition : la somme totale doit être paire, sinon renvoyer immédiatement False
- Carré maximal : ne pas oublier les cas de base (première ligne et première colonne recopiées directement)
- Le carré maximal renvoie l'aire (côté^2), et non la longueur du côté
- Une optimisation de l'espace en O(m) avec l'astuce des deux lignes est possible pour les deux problèmes de grille
- La version avec mémoïsation du problème de partition utilise l'état (index, somme_restante) et non (index, somme1, somme2)

## Voir aussi {#see-also}

- [[dp-optimization-problems]] - somme de sous-ensembles, sac à dos (étroitement lié à la partition)
- [[dynamic-programming-fundamentals]] - approche DP et descendante vs ascendante
- [[dp-sequence-problems]] - motifs de DP sur les chaînes
