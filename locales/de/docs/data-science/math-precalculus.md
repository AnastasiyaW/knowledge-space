---
title: "Grundlagen der Analysis vor der Differentialrechnung"
category: foundations
tags: [data-science, math, algebra, functions, sets]
level: 2
source_sha256: cfc7fccf46941d83e30a97a100c43ce6e2812aecb97209f9f3a5d1bbdffe3eb4
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen der Analysis vor der Differentialrechnung {#pre-calculus-foundations}

Zahlensysteme, Gleichungen, Funktionen und grundlegende Mengenlehre - die Voraussetzungen vor dem Einstieg in Analysis, Wahrscheinlichkeitsrechnung und lineare Algebra.

## Zahlensysteme {#number-systems}

N (natürliche Zahlen) ⊂ Z (ganze Zahlen) ⊂ Q (rationale Zahlen) ⊂ R (reelle Zahlen) ⊂ C (komplexe Zahlen)

- **Rationale Zahlen**: Brüche p/q. Die Dezimaldarstellung bricht ab oder ist periodisch
- **Irrationale Zahlen**: sqrt(2), pi, e. Nicht abbrechend und nicht periodisch
- **Fundamentalsatz der Arithmetik**: Jede ganze Zahl > 1 besitzt eine eindeutige Primfaktorzerlegung

## Gleichungen {#equations}

### Quadratisch: ax^2 + bx + c = 0 {#quadratic-ax2-bx-c-0}
- Diskriminante D = b^2 - 4ac
- D > 0: zwei reelle Lösungen, D = 0: eine Lösung, D < 0: keine reelle Lösung
- x = (-b +/- sqrt(D)) / (2a)
- Satz von Vieta: x1 + x2 = -b/a, x1 * x2 = c/a

### Gleichungssysteme {#systems}
- **Substitution**: eine Gleichung nach einer Variablen auflösen und einsetzen
- **Elimination**: Gleichungen addieren oder subtrahieren
- Arten: eindeutig lösbar (sich schneidend), keine Lösung (parallel), unendlich viele Lösungen (identisch)

## Ungleichungen {#inequalities}

- Beim Multiplizieren oder Dividieren mit einer negativen Zahl: **Ungleichungszeichen umkehren**
- **Vorzeichenverfahren** für rationale Ungleichungen: Nullstellen bestimmen, Vorzeichen in jedem Intervall prüfen
- Quadratisch: Nullstellen bestimmen, Öffnungsrichtung der Parabel verwenden

## Elementare Funktionen {#elementary-functions}

| Funktion | Definitionsbereich | Wichtige Eigenschaft |
|----------|--------|-------------|
| Linear: y = kx + b | R | Konstante Änderungsrate |
| Quadratisch: y = ax^2 + bx + c | R | Scheitelpunkt bei x = -b/(2a) |
| Exponentiell: y = a^x | R | Immer positiv, monoton |
| Logarithmisch: y = log_a(x) | x > 0 | Umkehrfunktion der Exponentialfunktion |
| Trigonometrisch: sin, cos | R | Periode 2*pi, Wertebereich [-1, 1] |

**Logarithmusregeln**: log(ab) = log(a) + log(b), log(a^n) = n*log(a), log_a(x) = ln(x)/ln(a)

**Wichtige Identitäten**: sin^2 + cos^2 = 1, e^(i*theta) = cos(theta) + i*sin(theta)

### Graphentransformationen {#graph-transformations}
- f(x) + c: Verschiebung nach oben
- f(x - c): Verschiebung nach rechts
- c*f(x): vertikale Streckung
- f(cx): horizontale Stauchung

## Mengen {#sets}

- **Vereinigung** A ∪ B: in A ODER B
- **Schnitt** A ∩ B: in A UND B
- **Differenz** A \ B: in A, aber nicht in B
- **De Morgan**: (A ∪ B)^c = A^c ∩ B^c
- **Inklusion-Exklusion**: |A ∪ B| = |A| + |B| - |A ∩ B|
- **Potenzmenge**: |P(A)| = 2^|A|

## Kombinatorik {#combinatorics}

- **Permutationen** (Reihenfolge wichtig): P(n,k) = n!/(n-k)!
- **Kombinationen** (Reihenfolge egal): C(n,k) = n!/(k!(n-k)!)
- **Binomischer Lehrsatz**: (a+b)^n = Summe C(n,k) * a^(n-k) * b^k
- **Schubfachprinzip**: n Objekte in m Fächer, n > m -> mindestens ein Fach enthält mehr als 1

## Folgen {#sequences}

- **Arithmetisch**: a_n = a_1 + (n-1)d, S_n = n(a_1+a_n)/2
- **Geometrisch**: a_n = a_1 * r^(n-1), unendliche Summe (|r|<1): S = a_1/(1-r)
- **Zinseszins**: A = P(1+r)^n

## Siehe auch {#see-also}
- [[math-for-ml]] - die Analysis baut auf diesen Grundlagen auf
- [[math-linear-algebra]] - Vektoren und Matrizen
- [[probability-distributions]] - die Wahrscheinlichkeitsrechnung nutzt die Kombinatorik
