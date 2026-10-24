---
title: "Bayessche Methoden im maschinellen Lernen"
category: concepts
tags: [data-science, bayesian, naive-bayes, inference, prior]
level: 2
source_sha256: aad80d100fe194f4e5c2fe4aa8804d39301b5f14d6a04628d50e940313479779
translation: machine
translated_at: '2026-10-24'
---
# Bayessche Methoden im maschinellen Lernen {#bayesian-methods-in-ml}

Bayessches Denken aktualisiert Überzeugungen anhand von Evidenz. Von der einfachen Naive-Bayes-Klassifikation bis zur Bayesschen Inferenz liefern diese Methoden eine prinzipiengeleitete Quantifizierung von Unsicherheit.

## Angewandter Satz von Bayes {#bayes-theorem-applied}

P(Hypothese | Daten) = P(Daten | Hypothese) * P(Hypothese) / P(Daten)

- **Prior** P(Hypothese): was wir vor Betrachtung der Daten glauben
- **Likelihood** P(Daten | Hypothese): Wahrscheinlichkeit der Daten unter der Hypothese
- **Posterior** P(Hypothese | Daten): aktualisierte Überzeugung nach Betrachtung der Daten
- **Evidenz** P(Daten): Normierungskonstante

## Naive-Bayes-Klassifikator {#naive-bayes-classifier}

P(Klasse | Merkmale) proportional zu P(Klasse) * Produkt(P(Merkmal_i | Klasse))

Die „naive“ Annahme: Merkmale sind unter gegebener Klasse bedingt unabhängig. Sie wird häufig verletzt, funktioniert aber überraschend gut.

```python
from sklearn.naive_bayes import GaussianNB, MultinomialNB

# Gaussian: continuous features (assumes normal distribution)
gnb = GaussianNB()
gnb.fit(X_train, y_train)

# Multinomial: count features (great for text/TF-IDF)
mnb = MultinomialNB()
mnb.fit(X_train_tfidf, y_train)
```

**Am besten geeignet für**: Textklassifikation (Spam-Filterung, Sentimentanalyse), wenn die Trainingsdaten klein sind, wenn schnelles Training erforderlich ist.

### Warum es trotz falscher Annahme funktioniert {#why-it-works-despite-wrong-assumption}
- Die Klassifikation muss Wahrscheinlichkeiten nur korrekt ordnen, nicht präzise schätzen
- Abhängigkeiten zwischen Merkmalen heben sich über die Klassen hinweg oft auf
- Bei begrenzten Daten generalisieren einfachere Modelle besser

## Bayessch vs. frequentistisch {#bayesian-vs-frequentist}

| Aspekt | Frequentistisch | Bayessch |
|--------|-------------|----------|
| Parameter | Fest, unbekannt | Zufallsvariablen mit Verteilungen |
| Daten | Zufällig (wiederholte Stichprobenziehung) | Fest (beobachtet) |
| Inferenz | Punktschätzer + KI | Vollständige a-posteriori-Verteilung |
| Vorwissen | Nicht einbezogen | Explizit einbezogen |
| Unsicherheit | Konfidenzintervalle | Glaubwürdigkeitsintervalle |

## Bayessche Inferenz {#bayesian-inference}

Statt Punktschätzern wird die vollständige a-posteriori-Verteilung der Parameter berechnet.

**Konjugierte Priors**: Prior und Posterior gehören derselben Familie an.
- Normal-Likelihood + Normal-Prior -> Normal-Posterior
- Binomial-Likelihood + Beta-Prior -> Beta-Posterior

**MCMC (Markov-Chain-Monte-Carlo)**: Ziehen von Stichproben aus der Posterior-Verteilung, wenn keine analytische Lösung handhabbar ist.

## Anwendungen in der Datenwissenschaft {#applications-in-data-science}

- **A/B-Tests**: Bayessche A/B-Tests liefern die Wahrscheinlichkeit, dass B besser ist als A (anschaulicher als p-Werte)
- **Hyperparameter-Optimierung**: Bayessche Optimierung (Optuna, Hyperopt)
- **Spam-Filterung**: Naive Bayes mit Worthäufigkeiten
- **Medizinische Diagnose**: Prävalenz der Krankheit als Prior + Sensitivität des Tests
- **Empfehlungssysteme**: Bayessche Personalisierung

## Stolperfallen {#gotchas}
- Naive Bayes setzt Merkmalsunabhängigkeit voraus – Korrelationen zwischen Merkmalen verschlechtern die Leistung
- Die Wahl des Priors ist wichtig, insbesondere bei kleinen Datenmengen
- MCMC kann bei komplexen Modellen langsam konvergieren
- Berechnung im Log-Raum ist unverzichtbar, um numerischen Underflow zu vermeiden (Produkt vieler kleiner Wahrscheinlichkeiten)
- Multinomial-NB erfordert nicht-negative Merkmale (Zähler, TF-IDF)

## Siehe auch {#see-also}
- [[probability-distributions]] - Verteilungstheorie, auf der Bayes aufbaut
- [[nlp-text-processing]] - Naive Bayes zur Textklassifikation
- [[hypothesis-testing]] - Bayessche Alternative zum frequentistischen Testen
- [[math-probability-statistics]] - formale Grundlagen der Wahrscheinlichkeitsrechnung
