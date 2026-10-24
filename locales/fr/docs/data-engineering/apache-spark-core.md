---
title: "Architecture de base d'Apache Spark"
category: tools
tags: [data-engineering, spark, distributed-computing, pyspark, architecture]
level: 3
source_sha256: 7952ae4e9797fd4455229889842cc37107005f3b7e6b108ad5d01ab56e158ec0
translation: machine
translated_at: '2026-10-24'
---
# Architecture de base d'Apache Spark {#apache-spark-core-architecture}

Apache Spark est un framework open source de traitement de données distribué. Avantages principaux par rapport à MapReduce : calcul en mémoire, API unifiée pour le batch, le streaming, le ML et le graphe, prise en charge de Python, Scala, Java et R.

## Composants du cluster {#cluster-components}

| Composant | Rôle |
|-----------|------|
| **Cluster Manager** | Alloue les ressources. Options : Standalone, YARN, Kubernetes, Mesos |
| **Driver** | Processus maître : convertit l'application en tâches, planifie, suit la progression |
| **SparkContext / SparkSession** | Point d'entrée pour interagir avec le cluster |
| **Worker Node** | Serveur ou VM exécutant des processus Executor |
| **Executor** | Processus sur un Worker qui exécute les Tasks |
| **Task** | Unité minimale de travail : une opération sur une Partition |
| **Partition** | Unité logique minimale de données. Nombre de partitions de shuffle par défaut : 200 |

## Modes de déploiement {#deploy-modes}

- **Mode client :** Driver sur la machine de soumission ; arrêter le client tue tous les executors
- **Mode cluster :** Driver et executors sont tous sur le cluster ; le client sert uniquement à la soumission
- **Mode local :** Tout tourne dans une seule JVM. `--master local[*]` utilise tous les cœurs. Pour le développement et les tests

## Hiérarchie d'exécution {#execution-hierarchy}

```php
Application -> Job(s) -> Stage(s) -> Task(s)
```

- **Job :** créé par l'appel d'une Action
- **Stage :** ensemble de Tasks sans frontière de Shuffle
- **Task :** une opération sur une Partition
- **Shuffle :** redistribution des données entre les nœuds. Déclenché par `join`, `groupBy`, `distinct`, `repartition`

## Pile Spark {#spark-stack}

| Module | Rôle |
|--------|------|
| **Spark Core** | Ordonnancement des tâches, gestion de la mémoire, tolérance aux pannes |
| **Spark SQL + DataFrames** | Données structurées via SQL ou l'API DataFrame |
| **Spark Streaming** | Traitement temps réel en micro-batchs |
| **MLlib** | ML distribué |
| **GraphX** | Traitement de graphes |

## Structures de données {#data-structures}

### RDD (Resilient Distributed Dataset) {#rdd-resilient-distributed-dataset}
API de plus bas niveau. Immuable, évaluation paresseuse, tolérant aux pannes grâce au lignage DAG. À utiliser pour les données non structurées ou les fichiers média.

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])
```

### DataFrame {#dataframe}
Collection distribuée de colonnes nommées. Objet principal de PySpark. Optimiseur Catalyst pour la planification des requêtes.

### Dataset {#dataset}
DataFrame typé (Scala/Java uniquement). Non disponible en Python.

## Évaluation paresseuse {#lazy-evaluation}

Spark construit un plan logique optimisé par le **Catalyst Optimizer** (pushdown de prédicats, repliement de constantes, réordonnancement des filtres). L'exécution ne démarre que lorsqu'une Action est appelée.

**Transformations (paresseuses) :**
- **Étroites** (sans shuffle) : `map`, `filter`, `select`, `withColumn`
- **Larges** (déclenchent un shuffle) : `join`, `groupBy`, `distinct`, `repartition`, `orderBy`

**Actions (déclenchent l'exécution) :**
```python
df.show()              # display rows
df.count()             # count rows
df.collect()           # all to driver (OOM risk!)
df.toPandas()          # convert to Pandas (all to driver)
df.write.parquet(path) # write to file
```

## Pipeline de l'optimiseur Catalyst {#catalyst-optimizer-pipeline}

1. **Planification logique :** analyse syntaxique -> analyse -> optimisation (pushdown de prédicats, repliement de constantes)
2. **Planification physique :** génération de plusieurs plans -> sélection basée sur le coût
3. **Tungsten :** génération de code au niveau de l'étape entière (whole-stage code generation) pour l'efficacité CPU

## spark-submit {#spark-submit}

```bash
spark-submit \
  --master spark://master:7077 \
  --deploy-mode cluster \
  --executor-memory 4g \
  --executor-cores 4 \
  --num-executors 10 \
  app.py [args]
```

## PySpark vs Pandas {#pyspark-vs-pandas}

| Caractéristique | PySpark | Pandas |
|-----------------|---------|--------|
| Exécution | Distribuée | Machine unique |
| Évaluation | Paresseuse | Immédiate |
| Mutabilité | Immuable | Mutable |
| Échelle | To+ | Limitée par la RAM |

## Pièges à éviter {#gotchas}
- `collect()` et `toPandas()` ramènent toutes les données au driver : risque d'OOM sur les grands jeux de données
- Les UDF contournent l'optimiseur Catalyst et entraînent une surcharge de sérialisation Python-JVM
- `inferSchema=True` lit l'intégralité du CSV pour déterminer les types : lent sur les gros fichiers
- L'API Structured de Spark Streaming n'autorise pas les actions terminales au milieu du pipeline
- Spark sur Kubernetes est prêt pour la production depuis Spark 3.1 (mars 2021)

## Voir aussi {#see-also}
- [[pyspark-dataframe-api]] - référence des opérations DataFrame
- [[spark-optimization]] - réglage des performances
- [[spark-streaming]] - traitement temps réel
- [[etl-elt-pipelines]] - Spark comme moteur ETL
