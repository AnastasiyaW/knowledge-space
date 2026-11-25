---
title: "Laravel-Migrationen"
category: framework
tags: [laravel, migrations, schema, database, foreign-keys, seeding]
level: 3
source_sha256: 9a2a4ae2ac4cc5f27d935c4e54b7ef27288d30179718cd62fd98d03d60574e55
translation: machine
translated_at: '2026-10-24'
---
# Laravel-Migrationen {#laravel-migrations}

Migrationen sind die Versionskontrolle für das Datenbankschema. Jede Migration ist eine PHP-Klasse, die Tabellen und Spalten erstellt, ändert oder löscht. Migrationen werden in der Reihenfolge ihrer Zeitstempel ausgeführt und können zurückgerollt werden. Sie arbeiten mit [[laravel-eloquent-orm]]-Modellen und unterstützen Fremdschlüssel-Constraints für Beziehungen.

## Wichtige Fakten {#key-facts}

- Migrationen liegen in `database/migrations/` mit zeitgestempelten Dateinamen
- `php artisan make:migration create_posts_table` erzeugt eine Migrationsklasse
- `php artisan make:model Post -m` erstellt Modell und Migration gemeinsam
- Die Methode `up()` wendet Änderungen an; die Methode `down()` macht sie rückgängig
- `php artisan migrate` führt alle ausstehenden Migrationen aus
- `php artisan migrate:rollback` macht den letzten Batch rückgängig
- `php artisan migrate:fresh` löscht alle Tabellen und führt alle Migrationen erneut aus (destruktiv)
- Fremdschlüssel erzwingen die referenzielle Integrität zwischen Tabellen
- `$table->softDeletes()` fügt die Spalte `deleted_at` für [[laravel-eloquent-orm]]-Soft-Deletes hinzu
- Die Standardmigrationen erstellen die Tabellen `users`, `password_reset_tokens`, `sessions`, `cache`, `jobs`
- SQLite ist die Standarddatenbank in Laravel 11; der Wechsel zu MySQL/MariaDB erfolgt über `.env`

## Muster {#patterns}

### Eine Tabelle erstellen {#creating-a-table}

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

### Many-to-many-Pivot-Tabelle {#many-to-many-pivot-table}

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

### Bestehende Tabellen ändern {#modifying-existing-tables}

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

### Referenz der Spaltentypen {#column-types-reference}

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

### Artisan-Befehle für Migrationen {#artisan-migration-commands}

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

## Fallstricke {#gotchas}

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| Fehler bei Fremdschlüssel-Constraint | Referenzierte Tabelle existiert noch nicht | Sicherstellen, dass die Migration der referenzierten Tabelle zuerst läuft (früherer Zeitstempel) |
| `Cannot delete parent row` | Kinddatensätze mit Fremdschlüssel existieren | `onDelete('cascade')` verwenden oder zuerst die Kinddatensätze löschen |
| `Column already exists` | Migration wurde teilweise ausgeführt oder nach dem Ausführen geändert | In der Entwicklung `migrate:fresh` ausführen; in der Produktion eine neue Migration erstellen |
| Standard-SQLite kann einige Funktionen nicht verarbeiten | SQLite unterstützt `ALTER TABLE DROP COLUMN` nicht (ältere Versionen) | Für den vollen Funktionsumfang in `.env` zu MySQL wechseln |
| Hinzufügen einer Spalte zu einer bestehenden Tabelle schlägt fehl | `Schema::create` statt `Schema::table` verwendet | Für Änderungen `Schema::table()` verwenden |
| Rollback macht Änderungen nicht rückgängig | Methode `down()` nicht implementiert | Immer eine `down()`-Methode implementieren, die `up()` umkehrt |

## Siehe auch {#see-also}

- [[laravel-eloquent-orm]] - Modelle, die auf migrierte Tabellen abgebildet werden
- [[laravel-architecture]] - Datenbankkonfiguration in `.env`
- https://laravel.com/docs/11.x/migrations
- https://laravel.com/docs/11.x/seeding
