---
title: "Algorithmes de recherche"
category: algorithms
tags: [algorithms, search, binary-search, linear-search, kmp, string-matching]
level: 3
source_sha256: f3fd73b1a796c94c882dd19c8d02ac68a7bb5f78cf718c3daa9ecf1a4184e989
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes de recherche {#searching-algorithms}

Couvre la recherche linéaire, la recherche binaire et la recherche de chaînes KMP. La recherche linéaire est en O(n) pour des données non triées, la recherche binaire est en O(log n) pour des données triées, et KMP réalise une recherche de motif dans une chaîne en O(n+m) en évitant les comparaisons redondantes.

## Points clés {#key-facts}

- **Recherche linéaire** : O(n) en temps, O(1) en espace - fonctionne sur n'importe quelles données, avec n'importe quel prédicat
- **Recherche binaire** : O(log n) en temps, O(1) en espace - nécessite un tableau trié
- **KMP** : O(n+m) en temps, O(m) en espace - recherche de motif sans retour en arrière dans le texte
- Pour une seule requête sur des données non triées, la recherche linéaire est plus rapide que trier puis chercher par dichotomie (O(n) contre O(n log n))
- Pour de nombreuses requêtes sur les mêmes données, trier une fois en O(n log n) puis effectuer une recherche binaire en O(log n) pour chaque requête

## Motifs {#patterns}

### Recherche linéaire {#linear-search}

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

Fonctionne avec n'importe quel prédicat, et pas seulement l'égalité :

```python
# First element greater than num
def search_greater(arr, num):
    for i in range(len(arr)):
        if arr[i] > num:
            return i
    return -1

# String containing character
def search_contains(arr, ch):
    for i in range(len(arr)):
        if ch in arr[i]:
            return i
    return -1
```

### Recherche binaire {#binary-search}

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Pourquoi O(log n) : en partant de n éléments, après k itérations, il en reste au plus ceil(n/2^k). On s'arrête lorsqu'il reste 1 élément : n/2^k = 1 -> k = log2(n).

### Quand choisir {#when-to-choose}

```python
def search(arr, target):
    if is_sorted(arr):
        return binary_search(arr, target)
    else:
        return linear_search(arr, target)
```

### Recherche de chaîne KMP - O(n+m) {#kmp-string-search-onm}

La recherche naïve de chaîne est en O(n*m) car elle recommence la recherche du motif depuis le début à chaque discordance. KMP utilise un tableau LPS (Longest Proper Prefix which is also Suffix, soit le plus long préfixe propre qui est aussi suffixe) pour sauter les caractères déjà reconnus.

**Construction du tableau LPS - O(m) :**

```python
def get_lps_arr(pattern):
    lps = [0] * len(pattern)
    length = 0  # length of previous longest prefix-suffix
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]  # fall back without moving i
        else:
            lps[i] = 0
            i += 1
    return lps
```

Exemple : `"aabaaab"` -> `[0, 1, 0, 1, 2, 2, 3]`

**Recherche KMP - O(n) :**

```python
def kmp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    if m == n:
        return 0 if text == pattern else -1
    lps = get_lps_arr(pattern)
    i, j = 0, 0  # text pointer, pattern pointer
    while i < n and j < m:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j > 0:
            j = lps[j - 1]  # don't advance i
        else:
            i += 1
    return i - j if j == m else -1
```

**Pourquoi ça fonctionne :** `i` ne recule jamais. En cas de discordance à la position j, `lps[j-1]` indique combien de caractères sont déjà reconnus (préfixe = suffixe de ce qui a été lu). Total : O(n) pour la recherche + O(m) pour le LPS = O(n+m).

## Pièges {#gotchas}

- La recherche binaire exige une entrée triée : l'appliquer à des données non triées donne des résultats faux
- Le calcul `mid = (left + right) // 2` peut provoquer un dépassement de capacité dans les langages à entiers de taille fixe ; utiliser plutôt `mid = left + (right - left) // 2` (pas de problème en Python)
- Dans la construction du LPS de KMP : en cas de discordance, revenir à `lps[length-1]`, et NON réinitialiser à 0
- Pour une recherche unique sur des données non triées, trier d'abord (O(n log n)) est inutile par rapport à la recherche linéaire (O(n))
- Pire cas de la recherche naïve de chaîne : texte = "aaa...a", motif = "aaa...ab" -> O(n*m)

## Voir aussi {#see-also}

- [[sorting-algorithms]] - la recherche binaire exige une entrée triée
- [[two-pointer-technique]] - motifs de recherche sur des tableaux triés
- [[complexity-analysis]] - comprendre la dérivation de O(log n)
