---
title: "BI-Entwicklungsprozess"
category: concepts
tags: [bi-analytics, requirements, dashboard-map, metrics-registry, workflow, stakeholders]
level: 3
source_sha256: eeba7ae76cb4f3f385e38954d0867a3af78c7db44217264de44d583ddc30580f
translation: machine
translated_at: '2026-10-24'
---
# BI-Entwicklungsprozess {#bi-development-process}

Der BI-Entwicklungsprozess umfasst den gesamten Lebenszyklus von der Anforderungserhebung über Stakeholder-Interviews, Dashboard-Planung mit Wireframes, Datenexploration, Entwicklung, Iteration und Veröffentlichung. Ein strukturierter Prozess verhindert die häufigste Anti-Praxis: das Falsche zu bauen.

## Wichtige Fakten {#key-facts}

- Typische Anti-Praxis: „Bau einfach etwas, die Details klären wir später“ -> Nacharbeitsschleifen und ungenutzte Dashboards
- 2 Tage in Anforderungen investieren, um 2 Wochen Nacharbeit zu sparen
- Dashboard Map = Wireframe + Zuordnung von Fragen zu Antworten, erstellt bevor Tableau geöffnet wird
- Metrics Registry = einzige Quelle der Wahrheit für alle Metrikdefinitionen
- BI-Analyst-Kompetenzmatrix: 4 Stufen (theoretisch -> kann andere schulen)
- Visualisierung = Informationsdesign + Grafikdesign + UX + Storytelling + Tool-Kompetenz

## Muster {#patterns}

### BI-Entwicklungsworkflow {#bi-development-workflow}

1. **Anforderungserhebung** - Stakeholder interviewen, Fragen und KPIs dokumentieren
2. **Dashboard Map** - Struktur als Wireframe entwerfen, bevor Tableau angefasst wird
3. **Datenexploration** - tatsächliche Datenstruktur, Granularität und Besonderheiten verstehen
4. **Datenaufbereitung** - Joins modellieren, berechnete Felder erstellen (zuerst auf Papier)
5. **MVP bauen** - minimale Version, mit Stakeholdern testen
6. **Iterieren** - auf Basis des Feedbacks verfeinern
7. **Veröffentlichen und dokumentieren** - auf dem Server veröffentlichen, Datenquellen und Metriken dokumentieren

### Interview zur Anforderungserhebung {#requirements-gathering-interview}

**Geschäftsfragen:**
- Welche Entscheidungen soll dieses Dashboard unterstützen?
- Wie oft wird es genutzt? (täglich, wöchentlich, monatlich)
- Welche Handlungen folgen aus den Daten? (untersuchen, eskalieren, nichts tun)

**Nutzer:**
- Wer sind die Nutzer? (PMs, Analysten, Führungskräfte)
- Wie hoch ist ihr Tableau-/BI-Kenntnisstand?
- Wer gehört zur Testgruppe?

**Datenfragen:**
- Welche Daten sind verfügbar? (DWH-Tabellen, CSV-Dateien, CRM-Exporte)
- Sind die Daten bereinigt oder roh? Wer hat sie aufbereitet?
- Gibt es nicht-additive Metriken? (erfordern ein separates Skalenfeld, dürfen nicht einfach summiert werden)
- Gibt es besondere Eigenheiten in den Daten? (z. B. muss die Zeile „All Regions“ im Feld Region gefiltert werden)

**Zeitplan:**
- Deadline? MVP oder Vollversion?

### Dashboard Map (Struktur) {#dashboard-map-structure}

Vor dem Bauen planen. Für jedes Element definieren:
- **Frage**, die der Nutzer stellt („Welche Region liegt unter dem Ziel?“)
- **Diagrammtyp**, der sie am besten beantwortet
- **Benötigte Datenfelder**
- **Anwendbare Filter**

Muster für die Dashboard-Struktur:
```text
Level 1: KPI summary (total state, one number per metric)
Level 2: Trend over time (improving or declining?)
Level 3: Breakdown by dimension (which segment drives the trend?)
Level 4: Detail/drill-down (individual records, anomalies)
```

### Metrics Registry {#metrics-registry}

Eine einzige Quelle der Wahrheit für alle Definitionen geschäftlicher Metriken:

| Feld | Beispiel |
|-------|---------|
| **Name** | active_sellers |
| **Geschäftsdefinition** | Verkäufer mit mindestens einem Inserat im Zeitraum |
| **SQL/Formel** | `COUNT(DISTINCT seller_id) WHERE adverts > 0` |
| **Owner** | Listings-Team |
| **Datenquelle** | DWH-Tabelle `listings.sellers` |
| **Granularität** | Täglich, mit Skalenfeld für wöchentlich/monatlich |
| **Besondere Hinweise** | Zeile „All Regions“ muss für Summen ausgeschlossen werden |

Ohne Registry zeigen verschiedene Dashboards für dieselbe Metrik unterschiedliche Zahlen, weil jeder Analyst sie anders definiert hat.

### Beispiel eines Datenfeld-Wörterbuchs {#data-field-dictionary-example}

Für ein Dashboard zu Inseraten:
- `execution_date` - Datum
- `region` - Geografische Region; Hinweis: Es gibt eine Zeile „All Regions“, beim Anzeigen von Summen filtern
- `scale` - Datengranularität (day/week/month); nicht additiv, muss nach Skala gefiltert statt summiert werden
- `listers` - Aktive Verkäufer (mit mindestens einem Inserat)
- `retention_7_days` - % noch aktiv 7 Tage nach dem ersten Inserat (nur auf Tagesebene gültig)
- `retention_28_days` - % noch aktiv nach 28 Tagen (nur auf Tagesebene gültig)

### Kommunikation mit Stakeholdern {#stakeholder-communication}

**Anti-Praxis**: isoliert bauen und Stakeholder mit „fertigen“ Ergebnissen überraschen.

**Besserer Ansatz:**
- Wireframe vor dem Bauen zeigen
- Entwurf bei 50 % Fertigstellung zeigen
- Wöchentliche Check-ins bei großen Projekten

**Umgang mit „Bau einfach etwas“-Anfragen:**
„Wenn ich ohne Verständnis der Anforderungen baue, müssen wir es voraussichtlich neu bauen. 2 Tage Anforderungen = spart 2 Wochen Nacharbeit.“

**Umgang mit dringendem Zeitdruck:**
Den MVP-Umfang vereinbaren: minimales tragfähiges Dashboard, das in der verfügbaren Zeit Nutzen liefert.

### Bewertung der BI-Analyst-Kompetenz {#bi-analyst-competency-assessment}

5 Visualisierungskomponenten: Informationsdesign, Grafikdesign, UX, Storytelling, Tool-Kompetenz.

4-stufige Kompetenzskala:
1. Nur theoretisches Wissen
2. Kann mit Dokumentation/Nachschlagen arbeiten
3. Kennt Nuancen, hat eigene Beispiele
4. Kann andere schulen

Den eigenen Stand mit dem Zielniveau vergleichen, um Lücken zu erkennen.

## Stolperfallen {#gotchas}

- Nicht-additive Metriken (z. B. Metriken mit einem Feld „scale“ für day/week/month) dürfen nicht summiert werden – nach Skala filtern
- Retention-Metriken sind möglicherweise nur auf Tagesebene gültig – vor der Berechnung die Granularität prüfen
- Zeilen „All Regions“ oder ähnliche Aggregatzeilen in den Quelldaten müssen bei Summen herausgefiltert werden, sonst entsteht Doppelzählung
- Die Lastspitzen auf BI-Servern verlaufen nicht linear und sind unvorhersehbar – ein einziger aufwendiger Bericht kann 75 % der Server-CPU beanspruchen
- Aktuelle unvollständige Zeiträume sollten ausgeschlossen oder deutlich gekennzeichnet werden, um irreführende Vergleiche zu vermeiden

## Siehe auch {#see-also}

- [[dashboard-design-patterns]] - visuelles Design, nachdem die Anforderungen feststehen
- [[product-analytics-fundamentals]] - Metrikpyramide und KPI-Auswahl
- [[tableau-fundamentals]] - Entwicklung in Tableau
- [[powerbi-fundamentals]] - Entwicklung in Power BI
- [[bi-tools-comparison]] - Auswahl des passenden BI-Tools
