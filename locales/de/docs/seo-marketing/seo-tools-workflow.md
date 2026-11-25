---
title: "SEO-Tools und Workflow"
category: reference
tags: [seo-marketing, tools, screaming-frog, ahrefs, wordpress, tilda, browser-extensions, ai-workflow]
level: 3
source_sha256: 1c5deb582105fcce323892f74fddcaf53521e1d32c10a2fe43127d1860429353
translation: machine
translated_at: '2026-10-24'
---
# SEO-Tools und Workflow {#seo-tools-and-workflow}

Vollständiger Tool-Stack für die SEO-Arbeit, CMS-Integration (WordPress, Tilda), Browser-Erweiterungen, Integration von KI-Workflows und Standardarbeitsanweisungen.

## Analytics-Plattformen {#analytics-platforms}

### Yandex Metrika {#yandex-metrika}
- Primäre Traffic-Analyse für das RU-Segment
- Zentrale Berichte: Traffic-Quellen, Absprungrate, Verweildauer, Zielkonversionen
- Webvisor: Sitzungsaufzeichnung für die Verhaltensanalyse
- Segmentierung nach Kanal (organisch/bezahlt/direkt/Empfehlung)
- Ziele einrichten für Leads, Anrufe, Käufe
- Liefert yandex-spezifische Daten, die anderswo nicht verfügbar sind

### Google Analytics (GA4) {#google-analytics-ga4}
- Unverzichtbar für die Analyse des Google-Traffics
- Zentrale Kennzahlen: Sitzungen, Nutzer, Engagement-Rate, Konversionen
- Integration mit der GSC für Daten auf Suchanfragen-Ebene
- Zielgruppenanalyse für die Content-Strategie

### Yandex Webmaster {#yandex-webmaster}
- Crawl- und Indexierungsstatus für Yandex
- Suchanfragen-Statistik: Impressionen, Klicks, CTR, durchschnittliche Position
- Fehlerberichte: 404er, Crawl-Blockaden, Weiterleitungsketten
- Sitemap.xml einreichen; regionale Zuordnung
- Turbo-Seiten für Mobilgeräte

### Google Search Console {#google-search-console}
- Abdeckungsbericht: indexierte vs. ausgeschlossene Seiten
- Performance: Suchanfragen, Impressionen, Klicks, CTR, Position
- Monitoring der Core Web Vitals
- Linkberichte, manuelle Maßnahmen
- URL-Prüfung für den Status einzelner Seiten

## Positions-Tracking {#position-tracking}

### Rush Analytics {#rush-analytics}
- Positions-Tracking für den russischen Markt (täglich/wöchentlich)
- Suchanfragen nach Clustern gruppieren; Sichtbarkeit nach Kategorie verfolgen
- Wettbewerbsvergleich; automatische Berichte planen

### Serpstat {#serpstat}
- Multifunktional: Tracking + Keyword-Recherche + Wettbewerbsanalyse
- Domain-Analyse; Backlink-Analyse; Site-Audit
- Stapelweise Analyse mehrerer Domains

### Alternativen {#alternatives}
SE Ranking, TopVisor – Positionsmonitoring mit anpassbarer Frequenz, White-Label-Berichte.

## Keyword-Recherche-Tools {#keyword-research-tools}

### Yandex Wordstat {#yandex-wordstat}
- Primäre Quelle für Suchvolumen im RU-Segment
- Operatoren für weite, Phrasen- und exakte Übereinstimmung
- Regionsfilter; saisonale Verlaufsdaten
- Browser-Erweiterung zur Anzeige der Häufigkeit direkt in der Suche

### Google Keyword Planner {#google-keyword-planner}
- Google-Suchvolumen (oft als Spannen, nicht als exakte Werte)
- Keyword-Ideen; Google-spezifische Nachfragemuster

### Key Collector (Desktop) {#key-collector-desktop}
- Massenhaftes Parsen von Wordstat mit Automatisierung
- Filterung von Stoppwörtern, Deduplizierung
- Mehrstufige Erfassung der Häufigkeiten
- Export nach Excel/CSV für die Verwaltung des semantischen Kerns

### Ahrefs / SEMrush {#ahrefs-semrush}
- Internationale Keyword-Datenbanken
- Schätzungen des Wettbewerber-Traffics
- Backlink-Analyse (Ahrefs am stärksten)
- Content-Gap-Analyse

## Tools für technische Audits {#technical-audit-tools}

### Screaming Frog SEO Spider {#screaming-frog-seo-spider}
- Desktop-Crawler, der Googlebot nachahmt
- Findet: 404er, Weiterleitungsketten, doppelte Titel, fehlende H1, Canonical-Probleme, übergroße Bilder
- Export nach Excel; kostenlos bis 500 URLs, kostenpflichtig unbegrenzt
- PageSpeed-API-Integration für die stapelweise CWV-Analyse
- Benutzerdefinierte Suche mit Regex für bestimmte Muster
- **Für große Websites**: Installation auf einem dedizierten Server, Crawl kann mehrere Tage dauern

### PageSpeed Insights / Lighthouse {#pagespeed-insights-lighthouse}
- Core Web Vitals: LCP, FID/INP, CLS
- Bewertungen für Mobil vs. Desktop
- Konkrete Verbesserungsempfehlungen

## Browser-Erweiterungen {#browser-extensions}

| Erweiterung | Zweck |
|-----------|---------|
| SEO Meta in 1 Click | Titel, Beschreibung, H1–H6, Canonical, Robots für jede Seite |
| Yandex Metrika Helper / Google Tag Assistant | Prüfung der Installation des Analytics-Codes |
| MozBar / Ahrefs Toolbar | Schnelle DA/PA-Schätzungen, Backlink-Anzahl in der SERP |
| Redirect Path | Weiterleitungsketten und Statuscodes |
| Web Developer | JS/CSS deaktivieren, um die Seite wie ein Robot zu sehen |
| User-Agent Switcher | Bot-Crawling simulieren |
| WordStatter / WordStat Assistant | Wordstat-Erfassung im Browser |

## CMS: Tilda {#cms-tilda}

### SEO-Einrichtung {#seo-setup}
- Zuerst Google Tag Manager verbinden -> Metrika, GA und GSC-Verifizierung ausrollen
- Seitenebene: Einstellungen -> SEO -> Titel, Beschreibung, Canonical, Noindex-Schalter
- Website-weit: Domain-Verbindung, HTTPS, www-Weiterleitung
- sitemap.xml und robots.txt: automatisch generiert (HTTPS-Checkbox verwenden)
- Lazy Load: aktiviert lassen (beeinflusst CWV)
- Individuelle 404-Seite: Vorlage erstellen, in den Einstellungen zuweisen

### Einschränkungen {#limitations}
- Beliebiges HTML im `<head>` ist nur mit Umwegen einfügbar
- Einschränkungen beim JS-Rendering im Vergleich zu einem vollwertigen CMS
- Geeignet für KMU, niedriger bis mittlerer Wettbewerb
- Funktioniert für die regionale Promotion außerhalb der Großstädte

## CMS: WordPress {#cms-wordpress}

### Ersteinrichtung {#initial-setup}
1. Installation über das Hosting-Panel
2. Plugins installieren: Yoast SEO (oder RankMath), Rus2Lat (URLs transliterieren)
3. Permalinks: "Post name" oder "Category/Post name"
4. Google Tag Manager im Theme-Header

### SEO pro Seite {#per-page-seo}
- Titel: Feld "SEO title" in Yoast/RankMath (getrennt von der H1)
- Beschreibung: Feld "Meta description"
- URL-Slug: keyword-basiert aus einer vorab erstellten Liste
- Canonical- und Noindex-Schalter verfügbar

### Architektur {#architecture}
- Seiten: zeitlos (Kontakt, Über uns, Leistungen)
- Beiträge: Blogartikel mit Kategorien
- Kategorien: können als Landingpages mit SEO-Metadaten dienen

## HTML-Grundlagen für SEO {#html-basics-for-seo}

### Wesentliche Tags {#essential-tags}
- `<title>` – Seitentitel in den Suchergebnissen
- `<meta name="description">` – Beschreibung des Snippets
- `<h1>` bis `<h6>` – Überschriftenhierarchie (eine H1 pro Seite)
- `<a href="">` – Hyperlinks
- `<img src="" alt="">` – Bilder mit Alt-Text
- `<p>`, `<ul>`, `<ol>`, `<li>` – Absätze und Listen

### Was im Code zu prüfen ist {#what-to-check-in-code}
- Titel und Beschreibung vorhanden und korrekt
- Eine einzige H1, die dem Ziel-Keyword entspricht
- Alt-Attribute für Bilder vorhanden
- Kein versehentliches `noindex`, das Seiten blockiert
- Canonical zeigt auf die richtige URL
- HTTPS auf allen Seiten; www-Normalisierung

### Relevanz von CSS/JS {#cssjs-relevance}
- CSS: Layout-Verschiebungen (CLS) beeinflussen die Core Web Vitals
- JS: Yandex rendert anders als Google; kritische Seiten sollten nicht von JS abhängen
- Umfangreiches JS verzögert die Indexierung

## KI-Tools im SEO {#ai-tools-in-seo}

### Integration von ChatGPT / Claude {#chatgpt-claude-integration}
**Wirksame Prompt-Struktur**: Kontext + Ziel + Rahmenbedingungen.
- Schlecht: "Wie verbessere ich die SEO?"
- Gut: "Welche Strategien erhöhen den organischen Traffic für einen E-Commerce-Shop für Damenmode auf einem umkämpften regionalen Markt?"

**Anwendungsfälle**:
- Entwürfe für Meta-Tags (Varianten für Titel/Beschreibung)
- Content-Briefings für Texter
- Zusammenfassungen von Wettbewerbsanalysen
- Erklärungen technischer Audits für Kunden
- Erstellung von FAQ-Abschnitten
- Erzeugung von Schema.org-Markup
- Aufbau von Ankertext-Listen aus Wettbewerbsdaten

Englische Prompts liefern oft bessere technische Antworten. Iterieren: Die erste Ausgabe ist ein Entwurf, der durch Nachfragen verfeinert wird.

## Standard-Workflow {#standard-workflow}

### Checkliste für das Projekt-Onboarding {#project-onboarding-checklist}
1. Zugänge: Webmaster, GSC, Metrika, GA4
2. Positions-Tracking: Suchanfragen in Rush Analytics konfigurieren
3. Ausgangs-Crawl: vollständiges Screaming-Frog-Audit -> Fehler dokumentieren
4. Ausgangs-Metriken: aktueller Traffic, Positionen, Indexierung
5. GTM installiert und funktionsfähig

### Monatliche Berichterstattung {#monthly-reporting}
- Positionsdynamik: Anzahl Top-10, Top-3
- Organischer Traffic: Sitzungen im Vergleich zum Vormonat/Vorjahr
- Konversionen aus organischer Suche
- Veränderungen des technischen Zustands
- Durchgeführte Arbeiten + Plan für den nächsten Monat

### Workflow zur Seitenoptimierung {#page-optimization-workflow}
1. Ziel-Cluster aus dem semantischen Kern bestimmen
2. Wettbewerber in den Top 10 prüfen
3. Vorbereiten: H1, URL, Titel, Beschreibung, Content-Briefing
4. Im CMS umsetzen
5. URL in GSC/Webmaster zur Indexierung einreichen
6. Position verfolgen

## Zusammenfassung zur Tool-Auswahl {#tool-selection-summary}

| Aufgabe | Primär | Alternative |
|------|---------|-------------|
| Traffic-Analyse | Metrika + GA4 | - |
| Positions-Tracking | Rush Analytics | Serpstat, SE Ranking |
| Keyword-Recherche | Wordstat | Key Collector (Massenabfrage) |
| Technischer Crawl | Screaming Frog | Netpeak Spider |
| Backlinks | Ahrefs | Serpstat |
| Seitengeschwindigkeit | PageSpeed Insights | GTmetrix |
| Schnelle Seitenprüfung | SEO-Meta-Erweiterung | MozBar |
| Wettbewerbsanalyse | Serpstat | Keys.so |

## Stolperfallen {#gotchas}
- **Die kostenlose Version von Screaming Frog ist auf 500 URLs begrenzt** – für Websites mit mehr als 500 Seiten ist eine kostenpflichtige Lizenz unverzichtbar
- **Tilda hat eine SEO-Obergrenze** – geeignet nur für KMU, nicht für umkämpfte Nischen
- **WordPress-Permalinks müssen zum Start festgelegt werden** – spätere Änderungen erfordern die Verwaltung von Weiterleitungen
- **GTM ist die universelle Methode zur Bereitstellung von Analytics** – Tracking-Codes niemals direkt in Templates einfügen
- **KI-generierte Meta-Tags müssen von Menschen geprüft werden** – immer die Aufnahme der Keywords und die natürliche Sprache kontrollieren
- **Die tägliche Morgenprüfung (5–10 Min.) erkennt Probleme früh** – daraus eine nicht verhandelbare Gewohnheit machen

## Siehe auch {#see-also}
- [[seo-analytics-reporting]] - KPIs und Berichtsmethodik
- [[technical-seo-audit]] - Audit-Rahmenwerk mit diesen Tools
- [[keyword-research-semantic-core]] - Werkzeugeinsatz für die semantische Arbeit
- [[core-web-vitals-performance]] - Details zu PageSpeed und Lighthouse
