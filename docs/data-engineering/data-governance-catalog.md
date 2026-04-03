---
title: Data Governance and Catalog
category: concepts
tags: [data-engineering, data-governance, data-catalog, dama, metadata]
---

# Data Governance and Catalog

Data governance is the framework of roles, policies, standards, and metrics ensuring effective data management. A data catalog is an organized inventory of data assets enabling users to find, understand, and trust data.

## Data Management vs Governance

- **Data Management:** operational processes (how to manage roles, track compliance, maintain standards)
- **Data Governance:** framework answering "who decides what" about data

## DAMA DMBOK Disciplines

| Discipline | Description |
|-----------|-------------|
| Data Governance | Roles, policies, standards, metrics |
| Data Architecture | Logical/physical data asset structure |
| Data Modeling | ER diagrams, DDL, dbt models |
| Data Storage | Backups, security, deployment |
| Data Security | PII/PHI protection, encryption, GDPR |
| Data Integration | ETL/ELT processes |
| Master Data & Reference | Standardized definitions, dedup |
| DWH & BI | Analytical processing, reporting |
| Metadata Management | Collecting, categorizing metadata |
| Data Quality | Monitoring, defining integrity |

## Data Catalog

Searchable inventory with:
- Dataset name and description
- Location (database, schema, table)
- Owner / steward
- Update frequency, schema, column descriptions
- Tags, classifications, usage statistics

### Tools

| Tool | Type |
|------|------|
| **Apache Atlas** | Open-source metadata management |
| **DataHub** (LinkedIn) | Open-source metadata platform |
| **Amundsen** (Lyft) | Open-source data discovery |
| **Alation, Collibra** | Commercial catalogs |

## Governance Roles
- **Data Owner:** business accountability for data domain
- **Data Steward:** day-to-day quality and metadata management
- **Data Custodian:** technical implementation of policies

## GDPR and Compliance

Key requirements:
- Right to access, rectification, erasure
- Data minimization, purpose limitation
- Data protection by design and default
- Breach notification within 72 hours

### Implementation
- Data classification and tagging (PII, PHI markers)
- Encryption at rest and in transit
- Access control and audit logging
- Anonymization / pseudonymization
- Retention policies and automated deletion

## Frameworks
- **TOGAF** - enterprise architecture framework
- **Zachman** - architecture matrix
- **DAMA DMBOK2** - data management body of knowledge

## Gotchas
- Data Lake without governance becomes "data swamp"
- Hashing is NOT encryption: hashing is irreversible, encryption is reversible
- Classification must be automated - manual tagging does not scale
- Governance without enforcement is documentation, not governance

## See Also
- [[data-quality]] - quality dimensions and monitoring
- [[data-lineage-metadata]] - lineage and provenance
- [[data-lake-lakehouse]] - governance in lake context
