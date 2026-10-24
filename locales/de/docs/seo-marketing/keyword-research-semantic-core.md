---
title: "Keyword-Recherche und semantischer Kern"
category: techniques
tags: [seo-marketing, keywords, semantic-core, wordstat, clustering, search-demand]
level: 3
source_sha256: 53a8ba01bec6098c07dbaade3ac13f0c9fa596c447464df1da8fe599d4f23ccf
translation: machine
translated_at: '2026-10-24'
---
# Keyword-Recherche und semantischer Kern {#keyword-research-and-semantic-core}

Vollständiger Prozess zum Sammeln, Bereinigen, Clustern und Zuordnen von Keyword-Gruppen zu Seiten. Behandelt die Operatoren von Yandex Wordstat, Erfassungsmethoden, SERP-basiertes Clustering und Tools.

## Grundlegende Terminologie {#core-terminology}

- **Semantischer Kern** - vollständige Menge an Keyword-Gruppen, die die gesamte Suchnachfrage der Nutzer für eine Website abdeckt
- **Marker** - Ankerquery, die den Inhalt einer Seite am präzisesten beschreibt; Grundlage für die Erweiterung
- **Cluster** - Gruppe von Queries, die von einer einzelnen Seite bedient werden
- **Frequenz** - Anzahl der Suchanfragen pro Monat für eine Query (Wordstat-Daten)
- **Query-Cloud** - vollständige erweiterte Menge an Queries, die um die Marker gesammelt wurden

## Quellen für die Query-Erfassung {#sources-for-query-collection}

### Verlässliche Quellen {#reliable-sources}
1. **Yandex Wordstat** - direkte Daten zur Suchnachfrage (am genauesten für das RU-Segment)
2. **Parsing von Suchvorschlägen** - Tools, die Autocomplete-Vorschläge sammeln
3. **Parsing-Programme** - Key Collector, Rush Analytics (automatisieren die Erfassung über Wordstat/Suchvorschläge)

### Weniger verlässlich (ergänzend) {#less-reliable-supplementary}
1. **Keyword-Datenbanken** - vorab gesammelte Query-Listen; unklare Herkunft/Vollständigkeit; können Müll enthalten
2. **Parsing von Konkurrenzseiten** - spiegelt die strukturellen Entscheidungen der Konkurrenz wider, nicht die gesamte Nachfrage

### Unterstützende Daten {#supporting-data}
- Yandex Metrika - Queries, die bisher Traffic gebracht haben
- Yandex Webmaster - Statistiken zur Suchdarstellung
- Google Keyword Planner - Google-Entsprechung zu Wordstat

## Tiefenanalyse Yandex Wordstat {#yandex-wordstat-deep-dive}

### Linke vs. rechte Spalte {#left-vs-right-column}
- **Linke Spalte** - N-Gramm-Häufigkeitswörterbuch: Summe aller Queries, die die Phrase in beliebiger Form, beliebiger Reihenfolge und beliebiger Länge enthalten
- **Rechte Spalte** - "Ähnliche Anfragen" - unzuverlässig; zeigt Queries, die dieselben Nutzer ebenfalls gesucht haben, keine Synonyme

### Wordstat-Operatoren {#wordstat-operators}

| Operator | Wirkung | Beispiel |
|---------|--------|---------|
| Keiner | Alle Queries, die das N-Gramm enthalten | `phone samsung` -> 1.250.000 |
| `"phrase"` | Fixiert die Wortanzahl (nur exakte Anzahl) | `"phone samsung"` -> 12.000 |
| `!word` | Fixiert die exakte Wortform (ohne Flexion) | `!mobile !phones` -> 61.000 |
| `[phrase]` | Fixiert die Wortreihenfolge | `[mobile phones]` -> 938.000 vs. `[phones mobile]` -> 60 |
| `+word` | Erzwingt die Einbeziehung von Stoppwörtern | `fridge +how` |
| `-word` | Schließt Queries mit diesem Wort aus | `fridge -reviews` |
| `(a\|b)` | ODER-Operator für Varianten | `smartphone (samsung\|galaxy)` |

### Kombination der Operatoren {#combining-operators}
**Für die Query-Erfassung:**
```text
fridge (samsung|lg) (buy|price|order) -reviews
```

**Für die präzise Frequenz:**
```text
"[!fridge !samsung]"
```
Anführungszeichen + eckige Klammern + Ausrufezeichen = präziseste Frequenz (alle drei Einschränkungen).

### 7-Wort-Trick {#7-word-trick}
Schreibe dasselbe Wort 7-mal in Anführungszeichen, um alle Queries genau dieser Länge zu finden:
```text
"keyword keyword keyword keyword keyword keyword keyword"
```
Funktioniert NICHT für Queries mit mehr als 7 Wörtern.

## Frequenztypen {#frequency-types}

| Typ | Operator | Wann verwenden |
|------|----------|-------------|
| Allgemein | `query` | Verkürzter Kern, HF-Marker |
| Phrase | `"query"` | Erweiterter Kern, Validierung der Frequenz |
| Exakt | `"[!exact !query]"` | Genaueste Zählung, Bestätigung der Nachfrage |

## Standardprozess der Erfassung {#standard-collection-process}

### Schritt 1: Marker sammeln {#step-1-collect-markers}
**Manuell** - für "schmutzige" Nischen oder kleine Semantiken (<30 Wordstat-Seiten). Tools: Erweiterungen WordStatter, WordStat Assistant.

**Automatisiert** - für große Kataloge und saubere Nischen. Tools: Rush Analytics, Key Collector.

**Marker vor der Erfassung erweitern**: kyrillische/lateinische Varianten, kommerzielle Präfixe, Preisindikatoren hinzufügen - jede erzeugt unterschiedliche Vorschlagsmengen.

### Schritt 2: Linke Spalte von Wordstat parsen {#step-2-parse-wordstat-left-column}
Für jeden erweiterten Marker alle Queries aus der linken Spalte erfassen.

### Schritt 3: Suchvorschläge parsen {#step-3-parse-search-suggestions}
Suchvorschläge können die Query-Liste um das 5- bis 7-Fache vergrößern. Jeder von 100 Markern kann 600-700 eindeutige Queries erzeugen.

### Schritt 4: Struktur der Konkurrenz parsen (optional) {#step-4-parse-competitor-structure-optional}
Kategorieseiten der Konkurrenz mit Screaming Frog crawlen, H1-Werte extrahieren = strukturierte semantische Entscheidungen der Konkurrenz.

**Beispiel**: Für einen Handyshop nur die `/tag/`-Seiten der Konkurrenz crawlen (Paginierung ausschließen), um alle Filter-/Attributseiten als H1-Werte zu extrahieren.

### Schritt 5: Zusammenführen und bereinigen {#step-5-combine-and-clean}
Stoppwörter entfernen: nicht-kommerzielle Stoppwörter ("Bewertungen", "Forum", "DIY"), Markennamen der Konkurrenz, geografische Stoppwörter, falls nicht benötigt.

### Schritt 6: Frequenz prüfen {#step-6-check-frequency}
Die Frequenz für alle erfassten Queries abrufen. Queries mit Frequenz null vor der Seitenerstellung entfernen.

### Schritt 7: Clustern {#step-7-cluster}
**SERP-basiertes Clustering** (Standard):
- Der Dienst erfasst die TOP-10-Ergebnisse für jede Query
- Teilen sich 2 Queries >=8 TOP-10-Seiten -> gleiche Gruppe (gleiche Intention)
- Prinzip: dieselben Dokumente in der SERP = identische Nutzerintention

**Manuelle Nachbearbeitung immer erforderlich**: fälschlich getrennte Cluster zusammenführen, fälschlich zusammengeführte aufteilen, Clusternamen korrigieren.

### Schritt 8: Kreuzmultiplikation (große Kataloge) {#step-8-cross-multiplication-large-catalogs}
Produkte x Marken x Attribute = generierte Query-Liste. Frequenz abrufen, Ergebnisse mit Frequenz null entfernen.

## Zuordnung von Clustern zu Seiten {#cluster-to-page-assignment}

| Seitentyp | Zuordnungsregel |
|-----------|----------------|
| Startseite | Häufigster "übergeordneter" Cluster |
| Kategorieseiten | Cluster auf Kategorieebene |
| Unterkategorieseiten | Unterkategorie-Cluster |
| Produkt-/Leistungsseiten | Spezifische Produkt-Cluster |
| Blog/Informationsseiten | Cluster informationaler Queries |

Manche Queries können NUR auf der Startseite ranken - SERP prüfen: Wenn alle Top-Ergebnisse Startseiten sind, der Startseite zuordnen.

## KI-gestützte Workflows {#ai-assisted-workflows}

### Markergenerierung mit KI {#marker-generation-with-ai}
**Iteration 1**: Seitentyp, Thema, Basis-Keywords und bekannte Merkmale angeben -> ALLE Merkmalstypen erhalten.

**Iteration 2**: Für jeden Merkmalstyp alle Werte auflisten, einschließlich Synonyme, Fachjargon und Schreibvarianten. Als Tabelle formatieren.

**Ergebnis**: Kombinationen [Merkmal] x [Wert] -> jede Zeile wird zu einem Parsing-Marker.

### Generierung von Meta-Tags {#meta-tag-generation}
**Title-Regeln**: häufigste Query am Anfang; jedes Wort nur einmal; bis 80 Zeichen / 12 Wörter; natürlicher Satz, keine Keyword-Liste; keine Rabattwörter.

**Description-Regeln**: 150-159 Zeichen, maximal 18 Wörter; Handlungsaufforderung + USP; Synonyme zu Keywords; 1-2 neutrale Emojis erlaubt.

### Content-Briefing mit KI {#content-brief-generation-via-ai}
1. Textanalyse über Rush Analytics für die Ziel-Keywords durchführen
2. Konkurrenzseiten parsen - Text mit Überschriftenhierarchie und Token-Anzahl extrahieren
3. Gliederung per KI erzeugen: Title, Zusammenfassung, Zielgruppe, H2-H3-Struktur
4. Keywords und LSI-Begriffe über die Gliederungsabschnitte verteilen, mit exakten Vorkommenszahlen

## Tools für die semantische Arbeit {#tools-for-semantic-work}

### SEOXL Excel-Add-in {#seoxl-excel-add-in}
- **Farbe nach Cluster** - alternierende Farben für Clustergrenzen
- **Sortierung innerhalb des Clusters** - sortiert nach Frequenz innerhalb jedes Clusters
- **Cluster nach Gesamtfrequenz sortieren** - Cluster mit dem meisten Traffic zuerst
- **Lemma-Wörterbuch** - häufigste Wortstämme über alle Queries; Kategorien von Stoppwörtern finden
- **Cluster-Review** - separates Blatt mit der ersten Zeile jedes Clusters; durch Ziehen benachbarter Zeilen zusammenführen
- **Squeeze** - entfernt angegebene Wortstämme; macht unterscheidende Modifikatoren für die Deduplizierung sichtbar

### Key Collector (Desktop) {#key-collector-desktop}
- Massen-Parsing von Wordstat, Frequenzerfassung, internes Clustering
- Frequenzerfassung in 4 Durchgängen (Basis, Phrase, exakte Phrase, [exact exact])
- SERP-basiertes Clustering: hart (Schnittmenge) oder weich (Vereinigungsmenge), konfigurierbar
- Aufgabenplaner für unbeaufsichtigte Läufe über Nacht
- Multi-Gruppen-Modus: Operationen gleichzeitig auf alle Gruppen anwenden

### Rush Analytics (Cloud) {#rush-analytics-cloud}
Cloudbasiertes Parsing, Frequenzprüfung, SERP-basiertes Clustering.

### Google Sheets-Skripte {#google-sheets-scripts}
Alle SEOXL-Funktionen lassen sich über Google Apps Script nachbilden, das per KI erzeugt wird. Prompt-Format: Umfang beschreiben ("mit ausgewähltem Bereich arbeiten") -> Aktion pro Zelle beschreiben -> Ausgabeort festlegen -> mit Korrekturen iterieren.

## Fallstricke {#gotchas}
- **Die rechte Spalte von Wordstat ist unzuverlässig** - nur ergänzend verwenden; zeigt "Queries, die dieselben Nutzer gesucht haben", keine Synonyme
- **Queries mit Frequenz null sollten keine Seiten bekommen** - erzeugt dünnen Inhalt, der die Gesamtqualität der Website schadet
- **SERP-basiertes Clustering erfordert manuelle Prüfung** - automatisches Clustering scheitert in 10-20 % der Fälle
- **Die Markererweiterung ist entscheidend** - nackte Marker verpassen die 5- bis 7-fache Menge an Queries, die erweiterte Varianten erfassen
- **Kreuzmultiplikation erzeugt Müll** - vor der Seitenerstellung immer mit Frequenzdaten validieren
- **LF-Queries nicht in den Textanalysator aufnehmen** - sie verzerren die Ergebnisse; optimal sind bis zu 6 Queries

## Siehe auch {#see-also}
- [[text-optimization]] - Verwendung des semantischen Kerns für Content-Briefings und den Textanalysator
- [[site-structure-urls]] - Wie Cluster auf die Seitenstruktur abgebildet werden
- [[seo-tools-workflow]] - Details zu Einrichtung und Konfiguration der Tools
- [[seo-strategy-by-site-type]] - Unterschiede in der Strategie beim semantischen Ansatz
