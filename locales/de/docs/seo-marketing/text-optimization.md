---
title: "Textoptimierung"
category: techniques
tags: [seo-marketing, text-optimization, meta-tags, title, h1, description, tf-idf, bm25, content-brief]
level: 4
source_sha256: a9e0a64d88e859f416e64cd4f3bcdbe99a72d90e406037e2c330cdcc4ef2297a
translation: machine
translated_at: '2026-10-24'
---
# Textoptimierung {#text-optimization}

Dokumenttextzonen, Regeln für Meta-Tags, Berechnung der Textrelevanz (TF-IDF, BM25), Workflow des Text-Analyzers und Erstellung von Content-Briefs. Behandelt sowohl traffic-orientierte als auch positionsorientierte Optimierungsstrategien.

## Berechnung der Textrelevanz {#text-relevance-calculation}

### TF-IDF {#tf-idf}
- **TF (Term Frequency)** - Verhältnis der Vorkommen eines Wortes zur Gesamtzahl der Wörter im Dokument
- **IDF (Inverse Document Frequency)** - Kehrwert der Häufigkeit, mit der ein Wort über alle Dokumente hinweg vorkommt
- Hoher TF-IDF-Wert = Wort ist in EINEM Dokument häufig, aber in der Sammlung selten
- Stoppwörter (Präpositionen, Konjunktionen) kommen überall vor -> sehr niedriger TF-IDF-Wert

### BM25 {#bm25}
Verbesserte Ranking-Funktion, die von Yandex aktiv eingesetzt wird:
- Bessere Relevanzberechnung für Mehrwort-Anfragen als TF-IDF
- Berücksichtigt NICHT die Position der Wörter zueinander
- Wird aktiv in den Ranking-Algorithmen von Yandex verwendet

### Quorum-Filterung und Wortreihenfolge {#quorum-filtering-and-word-order}
- Dokumente müssen ausreichende Passage-Abdeckung (Quorum) aufweisen, um in das Haupt-Ranking zu gelangen
- Paarweise Wortvorkommen (AB) und die vollständige Menge (ABC) werden getrennt gezählt
- Seltenere Wörter in der Anfrage haben ein höheres Gewicht
- Die Wortreihenfolge im Dokument sollte der Struktur der Anfrage entsprechen

## Zwei Optimierungsstrategien {#two-optimization-strategies}

### Traffic-Optimierung {#traffic-optimization}
**Geeignet für**: E-Commerce, Aggregatoren, Portale

- Maximale Abdeckung eines breiten semantischen Kerns
- Viele MF/LF-Anfragen statt Positionen für einzelne HF-Anfragen
- Wachstumstreiber: Erstellung und Optimierung neuer Landingpages
- Massenproduktionscharakter der SEO

**Iteration**: Semantik in erster Näherung -> Struktur für Hauptbereiche -> Erstellung aller möglichen Seiten -> Template-Optimierung -> detaillierte Semantik pro Kategorie -> manuelle Optimierung pro Kategorie -> Wiederholung.

### Positionsoptimierung {#positional-optimization}
**Geeignet für**: Dienstleistungsseiten, B2B, Bauwesen, Transport, Recht

- Maximales Positionswachstum bei einem kleinen Keyword-Set
- HF-Anfragen sind besonders wichtig
- Wachstumstreiber: iterative Verbesserung eines festen Seitensets
- Präziser, zielgerichteter Charakter der SEO

**Iteration**: Vollständige Semantik -> vollständige Struktur -> Erstellung aller Seiten -> manuelle Optimierung, Iteration 1 -> Veröffentlichung, Abwarten, Monitoring -> Korrekturen, Iteration 2 -> Wiederholung.

## Dokumenttextzonen {#document-text-zones}

| Zone | Tag | Einfluss auf das Ranking | Hinweise |
|------|-----|----------------|-------|
| Titel | `<title>` | Am höchsten | Wichtigste SEO-Zone |
| H1 | `<h1>` | Sehr hoch | Eine pro Seite, Hauptanfrage |
| H2-H6 | `<h2>`, `<h3>` | Hoch | Strukturierende Überschriften |
| Description | `<meta description>` | Nur CTR (nicht Ranking) | Optimierung der Klickrate |
| Ankertext | `<a>` | Hoch für Spender und Empfänger | Interne und externe Links |
| Textfragmente | Kleiner Text im Body | Mittel | Tabellen, Merkmale, Navigation |
| SEO-Text | Haupttext im Body | Mittel | Hauptsächlich verfasster Text |
| Keywords-Meta | `<meta keywords>` | Keiner | Wird ignoriert; löschen, wenn spamverdächtig |
| noindex-Blöcke | `<!--noindex-->` | Entfernung | Nur Yandex |

## Regeln für den Title-Tag {#title-tag-rules}

### Allgemeine Regeln {#general-rules}
- Wichtigste SEO-Zone
- Genaue Aufnahme der wichtigsten Anfragen
- Wichtigste Anfrage am Anfang
- Ein Satz, NICHT durch Punkt getrennt
- Yandex: bis zu 20 Wörter; Google: bis zu 12 Wörter
- Synsets (Synonymgruppen) verwenden
- Primären regionalen Toponym hinzufügen
- Einzige Zone, in der grammatikalische Kongruenz nicht kritisch ist

### Traffic-Title {#traffic-title}
Maximale Abdeckung von Anfragen:
```text
Buy fridge in Moscow, prices for fridges, online store Brand
```

**Vorlagenformel:**
```text
Buy %Category.Nom.Sg% in %City.Prep% online, prices for %Category.Nom.Pl%.
Sale of %Category.Gen.Pl%.
```

Regeln: Synonyme, Transliterationen, Permutationen; genaue Keyword-Form zugunsten der Breite opfern; Wortreihenfolge > Wortform; 2 Vorkommen des Hauptworts in unterschiedlichen Formen.

### Positions-Title {#positional-title}
Maximale Position bei konkreten Anfragen:
```sql
PVC windows from manufacturer - Moscow
```

Regeln: genaue Keyword-Vorkommen werden "wörtlich" eingefügt; fast keine Tail-Anfragen; Muster von starken Wettbewerbern übernehmen; kürzer als der Traffic-Title; 1 Vorkommen des Hauptworts.

### Artikel-Title {#article-title}
Klicks und Informationsabsicht:
```text
Simple recipe for cottage cheese pancakes with step-by-step photos
```

Regeln: Keyword-Aufnahme + Clickbait; aufmerksamkeitsstarke Formulierung; Lösungen der Wettbewerber prüfen.

## H1-Tag {#h1-tag}
- Muss EINMAL pro Seite vorkommen, oberhalb des Inhalts platziert
- Nur die Hauptanfrage (vorzugsweise in exakter Form)
- Kurz, grammatikalisch korrekt
- Nicht mit anderen Tags verunreinigt (`<p>` innerhalb von H1 = schlecht)

## Meta-Description {#meta-description}
- NICHT im Browser sichtbar (nur im Code)
- Fließt NICHT in die Textrelevanz ein
- Zweck: Erhöhung der CTR des SERP-Snippets
- Länge: 120-170 Zeichen (Yandex), bis zu 300 Zeichen (Google)
- Beide Schlüsselvorkommen sollten in 170 Zeichen passen
- 2-3 Sätze; 1 Keyword pro Satz
- Sonderzeichen: unicode-table.com

## noindex-Tag (nur Yandex) {#noindex-tag-yandex-only}
```html
<!--noindex-->content to hide<!--/noindex-->
```
Verbietet die Indexierung eines beliebigen Seitenabschnitts. Funktioniert NICHT bei Google.

## Text-Analyzer (TA) {#text-analyzer-ta}

**Zweck**: Referenzwerkzeug vor dem Schreiben JEDES SEO-Textes.

**Was er leistet**:
- Analysiert Wettbewerbstexte aus den TOP-Ergebnissen
- Ermittelt die sichere Anzahl von Keyword-Vorkommen je Typ
- Zeigt, ob überhaupt ein Text benötigt wird
- Erstellt das Content-Brief nahezu automatisch
- Prüft alle Dokumentzonen auf Keyword-Spam

**Tool**: Rush Analytics Text-Analyzer

### Anforderungen an den TA {#ta-requirements}
- Clustering: HARD-Modus mit Schwellenwert 3
- Seiten anderen Typs von der Analyse ausschließen
- Synonyme verwenden; NICHT einzelne Anfrage analysieren
- Optimal bis zu 6 Anfragen (mehr verwässert die Ergebnisse)
- KEINE LF-Anfragen einbeziehen - sie verzerren die Ergebnisse
- SERP der Zielregion verwenden

## SEO-Text auf kommerziellen Seiten {#seo-text-on-commercial-sites}

- Die Anforderungen des Text Analyzers strikt befolgen
- Genaue Anzahl der Keyword-Vorkommen und Textumfang einhalten
- Manchmal wird Text tatsächlich nicht benötigt
- Gleichmäßige Keyword-Dichte im gesamten Text
- Kommerzielle Wörter (kaufen, Preis, bestellen) nicht übermäßig verwenden
- Thematische LSI-Wörter einbeziehen, keine Füllwörter
- **OHNE ANALYSE DURCH DEN TEXT ANALYZER - NICHT SCHREIBEN**

### Spannung zwischen Yandex und Google bei Text {#yandex-vs-google-text-tension}
Google belohnt große, optimierte Texte; Yandex kann JEDEN Text auf kommerziellen Seiten bestrafen.

**Wenn Wettbewerber in den Yandex-TOP keinen Text haben -> optimierten Text nicht ohne Risiko verwenden.**

Umgehungslösungen, um Text nur Google zu zeigen:
- Text per JavaScript `document.write` ausgeben
- Text über den Google Tag Manager einfügen
- Über GTM: Canonical von einer Seite ohne Text auf die Kopie mit Text setzen

## Inhaltstypen nach Seite {#content-types-by-page}

### Produktlistings {#product-listings}
- Text nur schreiben, wenn der Text Analyzer es empfiehlt
- TA empfiehlt <100 Wörter -> Text NICHT nötig
- TA empfiehlt ~100-150 Wörter -> nur Generierung
- TA empfiehlt >150 Wörter -> vollständiger Text möglich
- Vorkommen im Ankerbereich `<a>` separat erfassen

### Regeln für die Generierung von Listings (Ära Baden-Baden) {#listing-generation-rules-baden-baden-era}
- 1 Vorkommen der Hauptanfrage
- 1-2 Vorkommen einzelner Wörter (voneinander entfernt verteilt)
- Kommerzielle Wörter NICHT in der Nähe der Anfrage schreiben
- 2-3 Sätze, insgesamt bis zu 100 Wörter
- Zusammenhängender, nützlicher Text

### Produktkarten {#product-cards}
- Textliche Einzigartigkeit NICHT kritisch
- Seiteneinzigartigkeit durch: generierten Text, Kundenbewertungen, Zubehörbereich
- Dieselben Generierungsregeln wie für Kategorieseiten

### Dienstleistungsseiten {#service-pages}
- Nur sinnvoller Text vom Texter
- NICHT generieren; verpflichtend: Text Analyzer verwenden
- Nur auf Grundlage des Content-Audits schreiben

### Informationsartikel {#informational-articles}
- Inhaltsverzeichnis, klare H1/H2/H3-Struktur
- LSI-Begriffe einbeziehen (nicht mehr als 50)
- ALLE nützlichen Punkte aller Wettbewerber abdecken + Zusätze
- Umfang: länger als jeder einzelne Wettbewerber
- Mehr Bilder, Video; Text/Bilder/Listen/Zitate abwechseln

## Aufbau des Texter-Briefs {#copywriter-brief-structure}

Ein vollständiges Brief muss enthalten:
1. Überschriftenstruktur (H2-H3 mit Zielkeywords)
2. Anweisungen für jeden Abschnitt
3. LSI-Keywords für jeden Absatz
4. Wort-/Absatzanzahl je Abschnitt
5. Links zu den besten Wettbewerbsbeispielen
6. Ausgabe des Text Analyzers mit hervorgehobenen Pflichtvorkommen

**Token-Anzahl**: 1 Wort = 1,3 Token; 1.000 Wörter = 1.300 Token.

## Checkliste zur Optimierung nach Seitentyp {#optimization-checklist-by-site-type}

| Zone | Traffic-Seite | Positions-Seite | Informativ |
|------|-------------|-----------------|---------------|
| Title | Template, breite Abdeckung | Exakte Übereinstimmung, kurz | Clickbait + Anfrage |
| H1 | Template oder manuell, exakt | Exakt, kurz | Natürliche Formulierung |
| Description | Template | Manuell, auf CTR ausgerichtet | Manuell, auf CTR ausgerichtet |
| SEO-Text | Nach TA; generiert, wenn kurz | Nach TA; Texter | Vollständiger Artikel |
| Überschriftenstruktur | Template h2/h3 | Manuell, semantisch | Umfangreich h2/h3/h4 |
| LSI-Wörter | Automatisch generiert | Nach TA | Umfangreich, 50 LSI |
| Content-Audit | Erforderlich | Erforderlich | Erforderlich |

## Stolperfallen {#gotchas}
- **Keywords-Meta-Tag bewirkt nichts** - löschen, wenn spamverdächtig, sonst ignorieren
- **Baden-Baden bestraft Keyword-Dichte** - vor dem Schreiben immer über den Text Analyzer prüfen
- **Keywords in Bold-/Strong-Tags signalisieren Manipulation** - `<b>`, `<strong>`, `<em>` nicht auf Keywords anwenden
- **Description beeinflusst das Ranking nicht** - nur die CTR; keine Keywords zur Rankingsteigerung einfügen
- **Der Konflikt zwischen Yandex und Google beim Text ist real** - der GTM/JS-Workaround ist eine gängige Praxis, kein Hack
- **Kommerzielle Tail-Wörter schaden** - "kaufen", "Preis", "bestellen" in der Nähe von Keywords lösen Spam-Erkennung aus

## Siehe auch {#see-also}
- [[keyword-research-semantic-core]] - Sammlung des semantischen Kerns und Clustering
- [[behavioral-factors-ctr]] - CTR-Optimierung über Snippets
- [[niche-content-audit]] - Methodik des Content-Audits
- [[filters-and-penalties]] - Details zu den Filtern von Baden-Baden
