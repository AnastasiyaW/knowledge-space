---
title: "Sortieralgorithmen"
category: algorithms
tags: [algorithms, sorting, comparison-sort, merge-sort, quick-sort, radix-sort]
level: 3
source_sha256: 58913e5b33db38b57aff1ed791e7fa72a908f54c1a3a2425274a199877cdb4b1
translation: machine
translated_at: '2026-10-24'
---
# Sortieralgorithmen {#sorting-algorithms}

Umfassende Referenz zu Sortieralgorithmen, die vergleichsbasierte Sortierverfahren (Insertion Sort, Bubble Sort, Selection Sort, Merge Sort, Quick Sort, Heap Sort), nicht vergleichsbasierte Sortierverfahren (Counting Sort, Radix Sort, Bucket Sort) und deren Eigenschaften behandelt. Die theoretische untere Schranke für vergleichsbasiertes Sortieren ist Omega(n log n).

## Vergleichstabelle {#comparison-table}

| Algorithmus | Best | Average | Worst | Speicher | Stabil | In-place |
|-----------|------|---------|-------|-------|--------|----------|
| Insertion Sort | O(n) | O(n^2) | O(n^2) | O(1) | Ja | Ja |
| Bubble Sort | O(n) | O(n^2) | O(n^2) | O(1) | Ja | Ja |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) | O(1) | Nein | Ja |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | Nein | Ja |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Ja | Nein |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | O(log n) | Nein | Ja |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | Ja | Nein |
| Radix Sort | O(d(n+k)) | O(d(n+k)) | O(d(n+k)) | O(n+k) | Ja | Nein |
| Bucket Sort | O(n+k) | O(n+k) | O(n^2) | O(n+k) | Ja | Nein |

## Klassifikationseigenschaften {#classification-properties}

| Eigenschaft | Definition |
|----------|-----------|
| **Stabil** | Gleiche Elemente behalten ihre ursprüngliche relative Reihenfolge bei |
| **In-place** | Benötigt O(1) zusätzlichen Speicher |
| **Adaptiv** | Schneller bei nahezu sortierter Eingabe |
| **Online** | Kann die Eingabe sequenziell verarbeiten |
| **Vergleichsbasiert** | Verwendet nur Elementvergleiche zur Bestimmung der Reihenfolge |

## Wichtige Fakten {#key-facts}

- **Untere Schranke für Vergleichssortierungen**: Omega(n log n) - Beweis über den Entscheidungsbaum (n! Blätter, Baumhöhe >= log2(n!) = Omega(n log n))
- **Nicht vergleichsbasierte Sortierverfahren** durchbrechen diese Schranke, indem sie die Struktur der Schlüssel nutzen (Counting, Radix, Bucket)
- Pythons `sorted()` und `.sort()` verwenden **Timsort** (hybrides Merge- und Insertion-Verfahren): O(n log n) im schlechtesten Fall, O(n) im besten Fall, stabil, adaptiv

## Muster {#patterns}

### Insertion Sort {#insertion-sort}

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
```

Geeignet für: kleine Arrays, nahezu sortierte Daten, Online-Sortierung. O(n) im besten Fall bei sortierter Eingabe.

### Selection Sort {#selection-sort}

```python
def selection_sort(arr):
    for i in range(len(arr)):
        pos_min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[pos_min]:
                pos_min = j
        arr[i], arr[pos_min] = arr[pos_min], arr[i]
```

Immer O(n^2), unabhängig von der Eingabereihenfolge. Nicht adaptiv, nicht stabil.

### Merge Sort {#merge-sort}

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```

Rekurrenz: T(n) = 2T(n/2) + O(n) -> O(n log n). Der Rekursionsbaum hat log2(n) Ebenen, wobei in jeder Ebene O(n) Arbeit für das Mischen anfällt. Stabil, benötigt jedoch O(n) zusätzlichen Speicher.

### Quick Sort {#quick-sort}

```python
def quick_sort(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
```

O(n^2) im schlechtesten Fall, wenn das Pivot-Element immer ungünstig gewählt wird (sortiertes Array und immer das erste/letzte Element als Pivot). O(n log n) im Durchschnitt. In der Praxis schneller als Merge Sort aufgrund von Cache-Lokalität und kleinen Konstanten. Der schlechteste Fall tritt bei zufälliger oder Median-of-Three-Pivot-Auswahl selten auf.

### Counting Sort {#counting-sort}

Für Ganzzahlen im Bereich [0, k). Zeit O(n + k), Speicher O(k). Nützlich, wenn k = O(n).

### Radix Sort {#radix-sort}

Sortierung nach Ziffern von LSD zu MSD unter Verwendung von Counting Sort als Teilroutine. Zeit O(d(n+k)), wobei d = Anzahl der Ziffern und k = Ziffernbereich. Für Ganzzahlen fester Breite: O(n).

### Python Built-in Sorting {#python-built-in-sorting}

```python
sorted(strs)                          # lexicographic
sorted(strs, key=len)                 # by length
sorted(strs, key=lambda s: s.count('c'))  # by custom criterion
sorted(products, key=lambda p: p['price'])  # by dict field
```

## Fallstricke {#gotchas}

- Quicksort hat im schlechtesten Fall O(n^2) bei bereits sortierten Arrays mit naiver Pivot-Wahl (erstes/letztes Element)
- Selection Sort ist NICHT stabil - weitreichende Vertauschungen verschieben gleiche Elemente
- Bubble Sort mit einem Flag zum vorzeitigen Abbruch wird adaptiv (O(n) bei sortierter Eingabe)
- Shell Sort (Insertion Sort mit Lücken) erreicht mit Hibbard-Lücken O(n log^2 n)
- Counting Sort erfordert nichtnegative Ganzzahlen in einem bekannten Bereich
- Bucket Sort degeneriert zu O(n^2), wenn alle Elemente im selben Bucket landen

## Siehe auch {#see-also}

- [[complexity-analysis]] - Verständnis der O-Notation
- [[searching-algorithms]] - binäre Suche erfordert sortierte Eingabe
- [[functions]] - Details zu sorted() und sort()
