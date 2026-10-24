---
title: "Algorithmes gloutons"
category: patterns
tags: [optimization, greedy-choice, scheduling, interval]
level: 3
source_sha256: 24492d655f241dbfed51069863f25b772913415e16deade54db850007e6d7a66
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes gloutons {#greedy-algorithms}

Construire des solutions de manière incrémentale en effectuant le choix localement optimal à chaque étape. Pas de retour en arrière : une fois un choix effectué, il n'est jamais reconsidéré.

## Points clés {#key-facts}

- Effectue le choix localement optimal à chaque point de décision
- Ne produit PAS toujours une solution globalement optimale
- Nécessite une preuve de correction (propriété du choix glouton + sous-structure optimale)
- Généralement en O(N log N) à cause de l'étape de tri
- Beaucoup plus rapide que la programmation dynamique ou le backtracking lorsqu'il est applicable
- Argument d'échange : prouver qu'échanger un choix non glouton avec un choix glouton ne dégrade jamais la solution

## Quand l'approche gloutonne fonctionne {#when-greedy-works}

Doit satisfaire les deux conditions suivantes :
1. **Propriété du choix glouton** : une solution globalement optimale peut être atteinte en effectuant des choix localement optimaux
2. **Sous-structure optimale** : une solution optimale contient des solutions optimales des sous-problèmes

## Problèmes classiques {#classic-problems}

### Sélection d'activités (ordonnancement d'intervalles) {#activity-selection-interval-scheduling}

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

### Sac à dos fractionnaire {#fractional-knapsack}

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

### Codage de Huffman {#huffman-coding}

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

### Rendu de monnaie (glouton - ne fonctionne que pour certaines coupures) {#coin-change-greedy-only-works-for-certain-denominations}

```python
def coin_change_greedy(coins, amount):
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1
```

### Ordonnancement de tâches avec échéances {#job-scheduling-with-deadlines}

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

## Comparaison glouton vs DP {#greedy-vs-dp-comparison}

| Aspect | Glouton | DP |
|--------|--------|-----|
| Choix | Un seul meilleur choix local | Tous les choix évalués |
| Sous-problèmes | Résolus une seule fois | Résolus et mémoïsés |
| Direction | Descendante uniquement | Descendante ou ascendante |
| Vitesse | Généralement O(N log N) | Généralement O(N*W) ou O(N^2) |
| Correction | Nécessite une preuve | Toujours correct pour une récurrence bien formée |

## Pièges à éviter {#gotchas}

- **Problème :** Le rendu de monnaie glouton échoue pour des coupures arbitraires (par ex. coins=[1,3,4], amount=6 : le glouton donne 4+1+1=3 pièces, l'optimal est 3+3=2 pièces) -> **Solution :** Utiliser la DP pour le rendu de monnaie général.
- **Problème :** Appliquer un glouton sans prouver sa correction -> **Solution :** Toujours vérifier la propriété du choix glouton. En cas de doute, utiliser la DP ou le backtracking.
- **Problème :** Le sac à dos 0/1 n'est PAS soluble par un glouton (seul le sac à dos fractionnaire l'est) -> **Solution :** Utiliser la DP pour le sac à dos 0/1.

## Voir aussi {#see-also}

- [[dynamic-programming-fundamentals]] - lorsque le glouton échoue, la DP est la solution de repli
- [[minimum-spanning-trees]] - Kruskal et Prim sont des algorithmes gloutons
- [[shortest-path-algorithms]] - Dijkstra est un algorithme glouton
