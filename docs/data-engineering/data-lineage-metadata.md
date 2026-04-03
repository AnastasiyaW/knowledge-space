---
title: Data Lineage and Metadata
category: concepts
tags: [data-engineering, data-lineage, metadata, observability, monitoring]
---

# Data Lineage and Metadata

Data lineage describes the origin and transformations of data over time - how data was transformed, what changed, and why. Metadata is "data about data" that enables discovery, quality monitoring, and governance.

## Lineage Types

| Type | Tracks |
|------|--------|
| **Column-level** | How individual columns transform across stages |
| **Table-level** | Which tables feed into which |
| **Pipeline-level** | DAG/job dependencies |

## Lineage Benefits
- **Impact analysis:** what breaks if this table changes?
- **Root cause analysis:** where did bad data originate?
- **Compliance and audit trails**
- **Auto-generated data flow diagrams**

## Metadata Categories

| Type | Examples |
|------|---------|
| **Technical** | Schema, data types, table sizes, indexes, partitions |
| **Business** | Descriptions, owners, glossary terms, classifications |
| **Operational** | Load timestamps, row counts, job durations, error logs |

## Monitoring Stack

### Prometheus + Grafana

**Prometheus** - pull-based monitoring:
- Scrapes metrics from targets at configured intervals
- Time-series database for storage
- PromQL for querying
- Built-in alerting rules

**Grafana** - visualization:
- Pre-built dashboard templates
- Multi-datasource support
- Alerting with notification channels

### Common Exporters

| Exporter | Metrics |
|----------|---------|
| PostgreSQL | Connection count, query duration, replication lag |
| Kafka | Consumer lag, partition count, message rate |
| Node | CPU, memory, disk, network |

## Key Facts
- Good metadata management enables data discovery, quality monitoring, and governance automation
- Column-level lineage is the most valuable but hardest to implement
- Operational metadata (load times, row counts) is cheap to collect and high-value for debugging

## Gotchas
- Prometheus pull model requires all targets to be network-accessible
- Lineage tools that rely on query parsing miss dynamic SQL and programmatic transformations
- MapReduce `_SUCCESS` file guarantees job completion, not data correctness

## See Also
- [[data-quality]] - quality monitoring
- [[data-governance-catalog]] - governance context
- [[apache-airflow]] - pipeline monitoring
