---
title: "Datenherkunft (Data Lineage) und Metadaten"
category: concepts
tags: [data-engineering, data-lineage, metadata, observability, monitoring]
level: 2
source_sha256: 005f6253b101d8a44d290999024dac54231dcbdad259ad86bf24d128149f2d21
translation: machine
translated_at: '2026-10-24'
---
# Datenherkunft (Data Lineage) und Metadaten {#data-lineage-and-metadata}

Datenherkunft beschreibt Ursprung und Transformationen von Daten über die Zeit – also wie Daten transformiert wurden, was sich geändert hat und warum. Metadaten sind „Daten über Daten“, die Auffindbarkeit, Qualitätsüberwachung und Governance ermöglichen.

## Lineage-Typen {#lineage-types}

| Typ | Erfasst |
|------|--------|
| **Spaltenebene** | Wie sich einzelne Spalten über die Stufen hinweg transformieren |
| **Tabellenebene** | Welche Tabellen in welche anderen einfließen |
| **Pipeline-Ebene** | DAG-/Job-Abhängigkeiten |

## Vorteile von Lineage {#lineage-benefits}
- **Impact-Analyse:** Was bricht, wenn sich diese Tabelle ändert?
- **Ursachenanalyse:** Wo sind die fehlerhaften Daten entstanden?
- **Compliance und Audit-Trails**
- **Automatisch generierte Datenflussdiagramme**

## Metadaten-Kategorien {#metadata-categories}

| Typ | Beispiele |
|------|---------|
| **Technisch** | Schema, Datentypen, Tabellengrößen, Indizes, Partitionen |
| **Geschäftlich** | Beschreibungen, Verantwortliche, Glossarbegriffe, Klassifizierungen |
| **Operativ** | Ladezeitstempel, Zeilenanzahl, Job-Dauern, Fehlerprotokolle |

## Monitoring-Stack {#monitoring-stack}

### Prometheus + Grafana {#prometheus-grafana}

**Prometheus** – pull-basiertes Monitoring:
- Scrapt Metriken von Zielen in konfigurierten Intervallen
- Zeitreihendatenbank für die Speicherung
- PromQL für Abfragen
- Integrierte Alerting-Regeln

**Grafana** – Visualisierung:
- Vorgefertigte Dashboard-Vorlagen
- Unterstützung für mehrere Datenquellen
- Alerting mit Benachrichtigungskanälen

### Gängige Exporter {#common-exporters}

| Exporter | Metriken |
|----------|---------|
| PostgreSQL | Anzahl Verbindungen, Abfragedauer, Replikationsverzögerung |
| Kafka | Consumer-Lag, Partitionsanzahl, Nachrichtenrate |
| Node | CPU, Speicher, Festplatte, Netzwerk |

## Wichtige Fakten {#key-facts}
- Gutes Metadatenmanagement ermöglicht Datenerkennung, Qualitätsüberwachung und die Automatisierung von Governance
- Spaltenebene-Lineage ist am wertvollsten, aber am schwierigsten umzusetzen
- Operative Metadaten (Ladezeiten, Zeilenanzahl) sind günstig zu erfassen und für die Fehlersuche sehr wertvoll

## Stolperfallen {#gotchas}
- Das Pull-Modell von Prometheus erfordert, dass alle Ziele netzwerkseitig erreichbar sind
- Lineage-Tools, die auf dem Parsen von Abfragen beruhen, übersehen dynamisches SQL und programmatische Transformationen
- Die Datei `_SUCCESS` bei MapReduce garantiert den Abschluss des Jobs, nicht die Korrektheit der Daten

## Siehe auch {#see-also}
- [[data-quality]] – Qualitätsüberwachung
- [[data-governance-catalog]] – Governance-Kontext
- [[apache-airflow]] – Pipeline-Monitoring
