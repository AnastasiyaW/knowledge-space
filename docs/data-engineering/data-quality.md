---
title: Data Quality
category: concepts
tags: [data-engineering, data-quality, validation, testing, observability]
---

# Data Quality

Data quality encompasses monitoring, defining, and maintaining data integrity. Critical in large organizations to prevent incorrect business decisions driven by bad data.

## Quality Dimensions

| Dimension | Question |
|-----------|----------|
| **Completeness** | Are all required values present? |
| **Accuracy** | Do values correctly represent real-world entities? |
| **Consistency** | Same facts represented the same way across systems? |
| **Timeliness** | Is data available when needed? Fresh enough? |
| **Uniqueness** | Are there duplicate records? |
| **Validity** | Does data conform to defined formats, types, ranges? |

## Data Quality Practices
- Define quality rules and thresholds per dataset/column
- Automated checks in pipelines (pre-load AND post-load)
- Quality dashboards and alerting on SLA breaches
- Root cause analysis for quality issues
- Data profiling to discover anomalies

## Tools

| Tool | Type |
|------|------|
| **Great Expectations** | Open-source Python validation |
| **dbt tests** | Built-in + custom assertions on models |
| **Apache Griffin** | Open-source for big data |
| **Monte Carlo, Bigeye, Soda** | Commercial observability platforms |

## Data Observability

Goes beyond pipeline monitoring to detect:
- Schema changes
- Distribution shifts
- Null rate changes
- Volume anomalies
- Freshness violations

## Pipeline Monitoring

| Category | Metrics |
|----------|---------|
| **Pipeline health** | DAG success/failure rate, task duration, retry count |
| **Data freshness** | Time since last update, SLA compliance |
| **Data volume** | Row count per load, deviation from expected |
| **Infrastructure** | CPU/memory/disk on workers, scheduler lag |
| **Data quality** | Failed validation count, null rate trends |

## Alerting Best Practices
- Alert on **SLA breaches**, not just failures
- Use **anomaly detection** for row counts (sudden drop/spike)
- Escalation tiers (warning -> critical -> pager)
- Include **runbook links** in alert messages
- Avoid alert fatigue - tune thresholds, group related alerts

## Gotchas
- Data Lake without governance becomes "data swamp"
- Row-level security must be tested with actual user accounts
- Prometheus pull model requires all targets to be network-accessible
- `_SUCCESS` file guarantees job completion, not data correctness

## See Also
- [[data-governance-catalog]] - governance framework
- [[data-lineage-metadata]] - tracing data issues
- [[etl-elt-pipelines]] - where quality checks run
- [[apache-airflow]] - orchestrating quality checks
