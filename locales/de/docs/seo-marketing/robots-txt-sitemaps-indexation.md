---
title: "robots.txt, Sitemaps und Indexierung"
category: techniques
tags: [seo-marketing, robots-txt, sitemap-xml, indexation, crawl-budget, indexnow, google-indexing-api]
level: 3
source_sha256: 42aad566216b7e3a57d6a86ff1a736224dc04e7014b0cdce77f6a4111e62a6c2
translation: machine
translated_at: '2026-10-24'
---
# robots.txt, Sitemaps und Indexierung {#robotstxt-sitemaps-and-indexation}

Detaillierte Darstellung der robots.txt-Konfiguration, der Anforderungen an sitemap.xml, der Indexierungsanalyse, der Optimierung des Crawl-Budgets und der Methoden zur erzwungenen Indexierung.

## robots.txt {#robotstxt}

### Anforderungen {#requirements}
- Drei getrennte Blöcke: Yandex, Google, andere Suchmaschinen
- Keine Ordner mit CSS- und JS-Dateien blockieren (Suchmaschinen müssen diese rendern können)
- Visuell auf Angemessenheit prüfen
- Immer die Sitemap-URL angeben

### Was disallowed werden sollte {#what-to-disallow}
```yaml
Disallow: /admin/                    # Admin panel
Disallow: /search/                   # Internal search results
Disallow: /?sort=                    # Sorting parameters
Disallow: /?results_on_page=         # Items per page
Disallow: /print/                    # Print pages
Disallow: /rss/                      # RSS feeds
Disallow: /?utm_                     # UTM parameters
```

### robots.txt vs. andere Direktiven {#robotstxt-vs-other-directives}
- **robots.txt** - steuert das Crawling (NICHT die Indexierung); spart Crawl-Budget; entfernt bereits indexierte Seiten nicht
- **Meta-robots-Tag** - steuert die Indexierung; `noindex` verwenden, um sie zu verhindern
- **X-Robots-Tag** - HTTP-Header für Nicht-HTML-Dokumente (PDF usw.)

### `clean-param` für GET-Parameter verwenden {#use-clean-param-for-get-parameters}
Anstatt jede Parametervariante in robots.txt zu blockieren, unterstützt Yandex die Direktive `clean-param`, um URL-Varianten zusammenzuführen.

## sitemap.xml {#sitemapxml}

### Anforderungen {#requirements_1}
- Erreichbar unter `https://site.ru/sitemap.xml`
- Enthält nur Seiten mit 200 OK
- Maximal 50.000 URLs pro Sitemap-Datei
- Maximal 10 MB pro Sitemap-Datei
- Mehrere Sitemaps -> eine Sitemap-Index-Datei erstellen
- Keine in robots.txt blockierten URLs
- Alle URLs verwenden den Haupthost (ohne www), https:// und abschließenden Schrägstrich
- Jede URL erscheint nur einmal
- Dynamisch generiert (muss bei jeder Anfrage aktuell sein)
- Muss `lastmod`-Tags mit korrekten Datumsangaben enthalten
- In Yandex Webmaster und Google Search Console einreichen

## Indexierungsanalyse {#indexation-analysis}

### Vorgehen {#process}
1. Website mit Screaming Frog crawlen
2. Ausgeschlossene/indexierte Seiten aus Yandex Webmaster herunterladen (max. 50.000)
3. Zwei Listen vergleichen: was auf der Website vorhanden ist vs. was nicht im Index ist
4. Grund für jede nicht indexierte Seite analysieren

### Prüfung der Verschachtelungstiefe {#nesting-level-check}
1. Mit Screaming Frog crawlen
2. Nach Verschachtelungstiefe sortieren
3. Alles mit mehr als 5 Ebenen Tiefe -> analysieren
4. Wenn Seiten mit Traffic tief vergraben sind -> Sitemap erstellen oder Struktur überarbeiten

### Prüfungen zur Indexierbarkeit {#indexation-accessibility-checks}
- Auf Meta-`noindex` und `nofollow` prüfen
- Auf Canonical-Tags prüfen (die auf eine andere Seite verweisen)
- X-Robots-Tag in HTTP-Headern
- In robots.txt blockierte Seiten

### Google Supplemental Index {#google-supplemental-index}
Ein minderwertiger sekundärer Index. Viele Seiten dort schaden dem Gesamtranking.

**Hauptursachen**:
1. Inhaltsduplikate - am häufigsten
2. Fehlerhafte interne Verlinkung, die zu geringem Seitengewicht führt
3. Zu kurze oder spammige Texte; automatisch generierte, unlesbare Inhalte

## Optimierung des Crawl-Budgets {#crawl-budget-optimization}

### Last-Modified- / If-Modified-Since-Header {#last-modified-if-modified-since-headers}
- **Häufiger Fehler**: Änderungsdatum bei jeder Anfrage auf die aktuelle Uhrzeit setzen
- **Korrekt**: nur aktualisieren, wenn sich der Inhalt tatsächlich ändert
- **Vorteile**: schnellerer Seitenaufbau, geringere Serverlast, Änderungsdatum in den SERPs, schnellere Indexierung

### Serverlog-Analyse {#server-log-analysis}
Screaming Frog Log File Analyser verwenden, um:
- Weiterleitungen zu finden, auf die Suchmaschinen-Bots treffen
- Am häufigsten und am seltensten gecrawlte URLs zu finden
- Nicht gecrawlte URLs und verwaiste Seiten zu finden
- Zu blockierende Bots zu identifizieren
- Crawl-Häufigkeit mit der Bedeutung der Seite zu korrelieren

## Erzwungene Indexierung {#forcing-indexation}

### Google Indexing API {#google-indexing-api}
- Große Mengen an Seiten ohne Entwickler hinzufügen
- Kann Seiten auf Websites indexieren, zu denen kein Search-Console-Zugang besteht
- Dienstkonten, die einmal erstellt wurden, sind für jede Website wiederverwendbar
- Am besten geeignet für umfangreiche Seitenerweiterungen

### Yandex IndexNow {#yandex-indexnow}
- Über neue, geänderte oder gelöschte Seiten benachrichtigen
- IndexNow-Plugins für gängige CMS verwenden
- In den meisten Fällen löst eine korrekte interne Verlinkung alle Indexierungsprobleme bei Yandex

### Weitere Methoden {#other-methods}
- URL in der URL-Prüfung der Google Search Console einreichen
- In Yandex Webmaster einreichen
- Sicherstellen, dass Seiten von indexierten Seiten aus verlinkt sind (interne Verlinkung behebt die meisten Probleme)

## Stolperfallen {#gotchas}
- **robots.txt blockiert das Crawling, nicht die Indexierung** - eine in robots.txt blockierte Seite kann trotzdem in Suchergebnissen erscheinen, wenn andere Seiten darauf verlinken
- **Statische Sitemaps veralten** - immer dynamisch generieren; eine veraltete Sitemap ist schlimmer als keine
- **lastmod muss korrekt sein** - alle Seiten auf das heutige Datum zu setzen, verringert die Crawl-Effizienz
- **Frühere Dienstleister hinterlassen oft fehlerhafte robots.txt-Regeln** - zu Projektbeginn immer manuell prüfen
- **Der Supplemental Index in Google ist ein Warnsignal** - viele Seiten dort deuten auf qualitative Probleme der gesamten Website hin
- **IndexNow garantiert keine Indexierung** - es beschleunigt nur die Entdeckung; die Qualität entscheidet weiterhin darüber, ob eine Seite indexiert wird

## Siehe auch {#see-also}
- [[technical-seo-audit]] - Vollständiges Audit-Framework inklusive robots.txt
- [[core-web-vitals-performance]] - Performance, die das Crawl-Budget beeinflusst
- [[site-structure-urls]] - Struktur, die die Crawl-Tiefe beeinflusst
- [[seo-analytics-reporting]] - Überwachung der Indexierungsmetriken
