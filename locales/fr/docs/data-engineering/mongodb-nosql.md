---
title: "MongoDB et NoSQL"
category: tools
tags: [data-engineering, mongodb, nosql, document-database, cap-theorem]
level: 4
source_sha256: 868b800507c06b8d8e2bc062f96188b25ea5e4649f9769ed81b259b8b14f1a15
translation: machine
translated_at: '2026-10-24'
---
# MongoDB et NoSQL {#mongodb-and-nosql}

MongoDB est une base de données NoSQL orientée documents, conçue pour les scénarios où les bases relationnelles atteignent leurs limites de scalabilité. Les bases NoSQL (« Not Only SQL ») répondent aux défis des 3V du big data : Volume, Vélocité, Variété.

## Modèles NoSQL {#nosql-models}

| Modèle | Structure | Cas d'usage | Exemples |
|-------|-----------|----------|----------|
| **Clé-valeur** | clé -> valeur | Cache, sessions | Redis, DynamoDB |
| **Document** | Documents JSON/BSON | Contenus, catalogues | MongoDB, CouchDB |
| **Famille de colonnes** | Groupes de colonnes | Séries temporelles, analytique | Cassandra, HBase |
| **Graphe** | Nœuds + arêtes | Réseaux sociaux | Neo4j, JanusGraph |

## Théorème CAP {#cap-theorem}

Dans tout système distribué, on ne peut garantir que deux des trois propriétés suivantes : **Cohérence** (Consistency), **Disponibilité** (Availability), **Tolérance au partitionnement** (Partition tolerance). MongoDB est de type CP (Cohérence + Tolérance au partitionnement) par défaut.

## Architecture de MongoDB {#mongodb-architecture}

- **Replica Set :** 3 processus mongod, bascule automatique (failover)
- **Sharding :** répartit les données selon la clé de shard pour une montée en charge horizontale
- 1 shard = 1 replica set

## Opérations CRUD {#crud-operations}

```javascript
// Filtering
{ capital: "Moscow" }
{ area: { $gt: 5000000 } }
{ borders: { $size: 2 } }
{ $and: [{ "languages.eng": { $exists: true } }, { region: "Asia" }] }
```

## Pipelines d'agrégation {#aggregation-pipelines}

```javascript
[
  { "$unwind": { "path": "$scores" } },
  { "$group": { "_id": "$scores.type", "avg": { "$avg": "$scores.score" } } }
]
```

Étapes clés : `$unwind`, `$group`, `$addFields`, `$sort`, `$match`, `$lookup` (équivalent d'un JOIN)

## Correspondance SQL vers MongoDB {#sql-to-mongodb-mapping}

| SQL | MongoDB |
|-----|---------|
| SELECT | `find()` / `$project` |
| WHERE | `$match` |
| GROUP BY | `$group` |
| ORDER BY | `$sort` |
| JOIN | `$lookup` |

## Voir aussi {#see-also}
- [[hbase]] - NoSQL en colonnes dans Hadoop
- [[dwh-architecture]] - NoSQL dans le contexte de la plateforme de données
- [[data-lake-lakehouse]] - schema-on-read patterns
