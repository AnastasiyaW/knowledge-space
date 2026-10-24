---
title: "Programmation dynamique et récursion"
category: concepts
tags: [algorithms, dynamic-programming, recursion, memoization]
level: 3
source_sha256: 479253ea74773e4ccd46f8dbb73ef3f5c374afed17481ada83ad290922b57bf0
translation: machine
translated_at: '2026-10-24'
---
# Programmation dynamique et récursion {#dynamic-programming-and-recursion}

Fondements de la récursion, mémoïsation (descendante), tabulation ascendante et reconnaissance des opportunités de programmation dynamique (PD). Technique centrale pour les problèmes d'optimisation présentant des sous-problèmes qui se chevauchent.

## Points clés {#key-facts}

- La récursion repose sur trois éléments : le cas de base, l'appel récursif (qui progresse vers le cas de base) et la propagation de la valeur de retour
- Fibonacci sans mémoïsation : O(2^N) ; avec mémoïsation : O(N)
- L'approche ascendante (itérative) est généralement plus économe en mémoire que l'approche descendante (récursion mémoïsée)
- La PD s'applique lorsqu'il existe des sous-problèmes qui se chevauchent : l'arbre des appels récursifs contient des branches dupliquées
- La mémoïsation échange de l'espace O(N) contre un gain de temps considérable
- Un dépassement de pile (stack overflow) survient lorsque la profondeur de récursion excède la mémoire de la pile d'appels

## Patrons {#patterns}

### Fondements de la récursion {#recursion-fundamentals}

```python
def factorial(n):
    return 1 if n == 1 else n * factorial(n - 1)
```

**Quand utiliser la récursion** : pour les problèmes dont la profondeur est inconnue ou variable (parcours du système de fichiers, opérations sur les arbres, structures fractales).

```ruby
# Directory traversal - unknown depth handled naturally
def find_directories(directory)
  Dir.foreach(directory) do |filename|
    if File.directory?("#{directory}/#{filename}") && filename != "." && filename != ".."
      puts "#{directory}/#{filename}"
      find_directories("#{directory}/#{filename}")
    end
  end
end
```

**Écrire une fonction récursive** : identifier l'action élémentaire, passer les paramètres supplémentaires nécessaires au suivi de l'état, et faire de la dernière ligne l'appel récursif.

```python
def double_array(array, index=0):
    if index >= len(array): return
    array[index] *= 2
    double_array(array, index + 1)
```

### Mémoïsation (descendante) {#memoization-top-down}

Mettre en cache les résultats des appels récursifs coûteux :

```python
def fib(n, memo={}):
    if n <= 1: return n
    if n not in memo:
        memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
```

### Tabulation ascendante {#bottom-up-tabulation}

Itérer des sous-problèmes les plus petits vers les plus grands, en stockant les résultats dans une table :

```python
def fib_bottom_up(n):
    if n <= 1: return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i-1] + table[i-2]
    return table[n]
```

### Méthode de résolution en programmation dynamique {#dp-problem-solving-framework}

1. **Identifier les sous-problèmes qui se chevauchent** : le même calcul est répété avec des paramètres différents
2. **Définir l'état** : dp[i] = « meilleure solution pour un problème de taille i »
3. **Relation de récurrence** : dp[i] = f(dp[i-1], dp[i-2], ...)
4. **Cas de base** : les plus petits sous-problèmes dont la réponse est connue
5. **Sens de construction** : ascendant (itératif) ou descendant (mémoïsé)

### Optimisation par prétraitement {#preprocessing-optimization}

Exemple : trouver le plus grand sous-carré d'une matrice dont toutes les cellules de bordure sont remplies.

Naïf : O(N^5). Avec prétraitement : O(N^3).

```python
# Preprocess consecutive filled cells in each direction
zeros_right = [[0]*n for _ in range(n)]
zeros_below = [[0]*n for _ in range(n)]
for i in range(n-1, -1, -1):
    for j in range(n-1, -1, -1):
        if matrix[i][j] == 1:
            zeros_right[i][j] = 1 + (zeros_right[i][j+1] if j+1 < n else 0)
            zeros_below[i][j] = 1 + (zeros_below[i+1][j] if i+1 < n else 0)
```

Vérifier désormais un candidat de bordure coûte O(1) par côté au lieu de O(N).

## Pièges {#gotchas}

- L'argument par défaut mutable en Python (`memo={}`) persiste entre les appels : pratique pour la mémoïsation, mais source de bogues fréquents dans d'autres contextes
- Limite de profondeur de récursion en Python : environ 1000 par défaut (`sys.setrecursionlimit()` permet de la modifier, mais il est préférable d'utiliser une approche itérative pour une récursion profonde)
- L'approche ascendante permet souvent une optimisation de l'espace (par exemple, Fibonacci n'a besoin que des deux valeurs précédentes, et non de la table complète)
- Tous les problèmes récursifs ne bénéficient pas de la PD : seuls ceux qui présentent des sous-problèmes qui se chevauchent sont concernés (pas les approches diviser pour régner comme le tri fusion)

## Voir aussi {#see-also}

- [[data-structures-fundamentals]] - récursion sur les tableaux, analyse en Big O
- [[trees-and-graphs]] - parcours récursif d'arbres, DFS
- [[algorithms/problem-patterns]] - fenêtre glissante, deux pointeurs, techniques d'entretien
