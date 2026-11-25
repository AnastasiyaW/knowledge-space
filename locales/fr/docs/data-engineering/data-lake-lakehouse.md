---
title: "Data Lake et Lakehouse"
category: concepts
tags: [data-engineering, data-lake, lakehouse, delta-lake, iceberg, hudi]
level: 2
source_sha256: 4847fa62e0c87af4c56f10eefcdd546246d2d4c83a6b665c0d14e758b215a50f
translation: machine
translated_at: '2026-10-24'
---
# Data Lake et Lakehouse {#data-lake-and-lakehouse}

Un data lake stocke tous les types de données sans schéma strict (schema-on-read). Un lakehouse combine la souplesse de stockage d'un data lake avec les fonctionnalités d'un DWH, comme les transactions ACID et l'accès SQL.

## Data Lake {#data-lake}

### Ce qu'il stocke {#what-it-stores}
- **Structurées :** tables de bases de données, CSV
- **Semi-structurées :** JSON, XML, Avro
- **Non structurées :** logs, vidéos, images, textes

### Avantages {#advantages}
- Scalable (ajout de nœuds en horizontal)
- Économique (basé sur de l'open source : Hadoop, S3)
- Universel (tous les types de données dans un seul système)
- Test d'hypothèses rapide (pas de conception de schéma préalable)

### Inconvénients {#disadvantages}
- Faible qualité des données sans contrôles de gouvernance
- Risque de devenir un « data swamp » sans catalogage
- Difficulté à déterminer la valeur des données

### Modèle moderne {#modern-pattern}
1. Le Data Lake collecte toutes les données brutes
2. Le DWH (ou le Lakehouse) stocke les données analytiques traitées

## Data Lakehouse {#data-lakehouse}

Combine le stockage d'un Data Lake avec les fonctionnalités d'un DWH :
- Catalogues de métadonnées et schémas
- Support des transactions ACID
- Accès SQL aux données
- Optimisé pour les charges de travail BI et ML

## Formats de tables ouverts {#open-table-formats}

| Technologie | Fonctionnalités clés |
|-----------|--------------|
| **Delta Lake** | Transactions ACID, time travel, évolution de schéma, Z-ordering |
| **Apache Iceberg** | Partitionnement masqué, évolution du partitionnement, isolation par snapshot, indépendant des fournisseurs |
| **Apache Hudi** | Upserts, traitement incrémental, modifications au niveau des enregistrements, compaction |

Les trois offrent :
- Une sémantique ACID sur le stockage objet (S3, GCS, ADLS)
- Une évolution de schéma sans réécriture des données
- Du time travel / des requêtes sur snapshots
- Une gestion des métadonnées pour l'optimisation des requêtes

## Points clés {#key-facts}
- S3 est 5 à 10 fois moins cher que HDFS pour le stockage
- Le Lakehouse permet d'exécuter BI et ML sur les mêmes données sans les copier
- La séparation entre stockage et calcul permet une mise à l'échelle indépendante
- Implémentations : Databricks (Delta Lake), Snowflake, Apache Iceberg sur Spark/Trino

## Pièges à éviter {#gotchas}
- Un Data Lake sans gouvernance devient un « data swamp » : cataloguer et documenter systématiquement
- Les formats de tables nécessitent un moteur de requêtes qui les comprend (Spark, Trino, Flink)
- Le time travel a un coût de stockage : les anciens snapshots doivent être nettoyés périodiquement
- Évolution de schéma ne signifie pas absence de schéma : définir des schémas pour faciliter la découverte des données

## Voir aussi {#see-also}
- [[dwh-architecture]] - Comparaison des DWH et évolution
- [[file-formats]] - Détails sur Parquet, ORC, Avro
- [[data-governance-catalog]] - Prévenir le data swamp
- [[cloud-data-platforms]] - Implémentations cloud
