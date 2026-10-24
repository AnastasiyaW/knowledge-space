---
title: "DML - INSERT, UPDATE, DELETE"
category: concepts
tags: [sql-databases, sql, insert, update, delete, truncate, dml, bulk-operations]
level: 3
source_sha256: c9427d3b0bf946cccc283c3687cc5c652aae8d41d229a02d9dd94dcc0bdbee6c
translation: machine
translated_at: '2026-10-24'
---
# DML - INSERT, UPDATE, DELETE {#dml-insert-update-delete}

Les instructions de manipulation de données (Data Manipulation Language, DML) modifient les données des tables. Comprendre leur comportement, leurs caractéristiques de performance et leurs implications sur les transactions est essentiel pour les systèmes en production.

## Points clés {#key-facts}

- INSERT, UPDATE, DELETE sont transactionnelles (elles peuvent être annulées par un rollback)
- TRUNCATE est du DDL dans la plupart des SGBDR - plus rapide que DELETE mais ne peut pas être annulée (MySQL) ou est transactionnelle (PostgreSQL)
- Un INSERT multi-lignes est nettement plus rapide que des instructions INSERT individuelles
- UPDATE réécrit la ligne entière dans PostgreSQL (MVCC) ; InnoDB modifie la ligne sur place lorsque c'est possible
- DELETE se contente de marquer les lignes pour suppression - l'espace est récupéré par VACUUM (PostgreSQL) ou par la purge en arrière-plan (InnoDB)

## Modèles {#patterns}

### INSERT {#insert}
```sql
-- Single row
INSERT INTO users (firstname, lastname, email) VALUES ('Alice', 'Smith', 'alice@example.com');

-- Multi-row (much faster than individual inserts)
INSERT INTO users (firstname, lastname) VALUES ('Bob', 'Jones'), ('Carol', 'Lee');

-- INSERT from SELECT
INSERT INTO archive_orders SELECT * FROM orders WHERE created_at < '2023-01-01';

-- INSERT with RETURNING (PostgreSQL)
INSERT INTO users (name, email) VALUES ('Dave', 'dave@example.com') RETURNING id, created_at;

-- UPSERT: INSERT ... ON CONFLICT (PostgreSQL)
INSERT INTO users (email, name) VALUES ('bob@example.com', 'Bob')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- UPSERT: INSERT ... ON DUPLICATE KEY UPDATE (MySQL)
INSERT INTO users (email, name) VALUES ('bob@example.com', 'Bob')
ON DUPLICATE KEY UPDATE name = VALUES(name);
```

### UPDATE {#update}
```sql
UPDATE users SET email = 'new@example.com' WHERE id = 1;
UPDATE users SET firstname = 'New', lastname = 'Name' WHERE id = 5;

-- Batch update with calculated values
UPDATE orders SET total = quantity * unit_price WHERE total IS NULL;

-- UPDATE from another table (PostgreSQL)
UPDATE orders o SET status = 'archived'
FROM users u WHERE o.user_id = u.id AND u.deleted = true;
```

### DELETE {#delete}
```sql
DELETE FROM users WHERE id = 1;
DELETE FROM orders WHERE created_at < '2020-01-01';

-- Delete with subquery
DELETE FROM album WHERE band_id IN (SELECT id FROM band WHERE country = 'DE');
```

### TRUNCATE {#truncate}
```sql
TRUNCATE TABLE users;              -- fast delete all rows
TRUNCATE TABLE users RESTART IDENTITY;  -- reset auto_increment (PostgreSQL)
-- MySQL: TRUNCATE always resets AUTO_INCREMENT
```

### Opérations par lots pour les grandes tables {#batch-operations-for-large-tables}
```sql
-- Avoid updating millions of rows at once - batch in chunks
UPDATE users SET status = 'inactive'
WHERE id IN (SELECT id FROM users WHERE last_login < '2023-01-01' LIMIT 10000);
-- Repeat until no rows affected, VACUUM between batches (PostgreSQL)
```

### CREATE TABLE AS SELECT {#create-table-as-select}
```sql
CREATE TABLE rock_albums AS SELECT * FROM album WHERE genre = 'rock';
```

## Pièges à éviter {#gotchas}

- TRUNCATE ne peut pas être annulée dans MySQL (c'est du DDL) ; le TRUNCATE de PostgreSQL est transactionnel
- Les grandes opérations DELETE/UPDATE peuvent provoquer une contention de verrous et du bloat - découpez-les en lots
- UPDATE dans PostgreSQL crée une nouvelle version de la ligne (tuple mort) - nécessite VACUUM pour récupérer l'espace
- Ajouter une colonne avec DEFAULT sur une grande table avant PG 11 impose une approche de mise à jour par lots
- Incluez toujours une clause WHERE dans les UPDATE/DELETE en production - une clause WHERE absente affecte toutes les lignes
- Les CASCADE de clés étrangères peuvent provoquer des suppressions massives inattendues

## Voir aussi {#see-also}

- [[ddl-schema-management]] - CREATE TABLE, ALTER TABLE, contraintes
- [[transactions-and-acid]] - encapsuler les DML dans des transactions
- [[postgresql-mvcc-vacuum]] - tuples morts issus de UPDATE/DELETE
- [[data-types-and-nulls]] - types de données pour les valeurs INSERT
