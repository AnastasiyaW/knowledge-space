---
title: "PostgreSQL pour l'ingénierie des données"
category: tools
tags: [data-engineering, postgresql, rdbms, transactions, plpgsql, optimization]
level: 3
source_sha256: 8a207e8d3c96b520062a6717dbad9b206c344f0cc9aa64445a9003df0ac21e70
translation: machine
translated_at: '2026-10-24'
---
# PostgreSQL pour l'ingénierie des données {#postgresql-for-data-engineering}

PostgreSQL est le SGBDR le plus courant en ingénierie des données, utilisé comme metastore d'Airflow, comme système source et parfois comme base analytique. Comprendre son architecture, ses transactions et ses extensions procédurales est indispensable.

## Architecture {#architecture}

- **Modèle client-serveur :** le postmaster gère les processus backend, un par connexion client
- **Pooling de connexions :** pgBouncer ou Odyssey pour un grand nombre de connexions
- **Stockage physique :** données dans des pages de 8 Ko, mises en cache dans shared_buffers
- **Logique :** Serveur -> Base de données -> Schéma -> Objets (tables, index, vues, fonctions)

## Transactions (ACID) {#transactions-acid}

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE name = 'Alice';
SAVEPOINT my_savepoint;
UPDATE accounts SET balance = balance + 100 WHERE name = 'Bob';
ROLLBACK TO my_savepoint;
UPDATE accounts SET balance = balance + 100 WHERE name = 'Wally';
COMMIT;
```

### Niveaux d'isolation {#isolation-levels}

| Niveau | Lecture sale | Lecture non répétable | Fantôme |
|-------|-----------|---------------|---------|
| Read Committed (par défaut) | Non | Possible | Possible |
| Repeatable Read | Non | Non | Non* |
| Serializable | Non | Non | Non |

*Le Repeatable Read de PostgreSQL empêche aussi les fantômes (plus strict que le standard).

### MVCC {#mvcc}
Chaque transaction travaille avec un instantané des données (les identifiants de transaction définissent la visibilité).
- **Read Committed :** instantané par instruction
- **Repeatable Read :** instantané par transaction

## PL/pgSQL {#plpgsql}

### Fonctions et procédures {#functions-vs-procedures}

| Caractéristique | Fonction | Procédure |
|---------|----------|-----------|
| Contrôle de transaction | Non | Oui |
| Utilisation dans un SELECT | Oui | Non |
| Syntaxe d'appel | `SELECT func()` | `CALL proc()` |

### Triggers {#triggers}

```sql
CREATE OR REPLACE FUNCTION log_changes() RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO audit (id, op) VALUES (NEW.id, 'INSERT');
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit (id, op) VALUES (NEW.id, 'UPDATE');
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO audit (id, op) VALUES (OLD.id, 'DELETE');
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_changes
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION log_changes();
```

## MERGE (PostgreSQL 15+) {#merge-postgresql-15}

```sql
MERGE INTO products AS p
USING product_updates AS u ON p.id = u.id
WHEN MATCHED THEN UPDATE SET name = u.name, price = u.price
WHEN NOT MATCHED THEN INSERT (id, name, price) VALUES (u.id, u.name, u.price)
WHEN NOT MATCHED BY SOURCE THEN DELETE;
```

Pour PostgreSQL < 15 : `INSERT ... ON CONFLICT DO UPDATE`.

## Opérations en masse {#bulk-operations}

```sql
COPY table_name FROM '/path/to/file.csv';
COPY (SELECT * FROM t) TO '/path/to/output.csv';
TRUNCATE TABLE employees;  -- fast clear (vs row-by-row DELETE)
```

## Méthodes physiques de JOIN {#physical-join-methods}

| Méthode | Complexité | Prérequis |
|--------|-----------|-------------|
| **Nested Loops** | O(M * N) | Universelle |
| **Merge Join** | O(M + N) trié | Égalité, données triées |
| **Hash Join** | O(N) | Égalité, mémoire pour la table de hachage |

## Optimisation des requêtes {#query-optimization}

```sql
EXPLAIN ANALYZE SELECT * FROM bookings;
-- Shows: plan type, cost, actual time, rows, loops
```

### Types de nœuds de plan {#plan-node-types}
- Seq Scan, Index Scan, Index Only Scan
- Nested Loop / Merge Join / Hash Join
- HashAggregate, Sort, Gather (parallèle)

### Statistiques {#statistics}
```sql
SELECT reltuples, relpages FROM pg_class WHERE relname = 'bookings';
ANALYZE table_name;  -- update statistics
```

## Pièges courants {#gotchas}
- La chaîne vide `''` n'est PAS NULL dans PostgreSQL (contrairement à Oracle)
- DateStyle affecte l'analyse des dates : utilisez toujours ISO 8601 (`YYYY-MM-DD`)
- Les tableaux sont indexés à partir de 1 dans PostgreSQL
- Ne jamais utiliser les types `float` pour les montants (erreurs d'arrondi)
- UPDATE avec FROM : en cas de correspondances multiples, la ligne utilisée est imprévisible
- Les suppressions en cascade sont implicites : préférez les suppressions explicites
- En DWH, les contraintes sont souvent désactivées pour accélérer les chargements en masse

## Voir aussi {#see-also}
- [[sql-for-de]] - patterns SQL et fonctions de fenêtrage
- [[data-modeling]] - normalisation et conception de schémas
- [[greenplum-mpp]] - MPP basé sur PostgreSQL
- [[docker-for-de]] - exécuter PostgreSQL dans Docker
