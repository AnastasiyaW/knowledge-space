---
title: "Suchmaschinen-Filter und Sanktionen"
category: reference
tags: [seo-marketing, filters, penalties, baden-baden, minusinsk, penguin, panda, ymyl]
level: 3
source_sha256: 741a4ceba15a28ba7bc5e63fc5b33593f608c2bac8933fd847114bf1115e97c8
translation: machine
translated_at: '2026-10-24'
---
# Suchmaschinen-Filter und Sanktionen {#search-engine-filters-and-penalties}

Vollständige Referenz zu Yandex- und Google-Filtern, ihren Auslösern, Symptomen, Diagnosemethoden und Wiederherstellungsverfahren.

## Diagnose bei Traffic-Einbruch {#traffic-drop-diagnostics}

Wenn die Analytics einen Traffic-Einbruch zeigen:
1. Prüfen, ob die Seite im Index ist: `url:site.ru/the-dropped-document/`
2. Gültigkeit der gespeicherten Kopie in der Suchmaschine prüfen
3. Verschachtelungsebene prüfen
4. Charakter des Einbruchs analysieren:
   - **Host eingebrochen** -> Sanktionen prüfen
   - **Seite eingebrochen** -> prüfen: relevante Seitenänderung, Dokumentsanktionen, Textprobleme, Linkprobleme

## Wofür Suchmaschinen bestrafen {#what-search-engines-penalize-for}
1. Probleme mit der Textqualität (Spam, dünner Inhalt)
2. Täuschung der Nutzer auf der Website
3. Manipulation von Verhaltensfaktoren
4. Zugehörigkeit: mehrere kommerzielle Websites desselben Inhabers
5. Linkmanipulation
6. Täuschung der Suchmaschine
7. Pornografische Inhalte, aufdringliche Werbung
8. Piraterie, Diebstahl von Inhalten

## Wo der Filterstatus geprüft wird {#where-to-check-filter-status}
- **Yandex Webmaster** -> Bereich "Violations"
- **Google Search Console** -> "Manual Actions"

### Arten des Filterumfangs {#filter-scope-types}
- Query-Dokument, Dokument, Domain, Entfernung von Seite/Bereich, Entfernung der Domain
- Nach Art: automatisch oder manuell

## Yandex-Filter {#yandex-filters}

### Baden-Baden {#baden-baden}
**Datum**: März 2017 | **Art**: automatisch | **Umfang**: Query-Dokument und Domain

**Auslöser**: Keyword-Density-Spam, übermäßiger Textumfang, versteckter Text, geringe Textqualität.

**Symptome**:
- Query-Ebene: deutlicher Abfall einer Query-Gruppe (nicht aller) um 5–40 Positionen; das Dokument rankt weiterhin für andere Queries
- Host-Ebene: deutlicher Abfall ALLER Queries um 20+ Positionen; nur markenbezogene Queries bleiben; Benachrichtigung im Webmaster

**Diagnose**: `arsenkin.ru/tools/filter/`; Massenabfall um 10+ Positionen = wahrscheinlich Baden-Baden.

**Entfernung**:
- Query-Ebene: zuerst `<noindex>`-Tag setzen, dann umschreiben; Anzahl der Keyword-Vorkommen und Textumfang reduzieren; wenn nichts hilft -> Text löschen
- Host-Ebene: **NUR TEXT LÖSCHEN** - nichts anderes funktioniert

### Minusinsk {#minusinsk}
**Datum**: Mai 2015 | **Art**: automatisch | **Umfang**: Domain

**Auslöser**: Linkmanipulation zur Förderung der Website.

**Was als SEO-Links gilt**: nahezu alle Ankerlinks auf die kommerzielle Website; 95 % der Links von bekannten Austauschbörsen; auch Nicht-Ankerlinks von Austauschbörsen.

**Entfernung**:
1. ALLE SEO-Links auf einmal entfernen
2. Auf die Neuindexierung der Spenderseiten warten
3. Der Filter wird nach 1–8 Monaten aufgehoben
4. Der Traffic stellt sich vollständig wieder her, wenn die Website von hoher Qualität ist
5. Der Yandex-Support kann Beispiele der erkannten Links zeigen

### Manipulation von Verhaltensfaktoren {#behavioral-factor-manipulation}
**Datum**: Juli 2011 | **Umfang**: Domain | **Art**: manuell oder automatisch

**Symptome**:
- Automatisch: -30–40 Positionen für die gesamte Website außer der Marke (ohne Benachrichtigung)
- Manuell: Benachrichtigung im Webmaster -> Diagnostik -> Sicherheit und Verstöße

**Merkmale**:
- Härteste Sanktionen bei Yandex
- Sperre wird 6–8 Monate NACH dem Eingeständnis der Manipulation aufgehoben
- **Schneller Ausweg**: 301-Weiterleitung auf eine andere Domain
- **Niemals Zugriff auf Webmaster/Metrika an Dritte geben**

### Clickjacking {#clickjacking}
**Datum**: Dezember 2015 | **Umfang**: Domain | **Art**: automatisch

**Auslöser**: unsichtbare Elemente, die Nutzerdaten ohne Einwilligung erfassen.

**Entfernung**: Nutzung ausbeuterischer Dienste beenden; im Webmaster auf "Ich habe alles behoben" klicken; Aufhebung innerhalb von 30 Tagen.

### Reputationsfilter {#reputation-filter}
**Datum**: Oktober 2021 | **Umfang**: Domain | **Art**: automatisch

**Auslöser**: negative Bewertungen, betrügerische Anrufe über SIP-Telefonie. Abfall um 15–30 Positionen.

### Affiliate-Filter {#affiliate-filter}
**Art**: manuell

**Auslöser**: 2 oder mehr kommerzielle Websites desselben Unternehmens für identische Produkte/Dienstleistungen.

**Vermeidung bei mehreren Websites**:
- Unterschiedliches Hosting/unterschiedliche Registrare
- Registrierung auf unterschiedliche Personen
- Unterschiedliches Sortiment und unterschiedliche Preise
- Unterschiedliche Konventionen für Produktbenennung
- Webmaster/Metrika auf unterschiedlichen Konten (anderer Rechner oder VM)
- Unterschiedliche Kontakte
- Werbung über unterschiedliche Konten

### Weitere Yandex-Filter {#other-yandex-filters}
- **Aufdringliche Abo-Benachrichtigungen** (Januar 2019)
- **Aggressive Werbung** (April 2019) - hauptsächlich Adsense-Monetarisierung; als Navigation getarnte Werbeblöcke

## Google-Filter {#google-filters}

### Google Panda {#google-panda}
**Datum**: Februar 2011 | **Umfang**: Dokument und Domain | **Art**: automatisch

**Auslöser**: minderwertiger Inhalt, gestohlene/doppelte Inhalte, interne Duplikate.

**Wiederherstellung**: Seiten ohne Traffic über GSC/GA finden; umschreiben (Copy-Paste und Spam entfernen); hochwertige Inhalte, Bilder, Videos ergänzen; moderierte UGC hinzufügen.

### Google Fred {#google-fred}
**Datum**: März 2017 | **Umfang**: Domain | **Art**: automatisch

**Auslöser**: geringe Inhaltsqualität, minderwertige Links, übermäßige Werbung, kein Mehrwert.

**Wiederherstellung**: Werbeblöcke reduzieren; Linkprofil verbessern; Mehrwertdienste ergänzen (Rechner, Tests).

### YMYL (Your Money or Your Life) {#ymyl-your-money-or-your-life}
**Datum**: August 2018 | **Umfang**: Domain | **Art**: automatisch

**YMYL-Nischen**: Finanzen, Medizin, Recht, Kindersicherheit, Verkehrssicherheit.

**Wiederherstellung über E-A-T**: Zertifikate, Nachweise/Belege, maßgebliche Links, Inhaltsqualität, Grammatik, Sortiment, Informationen zu Kauf/Lieferung.

### Google Penguin {#google-penguin}
**Datum**: April 2012 | **Umfang**: Query-Dokument | **Art**: automatisch

**Auslöser**:
- Große Anzahl kommerzieller Anker
- Unnatürliche Ankerverteilung (keine markenbezogenen Anker)
- Links nur auf die Startseite oder auf eine kleine Gruppe von Seiten
- Hoher Anteil gekaufter/minderwertiger Links

**Wiederherstellung**:
- Schlechte Links entfernen, Linkprofil ändern
- Links über den Host verteilen
- Anteil der Nicht-Ankerlinks auf über 20 % erhöhen
- Ankerspam mit Nicht-Ankerlinks verdünnen
- Schlechte Links über Google Disavow Links ablehnen

### Micromarkup-Spam {#micromarkup-spam}
**Datum**: 2016 | **Umfang**: Dokument | **Art**: automatisch

**Auslöser**: Missbrauch von Micromarkup zur Manipulation von Snippets. Alle Typen prüfen, unangemessenes Markup entfernen.

### DMCA (Piraterie) {#dmca-piracy}
**Datum**: 2012 | **Umfang**: Dokument

**Auslöser**: Kopieren von Inhalten anderer Websites. Nicht-einzigartige Inhalte löschen, Entfernung aus dem Filter beantragen.

### Exact Match Domain (EMD) {#exact-match-domain-emd}
**Datum**: 2012 | **Umfang**: Domain | **Art**: automatisch

**Auslöser**: kommerzielle Keyword-Phrase im Domainnamen. Behebung: Domain mit 301-Weiterleitung wechseln. Prävention: nicht mehr als ein Keyword in der Domain verwenden.

## Referenztabelle der Filter {#filter-reference-table}

| Filter | Suchmaschine | Umfang | Art | Hauptauslöser |
|--------|--------|-------|------|-------------|
| Baden-Baden | Yandex | Query-Dok/Domain | Auto | Text-Spam |
| Minusinsk | Yandex | Domain | Auto | Linkmanipulation |
| Clickjacking | Yandex | Domain | Auto | Unsichtbare Datenerfassung |
| Verhalten | Yandex | Domain | Manuell/Auto | Bots/bezahlte Klicks |
| Reputation | Yandex | Domain | Auto | Negative Bewertungen/Betrug |
| Affiliate | Yandex | Domain | Manuell | Mehrere Websites in derselben Nische |
| Panda | Google | Dok/Domain | Auto | Geringe Qualität/Duplikate |
| Fred | Google | Domain | Auto | Geringe Qualität + übermäßige Werbung |
| YMYL | Google | Domain | Auto | E-A-T-Defizit |
| Penguin | Google | Query-Dok | Auto | Link-Spam |
| Micromarkup | Google | Dokument | Auto | Markup-Manipulation |
| DMCA | Google | Dokument | - | Urheberrechtsverletzung |
| EMD | Google | Domain | Auto | Keyword-Domain |

## Fallstricke {#gotchas}
- **Baden-Baden auf Host-Ebene: NUR Text löschen** - Umschreiben funktioniert nicht, nur vollständige Entfernung
- **Minusinsk berechnet nach Hosts, nicht nach Seiten** - ein schlechter Link pro Domain zählt genauso viel wie 100
- **Manipulation von Verhaltensfaktoren ist die härteste Sanktion** - 6–8 Monate Sperre ohne Umgehungsmöglichkeit außer einem Domainwechsel
- **Der Affiliate-Filter erfordert strikte Trennung** - sogar Analytics auf demselben Konto können die Erkennung auslösen
- **Penguin wirkt auf Query-Dokument-Ebene** - einzelne Seiten können sich erholen, während andere weiterhin sanktioniert bleiben
- **EMD ist weiterhin relevant** - nicht mehr als ein kommerzielles Keyword im Domainnamen verwenden

## Siehe auch {#see-also}
- [[link-building-strategy]] - Linkstrategien, die Sanktionen vermeiden
- [[text-optimization]] - Textoptimierung innerhalb sicherer Grenzen
- [[behavioral-factors-ctr]] - Best Practices für Verhaltensfaktoren
- [[commercial-ranking-factors]] - E-A-T zur Wiederherstellung bei YMYL
