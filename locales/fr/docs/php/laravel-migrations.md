---
title: "Migrations Laravel"
category: framework
tags: [laravel, migrations, schema, database, foreign-keys, seeding]
level: 3
source_sha256: 9a2a4ae2ac4cc5f27d935c4e54b7ef27288d30179718cd62fd98d03d60574e55
translation: machine
translated_at: '2026-10-24'
---
# Migrations Laravel {#laravel-migrations}

Les migrations sont le système de contrôle de version du schéma de la base de données. Chaque migration est une classe PHP qui crée, modifie ou supprime des tables et des colonnes. Les migrations s'exécutent dans l'ordre et peuvent être annulées. Elles fonctionnent avec les modèles [[laravel-eloquent-orm]] et prennent en charge les contraintes de clés étrangères pour les relations.

## Points clés {#key-facts}

- Les migrations se trouvent dans `database/migrations/` avec des noms de fichiers horodatés
- `php artisan make:migration create_posts_table` génère une classe de migration
- `php artisan make:model Post -m` crée le modèle et la migration ensemble
- La méthode `up()` applique les modifications ; la méthode `down()` les annule
- `php artisan migrate` exécute toutes les migrations en attente
- `php artisan migrate:rollback` annule le dernier lot
- `php artisan migrate:fresh` supprime toutes les tables et réexécute toutes les migrations (destructif)
- Les clés étrangères garantissent l'intégrité référentielle entre les tables
- `$table->softDeletes()` ajoute la colonne `deleted_at` pour les suppressions logiques [[laravel-eloquent-orm]]
- Les migrations par défaut créent les tables `users`, `password_reset_tokens`, `sessions`, `cache` et `jobs`
- SQLite est la base de données par défaut dans Laravel 11 ; pour passer à MySQL/MariaDB, modifiez le fichier `.env`

## Modèles {#patterns}

### Création d'une table {#creating-a-table}

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();                          // bigint unsigned auto-increment PK
            $table->string('title');                // varchar(255)
            $table->string('slug')->unique();       // unique index
            $table->text('body');                   // text
            $table->string('image')->nullable();    // nullable varchar
            $table->boolean('is_published')->default(false);
            $table->foreignId('category_id')        // bigint unsigned
                  ->constrained()                   // foreign key to categories.id
                  ->onDelete('cascade');             // delete posts when category deleted
            $table->foreignId('user_id')
                  ->constrained();
            $table->softDeletes();                  // deleted_at timestamp
            $table->timestamps();                   // created_at, updated_at
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

### Table pivot pour une relation many-to-many {#many-to-many-pivot-table}

```php
<?php
// Pivot table for Post <-> Tag (many-to-many)
// Naming convention: alphabetical order, singular - post_tag
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('post_tag', function (Blueprint $table) {
            $table->id();
            $table->foreignId('post_id')->constrained()->onDelete('cascade');
            $table->foreignId('tag_id')->constrained()->onDelete('cascade');
            $table->timestamps();

            // Prevent duplicate assignments
            $table->unique(['post_id', 'tag_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('post_tag');
    }
};
```

### Modification de tables existantes {#modifying-existing-tables}

```php
<?php
// Add column to existing table
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->tinyInteger('role')->default(0)->after('email');
        });
    }

    public function down(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropColumn('role');
        });
    }
};
```

### Référence des types de colonnes {#column-types-reference}

```php
<?php
Schema::create('example', function (Blueprint $table) {
    // Numeric
    $table->id();                      // BIGINT UNSIGNED AUTO_INCREMENT PK
    $table->bigInteger('count');       // BIGINT
    $table->integer('quantity');        // INT
    $table->tinyInteger('role');        // TINYINT (0-255)
    $table->float('price', 8, 2);      // FLOAT
    $table->decimal('amount', 10, 2);  // DECIMAL

    // String
    $table->string('name', 100);       // VARCHAR(100)
    $table->text('body');              // TEXT
    $table->longText('content');       // LONGTEXT

    // Date/Time
    $table->timestamp('published_at'); // TIMESTAMP
    $table->date('birth_date');        // DATE
    $table->timestamps();              // created_at + updated_at

    // Boolean
    $table->boolean('is_active');      // TINYINT(1)

    // JSON
    $table->json('meta');              // JSON

    // Modifiers
    $table->string('avatar')->nullable();        // allows NULL
    $table->integer('sort')->default(0);          // default value
    $table->string('email')->unique();            // unique index
    $table->integer('position')->unsigned();      // unsigned
    $table->softDeletes();                         // deleted_at nullable timestamp
    $table->string('bio')->after('name');          // column position (MySQL)
});
```

### Commandes Artisan pour les migrations {#artisan-migration-commands}

```bash
# Generate migration
php artisan make:migration create_posts_table
php artisan make:migration add_role_to_users_table

# Run migrations
php artisan migrate              # execute pending
php artisan migrate --seed       # migrate + seed

# Rollback
php artisan migrate:rollback     # undo last batch
php artisan migrate:rollback --step=2  # undo last 2 batches
php artisan migrate:reset        # undo all migrations

# Fresh start (drops all tables)
php artisan migrate:fresh        # drop all + re-migrate
php artisan migrate:fresh --seed # drop all + re-migrate + seed

# Status
php artisan migrate:status       # show migration status
```

## Pièges courants {#gotchas}

| Symptôme | Cause | Solution |
|---------|-------|-----|
| Erreur de contrainte de clé étrangère | La table référencée n'existe pas encore | Assurez-vous que la migration de la table référencée s'exécute en premier (horodatage antérieur) |
| `Cannot delete parent row` | Des enregistrements enfants existent avec la clé étrangère | Utilisez `onDelete('cascade')` ou supprimez d'abord les enfants |
| `Column already exists` | La migration a été exécutée partiellement ou modifiée après son exécution | Exécutez `migrate:fresh` en développement ; créez une nouvelle migration en production |
| SQLite par défaut ne gère pas certaines fonctionnalités | SQLite ne prend pas en charge `ALTER TABLE DROP COLUMN` (versions anciennes) | Passez à MySQL dans `.env` pour un support complet des fonctionnalités |
| Échec de l'ajout d'une colonne à une table existante | Utilisation de `Schema::create` au lieu de `Schema::table` | Utilisez `Schema::table()` pour les modifications |
| Le rollback n'annule pas les modifications | La méthode `down()` n'est pas implémentée | Implémentez systématiquement une méthode `down()` qui inverse `up()` |

## Voir aussi {#see-also}

- [[laravel-eloquent-orm]] - modèles correspondant aux tables migrées
- [[laravel-architecture]] - configuration de la base de données dans `.env`
- https://laravel.com/docs/11.x/migrations
- https://laravel.com/docs/11.x/seeding
