---
title: Laravel Migrations
category: framework
tags: [laravel, migrations, schema, database, foreign-keys, seeding]
---

# Laravel Migrations

Migrations are version control for the database schema. Each migration is a PHP class that creates, modifies, or drops tables and columns. Migrations run in order and can be rolled back. They work with [[laravel-eloquent-orm]] models and support foreign key constraints for relationships.

## Key Facts

- Migrations live in `database/migrations/` with timestamped filenames
- `php artisan make:migration create_posts_table` generates a migration class
- `php artisan make:model Post -m` creates model + migration together
- `up()` method applies changes; `down()` method reverses them
- `php artisan migrate` runs all pending migrations
- `php artisan migrate:rollback` undoes the last batch
- `php artisan migrate:fresh` drops all tables and re-runs all migrations (destructive)
- Foreign keys enforce referential integrity between tables
- `$table->softDeletes()` adds `deleted_at` column for [[laravel-eloquent-orm]] soft deletes
- Default migrations create `users`, `password_reset_tokens`, `sessions`, `cache`, `jobs` tables
- SQLite is the default database in Laravel 11; switch to MySQL/MariaDB via `.env`

## Patterns

### Creating a table

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

### Many-to-many pivot table

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

### Modifying existing tables

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

### Column types reference

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

### Artisan migration commands

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

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| Foreign key constraint error | Referenced table doesn't exist yet | Ensure referenced table migration runs first (earlier timestamp) |
| `Cannot delete parent row` | Child records exist with foreign key | Use `onDelete('cascade')` or delete children first |
| `Column already exists` | Migration ran partially or was modified after running | Run `migrate:fresh` in development; create new migration in production |
| Default SQLite can't handle some features | SQLite lacks `ALTER TABLE DROP COLUMN` (older versions) | Switch to MySQL in `.env` for full feature support |
| Adding column to existing table fails | Using `Schema::create` instead of `Schema::table` | Use `Schema::table()` for modifications |
| Rollback doesn't undo changes | `down()` method not implemented | Always implement `down()` that reverses `up()` |

## See Also

- [[laravel-eloquent-orm]] - models that map to migrated tables
- [[laravel-architecture]] - database configuration in `.env`
- https://laravel.com/docs/11.x/migrations
- https://laravel.com/docs/11.x/seeding
