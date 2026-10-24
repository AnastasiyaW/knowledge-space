---
title: "Wahrscheinlichkeitstheorie und statistische Inferenz"
category: foundations
tags: [data-science, math, probability, statistics, estimation, mle]
level: 4
source_sha256: 08eafc9585ce02b38613df2e15e24d75277e3f148e5453270d88e74b6bf821ca
translation: machine
translated_at: '2026-10-24'
---
# Wahrscheinlichkeitstheorie und statistische Inferenz {#probability-theory-and-statistical-inference}

Fundierte Grundlagen der Wahrscheinlichkeitstheorie und statistische Schätzverfahren. Schließt die Lücke zwischen mathematischer Theorie und der praktischen Statistik, wie sie im ML verwendet wird.

## Wahrscheinlichkeitsaxiome {#probability-axioms}

1. P(A) >= 0 für jedes Ereignis A
2. P(Ergebnisraum) = 1
3. Für paarweise disjunkte Ereignisse: P(A1 oder A2 oder ...) = Summe P(Ai)

## Zentrale Sätze {#key-theorems}

### Schwaches Gesetz der großen Zahlen {#law-of-large-numbers-weak}
Das Stichprobenmittel konvergiert in Wahrscheinlichkeit gegen den Erwartungswert der Grundgesamtheit für n -> inf. Es rechtfertigt, Stichprobenkennzahlen zur Schätzung von Grundgesamtheitsparametern zu verwenden.

### Zentraler Grenzwertsatz {#central-limit-theorem}
Für u.i.v. Zufallsvariablen mit Mittelwert mu und Varianz sigma^2:
(X_bar - mu) / (sigma / sqrt(n)) -> N(0,1) für n -> inf

Unabhängig von der ursprünglichen Verteilung. Deshalb taucht die Normalverteilung überall auf.

### Tschebyschow-Ungleichung {#chebyshevs-inequality}
P(|X - mu| >= k*sigma) <= 1/k^2 für JEDE Verteilung
- k=2: höchstens 25 % der Daten jenseits von 2 sigma (empirisch: ~5 % bei Normalverteilung)
- k=3: höchstens 11 % jenseits von 3 sigma (empirisch: ~0,3 % bei Normalverteilung)

## Statistische Schätzung {#statistical-estimation}

### Eigenschaften von Punktschätzern {#point-estimation-properties}
- **Erwartungstreu (unbiased)**: E[theta_hat] = theta (im Mittel korrekt)
- **Konsistent**: theta_hat -> theta für n -> inf (konvergiert gegen den wahren Wert)
- **Effizient**: erreicht die minimale Varianz (Cramér-Rao-Schranke)
- **Suffizient**: erfasst die gesamte Information über theta aus der Stichprobe

### Maximum-Likelihood-Schätzung (MLE) {#maximum-likelihood-estimation-mle}

Bestimme die Parameter, welche die Likelihood der beobachteten Daten maximieren.

L(theta) = Produkt f(x_i | theta)

In der Praxis maximiert man die Log-Likelihood: l(theta) = Summe log f(x_i | theta)

**Eigenschaften**: Der MLE ist asymptotisch effizient, konsistent und asymptotisch normalverteilt.

**Beispiel (Normalverteilung)**: MLE für mu ist das Stichprobenmittel, MLE für sigma^2 ist die Stichprobenvarianz (verzerrt um den Faktor n/(n-1)).

### Momentenmethode {#method-of-moments}
Setze Stichprobenmomente den theoretischen Momenten gleich. Einfacher als MLE, aber oft weniger effizient.

## Hypothesentests (Theorie) {#hypothesis-testing-theory}

### Ablauf {#framework}
1. H0 (Nullhypothese) und H1 (Alternativhypothese)
2. Wähle alpha (Signifikanzniveau, typischerweise 0,05)
3. Berechne die Teststatistik
4. Vergleiche mit dem kritischen Wert oder berechne den p-Wert
5. Verwirf H0, wenn der p-Wert < alpha ist

### Fehlerarten {#error-types}
- **Fehler 1. Art** (alpha): Verwerfen einer wahren H0 (falsch positiv)
- **Fehler 2. Art** (beta): Nicht-Verwerfen einer falschen H0 (falsch negativ)
- **Power** = 1 - beta (Wahrscheinlichkeit, einen realen Effekt zu erkennen)

### Konfidenzintervalle {#confidence-intervals}
- Bekannte Varianz: x_bar +/- z_(alpha/2) * sigma / sqrt(n)
- Unbekannte Varianz: x_bar +/- t_(alpha/2, n-1) * s / sqrt(n)

Die t-Verteilung nach Student hat schwerere Ränder als die Normalverteilung. Sie wird bei kleinen Stichproben oder unbekannter Varianz der Grundgesamtheit verwendet.

## Konvergenzarten {#convergence-types}

Von schwächster zu stärkster:
1. **In Verteilung**: Verteilungsfunktionen konvergieren
2. **In Wahrscheinlichkeit**: P(|X_n - X| > epsilon) -> 0
3. **Fast sicher**: P(lim X_n = X) = 1
4. **Im Mittel (L^p)**: E[|X_n - X|^p] -> 0

## Asymptotische Analyse {#asymptotic-analysis}

- f = o(g): f wächst strikt langsamer. lim f/g = 0
- f = O(g): f wächst höchstens proportional (bis auf eine Konstante)
- f ~ g: asymptotisch äquivalent. lim f/g = 1
- Hierarchie: ln(n) << n^a << a^n << n! << n^n

## Bedingter Erwartungswert und bedingte Varianz {#conditional-expectation-and-variance}

- E[X] = E[E[X|Y]] (Satz vom iterierten Erwartungswert)
- Var(X) = E[Var(X|Y)] + Var(E[X|Y]) (Varianzzerlegung)

Nützlich bei: Bayes-Analyse, Mischmodellen, hierarchischen Modellen.

## Fallstricke {#gotchas}
- Der MLE der Varianz ist verzerrt (Division durch n, nicht n-1). Die Stichprobenvarianz verwendet n-1 (Bessel-Korrektur)
- Der ZGWS setzt endliche Varianz voraus und versagt bei der Cauchy-Verteilung und anderen Verteilungen mit schweren Rändern
- Der p-Wert ist NICHT die Wahrscheinlichkeit, dass H0 wahr ist. Er ist P(Daten | H0)
- Konfidenzintervall: "95 % der auf diese Weise konstruierten Intervalle enthalten den wahren Parameter" (frequentistische Interpretation)
- Statistische Signifikanz != praktische Relevanz. Ein winziger Effekt kann bei großem n statistisch signifikant sein

## Siehe auch {#see-also}
- [[probability-distributions]] - spezifische Verteilungen
- [[hypothesis-testing]] - praktische A/B-Tests
- [[descriptive-statistics]] - Stichprobenkennzahlen
- [[math-for-ml]] - Analysis für Optimierung
