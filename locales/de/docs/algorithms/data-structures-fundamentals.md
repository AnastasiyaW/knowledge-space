---
title: "Datenstrukturen-Grundlagen - Arrays, Hash-Tabellen, verkettete Listen"
category: concepts
tags: [data-structures, arrays, hash-tables, linked-lists, stacks, queues, big-o]
level: 2
source_sha256: bdf6b5188d6245ac9fb3477c00081e22c4181b53b6dc5c48730cda447ec9e825
translation: machine
translated_at: '2026-10-24'
---
# Datenstrukturen-Grundlagen - Arrays, Hash-Tabellen, verkettete Listen {#data-structures-fundamentals-arrays-hash-tables-linked-lists}

Grundlegende Operationen von Datenstrukturen und Komplexitätsanalyse: Arrays, sortierte Arrays mit binärer Suche, Hash-Tabellen, verkettete Listen, Stacks und Queues. Schwerpunkt auf den Kosten der Operationen und der Frage, wann welche Struktur zu wählen ist.

## Key Facts {#key-facts}

- Big O misst Schritte (hardwareunabhängig), nicht Zeit; Konstanten werden ignoriert
- Arrays: O(1) Lesen per Index, O(N) Einfügen/Löschen (Verschieben)
- Hash-Tabellen: O(1) im Durchschnitt Lesen/Schreiben/Löschen per Schlüssel, O(N) Suche per Wert
- Verkettete Listen: O(1) Einfügen/Löschen an bekannter Position, O(N) Lesen per Index
- Binäre Suche auf sortiertem Array: O(log N) - 1 Mio. Elemente = maximal 20 Schritte
- Idealer Load Factor einer Hash-Tabelle = 0,7 (7 Elemente pro 10 Zellen)

## Patterns {#patterns}

### Array-Operationen {#array-operations}

| Operation | Schritte | Hinweise |
|-----------|----------|----------|
| Lesen per Index | O(1) | Direkte Adressberechnung |
| Suche (linear) | O(N) | Jedes Element muss geprüft werden |
| Einfügen am Ende | O(1) | An der nächsten Adresse ablegen |
| Einfügen am Anfang | O(N) | Elemente müssen nach rechts verschoben werden |
| Löschen | O(N) | Elemente müssen nach links verschoben werden |

**Mengen (keine Duplikate)**: Das Einfügen erfordert zuerst eine O(N)-Suche, daher ist das Einfügen auch am Ende O(N).

### Binäre Suche {#binary-search}

```python
def binary_search(array, target):
    lo, hi = 0, len(array) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoids integer overflow
        if array[mid] == target: return mid
        elif array[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return None
```

| Elemente | Maximum lineare Suche | Maximum binäre Suche |
|----------|----------------------|----------------------|
| 100 | 100 | 7 |
| 10.000 | 10.000 | 14 |
| 1.000.000 | 1.000.000 | 20 |

### Hash-Tabellen {#hash-tables}

Eine Hash-Funktion wandelt den Schlüssel in einen Array-Index um. Kollisionen werden per Chaining behandelt (an jeder Zelle eine Liste aus Schlüssel-Wert-Paaren).

**Optimierungsmuster** - Array in Hash umwandeln für O(1)-Lookups:
```ruby
hash = {}
array.each { |elem| hash[elem] = true }
# Now: hash[value] -> O(1) instead of O(N) scan
```

**Prüfung auf Teilmenge eines Arrays** - naiv O(N*M), optimiert O(N+M):
```javascript
function isSubset(array1, array2) {
  const larger = array1.length > array2.length ? array1 : array2;
  const smaller = array1.length > array2.length ? array2 : array1;
  const hashTable = {};
  for (const elem of larger) { hashTable[elem] = true; }
  for (const elem of smaller) {
    if (!hashTable[elem]) return false;
  }
  return true;
}
```

**Bedingungen durch Hash-Lookup ersetzen**:
```python
STATUS_CODES = {200: "OK", 301: "Moved Permanently", 404: "Not Found", 500: "Internal Server Error"}
def status_code_meaning(code):
    return STATUS_CODES.get(code)
```

### Verkettete Listen {#linked-lists}

| Operation | Verkettete Liste | Array |
|-----------|-----------------|-------|
| Lesen per Index | O(N) | O(1) |
| Einfügen an bekannter Position | O(1) | O(N) |
| Einfügen am Kopf | O(1) | O(N) |
| Löschen an bekannter Position | O(1) | O(N) |
| Suche | O(N) | O(N) |

Queue auf einer doppelt verketteten Liste: enqueue = insert_at_end O(1), dequeue = remove_from_front O(1). Besser als eine array-basierte Queue.

### Stacks und Queues {#stacks-and-queues}

**Stack (LIFO)**: Push/Pop an demselben Ende. Verwendet für: Funktionsaufrufe, Undo, DFS.
**Queue (FIFO)**: Enqueue am Ende, Dequeue vorne. Verwendet für: BFS, Task-Queues.

### Big-O-Referenz {#big-o-reference}

| Notation | Bezeichnung | Beispiel |
|----------|-------------|----------|
| O(1) | Konstant | Array-Lesen, Hash-Lookup |
| O(log N) | Logarithmisch | Binäre Suche, BST-Operationen |
| O(N) | Linear | Lineare Suche, Traversierung |
| O(N log N) | Linearithmisch | Quicksort (Durchschnitt), Mergesort |
| O(N^2) | Quadratisch | Bubble-, Insertion- und Selection-Sort |
| O(2^N) | Exponentiell | Brute-Force-Kombinationen |

**Wichtig**: Big O ignoriert Konstanten. O(N/2), O(2N) und O(100N) vereinfachen sich alle zu O(N). Innerhalb derselben Kategorie sind Konstanten dennoch relevant.

### Speicherkomplexität {#space-complexity}

| Struktur | Speicher |
|----------|----------|
| Array mit N Elementen | O(N) |
| N x N Matrix | O(N^2) |
| Rekursionstiefe D | O(D) Stack-Frames |
| Hash-Tabelle mit N Elementen | O(N) |

## Gotchas {#gotchas}

- Die Suche in einer Hash-Tabelle ist nur mit dem Schlüssel O(1); die Suche per Wert ist O(N)
- Binäre Suche setzt sortierte Daten voraus - die Sortierkosten O(N log N) lohnen sich bei einer einzelnen Suche möglicherweise nicht
- Trade-off sortiertes Array: schnellere Suche O(log N), aber langsameres Einfügen O(N) zur Erhaltung der Reihenfolge
- Big O Best/Worst Case: Die angegebene Komplexität ist meist der Worst Case; lineare Suche ist im Best Case O(1), im Worst Case O(N)

## See Also {#see-also}

- [[trees-and-graphs]] - BST, Heaps, Tries, BFS, DFS, Dijkstra
- [[sorting-algorithms]] - detaillierte Sortierimplementierungen und Vergleiche
- [[dynamic-programming]] - Memoization, Rekursionsmuster
- [[algorithms/problem-patterns]] - Two-Pointer, Sliding Window, Interview-Techniken
