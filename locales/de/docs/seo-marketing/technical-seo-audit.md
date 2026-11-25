---
title: "Technisches SEO-Audit"
category: techniques
tags: [seo-marketing, technical-audit, hosting, duplicates, response-codes, crawl-budget, screaming-frog]
level: 3
source_sha256: 3ec7731532a6bb80cb4591f49fc3ba15b9686087604c33348e85c2a371f690a7
translation: machine
translated_at: '2026-10-24'
---
# Technisches SEO-Audit {#technical-seo-audit}

Umfassendes Framework für technische Audits mit Priorisierung, doppelten Seiten, HTTP-Statuscodes, Hosting-Anforderungen, Inhaltsvalidierung und CMS-Entwicklungsanforderungen.

## Priorisierungsframework für Audits {#audit-prioritization-framework}

### Prioritätsstufen {#priority-levels}
1. **Fehler, die die Indexierung von Seiten blockieren** - Hosting-Probleme, JS-Rendering, Mirrors/Canonicals, doppelte Seiten
2. **Fehler, die die korrekte Indexierung von Inhalten blockieren** - JS wird nicht gerendert, Markup-Probleme
3. **Fehler, die das Ranking von Seiten blockieren** - doppelte Tags, defekte Links, doppelter Inhalt, zu tiefe Verschachtelung, überoptimierter Inhalt
4. **Sonstiges** - Korrekturen mit niedrigerer Priorität

### Priorisierungsregeln {#priority-rules}
- Aufgaben priorisieren, die die größte Anzahl an Seiten betreffen
- Fehlerhafte Weiterleitungen bei Seitennavigation (hohe Priorität) vor fünf defekten Links, die auf 404-Seiten zeigen (niedrige Priorität)
- Neues Title-Template ausrollen (hohe Priorität) vor der Aktualisierung der HTML-Sitemap (niedrige Priorität)
- Das für die Umsetzung benötigte Budget des Kunden berücksichtigen; ergebnisrelevante Aufgaben zuerst umsetzen

### Priorität nach Websitegröße {#priority-by-site-size}
- **Kleine Websites (<50 Seiten)**: niedrige Priorität - Fehler haben kaum Auswirkungen
- **Mittlere Websites**: mittlere Priorität
- **Große Websites (50.000+ Seiten)**: kritisch - ein einziger struktureller Fehler kann Tausende Seiten vom Index ausschließen

## Einrichtung und Monitoring {#setup-and-monitoring}

### Proaktives Monitoring {#proactive-monitoring}
1. Top-1000-Suchanfragen aus Metrika -> Positionsverfolgung
2. Dieselben Suchanfragen -> Yandex Webmaster Favorites
3. Top-100-Traffic-Seiten -> "Wichtige Seiten" im Webmaster
4. Webmaster-Benachrichtigungen konfigurieren
5. Meta-Scanner (Rush Analytics) für die tägliche Erkennung von Seitenänderungen anbinden
6. robots.txt nicht überladen; für GET-Parameter `clean-param` verwenden

### Meta-Scanner {#meta-scanner}
Erfasst Ausgangszustände von Seiten, bevor sich Änderungen auf den Traffic auswirken:
- Überwacht: Title, Description, H1, URL, Meta robots, Canonical, robots.txt, Textinhalt
- Push-Benachrichtigung bei Abweichungen
- Verhindert Traffic-Verluste durch unbemerkte Änderungen von Entwicklern

### Hosting-Anforderungen {#hosting-requirements}
- **HTTP/2**: Prüfen unter `http2.pro/`; Hoster zur Aktivierung kontaktieren
- **SSL/TLS**: Prüfen unter `ssllabs.com/ssltest/`; TLS 1.2 empfehlen; DNS-CAA-Policy konfigurieren
- **Lasttests**: `loadimpact.com`
- **Stabilität**: Metrika-Benachrichtigungen einrichten

## Doppelte Seiten {#duplicate-pages}

### Typen und Lösungen {#types-and-solutions}

| Duplikat-Typ | Lösung |
|----------------|----------|
| www vs. non-www | Hauptmirror wählen, 301-Weiterleitung |
| http vs. https | 301-Weiterleitung auf https |
| Trailing Slash | Prüfen, was rankt, 301-Weiterleitung |
| Startseiten-Varianten (`/index.html`) | 301-Weiterleitung auf die Startseite |
| Groß-/Kleinschreibung (`/Page` vs. `/page`) | 301-Weiterleitung auf Kleinschreibung |
| Sortierungsparameter bei Produkten (`?sort=price`) | In robots.txt sperren oder per JS umsetzen |
| Paginierungsduplikate | Separate Meta-Templates für Seite 2 und folgende |
| Produkt in mehreren Kategorien | Canonical-Tags oder Weiterleitung |
| Technische Subdomains (old., dev.) | Von der Indexierung ausschließen oder per HTTP-Auth schützen |
| Druckseiten (`/print/`) | In robots.txt sperren |
| UTM-Parameter | In robots.txt mit Disallow sperren |

### Duplikate finden {#finding-duplicates}
- Yandex Webmaster (Bereich doppelte Seiten)
- Screaming Frog SEO Spider
- Suchoperatoren: `site:domain.ru`

## HTTP-Statuscodes {#server-response-codes}

### Erforderliches Verhalten {#required-behavior}
- **200 OK** - alle gültigen Seiten
- **301** - permanente Weiterleitung (für SEO immer verwenden, nie 302)
- **404** - defekte Seiten müssen tatsächlich 404 zurückgeben (nicht 200)
- **503** - während Wartungsarbeiten (nicht 403 oder 502)
- **500** - nicht akzeptabel, sofort beheben

### Linkqualität {#link-quality}
- Keine Links auf 3xx-/4xx-Seiten bei einem vollständigen Crawl der Website
- Keine defekten Links im Screaming-Frog-Crawl

## Grundlegende Zusammenführungen (auf jedem Projekt erforderlich) {#basic-merges-required-on-every-project}

Alle Weiterleitungen per 301 auf die kanonische URL:
1. `http://` -> `https://` (SSL erforderlich)
2. `www.domain.ru` -> `domain.ru` (eine Variante wählen, die andere per 301 weiterleiten)
3. `domain.ru/page/` -> `domain.ru/page` (Normalisierung des Trailing Slash)
4. `domain.ru/Page` -> `domain.ru/page` (Normalisierung der Großschreibung)

Jede Variante mit der Browser-Erweiterung Redirect Path prüfen.

## Prüfungen des Inhalts {#content-audit-checks}

### Versteckter Text {#hidden-text}
1. Styles und Skripte deaktivieren
2. 5–10 Seiten jedes Typs prüfen
3. Versteckter relevanter Text DARF verwendet werden, aber NIEMALS über `display:none`
4. Mobile-First: Inhalte in Spoilern/Collapsibles erhalten KEINE Gewichtungsabwertung (von Google bestätigt)

### Inhaltsqualität {#content-quality}
- 5–10 Seiten pro Typ auf Einzigartigkeit prüfen (content-watch.ru für Stapelprüfungen)
- Spam/automatische Generierung: auf inkonsistenten Text, Keyword-Stuffing und Spam mit semantischen Tags achten
- Generierter Text muss statisch sein

### Markup-/Layout-Audit {#markuplayout-audit}
- JS und CSS deaktivieren, prüfen: Inhalte, Preise und Fotos sind sichtbar
- Styles in .css-Dateien (keine Inline-Styles); JS in externen Dateien
- Maximal 20 externe CSS-/JS-Dateien pro Seite
- Standard-Zeichensatz: UTF-8

## Abwehr von Parsing {#anti-parsing-defense}

### Unwirksame Methoden {#ineffective-methods}
- Einschränkungen anhand des User-Agents (leicht zu umgehen)
- Länder-/Providersperren (verlieren echten Traffic)
- CAPTCHA (wird umgangen, verärgert Nutzer)

### Wirksame Methoden {#effective-methods}
1. **Fingerprinting** - Clientbewertung anhand mehrerer Parameter
2. **Traffic-Klassifizierung** - gute Bots, schlechte Bots, Browser, verdächtige Zugriffe
3. **Rate Limiting** - pro Minute, pro Sitzung, nach Dauer
4. **ML-/statistische Klassifizierung** - Mustererkennung
5. **Behavioral Biometrics** - Mausbewegungen, Geräteausrichtung

### Blockieren gefälschter Bot-Scraper {#blocking-fake-bot-scraping}
**Validierung per Reverse DNS**:
1. Bot gibt sich als GoogleBot/YandexBot aus -> IP extrahieren
2. Reverse DNS -> Hostname ermitteln
3. Prüfen: Google = `googlebot.com`/`google.com`; Yandex = `yandex.ru`/`.net`/`.com`
4. Forward DNS: Hostname -> IP
5. Stimmen die IPs nicht überein -> gefälschter Bot -> blockieren

## CMS-/Entwicklungsanforderungen {#cmsdevelopment-requirements}

- Title, Description, H1, SEO-Text: unabhängig pro Seite UND über Templates bearbeitbar
- Alt- und Title-Attribute für Bilder: einzeln und über befüllbare Templates
- Nutzer und Robots sehen identische Inhalte; kein versteckter Text im Quellcode
- Bei deaktiviertem JS: Links zu allen Seiten sind von der Startseite aus erreichbar
- favicon.ico im Wurzelverzeichnis der Website
- Statische Ressourcen: gzip-Komprimierung; Caching-Header von mindestens 3 Tagen; Cache-Busting per Zeitstempel
- Alle Dev-/Staging-Umgebungen per HTTP-Auth von robots ausschließen

## Werkzeuge {#tools}

| Werkzeug | Verwendung |
|------|-----|
| Screaming Frog SEO Spider | Vollständiger Crawl der Website: 404s, Weiterleitungsketten, doppelte Titles, fehlende H1, Canonical-Probleme |
| Screaming Frog Log File Analyser | Auswertung der Serverlogs: gecrawlte/nicht gecrawlte URLs, verwaiste Seiten, Bot-Identifikation |
| Redirect Path (Erweiterung) | Weiterleitungsketten für beliebige URLs prüfen |
| SEO in 1 Click (Erweiterung) | Meta-Tags, H1–H6 und Canonical der aktuellen Seite anzeigen |
| Web Developer (Erweiterung) | JS/CSS deaktivieren, um die Seite so zu sehen wie Robots |
| User-Agent Switcher | Bot simulieren, um das Rendering zu prüfen |
| Link Redirect Trace | Weiterleitungsketten verfolgen |

**Hinweis zur Infrastruktur**: Für das Crawlen großer Websites (hunderttausende Seiten) einen dedizierten Server beschaffen, Screaming Frog installieren und tagelang crawlen lassen.

## Zeitplan für Wiederholungsaudits {#repeat-audit-schedule}

| Projektgröße | Technisches Audit | Audit der Sichtbarkeit gegenüber Wettbewerbern |
|--------------|-----------------|---------------------------|
| Klein | Keine Wiederholung nötig | Alle 3–6 Monate |
| Mittel | Alle 3–6 Monate | Alle 3–6 Monate |
| Groß | Monatlich | Alle 3–6 Monate |

## Fallstricke {#gotchas}
- **robots.txt steuert das Crawling, nicht die Indexierung** - in robots.txt gesperrte Seiten können trotzdem im Index erscheinen, wenn sie von anderswo verlinkt sind
- **302-Weiterleitungen übertragen KEINE Ranking-Signale** - für dauerhafte Umzüge immer 301 verwenden
- **Frühere Dienstleister hinterlassen oft fehlerhafte robots.txt-Regeln** - vor allen anderen Arbeiten immer manuell prüfen
- **CloudFlare kann in Audit-Tools wie bertal.ru falsche 403-Antworten verursachen**
- **"Seitenqualität unzureichend" im Webmaster** bedeutet meist dünnen Inhalt auf automatisch generierten Seiten, nicht einen technischen Fehler
- **Änderungen durch Entwickler können SEO unbemerkt beschädigen** - der Meta-Scanner erkennt Probleme, bevor der Traffic einbricht

## Siehe auch {#see-also}
- [[robots-txt-sitemaps-indexation]] - robots.txt, sitemap.xml und Vertiefung zur Indexierung
- [[core-web-vitals-performance]] - Seitengeschwindigkeit und Core Web Vitals
- [[site-structure-urls]] - URL-Regeln und Validierung der Seitenstruktur
- [[seo-analytics-reporting]] - Monitoring und Diagnose-Workflow
