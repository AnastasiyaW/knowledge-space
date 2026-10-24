---
title: "Tableau-LOD-Ausdrücke"
category: tools
tags: [bi-analytics, tableau, lod, fixed, include, exclude, level-of-detail]
level: 3
source_sha256: 6519159ce39d66df75b9560b6a0f8efa685339c5488cc81b627068c9fc40dfc4
translation: machine
translated_at: '2026-10-24'
---
# Tableau-LOD-Ausdrücke {#tableau-lod-expressions}

Level-of-Detail-(LOD-)Ausdrücke berechnen Aggregationen auf einer anderen Granularität als der, die in der aktuellen Ansicht dargestellt wird. Sie erzeugen Unterabfragen, die unabhängig vom Ansichtskontext sind, und ermöglichen so granularitätsübergreifende Analysen ohne komplexe Umwege.

## Kernfakten {#key-facts}

- Drei LOD-Typen: FIXED, INCLUDE, EXCLUDE
- LOD erzeugt Unterabfragen, die unabhängig von der aktuellen Ansicht sind
- FIXED ignoriert die Ansicht vollständig; INCLUDE fügt Granularität hinzu; EXCLUDE entfernt Granularität
- FIXED-LOD wird auf der Ebene der Kontextfilter ausgewertet (Schritt 4 in der Filterreihenfolge)
- INCLUDE/EXCLUDE-LOD werden auf der Ebene der Dimensionsfilter ausgewertet (Schritt 5)
- LOD innerhalb komplexer verschachtelter Berechnungen verursacht Performance-Probleme (zusätzliche JOINs)

## Muster {#patterns}

### FIXED-LOD {#fixed-lod}

Berechnet auf den angegebenen Dimension(en) und ignoriert die Ansicht vollständig:

```sql
{FIXED [Customer ID] : SUM([Sales])}
-- Total sales per customer, regardless of view

{FIXED [Region], [Year] : AVG([Revenue])}
-- Average revenue per region per year

{FIXED [User ID] : MIN([Event Date])}
-- First event date per user (for cohort analysis)
```

Anwendungsfälle: Kohortenanalyse, Customer Lifetime Value, Ermittlung des ersten/letzten Kaufdatums, Summen pro Entität, die in beliebigem Ansichtskontext angezeigt werden.

### INCLUDE-LOD {#include-lod}

Berechnet auf einer feineren Granularität als die Ansicht (fügt Dimensionen hinzu):

```sql
{INCLUDE [Order ID] : SUM([Quantity])}
-- Per-order sum while viewing by month
```

Die Ansicht zeigt möglicherweise monatliche Aggregate, doch INCLUDE berechnet zunächst auf Bestellebene und aggregiert anschließend nach oben.

**Performance-Hinweis**: INCLUDE fügt 2 JOINs hinzu, wenn es in einer komplexen Berechnung verwendet wird.

### EXCLUDE-LOD {#exclude-lod}

Berechnet auf einer gröberen Granularität (entfernt Dimensionen aus dem Kontext):

```sql
{EXCLUDE [Region] : SUM([Sales])}
-- Total ignoring region, while view shows by region
```

Anwendungsfall: Anteil am Gesamtergebnis anzeigen, aufgeschlüsselt nach Unterkategorie.

### Klassisches Muster: Prozent vom Gesamtergebnis {#classic-pattern-percent-of-total}

```sql
SUM([Sales]) / {FIXED : SUM([Sales])} * 100
```

Der Ausdruck `{FIXED : SUM([Sales])}` ohne Dimensionen berechnet die Gesamtsumme, die von keinen ansichtsbezogenen Dimensionen beeinflusst wird.

### LOD in der Filterreihenfolge {#lod-in-filter-order}

Zum Verständnis, wo LOD in der Reihenfolge der Filteroperationen steht:

1. Extract-Filter
2. Datenquellenfilter
3. Kontextfilter
4. **FIXED-LOD** wird hier ausgewertet (zusammen mit Dimensionsfiltern)
5. **INCLUDE/EXCLUDE-LOD** wird hier ausgewertet (zusammen mit Measure-Filtern)
6. Filter für Tabellenberechnungen

Das bedeutet: FIXED-LOD wird von Kontextfiltern beeinflusst, aber NICHT von Dimensionsfiltern, während INCLUDE/EXCLUDE-LOD von beiden beeinflusst wird.

### Kohortenanalyse mit LOD {#cohort-analysis-with-lod}

```sql
-- Cohort month (first activity)
{FIXED [User ID] : MIN(DATETRUNC('month', [Event Date]))}

-- Period since first activity
DATEDIFF('month',
    {FIXED [User ID] : MIN([Event Date])},
    [Event Date])
```

### Verschachtelte LOD {#nested-lod}

Ein LOD innerhalb eines anderen LOD ist möglich, sollte aber wegen der Performance-Auswirkungen sorgfältig eingesetzt werden. Jede Verschachtelungsebene fügt der erzeugten Abfrage weitere JOINs hinzu.

## Stolperfallen {#gotchas}

- Vermeiden Sie LOD innerhalb komplexer verschachtelter Berechnungen – jedes LOD fügt JOINs hinzu:
```bash
  -- Slow (3+ JOINs):
  SUM({FIXED DATEPART('year', [Order Date]) : SUM([Sales])})

  -- Better: pre-aggregate in data source or use table calculation
  ```
- FIXED-LOD wird nicht von Dimensionsfiltern der Ansicht beeinflusst – dies kann zu Verwirrung führen, wenn ein Filter bei einer FIXED-Berechnung scheinbar nicht wirkt
- Kontextfilter beeinflussen FIXED-LOD – stufen Sie einen Filter zum Kontextfilter hoch, wenn FIXED-LOD ihn berücksichtigen soll
- INCLUDE/EXCLUDE sind intuitiver, in den meisten Fällen aber langsamer als FIXED
- Wenn möglich, sollten berechnete Felder vor der Veröffentlichung im Extract materialisiert werden, statt das LOD zur Abfragezeit zu berechnen

## Siehe auch {#see-also}

- [[tableau-calculations]] – zeilenbasierte, aggregierte und Tabellenberechnungen
- [[tableau-fundamentals]] – Reihenfolge der Filteroperationen, Datenverbindungen
- [[tableau-performance-optimization]] – Optimierung der LOD-Performance
- [[cohort-retention-analysis]] – Kohortenanalyse-Muster mit LOD
