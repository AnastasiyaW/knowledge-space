---
title: "Plateformes de données cloud"
category: tools
tags: [data-engineering, cloud, aws, gcp, snowflake, bigquery, s3]
level: 4
source_sha256: fedee1bace17ec71fea61b3eed8b8d7c051c3a3cd715a3120b245d1d12dee42c
translation: machine
translated_at: '2026-10-24'
---
# Plateformes de données cloud {#cloud-data-platforms}

Les plateformes cloud séparent le calcul du stockage, ce qui permet une mise à l'échelle élastique et une tarification à l'usage. Le « Big Three » (AWS, GCP, Azure) auquel s'ajoute Snowflake constitue la base de l'ingénierie des données moderne.

## Comparaison des modèles de service {#service-model-comparison}

| On-Premise | AWS | GCP | Usage |
|-----------|-----|-----|---------|
| HDFS | S3 | Cloud Storage | Stockage objet |
| Spark | EMR | Dataproc | Calcul distribué |
| Kafka | MSK / Kinesis | Pub/Sub | Streaming d'événements |
| PostgreSQL | RDS | Cloud SQL | SGBDR managé |

## Options de DWH cloud {#cloud-dwh-options}

| Système | Type | Caractéristique principale |
|--------|------|-------------|
| **Athena** | Service de requêtes | Presto managé, interroge S3 sans chargement |
| **Redshift** | DWH MPP | Architecture la plus proche de Greenplum |
| **BigQuery** | DWH serverless | Pas de contrôle du calcul : serverless au sens strict |
| **Snowflake** | Calcul/stockage séparés | Démarre des clusters à chaque requête, données dans S3 |
| **Presto/Trino** | Moteur de requêtes fédéré | Interroge les données des systèmes sources sans ETL |

## S3 - Simple Storage Service {#s3-simple-storage-service}
- 5 à 10 fois moins cher que HDFS
- Durabilité de 99,999999999 % (11 neuf)
- Élasticité pratiquement illimitée
- Sépare le stockage du calcul
- Accès via `boto3` (Python), la CLI ou Spark (`s3a://`)

## Modèles de service cloud pour l'ingénierie des données {#cloud-service-models-for-de}

| Approche | Exemples | Responsabilité du DE |
|----------|---------|-------------------|
| **IaaS** | ClickHouse auto-géré sur des VM | OS, base de données, supervision, sauvegardes |
| **PaaS** | ClickHouse managé, RDS | Configuration du service |
| **SaaS** | BigQuery, Snowflake | Écriture des requêtes uniquement |

## Architecture de Snowflake {#snowflake-architecture}
- Trois couches : stockage, calcul, services
- Pas d'accès direct à la couche de stockage
- Micro-partitionnement automatique
- Clusters virtuels (entrepôts) pour différentes charges de travail
- Facturation du temps de calcul par requête

## Bonnes pratiques VM et disques {#vm-and-disk-best-practices}

**Les performances des disques dépendent de leur taille (QoS).** Un SSD de 50 Go peut être lent, car les IOPS sont limitées proportionnellement. Solution : augmenter la taille du disque pour obtenir plus d'IOPS.

| Type de disque | Idéal pour |
|-----------|---------|
| HDD | Le moins cher, archives |
| SSD | Dev/test (rapport coût/efficacité) |
| SSD à IOPS élevées | Charges de production |
| NVMe local | Performances maximales, sans réplication |

## Gestion des coûts {#cost-management}
- **Toujours mettre en pause ou arrêter** les VM, bases de données et clusters K8s inutilisés
- Clusters éphémères pour les tâches ponctuelles : créer, utiliser, détruire
- HDD pour le dev/test, SSD pour la préproduction, IOPS élevées pour la production
- Surveiller les limites QoS : les petits disques ont des quotas d'IOPS plus faibles

## Modèle de données cloud-native {#cloud-native-data-pattern}
```text
Storage Layer: S3 (or compatible)
Compute Layer: Kubernetes (Spark, Presto run here)
```
La séparation permet un calcul élastique indépendant du stockage.

## Pièges à éviter {#gotchas}
- Les nœuds Redshift incluent par défaut le calcul et le stockage ; Snowflake les sépare nativement
- La montée en charge verticale nécessite un redémarrage de la VM (interruption de service)
- Toujours configurer le pare-feu : toute VM dotée d'une IP publique est une cible
- La latence réseau entre datacenters dégrade fortement les performances d'un cluster avec réplication synchrone
- BigQuery : l'absence de contrôle du calcul peut entraîner des coûts imprévus sur les requêtes complexes

## Voir aussi {#see-also}
- [[dwh-architecture]] - contexte de conception du DWH
- [[kubernetes-for-de]] - orchestration du calcul
- [[docker-for-de]] - bases de la conteneurisation
- [[data-lake-lakehouse]] - lakehouse sur le cloud
