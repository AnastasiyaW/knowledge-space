---
title: "Architecture Big Data et ML"
category: concepts
tags: [bigdata, machine-learning, data-pipeline, etl, data-lake, data-warehouse, mlops]
level: 4
source_sha256: 823c926fc6606e0e3e009ce22827b4f44d7948e61fb7d1dfe41a46da8aa6f647
translation: machine
translated_at: '2026-10-24'
---
# Architecture Big Data et ML {#big-data-and-ml-architecture}

Architecture pour le traitement de grands volumes de données et l'intégration de modèles ML en production. L'architecte choisit les plateformes de traitement adaptées, conçoit les pipelines de données et assure la gouvernance des données.

## Paradigmes de traitement des données {#data-processing-paradigms}

| Paradigme | Traitement | Technologies | Idéal pour |
|----------|-----------|--------------|----------|
| **Batch** | Intervalles planifiés, gros volumes | Hadoop, Spark, Hive | ETL, rapports, analyse historique |
| **Stream** | Continu, temps réel | Kafka Streams, Flink, Storm | Détection de fraude, recommandations temps réel |

### Architecture Lambda {#lambda-architecture}
Combine batch et stream. Couche batch (précise), couche de vitesse (temps réel), couche de service qui fusionne les deux. **Inconvénient :** maintenir deux bases de code.

### Architecture Kappa {#kappa-architecture}
Uniquement du traitement en flux pour tout. Retraitement par rejeu du flux. Plus simple, mais pas adaptée à toutes les charges de travail.

## Solutions de stockage des données {#data-storage-solutions}

| Solution | Approche | Technologies | Risque |
|----------|----------|-------------|------|
| **Data Lake** | Données brutes, schéma à la lecture | HDFS, S3, Azure Data Lake | « Data swamp » sans gouvernance |
| **Data Warehouse** | Données traitées, schéma à l'écriture | Snowflake, BigQuery, Redshift, ClickHouse | Modifications de schéma rigides |
| **Data Lakehouse** | Souplesse du lake + structure du warehouse | Delta Lake, Apache Iceberg, Hudi | Plus récent, moins mature |

### Approches de modélisation des données {#data-modeling-approaches}

| Modèle | Chargement | Suivi des changements | Idéal pour |
|-------|---------|----------------|----------|
| **Inmon (3NF)** | Complexe (ordre de dépendances) | Faible | Sources déjà normalisées |
| **Kimball (en étoile)** | Plus simple | SCD de type 2 ajoute de la complexité | Analyses simples |
| **Data Vault** | Le plus simple (chargements indépendants) | Natif (satellites + horodatages) | Données évolutives et changeantes |
| **Anchor Model** | Le plus souple | Le plus souple | Besoins de flexibilité extrême |

## ETL vs ELT {#etl-vs-elt}

| Approche | Processus | Idéal pour |
|----------|---------|----------|
| **ETL** | Transformation avant chargement | DWH traditionnel |
| **ELT** | Chargement brut, transformation dans la cible | DWH cloud moderne (exploite le calcul scalable) |

## Pipeline ML {#ml-pipeline}

```php
Data collection -> Preparation/cleaning -> Feature engineering ->
  Model training -> Evaluation -> Deployment -> Monitoring/retraining
```

### Modes de service des modèles {#model-serving-patterns}

| Mode | Description | Cas d'usage |
|---------|-------------|-------------|
| **Prédiction par lots** | Prédictions pré-calculées | Recommandations, scores de risque |
| **Inférence temps réel** | Prédiction en ligne via API | Recherche, détection de fraude |
| **Inférence en périphérie** | Sur l'appareil | Mobile, IoT |
| **Modèle embarqué** | Modèle intégré au code de l'application | Prédictions légères |

### MLOps {#mlops}
Appliquer le DevOps au ML : contrôle de version pour les données et les modèles, pipelines d'entraînement automatisés, tests A/B pour le déploiement, surveillance de la dérive des modèles.

**Feature Store :** dépôt centralisé des features ML. Cohérence entre l'entraînement et le service. Produits : Feast, Tecton, Vertex AI Feature Store.

## Exemple d'architecture de pipeline de données {#data-pipeline-architecture-example}

```bash
[Source 1C] --> [Kafka topic] --> [Airflow orchestrator] --> [DWH (PostgreSQL)]
[Source CRM] --> [Kafka topic] -->                               |
[External API] --> [API Fetcher] -->                             |
                                                          [Data Marts]
                                                               |
                                                          [BI Dashboard]
```

**Décisions clés :**
- Les systèmes internes **poussent** les changements vers Kafka (la source sait quand les données changent)
- API externe : **pull** (notre système interroge périodiquement)
- Airflow pour l'orchestration ETL (supervision, relances, gestion des erreurs)
- Les scripts PHP/Python maison sont fortement déconseillés : utiliser une orchestration adaptée

## Pile technologique {#technology-stack}

| Catégorie | Technologies |
|----------|-------------|
| Traitement batch | Hadoop, Spark, Hive |
| Traitement en flux | Kafka Streams, Flink, Spark Streaming |
| Stockage | HDFS, S3, Delta Lake |
| Entrepôt de données | Snowflake, BigQuery, Redshift, ClickHouse |
| Orchestration | Airflow, Prefect, Dagster |
| Plateformes ML | MLflow, Kubeflow, SageMaker, Vertex AI |
| Qualité des données | Great Expectations, tests dbt |

## Considérations d'architecture {#architecture-considerations}

- **Volume** - TB ou PB détermine les choix de stockage et de traitement
- **Vélocité** - le temps réel oriente vers le streaming ou le batch
- **Variété** - données structurées, semi-structurées ou non structurées influencent le stockage
- **Gouvernance des données** - confidentialité (RGPD), contrôle d'accès, pistes d'audit, traçabilité (lineage)
- **Coût** - dimensionnement du calcul, hiérarchisation du stockage, instances spot
- **Qualité des données** - garbage in, garbage out. Valider à l'entrée du pipeline

## Pièges à éviter {#gotchas}

- **Un data lake sans gouvernance** devient un « data swamp » : personne ne peut trouver ni faire confiance aux données
- **Le temps réel n'est pas toujours nécessaire** : un batch quotidien peut suffire pour un directeur qui consulte ses rapports du matin
- **Les données sources changent rétroactivement** : les données de ventes peuvent changer pendant plus d'un an (remboursements, recalculs). Concevoir un historique immuable (Data Vault)
- **Interroger la base source est risqué** : on ne connaît pas tous les changements de données, et les changements de schéma cassent les scripts. Privilégier le modèle push

## Voir aussi {#see-also}

- [[kafka-architecture]] - Streaming d'événements pour les pipelines de données
- [[database-selection]] - OLTP vs OLAP, types de bases de données
- [[distributed-systems-fundamentals]] - Partitionnement, réplication pour le big data
- [[devops-cicd]] - MLOps comme extension du DevOps
