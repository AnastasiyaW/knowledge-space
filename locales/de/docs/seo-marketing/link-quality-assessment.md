---
title: "Bewertung der Linkqualität"
category: techniques
tags: [seo-marketing, link-quality, outreach, pbn, drop-domains, donor-evaluation, link-audit]
level: 3
source_sha256: 17219edacf8607fdba75916525fa65bd09eab3528e46d523bd0f1ec7e0b40981
translation: machine
translated_at: '2026-10-24'
---
# Bewertung der Linkqualität {#link-quality-assessment}

Kriterien zur Bewertung von Donoren, Outreach-Methodik, Nutzung von PBNs (Private Blog Networks), Strategien mit Drop-Domains und Verfahren für Link-Audits.

## Outreach {#outreach}

Direkter Kontakt mit Seiten, um die Platzierung eines Artikels mit Link zu kaufen bzw. zu verhandeln.

**Vorteile**: Bringt Anfragen aktiv in die TOP; verbessert die gesamte Seite durch autoritative Links; gute Indexierung.

**Nachteile**: teuer; zeitaufwendig; schwer zu kontrollieren; ca. 20 % Betrugsrisiko.

### Kriterien zur Donor-Auswahl {#donor-selection-criteria}
- Aktive Dynamik des Linkwachstums in Ahrefs
- Nischenrelevant oder angrenzend + Medien
- DR >= 20, Traffic >= 1000, Index >= 100 Seiten
- Keine Spam-Nischen (Adult, Pharma) im Index
- Keine Beiträge mit der Kennzeichnung „Sponsored Content“ / „Werbung“
- Hat Anfragen aus Ihrer Nische in den TOP
- Gutes Design (kein Stil der 90er)
- Hochwertige eingehende Links aus dem Content
- Keine Spam-Wörter im Quelltext
- Hochwertiger Content, regelmäßige neue Artikel
- Nicht ausschließlich zum Verkauf von Links erstellt

## Dynamische Sitewide-Links {#dynamic-sitewide-links}

Ein Donor setzt von verschiedenen Seiten aus unterschiedliche Links auf Ihre Seite, mit wechselnden Ankertexten.

### Setup-Regeln {#setup-rules}
- 10–20 Links auf eine Ihrer Seiten (von verschiedenen Donor-Seiten)
- Unterschiedliche Ankertexte pro Query-Cluster
- 1 Link pro Ankertext/Query
- ~30 % Dilution für Google (URL, Marke, Toponym)
- Keine doppelten Links auf einer Donor-Seite
- Nicht von ALLEN Donor-Seiten aus verlinken
- Maximal 3–4 „Nachbar“-Seiten pro Donor-Seite
- Donor muss autoritativ sein: Portale, Nachrichtenseiten, regionale Seiten

## PBN (Private Blog Network) {#pbn-private-blog-network}

Verwaltetes Netzwerk von Seiten zur Stärkung der Hauptdomain.

### Wann einsetzen {#when-to-use}
- Schwarze/graue Nischen
- Hart umkämpfte Nischen
- Punktuelles Boosting für HF/Ultra-HF-Queries in weißen Nischen
- Für die meisten Nischen im RU-Markt nicht profitabel

### Qualitätsanforderungen {#quality-requirements}
- PBN: DR 5, TF 8, CF/TF > 1,8; Web-Archiv bevorzugt
- Money-Site: DR 15, TF 15, CF/TF > 2
- Glue: ähnlich wie PBN, etwas niedriger bei stark nischenspezifischen Seiten

### Regeln {#rules}
- PBN-Volumen <= 10–30 % des gesamten Linkprofils (nur punktuelles Boosting)
- Links müssen organisch zur Seite passen
- Kein PBN auf jungen Seiten ohne Dilution, besonders in den ersten 6 Monaten
- Keine günstigen Netzwerke von nicht verifizierten Webmastern kaufen

## Strategien mit Drop-Domains {#drop-domain-strategies}

### Was Drop-Domains sind {#what-drop-domains-are}
Zuvor bestehende, aber aufgegebene Domains mit Restwert: Alter, Vertrauen, Backlinks, Query-Index.

### 301-Weiterleitung / Glue {#301-redirect-glue}
Weiterleitung von der Drop-Domain auf Ihre Seite. Überträgt Links, Alter und Vertrauen.

**Zweck**: Gesamten Host mit Linkmasse stärken; Domainalter übertragen; beworbene Seite stärken; Vertrauen bei Google erhöhen.

**Auswahlkriterien**:
- Starke Domain mit Links aus schwer zugänglichen Quellen (.gov, Nischenseiten, Konkurrenzseiten)
- Stark nischenrelevant (oder sehr autoritativ und angrenzend)
- Idealerweise Auktionsdomain (Alter bleibt erhalten)
- Domain ist im Index und rankt

### Testprotokoll vor der Anwendung {#testing-protocol-before-applying}
1. Domain kaufen
2. Konkurrenten in den TOP 20–30 für Ihre Queries finden
3. Positionen des Konkurrenten verfolgen
4. Weiterleitung auf den Konkurrenten einrichten (so, wie Sie sie auf sich selbst anwenden würden)
5. 2–4 Wochen beobachten
6. Bei Wachstum -> Weiterleitung auf Ihre Seite
7. Bei keiner Reaktion -> nicht verwenden
8. Wenn der Konkurrent abfällt -> Weiterleitung entfernen, Domain verwerfen

### Einrichtung der Weiterleitung {#redirect-setup}
- Antibot-.htaccess auf der Drop-Domain installieren (Crawler zunächst blockieren)
- 301: Startseite -> Startseite; andere Seiten -> Startseite ODER nach Weiterleitungsplan
- Seiten mit den stärksten Links manuell weiterleiten
- Option: thematisch passende Drop-Domain auf die passende Kategorie weiterleiten

### Fundorte {#where-to-find}
- mydrop.io, expired.ru, reg.ru, nic.ru, dropmonitor.ru
- Web-Archiv-Auswertung über rush-analytics.ru
- Backlink-Auswertung autoritativer Seiten
- SERP-Auswertung (Top 100 für Keywords -> Domains extrahieren -> WHOIS prüfen)

### Bewertung von Drop-Domains {#drop-domain-evaluation}
1. Die Top 10–15 Links manuell auf Erreichbarkeit prüfen
2. Links zeigen direkt (keine Ketten)
3. Dofollow >= 60 %
4. Auf chinesische Zeichen prüfen (Hinweis auf Wiederverwendung)
5. Auf Link-Explosionen prüfen
6. Pharma, Glücksspiel, Essays, Einzelhandel -> überspringen
7. Viele Ankerlinks -> überspringen
8. Web-Archiv vorhanden -> gut; Themenwechsel-Historie prüfen
9. Anzahl der Drops: mehr als 2 Resets -> schlecht
10. IKS und Query-Index über Keys.So prüfen

## Link-Audit {#link-audit}

### Was zu prüfen ist {#what-to-check}
1. Anzahl (Links, Hosts)
2. Spam- und SEO-Anker (nach Hosts)
3. Dynamik des Linkwachstums (besonders bei SEO-Links)
4. Mit Spam überflutete Donoren, die aktiv an Börsen handeln
5. Defekte Seiten, Xrumer-Links, versteckte Links
6. **Besondere Aufmerksamkeit für neue Links**

### Automatische Erkennung von Link-Spam {#auto-detection-of-link-spam}
1. Export aus Ahrefs + GSC: 1 Link pro Domain
2. Prüfung in Screaming Frog (mit Browser-Emulation):
   - Custom Search: Regex für Ihre Domain-Links
   - Custom Search: Spam-Wörter (`viagra|payday|porn`)
3. Ablehnung über das Google Disavow Tool

Alternative: Abschnitt „Spam in links“ in Rush-Analytics PBN

## Checkliste zur Donor-Qualität {#donor-quality-checklist}

### Artikel-Links (Yandex + Google) {#article-links-yandex-google}
- IKS >= 50 (Prüfung: be1.ru/yandex-iks/)
- Google-Traffic über Ahrefs >= 5.000
- Preis <= 1.000–1.500 RUB
- TF >= 5 (Majestic.com)
- Nische: Thema, angrenzend, Zeitungen, Medien, Portale
- Indexierung > 1.000 Seiten (Operator `site:`)
- Spam-Prüfung: `site:site.com "spam words"` – Ergebnisse prüfen
- Verbleibende nach Traffic oder IKS sortieren; manuell prüfen:
  - Seite erreichbar, regelmäßig frische Artikel
  - Nicht alle Artikel kommerziell
  - Ahrefs: ausgehende Links überschreiten nicht die indexierten Seiten
  - Ahrefs-UR der bezahlten Artikel != 0

### Forum-Links {#forum-links}
- Google-Traffic über Ahrefs >= 100
- Indexierung > 1.000 Seiten
- Spam-Prüfung (wie bei Artikel-Links)
- Forum aktiv mit regelmäßig neuen Themen
- Bezahlte Themen sollten nicht überwiegen
- Foren finden: `inurl:forum OR inurl:showthread [keyword]`

## Linkbörsen {#link-exchange-platforms}

Marktplätze für den Kauf von ewigen (einmaligen) oder gemieteten Links.

**Regeln**:
- Manuelle Donor-Auswahl ist Pflicht
- Ankertexte und Dynamik auf Basis der Konkurrenz planen
- Keine Links für mehr als 1.500–2.000 RUB kaufen
- Empfehlungen der Börse nicht befolgen
- Kein „Link-Boosting“ verwenden (Börse schickt Bots -> Penalty-Risiko)

**Plattformen (RU)**: Miralinks, GGL, pr.Sape

## Tools zur Linkanalyse {#link-analysis-tools}

| Tool | Zweck |
|------|-------|
| Ahrefs | Vollständige Backlink-Datenbank, Ankeranalyse, Dynamik, Kennzahlen |
| MegaIndex | Kostenlos (RU): Verhältnis SEO- zu organischen Links (>40–50 % SEO = Warnung) |
| LinkPad | Backlink-Analyse für den RU-Markt |
| Majestic | Trust Flow / Citation Flow Kennzahlen |

## Stolperfallen {#gotchas}
- **Drop-Domains immer zuerst an einem Konkurrenten testen** – eine ungetestete Weiterleitung auf Ihre Seite kann Rankings massiv einbrechen lassen
- **20 % Betrugsrate im Outreach** – Donor-Qualität vor der Zahlung unabhängig prüfen
- **PBN sollte nie mehr als 30 % des Linkprofils ausmachen** – nur für punktuelles Boosting verwenden
- **Chinesische Zeichen im Web-Archiv = Domain wurde wiederverwendet** – meist geringe Qualität
- **Mehr als 2 Domain-Drops/Resets = toxisch** – diese Domains überspringen
- **Empfehlungen von Linkbörsen sind unzuverlässig** – Donoren immer manuell auswählen

## Siehe auch {#see-also}
- [[link-building-strategy]] - Gesamtstrategie für Links und Zusammensetzung der Anker
- [[filters-and-penalties]] - Minusinsk- und Penguin-Penalties durch schlechte Links
- [[seo-analytics-reporting]] - Linkverfolgung in Monatsberichten
- [[seo-tools-workflow]] - Ahrefs und Tools zur Linkanalyse
