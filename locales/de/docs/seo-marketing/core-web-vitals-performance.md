---
title: "Core Web Vitals und Performance"
category: techniques
tags: [seo-marketing, core-web-vitals, lcp, cls, fid, mobile-first, spa, ssr, page-speed]
level: 4
source_sha256: e66f27d5b69833dae9697ceb2f1fb67c25a718c9c1c3549f48e159a6393b9733
translation: machine
translated_at: '2026-10-24'
---
# Core Web Vitals und Performance {#core-web-vitals-and-performance}

Signale der Seitenerfahrung, einschließlich Core-Web-Vitals-Metriken, Mobile-First-Indexierung, SPA/AJAX-Rendering-Lösungen und Workflow zur Performance-Analyse.

## Core-Web-Vitals-Metriken {#core-web-vitals-metrics}

| Metrik | Was sie misst | Schwellenwert „schlecht“ |
|--------|-----------------|---------------|
| LCP (Largest Contentful Paint) | Renderzeit des größten sichtbaren Elements | >= 4000ms |
| TBT (Total Blocking Time) | Blockierungszeit durch JS | >= 300ms |
| CLS (Cumulative Layout Shift) | Visuelle Stabilität (Werbeblöcke verschieben Inhalte) | >= 0.25 |
| FID (First Input Delay) | Interaktivität nach der ersten Interaktion | Veraltet, zugunsten von INP |
| INP (Interaction to Next Paint) | Reaktionszeit nach beliebiger Interaktion | Ersetzt FID |

**Googles Haltung**: Inhaltsqualität hat Vorrang vor der Seitenerfahrung. Die Seitenerfahrung kann relevante und nützliche Inhalte nicht ersetzen.

## Signale der Seitenerfahrung {#page-experience-signals}
- Core Web Vitals (LCP, FID/INP, CLS)
- Mobile Optimierung
- HTTPS
- Keine aufdringlichen Interstitials

## Analyse-Workflow {#analysis-workflow}

### 1. Screaming Frog mit PageSpeed API einrichten {#1-setup-screaming-frog-with-pagespeed-api}
- Configuration -> API Access -> PageSpeed Insights
- Dienstkonto erstellen, API-Schlüssel abrufen, PageSpeed Insights API aktivieren
- In Screaming Frog verbinden; Mobile oder Desktop wählen

### Verfügbare Datenkategorien {#available-data-categories}
- **Overview**: Seitengröße, HTML-Größe, CSS-Größe
- **CrUX Metrics**: reale Nutzerdaten aus Chrome (28-Tage-Durchschnitt)
- **Lighthouse Metrics**: Labordaten (LCP-, TBT-, CLS-Werte)
- **Opportunities**: Verbesserungsvorschläge pro Seite
- **Diagnostics**: Anzahl der DOM-Elemente, Performance-Details

### 2. Seiten filtern, die die Schwellenwerte überschreiten {#2-filter-pages-exceeding-thresholds}
- LCP >= 4000ms
- TBT >= 300ms
- CLS >= 0.25

### 3. Konkrete Probleme untersuchen {#3-investigate-specific-issues}
Seite anklicken -> PageSpeed Details -> Opportunities -> z. B. „Eliminate Rendering-Blocking Resources“ -> zeigt die URLs der blockierenden Ressourcen.

### 4. Wettbewerbsvergleich {#4-competitive-comparison}
- Screaming Frog -> Mode -> List
- Vergleichen: Startseite, Kategorieseite, Produktkarte der eigenen Website sowie der wichtigsten Wettbewerber
- Export -> vergleichende Analyse
- **Ziel: den Nischendurchschnitt erreichen, nicht perfekte Werte**

## Mobile-First-Indexierung {#mobile-first-indexation}

- Google indexiert die mobile Version zur Bewertung im Ranking
- Mobile und Desktop-Inhalte auf Übereinstimmung prüfen
- Alle Seitentypen müssen die Tests zur mobilen Optimierung bestehen
- Adaptives Markup für PC, Tablets und Smartphones erforderlich
- Nur am Desktop vorhandene Inhalte, die auf Mobilgeräten nicht sichtbar sind, werden möglicherweise nicht indexiert

## SPA/AJAX-Websites {#spaajax-sites}

### Problem {#problem}
- SPA (Single Page Application): Das Rendering erfolgt clientseitig über JS
- Von Google gut indexiert (mit Problemen), von Yandex schlecht indexiert
- Technologien: Angular, React, Vue, Elm

### Lösung: Server-Side Rendering (SSR/Prerendering) {#solution-server-side-rendering-ssrprerendering}
Der Bot erhält statisches HTML, die Nutzer erhalten die JS-Version. Yandex hat bestätigt: Die Auslieferung unterschiedlichen HTMLs an Bots stellt keinen Verstoß dar, sofern sie nicht darauf abzielt, Nutzer zu täuschen.

### Was im gerenderten HTML enthalten sein muss {#what-must-be-in-rendered-html}
- Standard-Meta-Tags
- Grafische Inhalte mit allen Meta-Tags
- Interne und externe Links mit allen Attributen
- Textinhalte mit Formatierung
- Navigationsmenüs und -elemente
- Mikrodaten (OpenGraph, Schema.org)

### Prüfen, was der Bot sieht {#checking-bots-view}
1. User-Agent Switcher mit YandexBot/Googlebot aktivieren
2. JS deaktivieren (Erweiterung Web Developer)
3. Seiten öffnen, Inhalte im Quelltext mit STRG+U prüfen
4. In Yandex Webmaster prüfen
5. In der Google Search Console prüfen
6. In der gespeicherten Kopie (Cache) prüfen

### Prerender-Dienste {#prerender-services}
- prerender.io
- getseojs.com
- phantomjs.org
- SEO.js
- HtmlUnit

## Bildoptimierung {#image-optimization}

### Anforderungen an Dateinamen {#naming-requirements}
- Standardformate: .jpg, .png
- Alle Bilder im Ordner `/images/`
- Dateiname: transliterierte H1-Überschrift (Kleinbuchstaben, durch Bindestriche getrennt)
- Attribut `alt`: gleiche Vorlage wie der Dateiname (in der Originalsprache)
- Attribut `title`: identisch mit alt
- Alle Bilder vorab für Geschwindigkeit optimieren (häufigste Ursache für schlechte Werte)

## Performance-Tools {#performance-tools}

| Tool | Zweck |
|------|---------|
| PageSpeed Insights | Core-Web-Vitals-Metriken pro Seite |
| Google Lighthouse | Labordaten und Verbesserungsempfehlungen |
| Screaming Frog + PageSpeed API | Stapelweise CWV-Analyse der gesamten Website |
| GTmetrix | Alternatives Tool für Geschwindigkeitstests |

## Grundprinzip {#key-principle}

**Perfekte PageSpeed-Werte nicht um jeden Preis anstreben**, denn das kostet Zeit und Budget. Ziel ist der Nischendurchschnitt. Wenn Wettbewerber 40–50 Punkte erreichen, sind 95 nicht nötig.

## Stolperfallen {#gotchas}
- **CWV ist ein Tiebreaker, kein primäres Ranking-Signal**: Inhaltsqualität und Relevanz schlagen Geschwindigkeit immer
- **CrUX-Daten setzen Traffic voraus**: Neue Seiten oder Seiten mit wenig Traffic haben keine realen Nutzerdaten, nur Labordaten
- **Bilder sind die Hauptursache für langsame Seiten**: Bilder optimieren, bevor CSS/JS angefasst wird
- **Mobile-First bedeutet, dass Mobile der primäre Index ist**: Funktionen oder Inhalte, die nur am Desktop vorhanden sind, können vollständig ignoriert werden
- **SPA-Websites werden von Yandex schlecht indexiert**: SSR/Prerendering ist Pflicht, nicht optional
- **Inhalte unter Spoilern/Akkordeons zählen voll**: Google hat bestätigt, dass für mobilfreundliche aufklappbare Inhalte keine Abwertung erfolgt

## Siehe auch {#see-also}
- [[technical-seo-audit]] - Vollständiges Audit-Framework
- [[robots-txt-sitemaps-indexation]] - Indexierung und Crawl-Budget
- [[seo-tools-workflow]] - Tool-Stack für die Performance-Analyse
- [[search-engine-mechanics]] - Wie technische Faktoren ins Ranking einfließen
