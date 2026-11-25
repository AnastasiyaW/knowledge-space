---
title: "YARN-Ressourcenverwaltung"
category: tools
tags: [data-engineering, yarn, hadoop, resource-management, cluster]
level: 2
source_sha256: e472d73a6e25bc5d74db96361e0a37ef7b8daf4bc382994d791df20c984573ba
translation: machine
translated_at: '2026-10-24'
---
# YARN-Ressourcenverwaltung {#yarn-resource-management}

YARN (Yet Another Resource Negotiator) ersetzte den monolithischen JobTracker von Hadoop v1 durch eine verteilte Architektur für die Ressourcenverwaltung. Dabei wird die Ressourcenzuweisung von der Koordination der Jobs getrennt.

## Entwicklung von Hadoop v1 {#evolution-from-hadoop-v1}

**v1 (JobTracker/TaskTracker):**
- JobTracker: zentraler Koordinator für ALLE Jobs – Übermittlung, Überwachung, Ressourcen
- TaskTracker: pro Knoten, starre Map/Reduce-Slots
- **Problem:** Der JobTracker ist ein Single Point of Failure. Bei großer Skalierung wird er durch Statusaktualisierungen überlastet (DDoS-artig)

**v2+ (YARN):**
- **ResourceManager (RM):** verwaltet die Cluster-Ressourcen über abstrakte Container
- **NodeManager:** Agent pro Knoten, meldet den Status an den RM
- **ApplicationMaster (AM):** Koordinator pro Job. Verwaltet die eigenen Tasks
- **Container:** isolierter Java-Prozess mit zugewiesener CPU und RAM

**Wichtigste Verbesserung:** Der RM weist nur Container zu. Die jobspezifische Logik übernimmt der AM. So wird die zentrale Last verteilt, an der der JobTracker gescheitert ist.

## Queue-Konfiguration {#queue-configuration}

```text
root
  |-- engineering (40%)
  |-- marketing (30%)
  |-- support (30%)
```

Jede Queue hat garantierte Mindestressourcen, eine maximale Obergrenze und kann Ressourcen von weniger ausgelasteten Queues leihen.

## Scheduler-Typen {#scheduler-types}

| Scheduler | Verhalten | Trade-off |
|-----------|-----------|-----------|
| **FIFO** | Strikt sequenziell | Selten verwendet |
| **Capacity** | Parallel, sofern Ressourcen verfügbar sind | Standard in vielen Distributionen |
| **Fair** | Verdrängt laufende Jobs zugunsten neuer | Beste Auslastung, verschwendet aber Arbeit |

**Fallstrick beim Fair Scheduler:** Preemption beendet Container kurz vor dem Abschluss, wodurch bereits geleistete Arbeit verloren geht.

## Wichtige Fakten {#key-facts}
- Container können beliebige Anwendungen ausführen: MapReduce, Spark, HTTP-Server
- Der ResourceManager verfolgt den Fortschritt einzelner Tasks nicht – das tut nur der AM
- Zeitbasierte Planung ist möglich (nachts 90 % für ETL, tagsüber mehr für Analytics)
- Prioritäten für Queues werden pro Queue konfiguriert

## Fallstricke {#gotchas}
- Preemption im Fair Scheduler kann fast abgeschlossene Tasks beenden
- Der Overhead der Container-Initialisierung dominiert bei kleinen Datenmengen
- YARN ersetzte starre Map/Reduce-Slots durch flexible Container
- Der RM ist weiterhin ein potenzieller SPOF – daher HA-Konfiguration verwenden

## Siehe auch {#see-also}
- [[hadoop-hdfs]] - Speicherschicht
- [[mapreduce]] - Verarbeitungsparadigma
- [[apache-spark-core]] - Spark auf YARN
- [[kubernetes-for-de]] - moderne Alternative zur Ressourcenverwaltung
