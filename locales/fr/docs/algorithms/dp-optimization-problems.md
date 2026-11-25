---
title: "DP : problèmes d'optimisation"
category: algorithms
tags: [algorithms, dynamic-programming, knapsack, coin-change, subset-sum, optimization]
level: 4
source_sha256: 106ea334824589cab11644e144758508cd4dd9e45c6a191d913ea72ca9aa0ef8
translation: machine
translated_at: '2026-10-24'
---
# DP : problèmes d'optimisation {#dp-optimization-problems}

Problèmes classiques d'optimisation par programmation dynamique : House Robber, Coin Change, 0-1 Knapsack, Subset Sum, Rod Cutting, Minimum Ticket Cost et Matrix Chain Multiplication. Ils partagent le même schéma : choisir d'inclure ou d'exclure des éléments ou des actions afin d'optimiser un objectif.

## Points clés {#key-facts}

- **House Robber** : O(n) en temps, O(1) en espace (seules les deux valeurs précédentes sont nécessaires)
- **Coin Change** : O(amount * |coins|) en temps, O(amount) en espace
- **0-1 Knapsack** : O(n*W) en temps, réductible à O(W) en espace avec une itération à rebours
- **Subset Sum** : O(n*target) en temps, O(target) en espace - variante booléenne du sac à dos
- **Matrix Chain** : O(n^3) en temps, O(n^2) en espace - DP sur intervalles
- Le sac à dos et la somme de sous-ensemble sont NP-complets mais admettent des solutions DP pseudo-polynomiales

## Schémas {#patterns}

### House Robber - O(n) en temps, O(1) en espace {#house-robber-on-time-o1-space}

Maximiser le total volé sans cambrioler deux maisons adjacentes. À chaque maison : la cambrioler (on saute la suivante) ou la passer.

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

Exemple : `[4, 8, 12, 1, 2, 10, 3, 6, 8]` -> dp : `[4, 8, 16, 16, 18, 26, 26, 32, 34]` -> réponse 34

### Coin Change (nombre minimal de pièces) {#coin-change-minimum-coins}

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

### 0-1 Knapsack {#0-1-knapsack}

n éléments avec poids/valeur, capacité W. Chaque élément est utilisé au plus une fois.

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

**Optimisé en espace à O(W)** en parcourant les poids à rebours :

```python
def knapsack_opt(weights, values, W):
    dp = [0] * (W + 1)
    for i in range(len(weights)):
        for w in range(W, weights[i] - 1, -1):  # backward!
            dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    return dp[W]
```

### Subset Sum {#subset-sum}

Peut-on sélectionner un sous-ensemble dont la somme vaut target ? Variante booléenne du sac à dos.

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

Étant donné une tige de longueur n et le prix de chaque longueur, maximiser le revenu.

```python
def rod_cutting(prices, n):
    dp = [0] * (n + 1)
    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            dp[length] = max(dp[length], prices[cut - 1] + dp[length - cut])
    return dp[n]
```

### Minimum Ticket Cost {#minimum-ticket-cost}

Jours de voyage et prix des titres (passes 1 jour, 7 jours, 30 jours).

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

Parenthésage optimal pour minimiser le coût des multiplications.

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

Partir de n'importe quelle case de la colonne 0, se déplacer vers les cases adjacentes de la colonne suivante. Maximiser l'or récolté.

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

## Pièges {#gotchas}

- **L'itération à rebours** dans subset sum/knapsack empêche la réutilisation d'un élément (contrainte 0-1). Une itération directe correspond au sac à dos non borné
- Coin change renvoie -1 si le montant est inatteignable (tester l'infini)
- Matrix chain : la DP sur intervalles remplit par longueur d'intervalle croissante, et non ligne par ligne
- Rod cutting est non borné (une même longueur peut être coupée plusieurs fois) - l'itération directe est correcte ici
- House robber en O(1) d'espace : seuls `before_prev` et `prev` sont nécessaires, pas le tableau dp complet

## Voir aussi {#see-also}

- [[dynamic-programming-fundamentals]] - concepts et approche de la DP
- [[dp-grid-problems]] - problèmes de DP sur grille
- [[dp-sequence-problems]] - DP sur chaînes et séquences
- [[complexity-classes]] - le sac à dos et la somme de sous-ensemble sont NP-complets avec des solutions pseudo-polynomiales
