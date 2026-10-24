---
title: "Verhaltensfaktoren und CTR-Optimierung"
category: techniques
tags: [seo-marketing, behavioral-factors, ctr, snippets, micromarkup, schema-org, click-factors]
level: 4
source_sha256: 4fb4abdb1e4fc70b74c02dbf07d3e268cb3b9d220623378a6b40acdedbc75c4f
translation: machine
translated_at: '2026-10-24'
---
# Verhaltensfaktoren und CTR-Optimierung {#behavioral-factors-and-ctr-optimization}

Analyse von Verhaltensfaktoren, Snippet-Optimierung für die CTR und die Implementierung von Schema.org-Micromarkup. Verhaltensfaktoren sind die stärkste Gruppe von Ranking-Signalen bei Yandex.

## Verhaltensfaktoren {#behavioral-factors}

### Definition {#definition}
Analyse der realen Aktionen von Besuchern auf der Website. Eine der stärksten Gruppen von Ranking-Faktoren, besonders bei Yandex (Priorität #1).

### Datenquellen {#data-sources}
- Eigene Analyse der SERP-Positionen der Suchmaschine
- Analysesysteme (Yandex Metrika, Google Analytics)
- Browser
- Daten der Yandex-Toolbar „Bars"

### Faktoren-Hierarchie {#factor-hierarchy}
```text
Query-document factors > Document factors > Host factors
```

Wichtige Merkmale:
- Wirken auf organischen Traffic
- Wirken praktisch nicht bei niederfrequenten Anfragen
- Query-Dokument-Faktoren haben den größten Einfluss
- Keine universellen Richtwerte – jede Nische hat eigene Werte (E-Commerce: hohe Zeit und tiefes Browsing; Taxi: minimale Zeit ist normal)

## Arten von Verhaltensfaktoren {#types-of-behavioral-factors}

### Extern (SERP-seitig / Klickfaktoren) – STARKER Einfluss {#external-serp-side-click-factors-strong-impact}
- CTR des Dokuments und der Domain nach Anfrage in den organischen Ergebnissen
- Letzter Klick in den organischen Ergebnissen
- Einziger Klick in den Ergebnissen
- Rückkehr zur Suche
- Durchschnittliche Zeit bis zum Klick auf das Dokument
- Durchschnittliche Anzahl der Klicks in der SERP pro Anfrage

### Intern (auf der Website / nach dem Klick) – SCHWACHER Einfluss {#internal-on-site-post-click-weak-impact}
- Anzahl langer Klicks (>60 Sekunden)
- Anteil langer Klicks (nicht weniger als der Website-Durchschnitt)
- Durchschnittliche Verweildauer auf der Seite pro Anfrage
- Durchschnittliche Sitzungsdauer in Sekunden
- Gesamte Zeit auf der Website über alle Anfragen

### Einfluss nach Stärke {#impact-by-strength}
1. **Klicks in der SERP** (extern) = stark, pro Anfrage schwer zu beeinflussen
2. **Verhalten auf der Website** (intern) = schwach, leichter zu beeinflussen
3. **Auffinden dessen, wonach gesucht wurde** (Conversion = letzter Klick) = am stärksten, am schwersten zu beeinflussen

## Was optimiert werden sollte {#what-to-optimize}

**Extern**: CTR, Conversion (letzter Klick)

**Intern**: Absprungrate, Zeit auf Dokument/Website, Browsingtiefe, zufriedene Schritte, lange Klicks

### Analysewerkzeuge {#analysis-tools}
- **Extern**: Yandex Webmaster, Google Search Console. Fokus: Anfragen in den Top 10 mit hohen Impressionen, aber niedriger CTR
- **Intern**: Yandex Metrika, Google Analytics. Fokus: Seiten, die vom Durchschnitt abweichen; Auswertung nach Browser- und Gerätesegmenten
- **Wettbewerb**: SimilarWeb (nicht geeignet für kleine Nischen; Daten sind ungefähr, zeigen aber Muster)

## CTR-Optimierung über Snippets {#ctr-optimization-via-snippets}

### Yandex-Snippet – 4 Einflusszonen {#yandex-snippet-4-influence-zones}
1. **Titel** – manchmal verwendet Yandex stattdessen die Überschrift H1–H3
2. **Breadcrumbs** – automatisch generiert, begrenzte Kontrolle
3. **Beschreibung** – über Meta-Description, manchmal übernimmt Yandex den Seitentext
4. **Erweiterte Merkmale** – Bewertungen, Preise, Schnelllinks

**Zusätzliche Verbesserungen für Yandex**:
- Emoji in der Beschreibung: 5 Sterne am Anfang erscheinen häufig im Snippet
- Yandex Business Directory mit Bewertungen erweitert das Snippet der Startseite
- Schnelllinks: automatisch von Yandex generiert, schwer zu kontrollieren
- Produkte/Preise: Webmaster-Erweiterung; zeigt Lieferung und Preis

### Google-Snippet – 3 Einflusszonen {#google-snippet-3-influence-zones}
1. **Breadcrumbs** – über Schema.org BreadcrumbList
2. **Titel**
3. **Beschreibung** – über Meta-Description

**Zusätzliche Verbesserungen für Google**:
- Micromarkup Product: Preisspanne, Produktmenge
- Rating: Teil von Product, aber auch eigenständig nutzbar
- FAQ: Frage-Antwort-Block mit Micromarkup für erweitertes Snippet
- How-to: schrittweise Anleitungen (JSON-LD und Microdata)
- Nischenspezifische erweiterte Snippets (siehe Google-Dokumentation)

### Workflow zur CTR-Optimierung {#ctr-optimization-workflow}

**Große/mittlere Projekte**:
1. Template-Lösung implementieren
2. Snippet-Verlauf speichern
3. CTR-Veränderungen in den Webmaster-Panels verfolgen
4. Negative Auswirkung -> schnell zurückrollen
5. Templates weiter testen

**Kleine Projekte**: Gleicher Ablauf, aber Prioritätsseiten manuell korrigieren.

## Schema.org-Micromarkup {#schemaorg-micromarkup}

### Definition {#definition_1}
HTML-Seitenmarkup mit speziellen Attributen gemäß den Standards der jeweiligen Suchmaschine. Ermöglicht Robotern, Seiteninhalte besser zu verstehen und relevantere Ergebnisse auszuliefern.

### Vorteile {#benefits}
- Strukturiert Daten für Suchmaschinen-Roboter
- Verbessert die Attraktivität des Snippets -> erhöht die CTR
- Erweiterte Snippets verbessern Verhaltensfaktoren -> Positionswachstum
- Hilft Robotern, Produkt/Preis von Kommentaren/Spezifikationen zu unterscheiden

### Vokabulare {#vocabularies}
- **Schema.org** – am weitesten verbreitet, unterstützt von Google, Yandex, Yahoo, Bing
- **OpenGraph** – von Facebook; wird für Vorschauen in sozialen Medien genutzt (VK, Twitter, LinkedIn)
- **Microformats** – kleine HTML-Vorlagen für Personen, Veranstaltungen, Texte

### Syntaxen {#syntaxes}

**Microdata** – markiert Daten im HTML:
```html
<div itemscope itemtype="http://schema.org/BreadcrumbList">
  <div itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem">
    <a href="https://example.com" itemprop="item">
      <span itemprop="name">Home</span>
    </a>
  </div>
</div>
```

**JSON-LD** – Daten im `<script>`-Tag:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1,
     "item": {"@id": "https://example.com/category", "name": "Category"}}
  ]
}
</script>
```

**Regel für den GUS-Markt**: Microdata verwenden; Ausnahme = Breadcrumbs (JSON-LD möglich). JSON-LD eignet sich nur für Google (Yandex rendert es bei den meisten Typen nicht in den Ergebnissen).

### Wichtigste Typen {#primary-types}

| Typ | Anwendungsfall |
|-----|----------------|
| BreadcrumbList | Navigations-Breadcrumbs |
| Organization / LocalBusiness | Kontaktdaten, Unternehmensinformationen |
| Product / AggregateOffer / AggregateRating | Produkte und Angebote |
| FAQ / QA / HowTo | Frage-Antwort-Blöcke und Anleitungen |
| Article / NewsArticle | Artikel und Nachrichten |
| Review | Bewertungen und Rezensionen |
| OpenGraph | Vorschauen in sozialen Medien |

### Minimale OpenGraph-Tags {#opengraph-minimum-tags}
- `og:title`, `og:description` (optional), `og:image`, `og:type`, `og:url`

### Validierungswerkzeuge {#validation-tools}
1. Google Rich Results Test
2. Google Search Console
3. Yandex-Webmaster-Validator
4. Schema.org-Validator

## Manipulation von Verhaltensfaktoren {#behavioral-factor-manipulation}

**NICHT manipulieren**:
- Wird von Suchmaschinen leicht erkannt
- Strafe = Sperre der Website für 6–8 Monate (härteste Sanktion)
- Es gibt keine sicheren Manipulationsdienste im öffentlichen Zugang
- 99,99 % Sperrwahrscheinlichkeit bei Automatisierung

**Regeln**:
- Niemals Dritten Zugriff auf Webmaster/Metrika geben
- Schneller Ausweg aus der Sperre: 301-Weiterleitung auf eine andere Domain (aber riskant)
- **Fazit: Verhaltensfaktoren niemals manipulieren**

## Stolpersteine {#gotchas}
- **Verhaltensfaktoren sind bei Yandex Nr. 1, bei Google Nr. 3** – pro Suchmaschine unterschiedlich optimieren
- **JSON-LD funktioniert bei Yandex für die meisten Typen nicht** – für den GUS-Markt Microdata verwenden
- **Es gibt keine universellen Richtwerte** – jede Nische legt ihre eigenen „guten" Metriken fest
- **CTR-Optimierung kann nach hinten losgehen** – Snippet-Verlauf immer speichern und zum Zurückrollen bereit sein
- **SimilarWeb ist für kleine Nischen unzuverlässig** – für Websites mit wenig Traffic liegen keine Daten vor
- **Conversion = stärkstes Verhaltenssignal** – Qualität von Produkt/Dienstleistung zählt mehr als jeder Trick auf der Seite
- **Emoji in Beschreibungen müssen pro Nische getestet werden** – nicht grundsätzlich positiv

## Siehe auch {#see-also}
- [[commercial-ranking-factors]] – Kommerzielle Faktoren ergänzen Verhaltensfaktoren
- [[text-optimization]] – Meta-Description für die CTR
- [[search-engine-mechanics]] – Verhaltensfaktoren in der Ranking-Hierarchie
- [[filters-and-penalties]] – Strafen für Verhaltensmanipulation
