---
title: "Tableau-Diagrammtypen und Auswahl von Visualisierungen"
category: tools
tags: [bi-analytics, tableau, chart-types, visualization, encoding, anscombes-quartet]
level: 3
source_sha256: e82f1bf28306a74fa9e1a12e437e32c5b8d7920f71d472bcfcf2a69c99c837d8
translation: machine
translated_at: '2026-10-24'
---
# Tableau-Diagrammtypen und Auswahl von Visualisierungen {#tableau-chart-types-visualization-selection}

Die Wahl des richtigen Diagrammtyps ist eine zentrale BI-Kompetenz. Jede Visualisierung kodiert Datenattribute auf unterschiedliche Weise, und die Auswahl sollte sich an der konkreten Frage orientieren, die beantwortet werden soll. Anscombes Quartett zeigt, warum: Vier Datensätze mit identischen Kennzahlen erzeugen völlig unterschiedliche visuelle Muster.

## Kernfakten {#key-facts}

- Visualisierung = Menge von Kodierungsmethoden, die auf Daten abgebildet werden
- Für Präzision (exakte Werte): **Länge** und **Position auf Achsen** verwenden
- Für Unterscheidung (Gruppierung): **Farbe**, **Volumen**, **Größe** verwenden
- Regel: Zuerst verstehen, welche Frage der Nutzer stellt, dann das Diagramm wählen, das sie beantwortet
- Selbst erstellte Visualisierungen = interne Analyse (Jupyter, matplotlib); Vorgefertigte = Kommunikation an Nutzer (Dashboards, Präsentationen)

## Muster {#patterns}

### Attribute zur Datenkodierung {#data-encoding-attributes}

Die wichtigsten Kodierungsattribute, nach Präzision geordnet:
1. **Position auf gemeinsamer Skala** (am präzisesten)
2. **Länge**
3. **Winkel/Steigung**
4. **Fläche**
5. **Farbintensität**
6. **Farbton** (am wenigsten präzise für quantitative Daten)

### Leitfaden zur Auswahl des Diagrammtyps {#chart-type-selection-guide}

| Diagramm | Geeignet für | Hinweise |
|----------|--------------|----------|
| **Balken/Säulen** | Vergleiche zwischen Kategorien | Horizontale Balken bei langen Beschriftungen |
| **Linie** | Trends über die Zeit | Nur kontinuierliche Daten verbinden |
| **Kreis/Donut** | Anteil am Ganzen | Sparsam verwenden, maximal 5 Segmente |
| **Matrix/Pivot** | Kreuztabellierung | Wenn exakte Zahlen wichtig sind |
| **Card** | Einzelne KPI-Zahl | Kennzahlen im Dashboard-Kopf |
| **Tabelle** | Rohdaten in tabellarischer Form | Detail-Drilldown |
| **Treemap** | Hierarchischer Anteil am Ganzen mit Größe | Besser als Kreisdiagramm bei vielen Kategorien |
| **Karte/Flächenkarte** | Geografische Daten | Farbinterpolation prüfen |
| **Tachometer (Gauge)** | Fortschritt zu einem Ziel | Verfolgung eines einzelnen Zielwerts |
| **Streudiagramm** | Zusammenhang zwischen zwei Kennzahlen | Trendlinie zur Verdeutlichung hinzufügen |
| **Heatmap** | Musterdichte über zwei Dimensionen | Sequenzielle Farbskala |

### Visualisierungskategorien {#visualization-categories}

**Selbst erstellt (für interne Analyse):**
- Business Analytics: schnelle Datenexploration (Jupyter + matplotlib/seaborn)
- Wissenschaftliche Visualisierung: physikalische Prozesse, 3D
- Such- und Konzeptvisualisierung: Beziehungen und Prinzipien

**Vorgefertigt (zur Kommunikation an Nutzer):**
- Dashboards und Präsentationen: interaktive Panels zur Geschäftsleistung
- Entity Cards / persönliche Konten: bankähnliche Ansichten (KPI-Factoids + Sparklines)
- Werkzeuge zur Datenanalyse: Nutzer erkunden die Daten selbst über Interaktivität
- Infografiken und Journalismus: aufmerksamkeitsstark, gestalterisch aufwendig

### Sparklines und KPI-Factoids {#sparklines-and-kpi-factoids}

- **KPI-Factoid**: einzelne Zahl mit Beschriftung, zeigt den aktuellen Stand (z. B. „Umsatz 5,7 Mio. $")
- **Sparkline**: kleines eingebettetes Diagramm ohne Achsen, zeigt den Trend und steht neben dem Factoid
- Beide werden im oberen linken Bereich platziert, um maximale Aufmerksamkeit und schnelle Zustandsbewertung zu ermöglichen

### Dashboard-Aktionen (Interaktivität) {#dashboard-actions-interactivity}

| Aktion | Beschreibung |
|--------|--------------|
| **Filter** | Klick auf Element -> filtert andere Diagramme (am häufigsten) |
| **Hervorheben** | Klick -> hebt verwandte Daten hervor, ohne zu filtern |
| **Parameter** | Nutzeraktion -> ändert Parameterwert |
| **Set** | Nutzeraktion -> fügt Elemente zu einem Set hinzu bzw. entfernt sie |
| **GoToSheet** | Wechsel zu einem anderen Arbeitsblatt/Dashboard |
| **URL** | Öffnet URL mit dynamischen Parametern |

Beispiel für eine URL-Aktion:
```text
https://crm.example.com/deal?object=<object_number>
```

## Fallstricke {#gotchas}

- Anscombes Quartett: Daten immer visualisieren, bevor man zusammenfassenden Kennzahlen vertraut – vier Datensätze mit identischem Mittelwert, Varianz, Korrelation und Regressionsgerade sehen völlig unterschiedlich aus
- Kreisdiagramme mit mehr als 5 Segmenten werden unlesbar – stattdessen Balkendiagramm oder Treemap verwenden
- Große, bunte Objekte ziehen unabhängig von ihrer Position die Aufmerksamkeit auf sich (Kontrast überlagert das F-Muster des Lesens)
- Falsche Farbinterpolation in Heatmaps und Karten macht Diagramme irreführend – immer prüfen
- Jedes Arbeitsblatt erzeugt eine Abfrage an die Quelle – mehr Diagramme bedeuten mehr Abfragen und ein langsameres Dashboard

## Siehe auch {#see-also}

- [[dashboard-design-patterns]] - Layout, F-Muster, Gestalt-Prinzipien
- [[color-theory-visualization]] - Farbskalen und Barrierefreiheit
- [[tableau-calculations]] - berechnete Felder für Diagrammdaten
- [[powerbi-fundamentals]] - Visualisierungstypen in Power BI
