---
title: "Seitenstruktur und URL-Architektur"
category: techniques
tags: [seo-marketing, site-structure, urls, nesting-level, click-depth, url-construction]
level: 3
source_sha256: 9644a0cb88d26f6c549b689b701f01331f08eb3865d2e1b8e3a747834237b0e2
translation: machine
translated_at: '2026-10-24'
---
# Seitenstruktur und URL-Architektur {#site-structure-and-url-architecture}

Prinzipien der Seitenhierarchie, Regeln für die URL-Konstruktion, Verschachtelungstiefen und Strukturvorlagen nach Website-Typ. Strukturfehler können ein Ranking verhindern, unabhängig von anderen Optimierungen.

## Prinzipien des Strukturaufbaus {#principles-of-structure-building}

Vier aufeinanderfolgende Schritte:
1. **Semantik sammeln** - alle Nachfragesegmente
2. **Visuelle Struktur aufbauen** - Mindmap vor der Umsetzung
3. **Wettbewerber analysieren** - Struktur der Marktführer ansehen (identische Struktur vermeiden - Risiko eines Affiliation-Filters)
4. **URL-Adressen vorbereiten** - URL-Baum erstellen

## Verschachtelungstiefe {#nesting-level}

**Definition**: Anzahl der Klicks von der Startseite bis zur Seite (NICHT die Anzahl der Schrägstriche in der URL).

### Regeln {#rules}
- Alle primär beworbenen Seiten: nicht tiefer als 3 Klicks von der Startseite
- Seiten für HF-Anfragen: idealerweise nicht tiefer als 2 Klicks
- Eine Seite von 5 auf 1 Klick zu verschieben kann sie von Top-20 auf Top-10 bringen

### URL-Verschachtelung vs. Klicktiefe {#url-nesting-vs-click-depth}
Die URL-Verschachtelung (Anzahl der Schrägstriche) entspricht NICHT der Klicktiefe:
- `site.ru/catalog/category/subcategory` - 3 Schrägstriche, könnten aber über ein Mega-Menü 2 Klicks sein
- Die URL-Verschachtelung beeinflusst das Ranking nicht direkt
- Die URL-Tiefe ist nützlich für die Analyse-Segmentierung (Filterung nach URL-Ordner in Metrica/GA)

## Struktur auf Basis der Semantik {#structure-under-semantics}

**Kernprinzip**: Semantik = ein fertiger Querschnitt der Nutzernachfrage. Seiten erstellen, um diese Nachfrage abzudecken.

- Cluster mit Frequenz > 0 und eindeutiger Suchabsicht -> eigene Seite erstellen
- Warnung: viele inhaltsleere oder dünne Seiten -> Hinweise auf "unzureichende Seitenqualität"
- Startseite = stärkste Seite; ihr den übergeordneten Cluster mit dem größten Umfang zuweisen
- Die Startseite muss Verlinkungen (Feeds) zu allen Bereichen der Website enthalten

### Trennung nach Informations- und Kaufabsicht {#informationcommercial-separation}
- **Kommerzielle Anfragen**: Kategorie-, Produkt- und Leistungsseiten
- **Informationelle Anfragen**: Blog, Artikel, FAQs
- **Super-Cards**: Produkt- bzw. Leistungsseiten mit tiefgehendem Inhalt, der beide Suchabsichten bedient

## Regeln für die URL-Konstruktion {#url-construction-rules}

### SEO-optimierte URLs (lesbar für Menschen) {#seo-optimized-urls-human-readable}
1. Für SEO sind menschenlesbare URLs Pflicht
2. Korrekte Transliteration verwenden (bei russischsprachigen Seiten keine englische Übersetzung)
3. Müssen die Wörter der Zielanfrage enthalten
4. Kommerzielle Wörter in der URL vermeiden (kaufen, Preis, bestellen)
5. Keyword-Wiederholung im URL-Pfad vermeiden:
   - SCHLECHT: `/baby-strollers/baby-strollers-for-newborns/`
   - GUT: `/baby-strollers/for-newborns/`
6. Zu lange URLs oder 6+ Schrägstriche vermeiden

### Beispiele für URL-Qualität {#url-quality-examples}
```yaml
BAD:  splav.ru/catalog.aspx?cat=20081113151601100150
OK:   secretpoint.ru/catalog/shoes/military/
GOOD: voentorga.ru/catalog/bertsy/
```

### Technische Anforderungen an URLs {#technical-url-requirements}
- Ausschließlich lateinische Zeichen
- Nur Buchstaben und Ziffern, keine Sonderzeichen
- Wörter ausschließlich durch Bindestrich trennen (keine Unterstriche)
- Nur Kleinbuchstaben; Großbuchstaben -> 301-Weiterleitung auf Kleinschreibung
- Relative URLs im Code verwenden
- Hauptspiegel: `https://site.ru/` (mit abschließendem Schrägstrich)
- Keine doppelten Pfadsegmente
- Nicht mehr als 2 Weiterleitungen; keine Ketten oder Endlosschleifen
- Alle Dev- und Staging-Umgebungen per HTTP-Authentifizierung schließen

## Strukturvorlagen nach Website-Typ {#structure-templates-by-site-type}

### E-Commerce {#e-commerce}
```text
/ (Homepage)
+-- /contacts/
+-- /about/
+-- /delivery/
+-- /blog/
|   +-- /blog/article-1/
+-- /catalog/
    +-- /catalog/category/           <- "Digital technology"
    |   +-- /catalog/category/sub/   <- "Laptops"
    |   +-- /catalog/category/brand/ <- "Laptops Asus"
    |   +-- /catalog/category/tag/   <- "Gaming laptops"
    +-- /catalog/product-card/       <- Product card
```

**Unterseiten für Produktkarten** (SEO-Kniff): Unterseiten erstellen, die jeweils einzeln optimiert werden:
- `/product/reviews/` - Bewertungen
- `/product/specifications/` - technische Daten
- `/product/photos/` - Fotos
- `/product/accessories/` - Zubehör mit H2-Zwischenüberschriften pro Typ

### Dienstleistungswebsite {#service-site}
```text
/ (Homepage)
+-- /contacts/
+-- /about/
+-- /blog/          (with anchor links to services)
+-- /services/
    +-- /services/service-1/
    +-- /services/category-1/
        +-- /services/category-1/service-3/
```

### Blog/Informationsseite {#bloginformational}
```text
/ (Homepage)
+-- /about/
+-- /section-1/
|   +-- /section-1/article-1/
+-- /section-2/
|   +-- /section-2/article-3/
+-- /tags/
```

## Instrumente der Klickstruktur {#click-through-structure-instruments}

### Startseite {#homepage}
- Stärkste Seite (höchstes Gewicht)
- Links zu wichtigen Seiten hinzufügen, um die Klicktiefe zu verringern
- Blöcke "Neuheiten" für die schnelle Indexierung neuer Seiten
- Wichtige Unterkategorien hervorheben, um ihr Gewicht zu erhöhen

### HTML-Sitemap {#html-sitemap}
- Für Nutzer zugängliche Seite mit Ankerlinks zu allen Bereichen
- Verringert die Klicktiefe: Hauptseite -> Sitemap (1 Klick) -> beliebiger Bereich (2 Klicks)
- Bei großen Websites: in mehrere Sitemaps nach Bereichen aufteilen
- Üblicherweise im Footer als "Sitemap" verlinkt
- Bis zu 1.000 interne Links pro Seite sind unproblematisch; maximal 5.000

### XML-Sitemap {#xml-sitemap}
- Technische Datei unter `yourdomain.ru/sitemap.xml`
- Enthält alle URLs + `lastmod`-Tags
- In Webmaster und Search Console einreichen
- Die Sitemap-URL immer in die robots.txt aufnehmen

### Seitenübergreifende Navigation {#cross-navigational-menu}
- Navigation in Kopf-, Fußzeile und Seitenleiste auf allen Seiten
- **Muss als `<a href>`-HTML-Tags umgesetzt sein** - nicht in JavaScript
- Reine JS-Navigation ist für Suchroboter unsichtbar

## Häufige Strukturfehler {#common-structure-errors}

1. **Fehler in der Brotkrumennavigation**: aktuelle Seite anklickbar (selbstreferenzierend), Titel in der Brotkrume (zu lang), Brotkrumen über JS (für Roboter unsichtbar)
2. **Zyklische Links**: Seite verlinkt auf sich selbst; verschwendet das Crawl-Budget
3. **Keyword-Kannibalisierung**: Hub-Seite konkurriert mit Unterseiten um dieselben Anfragen. Lösung: Hub umbenennen oder von der Indexierung ausschließen
4. **Keine primär beworbenen Seiten, die von der Startseite nicht erreichbar sind**
5. **Keine "hängenden Knoten"** - Seiten, die auf nichts verlinken
6. **Reine JS-Navigation** - Bots können ihr nicht folgen

## Ergebnisse der Strukturarbeit {#deliverables-from-structure-work}
1. Fertige Mindmap der Website
2. Dokument zur Klicktiefe
3. URL-Adresstabelle (URL-Hierarchie)
4. Menüschema und Anforderungen an die interne Verlinkung pro Seitentyp

## Fallstricke {#gotchas}
- **Die Klicktiefe ist weitaus wichtiger als die URL-Tiefe** - eine Seite unter `site.com/a/b/c/d/`, die 2 Klicks von der Startseite entfernt ist, rankt besser als eine Seite `site.com/x/`, die 5 Klicks tief vergraben ist
- **Identische Wettbewerberstruktur birgt das Risiko eines Affiliation-Filters** - Wettbewerber analysieren, aber sich abheben
- **Die HTML-Sitemap ist ein SEO-Instrument, nicht nur eine UX-Funktion** - sie steuert direkt die Crawl-Tiefe
- **JavaScript-Navigation ist unsichtbar** - alle kritischen Links müssen direkte HTML-`<a>`-Tags sein
- **Unterseiten für Produktkarten werden zu wenig genutzt** - separate Seiten für Bewertungen, technische Daten und Zubehör erschließen zusätzlichen Long-Tail-Traffic

## Siehe auch {#see-also}
- [[internal-linking]] - Methoden der Verlinkung, SILO, Paginierung
- [[keyword-research-semantic-core]] - Wie Cluster auf die Struktur abgebildet werden
- [[technical-seo-audit]] - Technische Prüfung der Struktur
- [[seo-strategy-by-site-type]] - Unterschiede der Struktur nach Website-Typ
