---
title: "Power BI Erweiterte Funktionen"
category: tools
tags: [bi-analytics, power-bi, dax, bookmarks, drill-through, what-if, custom-visuals]
level: 4
source_sha256: bad9228921d5c64b5a152a7d81ba5bdad861912fa71052818112bbde75eee413
translation: machine
translated_at: '2026-10-24'
---
# Power BI Erweiterte Funktionen {#power-bi-advanced-features}

Erweiterte Power-BI-Funktionen wie benutzerdefinierte Designs, Visuals aus AppSource, What-If-Parameter für Szenarioanalysen, Drillthrough-Navigation, Lesezeichen für Storytelling und fortgeschrittene DAX-Muster.

## Wichtige Fakten {#key-facts}

- Benutzerdefinierte Designs über JSON-Dateien für Markenkonformität und Barrierefreiheit
- Benutzerdefinierte Visuals aus dem AppSource-Marktplatz (Format `.pbiviz`)
- What-If-Parameter erzeugen slicergesteuerte Szenarioanalysen
- Drillthrough ermöglicht die Navigation von der Zusammenfassung zum Detail per Rechtsklick
- Lesezeichen erfassen den Berichtszustand (Filter, Seite, Sichtbarkeit) für Navigation und Storytelling
- Performance Analyzer identifiziert langsame Visuals

## Muster {#patterns}

### Benutzerdefinierte Designs {#custom-themes}

```json
{
  "name": "MyTheme",
  "dataColors": ["#118DFF", "#12239E", "..."],
  "background": "#FFFFFF",
  "foreground": "#252423",
  "tableAccent": "#118DFF"
}
```

Anwenden: View -> Themes -> Browse for themes (JSON-Datei) oder aus der Galerie auswählen. Designgeneratoren sind als Webtools verfügbar.

### What-If-Parameter {#what-if-parameters}

Erstellen: Modeling -> New Parameter -> Name, Datentyp, Min, Max, Schrittweite und Standardwert festlegen.

Automatisch erzeugt werden: eine neue Tabelle mit einer Spalte als Wertebereich, ein Slicer und ein Measure für den ausgewählten Wert.

```dax
-- Auto-created
Discount Rate = SELECTEDVALUE('Discount'[Discount], 0)

-- User-created measure using the parameter
Revenue After Discount = [Total Revenue] * (1 - [Discount Rate])
```

**Metrik-Umschalter-Muster** (über einen Slicer auswählen, welche Metrik angezeigt wird):
```dax
Selected Metric =
SWITCH(
    SELECTEDVALUE('Metric Selector'[Metric]),
    "Revenue", [Total Revenue],
    "Profit", [Total Profit],
    "Orders", [Order Count]
)
```

### Drillthrough {#drill-through}

Einrichtung:
1. Detailseite erstellen
2. Dimensionsfeld in den Abschnitt "Drill-through" des Bereichs Filter ziehen
3. Auf Übersichtsseiten: Datenpunkt mit der rechten Maustaste anklicken -> Drill through -> [Seitenname]

Der Filter wird automatisch übergeben. Auf der Detailseite erscheint eine Schaltfläche "Back".

Anwendungsfall: Regionssummen -> Region anklicken -> alle Transaktionen dieser Region sehen.

### Lesezeichen {#bookmarks}

Erfassen: aktuelle Seite, Filter, Slicer-Werte, Sichtbarkeit der Visuals.

Erstellen: View -> Bookmarks pane -> Add bookmark.

Gängige Muster:
- **Storytelling**: eine Folge von Lesezeichen als geführte Erzählung
- **Benutzerdefinierte Navigation**: Schaltflächen mit der Aktion "Bookmark" ersetzen die standardmäßigen Seitenreiter
- **Bedingte Navigation**: Schaltfläche zeigt je nach Slicer-Auswahl eine andere Seite
- **Umschalten des Visualtyps**: Diagramm ODER Tabelle derselben Daten über Lesezeichen und Auswahlsichtbarkeit anzeigen
- **Erweiterte Tooltips**: Hover-Tooltips mit SVG-Bildern erstellen

Schaltflächenaktionen: Bookmark, Page navigation, Q&A, Drill-through, Web URL.

### Erweitertes DAX {#advanced-dax}

**FORMAT-Funktion**:
```dax
Sales Label = FORMAT([Total Sales], "$#,##0.00")
Month Name = FORMAT(Date[Date], "MMMM YYYY")
```

**Bedingte Formatierung über DAX**:
```dax
KPI Color = IF([Actual] >= [Target], "#28A745", "#DC3545")
```

Anwenden: Visualizations -> Value field -> Conditional formatting -> Field value.

**Berechnete Tabellen**:
```dax
Date Table = CALENDAR(DATE(2020,1,1), DATE(2025,12,31))
Top 10 Customers = TOPN(10, Customers, [Total Revenue], DESC)
```

### Leistungsoptimierung {#performance-optimization}

Performance Analyzer verwenden: View -> Performance Analyzer.

Optimierungstechniken:
- Import-Modus gegenüber DirectQuery für große Aggregationen bevorzugen
- Kardinalität der Spalten reduzieren (nicht verwendete Spalten entfernen)
- In Power Query vor dem Laden vorab aggregieren
- In Beziehungen ganzzahlige Surrogatschlüssel statt Textschlüssel verwenden
- Bidirektionale Beziehungen nur verwenden, wenn erforderlich
- Komplexe Berechnungen in Power Query (M) statt in DAX-Measures auslagern

## Fallstricke {#gotchas}

- Benutzerdefinierte Visuals aus AppSource unterstützen möglicherweise nicht alle Formatierungsoptionen oder verhalten sich im Power BI Service anders als in Desktop
- What-If-Parameter erzeugen tatsächliche Tabellen im Modell – viele Parameter bedeuten Modell-Aufblähung
- Lesezeichen erfassen den Sichtbarkeitszustand von Visuals; das kann brechen, wenn Visuals nach dem Erstellen der Lesezeichen hinzugefügt oder entfernt werden
- Drillthrough funktioniert nur bei Datenpunkten, die zur Drillthrough-Filterdimension passen
- Messwerte des Performance Analyzers können zwischen Desktop und Service aufgrund unterschiedlicher Abfrage-Engines abweichen

## Siehe auch {#see-also}

- [[powerbi-fundamentals]] - DAX-Grundlagen, Datenmodell, Power Query
- [[bi-tools-comparison]] - Vergleich der Funktionen von Power BI und Tableau
- [[dashboard-design-patterns]] - Gestaltungsprinzipien für Navigation
- [[color-theory-visualization]] - Designs und Best Practices für Farben
