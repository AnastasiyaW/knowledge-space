---
title: "Analyse de complexité"
category: concepts
tags: [algorithms, big-o, time-complexity, space-complexity, asymptotic-analysis]
level: 3
source_sha256: 40297372b9620c726d06356563d52be7f1b9a32be8a13d1a3a8700ed230dcc57
translation: machine
translated_at: '2026-10-24'
---
# Analyse de complexité {#complexity-analysis}

L'analyse de complexité mesure la façon dont l'utilisation des ressources d'un algorithme (temps ou espace) évolue en fonction de la taille de l'entrée n. Elle fait abstraction du matériel et du langage, et se concentre sur les taux de croissance asymptotiques. Les notations de base sont Big-O (borne supérieure), Big-Omega (borne inférieure) et Big-Theta (borne serrée).

## Points clés {#key-facts}

- **Complexité temporelle** = nombre d'opérations en fonction de n, classé selon la croissance asymptotique
- **Complexité spatiale** = mémoire auxiliaire au-delà de l'entrée (convention : on rapporte la mémoire auxiliaire, et non la mémoire totale)
- Ignorer les constantes : O(2n) = O(n), O(100n) = O(n)
- Ne garder que le terme dominant : O(n^2 + 100n + 12) = O(n^2)
- Plusieurs paramètres possibles : O(n * m) lorsque les entrées ont des tailles différentes
- **Les facteurs constants cachés** comptent en pratique : deux algorithmes en O(n) peuvent différer d'un facteur 100

## Hiérarchie de complexité {#complexity-hierarchy}

```text
O(1) < O(log n) < O(sqrt(n)) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)
```

| Classe | Exemple |
|-------|---------|
| O(1) | Accès par index dans un tableau, test pair/impair avec `n & 1` |
| O(log n) | Recherche dichotomique, somme des chiffres, nombre de chiffres |
| O(sqrt(n)) | Boucle `while i*i < n` |
| O(n) | Recherche linéaire, minimum/maximum d'un tableau |
| O(n log n) | Tri fusion, tri optimal par comparaison |
| O(n^2) | Tri par sélection, two-sum par force brute, toutes les paires |
| O(n^3) | Multiplication matricielle naïve |
| O(2^n) | LCS récursif sans mémoïsation |
| O(n!) | Génération de toutes les permutations |

## Notation {#notation}

| Symbole | Signification | Décrit |
|--------|---------|-----------|
| O(f(n)) | Borne supérieure serrée | Pire cas (et en dessous) |
| Omega(f(n)) | Borne inférieure serrée | Meilleur cas (et au-dessus) |
| Theta(f(n)) | Borne exacte | À la fois supérieure et inférieure |
| o(f(n)) | Borne supérieure stricte | Croît strictement plus lentement que f |
| omega(f(n)) | Borne inférieure stricte | Croît strictement plus vite que f |

Les cas meilleur, moyen et pire sont indépendants de Big-O/Omega/Theta : chaque cas a son propre T(n), qui peut être borné séparément.

## Schémas {#patterns}

### Compter les opérations à partir du code {#counting-operations-from-code}

```python
# Single loop: O(n)
for elem in arr:
    process(elem)

# Nested loops: O(n^2)
for i in range(n):
    for j in range(n):
        process(i, j)

# Doubling step: i = 1, 2, 4, 8, ... n -> O(log n)
i = 1
while i < n:
    i *= 2

# Square root pattern: i*i < n -> O(sqrt(n))
i = 0
while i * i < n:
    i += 1

# Triangular loops: sum 0+1+2+...+(n-1) = n(n-1)/2 -> O(n^2)
for i in range(1, n + 1):
    for j in range(i):
        process(j)

# Inner loop depends on i^2: total = sum of i^2 = O(n^3)
for i in range(n):
    for j in range(i * i):
        process(j)

# Conditional inner loop at i == n//2 only: O(n) + O((n/2)^2) = O(n^2)
for i in range(n):
    if i == n // 2:
        for j in range(i * i):
            process(j)

# Conditional at constant i == 10: O(n) + O(100) = O(n)
for i in range(n):
    if i == 10:
        for j in range(i * i):
            process(j)
```

### Pièges de la complexité spatiale {#space-complexity-traps}

```python
# String concatenation creates new string: O(len(s1) + len(s2))
result = str1 + str2

# Building prefixes: total space O(n^2)
prefixes = [s[0:i] for i in range(len(s))]

# Reference vs copy
copy = arr        # O(1) - same object, NOT a copy
copy = arr.copy() # O(n) - actual copy

# Fixed-size array is O(1) space
occurrences = [0] * 26  # constant regardless of input
```

### Plusieurs paramètres {#multiple-parameters}

```python
# O(n * m) where n = len(arr1), m = len(arr2)
def intersection(arr1, arr2):
    for elem in arr1:
        if elem in arr2:  # O(m) scan each time
            print(elem)

# O(min(n, m)) - loop terminates at shorter
def where_equal(str1, str2):
    i = 0
    while i < len(str1) and i < len(str2):
        if str1[i] == str2[i]:
            yield i
        i += 1
```

## Meilleur, moyen, pire cas {#best-average-worst-case}

- **Meilleur cas :** entrée la plus favorable (par exemple, élément à l'index 0 pour une recherche linéaire)
- **Pire cas :** entrée la moins favorable (par exemple, élément absent)
- **Cas moyen :** coût espéré sur l'ensemble des entrées possibles ; nécessite des hypothèses probabilistes
- Un **algorithme randomisé** utilise un aléa interne pour transformer le pire cas en moyenne espérée

## Pièges à éviter {#gotchas}

- Deux algorithmes en O(n) peuvent présenter une différence de temps d'exécution de 100x à cause des constantes
- Un algorithme en O(n log n) de constante 13 peut être plus lent qu'un algorithme en O(n^2) de constante 0.5 pour n < 200
- O(n^2) et O(m^2) sont incomparables sans connaître la relation entre n et m
- La somme des chiffres de n a une complexité en O(log n) (n possède floor(log10(n))+1 chiffres)
- `max(n, 10)` dans une condition de boucle : O(n) pour les grands n, O(1) pour n < 10
- `min(n, 10)` dans une condition de boucle : toujours O(1), quel que soit n

## Voir aussi {#see-also}

- [[amortized-analysis]] - coût moyen par opération sur des séquences
- [[complexity-classes]] - P, NP, NP-complet, NP-difficile
- [[sorting-algorithms]] - comparaison de la complexité des méthodes de tri
