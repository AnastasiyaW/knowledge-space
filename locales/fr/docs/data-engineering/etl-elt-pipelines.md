---
title: "Pipelines ETL/ELT"
category: concepts
tags: [data-engineering, etl, elt, pipelines, data-integration]
level: 3
source_sha256: 287713e6dd499afaa5b6f53aae04ee3c248838600a1e95746190a5d261a84930
translation: machine
translated_at: '2026-10-24'
---
# Pipelines ETL/ELT {#etlelt-pipelines}

ETL (Extract-Transform-Load) et ELT (Extract-Load-Transform) sont les deux modèles fondamentaux pour déplacer des données des systèmes sources vers un stockage analytique. La distinction réside dans l'emplacement de la transformation : à l'extérieur ou à l'intérieur du système cible.

## ETL vs ELT {#etl-vs-elt}

| Aspect | ETL | ELT |
|--------|-----|-----|
| Lieu de la transformation | Moteur externe (Spark, Python) | Au sein du DWH cible (SQL) |
| Idéal pour | Transformations complexes, systèmes legacy | DWH cloud disposant d'une forte capacité de calcul |
| Latence | Plus élevée (saut supplémentaire) | Plus faible |
| Flexibilité | Contrôle accru sur la transformation | Dépend des capacités SQL de la cible |
| Outils modernes | Spark, Airflow + Python | dbt, Snowflake, BigQuery |

## Trois étapes {#three-steps}

1. **Extract (E) :** Extraire les données des sources, les valider par rapport aux spécifications, les placer en zone de transit intermédiaire
2. **Transform (T) :** Conversion de format, normalisation de l'encodage, agrégation, nettoyage, déduplication, logique métier
3. **Load (L) :** Écrire les données transformées ainsi que les métadonnées dans le système cible (DWH, data mart, lac de données)

## Architecture en couches de données {#data-layers-architecture}

```php
Sources -> [STG/Raw] -> [Core/DDS] -> [Marts] -> BI/Analytics
```

| Couche | Rôle |
|--------|------|
| **Staging / Raw / ODS** | Données brutes issues des sources, transformation minimale, conservation du format d'origine. Découple l'extraction de la transformation |
| **Core / DDS (Intégration)** | Données nettoyées, intégrées et historisées. Data Vault, 3NF ou modélisation dimensionnelle appliquées à ce niveau |
| **Mart / Présentation** | Vues agrégées prêtes pour le métier (schéma en étoile, tables plates). Chaque mart sert des consommateurs spécifiques |

## Modes de traitement des pipelines {#pipeline-processing-modes}

| Mode | Latence | Complexité | Idéal pour |
|------|---------|-----------|------------|
| **Batch** | De quelques minutes à quelques heures | Faible | BI, reporting, analyse historique |
| **Micro-batch** | De quelques secondes à quelques minutes | Moyenne | Tableaux de bord quasi temps réel |
| **Stream** | Millisecondes | Élevée | Détection de fraude, supervision, fonctionnalités temps réel |

### Architecture Lambda {#lambda-architecture}
- **Couche batch :** données complètes et exactes, avec une latence plus élevée
- **Couche de vitesse (speed) :** approximations en temps réel
- **Couche de service (serving) :** fusionne les deux pour les requêtes

## Patterns {#patterns}

### ETL Spark typique {#typical-spark-etl}

```python
from pyspark.sql import SparkSession, functions as f

spark = SparkSession.builder.appName("etl").getOrCreate()

# Extract
df = spark.read.csv("s3a://bucket/raw/*.csv", header=True, schema=schema)

# Transform
result = (df
    .filter(f.col("vendor_id").isNotNull())
    .groupBy("vendor_id", f.to_date("pickup_datetime").alias("dt"))
    .agg(
        f.sum("total_amount").alias("sum_amount"),
        f.avg("tip_amount").alias("avg_tips")
    )
)

# Load
result.write.mode("overwrite").parquet("s3a://bucket/mart/daily_summary/")
```

### Modes d'écriture {#write-modes}
- `overwrite` - remplacer les données existantes
- `append` - ajouter aux données existantes
- `ignore` - ignorer si les données existent déjà
- `error` (par défaut) - échouer si les données existent déjà

### Script Python de migration de données {#python-data-migration-script}

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://user:pass@host:port/db')
df = pd.read_sql("SELECT * FROM source WHERE dt BETWEEN %s AND %s", engine, params=[start_dt, end_dt])
df.to_sql('target_table', engine, if_exists='append', index=False)
```

## Points clés {#key-facts}
- L'**idempotence** est essentielle : relancer un pipeline avec les mêmes entrées doit produire les mêmes sorties. Utiliser le mode `overwrite` ou la stratégie suppression-puis-insertion
- Les **chargements incrémentaux** ne traitent que les données nouvelles ou modifiées, à l'aide de watermarks, de CDC ou d'horodatages de dernière modification
- Le **filtrage précoce** déplace les filtres au plus près de la source afin de réduire le volume de données
- **Schéma d'abord :** définir des schémas explicites plutôt que de s'appuyer sur l'inférence
- Les **écritures partitionnées** (`partitionBy("year", "month")`) permettent des lectures aval efficaces

## Pièges {#gotchas}
- Le `schedule_interval` d'Airflow définit l'intervalle entre deux exécutions, et non l'heure d'exécution. Un DAG avec `@daily` et `start_date=2024-01-01` s'exécute pour la première fois le `2024-01-02`
- `catchup=True` (par défaut) rejoue tous les intervalles manqués depuis `start_date`, ce qui peut saturer le système
- Les jointures SCD2 entre satellites ayant des fréquences de changement différentes provoquent une explosion cartésienne sur les plages de dates
- Problème des petits fichiers : un nombre trop élevé de partitions crée de minuscules fichiers, ce qui dégrade les performances de HDFS/S3

## Voir aussi {#see-also}
- [[apache-airflow]] - orchestration de pipelines
- [[apache-spark-core]] - moteur de traitement distribué
- [[dwh-architecture]] - architecture du stockage cible
- [[data-quality]] - validation des pipelines
- [[data-lake-lakehouse]] - cibles de stockage modernes
