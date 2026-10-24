---
title: "SEO-Analytik und Reporting"
category: techniques
tags: [seo-marketing, analytics, kpis, reporting, position-tracking, traffic-analysis, monitoring]
level: 3
source_sha256: 92318ddc560a413f7ab81f85c9bc7e01149623922f9afb8a1dd8baf56e108f2a
translation: machine
translated_at: '2026-10-24'
---
# SEO-Analytik und Reporting {#seo-analytics-and-reporting}

Projektsteuerungssystem: KPI-Metriken, Struktur des monatlichen Reportings, Monitoring mit Meta-Scanner, Hypothesenbildung bei Traffic-Rückgängen und Aufgabenmanagement.

## Projekteinrichtung {#project-setup}

### Mit bestehender Historie {#with-existing-history}
1. Zugang einholen zu: Yandex Metrika, Yandex Webmaster, Google Analytics, Google Search Console
2. Queries mit Traffic aus Webmaster und Metrika extrahieren
3. Zum Positions-Tracking hinzufügen (Rush Analytics oder ähnlich)

### Neues Projekt {#new-project}
1. Hinzufügen zu: Metrika, Webmaster, GA, GSC
2. Initiale Query-Liste manuell sammeln oder generieren
3. Zum Positions-Tracking hinzufügen

## Tägliche Monitoring-Routine {#daily-monitoring-routine}

Jeden Morgen (5-10 Minuten):
1. Yandex Metrika öffnen
2. Yandex Webmaster öffnen
3. Google Search Console öffnen
4. Prüfen, ob alles in Ordnung ist

## Zentrale KPI-Metriken {#core-kpi-metrics}

### 1. Traffic + Segmente {#1-traffic-segments}
- Gesamter organischer Traffic
- Nach Suchmaschine (Yandex, Google)
- Nach Typ (Brand vs. Non-Brand)
- Nach Region (Stadtebene)
- Conversion-Raten pro Segment

### 2. Indexierung + Segmente {#2-indexation-segments}
**Prozess**: Website crawlen -> nach Seitentyp segmentieren -> Indexierung in Rush Analytics prüfen -> Anomalien identifizieren.

Nach Seitentyp verfolgen: Kategorien, Tags, Marken, Paginierung, Produktkarten.

**Hinweis**: Der Google-Index ist in der Regel etwa 30 % größer als der Yandex-Index.

### 3. Links + Segmente {#3-links-segments}
Verfolgen: Gesamtzahl der Donor-Domains und -Seiten, Metriken prioritärer Seiten, Metriken der Wettbewerber, Dynamik der Veränderungen.

### 4. Sichtbarkeit {#4-visibility}
**Definition**: geschätzter Prozentsatz des Traffics, der bei gegebenen Häufigkeiten des semantischen Kerns und aktuellen Positionen erreichbar ist.

**Einrichtung**: Queries in Projekte segmentieren, Segmente gruppieren, in den Tracker laden, Dynamik der Wettbewerber verfolgen.

**Zeitplan**: alle Wettbewerber alle 3-6 Monate; tiefgehendes Audit wachsender Wettbewerber alle 6 Monate.

### 5. Positionen + Segmente {#5-positions-segments}
Anteil der Queries in TOP-3, TOP-5, TOP-10 pro Suchmaschine. Weniger aussagekräftig als Sichtbarkeit, hilft aber, Muster zu erkennen.

## Meta-Scanner (Überwachung von Seitenänderungen) {#meta-scanner-page-change-monitoring}

**Zweck**: Seitenänderungen erkennen, bevor sie sich auf den Traffic auswirken.

**Ablauf**:
1. Aktuelle Daten als Referenz-Baseline laden
2. Dienst prüft in Intervallen
3. Abweichung -> Push-Benachrichtigung
4. Korrektur, bevor der Traffic betroffen ist

**Was überwacht wird**: Title, Description, H1, URL, Meta robots, Canonical, robots.txt, Textinhalt.

**Nutzen**: Entwickler lädt fehlerhafte robots.txt hoch -> am nächsten Tag Push-Benachrichtigung -> sofort behoben -> Traffic ist nie eingebrochen.

## Struktur des monatlichen Reports {#monthly-report-structure}

Pro Monat einen übergreifenden Report erstellen:

1. **Positionsdynamik**: Top-10, Anzahl Top-3, Sichtbarkeitstrend
2. **Organischer Traffic**: Sitzungen im Vergleich zum Vormonat und zum Vorjahresmonat (YoY)
3. **Zielkonversionen**: Leads, Käufe aus organischer Suche
4. **Technischer Zustand**: neue Crawling-Fehler, Änderungen der Indexierung
5. **Durchgeführte Arbeiten**: Liste aller umgesetzten Änderungen
6. **Plan für den nächsten Monat**

Reports knapp halten: Eine Zusammenfassung von 1-2 Seiten mit Diagrammen wirkt besser als ein 10-seitiges Dokument.

## Hypothesenbildung bei Traffic-Rückgängen {#hypothesis-building-for-traffic-drops}

### Ansatz mit segmentierter Analyse {#segmented-analysis-approach}

**Beispiel für einen plötzlichen Einbruch**:
1. Traffic ist gesunken
2. Nach Seitentyp segmentieren
3. Gezielt Brand-Seiten mit Rückgang
4. Brand-Seiten untersuchen
5. Title-Template auf Brand-Seiten defekt
6. Mit dem Entwicklungsteam beheben

**Beispiel für einen schleichenden Rückgang**:
1. Traffic sinkt allmählich
2. Hauptmetriken prüfen
3. Indexierung sinkt
4. Indexierung segmentieren
5. Tag-Seiten verlieren Indexierung
6. Entwickler hat sie versehentlich über Meta robots geschlossen
7. Beheben

### Diagnose bei Positionsverlust {#position-drop-diagnosis}
1. **Nicht in Panik geraten** (erste Regel)
2. Art bestimmen:
   - **Massiver Verlust** (alle Seiten) -> technisches Problem (robots.txt, Sitemap, Server)
   - **Segmentierter Verlust** (bestimmter Typ) -> Text- oder technisches Problem für dieses Template
   - **Punktueller Verlust** (einzelne Seite) -> Text- oder Linkproblem für diese Seite

## Aufgabenmanagement {#task-management}

**Erste Monate** (viele Briefings/Aufgaben):
- 3-5 prioritäre Aufgaben festlegen
- Status laufend prüfen
- Monatlich planen, Plan und Ist am Monatsende vergleichen
- Ins Stocken geratene Aufgaben verfolgen

## Zeitplan für wiederholte Audits {#repeat-audit-schedule}

| Projektgröße | Technisches Audit | Sichtbarkeit der Wettbewerber |
|--------------|-------------------|-------------------------------|
| Klein | Keine Wiederholung | Alle 3-6 Monate |
| Mittel | Alle 3-6 Monate | Alle 3-6 Monate |
| Groß | Monatlich | Alle 3-6 Monate |

## Analytik-Tools {#analytics-tools}

| Metrik | Primäres Tool | Alternative |
|--------|---------------|-------------|
| Traffic | Yandex Metrika + GA4 | - |
| Positionen | Rush Analytics | Serpstat, SE Ranking |
| Indexierung | Yandex Webmaster + GSC | - |
| Leads/Verkäufe | CRM (AmoCRM, TildaCRM) | Google Sheets |
| Multi-Channel | Roistat, Utmstat | - |

### Einrichtung des Positions-Trackings in Rush Analytics {#rush-analytics-position-tracking-setup}
1. Projekt anlegen: Name + vollständige Domain-URL
2. Zielsuchmaschine + Region hinzufügen (z. B. Yandex/Russland/Moskau)
3. Google mit derselben Region hinzufügen
4. Desktop und Mobile hinzufügen (separate SERP)
5. Tägliches Tracking einstellen (empfohlen)
6. Keyword-Liste importieren (mindestens 20-50 Queries)
7. Erste Prüfung ausführen; wiederkehrende Prüfungen konfigurieren

## Zusammenfassung: Steuerungssystem {#summary-control-system}

**Einrichtung zu Beginn**: alle Tools verbinden, Meta-Scanner konfigurieren, Queries zum Tracking hinzufügen, Queries segmentieren.

**Monatlich**: Traffic + Indexierung + Links + Sichtbarkeit + Positionen (jeweils segmentiert).

**Operativ**: 3-5 prioritäre Aufgaben, ins Stocken geratene Aufgaben verfolgen, tägliche Morgenprüfung.

**Periodisch**: technisches Audit gemäß Zeitplan, Sichtbarkeit der Wettbewerber alle 3-6 Monate.

## Stolperfallen {#gotchas}
- **Bei Traffic-Rückgängen nicht in Panik geraten** - zuerst segmentieren, dann diagnostizieren, dann handeln
- **Der Google-Index ist etwa 30 % größer als der Yandex-Index** - das ist normal und kein Fehler
- **Positionen sind weniger aussagekräftig als Sichtbarkeit** - Positionen schwanken täglich, Sichtbarkeit zeigt Trends
- **Der Meta-Scanner rechnet sich schon beim ersten Treffer** - Entwicklerfehler werden in 1 Tag statt in 2-3 Wochen erkannt
- **Die Unterscheidung Brand- vs. Non-Brand-Traffic ist entscheidend** - Wachstum beim Brand-Traffic kann einen Rückgang beim Non-Brand-Traffic verdecken
- **Monatliche Reports sollten knapp sein** - Kunden lesen 2-seitige Zusammenfassungen, keine 10-seitigen Dokumente

## Siehe auch {#see-also}
- [[seo-tools-workflow]] - Tool-Konfiguration und Einrichtung
- [[technical-seo-audit]] - Audit-Methodik
- [[seo-strategy-by-site-type]] - Strategie bestimmt die Auswahl der KPIs
- [[behavioral-factors-ctr]] - Verhaltensmetriken in der Analytik
