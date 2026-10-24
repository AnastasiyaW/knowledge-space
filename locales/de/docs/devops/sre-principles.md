---
title: "SRE-Prinzipien und Kultur"
category: concepts
tags: [devops, sre, reliability, error-budget, toil, culture, blameless]
level: 3
source_sha256: 6093815966eb46f4dbde65349266fec1a85e1d781163c9b0b111669b3fbbc124
translation: machine
translated_at: '2026-10-24'
---
# SRE-Prinzipien und Kultur {#sre-principles-and-culture}

Site Reliability Engineering (SRE) ist eine Sammlung von Ingenieurtechniken zum Aufbau und Betrieb zuverlässiger Systeme. Ursprung bei Google (2003, Ben Treynor). "SRE ist das, was entsteht, wenn ein Software-Ingenieur mit dem betraut wird, was früher als Operations bezeichnet wurde."

## SRE vs. DevOps {#sre-vs-devops}

- **DevOps** definiert WAS getan werden sollte (kulturelle Bewegung, breite Praktiken)
- **SRE** definiert WIE Zuverlässigkeit umgesetzt wird (präskriptiv, ingenieursorientiert)
- SRE setzt DevOps-Prinzipien um. SRE umfasst Programmierung: 50 % Betrieb, 50 % Ingenieursprojekte

## Zentrale Prinzipien {#key-principles}

1. **Betrieb ist ein Softwareproblem** - mit Ingenieurmethoden lösen
2. **Steuerung über SLOs** - nicht "maximale Zuverlässigkeit"
3. **Error Budgets** - quantifizierte akzeptable Unzuverlässigkeit
4. **Toil-Reduktion** - repetitive manuelle Arbeit automatisieren
5. **Geteilte Verantwortung** - SREs teilen sich die Verantwortung für den Produktivbetrieb mit Entwicklern
6. **Schuldzuweisungsfreie Postmortems** - Fokus auf systemische Korrekturen

## Säulen der Kultur {#culture-pillars}

### Ingenieurskultur {#engineering-culture}
- Freier Austausch von Ideen. Keine organisatorischen Konsequenzen bei Problemen (sofern SLO eingehalten)
- "Alle sitzen im selben Boot" - gemeinsame Verantwortung
- Schuldfrei: Schuldzuweisung ist neurophysiologisch bedingt - eine Kultur aufbauen, die sie überwindet

### Alles messen (Observability) {#measure-everything-observability}
- Das System kennen: wissen, wo man schaut und was passiert, und zwar schnell
- Einfach klingend, aber komplex und teuer in der Umsetzung

### Schuldzuweisungsfreie Postmortems {#blameless-postmortems}
- Schuldzuweisung ist kontraproduktiv
- Offene Kultur für die Besprechung von Problemen, sobald sie auftreten

### Incident Management {#incident-management}
- Ausfälle treten immer auf. Runbooks, Eskalationsstufen, Klassifizierung
- Gut klassifizierte Incidents mit bekannten Abläufen führen zu selbstheilenden Systemen
- Einfachstes Beispiel: Health Checks mit automatischem Neustart

## Zentrale Kennzahlen {#key-metrics}

| Metrik | Beschreibung |
|--------|-------------|
| Deployment-Häufigkeit | Wie oft neuer Code ausgeliefert wird. Sinkende Werte = Problem in der Pipeline |
| MTTC | Mean Time To Commit - vom Commit bis in die Produktion |
| Change Failure Rate | Anteil der Änderungen, die Ausfälle verursachen |
| MTTA | Mean Time To Acknowledge (~5 Min. branchenüblicher Standard) |
| MTTR | Mean Time To Resolve (~1 Stunde branchenüblicher Standard) |

## Error Budget {#error-budget}

`100% - SLO = error budget`

- SLO 99,9 % = 0,1 % Budget = 43,2 Min./Monat
- Budget aufgebraucht -> Feature-Releases einfrieren, Fokus auf Zuverlässigkeit
- Budget verbleibend -> schneller ausliefern, mehr Risiken eingehen
- Error-Budget-Burn-Rate erfasst die Geschwindigkeit des Verbrauchs
- Error-Budget-Policy definiert Maßnahmen bei Schwellenwerten

## Toil {#toil}

Repetitive manuelle Arbeit, die automatisiert werden kann. Merkmale: manuell, automatisierbar, taktisch, kein nachhaltiger Wert, skaliert linear mit dem Wachstum.

`Toil / All tasks` = Toil-Quote. Zielwert: unter 50 %.

### Reifegrade der Automatisierung {#automation-maturity-levels}

1. **Keine Automatisierung** - vollständig manuell
2. **Systemspezifische Skripte** - einzelne Administratoren
3. **Generische gemeinsam genutzte Automatisierung** - gemeinsame Werkzeuge
4. **Eingebaute Automatisierung** - System verwaltet sich selbst
5. **Autonome Systeme** - selbstheilend, selbstskalierend

## Modelle für SRE-Teams {#sre-team-models}

| Modell | Beschreibung |
|-------|-------------|
| **Infrastructure SRE** | Gemeinsames Plattformteam. Einheitlicher Ansatz. Risiko: von Produkt entkoppelt |
| **Product SRE** | Eingebettet im Produktteam. Tiefes Wissen. Risiko: abgeschottete Praktiken |
| **Consulting SRE** | Befristeter Einsatz. Unterstützt Teams bei Verbesserungen. Zieht weiter, wenn SLO erreicht |

### Wann SRE nicht nötig ist {#when-sre-is-not-needed}

- Dienst funktioniert bereits gut
- Dienst ist unwichtig
- Dienst ist ein Altsystem, das außer Betrieb genommen wird

## Anti-Patterns {#anti-patterns}

- "SRE löst alle Probleme" - SRE sind Techniken; Menschen lösen Probleme
- "SRE ist ein Allheilmittel" - funktioniert nur bei bestimmten Systemen in bestimmten Lebenszyklusphasen
- "SRE ist Teil des DevOps-Teams" - Ziele unterscheiden sich, Unterordnung ist problematisch
- SRE einführen ohne Verpflichtung von ALLEN Abteilungen

## Stolperfallen {#gotchas}

- Übermäßige Zuverlässigkeit ist verschwenderisch - SRE sorgt für "zuverlässig genug" für das Geschäft
- SRE erfordert Verpflichtung aller Abteilungen, nicht nur der Entwicklung
- Know-Do-Learn-Zyklen: ständiger Wandel ist die neue Normalität

## Siehe auch {#see-also}

- [[monitoring-and-observability]] - SLI/SLO/SLA-Messung
- [[sre-incident-management]] - Bereitschaft, Postmortems, Eskalation
- [[deployment-strategies]] - Release-Management und Error Budgets
- [[chaos-engineering-and-testing]] - Zuverlässigkeitstests
- [[sre-automation-and-toil]] - Automatisierungswerkzeuge und Praktiken
