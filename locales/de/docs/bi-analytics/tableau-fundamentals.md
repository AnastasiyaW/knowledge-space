---
title: "Tableau-Grundlagen"
category: tools
tags: [bi-analytics, tableau, data-connections, joins, extract, live]
level: 2
source_sha256: f0a9ff5b7f752567232ea76791e33cff33cdb90652b53ac8539073d9c853f83f
translation: machine
translated_at: '2026-10-24'
---
# Tableau-Grundlagen {#tableau-fundamentals}

Tableau ist eine Enterprise-BI-Plattform (Desktop + Server/Cloud) mit der leistungsstärksten Visualisierungs-Engine im BI-Markt. Dieser Eintrag behandelt Datenverbindungen, Join-Typen, die Filterreihenfolge und zentrale Architekturkonzepte.

## Wichtige Fakten {#key-facts}

- Tableau verbindet sich über: Tableau Server (veröffentlichte Datenquellen), Dateien (Excel/CSV/JSON/PDF), Server/Datenbank (200+ native Konnektoren), Cloud-Speicher
- Zwei Verbindungsmodi: Live (Abfragen in Echtzeit) und Extract (`.hyper`-Snapshot-Datei)
- Visueller Indikator: Live = ein Fass-Symbol, Extract = zwei Fässer
- Custom SQL ist verfügbar, aber Tableau optimiert es nicht, bevor es an die Datenbank gesendet wird
- ClickHouse wird nicht nativ unterstützt, erfordert einen ODBC- oder JDBC-Treiber
- Ökosystem: Tableau Prep (visuelles ETL), Tableau Catalog (Data Governance), Data Management Add-on

## Muster {#patterns}

### Live vs. Extract {#live-vs-extract}

**Live-Modus**: Jede Aktion im Arbeitsblatt sendet eine Abfrage an die Datenbank. Die Daten sind immer aktuell, die Performance hängt von der Geschwindigkeit der Datenbank ab.

**Extract-Modus**: Datensnapshot, gespeichert als `.hyper`-Datei mit hoher Kompression. Abgelegt im Ordner `Datasources`.

Extract-Einstellungen:
- Logischer vs. physischer Tabellenmodus
- Filter (z. B. nach Stadt oder Geo)
- Aggregation auf Extract-Ebene (optimiert Geschwindigkeit und Größe)
- Zeilenlimit
- **Inkrementelle Aktualisierung**: nur neue Daten aktualisieren
- **Alle nicht verwendeten Felder ausblenden**: entfernt ungenutzte Felder zur Optimierung

**Regel**: Extract ist in fast allen Fällen Live überlegen (materialisierte Daten sind schneller).

### Custom SQL vs. Visual Editor {#custom-sql-vs-visual-editor}

Vorteile von Custom SQL: schnelle Ad-hoc-Erstellung von Datenquellen; Parameter können eingebettet werden.

Nachteile von Custom SQL:
- Keine Syntaxhervorhebung im Editor
- Transformation für Teammitglieder nicht sichtbar
- Tableau optimiert Custom SQL nicht, bevor es an die Datenbank gesendet wird
- GROUP BY und ORDER BY in Custom SQL vermeiden

**Regel**: Für einfache Operationen den Visual Editor verwenden. Custom SQL nur dann einsetzen, wenn die Flexibilität wirklich benötigt wird.

### Methoden zum Kombinieren von Tabellen {#table-combining-methods}

**Join**: standardmäßiger relationaler Join. Erstellt automatisch einen Join über Felder mit gleichem Namen. Typen: Inner, Left, Right, Full Outer.
- Logischer Join: Tableau verbindet zuerst, dann wird ein Extract erstellt (Daten werden zusammengeführt, anschließend als Snapshot gespeichert)
- Physischer Join: je Tabelle ein Extract, danach Join bei der Abfrage

**Union**: Stapelt Tabellen mit identischem Schema. Unterstützt automatische Union anhand eines Blatt- bzw. Tabellennamensmusters.

**Relations** (Tableau 2020+): Analyse von Daten über Tabellen mit unterschiedlicher Granularität hinweg. Relations verbinden und aggregieren während der Analyse auf der benötigten Detailebene. Löst Datenduplikation ohne LOD-Berechnungen.

Bei unterschiedlicher Datumsgranularität (Bestellungen pro Tag, Plan pro Monat):
```sql
DATE(DATETRUNC("month", [Order Date]))
```

**Blending**: Mischt Daten aus verschiedenen Quellen pro Arbeitsblatt. Primäre Quelle = zuerst gezogenes Feld; sekundäre Quelle = durch eine andere Farbe gekennzeichnet.

Wann Blending statt Relations verwenden:
1. Flexibilität pro Arbeitsblatt nötig (Blending = pro Blatt, Relations = pro Datenquelle)
2. Zwei unabhängige Quellen, keine Berechnungen über beide hinweg nötig, aber ein Filter soll beide steuern

**Data Blending = Performance-Problem**: erzeugt mehrere Abfragen; wenn möglich vermeiden.

### Reihenfolge der Filteroperationen {#filter-order-of-operations}

Filter werden in dieser Reihenfolge angewendet (entscheidend für LOD-Berechnungen):

1. Extract-Filter
2. Datenquellenfilter
3. Kontextfilter
4. Dimensionsfilter (umfasst: Sets, bedingte Filter, Top N, **FIXED LOD**)
5. Kennzahlenfilter (umfasst: **INCLUDE/EXCLUDE LOD**, Data Blending)
6. Tabellenberechnungsfilter (umfasst: Prognosen, Tabellenberechnungen, Cluster, Summen)

### Zeilen- und Spaltensicherheit {#rowcolumn-security}

**Row Level Security (RLS)**: Verschiedenen Benutzern unterschiedliche Zeilen anzeigen.
- Integriert: Registerkarte Server -> Benutzerfilter erstellen, Benutzer Regionen zuweisen
- Skalierbar: Zugriffstabelle (Paare aus Benutzer und Region), physischer Join mit der Faktentabelle, Filter mit `regional_manager = USERNAME()`

**Column Level Security**: Verschiedenen Benutzergruppen unterschiedliche Dimensionen anzeigen.

**Wichtig**: RLS erfordert einen physischen JOIN (nicht logisch), um eine Datenexplosion zu vermeiden.

## Stolperfallen {#gotchas}

- Relations sind Blending bei granularitätsübergreifenden Daten vorzuziehen (oder im DWH vorab joinen)
- FIXED LOD wird auf Kontextfilter-Ebene (Schritt 4) ausgewertet, INCLUDE/EXCLUDE auf Dimensionsfilter-Ebene (Schritt 5); diese Unterscheidung ist für das Verhalten von Dashboards entscheidend
- Custom SQL in LIVE-Verbindungen ist besonders problematisch für die Performance
- Jedes Arbeitsblatt erzeugt eine Abfrage an die Quelle; mehr Blätter bedeuten mehr Abfragen
- Ein veröffentlichter Extract verliert seinen Cache, wenn er mit relevanten Filtern verwendet wird; ein eingebetteter Extract behält seinen Cache besser

## Siehe auch {#see-also}

- [[tableau-calculations]] - berechnete Felder und Tabellenberechnungen
- [[tableau-lod-expressions]] - Details zu FIXED/INCLUDE/EXCLUDE
- [[tableau-performance-optimization]] - Performance-Optimierung
- [[bi-tools-comparison]] - Tableau vs. Power BI vs. Alternativen
