---
title: "Conception de schémas et normalisation"
category: concepts
tags: [sql-databases, schema-design, normalization, 1nf, 2nf, 3nf, denormalization, primary-key, foreign-key]
level: 4
source_sha256: 633a650d278ff3066116bb4c01ae224d344c1bd8afde61d6b288ea58a2df1195
translation: machine
translated_at: '2026-10-24'
---
# Conception de schémas et normalisation {#schema-design-and-normalization}

Une bonne conception de schéma équilibre l'intégrité des données (normalisation) et les performances en lecture (dénormalisation). Ce choix influence chaque requête, chaque jointure et chaque index du système.

## Formes normales {#normal-forms}

**1NF (première forme normale) :** chaque colonne contient des valeurs atomiques (pas de tableaux ni de listes). Chaque ligne est unique (possède une clé primaire). Pas de groupes répétitifs.

**2NF :** 1NF + chaque colonne non clé dépend de la totalité de la clé primaire (et non d'une partie seulement). Élimine les dépendances partielles issues des clés composites.

**3NF :** 2NF + aucune dépendance transitive (colonne non clé dépendant d'une autre colonne non clé). Exemple : si la table `city` contient `country_code`, ne stockez pas également `country_name`.

**Recommandation pratique :** normalisez jusqu'à ce que les requêtes deviennent trop complexes ou trop lentes, puis dénormalisez de manière stratégique. Les systèmes OLTP profitent de la normalisation ; les systèmes OLAP et de reporting tolèrent davantage la dénormalisation.

## Points clés {#key-facts}

- La normalisation réduit la redondance et garantit l'intégrité via les clés étrangères
- La dénormalisation échange l'intégrité contre les performances en lecture (jointures précalculées, vues matérialisées)
- Un-à-un : PK utilisée comme FK, ou FK unique
- Un-à-plusieurs : FK du côté « plusieurs »
- Plusieurs-à-plusieurs : nécessite une table de jonction avec une clé primaire composite
- Choisissez les types de données les plus petits suffisants : cela influence la taille des index, l'efficacité du cache et les I/O

## Stratégies de clé primaire {#primary-key-strategies}

| Stratégie | Avantages | Inconvénients |
|----------|------|------|
| Auto-incrément (SERIAL) | Ordonnée, compacte, idéale pour un index clustered | Divulgue le nombre d'enregistrements, inadaptée aux systèmes distribués |
| UUID v4 | Globalement unique, sans coordination | Aléatoire = mauvais pour les index (scissions de pages) |
| UUID v7 / ULID | Ordonnée dans le temps et unique, adaptée au distribué | Plus large qu'un entier (16 octets) |

## Patrons {#patterns}

### Schéma applicatif typique (clone de Telegram) {#typical-application-schema-telegram-clone}
```sql
-- Users with settings (1:1)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone BIGINT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_settings (
    user_id BIGINT PRIMARY KEY REFERENCES users(id),
    theme VARCHAR(20) DEFAULT 'light',
    language VARCHAR(10) DEFAULT 'en'
);

-- Messages with self-referencing reply chain
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    sender_id BIGINT NOT NULL REFERENCES users(id),
    receiver_id BIGINT NOT NULL REFERENCES users(id),
    reply_to_id BIGINT REFERENCES messages(id),
    body TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Groups with members (M:M)
CREATE TABLE groups (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    owner_id BIGINT REFERENCES users(id)
);

CREATE TABLE group_members (
    group_id BIGINT REFERENCES groups(id),
    user_id BIGINT REFERENCES users(id),
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (group_id, user_id)
);
```

### Patrons de dénormalisation {#denormalization-patterns}
```sql
-- Materialized count: avoid COUNT(*) on large tables
ALTER TABLE users ADD COLUMN order_count INTEGER DEFAULT 0;
-- Update via trigger or application logic

-- Pre-computed join: store derived data
ALTER TABLE orders ADD COLUMN user_name VARCHAR(100);
-- Trade-off: faster reads, complex update logic
```

### Anti-patron de conception : imbriquer des listes {#design-anti-pattern-embedding-lists}
```sql
-- BAD: storing comma-separated values
CREATE TABLE users (id INT, hobbies TEXT);  -- hobbies = 'chess,reading,hiking'

-- GOOD: separate table for many-to-many
CREATE TABLE hobbies (id SERIAL PRIMARY KEY, name VARCHAR(50));
CREATE TABLE user_hobbies (user_id INT REFERENCES users(id), hobby_id INT REFERENCES hobbies(id));
```

## Pièges à éviter {#gotchas}

- Une normalisation excessive entraîne un nombre excessif de JOIN : dénormalisez stratégiquement les chemins critiques
- Les valeurs ENUM sont difficiles à modifier par la suite ; envisagez plutôt une table de référence (lookup)
- L'ordre des colonnes dans PostgreSQL affecte l'alignement en mémoire : regroupez les types de même taille
- Les clés primaires auto-incrémentées divulguent des informations métier (nombre de commandes, taux de croissance)
- L'absence d'index sur les colonnes FK est une cause fréquente de dégradation des performances

## Voir aussi {#see-also}

- [[ddl-schema-management]] - syntaxe de CREATE TABLE et contraintes
- [[data-types-and-nulls]] - choix des types de données appropriés
- [[partitioning-and-sharding]] - mise à l'échelle des grosses tables
- [[btree-and-index-internals]] - impact des UUID sur les performances des index
