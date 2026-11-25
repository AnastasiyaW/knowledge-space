---
title: "MapReduce"
category: concepts
tags: [data-engineering, mapreduce, hadoop, distributed-computing, batch]
level: 3
source_sha256: 1e80955c2a197d8e3ccb866d40bdf96000c7d8f9d15cc7be717a14202a0a98be
translation: machine
translated_at: '2026-10-24'
---
# MapReduce {#mapreduce}

MapReduce est un modèle de programmation pour le traitement distribué de données. Il repose sur deux opérations définies par l'utilisateur : Map (transformation/filtrage) et Reduce (agrégation). Le framework garantit que tous les enregistrements ayant la même clé arrivent au même Reducer.

## Paradigme {#paradigm}

```bash
Map:    (K1, V1) -> list(K2, V2)    -- transform each record
Reduce: (K2, list(V2)) -> list(K3, V3)  -- aggregate by key
```

## Pipeline d'exécution {#execution-pipeline}

```php
Input -> Split -> Map -> Spill -> Sort/Merge -> Shuffle -> Reduce -> Output
```

1. **Split :** InputFormat découpe les données en morceaux. Chaque split -> un Mapper
2. **Map :** Chaque Mapper traite son split via RecordReader. Sortie vers un tampon circulaire
3. **Spill :** Le tampon se remplit -> les données sont écrites sur le disque local (PAS sur HDFS). Partitionnées par `hash(key) % numReducers`
4. **Sort/Merge :** Le Mapper trie et fusionne (merge-sort) les fichiers de spill par partition de Reducer
5. **Shuffle :** Les Reducers **récupèrent** (pull) les données depuis les Mappers (v2 inverse le sens par rapport à v1)
6. **Reduce :** Fusion (merge-sort) des fichiers reçus, traitement du flux clé-valeur trié
7. **Output :** Un fichier de sortie par Reducer sur HDFS

## Hadoop Streaming (Python) {#hadoop-streaming-python}

```bash
hadoop jar $HADOOP_MAPRED_HOME/hadoop-streaming.jar \
  -mapper mapper.py \
  -reducer reducer.py \
  -file /local/path/mapper.py \
  -file /local/path/reducer.py \
  -input /hdfs/input/ \
  -output /hdfs/output/
```

## Détails clés {#key-details}
- **Split != bloc HDFS :** Les splits sont logiques (peuvent provenir d'une base de données, de S3) ; les blocs sont physiques
- **Types d'InputFormat :** TextInputFormat (par défaut), NLineInputFormat (N lignes par mapper), DBInputFormat
- **Nombre de Mappers :** déterminé par la logique de découpage de l'InputFormat, non directement configurable
- **Nombre de Reducers :** configurable via `mapreduce.job.reduces`
- **Fichier `_SUCCESS` :** marqueur vide indiquant la fin du job. Les fichiers commençant par `_` ou `.` sont ignorés par les jobs suivants
- **Le répertoire de sortie ne doit PAS exister** avant le lancement du job (protection contre l'écrasement de données)

## MapReduce v1 vs v2 {#mapreduce-v1-vs-v2}
- **v1 :** Les Mappers poussaient les données vers les Reducers -> DDoS sur les Reducers
- **v2 :** Les Reducers récupèrent les données depuis les Mappers (sens inversé)

## Pièges courants {#gotchas}
- Le surcoût d'initialisation des conteneurs domine pour les petits jeux de données (40 s pour 100 Ko avec 31 mappers contre 9 s avec 3)
- Un split n'est PAS la même chose qu'un bloc HDFS : ce sont deux couches d'abstraction différentes
- Hadoop Streaming (Python) ne propose pas certaines fonctionnalités de MapReduce Java (pas de hooks setup/cleanup)
- MapReduce est une technologie héritée : privilégier Spark pour les nouvelles charges de travail

## Voir aussi {#see-also}
- [[hadoop-hdfs]] - couche de stockage
- [[yarn-resource-management]] - allocation des ressources
- [[apache-hive]] - interface SQL au-dessus de MapReduce
- [[apache-spark-core]] - remplaçant moderne
