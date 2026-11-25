---
title: "Architecture d'entrepôt de données"
category: concepts
tags: [data-engineering, dwh, data-warehouse, olap, oltp, architecture]
level: 3
source_sha256: 6b1e53e88c61416e603d7d64eced4eae2e1ec17a385a5f722b31bc235048566e
translation: machine
translated_at: '2026-10-24'
---
# Architecture d'entrepôt de données {#data-warehouse-architecture}

Un entrepôt de données (DWH, *data warehouse*) est une collection de données orientée sujet, intégrée, non volatile et historisée, organisée pour soutenir la prise de décision (Bill Inmon). Le DWH existe parce que les charges OLTP et OLAP sont fondamentalement incompatibles au sein d'un même système.

## OLTP vs OLAP {#oltp-vs-olap}

| Caractéristique | OLTP | OLAP |
|---------------|------|------|
| Objectif | Traitement transactionnel | Requêtes analytiques |
| Requêtes | Simples, fréquentes, identiques | Complexes, peu fréquentes, ad hoc |
| Utilisateurs | Nombreux, simultanés | Peu d'analystes |
| Données | Actuelles, opérationnelles | Historiques, agrégées |
| Opérations | Lecture/écriture (CRUD) | Principalement lecture |
| Latence | Micro/millisecondes | De quelques secondes à quelques minutes |
| Exemples | PostgreSQL, MySQL (par service) | Snowflake, ClickHouse, Greenplum |

## Propriétés du DWH (Inmon) {#dwh-properties-inmon}

| Propriété | Signification |
|----------|---------|
| **Orienté sujet** | Couvre des domaines métier spécifiques ; les données non pertinentes sont exclues |
| **Intégré** | Aucune contradiction entre les données provenant de sources différentes |
| **Non volatile** | Les données sont uniquement ajoutées, jamais modifiées ni supprimées |
| **Historisé** | Conserve la profondeur historique maximale |

## Couches du DWH {#dwh-layers}

```rust
Sources -> Staging Area -> Central Warehouse -> Data Marts -> BI/Analytics
```

| Couche | Objectif |
|-------|---------|
| **Staging Area** | Réception des données brutes, nettoyage et normalisation avant chargement |
| **MDM (données de référence)** | Données de référence et de consultation garantissant la cohérence |
| **Entrepôt central** | Données historisées, orientées sujet et intégrées |
| **Data Marts / Cubes** | Vues spécialisées pour des tâches analytiques précises |

## Approches de conception {#design-approaches}

### Kimball (ascendante) {#kimball-bottom-up}
- DWH = ensemble de data marts
- Conception des marts selon les besoins de chaque consommateur (schéma en étoile)
- Livraison rapide de la valeur métier
- **Inconvénients :** les marts peuvent définir les métriques différemment ; difficile à standardiser

### Inmon (descendante) {#inmon-top-down}
- Construire d'abord le DWH d'entreprise (3NF), puis dériver les marts
- Source unique de vérité, meilleure cohérence
- **Inconvénients :** développement initial plus long, plus complexe

### Data Vault 2.0 {#data-vault-20}
- Gère de nombreuses sources aux schémas différents
- Ajout seul (*append-only*), auditabilité complète
- Règles métier isolées dans la couche mart
- Voir [[data-vault]] pour plus de détails

## Évolution des plateformes {#platform-evolution}

```rust
Gen 1: RDBMS DWH (Oracle, DB2) - 1990s
  -> Rigid schema, ETL, batch only

Gen 2: Hadoop ecosystem (HDFS + MapReduce) - 2007+
  -> Data Lake, schema-on-read, horizontal scale

Gen 3: Cloud DWH + Lakehouse - 2015+
  -> Snowflake, Databricks, BigQuery
  -> ELT, auto-scaling, separation of compute/storage

Gen 4: Data Mesh / Data Products - 2020+
  -> Domain-owned data, self-serve platform, federated governance
```

## Choisir une architecture {#choosing-architecture}

| Scénario | Recommandation |
|----------|-------------|
| Petite entreprise, données structurées, orientée BI | DWH cloud (Snowflake, BigQuery) |
| Types de données variés, charges de ML | Data Lakehouse (Databricks, Iceberg) |
| Grande entreprise, nombreuses sources, conformité | DWH + Data Lake en configuration hybride |
| Analytique temps réel + batch | Lambda/Kappa avec une couche de streaming |
| Nombreuses équipes data autonomes | Data Mesh avec plateforme en libre-service |

## Pièges courants {#gotchas}
- La dénormalisation des schémas en étoile échange de l'espace de stockage contre les performances de requêtes : acceptable pour l'OLAP
- Data Vault ajoute de nombreuses jointures : la couche mart doit pré-joindre les données pour obtenir des performances de requêtes acceptables
- Les bases OLTP ne doivent jamais être interrogées directement à des fins analytiques : répliquer systématiquement vers le DWH
- La fenêtre de traitement batch doit se terminer avant les heures ouvrées : surveiller et alerter en cas de dépassement de SLA
- Un Data Lake sans gouvernance devient un « data swamp » (marécage de données)

## Voir aussi {#see-also}
- [[data-modeling]] - théorie de la normalisation
- [[dimensional-modeling]] - schémas en étoile et en flocon de Kimball
- [[data-vault]] - méthodologie Data Vault
- [[data-lake-lakehouse]] - modèles Data Lake et Lakehouse
- [[cloud-data-platforms]] - implémentations de DWH cloud
