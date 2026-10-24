---
title: "Algorithmes de tri"
category: algorithms
tags: [algorithms, sorting, comparison-sort, merge-sort, quick-sort, radix-sort]
level: 3
source_sha256: 58913e5b33db38b57aff1ed791e7fa72a908f54c1a3a2425274a199877cdb4b1
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes de tri {#sorting-algorithms}

Référence complète des algorithmes de tri couvrant les tris par comparaison (insertion, bulle, sélection, fusion, rapide, tas), les tris sans comparaison (comptage, base, seaux) et leurs propriétés. La borne inférieure théorique pour le tri par comparaison est Omega(n log n).

## Tableau comparatif {#comparison-table}

| Algorithme | Meilleur | Moyen | Pire | Espace | Stable | En place |
|-----------|------|---------|-------|-------|--------|----------|
| Tri par insertion | O(n) | O(n^2) | O(n^2) | O(1) | Oui | Oui |
| Tri à bulles | O(n) | O(n^2) | O(n^2) | O(1) | Oui | Oui |
| Tri par sélection | O(n^2) | O(n^2) | O(n^2) | O(1) | Non | Oui |
| Tri par tas | O(n log n) | O(n log n) | O(n log n) | O(1) | Non | Oui |
| Tri fusion | O(n log n) | O(n log n) | O(n log n) | O(n) | Oui | Non |
| Tri rapide | O(n log n) | O(n log n) | O(n^2) | O(log n) | Non | Oui |
| Tri par comptage | O(n+k) | O(n+k) | O(n+k) | O(k) | Oui | Non |
| Tri par base | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Oui | Non |
| Tri par seaux | O(n+k) | O(n+k) | O(n^2) | O(n+k) | Oui | Non |

## Propriétés de classification {#classification-properties}

| Propriété | Définition |
|----------|-----------|
| **Stable** | Les éléments égaux conservent leur ordre relatif d'origine |
| **En place** | Utilise un espace auxiliaire en O(1) |
| **Adaptatif** | Plus rapide sur une entrée presque triée |
| **En ligne** | Peut traiter l'entrée séquentiellement |
| **Basé sur la comparaison** | Utilise uniquement des comparaisons d'éléments pour déterminer l'ordre |

## Faits essentiels {#key-facts}

- **Borne inférieure des tris par comparaison** : Omega(n log n) - démonstration par arbre de décision (n! feuilles, hauteur de l'arbre >= log2(n!) = Omega(n log n))
- **Les tris sans comparaison** contournent cette barrière en exploitant la structure des clés (comptage, base, seaux)
- `sorted()` et `.sort()` de Python utilisent **Timsort** (hybride fusion+insertion) : O(n log n) au pire, O(n) au meilleur, stable, adaptatif

## Motifs {#patterns}

### Tri par insertion {#insertion-sort}

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
```

Idéal pour : petits tableaux, données presque triées, tri en ligne. Cas optimal en O(n) sur une entrée déjà triée.

### Tri par sélection {#selection-sort}

```python
def selection_sort(arr):
    for i in range(len(arr)):
        pos_min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[pos_min]:
                pos_min = j
        arr[i], arr[pos_min] = arr[pos_min], arr[i]
```

Toujours en O(n^2), quel que soit l'ordre de l'entrée. Non adaptatif, non stable.

### Tri fusion {#merge-sort}

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

Récurrence : T(n) = 2T(n/2) + O(n) -> O(n log n). L'arbre de récursion comporte log2(n) niveaux, chacun effectuant O(n) travail de fusion. Stable mais nécessite un espace supplémentaire en O(n).

### Tri rapide {#quick-sort}

```python
def quick_sort(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
```

O(n^2) au pire lorsque le pivot est systématiquement le pire (tableau trié et choix toujours du premier/dernier élément). O(n log n) en moyenne. En pratique plus rapide que le tri fusion grâce à la localité de cache et aux petites constantes. Le pire cas est rare avec un pivot aléatoire ou médiane de trois.

### Tri par comptage {#counting-sort}

Pour des entiers dans l'intervalle [0, k). Temps O(n + k), espace O(k). Utile lorsque k = O(n).

### Tri par base {#radix-sort}

Tri par chiffres du poids faible au poids fort (LSD vers MSD), en utilisant le tri par comptage comme sous-routine. Temps O(d(n+k)) où d = nombre de chiffres, k = intervalle des chiffres. Pour des entiers de largeur fixe : O(n).

### Tri intégré de Python {#python-built-in-sorting}

```python
sorted(strs)                          # lexicographic
sorted(strs, key=len)                 # by length
sorted(strs, key=lambda s: s.count('c'))  # by custom criterion
sorted(products, key=lambda p: p['price'])  # by dict field
```

## Pièges {#gotchas}

- Le tri rapide atteint O(n^2) au pire sur des tableaux déjà triés avec un pivot naïf (premier/dernier élément)
- Le tri par sélection n'est PAS stable : les échanges sur de longues distances déplacent les éléments égaux
- Le tri à bulles avec un drapeau d'arrêt anticipé devient adaptatif (O(n) sur une entrée triée)
- Le tri de Shell (insertion à intervalles décroissants) atteint O(n log^2 n) avec les intervalles de Hibbard
- Le tri par comptage exige des entiers positifs ou nuls dans un intervalle connu
- Le tri par seaux dégénère en O(n^2) si tous les éléments tombent dans le même seau

## Voir aussi {#see-also}

- [[complexity-analysis]] - comprendre la notation O
- [[searching-algorithms]] - la recherche dichotomique exige une entrée triée
- [[functions]] - détails sur sorted() et sort()
