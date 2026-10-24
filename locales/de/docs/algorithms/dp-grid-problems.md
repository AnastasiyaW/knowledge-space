---
title: "DP: Gitter- und Kombinatorik-Probleme"
category: algorithms
tags: [algorithms, dynamic-programming, grid, matrix, partition, combinatorics]
level: 3
source_sha256: 33bc4326a61186df21d5dc1869b38ebfbd6af0e02df04828518f284fe8165e83
translation: machine
translated_at: '2026-10-24'
---
# DP: Gitter- und Kombinatorik-Probleme {#dp-grid-and-combinatorics-problems}

Gitterbasierte und kombinatorische DP-Probleme: Partition Problem, Maximal Square, Count Sorted Vowel Strings sowie das Zählen von Mustern. Diese kombinieren Teilmengenauswahl mit geometrischen oder zählenden Nebenbedingungen.

## Kernfakten {#key-facts}

- **Partition Problem**: Reduktion auf Subset Sum mit Ziel = Summe/2. Zeitaufwand O(n * Summe)
- **Maximal Square**: dp[i][j] = 1 + min(links, oben, diagonal). Zeitaufwand O(nm)
- **Count Sorted Vowel Strings**: Stars and Bars = C(n+4, 4), alternativ DP mit Präfixsummen
- Das Partition Problem ist NP-vollständig, besitzt aber eine pseudopolynomielle DP-Lösung

## Muster {#patterns}

### Partition Problem {#partition-problem}

Ein Array wird in zwei Teilmengen mit gleicher Summe aufgeteilt. Dies reduziert sich auf die Frage, ob eine Teilmenge die Summe total/2 ergibt.

```python
def partition(arr):
    s = sum(arr)
    if s % 2 == 1:
        return False  # odd sum impossible
    target = s // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in arr:
        for t in range(target, x - 1, -1):  # backward: use each item once
            dp[t] = dp[t] or dp[t - x]
    return dp[target]
```

**Warum rückwärts iterieren:** So wird sichergestellt, dass jedes Element höchstens einmal verwendet wird. Eine Vorwärtsiteration würde dasselbe Element mehrfach zulassen (unbeschränkte Variante).

### Maximal Square of Ones - O(nm) {#maximal-square-of-ones-onm}

Ermittelt die Fläche des größten quadratischen Teilmatrix, die nur 1en enthält.

**Rekurrenz:**
```yaml
if matrix[i][j] == 0: dp[i][j] = 0
else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```

Warum das Minimum aus drei Werten: Um ein Quadrat der Seitenlänge k an der Position (i,j) zu bilden, benötigt man Quadrate der Seitenlänge k-1 oben, links und diagonal. Der Engpass ist der kleinste Wert.

```python
def maximal_square(matrix):
    n, m = len(matrix), len(matrix[0])
    dp = [[0] * m for _ in range(n)]
    max_side = 0
    for j in range(m):
        dp[0][j] = matrix[0][j]
    for i in range(n):
        dp[i][0] = matrix[i][0]
    for i in range(1, n):
        for j in range(1, m):
            if matrix[i][j] == 0:
                dp[i][j] = 0
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
            max_side = max(max_side, dp[i][j])
    return max_side ** 2  # area
```

### Count Sorted Vowel Strings {#count-sorted-vowel-strings}

Zählt Zeichenketten der Länge n, die aus den Vokalen a, e, i, o, u in nicht fallender Reihenfolge bestehen.

```python
def count_vowel_strings(n):
    dp = [1] * 5  # length 1: one string per vowel
    for _ in range(1, n):
        new_dp = [0] * 5
        for v in range(5):
            new_dp[v] = sum(dp[:v + 1])  # can use same or earlier vowel
        dp = new_dp
    return sum(dp)
```

Mathematische Abkürzung: C(n+4, 4) (Stars and Bars).

### Allgemeine kombinatorische DP-Muster {#general-combinatorics-dp-patterns}

**Zählen von Pfaden in einem DAG:**
```python
dp[v] = sum(dp[u] for all u with edge u -> v)
```

**Zählen von Bitfolgen mit Nebenbedingungen:**
```python
dp[i][last] = count of valid strings of length i ending with `last`
```

**Zählen der Partitionen von n in k Teile:**
```python
dp[n][k] = dp[n-1][k-1] + dp[n-k][k]
```

## Stolperfallen {#gotchas}

- Partition: Die Gesamtsumme muss gerade sein, andernfalls sofort False zurückgeben
- Maximal Square: Basisfälle nicht vergessen (erste Zeile und erste Spalte werden direkt übernommen)
- Maximal Square gibt die Fläche (Seitenlänge^2) zurück, nicht die Seitenlänge
- Eine Speicheroptimierung auf O(m) mit der Zwei-Zeilen-Technik ist für beide Gitterprobleme möglich
- Die memoisierte Version des Partition-Problems verwendet den Zustand (Index, verbleibende_Summe) und nicht (Index, Summe1, Summe2)

## Siehe auch {#see-also}

- [[dp-optimization-problems]] - Subset Sum, Knapsack (eng verwandt mit Partition)
- [[dynamic-programming-fundamentals]] - DP-Ansatz und Top-down vs. Bottom-up
- [[dp-sequence-problems]] - zeichenkettenbasierte DP-Muster
