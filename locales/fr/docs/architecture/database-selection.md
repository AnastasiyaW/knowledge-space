---
title: "Sélection et conception de bases de données"
category: reference
tags: [database, postgresql, redis, mongodb, cassandra, nosql, sql, orm]
level: 4
source_sha256: 54234710ca31cc281a41f38b2567d2f06c26e0a0f3ba10b62d2e04523fbf189b
translation: machine
translated_at: '2026-10-24'
---
# Sélection et conception de bases de données {#database-selection-and-design}

Choisir la bonne base de données est une décision d'architecture aux conséquences durables. Il faut tenir compte du type de données, des exigences de cohérence, des besoins de performance, des compétences de l'équipe et du budget.

## OLTP vs OLAP {#oltp-vs-olap}

| Aspect | OLTP | OLAP |
|--------|------|------|
| Objectif | Transactions en temps réel | Requêtes analytiques, reporting |
| Transactions | Nombreuses et courtes | Peu nombreuses et longues |
| Exemples | PostgreSQL, MySQL, Oracle | ClickHouse, BigQuery, Greenplum |
| Cas d'usage | Données opérationnelles des services | DWH, analytique, rapports |

## Sélection selon le type de données {#selection-by-data-type}

| Type de données | Type de BD | Exemple | Idéal pour |
|-----------------|------------|---------|------------|
| Structurées | Relationnelle | PostgreSQL | Commandes, utilisateurs, transactions |
| Documents/JSON | Documentaire | MongoDB | Données hiérarchiques, semi-structurées |
| Volume élevé, changements fréquents | Clé-valeur | Redis | Sessions, mise en cache |
| Analytique/rapports | Colonnaire | ClickHouse, Cassandra | Agrégations sur des To/Po |
| Binaires/gros fichiers | Stockage objet | S3, MinIO | Images, vidéos, audio |
| Relations | Graphe | Neo4j | Réseaux sociaux, recommandations |

## Arbre de décision {#decision-tree}

```rust
Need ACID transactions?
  Yes -> PostgreSQL (or MySQL)
Need flexible schema?
  Yes -> MongoDB
Need high write throughput (>500K TPS)?
  Yes -> Cassandra / ScyllaDB
Need sub-ms latency for simple keys?
  Yes -> Redis
Need full-text search?
  Yes -> Elasticsearch
Need relationship traversal?
  Yes -> Neo4j
Need analytical aggregations?
  Yes -> ClickHouse / BigQuery
```

## Focus sur les bases de données {#database-deep-dives}

### PostgreSQL {#postgresql}
Débit d'écriture élevé, lectures rapides, support JSON/XML. Nécessite une conception de schéma rigoureuse.
- À utiliser pour : traitement des commandes, données critiques nécessitant ACID, charges OLTP
- Extensions OLAP : GreenPlum, ClickHouse pour la couche analytique

### Redis {#redis}
En mémoire, clé-valeur. Lectures et écritures extrêmement rapides. TTL intégré.
- À utiliser pour : sessions, mise en cache, limitation de débit (rate limiting), classements
- Mise en garde : consommation de ressources importante pour les grands volumes (tout est en RAM)

### MongoDB / CouchDB {#mongodb-couchdb}
Schéma flexible (documents JSON). Développement rapide.
- À utiliser pour : données hiérarchiques, prototypage rapide, évolution du schéma
- Mise en garde : peu adapté aux transactions complexes

### Cassandra {#cassandra}
Familles de colonnes, échelle de l'ordre du To/Po. Excellente scalabilité horizontale.
- À utiliser pour : analytique, séries temporelles, données IoT
- Mise en garde : déconseillé pour les écritures fréquentes ou les transactions complexes

### S3 / MinIO {#s3-minio}
Stockage objet. Évolutif, contrôle d'accès granulaire.
- À utiliser pour : fichiers non structurés (images, vidéos, documents)
- Mise en garde : peut devenir coûteux à grande échelle

## Principes fondamentaux de conception {#database-design-fundamentals}

### Normalisation {#normalization}
- **1NF** - valeurs atomiques, pas de groupes répétitifs
- **2NF** - tous les attributs non clés dépendent de la clé primaire complète
- **3NF** - aucune dépendance transitive

### Clés {#keys}
- **Clé primaire** - identifiant unique de la ligne
- **Clé étrangère** - référence à la PK d'une autre table
- **Clé composite** - plusieurs colonnes formant la PK
- **Surrogate** - générée automatiquement (sans signification métier)
- **Naturelle** - porteuse de sens métier (e-mail, numéro de sécurité sociale)

### Index {#indexes}
| Type | Idéal pour |
|------|------------|
| B-Tree | Requêtes par intervalle, égalité (par défaut) |
| Hash | Recherches d'égalité rapides |
| GIN | Recherche plein texte, JSONB |
| Partiel | Sous-ensemble de lignes (clause WHERE) |

### Transactions ACID {#acid-transactions}
- **Atomicité** - tout ou rien
- **Cohérence** - passage d'un état valide à un autre état valide
- **Isolation** - les transactions concurrentes ne s'interfèrent pas
- **Durabilité** - les données validées survivent aux pannes

### Niveaux d'isolation {#isolation-levels}
| Niveau | Lectures sales | Lectures non répétables | Fantômes |
|--------|----------------|-------------------------|----------|
| Read Uncommitted | Oui | Oui | Oui |
| Read Committed | Non | Oui | Oui |
| Repeatable Read | Non | Non | Oui |
| Serializable | Non | Non | Non |

Valeur par défaut de PostgreSQL : Read Committed.

## Considérations sur les ORM {#orm-considerations}

**Quand l'utiliser :** développement rapide, CRUD standard, réduction du code répétitif. Une migration a ramené 1500 classes de SQL manuel à un code cinq fois plus court.

**Quand ne pas l'utiliser :** rapports (SQL brut), chemins critiques à forte charge, requêtes analytiques complexes.

**Approche hybride :** ORM pour la logique métier, SQL brut pour les rapports. Outils de migration : Flyway, Liquibase (Java), migrations Entity Framework (.NET).

## Optimisation des requêtes {#query-optimization}

1. **EXPLAIN ANALYZE** - comprendre le plan d'exécution
2. **Utilisation des index** - s'assurer que les requêtes utilisent les index
3. **Éviter SELECT \*** - ne récupérer que les colonnes nécessaires
4. **Optimisation des JOIN** - ordre adéquat, index sur les colonnes de jointure
5. **Pooling de connexions** - PgBouncer pour PostgreSQL
6. **Partitionnement** - découper les grandes tables (par intervalle, liste ou hash)
7. **Vues matérialisées** - résultats précalculés pour les rapports complexes

## Modèles de montée en charge {#scaling-patterns}

- **Réplicas en lecture** - répartir la charge de lecture
- **Sharding** - répartir les données entre plusieurs BD selon une clé
- **Partitionnement** - découper les tables au sein d'une même BD
- **Stockage chaud/froid** - données récentes sur SSD, données anciennes sur stockage économique

## Pièges à éviter {#gotchas}

- **Base de données partagée entre microservices** : anti-pattern, couplage fort et problèmes de coordination des schémas
- **NoSQL prématuré** : commencer par PostgreSQL, sauf si des exigences NoSQL claires existent
- **Redis comme magasin principal** sans configuration de persistance : perte de données au redémarrage
- **Problème de requêtes N+1** : le chargement paresseux des ORM génère N+1 requêtes dans les boucles. Utiliser le chargement anticipé (eager loading) ou la récupération par lots
- **Migration de schéma sans plan de retour arrière** : chaque migration doit avoir un script de rollback correspondant
- **Confusion entre sharding et réplication** : le sharding répartit les données entre machines, la réplication copie les mêmes données sur plusieurs machines

## Voir aussi {#see-also}

- [[solution-architecture-process]] - Sélection de bases de données dans le contexte de l'architecture
- [[caching-and-performance]] - Redis comme cache, pooling de connexions
- [[distributed-systems-fundamentals]] - Sharding, réplication, CAP
- [[bigdata-ml-architecture]] - OLAP, entrepôts de données
- [[devops-cicd]] - Migrations de bases de données sans interruption de service
