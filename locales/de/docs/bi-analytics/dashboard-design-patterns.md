---
title: "Dashboard-Designmuster"
category: concepts
tags: [bi-analytics, dashboard, design, ux, layout, gestalt, f-pattern, storytelling]
level: 3
source_sha256: 9ad5648f8b9e75bacd3f2be18295db0aa348688f52cec7a8ab37ba1d12971667
translation: machine
translated_at: '2026-10-24'
---
# Dashboard-Designmuster {#dashboard-design-patterns}

Dashboard-Design verbindet Informationsdesign, Grafikdesign, UX und Storytelling. Gutes Design folgt etablierten Mustern für Leserichtung, visuelle Hierarchie und kognitive Prinzipien, damit Nutzer Erkenntnisse schnell finden und darauf reagieren können.

## Wichtige Fakten {#key-facts}

- Nutzer lesen von links nach rechts und von oben nach unten (F-Muster für europäische Zielgruppen)
- Zone hoher Aufmerksamkeit: obere linke Ecke; Zone geringer Aufmerksamkeit: untere rechte Ecke
- Kontrast schlägt das F-Muster: große, farbige Objekte ziehen unabhängig von ihrer Position die Aufmerksamkeit auf sich
- KPI-Factoids und Sparklines gehören für maximale Wirkung in die obere linke Ecke
- Dashboard-Struktur: Zusammenfassung -> Trend -> Aufschlüsselung -> Detail (vom Allgemeinen zum Speziellen)
- Maximal 5-7 Farben pro Dashboard; einheitliche Farbcodierung über alle Diagramme hinweg
- Jedes Diagramm sollte genau eine Nutzerfrage beantworten

## Muster {#patterns}

### Dashboard-Struktur (vom Allgemeinen zum Speziellen) {#dashboard-structure-general-to-specific}

```text
Level 1: KPI summary (total state, one number per metric)
Level 2: Trend over time (is it improving or declining?)
Level 3: Breakdown by dimension (which segment drives the trend?)
Level 4: Detail/drill-down (individual records, anomalies)
```

Visuelles Layout:
```text
Header (title)
+-- KPI factoids + sparklines (upper area, high attention)
+-- Trend charts (middle area)
+-- Detail table (lower area)
```

### Modulares Layout {#modular-layout}

Das Dashboard in unsichtbare rechteckige Blöcke unterteilen (ähnlich wie Zeitungsspalten):
- Tiled-Container verwenden (nur ein äußerer Tiled-Container, darin vertikale/horizontale Container)
- Keine frei schwebenden Elemente (sie brechen die adaptive Größenanpassung)

Größenmodi des Dashboards:
- **Fixed**: behält die exakt angegebene Größe bei
- **Range**: Bereich aus minimaler/maximaler Breite und Höhe (empfohlen)
- **Automatic**: passt sich an den Bildschirm an, wobei Elemente sich verschieben können

Regel: Zuerst die Struktur planen, dann die Container erstellen. Außen vertikal, innen horizontal, danach innerhalb der horizontalen Container vertikal.

### UX-Prinzipien {#ux-principles}

**Fitts'sches Gesetz**: Elemente, die häufig bedient werden müssen, sollten größer und näher an der Mitte platziert sein.

**Hicks Gesetz**: Mehr Auswahlmöglichkeiten bedeuten längere Entscheidungszeiten. Filteroptionen nach Möglichkeit minimieren.

Filterplatzierung: nahe an den Diagrammen, die sie steuern. UX = Nutzergewohnheiten + gesunder Menschenverstand.

### Gestalt-Prinzipien {#gestalt-principles}

- **Nähe**: nah beieinander liegende Objekte werden als zusammengehörig wahrgenommen – Abstände nutzen, um zusammengehörige Diagramme zu gruppieren
- **Umschlossene Fläche**: Objekte innerhalb eines sichtbaren Containers werden als eine Gruppe wahrgenommen
- **Ähnlichkeit/Kontrast**: ähnlich aussehende Elemente werden gruppiert; unterschiedlich aussehende werden getrennt

### Storytelling vs. operative Dashboards {#storytelling-vs-operational-dashboards}

**Storytelling** = Daten + Visualisierung + Narrativ. Wird in Präsentationen verwendet, nicht in operativen Dashboards. Annotationen, Titel und Kontextzeilen hinzufügen, um den Nutzer durch die Erkenntnis zu führen.

**Operative Dashboards** = für wiederholte Nutzung, Self-Service-Exploration und minimales Narrativ konzipiert.

### Visualisierungs-Checkliste {#visualization-checklist}

Vor der Fertigstellung eines Dashboards:
- [ ] KPI-Factoids in der oberen linken Ecke (Zone hoher Aufmerksamkeit)
- [ ] Diagramm-Hierarchie: Zusammenfassung -> Trend -> Aufschlüsselung -> Detail
- [ ] Maximal 5-7 Farben; einheitliche Farbcodierung über alle Diagramme
- [ ] Jedes Diagramm beantwortet genau eine Nutzerfrage
- [ ] Filterbeschriftungen sind klar; Filterpositionen nahe bei den betroffenen Diagrammen
- [ ] Kontextlinien und Annotationen, wo sinnvoll
- [ ] Performance: initiale Ladezeit < 10 Sekunden
- [ ] Mobiles Layout berücksichtigt, falls erforderlich
- [ ] Mit tatsächlichen Stakeholdern in einer Testgruppe getestet

### Prinzipien für Storytelling in Berichten {#report-storytelling-principles}

- Eine klare Frage pro Seite beantworten
- Der Titel nennt die Erkenntnis, nicht nur das Thema („Umsatz um 23 % gegenüber Vorjahr gestiegen“ statt „Umsatzanalyse“)
- Einheitliche Farbcodierung (Rot = schlecht, Grün = gut)
- Annotationen zu wichtigen Ereignissen in Zeitreihen
- Kontext: Vergleichszeiträume, Ziele und Benchmarks ergänzen

## Stolperfallen {#gotchas}

- Isoliert entwickeln ohne Abstimmung mit Stakeholdern ist das Anti-Pattern Nr. 1 – Wireframe vor dem Bauen zeigen, Entwurf bei 50 % vorlegen
- Eine große Karte in der unteren rechten Ecke lenkt aufgrund des Kontrasteffekts die Aufmerksamkeit von den KPIs in der oberen linken Ecke weg
- Mehr als 6 Blätter pro Arbeitsmappe verschlechtern die Performance – erwägen, auf mehrere Dashboards aufzuteilen
- Das mobile Layout ist in Tableau ein eigenständiges Design und nicht automatisch – bei Bedarf explizit einplanen
- „Bau einfach irgendetwas“-Anfragen führen zu Nacharbeit – zwei Tage in Anforderungen investieren, um zwei Wochen Neubau zu sparen

## Siehe auch {#see-also}

- [[color-theory-visualization]] – Farbskalen und Barrierefreiheit
- [[tableau-chart-types]] – Diagrammauswahl und Kodierung
- [[bi-development-process]] – Anforderungserhebung vor dem Design
- [[powerbi-advanced-features]] – Lesezeichen und Drill-through für die Navigation
