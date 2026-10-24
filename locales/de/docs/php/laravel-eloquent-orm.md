---
title: "Laravel Eloquent ORM"
category: framework
tags: [laravel, eloquent, orm, models, relationships, query-builder, soft-deletes, mass-assignment]
level: 3
source_sha256: 1b14e98b823201ad730ca46e4a65360c5c47a4b3c5bd897655f0b10578e6d22a
translation: machine
translated_at: '2026-10-24'
---
# Laravel Eloquent ORM {#laravel-eloquent-orm}

Eloquent ist der Active-Record-ORM von Laravel. Jede Datenbanktabelle hat eine entsprechende Model-Klasse, die zum Abfragen und Bearbeiten von Daten verwendet wird. Models definieren Beziehungen (hasMany, belongsTo, belongsToMany), Scopes, Accessors/Mutators und unterstützen Soft Deletes. Sie bilden die Grundlage aller CRUD-Operationen in den Controllern von [[laravel-routing]].

## Key Facts {#key-facts}

- Jedes Model ist einer Tabelle zugeordnet: `Post`-Model -> `posts`-Tabelle (Konvention: Klassenname im Singular, Tabellenname im Plural)
- Der Primärschlüssel ist standardmäßig `id`; mit der Property `$primaryKey` lässt er sich überschreiben
- Zeitstempel (`created_at`, `updated_at`) werden automatisch verwaltet; deaktivieren mit `$timestamps = false`
- Schutz vor Mass Assignment über das Array `$fillable` (Whitelist) oder `$guarded` (Blacklist)
- Soft Deletes: Der Trait `use SoftDeletes` fügt die Spalte `deleted_at` hinzu - Datensätze werden ausgeblendet, aber nicht entfernt
- Beziehungen: `hasOne`, `hasMany`, `belongsTo`, `belongsToMany`, `hasManyThrough`, `morphMany`
- Query-Builder-Methoden sind verkettbar: `Post::where()->orderBy()->paginate()`
- `findOrFail($id)` gibt das Model zurück oder wirft einen 404-Fehler; `firstOrFail()` für Abfrageergebnisse
- Eager Loading: `Post::with('category', 'tags')->get()` verhindert N+1-Abfragen
- Collections: Eloquent liefert `Collection`-Objekte mit den Methoden `map`, `filter`, `pluck` und `groupBy`

## Patterns {#patterns}

### Model definition {#model-definition}

```php
<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use SoftDeletes;

    protected $table = 'posts';  // only needed if non-conventional

    protected $fillable = [
        'title', 'slug', 'body', 'category_id', 'is_published'];

    protected $casts = [
        'is_published' => 'boolean',
        'published_at' => 'datetime'];

    // Relationships
    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function tags()
    {
        return $this->belongsToMany(Tag::class);  // many-to-many via pivot table
    }

    public function author()
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

### CRUD operations {#crud-operations}

```php
<?php
// CREATE
$post = Post::create([
    'title'       => 'My Post',
    'slug'        => 'my-post',
    'body'        => 'Content here',
    'category_id' => 1]);

// READ
$posts = Post::all();                              // all records
$post = Post::find(1);                             // by ID (or null)
$post = Post::findOrFail(1);                       // by ID (or 404)
$posts = Post::where('is_published', true)->get();  // with condition
$post = Post::where('slug', 'my-post')->first();   // single record
$latest = Post::latest()->take(5)->get();           // latest 5

// UPDATE
$post = Post::findOrFail($id);
$post->update(['title' => 'Updated Title']);

// or individually
$post->title = 'Updated Title';
$post->save();

// DELETE
$post->delete();           // soft delete if SoftDeletes trait used
$post->forceDelete();      // permanent delete (bypasses soft delete)

// RESTORE (soft deleted)
$post->restore();
```

### Relationships in practice {#relationships-in-practice}

```php
<?php
// One-to-Many: Category has many Posts
class Category extends Model {
    public function posts() {
        return $this->hasMany(Post::class);
    }
}

// Inverse: Post belongs to Category
class Post extends Model {
    public function category() {
        return $this->belongsTo(Category::class);
    }
}

// Many-to-Many: Post <-> Tag (through post_tag pivot table)
class Post extends Model {
    public function tags() {
        return $this->belongsToMany(Tag::class);
    }
}

// Attaching/detaching many-to-many
$post->tags()->attach([1, 2, 3]);        // add tag IDs
$post->tags()->detach([2]);               // remove tag ID 2
$post->tags()->sync([1, 3, 5]);           // set exactly these tags
$post->tags()->toggle([2, 4]);            // add if missing, remove if present

// Eager loading (prevent N+1 queries)
$posts = Post::with('category', 'tags')->paginate(15);
// Now $post->category and $post->tags are pre-loaded
```

### Query scopes {#query-scopes}

```php
<?php
class Post extends Model
{
    // Local scope
    public function scopePublished($query)
    {
        return $query->where('is_published', true);
    }

    public function scopeByCategory($query, int $categoryId)
    {
        return $query->where('category_id', $categoryId);
    }
}

// Usage
$posts = Post::published()->byCategory(3)->latest()->get();
```

### Soft deletes {#soft-deletes}

```php
<?php
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use SoftDeletes;  // requires 'deleted_at' column in migration
}

// Querying
$posts = Post::all();              // only non-deleted
$posts = Post::withTrashed()->get(); // include soft-deleted
$posts = Post::onlyTrashed()->get(); // only soft-deleted (trash)

// Restore
$post = Post::onlyTrashed()->findOrFail($id);
$post->restore();

// Permanent delete
$post->forceDelete();

// Check if soft deleted
if ($post->trashed()) { /* ... */ }
```

### Pagination {#pagination}

```php
<?php
// Controller
$posts = Post::latest()->paginate(15);  // 15 per page
return view('posts.index', compact('posts'));

// Blade template
@foreach ($posts as $post)
    <h2>{{ $post->title }}</h2>
@endforeach

{{ $posts->links() }}  {{-- pagination links --}}
```

## Gotchas {#gotchas}

| Symptom | Cause | Fix |
|---------|-------|-----|
| `MassAssignmentException` | Property not in `$fillable` | Add column to `$fillable` array on model |
| N+1 query problem | Accessing relationship in loop without eager loading | Use `::with('relation')` for eager loading |
| Soft deleted records still showing | Not using `SoftDeletes` trait | Add `use SoftDeletes` to model + migration |
| Foreign key constraint error on delete | Child records reference parent | Delete children first or use `onDelete('cascade')` in migration |
| `belongsToMany` not working | Missing pivot table or wrong naming | Create `post_tag` table (alphabetical, singular) with `post_id` and `tag_id` |
| `$post->category` returns null | `category_id` is null or invalid | Check foreign key value; use `belongsTo` not `hasOne` |
| `update()` not saving | Missing `$fillable` or passing non-fillable fields | Check `$fillable` matches the fields you're updating |

## See Also {#see-also}

- [[laravel-migrations]] - creating tables and columns for models
- [[laravel-routing]] - CRUD routes calling Eloquent operations
- [[laravel-validation]] - validating data before Eloquent operations
- https://laravel.com/docs/11.x/eloquent
- https://laravel.com/docs/11.x/eloquent-relationships
- https://laravel.com/docs/11.x/eloquent-collections
