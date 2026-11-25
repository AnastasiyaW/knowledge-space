---
title: "Patterns de bases de données en Go - PostgreSQL, MongoDB, Redis"
category: concepts
tags: [go, golang, postgresql, mongodb, redis, database, caching, transactions]
level: 3
source_sha256: 112314f32db3db529523fb49021810eb42bae42d637140b36243bad85af4418f
translation: machine
translated_at: '2026-10-24'
---
# Patterns de bases de données en Go - PostgreSQL, MongoDB, Redis {#go-database-patterns-postgresql-mongodb-redis}

Patterns de bases de données en Go pour la production : PostgreSQL avec pgx, MongoDB avec le driver officiel, mise en cache avec Redis, outbox transactionnel et gestion des migrations.

## Points clés {#key-facts}

- pgx est le driver PostgreSQL recommandé pour Go (Go pur, pool de connexions, requêtes préparées)
- goqu/Squirrel fournissent une construction de SQL typée qui prévient l'injection
- Goose gère les migrations avec les annotations `-- +goose Up` / `-- +goose Down`
- BSON (Binary JSON) est le format de transport de MongoDB : utilisez `bson.M`, `bson.D` ou des structs typées
- Pattern cache-aside avec Redis : interroger le cache en premier, se replier sur la base de données, puis écrire dans le cache (write-through) en cas d'absence
- L'outbox transactionnel permet de garantir la mise à jour atomique de la base et la publication du message, sans commit en deux phases

## Patterns {#patterns}

### PostgreSQL avec pgx {#postgresql-with-pgx}

```go
// Connection pool
pool, err := pgxpool.New(ctx, os.Getenv("DB_URI"))

// Transaction helper - transaction from context
func getTx(ctx context.Context) pgx.Tx {
    tx, ok := ctx.Value(txKey).(pgx.Tx)
    if !ok { return nil }
    return tx
}

// Run in transaction
func (r *Repo) RunInTransaction(ctx context.Context, fn func(ctx context.Context) error) error {
    tx, err := r.pool.Begin(ctx)
    if err != nil { return err }
    ctx = context.WithValue(ctx, txKey, tx)
    if err := fn(ctx); err != nil {
        tx.Rollback(ctx)
        return err
    }
    return tx.Commit(ctx)
}
```

### Migrations avec Goose {#migrations-with-goose}

```sql
-- +goose Up
CREATE TABLE users (...);

-- +goose Down
DROP TABLE IF EXISTS users;
```

Exécutez-les via `goose up/down/status`. Intégrez les fichiers de migration dans le binaire avec `//go:embed migrations/*.sql`.

### MongoDB avec mongo-driver {#mongodb-with-mongo-driver}

```go
client, err := mongo.Connect(ctx, options.Client().ApplyURI(mongoURI))
db := client.Database("mydb")
coll := db.Collection("notes")

result, err := coll.InsertOne(ctx, bson.M{"title": "test"})
cursor, err := coll.Find(ctx, bson.M{"title": bson.M{"$regex": "^test"}})
```

Créez explicitement les index au démarrage pour les requêtes sur lesquelles vous vous appuyez. Utilisez des index texte pour la recherche plein texte.

### Cache-aside avec Redis {#redis-cache-aside}

```go
type CacheRepository interface {
    Get(ctx context.Context, key string) (*model.Item, error)
    Set(ctx context.Context, key string, item *model.Item, ttl time.Duration) error
    Delete(ctx context.Context, key string) error
}

func (s *Service) GetItem(ctx context.Context, id string) (*model.Item, error) {
    if item, err := s.cache.Get(ctx, id); err == nil {
        return item, nil
    }
    item, err := s.repo.Get(ctx, id)
    if err != nil { return nil, err }
    s.cache.Set(ctx, id, item, 15*time.Minute)
    return item, nil
}
```

**Patterns clés** :
- Convention de nommage `{service}:{entity}:{id}`
- Définir un TTL sur toutes les entrées du cache (pour éviter les données périmées)
- `SETNX` (SET if Not eXists) pour les verrous distribués
- `DEL` ou `UNLINK` (suppression asynchrone) lors de l'invalidation

**Dégradation gracieuse** : si Redis est indisponible, le service continue de fonctionner à partir de la base de données principale.

### Outbox transactionnel {#transactional-outbox}

Problème : il faut mettre à jour la base de données et envoyer un message Kafka de manière atomique. Le commit en deux phases est peu praticable.

Solution :
1. Dans la même transaction de base de données : mettre à jour l'entité métier et insérer l'événement dans la table `outbox`
2. Un poller en arrière-plan lit les événements non envoyés de l'outbox, les publie sur Kafka et les marque comme envoyés
3. Déduplication : le consommateur utilise des clés d'idempotence pour gérer les livraisons en double

Le poller peut être une goroutine utilisant `time.Ticker`, ou être déclenché par `LISTEN/NOTIFY` de la base de données.

## Pièges courants {#gotchas}

- Le pool de connexions pgx doit être fermé à l'arrêt afin d'éviter les fuites de connexions
- Les index MongoDB doivent être créés explicitement : il n'existe aucun index automatique au-delà de `_id`
- Le `SETNX` utilisé pour les verrous doit avoir un TTL, afin d'éviter un blocage (deadlock) en cas de plantage
- L'ordre d'application des migrations Goose dépend du préfixe horodaté des noms de fichiers : gardez-les séquentiels
- `bson.M` n'est pas ordonné ; utilisez `bson.D` lorsque l'ordre compte (par exemple pour les index composés)

## Voir aussi {#see-also}

- [[microservices]] - architecture propre, injection de dépendances, organisation du projet
- [[kafka-messaging-fundamentals]] - sémantiques de livraison pour les consommateurs d'outbox
- [[sql-databases/advanced-patterns]] - fonctions de fenêtrage, sous-requêtes (PostgreSQL)
