---
title: "Grundlagen der dynamischen Programmierung"
category: concepts
tags: [algorithms, dynamic-programming, memoization, tabulation, optimization]
level: 2
source_sha256: 169db07a934f0bb1a9a7d117b19cf6208b89fb1970b793f8019ad7732815a7a8
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen der dynamischen Programmierung {#dynamic-programming-fundamentals}

Dynamische Programmierung (DP) löst Probleme, indem sie diese in überlappende Teilprobleme zerlegt und Ergebnisse speichert, um erneute Berechnungen zu vermeiden. Sie ist anwendbar, wenn ein Problem optimale Teilstruktur (optimale Lösung aus optimalen Teillösungen) und überlappende Teilprobleme (dieselben Teilprobleme werden in der naiven Rekursion wiederholt gelöst) besitzt.

## Wichtige Fakten {#key-facts}

- **Top-down (Memoization)**: Rekursiv + Cache, berechnet nur benötigte Teilprobleme
- **Bottom-up (Tabulation)**: Iterativ, füllt die Tabelle ausgehend von den Basisfällen, kein Overhead durch Rekursion
- DP reduziert exponentielle Rekursion durch Caching auf polynomiell – typischerweise von O(2^n) auf O(n*m) oder O(n^2)
- Zuerst mit Memoization die Logik validieren, dann für Performance in Tabulation umwandeln
- Speicheroptimierung ist oft möglich, indem nur die letzten 1–2 Zeilen bzw. Werte aufbewahrt werden

## Top-Down vs. Bottom-Up {#top-down-vs-bottom-up}

| | Top-Down (Memoization) | Bottom-Up (Tabulation) |
|-|----------------------|----------------------|
| Implementierung | Rekursiv – ergibt sich natürlich aus der Rekursionsgleichung | Iterativ – erfordert die Bestimmung der Füllreihenfolge |
| Berechnete Teilprobleme | Nur die benötigten | Alle Teilprobleme |
| Overhead | Call Stack, Dictionary-Zugriffe | Array-Zugriffe (schneller) |
| Stack Overflow | Risiko bei tiefer Rekursion | Kein Risiko |
| Speicheroptimierung | Schwieriger | Einfacher (zeilenweise) |

## Muster {#patterns}

### Identifizieren der DP-Rekursion {#identifying-dp-recurrence}

1. Definieren, was `dp[state]` repräsentiert (präzise festlegen, was es bedeutet)
2. Basisfälle formulieren
3. Rekursion aufschreiben: `dp[state] = f(dp[smaller_states])`
4. Durchlaufreihenfolge bestimmen, sodass Abhängigkeiten vor der Verwendung aufgelöst sind
5. Zielzustand zurückgeben

### Laufendes Beispiel: Minimaler Kostenpfad in einer Matrix {#running-example-min-cost-path-in-matrix}

Von oben links nach unten rechts ausschließlich nach rechts oder unten gehen und die Gesamtkosten minimieren.

**Naive Rekursion – O(2^(n+m)):**

```python
def min_cost(matrix, i=0, j=0):
    n, m = len(matrix), len(matrix[0])
    if i == n or j == m:
        return float('inf')
    if i == n - 1 and j == m - 1:
        return matrix[i][j]
    return matrix[i][j] + min(min_cost(matrix, i + 1, j),
                               min_cost(matrix, i, j + 1))
```

**Top-Down (Memoization) – O(n*m):**

```python
def min_cost(matrix, i=0, j=0, memo=None):
    if memo is None:
        memo = {}
    if (i, j) in memo:
        return memo[(i, j)]
    n, m = len(matrix), len(matrix[0])
    if i == n or j == m:
        return float('inf')
    if i == n - 1 and j == m - 1:
        return matrix[i][j]
    memo[(i, j)] = matrix[i][j] + min(
        min_cost(matrix, i + 1, j, memo),
        min_cost(matrix, i, j + 1, memo)
    )
    return memo[(i, j)]
```

**Bottom-Up (Tabulation) – O(n*m):**

```python
def min_cost(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * m for _ in range(n)]
    dp[n - 1][m - 1] = matrix[n - 1][m - 1]

    for j in range(m - 2, -1, -1):  # last row
        dp[n - 1][j] = matrix[n - 1][j] + dp[n - 1][j + 1]
    for i in range(n - 2, -1, -1):  # last column
        dp[i][m - 1] = matrix[i][m - 1] + dp[i + 1][m - 1]
    for i in range(n - 2, -1, -1):  # rest
        for j in range(m - 2, -1, -1):
            dp[i][j] = matrix[i][j] + min(dp[i + 1][j], dp[i][j + 1])

    return dp[0][0]
```

### Zählen von Pfaden im Gitter {#counting-paths-in-grid}

```python
def count_paths(n, m):
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        dp[i][0] = 1
    for j in range(m):
        dp[0][j] = 1
    for i in range(1, n):
        for j in range(1, m):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[n - 1][m - 1]
```

Mathematische Formel: C(n+m-2, n-1) – wähle aus, welche Schritte nach unten gehen.

## Stolperfallen {#gotchas}

- Greedy-Verfahren scheitern oft dort, wo DP erfolgreich ist – immer zum günstigsten Nachbarn zu gehen kann das globale Optimum verfehlen
- Top-down mit Python-Dictionaries kann bei großen Zustandsräumen langsam sein – Tabulation mit Arrays ist schneller
- Das Python-Rekursionslimit (Standard 1000) kann Top-down-DP bei großen Eingaben abstürzen lassen – `sys.setrecursionlimit` verwenden oder auf Bottom-up umstellen
- Falle bei veränderlichen Standardargumenten: `None` als Standardwert verwenden und innerhalb der Funktion initialisieren
- Speicheroptimierung (nur die letzte Zeile behalten) verhindert die Rekonstruktion des tatsächlichen Lösungspfads

## Siehe auch {#see-also}

- [[dp-sequence-problems]] – LCS, Edit Distance, LIS, Word Break
- [[dp-optimization-problems]] – Knapsack, Coin Change, House Robber
- [[dp-grid-problems]] – Matrix Path, Maximal Square, Gold Mine
- [[complexity-analysis]] – Verständnis der Komplexitätsreduktion durch DP
