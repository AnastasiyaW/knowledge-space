---
title: "Greedy-Algorithmen"
category: patterns
tags: [optimization, greedy-choice, scheduling, interval]
level: 3
source_sha256: 24492d655f241dbfed51069863f25b772913415e16deade54db850007e6d7a66
translation: machine
translated_at: '2026-10-24'
---
# Greedy-Algorithmen {#greedy-algorithms}

Lösungen werden schrittweise aufgebaut, indem an jedem Schritt die lokal optimale Wahl getroffen wird. Es gibt kein Backtracking – einmal getroffene Entscheidungen werden nie erneut überprüft.

## Wichtige Fakten {#key-facts}

- Trifft an jedem Entscheidungspunkt die lokal optimale Wahl
- Liefert NICHT immer eine global optimale Lösung
- Erfordert einen Korrektheitsbeweis (Greedy-Choice-Eigenschaft + optimale Teilstruktur)
- Typischerweise O(N log N) aufgrund des Sortierschritts
- Deutlich schneller als DP oder Backtracking, wo anwendbar
- Austauschargument: Man beweist, dass das Ersetzen einer nicht-gierigen Wahl durch eine gierige Wahl die Lösung nie verschlechtert

## Wann Greedy funktioniert {#when-greedy-works}

Beide Bedingungen müssen erfüllt sein:
1. **Greedy-Choice-Eigenschaft**: Eine global optimale Lösung kann durch lokal optimale Entscheidungen erreicht werden
2. **Optimale Teilstruktur**: Eine optimale Lösung enthält optimale Lösungen der Teilprobleme

## Klassische Probleme {#classic-problems}

### Activity Selection (Intervall-Scheduling) {#activity-selection-interval-scheduling}

```python
def max_activities(intervals):
    # Sort by end time
    intervals.sort(key=lambda x: x[1])
    count = 1
    last_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start >= last_end:
            count += 1
            last_end = end
    return count
```

### Fractional Knapsack {#fractional-knapsack}

```python
def fractional_knapsack(capacity, items):
    # items: [(value, weight), ...]
    # Sort by value/weight ratio descending
    items.sort(key=lambda x: x[0] / x[1], reverse=True)
    total_value = 0

    for value, weight in items:
        if capacity >= weight:
            total_value += value
            capacity -= weight
        else:
            total_value += value * (capacity / weight)
            break
    return total_value
```

### Huffman-Codierung {#huffman-coding}

```python
import heapq

def huffman(frequencies):
    heap = [[freq, [char, ""]] for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heap[0][1:], key=lambda p: (len(p[1]), p))
```

### Münzwechsel (Greedy – funktioniert nur für bestimmte Stückelungen) {#coin-change-greedy-only-works-for-certain-denominations}

```python
def coin_change_greedy(coins, amount):
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1
```

### Job-Scheduling mit Fristen {#job-scheduling-with-deadlines}

```python
def job_scheduling(jobs):
    # jobs: [(profit, deadline), ...]
    jobs.sort(key=lambda x: x[0], reverse=True)
    max_deadline = max(j[1] for j in jobs)
    slots = [False] * (max_deadline + 1)
    total_profit = 0

    for profit, deadline in jobs:
        for t in range(deadline, 0, -1):
            if not slots[t]:
                slots[t] = True
                total_profit += profit
                break
    return total_profit
```

## Greedy vs. DP im Vergleich {#greedy-vs-dp-comparison}

| Aspekt | Greedy | DP |
|--------|--------|-----|
| Entscheidungen | Eine beste lokale Wahl | Alle Entscheidungen werden bewertet |
| Teilprobleme | Einmal gelöst | Gelöst und memoisiert |
| Richtung | Nur Top-down | Top-down oder Bottom-up |
| Geschwindigkeit | Meist O(N log N) | Meist O(N*W) oder O(N^2) |
| Korrektheit | Erfordert Beweis | Immer korrekt bei wohldefinierter Rekurrenz |

## Fallstricke {#gotchas}

- **Problem:** Greedy-Münzwechsel scheitert bei beliebigen Stückelungen (z. B. coins=[1,3,4], amount=6: Greedy liefert 4+1+1=3 Münzen, optimal sind 3+3=2 Münzen) -> **Lösung:** Für allgemeinen Münzwechsel DP verwenden.
- **Problem:** Greedy ohne Korrektheitsbeweis anwenden -> **Lösung:** Greedy-Choice-Eigenschaft immer prüfen. Im Zweifel DP oder Backtracking verwenden.
- **Problem:** 0/1-Knapsack ist NICHT mit Greedy lösbar (nur Fractional Knapsack) -> **Lösung:** Für 0/1-Knapsack DP verwenden.

## Siehe auch {#see-also}

- [[dynamic-programming-fundamentals]] – wenn Greedy scheitert, ist DP die Alternative
- [[minimum-spanning-trees]] – Kruskal und Prim sind Greedy-Algorithmen
- [[shortest-path-algorithms]] – Dijkstra ist ein Greedy-Algorithmus
