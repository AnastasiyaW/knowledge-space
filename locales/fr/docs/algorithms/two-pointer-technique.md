---
title: "Technique des deux pointeurs"
category: patterns
tags: [algorithms, two-pointers, sorted-array, optimization, space-time-tradeoff]
level: 3
source_sha256: 58cd00b0eb6311f92646aa72bdd41435fcec7376a67799b1633039c8a1b757cb
translation: machine
translated_at: '2026-10-24'
---
# Technique des deux pointeurs {#two-pointer-technique}

La technique des deux pointeurs utilise deux indices pour parcourir des structures de données (typiquement des tableaux), ce qui réduit la complexité temporelle en exploitant l'ordre trié ou d'autres propriétés structurelles. Elle est courante dans les problèmes impliquant des paires, des sous-tableaux et des sous-séquences.

## Points clés {#key-facts}

- Permet généralement de ramener une approche par force brute en O(n^2) à O(n) ou O(n log n)
- Nécessite un tableau trié pour l'approche à pointeurs convergents
- Deux variantes : convergente (gauche/droite se rapprochant l'un de l'autre) et parallèle (les deux avancent dans le même sens)
- Fait souvent partie du compromis espace-temps : O(n^2) temps O(1) espace -> O(n) temps O(n) espace (hachage) ou O(n log n) temps O(1) espace (tri + deux pointeurs)

## Patrons {#patterns}

### Somme de deux avec tri + deux pointeurs - O(n log n) {#two-sum-with-sort-two-pointers-on-log-n}

```python
def find_pair(arr, k):
    arr = sorted(arr)
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == k:
            return True
        elif s < k:
            left += 1   # need larger sum
        else:
            right -= 1  # need smaller sum
    return False
```

Pourquoi ça fonctionne : lorsque la somme est trop petite, seul l'incrément de gauche peut l'augmenter ; lorsqu'elle est trop grande, seul le décrément de droite peut la diminuer. Aucune paire n'est manquée car arr[left+1] >= arr[left] et arr[right-1] <= arr[right].

### Somme de deux avec ensemble de hachage - O(n) {#two-sum-with-hash-set-on}

```python
def find_pair(arr, k):
    visited = set()
    for elem in arr:
        if (k - elem) in visited:
            return True
        visited.add(elem)
    return False
```

### Vérification de sous-séquence - O(n+m) {#subsequence-check-onm}

```python
def is_subsequence(text, pattern):
    ptr_t, ptr_p = 0, 0
    while ptr_t < len(text) and ptr_p < len(pattern):
        if text[ptr_t] == pattern[ptr_p]:
            ptr_p += 1
        ptr_t += 1
    return ptr_p == len(pattern)
```

### Synthèse des compromis pour la somme de deux {#trade-off-summary-for-two-sum}

| Approche | Temps | Espace | Remarques |
|----------|------|-------|-----------|
| Force brute (toutes les paires) | O(n^2) | O(1) | Pas de prétraitement |
| Tri + deux pointeurs | O(n log n) | O(1) supplémentaire | Modifie/copie le tableau |
| Ensemble de hachage | O(n) | O(n) | Le plus rapide, utilise de la mémoire supplémentaire |

## Pièges à éviter {#gotchas}

- Le tri + deux pointeurs fait perdre les indices d'origine (si vous en avez besoin, stockez des paires (valeur, indice))
- L'approche par ensemble de hachage gère les doublons différemment : vérifiez si le complément a déjà été rencontré
- Pour les tableaux triés, les deux pointeurs sont préférés à l'ensemble de hachage (O(1) espace)
- La technique ne fonctionne pas sur un tableau non trié sans tri préalable (pour la variante convergente)

## Voir aussi {#see-also}

- [[searching-algorithms]] - la recherche dichotomique, autre technique sur tableau trié
- [[sorting-algorithms]] - le tri comme étape de prétraitement
- [[dp-sequence-problems]] - techniques plus avancées sur les séquences
