---
title: "Tableau-Berechnungen"
category: tools
tags: [bi-analytics, tableau, calculated-fields, table-calculations, window-functions, parameters]
level: 3
source_sha256: 27314abcb76deaf17a5ca1a488b8e99e734a9a6e4edf64d191d3296e6822457f
translation: machine
translated_at: '2026-10-24'
---
# Tableau-Berechnungen {#tableau-calculations}

Tableau bietet mehrere Berechnungstypen, die auf unterschiedlichen Granularitätsebenen arbeiten. Das Verständnis, wann welcher Typ zu verwenden ist, ist entscheidend für den Aufbau korrekter und performanter Dashboards.

## Wichtige Fakten {#key-facts}

- Sechs Berechnungstypen: zeilenbasiert, aggregiert, Quick-Tabellenberechnungen, Tabellenberechnungen, Fensterberechnungen, LOD
- Zeilenbasierte Berechnungen werden pro Zeile ausgeführt; aggregierte erfordern Aggregationsfunktionen
- Tabellenberechnungen rechnen über die im aktuellen View sichtbaren Werte
- Fensterberechnungen sind ein Untertyp der Tabellenberechnungen, die über ein Fenster sichtbarer Werte arbeiten
- Quick-Tabellenberechnungen sind Wrapper um Fensterfunktionen, die mit 2 Klicks angewendet werden
- Parameter sind vom Benutzer steuerbare Variablen, die das Verhalten des Dashboards verändern

## Muster {#patterns}

### Berechnungstypen im Überblick {#calculation-types-overview}

| Typ | Beschreibung | Beispiel |
|------|-------------|---------|
| **Zeilenbasiert** | Pro Zeile (Beobachtung) | `[Price] * [Quantity]` |
| **Aggregiert** | Verwendet Aggregationsfunktion | `SUM([Sales]) / COUNT([Orders])` |
| **Quick-Tabellenberechnung** | Integrierte Tabellenberechnungen (2 Klicks) | Laufende Summe, Anteil am Gesamtwert |
| **Tabellenberechnung** | Benutzerdefinierte Formel über sichtbare Werte | `INDEX()`, `RANK()`, `LOOKUP()` |
| **Fensterberechnung** | Über ein Fenster sichtbarer Werte | `WINDOW_AVG(SUM([Sales]), -2, 0)` |
| **LOD** | Auf festgelegter Granularität | `{FIXED [Customer] : SUM([Sales])}` |

### Datumsfunktionen {#date-functions}

```sql
DATEPART('month', [Order Date])    -- extracts integer (3 for March)
DATETRUNC('month', [Order Date])   -- returns first date of period (2023-03-01)
DATEDIFF('day', [Order Date], TODAY())  -- difference between dates
DATENAME('weekday', [Order Date])  -- returns string ("Monday")
```

Hinweis: Tableau umschließt DATETRUNC standardmäßig mit DATEBAR. Wählen Sie im Dropdown des Feldes „exact date“, um das tatsächliche Datum zu sehen.

### Zeichenkettenfunktionen {#string-functions}

```sql
SPLIT([Product Name], '-', 1)      -- split by delimiter, first part
FIND([String], 'word')             -- position of substring
REPLACE([String], 'old', 'new')    -- replace substring
CONTAINS([String], 'word')         -- true/false
STARTSWITH([Category], 'word')     -- true/false (faster than CONTAINS)
REGEXP_MATCH / REGEXP_EXTRACT / REGEXP_REPLACE  -- regex
```

**Performance-Tipp**: `STARTSWITH` ist schneller als `CONTAINS`, wenn möglich.

### Aggregierte Berechnungen {#aggregated-calculations}

```sql
SUM([Sales])
AVG([Profit])
MEDIAN([Revenue])
COUNTD([User ID])               -- count distinct
ATTR([Region])                  -- checks if unique; marks * if multiple values
SUM([Revenue] - [Cost]) / SUM([Revenue])  -- margin calculation
```

### Tabellenberechnungen {#table-calculations}

**Indizierung und Ranking:**
```sql
INDEX()                -- row number within partition (1, 2, 3...)
FIRST()                -- offset from first row (0 for first)
LAST()                 -- offset from last row (0 for last)
RANK(expression)       -- rank by value
RANK_UNIQUE(), RANK_DENSE(), RANK_PERCENTILE()
```

**Laufende Summen:**
```sql
RUNNING_SUM(SUM([Sales]))
RUNNING_AVG(SUM([Profit]))
RUNNING_MAX(SUM([Revenue]))
```

**Lookup und Referenz:**
```sql
LOOKUP(SUM([Sales]), -1)       -- value from 1 row earlier
LOOKUP(SUM([Sales]), FIRST())  -- value from first row in partition
PREVIOUS_VALUE(0)              -- previous value or 0 if none
```

**Partition und Address**: Die Einstellungen unter „Compute Using“ legen fest, welche Dimension adressiert wird (entlang derer gerechnet wird) und welche partitioniert wird (die Berechnung zurücksetzt).

### Fensterberechnungen {#window-calculations}

```sql
WINDOW_SUM(SUM([Sales]), -2, 0)    -- rolling 3-period sum
WINDOW_AVG(SUM([Sales]), -2, 0)    -- rolling 3-period average
WINDOW_MAX(SUM([Profit]))           -- max in entire window
WINDOW_MIN(SUM([Profit]))           -- min in entire window
WINDOW_STDEV(SUM([Sales]))         -- std deviation
```

Offsets: `FIRST()` = Anfang, `LAST()` = Ende, `0` = aktuelle Zeile. Der zweite und dritte Parameter sind der relative Start bzw. das relative Ende.

### Quick-Tabellenberechnungen {#quick-table-calculations}

Anwendung über Rechtsklick auf die Kennzahl im Ablagebereich -> Quick Table Calculation:

| Funktion | Beschreibung |
|----------|-------------|
| Running Total | Kumulative Summe |
| Difference | Differenz zum vorherigen Zeitraum |
| Percent Difference | `(current - previous) / previous * 100%` |
| Percent of Total | Anteil am Gesamtwert |
| Moving Average | Gleitender Durchschnitt über N Perioden |
| YTD Total | Laufende Summe seit Jahresbeginn |
| Compound Growth Rate | CAGR |
| Rank | Rangfolge innerhalb der Partition |

Filter „Letzten Monat anzeigen“: `LAST() = 0` als Filter für die Tabellenberechnung.

### Parameter {#parameters}

Erstellen: Rechtsklick auf den Datenbereich -> Create Parameter. Typen: String, Integer, Float, Boolean, Date.

```ruby
IF [Sales] > [Parameter: Sales Threshold] THEN 'Above' ELSE 'Below' END
```

**Muster „Metrikumschalter“**: Parameter + IF/CASE, um je nach Auswahl im Dropdown unterschiedliche Kennzahlen anzuzeigen.

### Logische Funktionen {#logical-functions}

```ruby
// IF
IF [Profit] > 0 THEN 'Profitable'
ELSEIF [Profit] = 0 THEN 'Break Even'
ELSE 'Loss'
END

// CASE (cleaner for multiple fixed values)
CASE [Region]
  WHEN 'North' THEN 'Northern Division'
  WHEN 'South' THEN 'Southern Division'
  ELSE 'Other'
END
```

## Fallstricke {#gotchas}

- Die Aggregationsrichtung ist relevant: Im Menü „Compute Using“ festlegen, ob die Berechnung über Spalten oder entlang der Zeilen läuft
- Quick-Tabellenberechnungen sind eigentlich Fensterfunktionen – sie kapseln die Formeln, sodass Sie diese nicht manuell schreiben müssen
- Das Mischen aggregierter und nicht aggregierter Felder in einer Berechnung führt zu Fehlern – alle müssen auf derselben Ebene liegen
- Operationen mit dem Typ String sind am langsamsten; bevorzugen Sie die Typhierarchie: `String > Date > Numeric > Boolean`
- `DUPLICATE_AS_CROSSTAB` zeigt die zugrunde liegende Datentabelle einer Visualisierung – nützlich zur Fehlersuche

## Siehe auch {#see-also}

- [[tableau-lod-expressions]] – FIXED/INCLUDE/EXCLUDE für granularitätsübergreifende Berechnungen
- [[tableau-fundamentals]] – Datenverbindungen und Filterreihenfolge
- [[tableau-performance-optimization]] – Performance-Optimierung von Berechnungen
- [[powerbi-fundamentals]] – DAX-Entsprechungen der Berechnungen
