---
title: "Optimisation des performances de Spark"
category: reference
tags: [data-engineering, spark, optimization, partitioning, skew, broadcast]
level: 4
source_sha256: dd810ed7957280bd35cd7b5f7a2e5b969744b853ce5dfa5e274ccbef55c97db0
translation: machine
translated_at: '2026-10-24'
---
# Optimisation des performances de Spark {#spark-performance-optimization}

L'optimisation de Spark repose sur la minimisation des shuffles, la gestion des partitions et l'exploitation efficace de l'optimiseur Catalyst.

## Gestion des partitions {#partition-management}

**Partitions de shuffle par défaut :** 200. Configuration :

```python
spark.conf.set("spark.sql.shuffle.partitions", 400)
spark.conf.set("spark.default.parallelism", 400)
```

**Nombre optimal de partitions :**
```text
num_executors * executor_cores * (2 to 4)
```

**Taille cible d'une partition :** ~128 Mo (plage : 64-256 Mo).

### Repartition ou Coalesce {#repartition-vs-coalesce}

```python
df = df.repartition(1000)                    # by count (triggers full shuffle)
df = df.repartition("col1", "col2")          # by columns
df = df.coalesce(10)                         # reduce without full shuffle
```

**Règle :** `coalesce` pour réduire le nombre de partitions, `repartition` pour l'augmenter.

## Problème des petits fichiers {#small-file-problem}

Un grand nombre de petits fichiers (< 128 Mo, taille de bloc HDFS) entraîne : une surcharge du NameNode, des lectures lentes et un nombre excessif de petites tâches.

**Solutions :**
- `repartition(N)` - crée N fichiers de taille égale (shuffle)
- `coalesce(N)` - réduit le nombre de partitions sans shuffle complet (tailles potentiellement inégales)

## Asymétrie des données (data skew) {#data-skew}

Lorsque certaines partitions contiennent beaucoup plus de données que les autres : exécuteurs surchargés, ressources inactives, risque d'OOM.

### Solution 1 : Broadcast Hash Join {#solution-1-broadcast-hash-join}

Pour joindre une grande table avec une petite table (la petite doit tenir dans la mémoire de l'exécuteur) :

```python
spark.table("big").join(spark.table("small").hint("broadcast"), "key")
# Auto-broadcast threshold:
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 104857600)  # 100MB
```

### Solution 2 : Salting des clés {#solution-2-key-salting}

Ajouter un suffixe aléatoire aux clés asymétriques pour répartir la charge uniformément :

```python
df_big = df_big.withColumn('city', F.concat(
    F.col('city'), F.lit('_'),
    F.floor(F.rand(seed=17) * 5 + 1).cast('string')
))
# Explode corresponding keys in smaller table to match
```

### Solution 3 : Adaptive Query Execution (AQE) {#solution-3-adaptive-query-execution-aqe}

Activée automatiquement depuis Spark 3.0 :

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
# Skew threshold: partition > 5x median AND > 256MB
```

## Autres techniques d'optimisation {#other-optimization-techniques}

| Technique | Détails |
|-----------|---------|
| **Filtrage précoce** | Filtrer avant les shuffles pour réduire le volume de données |
| **Éviter les UDF** | Les UDF contournent Catalyst et provoquent une sérialisation Python-JVM. Privilégier les fonctions natives |
| **Mise en cache** | `df.cache()` ou `df.persist(StorageLevel.MEMORY_AND_DISK)` pour les DataFrames réutilisés |
| **Formats colonnaires** | Parquet/ORC prennent en charge le predicate pushdown et l'élagage de colonnes |
| **Dimensionnement des exécuteurs** | 3 à 5 cœurs par exécuteur ; réserver 1 cœur pour le système d'exploitation ; 2 à 3 tâches par cœur CPU |

## Points de vigilance {#gotchas}
- `repartition` déclenche toujours un shuffle complet ; `coalesce` n'en déclenche pas, mais peut produire des partitions inégales
- Broadcast join : la plus petite table doit tenir à la fois dans la mémoire du driver ET dans celle des exécuteurs
- Les 200 partitions de shuffle par défaut peuvent être insuffisantes pour de gros volumes, ou excessives pour de petits volumes
- La mise en cache n'est pas toujours bénéfique : tester avant de l'adopter ; à vérifier dans l'onglet Storage de l'interface Spark UI
- AQE dans Spark 3.0+ gère automatiquement de nombreux cas d'asymétrie

## Voir aussi {#see-also}
- [[apache-spark-core]] - principes d'architecture
- [[pyspark-dataframe-api]] - opérations sur les DataFrames
- [[file-formats]] - avantages de Parquet/ORC
