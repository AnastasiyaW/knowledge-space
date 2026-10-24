---
title: "Types de données et gestion de NULL"
category: concepts
tags: [sql-databases, sql, data-types, null, mysql, postgresql, varchar, integer, decimal, timestamp]
level: 4
source_sha256: bdc5b18156cbbdf865b5476b31bde5cfdf45cf89020df52f040b2110eb90d03b
translation: machine
translated_at: '2026-10-24'
---
# Types de données et gestion de NULL {#data-types-and-null-handling}

Le choix des types de données affecte le stockage, les performances et l'intégrité des données. La gestion de NULL avec une logique à trois valeurs est l'un des aspects les plus subtils de SQL.

## Types de données MySQL {#mysql-data-types}

### Numériques {#numeric}
| Type | Taille | Plage |
|------|--------|-------|
| TINYINT | 1 octet | -128 à 127 (UNSIGNED : 0 à 255) |
| SMALLINT | 2 octets | -32768 à 32767 |
| MEDIUMINT | 3 octets | -8M à 8M |
| INT | 4 octets | -2B à 2B |
| BIGINT | 8 octets | -9.2E18 à 9.2E18 |
| DECIMAL(M,D) | variable | précision exacte (pour les montants) |
| FLOAT | 4 octets | précision d'environ 7 chiffres |
| DOUBLE | 8 octets | précision d'environ 15 chiffres |

### Chaînes de caractères {#string}
| Type | Taille max | Remarques |
|------|-----------|-----------|
| CHAR(N) | 255 | longueur fixe, complétée par des espaces |
| VARCHAR(N) | 65 535 octets | longueur variable, 1 à 2 octets de surcharge |
| TEXT | 65 Ko | |
| MEDIUMTEXT | 16 Mo | |
| LONGTEXT | 4 Go | |
| ENUM | 1 à 2 octets | une valeur parmi une liste prédéfinie |

### Date et heure {#datetime}
| Type | Format | Remarques |
|------|--------|-----------|
| DATE | YYYY-MM-DD | |
| TIME | HH:MM:SS | |
| DATETIME | YYYY-MM-DD HH:MM:SS | 8 octets, sans fuseau horaire |
| TIMESTAMP | même format | 4 octets, conversion en UTC, plage 1970-2038 |
| YEAR | YYYY | 1 octet |

## Types de données PostgreSQL {#postgresql-data-types}

| Type | Remarques |
|------|-----------|
| SERIAL / BIGSERIAL | entier à incrémentation automatique (4/8 octets) |
| INTEGER, BIGINT, SMALLINT | entiers exacts |
| NUMERIC(p,s) / DECIMAL | décimal exact |
| REAL, DOUBLE PRECISION | virgule flottante |
| VARCHAR(n), TEXT | aucune différence de performance dans PG |
| CHAR(n) | longueur fixe, rarement utilisé |
| BOOLEAN | true/false/null |
| DATE, TIME, TIMESTAMP | date/heure standard |
| TIMESTAMPTZ | horodatage avec fuseau horaire (à privilégier) |
| INTERVAL | durée |
| JSON / JSONB | JSON natif (JSONB est binaire et indexable) |
| UUID | identifiant unique universel sur 128 bits |
| BYTEA | données binaires |
| INET, CIDR | adresses IP |

## Gestion de NULL - logique à trois valeurs {#null-handling-three-valued-logic}

NULL représente une donnée manquante ou inconnue. Ce n'est PAS une valeur en soi.

```sql
-- Any comparison with NULL yields UNKNOWN
NULL = NULL    -- UNKNOWN (not TRUE)
NULL != 5      -- UNKNOWN (not TRUE)
NULL > 0       -- UNKNOWN

-- Correct NULL checks
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;

-- COALESCE: first non-NULL argument
SELECT name, COALESCE(phone, 'No phone') FROM users;

-- NULLIF: returns NULL if arguments are equal
SELECT NULLIF(score, 0) FROM results;  -- avoid division by zero
```

## Points clés {#key-facts}

- Stockage de NULL : 1 bit par colonne nullable dans le bitmap de NULL de la ligne
- `COUNT(*)` compte toutes les lignes ; `COUNT(colonne)` exclut les NULL
- SUM, AVG, MIN, MAX ignorent tous les NULL
- GROUP BY regroupe tous les NULL dans un même groupe
- NULL dans les index UNIQUE : la plupart des SGBDR autorisent plusieurs NULL ; SQL Server ne le permet pas par défaut
- PostgreSQL : aucune différence de performance entre VARCHAR(n) et TEXT
- Utilisez toujours DECIMAL/NUMERIC pour les montants : FLOAT/DOUBLE introduisent des erreurs d'arrondi

## Fonctions courantes {#common-functions}

### Fonctions de chaînes {#string-functions}
```sql
CONCAT(s1, s2)              -- concatenate (both)
LENGTH(s) / CHAR_LENGTH(s)  -- byte/character length
UPPER(s) / LOWER(s)         -- case conversion
TRIM(s) / LTRIM(s) / RTRIM(s)
SUBSTRING(s, pos, len)      -- extract substring
REPLACE(s, from, to)        -- replace occurrences
LEFT(s, n) / RIGHT(s, n)   -- first/last n characters
```

### Fonctions numériques {#numeric-functions}
```sql
ROUND(n, d)  -- round to d decimal places
CEIL(n)      -- round up
FLOOR(n)     -- round down
ABS(n)       -- absolute value
MOD(n, m)    -- modulo
```

### Fonctions de date {#date-functions}
```sql
-- PostgreSQL
NOW(), CURRENT_DATE, CURRENT_TIMESTAMP
EXTRACT(YEAR FROM date_col)
AGE(timestamp1, timestamp2)         -- returns interval
date_col + INTERVAL '1 month'
TO_CHAR(date_col, 'YYYY-MM-DD')

-- MySQL
NOW(), CURDATE(), CURTIME()
YEAR(d) / MONTH(d) / DAY(d)
DATE_ADD(d, INTERVAL 1 DAY)
DATEDIFF(d1, d2)                    -- difference in days
TIMESTAMPDIFF(HOUR, d1, d2)
DATE_FORMAT(d, '%Y-%m-%d')
STR_TO_DATE(s, '%d/%m/%Y')
```

### Colonnes générées (MySQL 8.0+, PostgreSQL 12+) {#generated-columns-mysql-80-postgresql-12}

Colonnes calculées, stockées ou évaluées à la volée :
```sql
-- MySQL: STORED (on disk) or VIRTUAL (computed at read)
CREATE TABLE users (
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    full_name VARCHAR(101) GENERATED ALWAYS AS (CONCAT(first_name, ' ', last_name)) STORED
);
-- Can index STORED generated columns
CREATE INDEX idx_fullname ON users (full_name);

-- PostgreSQL 12+: only STORED
ALTER TABLE users ADD COLUMN full_name TEXT GENERATED ALWAYS AS (first_name || ' ' || last_name) STORED;
```

### Modèles pour les colonnes JSON {#json-column-patterns}

```sql
-- PostgreSQL JSONB: binary storage, indexable
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    payload JSONB NOT NULL
);

-- GIN index for containment queries
CREATE INDEX idx_payload ON events USING GIN (payload);

-- Query with operators
SELECT * FROM events WHERE payload @> '{"type": "click"}';         -- contains
SELECT * FROM events WHERE payload ->> 'user_id' = '42';           -- text extraction
SELECT * FROM events WHERE (payload -> 'meta' ->> 'score')::int > 90;  -- nested + cast

-- MySQL 8.0: JSON with generated column for indexing
ALTER TABLE events ADD COLUMN event_type VARCHAR(50)
    GENERATED ALWAYS AS (JSON_UNQUOTE(JSON_EXTRACT(payload, '$.type'))) STORED;
CREATE INDEX idx_event_type ON events (event_type);
```

### UUID comme clé primaire {#uuid-as-primary-key}

```sql
-- PostgreSQL: native UUID type
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL
);
-- Pro: no sequential guessing, safe for distributed systems
-- Con: larger than INT (16 bytes vs 4), random = fragmented B-tree inserts

-- UUIDv7 (time-sorted) available via extensions - preserves insert order
-- Better B-tree locality than UUIDv4
```

### Conversions de types inattendues {#unexpected-type-coercions}

```sql
-- MySQL silently truncates
INSERT INTO t (tinyint_col) VALUES (999);  -- stores 127 (max) with warning
-- PostgreSQL raises error for out-of-range

-- MySQL string-to-number coercion
SELECT * FROM users WHERE phone = 0;
-- Matches ALL rows where phone is a non-numeric string (coerced to 0)!
-- Always use: WHERE phone = '0'
```

## Pièges {#gotchas}

- Le `utf8` de MySQL ne couvre que 3 octets (pas les emojis) : utilisez toujours `utf8mb4`
- TIMESTAMP est limité à 2038 ; utilisez DATETIME ou TIMESTAMPTZ pour des dates pérennes
- Arithmétique en virgule flottante : `0.1 + 0.2 != 0.3` ; utilisez DECIMAL pour des comparaisons exactes
- SERIAL de PostgreSQL est déprécié au profit de `GENERATED ALWAYS AS IDENTITY`
- NULL dans NOT IN : si la sous-requête renvoie au moins un NULL, NOT IN renvoie un résultat vide
- Conversion implicite de types dans MySQL : `WHERE varchar_col = 0` correspond aux chaînes non numériques ; mettez toujours les comparaisons de chaînes entre guillemets
- JSONB dans PostgreSQL occupe environ 30 % de plus que JSON, mais il est beaucoup plus rapide pour les requêtes ; privilégiez JSONB sauf si vous avez besoin de préserver le formatage exact
- Les clés primaires UUID provoquent des divisions de pages B-tree lors des insertions aléatoires ; envisagez UUIDv7 (ordonné dans le temps) pour de meilleures performances en écriture
- Les colonnes générées ne peuvent pas référencer d'autres colonnes générées ni utiliser de sous-requêtes

## Voir aussi {#see-also}

- [[ddl-schema-management]] - CREATE TABLE avec les types de données
- [[schema-design-normalization]] - choix des types lors de la conception du schéma
- [[select-fundamentals]] - expressions CASE et champs calculés
