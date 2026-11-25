---
title: "Muster zur Lösung algorithmischer Probleme"
category: concepts
tags: [algorithms, interview, two-pointer, sliding-window, binary-search, problem-solving]
level: 3
source_sha256: 1056872047f7918ef93d8b5f52fa294c1ecc0f1d14792397af438fd3ae36f786
translation: machine
translated_at: '2026-10-24'
---
# Muster zur Lösung algorithmischer Probleme {#algorithm-problem-solving-patterns}

Systematischer Ansatz für Algorithmusprobleme: der 7-Schritte-Interviewprozess, gängige Muster (Two-Pointer, Sliding Window), Optimierungstechniken und Richtlinien zur Auswahl von Datenstrukturen.

## Wichtige Fakten {#key-facts}

- BUD-Optimierung: Engpässe (Bottlenecks), Unnötige Arbeit (Unnecessary work), Doppelte Arbeit (Duplicate work) identifizieren
- Hash-Maps lösen jedes Problem vom Typ „Habe ich das schon gesehen?“ oder „Suche nach Schlüssel“ in O(1)
- Heaps lösen Probleme wie das k-größte/k-kleinste Element, das Zusammenführen von k sortierten Listen und Scheduling-Probleme
- Two-Pointer funktioniert auf sortierten Arrays oder bei der Suche nach Paaren
- Sliding Window funktioniert bei Problemen mit zusammenhängenden Teilarrays bzw. Teilstrings
- Bottom-up-DP ist meist effizienter als Top-down-Rekursion mit Memoisierung

## Muster {#patterns}

### Der 7-Schritte-Prozess {#the-7-step-process}

1. **Aufmerksam zuhören** – eindeutige Randbedingungen identifizieren (sortiert? Baum vs. Graph? Speichergrenzen?)
2. **Ein Beispiel zeichnen** – konkret, groß genug, kein Spezialfall
3. **Brute-Force formulieren** – auch mit O(N^3); zeigt das Verständnis
4. **Optimieren** – BUD: Engpässe (Bottlenecks), Unnötige Arbeit (Unnecessary work), Doppelte Arbeit (Duplicate work)
5. **Durchgehen** – Algorithmus vor dem Programmieren anhand des Beispiels überprüfen
6. **Programmieren** – modular, echter Code (kein Pseudocode)
7. **Testen** – Randfälle: leer, einzelnes Element, Duplikate, negative Werte

### Two-Pointer {#two-pointer}

```python
left, right = 0, len(arr) - 1
while left < right:
    if condition: left += 1
    else: right -= 1
```

Verwendung für: Paarsuche in sortierten Arrays, Prüfung auf Palindrome, Partitionierungsprobleme.

### Sliding Window {#sliding-window}

```python
start = 0
for end in range(len(s)):
    # expand window
    while window_invalid:
        # shrink from start
        start += 1
    best = max(best, end - start + 1)
```

Verwendung für: längster/kürzester Teilstring mit einer Bedingung, Teilarray maximaler Summe der Länge k.

### Vorlage für die binäre Suche {#binary-search-template}

```python
lo, hi = 0, len(arr) - 1
while lo <= hi:
    mid = lo + (hi - lo) // 2  # avoids integer overflow
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
```

Verwendung für: sortierte Daten, Reduzierung des Suchraums, Ermittlung von Grenzen.

### Leitfaden zur Auswahl von Datenstrukturen {#data-structure-selection-guide}

| Problemtyp | Datenstruktur | Zugriff |
|-------------|---------------|--------|
| „Habe ich das schon gesehen?“ | Hash-Map | O(1) im Mittel |
| k-größtes/k-kleinstes Element | Heap | O(log N) |
| Bereichsabfragen, Vorgänger | BST / sortierte Struktur | O(log N) |
| Zusammenhangskomponenten | Union-Find | O(alpha(N)) |
| Kürzester Pfad (ungewichtet) | BFS mit Queue | O(V + E) |
| Kürzester Pfad (gewichtet) | Dijkstra mit Heap | O((V+E) log V) |

### Optimierungstechniken {#optimization-techniques}

**Abwägungen zwischen Speicher und Zeit**:
- Hash-Tabellen für O(1)-Zugriff statt O(N)-Durchlauf
- Vorverarbeitung/Sortierung, um binäre Suche zu ermöglichen
- Memoisierung, um die wiederholte Berechnung von Teilproblemen zu vermeiden

**Dynamische Programmierung**:
- Überlappende Teilprobleme identifizieren
- Zustand definieren: dp[i] = „beste Lösung für ein Problem der Größe i“
- Rekurrenz: dp[i] = f(dp[i-1], dp[i-2], ...)

### Sauberer Code für Algorithmen {#clean-code-for-algorithms}

- **Aussagekräftige Namen**: `leftPointer` statt `l`, `currentMax` statt `cm`
- **Funktionslänge**: Passt eine Funktion nicht auf den Bildschirm, aufteilen
- **Single Responsibility**: Parsing, Logik und Ausgabe trennen
- **Keine Magic Numbers**: `MAX_SIZE = 1000` statt nur `1000`
- **Kommentare erklären das WARUM**: nicht das Was (das sollte lesbar sein), sondern warum dieser Ansatz gewählt wurde

## Stolperfallen {#gotchas}

- `lo + (hi - lo) // 2` vermeidet Integer-Überläufe; `(lo + hi) // 2` kann in Sprachen mit fester Ganzzahlbreite überlaufen
- Off-by-one-Fehler bei der binären Suche: `lo <= hi` vs. `lo < hi` hängt davon ab, ob die Endpunkte eingeschlossen sind
- Sliding Window funktioniert nur bei Problemen, in denen das Verkleinern des Fensters von links immer gültig ist
- Two-Pointer auf unsortierten Daten erfordert zuerst eine Sortierung – die Kosten von O(N log N) einplanen
- Randfälle immer explizit behandeln: leere Eingabe, einzelnes Element, nur Duplikate

## Siehe auch {#see-also}

- [[data-structures-fundamentals]] – Arrays, Hash-Tabellen, Big-O-Analyse
- [[trees-and-graphs]] – Algorithmen zur Graphtraversierung
- [[sorting-algorithms]] – Sortierung als Vorverarbeitungsschritt
- [[dynamic-programming]] – Memoisierung und Tabellierung
