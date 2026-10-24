---
title: "Concurrence et verrouillage"
category: concepts
tags: [sql-databases, locks, deadlock, advisory-lock, pessimistic, optimistic, two-phase-locking, postgresql, mysql]
level: 3
source_sha256: c80e5fad992fb838bbe5eeb36cd88c7e0d8aee996ce4e8c863be0f6b502f3283
translation: machine
translated_at: '2026-10-24'
---
# Concurrence et verrouillage {#concurrency-and-locking}

Le verrouillage des bases de données contrôle l'accès concurrent aux données partagées. Comprendre les types de verrous, leur granularité et les schémas d'interblocage est indispensable pour construire des applications concurrentes fiables.

## Types de verrous de table PostgreSQL (8 niveaux) {#postgresql-table-lock-types-8-levels}

Du plus léger au plus lourd :

| Verrou | Acquis par | Bloque |
|--------|-------------|--------|
| ACCESS SHARE | SELECT | Uniquement ACCESS EXCLUSIVE |
| ROW SHARE | SELECT FOR UPDATE/SHARE | ACCESS EXCLUSIVE, EXCLUSIVE |
| ROW EXCLUSIVE | INSERT, UPDATE, DELETE | SHARE et supérieurs |
| SHARE UPDATE EXCLUSIVE | VACUUM, ANALYZE, CREATE INDEX CONCURRENTLY | Lui-même et supérieurs |
| SHARE | CREATE INDEX (non concurrent) | ROW EXCLUSIVE et supérieurs (PAS lui-même) |
| SHARE ROW EXCLUSIVE | CREATE TRIGGER, ALTER TABLE ADD FK | Lui-même et supérieurs |
| EXCLUSIVE | REFRESH MATERIALIZED VIEW CONCURRENTLY | Tout sauf ACCESS SHARE |
| ACCESS EXCLUSIVE | DROP TABLE, TRUNCATE, VACUUM FULL, la plupart des ALTER TABLE | Tout, y compris SELECT |

Point clé : différentes opérations ALTER TABLE acquièrent différents niveaux de verrou.

## Types de verrous de ligne PostgreSQL {#postgresql-row-lock-types}

| Verrou | Acquis par | Bloque |
|--------|-------------|--------|
| FOR KEY SHARE | SELECT FOR KEY SHARE | Uniquement FOR UPDATE |
| FOR SHARE | SELECT FOR SHARE | UPDATE, DELETE, FOR UPDATE |
| FOR NO KEY UPDATE | UPDATE sur des colonnes non clés | FOR SHARE et supérieurs |
| FOR UPDATE | DELETE, UPDATE sur des colonnes clés | Tout |

Implémentation : PostgreSQL stocke les verrous de ligne dans l'en-tête du tuple (champ `xmax`), et non en mémoire. Cela économise de la mémoire, mais SELECT FOR UPDATE peut rendre des pages sales.

## Types de verrous MySQL InnoDB {#mysql-innodb-lock-types}

- **Partagé (S) :** `SELECT ... FOR SHARE`. Plusieurs détenteurs autorisés.
- **Exclusif (X) :** `SELECT ... FOR UPDATE`, INSERT, UPDATE, DELETE. Un seul détenteur.
- **Verrous d'intention (IS/IX) :** signaux au niveau de la table indiquant qu'une transaction a l'intention de verrouiller des lignes.
- **Verrou de gap :** verrouille l'intervalle entre les enregistrements d'index. Empêche les lectures fantômes en REPEATABLE READ.
- **Verrou next-key :** verrou de gap + verrou d'enregistrement. Par défaut en RR dans InnoDB.
- **Verrou d'intention d'insertion :** autorise des insertions concurrentes à différentes positions au sein d'un même gap.
- **MDL (Metadata Lock) :** le DDL acquiert un MDL exclusif, bloqué jusqu'à la fin de tous les DML actifs.

## Motifs {#patterns}

### Prévention des doubles réservations {#double-booking-prevention}
```sql
-- Pessimistic: SELECT FOR UPDATE
BEGIN;
SELECT * FROM seats WHERE seat_id = 42 AND status = 'available' FOR UPDATE;
UPDATE seats SET status = 'booked', user_id = 123 WHERE seat_id = 42;
COMMIT;

-- Optimistic: unique constraint
ALTER TABLE bookings ADD CONSTRAINT uq_seat_event UNIQUE (seat_id, event_id);
-- Second booking attempt fails with constraint violation
```

### Verrous consultatifs (PostgreSQL) {#advisory-locks-postgresql}
```sql
-- Session-level: held until explicit release or session end
SELECT pg_advisory_lock(42);      -- lock ID 42
-- Do work across multiple transactions...
SELECT pg_advisory_unlock(42);

-- Transaction-level: released on COMMIT/ROLLBACK
SELECT pg_advisory_xact_lock(42);
```

Les verrous consultatifs ne bloquent pas les modifications de lignes et peuvent couvrir plusieurs transactions. Ils sont utiles pour le verrouillage au niveau applicatif sans lignes réelles.

### Motif d'interblocage {#deadlock-pattern}
```sql
-- Session 1:                    -- Session 2:
BEGIN;                            BEGIN;
UPDATE t SET v=1 WHERE id=1;     UPDATE t SET v=2 WHERE id=2;
-- holds lock on id=1             -- holds lock on id=2
UPDATE t SET v=1 WHERE id=2;     UPDATE t SET v=2 WHERE id=1;
-- waits for id=2                 -- waits for id=1 -> DEADLOCK
```

### Verrouillage à deux phases (2PL) {#two-phase-locking-2pl}

Phase de croissance (acquisition des verrous) puis phase de décroissance (libération des verrous). Le 2PL strict conserve tous les verrous jusqu'au COMMIT/ROLLBACK. Il garantit la sérialisabilité en conflit.

## Faits clés {#key-facts}

- PostgreSQL : VACUUM acquiert SHARE UPDATE EXCLUSIVE (autorise les lectures et écritures concurrentes)
- VACUUM FULL acquiert ACCESS EXCLUSIVE (bloque tout, y compris SELECT)
- Les verrous faibles utilisent une optimisation « fast-path » (16 emplacements par backend) ; les tables fortement partitionnées peuvent dépasser cette limite
- PostgreSQL détecte automatiquement les interblocages et annule une transaction (la victime)
- Même un DML ne modifiant aucune ligne acquiert un verrou ROW EXCLUSIVE sur la table
- Cascade MDL dans MySQL : ALTER TABLE attend un SELECT long, et les nouveaux SELECT se mettent en file derrière l'ALTER

## Pièges courants {#gotchas}

- `SELECT FOR SHARE` pris par deux transactions, puis tentative d'UPDATE par l'une d'elles = interblocage
- Les verrous consultatifs couvrent plusieurs transactions en mode session : des fuites sont possibles s'ils ne sont pas explicitement libérés
- Le pooling en mode transaction de PgBouncer libère de façon inattendue les verrous consultatifs de session
- Les tuples insérés n'ont pas besoin de verrous de ligne dans PostgreSQL : ils sont invisibles pour les autres transactions
- La détection d'interblocages ajoute un surcoût : concevez un ordre de verrouillage qui prévient les interblocages

## Voir aussi {#see-also}

- [[transactions-and-acid]] - niveaux d'isolation et phénomènes de lecture
- [[postgresql-mvcc-vacuum]] - MVCC comme alternative au verrouillage
- [[mysql-innodb-engine]] - fonctionnement interne du verrouillage InnoDB
- [[connection-pooling]] - comportement des verrous avec les poolers de connexions
