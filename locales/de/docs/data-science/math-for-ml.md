---
title: "Mathematik für maschinelles Lernen"
category: foundations
tags: [data-science, math, calculus, optimization, gradient]
level: 3
source_sha256: 425e14aec93d37680ce5610a8704e348d5b167df4ea4a1b74fec5ce3bb3278d1
translation: machine
translated_at: '2026-10-24'
---
# Mathematik für maschinelles Lernen {#mathematics-for-machine-learning}

Die grundlegende Mathematik hinter ML-Algorithmen. Der Fokus liegt darauf, zu verstehen, WARUM Algorithmen funktionieren, und nicht nur darauf, wie man sie aufruft.

## Analysis für ML {#calculus-for-ml}

### Ableitungen {#derivatives}

f'(x) = lim(h->0) [f(x+h) - f(x)] / h. Änderungsrate. Steigung der Tangente.

**Wichtige Regeln:**
- Potenzregel: (x^n)' = n*x^(n-1)
- Kettenregel: (f(g(x)))' = f'(g(x)) * g'(x)
- Produktregel: (fg)' = f'g + fg'
- e^x: (e^x)' = e^x
- ln(x): (ln(x))' = 1/x

### Partielle Ableitungen und Gradient {#partial-derivatives-and-gradient}

Für f(x1, ..., xn): Gradient = Vektor der partiellen Ableitungen.

nabla f = [df/dx1, df/dx2, ..., df/dxn]

**Der Gradient zeigt in Richtung des steilsten Anstiegs.** Der Gradientenabstieg bewegt sich in die entgegengesetzte Richtung: w -= lr * nabla_f.

### Kritische Punkte und Optimierung {#critical-points-and-optimization}

- Kritischer Punkt: Gradient = 0
- Test mit der zweiten Ableitung: f''(x) > 0 -> Minimum, f''(x) < 0 -> Maximum
- **Hesse-Matrix**: zweite partielle Ableitungen. Die Eigenwerte bestimmen die Art des kritischen Punktes
- **Konvexe Funktionen**: Jedes lokale Minimum ist ein globales Minimum. Der MSE ist für lineare Regression konvex

### Backpropagation {#backpropagation}

Kettenregel durch den Berechnungsgraphen. Für die Ausgabe einer Schicht = sigma(Wx + b):
```text
d(Loss)/dW = d(Loss)/d(output) * d(output)/d(Wx+b) * d(Wx+b)/dW
```

Berechnungsgraph und automatische Differentiation machen dies für tiefe Netze handhabbar.

### Taylor-Reihe {#taylor-series}

f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)^2/2! + ...

Wichtige Entwicklungen: e^x = 1 + x + x^2/2! + ..., ln(1+x) = x - x^2/2 + ...

In ML: Verständnis des Verlustverhaltens in der Nähe von Optima, Newton-Verfahren (Approximation zweiter Ordnung).

## Optimierung {#optimization}

### Gradientenabstieg {#gradient-descent}

w_(t+1) = w_t - alpha * nabla f(w_t)

- **Lernrate** alpha: zu groß -> Divergenz, zu klein -> langsam
- **Stochastischer GD**: Gradient aus einem einzelnen Sample (verrauscht, aber schnell)
- **Mini-Batch-GD**: kleiner Batch (Kompromiss)
- **Momentum**: v_t = beta*v_(t-1) + nabla f. Beschleunigt das Durchqueren schmaler Täler
- **Konvergenz**: O(1/t) für konvexe Funktionen mit Lipschitz-stetigem Gradienten

### Newton-Verfahren {#newtons-method}

w_new = w_old - H^(-1) * gradient. Nutzt zweite Ableitungen (Hesse-Matrix). Konvergiert schneller, aber H^(-1) ist teuer.

**Quasi-Newton** (L-BFGS): Approximation der inversen Hesse-Matrix mit geringem Aufwand.

### Lagrange-Multiplikatoren {#lagrange-multipliers}

Optimiere f(x) unter der Nebenbedingung g(x) = 0: nabla f = lambda * nabla g.

In ML: SVM-Optimierung (Maximierung des Margins unter Nebenbedingungen).

## Log-Sum-Exp-Trick {#log-sum-exp-trick}

Numerischen Überlauf in Softmax/Log-Likelihood vermeiden:
```sql
log(sum(exp(x_i))) = c + log(sum(exp(x_i - c)))  where c = max(x_i)
```

## Integration in ML {#integration-in-ml}

- Berechnung von Erwartungswerten und Wahrscheinlichkeiten (Fläche unter der PDF)
- Normierungskonstanten für Verteilungen
- KL-Divergenz zwischen Verteilungen
- Lebesgue-Integral: Grundlage der modernen Wahrscheinlichkeitstheorie

## Fallstricke {#gotchas}
- Gradientenabstieg auf nicht-konvexen Funktionen (neuronale Netze) findet lokale Minima, nicht das globale - das ist meist unproblematisch
- Numerische Stabilität ist wichtig: für Produkte von Wahrscheinlichkeiten den Log-Raum verwenden
- Die Berechnung der Hesse-Matrix ist O(n^2) in den Parametern - für große Modelle nicht praktikabel
- Fehler in der Kettenregel pflanzen sich fort - Gradienten immer numerisch überprüfen

## Siehe auch {#see-also}
- [[math-linear-algebra]] - Vektoren, Matrizen, Eigenwerte
- [[linear-models]] - direkte Anwendung der Analysis auf ML
- [[neural-networks]] - Backpropagation nutzt die Kettenregel
- [[probability-distributions]] - Integration für Erwartungswerte
