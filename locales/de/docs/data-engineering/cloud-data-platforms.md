---
title: "Cloud-Datenplattformen"
category: tools
tags: [data-engineering, cloud, aws, gcp, snowflake, bigquery, s3]
level: 4
source_sha256: fedee1bace17ec71fea61b3eed8b8d7c051c3a3cd715a3120b245d1d12dee42c
translation: machine
translated_at: '2026-10-24'
---
# Cloud-Datenplattformen {#cloud-data-platforms}

Cloud-Plattformen trennen Rechenleistung von Speicher und ermöglichen so elastische Skalierung und nutzungsabhängige Abrechnung (Pay-per-Use). Die „Big Three" (AWS, GCP, Azure) plus Snowflake bilden die Grundlage für modernes Data Engineering.

## Service-Modell-Vergleich {#service-model-comparison}

| On-Premise | AWS | GCP | Zweck |
|-----------|-----|-----|---------|
| HDFS | S3 | Cloud Storage | Objektspeicher |
| Spark | EMR | Dataproc | Verteilte Berechnung |
| Kafka | MSK / Kinesis | Pub/Sub | Event-Streaming |
| PostgreSQL | RDS | Cloud SQL | Verwaltetes RDBMS |

## Cloud-DWH-Optionen {#cloud-dwh-options}

| System | Typ | Wichtigstes Merkmal |
|--------|------|-------------|
| **Athena** | Query-Dienst | Verwaltetes Presto, fragt S3 ohne vorheriges Laden ab |
| **Redshift** | MPP-DWH | Architektonisch am nächsten zu Greenplum |
| **BigQuery** | Serverless-DWH | Keine Steuerung der Rechenressourcen – echtes Serverless |
| **Snowflake** | Getrennte Compute/Storage | Startet Cluster pro Abfrage, Daten in S3 |
| **Presto/Trino** | Föderierte Query-Engine | Fragt Daten in Quellsystemen ohne ETL ab |

## S3 - Simple Storage Service {#s3-simple-storage-service}
- 5–10-mal günstiger als HDFS
- 99,999999999 % Haltbarkeit (11 Neunen)
- Praktisch unbegrenzte Elastizität
- Trennt Speicher von Rechenleistung
- Zugriff über `boto3` (Python), CLI oder Spark (`s3a://`)

## Cloud-Service-Modelle für DE {#cloud-service-models-for-de}

| Ansatz | Beispiele | Verantwortung im DE |
|----------|---------|-------------------|
| **IaaS** | Selbstverwaltetes ClickHouse auf VMs | OS, Datenbank, Monitoring, Backups |
| **PaaS** | Verwaltetes ClickHouse, RDS | Dienstkonfiguration |
| **SaaS** | BigQuery, Snowflake | Nur Schreiben von Abfragen |

## Snowflake-Architektur {#snowflake-architecture}
- Drei Schichten: Storage, Compute, Services
- Kein direkter Zugriff auf die Storage-Schicht
- Automatische Micro-Partitionierung
- Virtuelle Cluster (Warehouses) für unterschiedliche Workloads
- Abrechnung nach Compute-Zeit pro Abfrage

## VM- und Disk-Best-Practices {#vm-and-disk-best-practices}

**Disk-Performance skaliert mit der Größe (QoS).** Eine 50-GB-SSD kann langsam sein, weil die IOPS proportional gedrosselt werden. Abhilfe: Disk-Größe erhöhen, um mehr IOPS zu erhalten.

| Disk-Typ | Geeignet für |
|-----------|---------|
| HDD | Am günstigsten, Archive |
| SSD | Dev/Test (kosteneffizient) |
| High-IOPS-SSD | Produktionsworkloads |
| Lokales NVMe | Maximale Performance, keine Replikation |

## Kostenmanagement {#cost-management}
- **Ungenutzte** VMs, Datenbanken und K8s-Cluster **immer pausieren/stoppen**
- Transiente Cluster für einmalige Jobs – erstellen, nutzen, löschen
- HDD für Dev/Test, SSD für Staging, High-IOPS für Produktion
- QoS-Limits überwachen – kleine Disks haben niedrigere IOPS-Kontingente

## Cloud-native Datenmuster {#cloud-native-data-pattern}
```text
Storage Layer: S3 (or compatible)
Compute Layer: Kubernetes (Spark, Presto run here)
```
Die Trennung ermöglicht elastische Rechenleistung unabhängig vom Speicher.

## Stolperfallen {#gotchas}
- Redshift-Knoten enthalten standardmäßig Compute und Storage; Snowflake trennt beides nativ
- Vertikale Skalierung erfordert einen VM-Neustart (Ausfallzeit)
- Firewall immer konfigurieren – jede VM mit öffentlicher IP ist ein Ziel
- Netzwerklatenz zerstört bei synchroner Replikation die Performance von Clustern über Rechenzentren hinweg
- BigQuery: Fehlende Steuerung der Rechenressourcen führt bei komplexen Abfragen zu unerwarteten Kosten

## Siehe auch {#see-also}
- [[dwh-architecture]] - DWH-Designkontext
- [[kubernetes-for-de]] - Orchestrierung von Rechenleistung
- [[docker-for-de]] - Grundlagen der Containerisierung
- [[data-lake-lakehouse]] - Lakehouse in der Cloud
