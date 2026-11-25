---
title: "Retour sur trace"
category: patterns
tags: [recursion, search, constraint-satisfaction, pruning]
level: 3
source_sha256: fdcff00b84d75430ab3e880b9f1ca814dd25259c847274309c37e554ad65c9dd
translation: machine
translated_at: '2026-10-24'
---
# Retour sur trace {#backtracking}

Exploration systématique de l'espace des solutions en construisant des candidats de manière incrémentale et en abandonnant (« retour sur trace ») les branches qui violent des contraintes. Combine un parcours en profondeur (DFS) avec de l'élagage.

## Points clés {#key-facts}

- Explore l'arbre des états en profondeur d'abord
- Élague les branches qui ne peuvent pas mener à des solutions valides (vérification de contraintes)
- Complexité temporelle souvent exponentielle, mais l'élagage réduit considérablement le temps d'exécution en pratique
- Base pour résoudre des problèmes NP-complets (somme de sous-ensembles, coloration de graphes, N-reines, Sudoku)
- Revient toujours au dernier point de décision et essaie l'option suivante
- Peut trouver une solution, toutes les solutions ou la solution optimale selon l'implémentation

## Modèle de base {#core-template}

```python
def backtrack(state, choices):
    if is_solution(state):
        process_solution(state)
        return

    for choice in choices:
        if is_valid(state, choice):
            make_choice(state, choice)
            backtrack(state, remaining_choices(choices, choice))
            undo_choice(state, choice)  # backtrack
```

## Motifs {#patterns}

### N-reines {#n-queens}

```python
def solve_n_queens(n):
    results = []

    def backtrack(row, cols, diag1, diag2, board):
        if row == n:
            results.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            board[row][col] = "Q"
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            backtrack(row + 1, cols, diag1, diag2, board)
            board[row][col] = "."
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    board = [["." for _ in range(n)] for _ in range(n)]
    backtrack(0, set(), set(), set(), board)
    return results
```

### Résolveur de Sudoku (approche par coloration de graphe) {#sudoku-solver-graph-coloring-approach}

```python
def solve_sudoku(grid):
    def get_candidates(r, c):
        used = set()
        used.update(grid[r])  # row
        used.update(grid[i][c] for i in range(9))  # col
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                used.add(grid[i][j])
        return [n for n in range(1, 10) if n not in used]

    def solve():
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    for num in get_candidates(r, c):
                        grid[r][c] = num
                        if solve():
                            return True
                        grid[r][c] = 0
                    return False
        return True

    solve()
    return grid
```

### Somme de sous-ensembles {#subset-sum}

```python
def subset_sum(nums, target):
    result = []

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:
                break  # prune (requires sorted input)
            current.append(nums[i])
            backtrack(i + 1, current, remaining - nums[i])
            current.pop()

    nums.sort()
    backtrack(0, [], target)
    return result
```

### Permutations {#permutations}

```python
def permutations(nums):
    result = []

    def backtrack(first):
        if first == len(nums):
            result.append(nums[:])
            return
        for i in range(first, len(nums)):
            nums[first], nums[i] = nums[i], nums[first]
            backtrack(first + 1)
            nums[first], nums[i] = nums[i], nums[first]

    backtrack(0)
    return result
```

## Complexité {#complexity}

| Problème | Temps | Espace |
|---------|------|-------|
| N-reines | O(N!) | O(N) |
| Sudoku | O(9^(cases vides)) | O(1) |
| Somme de sous-ensembles | O(2^N) | O(N) |
| Permutations | O(N!) | O(N) |
| Coloration de graphe | O(k^N) | O(N) |

## Techniques d'optimisation {#optimization-techniques}

- **Propagation de contraintes** : réduire le domaine avant la récursion (par exemple, la cohérence d'arc dans le Sudoku)
- **Ordre des variables** : choisir d'abord la variable la plus contrainte (heuristique MRV)
- **Ordre des valeurs** : essayer d'abord la valeur la moins contraignante
- **Brisure de symétrie** : éviter d'explorer des configurations équivalentes
- **Arrêt anticipé** : s'arrêter dès qu'une première solution valide est trouvée (si une seule est nécessaire)

## Pièges {#gotchas}

- **Problème :** oublier d'annuler les changements d'état après un appel récursif -> **Correctif :** toujours associer `make_choice` à `undo_choice`. Utiliser des structures de données immuables ou une annulation explicite.
- **Problème :** explosion exponentielle due à un élagage insuffisant -> **Correctif :** ajouter les vérifications de contraintes le plus tôt possible. Trier les tableaux d'entrée pour un élagage numérique.
- **Problème :** solutions dupliquées lorsque l'entrée contient des doublons -> **Correctif :** trier l'entrée et ignorer `nums[i] == nums[i-1]` au même niveau de récursion.

## Voir aussi {#see-also}

- [[dynamic-programming-fundamentals]] - lorsque les sous-problèmes se chevauchent, la programmation dynamique est plus efficace que le retour sur trace
- [[graph-coloring]] - application classique du retour sur trace
- [[graph-traversal-bfs-dfs]] - le retour sur trace est un DFS avec élagage
