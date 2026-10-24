---
title: "Apache Spark et traitement de Big Data"
category: tools
tags: [data-science, spark, big-data, distributed, optimization]
level: 3
source_sha256: 14ee00167466f417300b7f7745468378dcccdea024a24b9cda9c1dfaeb792536
translation: machine
translated_at: '2026-10-24'
---
# Apache Spark et traitement de Big Data {#apache-spark-and-big-data-processing}

Lorsque les données dépassent la mémoire d'une seule machine, Spark distribue le calcul sur des clusters. Comprendre le modèle d'exécution de Spark est essentiel pour les performances.

## Architecture {#architecture}

- **SparkContext** : point d'entrée des fonctionnalités
- **Driver** : orchestre l'exécution
- **Worker Node -> Executor -> Task** : hiérarchie d'exécution
- **Partition** : unité de parallélisme des données
- **Job -> Stage -> Task** : hiérarchie de calcul

## Règles d'optimisation essentielles {#core-optimization-rules}

- **2 à 3 tâches par cœur CPU** pour un parallélisme optimal
- **~128 Mo par partition** recommandé
- Surveiller le data skew via la Spark UI
- Appliquer les filtres le plus tôt possible (predicate pushdown)
- Éviter les UDF Python (elles cassent l'optimiseur Catalyst) : privilégier les fonctions intégrées

## Shuffle {#shuffle}

Redistribution des données entre les nœuds. **Opération la plus coûteuse.**

Déclencheurs : `groupBy`, `join`, `distinct`, `repartition`, `orderBy`

Pour minimiser le shuffle :
- Filtrer avant de joindre
- Diffuser les petites tables (broadcast)
- Utiliser `coalesce` (sans shuffle) plutôt que `repartition` lorsqu'on réduit le nombre de partitions

## Techniques clés {#key-techniques}

### Broadcast Join {#broadcast-join}
Envoyer la petite table à tous les executors, évitant ainsi le shuffle.
```python
from pyspark.sql.functions import broadcast
result = big_df.join(broadcast(small_df), 'key')
```

À utiliser lorsqu'un des deux côtés est petit (< 10 Mo par défaut, configurable).

### Mise en cache {#caching}
```python
df.cache()     # in memory
df.persist()   # configurable storage level
df.unpersist() # free memory
```

Mettre en cache les DataFrames réutilisés plusieurs fois. Ne pas tout mettre en cache : la mémoire est limitée.

### Repartition vs Coalesce {#repartition-vs-coalesce}
```python
df.repartition(100)     # full shuffle, any number of partitions
df.repartition('key')   # partition by column (useful before groupBy)
df.coalesce(10)         # reduce partitions without shuffle
```

## Data Skew {#data-skew}

**Problème** : une partition beaucoup plus volumineuse que les autres, ce qui fait qu'une tâche prend un temps disproportionné.

**Détection** : la Spark UI affiche la durée des tâches. Si le maximum est très supérieur à la médiane, il y a du skew.

**Solutions** :
- **Salting** : ajouter un préfixe aléatoire à la clé asymétrique, puis joindre avec la dimension éclatée
- **Broadcast join** : pour le côté asymétrique, s'il est suffisamment petit
- **Repartitionner selon une autre clé** : redistribuer les données

## Problème des petits fichiers {#small-file-problem}

Trop de petits fichiers = trop de tâches = surcoût d'ordonnancement.

**Correctif** : compacter les fichiers via `coalesce()` ou un repartitionnement avant l'écriture.

```python
df.coalesce(10).write.parquet('output/')
```

## Dimensionnement des executors {#executor-sizing}

- **Mémoire** : trop petite = débordement sur disque (lent), trop grande = pauses du GC
- **Cœurs** : 5 cœurs par executor est une bonne valeur par défaut
- Équilibre : plus d'executors avec des ressources modérées, ou moins d'executors avec davantage de ressources

## Pièges courants {#gotchas}
- Spark est paresseux : les transformations ne s'exécutent pas tant qu'une action (collect, count, write) n'est pas déclenchée
- `collect()` ramène toutes les données sur le driver : OOM pour les grands jeux de données. Utiliser `take()` ou `show()`
- Les UDF Python sont 10 à 100 fois plus lentes que les fonctions intégrées de Spark à cause du surcoût de sérialisation
- Les jointures sur des clés asymétriques peuvent tourner indéfiniment sans intervention
- Toujours vérifier le nombre de partitions après la lecture : `df.rdd.getNumPartitions()`

## Voir aussi {#see-also}
- [[sql-for-data-science]] - Spark SQL utilise les mêmes concepts
- [[pandas-eda]] - L'API DataFrame de Spark est inspirée de pandas
- [[ds-workflow]] - Spark dans le pipeline de données
