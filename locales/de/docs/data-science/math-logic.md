---
title: "Mathematische Logik"
category: foundations
tags: [data-science, math, logic, propositional, sets, proofs]
level: 3
source_sha256: 7281068e6a65810dfbe1eba8b18d5ef141cbd48c23e8ddab617f580b629549a3
translation: machine
translated_at: '2026-10-24'
---
# Mathematische Logik {#mathematical-logic}

Formale Schlusssysteme, die der Informatik und mathematischen Beweisen zugrunde liegen. Aussagenlogik, Prädikatenlogik erster Stufe, Beweistechniken und Algorithmentheorie.

## Aussagenlogik {#propositional-logic}

### Junktoren {#connectives}

| Junktor | Symbol | Wahr, wenn |
|-----------|--------|-----------|
| Negation | ~P | P falsch ist |
| Konjunktion | P & Q | Beide wahr sind |
| Disjunktion | P v Q | Mindestens eines wahr ist |
| Exklusives Oder | P XOR Q | Genau eines wahr ist |
| Implikation | P -> Q | P falsch ist oder beide wahr sind |
| Äquivalenz | P <-> Q | Denselben Wahrheitswert haben |

### Wichtige Eigenschaften {#key-properties}
- **Tautologie**: immer wahr, unabhängig von den Werten der Variablen. Beispiel: P v ~P
- **Kontradiktion**: immer falsch. Beispiel: P & ~P
- **Logische Äquivalenz**: gleiche Wahrheitstafel
- **De Morgansche Gesetze**: ~(P & Q) = ~P v ~Q, ~(P v Q) = ~P & ~Q
- **Kontraposition**: P -> Q ist äquivalent zu ~Q -> ~P
- Bei n Variablen: 2^n Zeilen in der Wahrheitstafel

### Fallstrick bei der Implikation {#implication-gotcha}
P -> Q ist wahr, wenn P falsch ist (leere Wahrheit). „Wenn Schweine fliegen, dann bin ich der König“ ist logisch wahr.

## Prädikatenlogik erster Stufe {#first-order-logic}

Erweitert die Aussagenlogik um:
- **Variablen** über einem Bereich
- **Quantoren**: „für alle“ (Allquantor) und „es existiert“ (Existenzquantor)
- **Prädikate**: P(x), R(x, y)
- **Funktionen**: f(x)

**Negation von Quantoren:**
- ~(forall x, P(x)) = exists x, ~P(x)
- ~(exists x, P(x)) = forall x, ~P(x)

## Beweistechniken {#proof-techniques}

| Methode | Vorgehen |
|--------|----------|
| Direkt | Voraussetzungen annehmen, Folgerung ableiten |
| Widerspruch | Negation der Folgerung annehmen, Widerspruch ableiten |
| Kontraposition | ~Q -> ~P statt P -> Q beweisen |
| Induktion | Induktionsanfang + Induktionsschritt (P(n) -> P(n+1)) |
| Gegenbeispiel | Eine allgemeine Aussage mit einem Beispiel widerlegen |

### Vollständige Induktion {#mathematical-induction}
1. **Induktionsanfang**: P(1) (oder P(0)) beweisen
2. **Induktionsschritt**: P(k) als wahr annehmen, P(k+1) beweisen
3. **Schluss**: P(n) gilt für alle n >= Anfangswert

## Algorithmentheorie {#algorithm-theory}

### Berechenbarkeit {#computability}
- **Turingmaschine**: abstraktes Berechnungsmodell
- **Church-Turing-These**: Alles, was berechenbar ist, kann von einer Turingmaschine berechnet werden
- **Halteproblem**: Kein Algorithmus kann für jedes Programm entscheiden, ob es hält (unentscheidbar)
- **Entscheidbar**: Es existiert ein Algorithmus, der stets hält und die richtige Antwort liefert

### Komplexität {#complexity}
- **P**: in polynomieller Zeit lösbar
- **NP**: in polynomieller Zeit verifizierbar
- **NP-vollständig**: schwierigste Probleme in NP (wenn eines davon in P liegt, liegt ganz NP in P)
- **P vs. NP**: offenes Millennium-Problem

## Axiomatische Systeme {#axiomatic-systems}

- **Axiome**: ohne Beweis akzeptierte Aussagen
- **Theoreme**: aus Axiomen bewiesene Aussagen
- **Widerspruchsfreiheit (Konsistenz)**: Es lassen sich keine Widersprüche herleiten
- **Vollständigkeit**: Jede wahre Aussage ist beweisbar (Gödel: für hinreichend mächtige Systeme unmöglich)

## Relevanz für Data Science {#relevance-to-ds}
- Boolesche Logik liegt der Filterung in pandas zugrunde: `df[(cond1) & (cond2)]`
- SQL-WHERE-Klauseln sind Aussagenlogik
- Entscheidungsbäume sind Konjunktionen von Prädikaten
- Die Berechnungskomplexität bestimmt die Skalierbarkeit von Algorithmen

## Siehe auch {#see-also}
- [[math-precalculus]] - Mengen und Kombinatorik
- [[python-for-ds]] - Boolesche Operationen in Python
- [[sql-for-data-science]] - SQL WHERE als Logik
