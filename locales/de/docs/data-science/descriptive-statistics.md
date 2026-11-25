---
title: "Deskriptive Statistik"
category: concepts
tags: [data-science, statistics, eda, fundamentals]
level: 3
source_sha256: c599a5c2ccb7f7478ce8b8464bb53c59aba3f7f45f3c0d9514131b6a8d023afd
translation: machine
translated_at: '2026-10-24'
---
# Deskriptive Statistik {#descriptive-statistics}

Quantitative Zusammenfassungen von Datenverteilungen. Die Grundlage der EDA: Berechne diese immer vor der Modellierung. Das Verständnis von zentraler Tendenz, Streuung und Form zeigt dir, welche Modelle und Vorverarbeitungsschritte geeignet sind.

## Maße der zentralen Tendenz {#measures-of-central-tendency}

- **Mittelwert (Mean)**: Summe / Anzahl. Empfindlich gegenüber Ausreißern. `df['col'].mean()`
- **Median**: mittlerer Wert bei sortierten Daten. Robust gegenüber Ausreißern. `df['col'].median()`
- **Modus (Mode)**: häufigster Wert. Kann multimodal sein. `df['col'].mode()`

**Mittelwert vs. Median zeigt die Schiefe:**
- Mittelwert > Median: rechtsschief (wenige hohe Werte ziehen den Mittelwert nach oben), z. B. Einkommensverteilungen
- Mittelwert < Median: linksschief (wenige niedrige Werte ziehen den Mittelwert nach unten), z. B. Prüfungsergebnisse
- Mittelwert ~ Median: annähernd symmetrisch

## Maße der Streuung {#measures-of-spread}

```python
import numpy as np
from scipy import stats

salary_range = df['income'].max() - df['income'].min()  # range
salary_var = df['income'].var()                          # variance
salary_std = df['income'].std()                          # standard deviation
iqr = df['income'].quantile(0.75) - df['income'].quantile(0.25)  # IQR
```

- **Spannweite (Range)**: max - min. Einfach, aber extrem empfindlich gegenüber Ausreißern
- **Varianz**: mittlere quadrierte Abweichung vom Mittelwert. Die Einheiten sind quadriert
- **Standardabweichung**: sqrt(Varianz). Gleiche Einheiten wie die Daten, dadurch leichter zu interpretieren
- **IQR** (Interquartilsabstand): Q3 - Q1. Robustes Streuungsmaß, das zur Ausreißererkennung verwendet wird

## Maße der Form {#measures-of-shape}

**Schiefe (Skewness)**: Asymmetrie der Verteilung:
```python
skewness = stats.skew(df['income'])
# > 0: right-skewed (long right tail)
# < 0: left-skewed (long left tail)
# ~ 0: symmetric
```

**Wölbung (Kurtosis)**: Schwere der Ränder relativ zur Normalverteilung:
```python
kurtosis = stats.kurtosis(df['income'])
# > 0 (leptokurtic): heavy tails, sharp peak - more extreme values
# < 0 (platykurtic): light tails, flat peak
# ~ 0 (mesokurtic): similar to normal
```

**Warum die Form wichtig ist**: Sie leitet die Vorverarbeitung (Log-Transformation für schiefe Merkmale), die Ausreißererkennung (leptokurtisch = mehr Extremwerte) und die Modellauswahl (lineare Modelle setzen annähernd normalverteilte Residuen voraus).

## Lagemaße {#measures-of-position}

```python
# Percentiles
p25, p50, p75 = np.percentile(df['income'], [25, 50, 75])

# Quartiles via describe()
df['income'].describe()
# count, mean, std, min, 25%, 50%, 75%, max
```

## Z-Werte {#z-scores}

Z = (X - mu) / sigma. Anzahl der Standardabweichungen vom Mittelwert.

```python
z_scores = stats.zscore(df['income'])
# |z| > 2: unusual (5% of normal data)
# |z| > 3: extreme outlier (0.3% of normal data)
```

**68-95-99,7-Regel** (empirische Regel für Normalverteilungen):
- ca. 68 % der Daten liegen innerhalb von 1 Standardabweichung vom Mittelwert
- ca. 95 % innerhalb von 2 Standardabweichungen
- ca. 99,7 % innerhalb von 3 Standardabweichungen

## Korrelation {#correlation}

Misst Stärke und Richtung des Zusammenhangs zwischen zwei Variablen. Wertebereich: [-1, +1].

```python
# Pearson - linear relationships, assumes normality
pearson_r = df['income'].corr(df['experience'])

# Full correlation matrix
corr_matrix = df.corr()

# Spearman - monotonic (not just linear), rank-based, no normality assumption
spearman_r = df['income'].corr(df['experience'], method='spearman')

# Kendall - concordant/discordant pairs, robust to outliers, good for small samples
kendall_tau = df['income'].corr(df['experience'], method='kendall')
```

| Methode | Misst | Annahmen | Verwenden, wenn |
|---------|-------|----------|-----------------|
| Pearson | Lineare Beziehung | Normalverteilung, Homoskedastizität | Beide stetig, annähernd normalverteilt |
| Spearman | Monotone Beziehung | Keine (rangbasiert) | Ordinale Daten, nicht-lineare monotone Beziehung |
| Kendall | Konkordanz | Keine (rangbasiert) | Kleine Stichproben, ordinale Daten |

**Korrelation impliziert keine Kausalität.** Eisverkäufe korrelieren mit Ertrinkungsfällen (Störvariable: heißes Wetter).

## Stichprobe vs. Grundgesamtheit {#sample-vs-population}

- **Grundgesamtheit** (mu, sigma): gesamte interessierende Menge. Selten vollständig beobachtbar
- **Stichprobe** (x_bar, s): Teilmenge, die zur Schätzung der Parameter der Grundgesamtheit verwendet wird
- Größere Stichprobe = Stichprobenkennwerte liegen näher an den Parametern der Grundgesamtheit

## Fallstricke {#gotchas}
- Verwendung des Mittelwerts bei stark schiefen Daten, ohne den Median anzugeben
- Pearson-Korrelation = 0 bedeutet NICHT, dass kein Zusammenhang besteht (er könnte nicht-linear sein)
- Die Spannweite ist beim Vergleich von Verteilungen nahezu nutzlos (sie wird von einzelnen Ausreißern dominiert)
- `df.describe()` zeigt standardmäßig nur numerische Spalten. Verwende `include='all'` oder `include='object'`

## Siehe auch {#see-also}
- [[probability-distributions]] - theoretische Verteilungen, die den Daten zugrunde liegen
- [[pandas-eda]] - Berechnung dieser Statistiken in pandas
- [[data-visualization]] - Visualisierung von Verteilungen
- [[hypothesis-testing]] - Prüfung, ob beobachtete Unterschiede signifikant sind
