---
title: "Gestion des ressources YARN"
category: tools
tags: [data-engineering, yarn, hadoop, resource-management, cluster]
level: 2
source_sha256: e472d73a6e25bc5d74db96361e0a37ef7b8daf4bc382994d791df20c984573ba
translation: machine
translated_at: '2026-10-24'
---
# Gestion des ressources YARN {#yarn-resource-management}

YARN (Yet Another Resource Negotiator) a remplacé le JobTracker monolithique de Hadoop v1 par une architecture de gestion des ressources distribuée. Il sépare l'allocation des ressources de la coordination des jobs.

## Évolution depuis Hadoop v1 {#evolution-from-hadoop-v1}

**v1 (JobTracker/TaskTracker) :**
- JobTracker : coordinateur unique pour TOUS les jobs - soumission, supervision, ressources
- TaskTracker : par nœud, slots Map/Reduce rigides
- **Problème :** le JobTracker = point de défaillance unique. À grande échelle, submergé par les mises à jour de statut

**v2+ (YARN) :**
- **ResourceManager (RM) :** gère les ressources du cluster via des conteneurs abstraits
- **NodeManager :** agent par nœud, remonte son statut au RM
- **ApplicationMaster (AM) :** coordinateur par job. Gère ses propres tâches
- **Container :** processus Java isolé avec un allocation de CPU + RAM

**Amélioration clé :** le RM ne fait qu'allouer des conteneurs. L'AM gère la logique propre à chaque job. Cela répartit la charge centralisée qui a fait tomber le JobTracker.

## Configuration des files d'attente {#queue-configuration}

```text
root
  |-- engineering (40%)
  |-- marketing (30%)
  |-- support (30%)
```

Chaque file d'attente dispose de ressources minimales garanties, d'un plafond maximal, et de la capacité d'emprunter aux files moins chargées.

## Types d'ordonnanceurs {#scheduler-types}

| Ordonnanceur | Comportement | Compromis |
|--------------|--------------|-----------|
| **FIFO** | Séquentiel strict | Rarement utilisé |
| **Capacity** | Parallèle si ressources disponibles | Par défaut dans de nombreuses distributions |
| **Fair** | Préempte les jobs en cours pour en lancer de nouveaux | Meilleure utilisation, mais gaspille du travail |

**Piège du Fair Scheduler :** la préemption tue les conteneurs proches de la fin, ce qui entraîne un travail perdu.

## Points essentiels {#key-facts}
- Les conteneurs peuvent exécuter n'importe quoi : MapReduce, Spark, serveurs HTTP
- Le ResourceManager ne suit PAS la progression des tâches individuelles - seul l'AM le fait
- Une planification basée sur le temps est possible (90 % pour l'ETL la nuit, davantage pour l'analytique le jour)
- Priorités au niveau des files, configurées par file

## Pièges {#gotchas}
- La préemption du Fair Scheduler peut tuer des tâches presque terminées
- Le coût d'initialisation des conteneurs domine pour les petites données
- YARN a remplacé les slots Map/Reduce rigides par des conteneurs flexibles
- Le RM reste un SPOF potentiel - utiliser la configuration HA

## Voir aussi {#see-also}
- [[hadoop-hdfs]] - couche de stockage
- [[mapreduce]] - paradigme de traitement
- [[apache-spark-core]] - Spark sur YARN
- [[kubernetes-for-de]] - alternative moderne pour la gestion des ressources
