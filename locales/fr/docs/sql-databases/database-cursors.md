---
title: "Curseurs de base de données"
category: concepts
tags: [sql-databases, cursor, server-side-cursor, client-side-cursor, batch-processing, postgresql, psycopg2]
level: 3
source_sha256: 9e3e69fd89c79c4f0066f19c6ccbaeec6a01ca759ad6f600dfe2274f9776f8c2
translation: machine
translated_at: '2026-10-24'
---
# Curseurs de base de données {#database-cursors}

Un curseur est un pointeur vers un ensemble de résultats qui permet un traitement ligne par ligne ou par lots, au lieu de récupérer tous les résultats en une seule fois. Le choix entre curseurs côté client et curseurs côté serveur a des implications importantes sur les performances.

## Curseurs côté client (par défaut) {#client-side-cursors-default}

La base de données exécute la requête et transfère TOUS les résultats vers le client. Le client conserve l'ensemble des résultats en mémoire et itère localement.

```python
# Default psycopg2 cursor (client-side)
cur = conn.cursor()
cur.execute("SELECT * FROM large_table")
rows = cur.fetchall()  # ALL rows loaded into Python memory
```

**Avantages :** libère les ressources du serveur après le transfert, itération locale rapide.
**Inconvénients :** bande passante réseau élevée (ensemble complet des résultats), pression sur la mémoire du client, exécution initiale lente.

## Curseurs côté serveur {#server-side-cursors}

La base de données conserve les résultats sur le serveur. Le client les récupère par petits lots via des requêtes FETCH.

```python
# psycopg2 named cursor (server-side)
cur = conn.cursor(name='server_cursor')
cur.execute("SELECT * FROM large_table")
batch = cur.fetchmany(1000)  # fetch 1000 rows at a time
```

```sql
-- SQL-level cursor
DECLARE my_cursor CURSOR FOR SELECT * FROM large_table;
FETCH 100 FROM my_cursor;
CLOSE my_cursor;
```

**Avantages :** ~3 ms d'exécution initiale, mémoire client minimale, faible réseau par lot.
**Inconvénients :** chaque FETCH = un aller-retour réseau, le serveur conserve l'état en mémoire, risque de fuite de curseurs.

## Quand utiliser l'un ou l'autre {#when-to-use-which}

| Scénario | Recommandation |
|----------|---------------|
| Petit ensemble de résultats, besoin de toutes les données | Côté client |
| Grand ensemble de résultats, besoin d'une partie seulement | Côté serveur |
| Traitement en flux ou en pipeline | Côté serveur |
| Opérations CRUD simples | Côté client (par défaut) |

## Points clés {#key-facts}

- Les curseurs côté serveur maintiennent les ressources du serveur allouées jusqu'à leur fermeture explicite
- Fermez/désallouez toujours les curseurs explicitement pour éviter les fuites
- Évitez les curseurs lorsque des opérations ensemblistes suffisent (UPDATE...SET, INSERT...SELECT)
- Avec PgBouncer en mode transaction, les curseurs côté serveur doivent être ouverts et fermés dans la même transaction
- Les curseurs côté serveur de PostgreSQL nécessitent une transaction active (BEGIN/COMMIT)

## Pièges {#gotchas}

- Les fuites de curseurs avec de nombreux clients simultanés peuvent épuiser la mémoire du serveur
- Le pooling de connexions complique les curseurs côté serveur : l'état du curseur est lié à la connexion
- Les opérations ensemblistes (JOIN, UPDATE) sont presque toujours plus rapides que le traitement ligne par ligne par curseur
- Les curseurs nommés dans psycopg2 créent automatiquement des curseurs côté serveur, et `itersize` contrôle la taille des lots

## Voir aussi {#see-also}

- [[connection-pooling]] - comportement des curseurs avec les connexions poolées
- [[query-optimization-explain]] - privilégier les opérations ensemblistes aux curseurs
- [[select-fundamentals]] - LIMIT/OFFSET comme alternative aux curseurs
