---
title: "Manipulation de bits"
category: concepts
tags: [bitwise, binary, optimization, low-level]
level: 3
source_sha256: a96aeb7feaff3a13ac2fbbacefc0a0a48dc2f81738dd2c514337400349d54b95
translation: machine
translated_at: '2026-10-24'
---
# Manipulation de bits {#bit-manipulation}

Opérations sur les bits individuels des entiers. Essentielles pour l'optimisation, la cryptographie, les réseaux et la programmation compétitive.

## Points clés {#key-facts}

- ET bit à bit (`&`) : les deux bits à 1 -> 1
- OU bit à bit (`|`) : au moins un bit à 1 -> 1
- OU exclusif bit à bit (`^`) : bits différents -> 1
- NON bit à bit (`~`) : inverse tous les bits (complément à deux : `~x = -x - 1`)
- Décalage à gauche (`<<`) : multiplication par 2^n
- Décalage à droite (`>>`) : division par 2^n (le décalage arithmétique conserve le signe)
- Les entiers Python ont une précision arbitraire : pas de dépassement de capacité

## Astuces essentielles {#essential-tricks}

```python
# Check if n-th bit is set
(x >> n) & 1

# Set n-th bit
x | (1 << n)

# Clear n-th bit
x & ~(1 << n)

# Toggle n-th bit
x ^ (1 << n)

# Check if power of 2
x > 0 and (x & (x - 1)) == 0

# Count set bits (Brian Kernighan)
def count_bits(n):
    count = 0
    while n:
        n &= n - 1  # clears lowest set bit
        count += 1
    return count

# Lowest set bit
x & (-x)

# Clear lowest set bit
x & (x - 1)

# Check if even/odd
x & 1  # 0 = even, 1 = odd

# Swap without temp
a ^= b; b ^= a; a ^= b

# Two's complement negation
-x == ~x + 1
```

## Motifs {#patterns}

### Nombre unique (XOR) {#single-number-xor}

```python
def single_number(nums):
    """Every element appears twice except one. Find it."""
    result = 0
    for n in nums:
        result ^= n
    return result
# XOR properties: a ^ a = 0, a ^ 0 = a, commutative + associative
```

### Nombre manquant {#missing-number}

```python
def missing_number(nums):
    """Array [0..n] with one missing."""
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)

# XOR approach
def missing_number_xor(nums):
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```

### Ensemble des parties via masque de bits {#power-set-via-bitmask}

```python
def subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    return result
```

### Comptage des bits pour tous les nombres de 0 à N {#counting-bits-for-all-numbers-0n}

```python
def count_bits_array(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### Programmation dynamique par masque de bits (voyageur de commerce) {#bitmask-dp-traveling-salesman}

```python
def tsp(dist):
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # start at city 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])

    full = (1 << n) - 1
    return min(dp[full][u] + dist[u][0] for u in range(n))
```

## Motifs binaires courants {#common-bit-patterns}

| Opération | Expression | Résultat |
|-----------|-----------|--------|
| Est une puissance de 2 | `n & (n-1) == 0` | True si puissance de 2 |
| Bit à 1 le plus à droite | `n & (-n)` | Isole le plus petit 1 |
| Éteindre le 1 le plus à droite | `n & (n-1)` | Efface le plus petit 1 |
| Suite de k bits à 1 | `(1 << k) - 1` | Binaire : 0..01..1 |
| Le n-ième bit est-il à 1 | `(x >> n) & 1` | 0 ou 1 |

## Pièges {#gotchas}

- **Problème :** En Python, `~x` renvoie `-(x+1)` à cause des entiers à précision arbitraire (sans largeur fixe) -> **Solution :** Pour un comportement à largeur fixe, appliquer un masque `~x & 0xFFFFFFFF` pour 32 bits.
- **Problème :** Le décalage à droite signé étend le bit de signe, le décalage non signé ne le fait pas -> **Solution :** Python ne dispose que du décalage à droite arithmétique (signé). Pour un comportement non signé sur des nombres négatifs, convertir d'abord en non signé : `(x & 0xFFFFFFFF) >> n`.
- **Problème :** Explosion mémoire de la programmation dynamique par masque de bits pour N grand -> **Solution :** Cette approche n'est praticable que pour N <= 20-25 (2^N états). Pour N plus grand, utiliser d'autres approches.

## Voir aussi {#see-also}

- [[complexity-analysis]] - la manipulation de bits permet souvent d'atteindre O(1) ou O(log N) par opération
- [[dynamic-programming-fundamentals]] - la programmation dynamique par masque de bits combine bits et programmation dynamique
- [[traveling-salesman-problem]] - application classique de la programmation dynamique par masque de bits
