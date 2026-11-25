---
title: "DDL et gestion du schéma"
category: concepts
tags: [sql-databases, sql, ddl, create-table, alter-table, constraints, foreign-key, primary-key]
level: 3
source_sha256: cc18eb38f4ad4bd314f1efa7131b46283180b35b42ae719ae74cb308a6149185
translation: machine
translated_at: '2026-10-24'
---
# DDL et gestion du schéma {#ddl-and-schema-management}

Le langage de définition de données (DDL, *Data Definition Language*) permet de créer, modifier et supprimer des objets de base de données. Un DDL bien conçu inclut des contraintes qui garantissent l'intégrité des données au niveau de la base.

## Points clés {#key-facts}

- Le DDL comprend CREATE, ALTER, DROP, TRUNCATE
- PRIMARY KEY = unique + NOT NULL, crée un index clustered dans InnoDB
- FOREIGN KEY garantit l'intégrité référentielle avec les actions CASCADE/RESTRICT/SET NULL
- MySQL `SERIAL` = `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`
- PostgreSQL `SERIAL` = entier à incrémentation automatique (privilégier `GENERATED ALWAYS AS IDENTITY` dans les versions récentes de PG)
- Le comportement de verrouillage de ALTER TABLE varie selon l'opération : certaines bloquent toutes les lectures, d'autres autorisent les DML concurrents

## Modèles {#patterns}

### CREATE TABLE {#create-table}
```sql
-- PostgreSQL
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    age SMALLINT CHECK (age > 0),
    created_at TIMESTAMP DEFAULT NOW()
);

-- MySQL
CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100) COMMENT 'surname',
    phone BIGINT UNSIGNED UNIQUE,
    email VARCHAR(255),
    created_at DATETIME DEFAULT NOW(),
    INDEX idx_users_name(firstname, lastname)
) DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Relations entre tables {#table-relationships}
```sql
-- One-to-Many: FK in the many-side table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2)
);

-- One-to-One: PK as FK
CREATE TABLE user_settings (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    theme VARCHAR(20) DEFAULT 'light'
);

-- Many-to-Many: junction table
CREATE TABLE group_members (
    group_id INTEGER REFERENCES groups(id),
    user_id INTEGER REFERENCES users(id),
    PRIMARY KEY (group_id, user_id)
);
```

### ALTER TABLE {#alter-table}
```sql
ALTER TABLE users ADD COLUMN birthday DATE;
ALTER TABLE users ALTER COLUMN birthday SET NOT NULL;  -- PostgreSQL
ALTER TABLE users MODIFY COLUMN birthday DATE NOT NULL; -- MySQL
ALTER TABLE users RENAME COLUMN birthday TO date_of_birth;
ALTER TABLE users DROP COLUMN date_of_birth;

-- Add foreign key
ALTER TABLE orders ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

### Actions de clé étrangère {#foreign-key-actions}
```sql
ON DELETE CASCADE    -- delete children when parent deleted
ON DELETE RESTRICT   -- prevent parent deletion if children exist (default)
ON DELETE SET NULL   -- set FK to NULL when parent deleted
ON UPDATE CASCADE    -- update FK when parent PK changes
```

### DROP {#drop}
```sql
DROP TABLE IF EXISTS temp_data;
DROP DATABASE IF EXISTS test_db;
```

### Types ENUM (MySQL) {#enum-types-mysql}
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    media_type ENUM('text', 'image', 'audio', 'video'),
    status ENUM('sent', 'delivered', 'read')
);
-- ENUM stores as integer internally (1-2 bytes). Good for fixed lists.
```

## Pièges {#gotchas}

- ALTER TABLE ADD COLUMN dans PostgreSQL acquiert un verrou ACCESS EXCLUSIVE (bloque les lectures) pour la plupart des opérations
- MySQL `utf8` ne gère que l'UTF-8 sur 3 octets (pas d'emoji) : utiliser systématiquement `utf8mb4`
- Ajouter une colonne NOT NULL sans DEFAULT échoue si la table contient des lignes
- PostgreSQL 11+ gère ADD COLUMN avec DEFAULT de manière efficace ; avant la version 11, il faut recourir à une mise à jour par lots
- MDL (*Metadata Lock*) dans MySQL : le DDL est bloqué tant que tous les DML actifs ne sont pas terminés, et les nouveaux DML se mettent en file d'attente derrière le DDL

## Voir aussi {#see-also}

- [[data-types-and-nulls]] - choisir les types de données appropriés
- [[schema-design-normalization]] - normalisation et modèles de relations
- [[index-strategies]] - index créés par les contraintes
- [[concurrency-and-locking]] - implications des opérations DDL sur les verrous
