---
title: "Zwei-Zeiger-Technik"
category: patterns
tags: [algorithms, two-pointers, sorted-array, optimization, space-time-tradeoff]
level: 3
source_sha256: 58cd00b0eb6311f92646aa72bdd41435fcec7376a67799b1633039c8a1b757cb
translation: machine
translated_at: '2026-10-24'
---
# Zwei-Zeiger-Technik {#two-pointer-technique}

Die Zwei-Zeiger-Technik verwendet zwei Indizes, um Datenstrukturen (typischerweise Arrays) zu durchlaufen, und reduziert dabei die Zeitkomplexität, indem sie die sortierte Reihenfolge oder andere strukturelle Eigenschaften ausnutzt. Sie ist verbreitet bei Problemen mit Paaren, Teilarrays und Teilfolgen.

## Wichtige Fakten {#key-facts}

- Reduziert typischerweise die Brute-Force-Lösung mit O(n^2) auf O(n) oder O(n log n)
- Erfordert ein sortiertes Array für den konvergierenden Zeigeransatz
- Zwei Varianten: konvergierend (linker und rechter Zeiger bewegen sich aufeinander zu) und parallel (beide bewegen sich vorwärts)
- Häufig Teil des Zeit-Speicher-Tradeoffs: O(n^2) Zeit, O(1) Speicher -> O(n) Zeit, O(n) Speicher (Hash) oder O(n log n) Zeit, O(1) Speicher (Sortieren + Zwei Zeiger)

## Muster {#patterns}

### Two-Sum mit Sortieren + Zwei Zeigern - O(n log n) {#two-sum-with-sort-two-pointers-on-log-n}

```python
def find_pair(arr, k):
    arr = sorted(arr)
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == k:
            return True
        elif s < k:
            left += 1   # need larger sum
        else:
            right -= 1  # need smaller sum
    return False
```

Warum es funktioniert: Ist die Summe zu klein, kann nur das Inkrementieren von `left` sie vergrößern; ist sie zu groß, kann nur das Dekrementieren von `right` sie verkleinern. Kein Paar wird übersehen, da `arr[left+1] >= arr[left]` und `arr[right-1] <= arr[right]` gilt.

### Two-Sum mit Hash-Set - O(n) {#two-sum-with-hash-set-on}

```python
def find_pair(arr, k):
    visited = set()
    for elem in arr:
        if (k - elem) in visited:
            return True
        visited.add(elem)
    return False
```

### Teilfolgenprüfung - O(n+m) {#subsequence-check-onm}

```python
def is_subsequence(text, pattern):
    ptr_t, ptr_p = 0, 0
    while ptr_t < len(text) and ptr_p < len(pattern):
        if text[ptr_t] == pattern[ptr_p]:
            ptr_p += 1
        ptr_t += 1
    return ptr_p == len(pattern)
```

### Tradeoff-Übersicht für Two-Sum {#trade-off-summary-for-two-sum}

| Ansatz | Zeit | Speicher | Anmerkungen |
|----------|------|-------|-------|
| Brute Force (alle Paare) | O(n^2) | O(1) | Keine Vorverarbeitung |
| Sortieren + Zwei Zeiger | O(n log n) | O(1) zusätzlich | Verändert/kopiert das Array |
| Hash-Set | O(n) | O(n) | Am schnellsten, benötigt zusätzlichen Speicher |

## Stolpersteine {#gotchas}

- Sortieren + Zwei Zeiger verliert die ursprünglichen Indizes (wenn diese benötigt werden, Paare aus (Wert, Index) speichern)
- Der Hash-Set-Ansatz behandelt Duplikate anders – prüfen, ob das Komplement bereits gesehen wurde
- Für sortierte Arrays ist Zwei Zeiger gegenüber Hash-Set zu bevorzugen (O(1) Speicher)
- Die Technik funktioniert bei unsortierten Arrays nicht ohne vorheriges Sortieren (bei der konvergierenden Variante)

## Siehe auch {#see-also}

- [[searching-algorithms]] - Binärsuche als weitere Technik für sortierte Arrays
- [[sorting-algorithms]] - Sortieren als Vorverarbeitungsschritt
- [[dp-sequence-problems]] - fortgeschrittenere Techniken für Sequenzen
