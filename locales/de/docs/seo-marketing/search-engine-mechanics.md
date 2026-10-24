---
title: "Suchmaschinen-Mechanik"
category: concepts
tags: [seo-marketing, search-engines, crawling, indexing, ranking, relevance]
level: 3
source_sha256: e3dca74ae901ea1f5c189ebd6fa0d195507d4e28fe93924947c122eb670dcbeb
translation: machine
translated_at: '2026-10-24'
---
# Suchmaschinen-Mechanik {#search-engine-mechanics}

Wie Suchmaschinen Webdokumente finden, verarbeiten und ranken. Behandelt werden Crawling, die Indexierungspipeline, linguistische Verarbeitung sowie die zentralen Gruppen von Ranking-Faktoren, die die Positionen in den SERPs bestimmen.

## Zentrale Begriffe {#key-terminology}

- **Dokument** - eine Webseite (nicht eine Website); die grundlegende Einheit der Suche
- **Kollektion** - Gesamtmenge der indexierten Dokumente (~13,5 Milliarden bei Yandex)
- **Term** - ein einzelnes Wort
- **Query** - Text, der in das Suchfeld eingegeben wird
- **Intent** - was der Nutzer tatsächlich will (nicht nur, was er eingegeben hat)
- **Relevanz** - wie gut ein Dokument der über die Query ausgedrückten Nutzerabsicht entspricht

## Crawling-Architektur {#crawling-architecture}

**Crawler (Suchbot/Robot/Spider)** - Programm, das Websites findet und scannt, indem es Links folgt, und den Inhalt in der Datenbank der Suchmaschine speichert.

### Steuerungsmechanismen für Crawler {#crawler-control-mechanisms}
1. `robots.txt` - Erlaubt- und Verboten-Regeln für den Botzugriff
2. `sitemap.xml` - Karte der zu crawlenden Seiten
3. Yandex Webmaster / Google Search Console - direkte Verwaltung
4. Meta-Robots, Canonical, X-Robots-Tag, noindex/nofollow-Tags
5. RSS-Feed
6. YML-Datei (Produktkatalogformat von Yandex)
7. IndexNow / Google Indexing API - Push-Benachrichtigungen in Echtzeit

## Linguistische Verarbeitung {#linguistic-processing}

### Lemmatisierung {#lemmatization}
Alle Wortformen werden auf die Grundform (Lemma) zurückgeführt. Dadurch lassen sich Queries unabhängig von der Flexion mit Dokumenten abgleichen.

### Invertierter Index {#inverted-index}
Für jeden Term über alle Dokumente hinweg wird gespeichert, welche Dokumente diesen Term enthalten.

```yaml
Direct:   Document 1 → [word_a, word_b, word_c]
Inverted: word_a → [Document 1, Document 3]
          word_b → [Document 1, Document 2]
```

**Boolesche Suche**: `Cat AND Hare AND NOT Fox` - findet alle Dokumente, die den Ausdruck erfüllen.

### Query Rewriting {#query-rewriting}
- **Query Rewrite** - Anpassung der Gewichtung einzelner Wörter in der Query für bessere Ergebnisse
- **Query-Reformulierung** - automatisches Hinzufügen von Synonymen zur Query
- Beispiel: "what is seo" wird um "means", "abbreviation", "stands for" erweitert

## Ranking-Faktorgruppen {#ranking-factor-groups}

Es existieren über 2000 Faktoren. Sie lassen sich in Kategorien gliedern:

### Textfaktoren (intern) {#text-factors-internal}
- Termhäufigkeit in den Dokumentzonen (TF-IDF, BM25)
- Textuniqueness (Einzigartigkeit des Textes)
- LSI (latente semantische Indexierung - verwandte Begriffe)
- Textlänge, grammatikalische Qualität
- Direkte Keyword-Einbindung und Vorhandensein von Wortpermutationen

### Linkfaktoren (extern) {#link-factors-external}
- Zusammensetzung der Ankertexte
- Wachstumsrate der Links und Gesamtzahl der Backlinks
- Autorität und Anzahl der verlinkenden Domains
- Thematische Ähnlichkeit zwischen Donor und Akzeptor
- Indikator für die kommerzielle „Verkäuflichkeit“ des Donors

### Kommerzielle Faktoren (intern) {#commercial-factors-internal}
- Umfang des Produkt- bzw. Dienstleistungssortiments
- Zahlungs- und Lieferoptionen
- Garantie- und Rückgabebedingungen, Preistransparenz
- Strukturierter Katalog, mehrere Kontaktmöglichkeiten
- Conversion-Elemente (CTAs, Formulare, Rückrufmöglichkeit)

### Host-Faktoren (intern) {#host-factors-internal}
- Domainalter, Anzahl indexierter Seiten
- Historie von Domain-Inhaberwechseln
- Domainzone (.ru, .com usw.)

### Technische Faktoren (intern) {#technical-factors-internal}
- Server-Antwortcodes, Code-Validität
- Ladegeschwindigkeit der Seite, HTTPS
- Duplicate Content und Weiterleitungen

### Verhaltensfaktoren {#behavioral-factors}
- **Intern (auf der Website)**: Verweildauer, Tiefe der Navigation, Absprungrate
- **Extern (in den SERPs)**: Last Click, Single Click, Rückkehr per Direkteingabe, Snippet-CTR

## Ranking-Priorität nach Suchmaschine {#ranking-priority-by-search-engine}

| Faktorgruppe | Priorität Yandex | Priorität Google |
|-------------|----------------|----------------|
| Verhalten | #1 (höchste) | #3 |
| Text | #2 | #2 |
| Links | #3 | #1 (höchste) |
| Kommerziell | #4 | #4 |
| Technisch | grundlegend | grundlegend |

## Sandbox-Filter {#sandbox-filter}

Temporärer Filter für neue Websites, um Manipulation zu verhindern:
- Dauer: 2-12 Monate, je nach Website
- Betrifft nahezu alle neu erstellten Websites
- Zweck: Filterung von Websites, die mit Black-Hat-Methoden erstellt wurden

## Stolpersteine {#gotchas}
- **Prioritäten von Yandex und Google sind invers** - bei Google dominieren Links, bei Yandex Verhaltensfaktoren. Die Strategie muss dies berücksichtigen
- **2000+ Faktoren** heißt nicht, dass alle gleich gewichtet sind - eine Handvoll Faktoren pro Query-Typ bestimmt 80 %+ der Ranking-Varianz
- **Relevanz != Keyword-Anzahl** - moderne Suchmaschinen nutzen semantisches Verständnis, nicht nur Termabgleich
- **Sandbox gilt universell** - auch legitime neue Websites haben 2-12 Monate unterdrückte Rankings

## Siehe auch {#see-also}
- [[ranking-algorithms-history]] - Algorithmus-Zeitleisten und Entwicklung neuronaler Netze
- [[text-optimization]] - Dokumentzonen und Relevanzbewertung
- [[behavioral-factors-ctr]] - Vertiefung der Verhaltensfaktoren
- [[commercial-ranking-factors]] - Kommerzielle Faktoren und E-E-A-T
