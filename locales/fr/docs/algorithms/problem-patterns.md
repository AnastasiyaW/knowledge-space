---
title: "Schémas de résolution de problèmes algorithmiques"
category: concepts
tags: [algorithms, interview, two-pointer, sliding-window, binary-search, problem-solving]
level: 3
source_sha256: 1056872047f7918ef93d8b5f52fa294c1ecc0f1d14792397af438fd3ae36f786
translation: machine
translated_at: '2026-10-24'
---
# Schémas de résolution de problèmes algorithmiques {#algorithm-problem-solving-patterns}

Approche méthodique des problèmes algorithmiques : le processus en 7 étapes utilisé en entretien, les schémas courants (deux pointeurs, fenêtre glissante), les techniques d'optimisation et les règles de choix des structures de données.

## Points clés {#key-facts}

- Optimisation BUD : identifier les Bottlenecks (goulots d'étranglement), le Unnecessary work (travail inutile) et le Duplicate work (travail dupliqué)
- Les tables de hachage résolvent tout problème du type « ai-je déjà vu cet élément ? » ou « recherche par clé » en O(1)
- Les tas résolvent les problèmes de k-ième plus grand/plus petit élément, de fusion de k listes triées et d'ordonnancement
- Les deux pointeurs s'appliquent aux tableaux triés ou à la recherche de paires
- La fenêtre glissante s'applique aux problèmes de sous-tableau ou sous-chaîne contigus
- La programmation dynamique ascendante (bottom-up) est généralement plus efficace que la mémoïsation récursive descendante (top-down)

## Schémas {#patterns}

### Le processus en 7 étapes {#the-7-step-process}

1. **Écouter attentivement** : identifier les contraintes particulières (données triées ? arbre ou graphe ? limites de mémoire ?)
2. **Dessiner un exemple** : spécifique, suffisamment grand, sans être un cas particulier
3. **Énoncer la solution par force brute** : même en O(N^3) ; cela montre la compréhension du problème
4. **Optimiser** : BUD : Bottlenecks, Unnecessary work, Duplicate work
5. **Dérouler** : vérifier l'algorithme sur l'exemple avant de coder
6. **Coder** : code modulaire et réel (pas du pseudo-code)
7. **Tester** : cas limites : entrée vide, élément unique, doublons, nombres négatifs

### Deux pointeurs {#two-pointer}

```python
left, right = 0, len(arr) - 1
while left < right:
    if condition: left += 1
    else: right -= 1
```

À utiliser pour : la recherche de paires dans des tableaux triés, la vérification de palindromes, les problèmes de partition.

### Fenêtre glissante {#sliding-window}

```python
start = 0
for end in range(len(s)):
    # expand window
    while window_invalid:
        # shrink from start
        start += 1
    best = max(best, end - start + 1)
```

À utiliser pour : la plus longue ou la plus courte sous-chaîne soumise à une contrainte, la somme maximale d'un sous-tableau de taille k.

### Modèle de recherche dichotomique {#binary-search-template}

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = lo + (hi - lo) // 2  # avoids integer overflow
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
```

À utiliser pour : les données triées, la réduction de l'espace de recherche, la recherche de bornes.

### Guide de choix des structures de données {#data-structure-selection-guide}

| Type de problème | Structure de données | Recherche |
|-------------|---------------|--------|
| « Ai-je déjà vu cet élément ? » | Table de hachage | O(1) moy. |
| k-ième plus grand/plus petit | Tas | O(log N) |
| Requêtes sur intervalles, prédécesseur | ABR / structure triée | O(log N) |
| Composantes connexes | Union-Find | O(alpha(N)) |
| Plus court chemin (non pondéré) | BFS avec file | O(V + E) |
| Plus court chemin (pondéré) | Dijkstra avec tas | O((V+E) log V) |

### Techniques d'optimisation {#optimization-techniques}

**Compromis espace/temps** :
- Tables de hachage pour une recherche en O(1) au lieu d'un parcours en O(N)
- Prétraitement ou tri pour permettre la recherche dichotomique
- Mémoïsation pour éviter le recalcul des sous-problèmes répétés

**Programmation dynamique** :
- Identifier les sous-problèmes qui se chevauchent
- Définir l'état : dp[i] = « meilleure solution pour un problème de taille i »
- Relation de récurrence : dp[i] = f(dp[i-1], dp[i-2], ...)

### Code propre pour les algorithmes {#clean-code-for-algorithms}

- **Noms significatifs** : `leftPointer` plutôt que `l`, `currentMax` plutôt que `cm`
- **Longueur des fonctions** : si elle ne tient pas à l'écran, la découper
- **Responsabilité unique** : séparer l'analyse, la logique et la sortie
- **Pas de nombres magiques** : `MAX_SIZE = 1000` plutôt que simplement `1000`
- **Les commentaires expliquent le POURQUOI** : pas le quoi (qui doit rester lisible), mais pourquoi cette approche

## Pièges courants {#gotchas}

- `lo + (hi - lo) // 2` évite le dépassement de capacité entier ; `(lo + hi) // 2` peut déborder dans les langages à entiers de taille fixe
- Erreurs de décalage (off-by-one) dans la recherche dichotomique : `lo <= hi` ou `lo < hi` dépend de l'inclusion des bornes
- La fenêtre glissante ne fonctionne que pour les problèmes où réduire la fenêtre par la gauche est toujours valide
- Les deux pointeurs sur des données non triées nécessitent d'abord un tri : intégrer le coût en O(N log N)
- Toujours traiter explicitement les cas limites : entrée vide, élément unique, doublons uniquement

## Voir aussi {#see-also}

- [[data-structures-fundamentals]] - tableaux, tables de hachage, analyse en notation de Landau (Big O)
- [[trees-and-graphs]] - algorithmes de parcours de graphes
- [[sorting-algorithms]] - le tri comme étape de prétraitement
- [[dynamic-programming]] - mémoïsation et tabulation
