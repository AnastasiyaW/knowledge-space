---
title: "Sliding-Window-Technik"
category: patterns
tags: [arrays, strings, subarray, optimization]
level: 3
source_sha256: bd19d0700f6e597f90db856f2bacb4011f94726f2b82b2520e87417a09001298
translation: machine
translated_at: '2026-10-24'
---
# Sliding-Window-Technik {#sliding-window-technique}

Ein Fenster (zusammenhängendes Teilarray bzw. Teilstring) wird über die Eingabe geschoben und dabei vergrößert oder verkleinert, bis die Bedingungen erfüllt sind. Dadurch sinkt die Laufzeit der Brute-Force-Lösung von O(N*K) auf O(N).

## Wichtige Fakten {#key-facts}

- Zwei Varianten: Fenster mit fester Größe und Fenster mit variabler Größe
- Verwendet zwei Zeiger (left, right), die die Fenstergrenzen festlegen
- Der rechte Zeiger vergrößert das Fenster, der linke Zeiger verkleinert es
- Vermeidet Neuberechnungen, indem der Fensterzustand inkrementell aktualisiert wird
- Anwendbar, wenn das Problem nach zusammenhängenden Teilarrays bzw. Teilstrings fragt
- Laufzeit: O(N), da jedes Element das Fenster höchstens einmal betritt und einmal verlässt

## Fenster mit fester Größe {#fixed-size-window}

```python
def max_sum_subarray(arr, k):
    """Maximum sum of subarray of size k."""
    window_sum = sum(arr[:k])
    max_sum = window_sum

    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

## Vorlage für Fenster mit variabler Größe {#variable-size-window-template}

```python
def variable_window(arr):
    left = 0
    window_state = {}  # track what's in window
    result = 0

    for right in range(len(arr)):
        # Expand: add arr[right] to window state
        update_state(window_state, arr[right])

        # Shrink: while window violates constraint
        while not valid(window_state):
            remove_state(window_state, arr[left])
            left += 1

        # Update result
        result = max(result, right - left + 1)
    return result
```

## Muster {#patterns}

### Längster Teilstring ohne sich wiederholende Zeichen {#longest-substring-without-repeating-characters}

```python
def length_of_longest_substring(s):
    seen = {}
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
```

### Minimales Fenster-Teilstring {#minimum-window-substring}

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = 0
    start, end = 0, float('inf')

    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1

        while missing == 0:
            if right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1

    return s[start:end + 1] if end != float('inf') else ""
```

### Maximum aller Teilarrays der Größe K (Monotone Deque) {#maximum-of-all-subarrays-of-size-k-monotonic-deque}

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # stores indices, front = max
    result = []

    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        # Maintain decreasing order
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

### Teilarray-Summe gleich K (Präfixsumme + HashMap) {#subarray-sum-equals-k-prefix-sum-hashmap}

```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}

    for num in nums:
        prefix_sum += num
        count += seen.get(prefix_sum - k, 0)
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    return count
```

## Wann einsetzen {#when-to-use}

| Signal | Technik |
|--------|---------|
| "Teilarray der Größe k" | Fenster mit fester Größe |
| "längstes/kürzestes Teilarray mit Bedingung" | Fenster mit variabler Größe |
| "alle Teilarrays, die ... erfüllen" | Fenster mit variabler Größe + Zählung |
| Zusammenhängende Elemente | Kandidat für Sliding Window |
| Nicht zusammenhängende Elemente | KEIN Sliding Window |

## Stolperfallen {#gotchas}

- **Problem:** Sliding Window bei Problemen einsetzen, die nicht zusammenhängende Elemente erfordern -> **Lösung:** Sliding Window funktioniert nur für zusammenhängende Teilarrays bzw. Teilstrings. Für nicht zusammenhängende Elemente DP oder Two-Pointer verwenden.
- **Problem:** Die Verkleinerungsbedingung falsch behandeln, was zu einer Endlosschleife führt -> **Lösung:** Sicherstellen, dass der linke Zeiger in der Verkleinerungsschleife immer vorrückt. Der Fensterzustand muss monoton aktualisiert werden.
- **Problem:** Off-by-one-Fehler bei festem Fenster (Berechnung des ersten Fensters) -> **Lösung:** Das erste Fenster separat initialisieren und dann ab Index k verschieben.

## Siehe auch {#see-also}

- [[two-pointer-technique]] - verwandt, die Zeiger können sich jedoch unabhängig voneinander bewegen
- [[searching-algorithms]] - binäre Suche lässt sich mit Sliding Window kombinieren
- [[complexity-analysis]] - Sliding Window erreicht O(N) amortisiert
