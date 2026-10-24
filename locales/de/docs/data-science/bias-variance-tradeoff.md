---
title: "Bias-Varianz-Tradeoff"
category: concepts
tags: [data-science, ml, overfitting, underfitting, regularization]
level: 2
source_sha256: ddbccf5644bf36c42536dd73071a9f6ea9a2a84be21744ec265ef67d8a40fa39
translation: machine
translated_at: '2026-10-24'
---
# Bias-Varianz-Tradeoff {#bias-variance-tradeoff}

Die grundlegende Spannung im maschinellen Lernen: Modelle, die zu einfach sind, übersehen Muster (Bias), Modelle, die zu komplex sind, merken sich Rauschen auf (Varianz). Jede Modellierungsentscheidung ist ein Punkt auf diesem Spektrum.

## Definitionen {#definitions}

**Bias** = systematischer Fehler. Wie weit die Vorhersagen im Durchschnitt von den wahren Werten abweichen.
- Hoher Bias = Underfitting (Modell zu einfach, übersieht Muster)
- Beispiel: Lineare Regression an quadratische Daten anpassen

**Varianz** = wie stark die Vorhersagen über verschiedene Trainingsmengen hinweg schwanken.
- Hohe Varianz = Overfitting (Modell erfasst Rauschen statt Signal)
- Beispiel: Polynom vom Grad 10 auf 20 Datenpunkten

**Gesamtfehler = Bias^2 + Varianz + irreduzibles Rauschen**

## Diagnose {#diagnosis}

| Symptom | Diagnose | Lösung |
|---------|-----------|----------|
| Hoher Trainingsfehler, hoher Validierungsfehler | Underfitting (hoher Bias) | Komplexeres Modell, mehr Features |
| Niedriger Trainingsfehler, hoher Validierungsfehler | Overfitting (hohe Varianz) | Regularisierung, mehr Daten, einfacheres Modell |
| Niedriger Trainingsfehler, niedriger Validierungsfehler | Guter Fit | Ausliefern |
| Hoher Trainingsfehler, niedriger Validierungsfehler | Unmöglich (Data Leakage?) | Auf Fehler prüfen |

**Lernkurven**: Trainings- und Validierungsfehler gegen die Größe der Trainingsmenge auftragen.
- Konvergieren auf hohem Fehlerniveau -> Bias-Problem (mehr Daten helfen nicht, es braucht ein besseres Modell)
- Große Lücke -> Varianz-Problem (mehr Daten werden helfen)

## Spektrum der Modellkomplexität {#model-complexity-spectrum}

Geringe Komplexität <---------> Hohe Komplexität
Lineare Regression --- Polynom --- Entscheidungsbaum --- Deep Forest --- Neuronales Netz

Geringer Bias, hohe Varianz <--> Hoher Bias, geringe Varianz

## Umgang mit dem Tradeoff {#managing-the-tradeoff}

### Varianz reduzieren (Overfitting bekämpfen) {#reduce-variance-fight-overfitting}
- **Regularisierung**: L1/L2-Strafterme auf Modellgewichte
- **Dropout**: Neuronen während des Trainings zufällig auf null setzen
- **Early Stopping**: Training beenden, sobald der Validierungsverlust steigt
- **Kreuzvalidierung**: robuste Schätzung der Leistung
- **Mehr Trainingsdaten**: beste Gegenmaßnahme gegen Overfitting
- **Ensemble-Methoden**: Mittelung reduziert Varianz (Random Forest, Bagging)
- **Feature-Selektion**: verrauschte/irrelevante Features entfernen
- **Einfacheres Modell**: weniger Parameter, flachere Bäume

### Bias reduzieren (Underfitting bekämpfen) {#reduce-bias-fight-underfitting}
- **Komplexeres Modell**: tiefere Bäume, mehr Schichten
- **Mehr/bessere Features**: Feature Engineering
- **Weniger Regularisierung**: Strafterm reduzieren
- **Ensemble-Methoden**: Boosting reduziert Bias (Gradient Boosting, AdaBoost)
- **Länger trainieren**: mehr Epochen/Iterationen

## Ensemble-Methoden und der Tradeoff {#ensemble-methods-and-the-tradeoff}

- **Bagging** (Random Forest): trainiert mehrere Modelle unabhängig voneinander und mittelt sie. Reduziert VARIANZ
- **Boosting** (Gradient Boosting): trainiert Modelle sequentiell, wobei jedes die Fehler der vorherigen korrigiert. Reduziert BIAS

Deshalb ist Gradient Boosting (reduziert Bias) in Kombination mit Regularisierung (kontrolliert Varianz) so leistungsstark.

## Stolperfallen {#gotchas}
- „Mehr Daten" hilft gegen Varianz, aber NICHT gegen Bias – ist das Modell zu einfach, behebt mehr Daten das nicht
- Regularisierung ist NICHT kostenlos – zu viel Regularisierung erhöht den Bias
- Overfitting auf die Validierungsmenge ist real – starkes Hyperparameter-Tuning auf derselben Validierungsmenge
- Neuronale Netze stellen den klassischen Tradeoff infrage – sehr große Modelle können gut generalisieren (Double-Descent-Phänomen)
- Kreuzvalidierung liefert eine bessere Schätzung als ein einzelner Split, ist aber langsamer

## Siehe auch {#see-also}
- [[model-evaluation]] - Erkennen von Overfitting
- [[feature-engineering]] - Regularisierungstechniken
- [[gradient-boosting]] - praktisches Bias-Varianz-Management
- [[neural-networks]] - Regularisierung im Deep Learning
