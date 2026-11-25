---
title: "DP: Optimierungsprobleme"
category: algorithms
tags: [algorithms, dynamic-programming, knapsack, coin-change, subset-sum, optimization]
level: 4
source_sha256: 106ea334824589cab11644e144758508cd4dd9e45c6a191d913ea72ca9aa0ef8
translation: machine
translated_at: '2026-10-24'
---
# DP: Optimierungsprobleme {#dp-optimization-problems}

Klassische DP-Optimierungsprobleme: House Robber, Coin Change, 0-1-Knapsack, Subset Sum, Rod Cutting, Minimum Ticket Cost und Matrix Chain Multiplication. Sie teilen das Muster, Elemente bzw. Aktionen einzuschließen oder auszuschließen, um eine Zielfunktion zu optimieren.

## Key Facts {#key-facts}

- **House Robber**: O(n) Zeit, O(1) Speicher (es werden nur die beiden vorherigen Werte benötigt)
- **Coin Change**: O(amount * |coins|) Zeit, O(amount) Speicher
- **0-1-Knapsack**: O(n*W) Zeit, durch Rückwärtsiteration auf O(W) Speicher reduzierbar
- **Subset Sum**: O(n*target) Zeit, O(target) Speicher - boolesche Variante des Knapsack
- **Matrix Chain**: O(n^3) Zeit, O(n^2) Speicher - Intervall-DP
- Knapsack und Subset Sum sind NP-vollständig, besitzen aber pseudopolynomielle DP-Lösungen

## Patterns {#patterns}

### House Robber - O(n) Zeit, O(1) Speicher {#house-robber-on-time-o1-space}

Maximale Gesamtsumme ohne Ausrauben benachbarter Häuser. An jedem Haus: ausrauben (nächstes überspringen) oder auslassen.

```python
def rob(arr):
    n = len(arr)
    if n == 1:
        return arr[0]
    before_prev = arr[0]
    prev = max(arr[0], arr[1])
    for i in range(2, n):
        curr = max(prev, arr[i] + before_prev)
        before_prev = prev
        prev = curr
    return prev
```

Beispiel: `[4, 8, 12, 1, 2, 10, 3, 6, 8]` -> dp: `[4, 8, 16, 16, 18, 26, 26, 32, 34]` -> Ergebnis 34

### Coin Change (Minimale Münzanzahl) {#coin-change-minimum-coins}

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for amt in range(1, amount + 1):
        for coin in coins:
            if coin <= amt and dp[amt - coin] + 1 < dp[amt]:
                dp[amt] = dp[amt - coin] + 1
    return dp[amount] if dp[amount] != float('inf') else -1
```

### 0-1-Knapsack {#0-1-knapsack}

n Elemente mit Gewicht/Wert, Kapazität W. Jedes Element wird höchstens einmal verwendet.

```python
def knapsack(weights, values, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]  # don't take
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               values[i - 1] + dp[i - 1][w - weights[i - 1]])
    return dp[n][W]
```

**Auf O(W) Speicher optimiert** durch rückwärts laufende Iteration über die Gewichte:

```python
def knapsack_opt(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):  # backward!
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]
```

### Subset Sum {#subset-sum}

Lässt sich eine Teilmenge wählen, deren Summe dem Zielwert entspricht? Boolesche Variante des Knapsack.

```python
def subset_sum(arr, target):
    dp = [False] * (target + 1)
    dp[0] = True
    for x in arr:
        for s in range(target, x - 1, -1):  # backward to use each item once
            dp[s] = dp[s] or dp[s - x]
    return dp[target]
```

### Rod Cutting {#rod-cutting}

Gegeben ein Stab der Länge n und ein Preis für jede Länge: Erlös maximieren.

```python
def rod_cutting(prices, n):
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            dp[length] = max(dp[length], prices[cut - 1] + dp[length - cut])
    return dp[n]
```

### Minimum Ticket Cost {#minimum-ticket-cost}

Reisetage und Ticketpreise (1-Tages-, 7-Tages- und 30-Tages-Pass).

```python
def min_cost_tickets(days, costs):
    day_set = set(days)
    max_day = max(days)
    dp = [0] * (max_day + 1)
    for d in range(1, max_day + 1):
        if d not in day_set:
            dp[d] = dp[d - 1]
        else:
            dp[d] = min(
                dp[d - 1] + costs[0],
                dp[max(0, d - 7)] + costs[1],
                dp[max(0, d - 30)] + costs[2]
            )
    return dp[max_day]
```

### Matrix Chain Multiplication - O(n^3) {#matrix-chain-multiplication-on3}

Optimale Klammerung zur Minimierung der Multiplikationskosten.

```python
def matrix_chain(dims):
    n = len(dims)
    cost = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float('inf')
            for k in range(i, j):
                c = (cost[i][k] + cost[k + 1][j] +
                     dims[i][0] * dims[k][1] * dims[j][1])
                cost[i][j] = min(cost[i][j], c)
    return cost[0][n - 1]
```

### Gold Mine - O(n*m) {#gold-mine-onm}

Start in einer beliebigen Zelle der Spalte 0, Übergang zu benachbarten Zellen der nächsten Spalte. Gold maximieren.

```python
def gold(mine):
    n, m = len(mine), len(mine[0])
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        dp[i][m - 1] = mine[i][m - 1]
    for j in range(m - 2, -1, -1):
        for i in range(n):
            best = dp[i][j + 1]
            if i > 0:
                best = max(best, dp[i - 1][j + 1])
            if i < n - 1:
                best = max(best, dp[i + 1][j + 1])
            dp[i][j] = mine[i][j] + best
    return max(dp[i][0] for i in range(n))
```

## Gotchas {#gotchas}

- **Rückwärtsiteration** bei Subset Sum/Knapsack verhindert die Wiederverwendung von Elementen (0-1-Bedingung). Vorwärtsiteration ergibt den unbeschränkten Knapsack
- Coin Change gibt -1 zurück, wenn der Betrag nicht erreichbar ist (auf Unendlich prüfen)
- Matrix Chain: Die Intervall-DP füllt nach wachsender Intervalllänge, nicht zeilenweise
- Rod Cutting ist unbeschränkt (dieselbe Länge kann mehrfach geschnitten werden) - hier ist Vorwärtsiteration korrekt
- House Robber mit O(1) Speicher: benötigt nur `before_prev` und `prev`, nicht das vollständige dp-Array

## Siehe auch {#see-also}

- [[dynamic-programming-fundamentals]] - DP-Konzepte und Vorgehensweise
- [[dp-grid-problems]] - DP-Probleme auf Gittern
- [[dp-sequence-problems]] - DP für Zeichenketten und Sequenzen
- [[complexity-classes]] - Knapsack und Subset Sum sind NP-vollständig mit pseudopolynomiellen Lösungen
