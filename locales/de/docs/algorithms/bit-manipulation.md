---
title: "Bitmanipulation"
category: concepts
tags: [bitwise, binary, optimization, low-level]
level: 3
source_sha256: a96aeb7feaff3a13ac2fbbacefc0a0a48dc2f81738dd2c514337400349d54b95
translation: machine
translated_at: '2026-10-24'
---
# Bitmanipulation {#bit-manipulation}

Operationen auf einzelnen Bits von Ganzzahlen. Entscheidend für Optimierung, Kryptografie, Netzwerktechnik und Competitive Programming.

## Wichtige Fakten {#key-facts}

- Bitweises UND (`&`): beide Bits 1 -> 1
- Bitweises ODER (`|`): mindestens ein Bit 1 -> 1
- Bitweises XOR (`^`): Bits verschieden -> 1
- Bitweises NICHT (`~`): alle Bits invertieren (Zweierkomplement: `~x = -x - 1`)
- Linksverschiebung (`<<`): Multiplikation mit 2^n
- Rechtsverschiebung (`>>`): Division durch 2^n (arithmetische Verschiebung erhält das Vorzeichen)
- Python-Ganzzahlen haben beliebige Genauigkeit - kein Überlauf

## Grundlegende Tricks {#essential-tricks}

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

## Muster {#patterns}

### Single Number (XOR) {#single-number-xor}

```python
def single_number(nums):
    """Every element appears twice except one. Find it."""
    result = 0
    for n in nums:
        result ^= n
    return result
# XOR properties: a ^ a = 0, a ^ 0 = a, commutative + associative
```

### Fehlende Zahl {#missing-number}

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

### Potenzmenge über Bitmaske {#power-set-via-bitmask}

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

### Bits zählen für alle Zahlen 0..N {#counting-bits-for-all-numbers-0n}

```python
def count_bits_array(n):
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

### Bitmasken-DP (Problem des Handlungsreisenden) {#bitmask-dp-traveling-salesman}

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

## Häufige Bitmuster {#common-bit-patterns}

| Operation | Ausdruck | Ergebnis |
|-----------|-----------|--------|
| Ist Zweierpotenz | `n & (n-1) == 0` | True, wenn Zweierpotenz |
| Niederwertigstes gesetztes Bit | `n & (-n)` | Isoliert das niedrigste 1-Bit |
| Niederwertigstes 1-Bit löschen | `n & (n-1)` | Löscht das niedrigste 1-Bit |
| Alle 1en der Länge k | `(1 << k) - 1` | Binär: 0..01..1 |
| Ist n-tes Bit gesetzt | `(x >> n) & 1` | 0 oder 1 |

## Fallstricke {#gotchas}

- **Problem:** Python `~x` liefert `-(x+1)` aufgrund von Ganzzahlen mit beliebiger Genauigkeit (keine feste Breite) -> **Lösung:** Für Verhalten mit fester Breite mit `~x & 0xFFFFFFFF` für 32 Bit maskieren.
- **Problem:** Vorzeichenbehaftete Rechtsverschiebung erweitert das Vorzeichenbit, vorzeichenlose Rechtsverschiebung nicht -> **Lösung:** Python kennt nur die arithmetische (vorzeichenbehaftete) Rechtsverschiebung. Für vorzeichenloses Verhalten bei negativen Zahlen zuerst in vorzeichenlos umwandeln: `(x & 0xFFFFFFFF) >> n`.
- **Problem:** Speicherexplosion bei Bitmasken-DP für großes N -> **Lösung:** Bitmasken-DP ist nur für N <= 20-25 (2^N Zustände) praktikabel. Für größere N andere Ansätze verwenden.

## Siehe auch {#see-also}

- [[complexity-analysis]] - Bitmanipulation erreicht oft O(1) oder O(log N) pro Operation
- [[dynamic-programming-fundamentals]] - Bitmasken-DP kombiniert Bits mit DP
- [[traveling-salesman-problem]] - klassische Anwendung der Bitmasken-DP
