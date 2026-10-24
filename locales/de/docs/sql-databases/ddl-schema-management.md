---
title: "DDL und Schema-Management"
category: concepts
tags: [sql-databases, sql, ddl, create-table, alter-table, constraints, foreign-key, primary-key]
level: 3
source_sha256: cc18eb38f4ad4bd314f1efa7131b46283180b35b42ae719ae74cb308a6149185
translation: machine
translated_at: '2026-10-24'
---
# DDL und Schema-Management {#ddl-and-schema-management}

Die Data Definition Language (DDL) erstellt, ändert und löscht Datenbankobjekte. Korrektes DDL umfasst Constraints, die die Datenintegrität auf Datenbankebene sicherstellen.

## Wichtige Fakten {#key-facts}

- DDL umfasst CREATE, ALTER, DROP, TRUNCATE
- PRIMARY KEY = eindeutig + NOT NULL, erzeugt einen clustered Index in InnoDB
- FOREIGN KEY erzwingt referenzielle Integrität mit den Aktionen CASCADE/RESTRICT/SET NULL
- MySQL `SERIAL` = `BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`
- PostgreSQL `SERIAL` = automatisch inkrementierender Integer (in modernem PG bevorzugt `GENERATED ALWAYS AS IDENTITY`)
- Das Sperrverhalten von ALTER TABLE hängt von der Operation ab - manche blockieren alle Lesezugriffe, andere erlauben parallele DML

## Muster {#patterns}

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

### Tabellenbeziehungen {#table-relationships}
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

### Aktionen für Fremdschlüssel {#foreign-key-actions}
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

### ENUM-Typen (MySQL) {#enum-types-mysql}
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    media_type ENUM('text', 'image', 'audio', 'video'),
    status ENUM('sent', 'delivered', 'read')
);
-- ENUM stores as integer internally (1-2 bytes). Good for fixed lists.
```

## Fallstricke {#gotchas}

- ALTER TABLE ADD COLUMN in PostgreSQL erwirbt für die meisten Operationen eine ACCESS EXCLUSIVE-Sperre (blockiert Lesezugriffe)
- MySQL `utf8` ist nur 3-Byte-UTF-8 (keine Emojis) - immer `utf8mb4` verwenden
- Das Hinzufügen einer NOT NULL-Spalte ohne DEFAULT schlägt fehl, wenn die Tabelle Zeilen enthält
- PostgreSQL 11+ behandelt ADD COLUMN mit DEFAULT effizient; ältere Versionen erfordern einen Batch-Update-Ansatz
- MDL (Metadata Lock) in MySQL: DDL wartet, bis alle aktiven DML-Vorgänge beendet sind, und neue DML-Vorgänge stellen sich hinter das DDL in die Warteschlange

## Siehe auch {#see-also}

- [[data-types-and-nulls]] - Auswahl geeigneter Datentypen
- [[schema-design-normalization]] - Normalisierung und Beziehungsmuster
- [[index-strategies]] - Indizes, die durch Constraints erzeugt werden
- [[concurrency-and-locking]] - Sperrauswirkungen von DDL-Operationen
