---
title: "Transactions distribuées et patterns"
category: concepts
tags: [sql-databases, distributed-transactions, two-phase-commit, saga, eventual-consistency, double-booking]
level: 4
source_sha256: 75178f1623ae7c5692f1feff79fb88a07a60ce833a78c9264fe51f976f4f81da
translation: machine
translated_at: '2026-10-24'
---
# Transactions distribuées et patterns {#distributed-transactions-and-patterns}

Lorsque les données s'étendent sur plusieurs bases de données ou services, le maintien de la cohérence exige des patterns qui vont au-delà de l'ACID d'une base unique. Les deux approches principales, 2PC et Saga, arbitrent entre garanties de cohérence et disponibilité.

## Two-Phase Commit (2PC) {#two-phase-commit-2pc}

Le coordinateur demande à tous les participants de se préparer (phase 1), puis de valider (phase 2). Si un participant vote non, tous annulent.

**Problème :** une défaillance du coordinateur pendant la phase de validation laisse les participants dans un état incertain (protocole bloquant). Protocole synchrone, latence élevée.

**Cas d'usage :** lorsqu'une forte cohérence est requise entre plusieurs bases de données et que la latence est acceptable.

## Pattern Saga {#saga-pattern}

Séquence de transactions locales avec des transactions de compensation pour le rollback. Chaque étape valide indépendamment.

```php
Step 1: Reserve inventory  -> Compensate: Release inventory
Step 2: Charge payment     -> Compensate: Refund payment
Step 3: Ship order         -> Compensate: Cancel shipment
```

Si l'étape N échoue, exécuter les transactions de compensation des étapes N-1 à 1.

**Types :** chorégraphie (événements entre services) ou orchestration (coordinateur central).

**Avantages :** meilleure disponibilité que le 2PC, pas de blocage. **Inconvénients :** logique de compensation complexe, cohérence à terme.

## Prévention du double-booking {#double-booking-prevention}

### Pessimiste (SELECT FOR UPDATE) {#pessimistic-select-for-update}
```sql
BEGIN;
SELECT * FROM seats WHERE id = 42 AND status = 'available' FOR UPDATE;
-- Row locked. If available:
UPDATE seats SET status = 'booked', user_id = 123 WHERE id = 42;
COMMIT;
```

### Optimiste (contrainte d'unicité) {#optimistic-unique-constraint}
```sql
ALTER TABLE bookings ADD CONSTRAINT uq_seat_event UNIQUE (seat_id, event_id);
-- Second booking fails with constraint violation - app catches and retries
```

### Verrous consultatifs {#advisory-locks}
```sql
SELECT pg_advisory_lock(42);  -- lock seat 42
-- Check and book...
SELECT pg_advisory_unlock(42);
```

### Isolation sérialisable {#serializable-isolation}
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Database detects conflicts automatically - simplest code, higher abort rate
```

## Tables de hachage dans les bases de données {#hash-tables-in-databases}

Utilisées en interne pour : les hash joins (construction sur la plus petite table, sondage avec la plus grande), l'agrégation par hachage (GROUP BY), le partitionnement par hachage, les index de hachage.

Stratégies de collision : chaînage (listes chaînées), adressage ouvert (sondage linéaire ou quadratique), cuckoo hashing (deux fonctions de hachage, O(1) garanti).

## Points clés {#key-facts}

- Le 2PC est un protocole bloquant : la défaillance d'un participant pendant la validation bloque tous les autres
- Saga assure une cohérence à terme, et non une cohérence forte
- Les transactions de compensation doivent être idempotentes (sûres à rejouer)
- `SELECT FOR UPDATE` est la solution la plus simple contre le double-booking dans un scénario à base unique
- L'isolation sérialisable dans PostgreSQL utilise SSI (Serializable Snapshot Isolation), et non une exécution réellement sérielle

## Pièges courants {#gotchas}

- Le coordinateur 2PC est un point de défaillance unique : il requiert sa propre haute disponibilité
- La logique de compensation d'une saga peut être aussi complexe que la logique métier d'origine
- La cohérence à terme signifie que les utilisateurs peuvent voir des données obsolètes temporairement
- `SELECT FOR UPDATE` bloque les accès concurrents : forte contention = goulot d'étranglement
- Les verrous consultatifs dans PgBouncer en mode transaction sont libérés lorsque la connexion retourne au pool

## Voir aussi {#see-also}

- [[transactions-and-acid]] - garanties ACID d'une base unique
- [[concurrency-and-locking]] - types de verrous pour prévenir les conflits
- [[distributed-databases]] - bases de données disposant de transactions distribuées intégrées
- [[partitioning-and-sharding]] - difficultés des transactions inter-shards
