---
title: "Dynamische Programmierung und Rekursion"
category: concepts
tags: [algorithms, dynamic-programming, recursion, memoization]
level: 3
source_sha256: 479253ea74773e4ccd46f8dbb73ef3f5c374afed17481ada83ad290922b57bf0
translation: machine
translated_at: '2026-10-24'
---
# Dynamische Programmierung und Rekursion {#dynamic-programming-and-recursion}

Grundlagen der Rekursion, Memoization (Top-down), Bottom-up-Tabulierung und das Erkennen von DP-Möglichkeiten. Zentrale Technik für Optimierungsprobleme mit überlappenden Teilproblemen.

## Wichtige Fakten {#key-facts}

- Rekursion benötigt drei Bestandteile: Basisfall, rekursiver Aufruf (bewegt sich auf den Basisfall zu) und Weitergabe des Rückgabewerts
- Fibonacci ohne Memoization: O(2^N); mit Memoization: O(N)
- Bottom-up (iterativ) ist meist speichereffizienter als Top-down (memoisierte Rekursion)
- DP ist anwendbar, wenn es überlappende Teilprobleme gibt - der Baum der rekursiven Aufrufe enthält doppelte Zweige
- Memoization tauscht O(N) Speicherplatz gegen eine drastische Zeitersparnis
- Stack-Overflow tritt auf, wenn die Rekursionstiefe den Speicher des Aufrufstapels überschreitet

## Muster {#patterns}

### Grundlagen der Rekursion {#recursion-fundamentals}

```python
def factorial(n):
    return 1 if n == 1 else n * factorial(n - 1)
```

**Wann Rekursion verwenden**: Probleme mit unbekannter oder variabler Tiefe (Traversierung von Dateisystemen, Baumoperationen, fraktale Strukturen).

```ruby
# Directory traversal - unknown depth handled naturally
def find_directories(directory)
  Dir.foreach(directory) do |filename|
    if File.directory?("#{directory}/#{filename}") && filename != "." && filename != ".."
      puts "#{directory}/#{filename}"
      find_directories("#{directory}/#{filename}")
    end
  end
end
```

**Rekursive Funktionen schreiben**: Identifiziere die Aktion für einen einzelnen Schritt, übergebe zusätzliche Parameter zur Verfolgung des Zustands, und die letzte Zeile ist der rekursive Aufruf.

```python
def double_array(array, index=0):
    if index >= len(array): return
    array[index] *= 2
    double_array(array, index + 1)
```

### Memoization (Top-down) {#memoization-top-down}

Ergebnisse teurer rekursiver Aufrufe zwischenspeichern:

```python
def fib(n, memo={}):
    if n <= 1: return n
    if n not in memo:
        memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]
```

### Bottom-up-Tabulierung {#bottom-up-tabulation}

Von kleinen zu großen Teilproblemen iterieren und die Ergebnisse in einer Tabelle speichern:

```python
def fib_bottom_up(n):
    if n <= 1: return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i-1] + table[i-2]
    return table[n]
```

### DP-Framework zur Problemlösung {#dp-problem-solving-framework}

1. **Überlappende Teilprobleme identifizieren** - dieselbe Berechnung wird mit unterschiedlichen Parametern wiederholt
2. **Zustand definieren**: dp[i] = "beste Lösung für ein Problem der Größe i"
3. **Rekurrenz**: dp[i] = f(dp[i-1], dp[i-2], ...)
4. **Basisfälle**: kleinste Teilprobleme mit bekannten Antworten
5. **Berechnungsrichtung**: bottom-up (iterativ) oder top-down (memoisiert)

### Vorverarbeitungsoptimierung {#preprocessing-optimization}

Beispiel - das größte Teilquadrat in einer Matrix finden, in dem alle Randzellen gefüllt sind:

Naiv: O(N^5). Mit Vorverarbeitung besser: O(N^3).

```python
# Preprocess consecutive filled cells in each direction
zeros_right = [[0]*n for _ in range(n)]
zeros_below = [[0]*n for _ in range(n)]
for i in range(n-1, -1, -1):
    for j in range(n-1, -1, -1):
        if matrix[i][j] == 1:
            zeros_right[i][j] = 1 + (zeros_right[i][j+1] if j+1 < n else 0)
            zeros_below[i][j] = 1 + (zeros_below[i+1][j] if i+1 < n else 0)
```

Eine Randkandidatenprüfung kostet nun pro Seite O(1) statt O(N).

## Fallstricke {#gotchas}

- Standardmäßiges veränderliches Default-Argument in Python (`memo={}`) bleibt über Aufrufe hinweg erhalten - nützlich für Memoization, aber in anderen Kontexten ein häufiger Fehler
- Rekursionstiefenlimit in Python: Standardwert etwa 1000 (mit `sys.setrecursionlimit()` änderbar, bei tiefer Rekursion ist jedoch eine iterative Lösung vorzuziehen)
- Bottom-up erlaubt oft eine Speicheroptimierung (z. B. benötigt Fibonacci nur die letzten zwei Werte statt der vollständigen Tabelle)
- Nicht jedes rekursive Problem profitiert von DP - nur solche mit überlappenden Teilproblemen (nicht Divide-and-Conquer wie Mergesort)

## Siehe auch {#see-also}

- [[data-structures-fundamentals]] - Rekursion auf Arrays, Big-O-Analyse
- [[trees-and-graphs]] - rekursive Baumtraversierung, DFS
- [[algorithms/problem-patterns]] - Sliding Window, Two-Pointer, Interview-Techniken
