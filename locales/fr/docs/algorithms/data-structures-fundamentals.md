---
title: "Fondamentaux des structures de données - Tableaux, tables de hachage, listes chaînées"
category: concepts
tags: [data-structures, arrays, hash-tables, linked-lists, stacks, queues, big-o]
level: 2
source_sha256: bdf6b5188d6245ac9fb3477c00081e22c4181b53b6dc5c48730cda447ec9e825
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux des structures de données - Tableaux, tables de hachage, listes chaînées {#data-structures-fundamentals-arrays-hash-tables-linked-lists}

Opérations de base sur les structures de données et analyse de complexité : tableaux, tableaux triés avec recherche binaire, tables de hachage, listes chaînées, piles et files. Accent sur le coût des opérations et le choix de chaque structure.

## Points clés {#key-facts}

- Big O mesure le nombre d'étapes (indépendant du matériel), et non le temps ; il ignore les constantes
- Tableaux : lecture par index en O(1), insertion/suppression en O(N) (décalage)
- Tables de hachage : lecture/écriture/suppression par clé en O(1) en moyenne, recherche par valeur en O(N)
- Listes chaînées : insertion/suppression à une position connue en O(1), lecture par index en O(N)
- Recherche binaire sur tableau trié : O(log N) - 1 M d'éléments = 20 étapes au maximum
- Facteur de charge idéal d'une table de hachage = 0,7 (7 éléments pour 10 cases)

## Motifs {#patterns}

### Opérations sur les tableaux {#array-operations}

| Opération | Étapes | Remarques |
|-----------|--------|-----------|
| Lecture par index | O(1) | Calcul direct de l'adresse |
| Recherche (linéaire) | O(N) | Chaque élément doit être vérifié |
| Insertion en fin | O(1) | Placer à l'adresse suivante |
| Insertion en début | O(N) | Décaler les éléments vers la droite |
| Suppression | O(N) | Décaler les éléments vers la gauche |

**Ensembles (sans doublons)** : l'insertion nécessite d'abord une recherche en O(N), ce qui rend l'insertion en O(N) même en fin de tableau.

### Recherche binaire {#binary-search}

```python
def binary_search(array, target):
    lo, hi = 0, len(array) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoids integer overflow
        if array[mid] == target: return mid
        elif array[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return None
```

| Éléments | Maximum recherche linéaire | Maximum recherche binaire |
|----------|---------------------------|---------------------------|
| 100 | 100 | 7 |
| 10 000 | 10 000 | 14 |
| 1 000 000 | 1 000 000 | 20 |

### Tables de hachage {#hash-tables}

Une fonction de hachage convertit une clé en index de tableau. La gestion des collisions se fait par chaînage (un tableau de paires clé-valeur dans chaque case).

**Motif d'optimisation** - convertir un tableau en table de hachage pour des recherches en O(1) :
```ruby
hash = {}
array.each { |elem| hash[elem] = true }
# Now: hash[value] -> O(1) instead of O(N) scan
```

**Vérification de sous-ensemble dans un tableau** - naïve en O(N*M), optimisée en O(N+M) :
```javascript
function isSubset(array1, array2) {
  const larger = array1.length > array2.length ? array1 : array2;
  const smaller = array1.length > array2.length ? array2 : array1;
  const hashTable = {};
  for (const elem of larger) { hashTable[elem] = true; }
  for (const elem of smaller) {
    if (!hashTable[elem]) return false;
  }
  return true;
}
```

**Remplacer des conditionnelles par une recherche dans une table de hachage** :
```python
STATUS_CODES = {200: "OK", 301: "Moved Permanently", 404: "Not Found", 500: "Internal Server Error"}
def status_code_meaning(code):
    return STATUS_CODES.get(code)
```

### Listes chaînées {#linked-lists}

| Opération | Liste chaînée | Tableau |
|-----------|---------------|---------|
| Lecture par index | O(N) | O(1) |
| Insertion à une position connue | O(1) | O(N) |
| Insertion en tête | O(1) | O(N) |
| Suppression à une position connue | O(1) | O(N) |
| Recherche | O(N) | O(N) |

File sur liste doublement chaînée : enfiler = insertion en fin en O(1), défiler = suppression en tête en O(1). Meilleure qu'une file basée sur un tableau.

### Piles et files {#stacks-and-queues}

**Pile (LIFO)** : empiler/dépiler par la même extrémité. Utilisée pour : appels de fonctions, annulation, DFS.
**File (FIFO)** : enfiler à l'arrière, défiler à l'avant. Utilisée pour : BFS, files de tâches.

### Référence Big O {#big-o-reference}

| Notation | Nom | Exemple |
|----------|-----|---------|
| O(1) | Constante | Lecture de tableau, recherche dans une table de hachage |
| O(log N) | Logarithmique | Recherche binaire, opérations sur un ABR |
| O(N) | Linéaire | Recherche linéaire, parcours |
| O(N log N) | Linéarithmique | Tri rapide (moyenne), tri fusion |
| O(N^2) | Quadratique | Tri à bulles, par insertion, par sélection |
| O(2^N) | Exponentielle | Combinaisons par force brute |

**Important** : Big O ignore les constantes. O(N/2), O(2N) et O(100N) se simplifient toutes en O(N). Les constantes comptent au sein d'une même catégorie.

### Complexité spatiale {#space-complexity}

| Structure | Espace |
|-----------|--------|
| Tableau de N éléments | O(N) |
| Matrice N x N | O(N^2) |
| Profondeur de récursion D | O(D) cadres de pile |
| Table de hachage de N éléments | O(N) |

## Pièges {#gotchas}

- La recherche dans une table de hachage n'est en O(1) qu'avec la clé ; la recherche par valeur est en O(N)
- La recherche binaire exige des données triées : le coût du tri en O(N log N) peut ne pas être rentable pour une recherche unique
- Compromis du tableau trié : recherche plus rapide en O(log N), mais insertion plus lente en O(N) pour maintenir l'ordre
- Big O meilleur/pire cas : la complexité énoncée est généralement celle du pire cas ; la recherche linéaire est en O(1) au mieux, O(N) au pire

## Voir aussi {#see-also}

- [[trees-and-graphs]] - ABR, tas, tries, BFS, DFS, Dijkstra
- [[sorting-algorithms]] - implémentations détaillées des tris et comparaisons
- [[dynamic-programming]] - mémoïsation, motifs de récursion
- [[algorithms/problem-patterns]] - deux pointeurs, fenêtre glissante, techniques d'entretien
