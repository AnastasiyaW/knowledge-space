---
title: "Suchalgorithmen"
category: algorithms
tags: [algorithms, search, binary-search, linear-search, kmp, string-matching]
level: 3
source_sha256: f3fd73b1a796c94c882dd19c8d02ac68a7bb5f78cf718c3daa9ecf1a4184e989
translation: machine
translated_at: '2026-10-24'
---
# Suchalgorithmen {#searching-algorithms}

Behandelt lineare Suche, binäre Suche und KMP-Zeichenkettensuche. Die lineare Suche hat eine Laufzeit von O(n) für unsortierte Daten, die binäre Suche O(log n) für sortierte Daten, und KMP erreicht O(n+m) beim Mustervergleich in Zeichenketten, indem es redundante Vergleiche vermeidet.

## Wichtige Fakten {#key-facts}

- **Lineare Suche**: O(n) Zeit, O(1) Speicher - funktioniert mit beliebigen Daten und beliebigen Prädikaten
- **Binäre Suche**: O(log n) Zeit, O(1) Speicher - erfordert ein sortiertes Array
- **KMP**: O(n+m) Zeit, O(m) Speicher - Mustersuche ohne Zurücksetzen im Text
- Für eine einzelne Abfrage auf unsortierten Daten ist die lineare Suche schneller als Sortieren gefolgt von binärer Suche (O(n) vs. O(n log n))
- Für viele Abfragen auf denselben Daten: einmal sortieren in O(n log n), dann jede Suche binär in O(log n)

## Muster {#patterns}

### Lineare Suche {#linear-search}

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

Funktioniert mit beliebigen Prädikaten - nicht nur mit Gleichheit:

```python
# First element greater than num
def search_greater(arr, num):
    for i in range(len(arr)):
        if arr[i] > num:
            return i
    return -1

# String containing character
def search_contains(arr, ch):
    for i in range(len(arr)):
        if ch in arr[i]:
            return i
    return -1
```

### Binäre Suche {#binary-search}

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

Warum O(log n): Beginnend mit n Elementen verbleiben nach k Iterationen höchstens ceil(n/2^k) Elemente. Stopp, wenn ein Element übrig bleibt: n/2^k = 1 -> k = log2(n).

### Wann welcher Algorithmus {#when-to-choose}

```python
def search(arr, target):
    if is_sorted(arr):
        return binary_search(arr, target)
    else:
        return linear_search(arr, target)
```

### KMP-Zeichenkettensuche - O(n+m) {#kmp-string-search-onm}

Die naive Zeichenkettensuche hat eine Laufzeit von O(n*m), weil sie bei einer Nichtübereinstimmung den Mustervergleich von vorne beginnt. KMP verwendet ein LPS-Array (Longest Proper Prefix which is also Suffix, also das längste echte Präfix, das zugleich Suffix ist), um bereits bekannte übereinstimmende Zeichen zu überspringen.

**Aufbau des LPS-Arrays - O(m):**

```python
def get_lps_arr(pattern):
    lps = [0] * len(pattern)
    length = 0  # length of previous longest prefix-suffix
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length > 0:
            length = lps[length - 1]  # fall back without moving i
        else:
            lps[i] = 0
            i += 1
    return lps
```

Beispiel: `"aabaaab"` -> `[0, 1, 0, 1, 2, 2, 3]`

**KMP-Suche - O(n):**

```python
def kmp(text, pattern):
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    if m == n:
        return 0 if text == pattern else -1
    lps = get_lps_arr(pattern)
    i, j = 0, 0  # text pointer, pattern pointer
    while i < n and j < m:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j > 0:
            j = lps[j - 1]  # don't advance i
        else:
            i += 1
    return i - j if j == m else -1
```

**Warum es funktioniert:** `i` bewegt sich nie rückwärts. Bei einer Nichtübereinstimmung an Position j gibt `lps[j-1]` an, wie viele Zeichen bereits übereinstimmen (Präfix = Suffix des bisher Gelesenen). Gesamt: O(n) für die Suche + O(m) für das LPS-Array = O(n+m).

## Fallstricke {#gotchas}

- Binäre Suche erfordert sortierte Eingaben - angewandt auf unsortierte Daten liefert sie falsche Ergebnisse
- Die Berechnung `mid = (left + right) // 2` kann in Sprachen mit Ganzzahlen fester Größe überlaufen; stattdessen `mid = left + (right - left) // 2` verwenden (in Python kein Problem)
- Beim Aufbau des KMP-LPS-Arrays gilt bei einer Nichtübereinstimmung: auf `lps[length-1]` zurückfallen, NICHT auf 0 zurücksetzen
- Für eine einzelne Suche auf unsortierten Daten ist vorheriges Sortieren (O(n log n)) verschwenderisch gegenüber der linearen Suche (O(n))
- Schlechtester Fall der naiven Zeichenkettensuche: text="aaa...a", pattern="aaa...ab" -> O(n*m)

## Siehe auch {#see-also}

- [[sorting-algorithms]] - binäre Suche erfordert sortierte Eingaben
- [[two-pointer-technique]] - Suchmuster auf sortierten Arrays
- [[complexity-analysis]] - Herleitung von O(log n) verstehen
