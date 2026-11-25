---
title: "Technique de la fenêtre glissante"
category: patterns
tags: [arrays, strings, subarray, optimization]
level: 3
source_sha256: bd19d0700f6e597f90db856f2bacb4011f94726f2b82b2520e87417a09001298
translation: machine
translated_at: '2026-10-24'
---
# Technique de la fenêtre glissante {#sliding-window-technique}

Maintenir une fenêtre (sous-tableau ou sous-chaîne contigu) qui glisse sur l'entrée, en s'agrandissant et en se rétrécissant pour satisfaire des contraintes. Elle réduit la complexité de l'approche par force brute, O(N*K), à O(N).

## Points clés {#key-facts}

- Deux variantes : fenêtre de taille fixe et fenêtre de taille variable
- Utilise deux pointeurs (gauche, droit) qui délimitent les bornes de la fenêtre
- Le pointeur droit agrandit la fenêtre ; le pointeur gauche la rétrécit
- Évite les recalculs en mettant à jour incrémentalement l'état de la fenêtre
- Applicable lorsque le problème porte sur des sous-tableaux ou sous-chaînes contigus
- Temps : O(N) - chaque élément entre dans la fenêtre et en sort au plus une fois

## Fenêtre de taille fixe {#fixed-size-window}

```python
def max_sum_subarray(arr, k):
    """Maximum sum of subarray of size k."""
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

## Modèle de fenêtre de taille variable {#variable-size-window-template}

```python
def variable_window(arr):
    left = 0
    window_state = {}  # track what's in window
    result = 0

    for right in range(len(arr)):
        # Expand: add arr[right] to window state
        update_state(window_state, arr[right])

        # Shrink: while window violates constraint
        while not valid(window_state):
            remove_state(window_state, arr[left])
            left += 1

        # Update result
        result = max(result, right - left + 1)
    return result
```

## Motifs {#patterns}

### Plus longue sous-chaîne sans caractères répétés {#longest-substring-without-repeating-characters}

```python
def length_of_longest_substring(s):
    seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

### Plus petite sous-chaîne couvrante (Minimum Window Substring) {#minimum-window-substring}

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = 0
    start, end = 0, float('inf')

    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1

        while missing == 0:
            if right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1

    return s[start:end + 1] if end != float('inf') else ""
```

### Maximum de tous les sous-tableaux de taille K (deque monotone) {#maximum-of-all-subarrays-of-size-k-monotonic-deque}

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # stores indices, front = max
    result = []

    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Maintain decreasing order
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

### Sous-tableau dont la somme vaut K (somme préfixe + HashMap) {#subarray-sum-equals-k-prefix-sum-hashmap}

```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}

    for num in nums:
        prefix_sum += num
        count += seen.get(prefix_sum - k, 0)
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    return count
```

## Quand l'utiliser {#when-to-use}

| Indice | Technique |
|--------|-----------|
| « sous-tableau de taille k » | Fenêtre fixe |
| « plus long/plus court sous-tableau avec condition » | Fenêtre variable |
| « tous les sous-tableaux qui satisfont... » | Fenêtre variable + comptage |
| Éléments contigus | Candidat pour la fenêtre glissante |
| Éléments non contigus | PAS de fenêtre glissante |

## Pièges {#gotchas}

- **Problème :** utiliser la fenêtre glissante sur des problèmes nécessitant des éléments non contigus -> **Correction :** la fenêtre glissante ne fonctionne que pour les sous-tableaux et sous-chaînes contigus. Utiliser la programmation dynamique ou le double pointeur pour les éléments non contigus.
- **Problème :** mauvaise gestion de la condition de rétrécissement, provoquant une boucle infinie -> **Correction :** s'assurer que le pointeur gauche avance toujours dans la boucle de rétrécissement. L'état de la fenêtre doit être mis à jour de façon monotone.
- **Problème :** erreur de décalage d'un (off-by-one) dans la fenêtre fixe (calcul de la première fenêtre) -> **Correction :** initialiser la première fenêtre séparément, puis faire glisser la fenêtre à partir de l'indice k.

## Voir aussi {#see-also}

- [[two-pointer-technique]] - lié, mais les pointeurs peuvent se déplacer indépendamment
- [[searching-algorithms]] - la recherche binaire peut se combiner avec la fenêtre glissante
- [[complexity-analysis]] - la fenêtre glissante atteint O(N) amorti
