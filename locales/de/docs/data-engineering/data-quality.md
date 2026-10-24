---
title: "Datenqualität"
category: concepts
tags: [data-engineering, data-quality, validation, testing, observability]
level: 2
source_sha256: b6afc4fa06600a31e61c8b56e85fb8a5a75641337c13a26f14995e0a0d40d8cf
translation: machine
translated_at: '2026-10-24'
---
# Datenqualität {#data-quality}

Datenqualität umfasst das Überwachen, Definieren und Sicherstellen der Datenintegrität. In großen Organisationen ist sie entscheidend, um falsche Geschäftsentscheidungen aufgrund fehlerhafter Daten zu vermeiden.

## Qualitätsdimensionen {#quality-dimensions}

| Dimension | Frage |
|-----------|----------|
| **Vollständigkeit** | Sind alle erforderlichen Werte vorhanden? |
| **Genauigkeit** | Bilden die Werte reale Entitäten korrekt ab? |
| **Konsistenz** | Werden dieselben Fakten über alle Systeme hinweg gleich dargestellt? |
| **Aktualität** | Sind die Daten verfügbar, wenn sie benötigt werden? Sind sie aktuell genug? |
| **Eindeutigkeit** | Gibt es doppelte Datensätze? |
| **Validität** | Entsprechen die Daten den definierten Formaten, Typen und Wertebereichen? |

## Praktiken der Datenqualität {#data-quality-practices}
- Qualitätsregeln und Schwellenwerte pro Datensatz bzw. pro Spalte definieren
- Automatisierte Prüfungen in Pipelines (vor dem Laden UND nach dem Laden)
- Qualitäts-Dashboards und Alerting bei SLA-Verletzungen
- Ursachenanalyse (Root Cause Analysis) für Qualitätsprobleme
- Data Profiling zur Erkennung von Anomalien

## Werkzeuge {#tools}

| Werkzeug | Typ |
|------|------|
| **Great Expectations** | Open-Source-Validierung in Python |
| **dbt tests** | Integrierte und benutzerdefinierte Assertions auf Modellen |
| **Apache Griffin** | Open Source für Big Data |
| **Monte Carlo, Bigeye, Soda** | Kommerzielle Observability-Plattformen |

## Data Observability {#data-observability}

Geht über das Pipeline-Monitoring hinaus und erkennt:
- Schemaänderungen
- Verschiebungen in der Verteilung
- Änderungen der Null-Rate
- Volumenanomalien
- Verletzungen der Aktualität

## Pipeline-Monitoring {#pipeline-monitoring}

| Kategorie | Metriken |
|----------|---------|
| **Pipeline-Zustand** | Erfolgs-/Fehlerrate der DAGs, Taskdauer, Anzahl der Wiederholungen |
| **Aktualität der Daten** | Zeit seit dem letzten Update, Einhaltung der SLA |
| **Datenvolumen** | Zeilenanzahl pro Ladevorgang, Abweichung vom Erwartungswert |
| **Infrastruktur** | CPU/Speicher/Festplatte auf Workern, Verzögerung des Schedulers |
| **Datenqualität** | Anzahl fehlgeschlagener Validierungen, Trends der Null-Rate |

## Best Practices für Alerting {#alerting-best-practices}
- Alarm bei **SLA-Verletzungen** auslösen, nicht nur bei Fehlern
- **Anomalieerkennung** für Zeilenanzahlen verwenden (plötzlicher Einbruch oder Anstieg)
- Eskalationsstufen (Warnung -> kritisch -> Pager)
- **Runbook-Links** in Alarmmeldungen einfügen
- Alert Fatigue vermeiden: Schwellenwerte abstimmen, zusammengehörige Alarme gruppieren

## Stolperfallen {#gotchas}
- Ein Data Lake ohne Governance wird zum „Data Swamp“
- Row-Level Security muss mit tatsächlichen Benutzerkonten getestet werden
- Das Pull-Modell von Prometheus setzt voraus, dass alle Targets im Netzwerk erreichbar sind
- Die Datei `_SUCCESS` garantiert den Abschluss des Jobs, nicht die Korrektheit der Daten

## Siehe auch {#see-also}
- [[data-governance-catalog]] - Governance-Framework
- [[data-lineage-metadata]] - Nachverfolgung von Datenproblemen
- [[etl-elt-pipelines]] - Wo Qualitätsprüfungen ausgeführt werden
- [[apache-airflow]] - Orchestrierung von Qualitätsprüfungen
