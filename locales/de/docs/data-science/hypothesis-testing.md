---
title: "Hypothesentests und A/B-Tests"
category: concepts
tags: [data-science, statistics, ab-testing, experimentation]
level: 3
source_sha256: 1a9579c045ca3d920c02a38003c9387cad49f269ecdbfbc05010f7515334fb96
translation: machine
translated_at: '2026-10-24'
---
# Hypothesentests und A/B-Tests {#hypothesis-testing-and-ab-testing}

Statistisches Framework für datenbasierte Entscheidungen. A/B-Tests wenden diese Prinzipien auf kontrollierte Experimente an. Eine zentrale Fähigkeit für Data Scientists, die echte Effekte von Zufallsschwankungen unterscheiden müssen.

## Framework für Hypothesentests {#hypothesis-testing-framework}

1. **Hypothesen formulieren**: H0 (Nullhypothese, kein Effekt) und H1 (Alternativhypothese, es gibt einen Effekt)
2. **Signifikanzniveau wählen** alpha (typischerweise 0,05)
3. **Teststatistik berechnen** aus den Daten
4. **p-Wert berechnen** oder mit dem kritischen Wert vergleichen
5. **Entscheidung**: H0 verwerfen, wenn p-Wert < alpha

### Fehlerarten {#error-types}

| | H0 wahr | H0 falsch |
|--|---------|----------|
| **H0 verwerfen** | Typ I (alpha) | Korrekt |
| **H0 nicht verwerfen** | Korrekt | Typ II (beta) |

- **Typ I** (falsch positiv): Ein Effekt wird behauptet, obwohl keiner existiert. Wird durch alpha kontrolliert
- **Typ II** (falsch negativ): Ein realer Effekt wird übersehen. Power = 1 - beta
- **p-Wert**: Wahrscheinlichkeit, Daten zu beobachten, die mindestens so extrem sind wie unsere, unter der Annahme, dass H0 wahr ist

### Gängige Tests {#common-tests}

| Test | Anwendungsfall | Annahmen |
|------|----------------|----------|
| t-Test (Student) | Mittelwerte zweier Gruppen vergleichen | ~normalverteilt, ähnliche Varianz |
| Welch-t-Test | Mittelwerte vergleichen, ungleiche Varianz | ~normalverteilt |
| Mann-Whitney-U | Verteilungen nichtparametrisch vergleichen | Ordinal oder höher |
| z-Test für Anteile | Binäre Anteile vergleichen | Großes n |
| Chi-Quadrat | Unabhängigkeit kategorialer Merkmale prüfen | Erwartete Häufigkeit >= 5 |
| ANOVA | Mittelwerte von 3 oder mehr Gruppen vergleichen | Normalverteilt, gleiche Varianz |

### Konfidenzintervalle {#confidence-intervals}

```python
from scipy import stats
import numpy as np

data = np.array([...])
confidence = 0.95
n = len(data)
mean = data.mean()
se = stats.sem(data)  # standard error
ci = stats.t.interval(confidence, df=n-1, loc=mean, scale=se)
```

Für den Mittelwert bei bekannter Varianz: x_bar +/- z_(alpha/2) * sigma / sqrt(n)
Für den Mittelwert bei unbekannter Varianz: x_bar +/- t_(alpha/2, n-1) * s / sqrt(n)

## A/B-Tests {#ab-testing}

Zwei Versionen (A = Kontrolle, B = Test) werden auf unabhängigen Nutzergruppen verglichen. Gemessen werden Geschäftsmetriken.

### Warum nicht nur Offline-Metriken? {#why-not-just-offline-metrics}

Offline-Modellmetriken (Precision, NDCG) messen die geschäftliche Wirkung nicht direkt. Unternehmen interessieren sich für Sitzungsdauer, Klicks, Conversions, Retention und Umsatz. A/B-Tests verbinden Modelländerungen mit dem tatsächlichen Nutzerverhalten.

### Versuchsdesign {#experimental-design}

1. **Nutzer aufteilen** in Kontroll- und Testgruppe (hashbasiert: `hash(user_id + salt) % 100`)
2. **Über einen festen Zeitraum laufen lassen** (nicht vorzeitig hineinschauen und abbrechen)
3. **Metriken vergleichen** zwischen den Gruppen
4. **Statistische Tests anwenden** auf Signifikanz

### Power des Tests {#test-power}

Power = Wahrscheinlichkeit, einen realen Effekt zu erkennen. Beeinflusst durch:
- **Stichprobengröße**: mehr Nutzer = mehr Power (wichtigster Hebel)
- **Effektgröße**: größere Effekte sind leichter zu erkennen
- **Varianz**: geringere Varianz = mehr Power (CUPED verwenden)
- **Signifikanzniveau**: höheres alpha = mehr Power, aber mehr falsch positive Ergebnisse

### CUPED (Controlled-experiment Using Pre-Experiment Data) {#cuped-controlled-experiment-using-pre-experiment-data}

Reduziert die Varianz einer Metrik um 20 bis 30 % mithilfe von Daten aus der Zeit vor dem Experiment.

```toml
Y_cuped = Y - theta * X
theta* = cov(Y, X) / Var(X)
Var(Y_cuped) = Var(Y) * (1 - rho^2(Y, X))
```

Je höher die Korrelation zwischen der Metrik vor und während des Experiments, desto stärker die Varianzreduktion.

### CTR messen {#measuring-ctr}

CTR = Klicks / Aufrufe. Problem: Einzelne Klicks sind nicht unabhängig (ein Nutzer erzeugt mehrere).

**Lösungen:**
- **Aggregation pro Nutzer**: Klicks je Nutzer aggregieren, dann t-Test
- **Bootstrap**: Nutzer mit Zurücklegen resampeln, CTR pro Stichprobe berechnen
- **Bucketing**: Nutzer in ca. 100 Buckets hashen, CTR pro Bucket berechnen, t-Test auf den Buckets
- **Linearisierung**: LinearizedCTR = clicks - A * views (A = globale CTR aus der Kontrollgruppe)

### Bedrohungen der Validität {#threats-to-validity}

- **Neuheitseffekt**: Neue Nutzer reagieren überschwänglich positiv. Blässt die Ergebnisse auf
- **Veränderungsaversion**: Erfahrene Nutzer wehren sich gegen Änderungen. Erhöht die falsch negativen Ergebnisse
- **Erkennung**: Effekt zwischen neuen und erfahrenen Nutzern vergleichen
- **SRM** (Sample Ratio Mismatch): Gruppen sind nicht gleich groß, ein Hinweis auf fehlerhafte Randomisierung

### Wann A/B-Tests nicht möglich sind {#when-ab-tests-are-impossible}

- **Zweiseitige Marktplätze** (Taxi, Lieferdienste): Die Änderung einer Seite wirkt sich auf die andere aus
- **Sichtbare Features**: Nutzer in unterschiedlichen Gruppen sehen das Erlebnis der anderen
- **Feature bereits live**: Ein umgekehrter Test ist nicht möglich

**Alternativen:**
- **Switchback-Testing**: Algorithmen über Geografie x Zeitfenster abwechselnd einsetzen
- **Synthetic Control**: Überall ausrollen, mit einer aus Kontrollregionen prognostizierten Baseline vergleichen
- **Difference-in-Differences**: Behandlungs- und Kontrollgruppe vor und nach der Intervention vergleichen
- **Propensity Score Matching**: Behandelte Einheiten mit ähnlichen Kontrolleinheiten paaren

## Methoden der kausalen Inferenz {#causal-inference-methods}

| Methode | Stärke | Wann einsetzen |
|---------|--------|----------------|
| Randomisierter A/B-Test | Goldstandard | Volle Kontrolle über die Zuweisung |
| DiD | Mittel | Keine Randomisierung möglich, Daten vor und nach der Intervention vorhanden |
| PSM | Mittel | Keine Randomisierung möglich, Kovariaten vorhanden |
| Synthetic Control | Schwach | Keine Aufteilung möglich, Kontrollregionen vorhanden |

## Stolperfallen {#gotchas}
- **Peeking-Problem**: Ergebnisse täglich prüfen und bei Signifikanz abbrechen erhöht die falsch positive Rate. Wenn man trotzdem zwischendurch schaut, sequenzielle Tests (SPRT) verwenden
- **Multiple Vergleiche**: 20 Metriken bei alpha=0,05 testen bedeutet, dass etwa eine zufällig "signifikant" wird. Bonferroni-Korrektur anwenden
- **P-Hacking**: So lange verschiedene Analysen probieren, bis eine signifikant ist. Analyseplan vorab registrieren
- **Genauigkeitsfalle bei A/B-Tests**: Eine Steigerung der CTR um 1 % kann Millionen wert sein. Kleine, aber signifikante Effekte nicht abtun
- **Ergebnisse nicht horten**: Saisonalität bedeutet, dass die Ergebnisse des letzten Quartals möglicherweise nicht übertragbar sind

## Siehe auch {#see-also}
- [[probability-distributions]] - zugrunde liegende Theorie
- [[descriptive-statistics]] - Daten vor dem Testen zusammenfassen
- [[bi-dashboards]] - Präsentation von Experimentergebnissen
- [[model-evaluation]] - Offline-Metriken, die A/B-Tests ergänzen
