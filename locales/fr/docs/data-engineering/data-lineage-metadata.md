---
title: "Lignage des données et métadonnées"
category: concepts
tags: [data-engineering, data-lineage, metadata, observability, monitoring]
level: 2
source_sha256: 005f6253b101d8a44d290999024dac54231dcbdad259ad86bf24d128149f2d21
translation: machine
translated_at: '2026-10-24'
---
# Lignage des données et métadonnées {#data-lineage-and-metadata}

Le lignage des données décrit l'origine et les transformations des données au fil du temps : comment les données ont été transformées, ce qui a changé et pourquoi. Les métadonnées sont des « données sur les données » qui permettent la découverte, la surveillance de la qualité et la gouvernance.

## Types de lignage {#lineage-types}

| Type | Suit |
|------|--------|
| **Au niveau colonne** | Comment les colonnes individuelles se transforment à travers les étapes |
| **Au niveau table** | Quelles tables alimentent quelles autres tables |
| **Au niveau pipeline** | Dépendances entre DAG/jobs |

## Avantages du lignage {#lineage-benefits}
- **Analyse d'impact :** qu'est-ce qui casse si cette table change ?
- **Analyse des causes profondes :** d'où proviennent les mauvaises données ?
- **Conformité et pistes d'audit**
- **Génération automatique de diagrammes de flux de données**

## Catégories de métadonnées {#metadata-categories}

| Type | Exemples |
|------|---------|
| **Techniques** | Schéma, types de données, tailles des tables, index, partitions |
| **Métier** | Descriptions, propriétaires, termes du glossaire, classifications |
| **Opérationnelles** | Horodatages de chargement, nombres de lignes, durées des jobs, journaux d'erreurs |

## Pile de supervision {#monitoring-stack}

### Prometheus + Grafana {#prometheus-grafana}

**Prometheus** - supervision en mode pull :
- Collecte les métriques des cibles à intervalles configurés
- Base de données de séries temporelles pour le stockage
- PromQL pour les requêtes
- Règles d'alerte intégrées

**Grafana** - visualisation :
- Modèles de tableaux de bord prêts à l'emploi
- Prise en charge de plusieurs sources de données
- Alertes avec canaux de notification

### Exporteurs courants {#common-exporters}

| Exporteur | Métriques |
|----------|---------|
| PostgreSQL | Nombre de connexions, durée des requêtes, retard de réplication |
| Kafka | Retard des consommateurs, nombre de partitions, débit de messages |
| Node | CPU, mémoire, disque, réseau |

## Points clés {#key-facts}
- Une bonne gestion des métadonnées permet la découverte des données, la surveillance de la qualité et l'automatisation de la gouvernance
- Le lignage au niveau colonne est le plus précieux mais le plus difficile à mettre en œuvre
- Les métadonnées opérationnelles (heures de chargement, nombres de lignes) sont peu coûteuses à collecter et très utiles pour le débogage

## Pièges à éviter {#gotchas}
- Le modèle pull de Prometheus exige que toutes les cibles soient accessibles sur le réseau
- Les outils de lignage qui reposent sur l'analyse des requêtes ratent le SQL dynamique et les transformations programmatiques
- Le fichier `_SUCCESS` de MapReduce garantit la fin du job, pas l'exactitude des données

## Voir aussi {#see-also}
- [[data-quality]] - surveillance de la qualité
- [[data-governance-catalog]] - contexte de gouvernance
- [[apache-airflow]] - supervision des pipelines
