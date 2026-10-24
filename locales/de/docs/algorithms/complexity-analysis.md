---
title: "Komplexitätsanalyse"
category: concepts
tags: [algorithms, big-o, time-complexity, space-complexity, asymptotic-analysis]
level: 3
source_sha256: 40297372b9620c726d06356563d52be7f1b9a32be8a13d1a3a8700ed230dcc57
translation: machine
translated_at: '2026-10-24'
---
# Komplexitätsanalyse {#complexity-analysis}

Die Komplexitätsanalyse misst, wie sich der Ressourcenverbrauch eines Algorithmus (Zeit oder Speicher) mit der Eingabegröße n skaliert. Sie abstrahiert von Hardware und Programmiersprache und konzentriert sich auf asymptotische Wachstumsraten. Die zentralen Notationen sind Big-O (obere Schranke), Big-Omega (untere Schranke) und Big-Theta (scharfe Schranke).

## Wichtige Fakten {#key-facts}

- **Zeitkomplexität** = Anzahl der Operationen in Abhängigkeit von n, klassifiziert nach asymptotischem Wachstum
- **Speicherkomplexität** = zusätzlicher Speicher über die Eingabe hinaus (Konvention: zusätzlichen Speicher angeben, nicht den Gesamtspeicher)
- Konstanten weglassen: O(2n) = O(n), O(100n) = O(n)
- Nur den dominanten Term behalten: O(n^2 + 100n + 12) = O(n^2)
- Mehrere Parameter möglich: O(n * m), wenn die Eingaben unterschiedliche Größen haben
- **Verborgene Konstanten** sind in der Praxis relevant: Zwei O(n)-Algorithmen können sich um den Faktor 100 unterscheiden

## Komplexitätshierarchie {#complexity-hierarchy}

```text
O(1) < O(log n) < O(sqrt(n)) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)
```

| Klasse | Beispiel |
|--------|----------|
| O(1) | Zugriff auf Array-Index, Gerade/ungerade prüfen mit `n & 1` |
| O(log n) | Binäre Suche, Quersumme, Anzahl der Ziffern |
| O(sqrt(n)) | Schleife `while i*i < n` |
| O(n) | Lineare Suche, Array-Minimum/-Maximum |
| O(n log n) | Merge Sort, optimales vergleichsbasiertes Sortieren |
| O(n^2) | Selection Sort, Brute-Force Two-Sum, alle Paare |
| O(n^3) | Naive Matrixmultiplikation |
| O(2^n) | Rekursive LCS ohne Memoization |
| O(n!) | Erzeugung aller Permutationen |

## Notation {#notation}

| Symbol | Bedeutung | Beschreibt |
|--------|-----------|------------|
| O(f(n)) | Scharfe obere Schranke | Schlechtester Fall (und darunter) |
| Omega(f(n)) | Scharfe untere Schranke | Bester Fall (und darüber) |
| Theta(f(n)) | Exakte Schranke | Obere und untere Schranke zugleich |
| o(f(n)) | Strikte obere Schranke | Wächst strikt langsamer als f |
| omega(f(n)) | Strikte untere Schranke | Wächst strikt schneller als f |

Bester, durchschnittlicher und schlechtester Fall sind unabhängig von Big-O/Omega/Theta. Jeder Fall hat eine eigene Funktion T(n), die separat abgeschätzt werden kann.

## Muster {#patterns}

### Operationen aus Code zählen {#counting-operations-from-code}

```python
# Single loop: O(n)
for elem in arr:
    process(elem)

# Nested loops: O(n^2)
for i in range(n):
    for j in range(n):
        process(i, j)

# Doubling step: i = 1, 2, 4, 8, ... n -> O(log n)
i = 1
while i < n:
    i *= 2

# Square root pattern: i*i < n -> O(sqrt(n))
i = 0
while i * i < n:
    i += 1

# Triangular loops: sum 0+1+2+...+(n-1) = n(n-1)/2 -> O(n^2)
for i in range(1, n + 1):
    for j in range(i):
        process(j)

# Inner loop depends on i^2: total = sum of i^2 = O(n^3)
for i in range(n):
    for j in range(i * i):
        process(j)

# Conditional inner loop at i == n//2 only: O(n) + O((n/2)^2) = O(n^2)
for i in range(n):
    if i == n // 2:
        for j in range(i * i):
            process(j)

# Conditional at constant i == 10: O(n) + O(100) = O(n)
for i in range(n):
    if i == 10:
        for j in range(i * i):
            process(j)
```

### Fallstricke bei der Speicherkomplexität {#space-complexity-traps}

```python
# String concatenation creates new string: O(len(s1) + len(s2))
result = str1 + str2

# Building prefixes: total space O(n^2)
prefixes = [s[0:i] for i in range(len(s))]

# Reference vs copy
copy = arr        # O(1) - same object, NOT a copy
copy = arr.copy() # O(n) - actual copy

# Fixed-size array is O(1) space
occurrences = [0] * 26  # constant regardless of input
```

### Mehrere Parameter {#multiple-parameters}

```python
# O(n * m) where n = len(arr1), m = len(arr2)
def intersection(arr1, arr2):
    for elem in arr1:
        if elem in arr2:  # O(m) scan each time
            print(elem)

# O(min(n, m)) - loop terminates at shorter
def where_equal(str1, str2):
    i = 0
    while i < len(str1) and i < len(str2):
        if str1[i] == str2[i]:
            yield i
        i += 1
```

## Bester, durchschnittlicher, schlechtester Fall {#best-average-worst-case}

- **Bester Fall:** Günstigste Eingabe (z. B. Element an Index 0 bei der linearen Suche)
- **Schlechtester Fall:** Ungünstigste Eingabe (z. B. Element nicht vorhanden)
- **Durchschnittlicher Fall:** Erwartete Kosten über alle möglichen Eingaben; erfordert Wahrscheinlichkeitsannahmen
- Ein **randomisierter Algorithmus** nutzt interne Zufälligkeit, um den schlechtesten Fall in einen erwarteten Durchschnittsfall zu überführen

## Stolperfallen {#gotchas}

- Zwei O(n)-Algorithmen können sich durch Konstanten um den Faktor 100 in der Laufzeit unterscheiden
- Ein O(n log n)-Algorithmus mit Konstante 13 kann für n < 200 langsamer sein als ein O(n^2)-Algorithmus mit Konstante 0,5
- O(n^2) und O(m^2) sind nicht vergleichbar, solange das Verhältnis von n und m unbekannt ist
- Die Quersumme von n hat die Komplexität O(log n) (n hat floor(log10(n))+1 Ziffern)
- `max(n, 10)` in der Schleifenbedingung: O(n) für große n, O(1) für n < 10
- `min(n, 10)` in der Schleifenbedingung: immer O(1), unabhängig von n

## Siehe auch {#see-also}

- [[amortized-analysis]] - durchschnittliche Kosten pro Operation über Operationsfolgen
- [[complexity-classes]] - P, NP, NP-vollständig, NP-schwer
- [[sorting-algorithms]] - Komplexitätsvergleich von Sortierverfahren
