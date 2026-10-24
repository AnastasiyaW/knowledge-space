---
title: "Backtracking"
category: patterns
tags: [recursion, search, constraint-satisfaction, pruning]
level: 3
source_sha256: fdcff00b84d75430ab3e880b9f1ca814dd25259c847274309c37e554ad65c9dd
translation: machine
translated_at: '2026-10-24'
---
Hmm, I need to produce the German translation. Let me write it out.

---
title: Backtracking
category: patterns
tags: [recursion, search, constraint-satisfaction, pruning]
---

Wait, the title and description values should be translated. The title "Backtracking" is the same in German (established term). The YAML has no description field, so copy unchanged.

# Backtracking {#backtracking}

Systematische Erkundung des Lösungsraums, indem Kandidaten schrittweise aufgebaut und Zweige, die Nebenbedingungen verletzen, verworfen werden ("Backtracking"). Kombiniert DFS mit Pruning.

## Wichtige Fakten {#key-facts}

- Durchsucht den Zustandsraumbaum in Tiefensuche
- Schneidet Zweige ab, die nicht zu gültigen Lösungen führen können (Constraint-Prüfung)
- Die Zeitkomplexität ist oft exponentiell, doch Pruning reduziert die praktische Laufzeit deutlich
- Grundlage für die Lösung NP-vollständiger Probleme (Teilsummenproblem, Graphenfärbung, N-Damen, Sudoku)
- Kehrt stets zum letzten Entscheidungspunkt zurück und probiert die nächste Option
- Kann je nach Implementierung eine Lösung, alle Lösungen oder die optimale Lösung finden

## Grundschema {#core-template}

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

## Muster {#patterns}

### N-Damen {#n-queens}

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

### Sudoku-Löser (Graphenfärbungs-Ansatz) {#sudoku-solver-graph-coloring-approach}

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

### Teilsummenproblem {#subset-sum}

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

### Permutationen {#permutations}

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

## Komplexität {#complexity}

| Problem | Zeit | Speicher |
|---------|------|----------|
| N-Damen | O(N!) | O(N) |
| Sudoku | O(9^(leere Zellen)) | O(1) |
| Teilsummenproblem | O(2^N) | O(N) |
| Permutationen | O(N!) | O(N) |
| Graphenfärbung | O(k^N) | O(N) |

## Optimierungstechniken {#optimization-techniques}

- **Constraint-Propagation**: Domäne vor dem Rekursionsaufruf verkleinern (z. B. Arc-Konsistenz beim Sudoku)
- **Variablenreihenfolge**: die am stärksten eingeschränkte Variable zuerst wählen (MRV-Heuristik)
- **Wertereihenfolge**: zuerst den am wenigsten einschränkenden Wert probieren
- **Symmetriebrechung**: Vermeiden, äquivalente Konfigurationen zu untersuchen
- **Frühzeitiger Abbruch**: stoppen, sobald die erste gültige Lösung gefunden wurde (falls nur eine benötigt wird)

## Fallstricke {#gotchas}

- **Problem:** Zustandsänderungen nach dem rekursiven Aufruf nicht rückgängig machen -> **Lösung:** `make_choice` immer mit `undo_choice` paaren. Unveränderliche Datenstrukturen oder explizites Zurücksetzen verwenden.
- **Problem:** Exponentielles Wachstum durch unzureichendes Pruning -> **Lösung:** Constraint-Prüfungen so früh wie möglich einbauen. Eingabearrays für numerisches Pruning sortieren.
- **Problem:** Doppelte Lösungen, wenn die Eingabe Duplikate enthält -> **Lösung:** Eingabe sortieren und auf derselben Rekursionsebene `nums[i] == nums[i-1]` überspringen.

## Siehe auch {#see-also}

- [[dynamic-programming-fundamentals]] - wenn sich Teilprobleme überlappen, ist DP dem Backtracking überlegen
- [[graph-coloring]] - klassische Anwendung des Backtrackings
- [[graph-traversal-bfs-dfs]] - Backtracking ist DFS mit Pruning
