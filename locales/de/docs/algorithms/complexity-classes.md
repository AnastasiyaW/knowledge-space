---
title: "Komplexitätsklassen: P, NP, NP-vollständig"
category: concepts
tags: [algorithms, complexity-theory, P, NP, NP-complete, NP-hard, reductions]
level: 2
source_sha256: db9d509f35ebb5f29a067aa20a4e580604f24aae9beae6911afe9b22ed70ba7c
translation: machine
translated_at: '2026-10-24'
---
# Komplexitätsklassen: P, NP, NP-vollständig {#complexity-classes-p-np-np-complete}

Komplexitätsklassen ordnen Entscheidungsprobleme nach den Rechenressourcen, die benötigt werden, um sie zu lösen oder ihre Lösung zu verifizieren. Die Frage P vs. NP – ob jedes Problem, dessen Lösung sich schnell verifizieren lässt, auch schnell gelöst werden kann – gehört zu den wichtigsten offenen Problemen der Informatik.

## Wichtige Fakten {#key-facts}

- **P**: Entscheidungsprobleme, die in polynomieller Zeit lösbar sind. Beispiele: Palindromprüfung, kürzester Pfad, Sortieren
- **NP**: Entscheidungsprobleme, bei denen eine JA-Antwort in polynomieller Zeit **verifiziert** werden kann. Beispiel: Gegeben eine Partition, prüfen, ob beide Hälften die gleiche Summe haben, in O(n)
- **NP-vollständig**: Die schwersten Probleme in NP – jedes NP-Problem lässt sich in polynomieller Zeit auf sie reduzieren. Beispiel: Hamiltonpfad, 3-SAT
- **NP-schwer**: Mindestens so schwer wie NP-vollständig, aber nicht notwendigerweise in NP (möglicherweise keine Entscheidungsprobleme). Beispiel: Halteproblem, TSP-Optimierung
- Alle Probleme in P liegen auch in NP (wenn in polynomieller Zeit lösbar, dann auch in polynomieller Zeit verifizierbar)
- P != NP wird weithin angenommen, ist aber nicht bewiesen (Millennium-Preis-Problem, 1 Mio. US-Dollar Preisgeld)

## Klassenhierarchie {#class-hierarchy}

```text
NP-hard
  |-- NP-complete  <-- hardest problems IN NP
  |-- (problems not in NP, e.g., halting problem)
NP
  |-- NP-complete
  |-- P  (assuming P != NP)
```

## Muster {#patterns}

### Reduktion {#reduction}

Problem A in Problem B transformieren, sodass die Lösung von B auch A löst. Liegt B in P und lässt sich A in polynomieller Zeit auf B reduzieren, dann liegt A in P.

Um zu beweisen, dass ein Problem X NP-vollständig ist:
1. Zeigen, dass X in NP liegt (Lösung in polynomieller Zeit verifizierbar)
2. Zeigen, dass ein bekanntes NP-vollständiges Problem in polynomieller Zeit auf X reduziert werden kann

### Häufige NP-vollständige Probleme {#common-np-complete-problems}

| Problem | Beschreibung |
|---------|-------------|
| 3-SAT | Erfüllbarkeit einer booleschen Formel in 3-KNF |
| Hamiltonpfad/-kreis | Jeden Knoten genau einmal besuchen |
| Graphenfärbung (k >= 3) | Knoten mit k Farben färben, benachbarte Knoten nie gleich |
| Teilsummenproblem | Gibt es eine Teilmenge, deren Summe dem Zielwert entspricht? |
| Handlungsreisendenproblem (Entscheidung) | Gibt es eine Tour mit Kosten <= k? |
| Partition | Array in zwei Hälften mit gleicher Summe aufteilen |

### Praktische Konsequenzen {#practical-implications}

- Wenn das Problem NP-schwer ist, nicht nach polynomiellen exakten Algorithmen suchen
- Approximationsalgorithmen verwenden (z. B. Christofides für TSP: 1,5-fach des Optimums)
- Heuristiken einsetzen (Greedy, lokale Suche, genetische Algorithmen)
- Exakte Lösungen sind nur für kleine Eingaben machbar (DP mit exponentieller Laufzeit, z. B. Held-Karp O(2^n * n^2))

## Stolperfallen {#gotchas}

- NP bedeutet NICHT „nicht polynomiell“ – es steht für „nichtdeterministisch polynomiell“
- NP-schwere Probleme liegen womöglich gar nicht in NP (Optimierungsvarianten von Entscheidungsproblemen)
- 2-Färbbarkeit ist polynomiell, 3-Färbbarkeit dagegen NP-vollständig
- Teilsummenproblem ist NP-vollständig, besitzt aber eine pseudopolynomielle DP-Lösung in O(n*S) (polynomiell im Wert von S, nicht in der Bitlänge)
- Dass ein Problem NP-vollständig ist, heißt nicht, dass es immer schwer ist – viele Instanzen sind leicht, nur der Worst Case ist schwer

## Siehe auch {#see-also}

- [[complexity-analysis]] - Grundlagen der asymptotischen Analyse
- [[traveling-salesman-problem]] - klassisches NP-schweres Optimierungsproblem
- [[graph-coloring]] - NP-vollständig für k >= 3
- [[dp-optimization-problems]] - pseudopolynomielle Lösungen für NP-vollständige Probleme
