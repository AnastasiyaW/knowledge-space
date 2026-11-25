---
title: "Power BI Grundlagen"
category: tools
tags: [bi-analytics, power-bi, dax, power-query, data-model, microsoft]
level: 2
source_sha256: 2b42c6be1f15d2b8242dcf311133a460bc9686c954ef459e87f3dc8759cd79ca
translation: machine
translated_at: '2026-10-24'
---
# Power BI Grundlagen {#power-bi-fundamentals}

Power BI ist Microsofts BI-Plattform (Desktop + Cloud) mit enger Integration in das Microsoft-Ökosystem, einem großzügigen kostenlosen Angebot und der DAX-Berechnungsengine. Die Stärken zeigen sich vor allem in Organisationen, die bereits Azure, Excel, Teams und SharePoint nutzen.

## Wichtige Fakten {#key-facts}

- Drei Arbeitsansichten: Berichtsansicht (Arbeitsfläche), Datenansicht (Tabellenprüfung), Modellansicht (Beziehungen)
- Zwei Verbindungsmodi: Import (Daten werden in die In-Memory-Engine geladen) und DirectQuery (Live-Abfragen an die Quelle)
- Sternschema empfohlen: Faktentabelle im Zentrum, Dimensionstabellen darum herum
- DAX (Data Analysis Expressions) = Formelsprache für berechnete Spalten und Measures
- Power Query Editor = integriertes ETL-Werkzeug mit der M-Sprache
- Unterstützt über 100 Datenquellen: Excel, CSV, JSON, PDF, SQL Server, PostgreSQL, MySQL, Azure, SharePoint, Web, OData

## Muster {#patterns}

### Verbindungsablauf {#connection-workflow}

1. Start -> Daten abrufen -> Quelltyp auswählen
2. Verbindungsparameter eingeben / Datei auswählen
3. Navigator: zu ladende Tabellen/Blätter auswählen
4. Daten transformieren (öffnet Power Query) oder direkt laden

**Import-Modus**: Daten werden in die `.pbix`-Datei geladen, immer schnell, aber veraltet, bis sie aktualisiert werden.
**DirectQuery**: Live-Abfragen bei jeder Interaktion, immer aktuell, aber langsamer.

### Transformationen mit Power Query (M-Sprache) {#power-query-m-language-transformations}

| Operation | SQL-Entsprechung |
|-----------|---------------|
| Datentyp ändern | CAST |
| Zeilen entfernen | WHERE + DELETE |
| Zeilen filtern | WHERE |
| Spalte teilen | SUBSTRING / SPLIT |
| Spalten zusammenführen | CONCAT |
| Benutzerdefinierte Spalte hinzufügen | Berechnete Spalte |
| Pivot/Unpivot | PIVOT / UNPIVOT |
| Abfragen zusammenführen | JOIN |
| Abfragen anhängen | UNION |

Bereich „Angewendete Schritte“: Jede Transformation wird als umkehrbarer Schritt protokolliert. Der zugrunde liegende M-Code ist im Erweiterten Editor sichtbar.

### Datenmodell: Beziehungen {#data-model-relationships}

Eigenschaften von Beziehungen:
- **Kardinalität**: Eins-zu-Viele (am häufigsten), Viele-zu-Viele, Eins-zu-Eins
- **Filterrichtung**: Einfach (von 1 zu Viele), Beide (bidirektional)
- **Aktiv/Inaktiv**: nur eine aktive Beziehung pro Tabellenpaar

Erstellen: In der Modellansicht ein Feld von einer Tabelle auf das passende Feld in einer anderen Tabelle ziehen.

### DAX-Grundlagen {#dax-basics}

**Berechnete Spalte (Calculated Column)** – wird beim Laden der Daten berechnet und zeilenweise gespeichert:
```dax
Full Name = Customers[First Name] & " " & Customers[Last Name]
Profit = Sales[Revenue] - Sales[Cost]
```

**Measure** – wird zur Abfragezeit auf Basis des Filterkontexts berechnet:
```dax
Total Sales = SUM(Sales[Revenue])
Average Order = AVERAGE(Sales[OrderValue])
Num Customers = DISTINCTCOUNT(Sales[CustomerID])
Sales LY = CALCULATE([Total Sales], SAMEPERIODLASTYEAR(Date[Date]))
YoY Growth % = DIVIDE([Total Sales] - [Sales LY], [Sales LY])
```

### Wichtige DAX-Funktionen {#key-dax-functions}

| Funktion | Zweck |
|----------|---------|
| `SUM()` | Summe aggregieren |
| `AVERAGE()` | Mittelwert aggregieren |
| `COUNT()` / `COUNTA()` | Zeilen zählen / nicht leere Werte zählen |
| `DISTINCTCOUNT()` | Eindeutige Werte zählen |
| `CALCULATE()` | Filterkontext ändern |
| `FILTER()` | Gefilterte Tabelle zurückgeben |
| `ALL()` | Filter von Spalte/Tabelle entfernen |
| `RELATED()` | Wert aus einer verknüpften Tabelle abrufen |
| `DIVIDE(num, den)` | Sichere Division (BLANK bei Division durch 0) |
| `IF(cond, true, false)` | Bedingte Logik |
| `SWITCH()` | Mehrere Bedingungen |
| `SAMEPERIODLASTYEAR()` | Zeitintelligenz – gleiche Periode im Vorjahr |
| `DATEADD()` | Zeitintelligenz – Datumswerte verschieben |

**Filterkontext**: Measures berücksichtigen automatisch aktive Slicer, Seitenfilter und visuelle Filter. `CALCULATE` verändert diesen Kontext.

### Filtertypen (nach Priorität) {#filter-types-by-precedence}

1. **Visualisierungsebene** – gilt für ein einzelnes Diagramm
2. **Seitenebene** – gilt für alle Visuals auf der Seite
3. **Berichtsebene** – gilt für alle Seiten
4. **Detailfilter (Drillthrough)** – wird beim Drillthrough automatisch übergeben

Slicer-Visual = interaktives Filter-Steuerelement. Typen: Liste, Dropdown, Zwischen (Datumsbereich), relatives Datum.

### Gängige Visualisierungen {#common-visualizations}

- Balken-/Säulendiagramm – Vergleich von Kategorien
- Liniendiagramm – Zeitverläufe
- Kreis-/Ringdiagramm – Anteil am Ganzen (maximal 5 Segmente)
- Matrix – Kreuztabelle
- Karte (Card) – einzelne KPI-Zahl
- Tabelle – Rohdaten
- Treemap – Vergleich hierarchischer Größen
- Karte/Gefüllte Karte – geografische Daten
- Messanzeige (Gauge) – Fortschritt zum Ziel

## Stolpersteine {#gotchas}

- DAX ist ein leistungsfähiges, aber eigenständiges Paradigma im Vergleich zu SQL – die Lernkurve ist steil
- Berechnete Spalten vergrößern die Dateigröße (zeilenweise gespeichert); nach Möglichkeit Measures bevorzugen
- Bidirektionale Beziehungen können zu unerwarteter Filterweitergabe führen – nur verwenden, wenn nötig
- `.pbix`-Dateien sind binär und für Git ungeeignet; für Versionskontrolle Azure DevOps verwenden
- `.pbix`-Dateien im Import-Modus können bei großen Datenmengen sehr groß werden – DirectQuery oder Aggregationen in Betracht ziehen

## Siehe auch {#see-also}

- [[powerbi-advanced-features]] - Designs, Lesezeichen, Drillthrough, DAX fortgeschritten
- [[bi-tools-comparison]] - Power BI vs. Tableau vs. Alternativen
- [[dashboard-design-patterns]] - Gestaltungsprinzipien, die über Werkzeuge hinweg gelten
- [[sql-for-analytics]] - SQL-Grundlagen für DAX-Anwender
