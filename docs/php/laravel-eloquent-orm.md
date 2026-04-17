---
title: Laravel Eloquent ORM
category: framework
tags: [laravel, eloquent, orm, models, relationships, query-builder, soft-deletes, mass-assignment]
---

# Laravel Eloquent ORM

Eloquent is Laravel's Active Record ORM. Each database table has a corresponding Model class used for querying and manipulating data. Models define relationships (hasMany, belongsTo, belongsToMany), scopes, accessors/mutators, and support soft deletes. Foundation of all CRUD operations in [[laravel-routing]] controllers.

## Key Facts

- Each model maps to a table: `Post` model -> `posts` table (convention: singular class, plural table)
- Primary key is `id` by default; `$primaryKey` property to override
- Timestamps (`created_at`, `updated_at`) are auto-managed; disable with `$timestamps = false`
- Mass assignment protection via `$fillable` (whitelist) or `$guarded` (blacklist) array
- Soft deletes: `use SoftDeletes` trait adds `deleted_at` column - records hidden but not removed
- Relationships: `hasOne`, `hasMany`, `belongsTo`, `belongsToMany`, `hasManyThrough`, `morphMany`
- Query builder methods are chainable: `Post::where()->orderBy()->paginate()`
- `findOrFail($id)` returns model or throws 404; `firstOrFail()` for query results
- Eager loading: `Post::with('category', 'tags')->get()` prevents N+1 queries
- Collections: Eloquent returns `Collection` objects with `map`, `filter`, `pluck`, `groupBy` methods

## Patterns

### Model definition

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

### CRUD operations

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

### Relationships in practice

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

### Query scopes

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

### Soft deletes

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

### Pagination

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

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `MassAssignmentException` | Property not in `$fillable` | Add column to `$fillable` array on model |
| N+1 query problem | Accessing relationship in loop without eager loading | Use `::with('relation')` for eager loading |
| Soft deleted records still showing | Not using `SoftDeletes` trait | Add `use SoftDeletes` to model + migration |
| Foreign key constraint error on delete | Child records reference parent | Delete children first or use `onDelete('cascade')` in migration |
| `belongsToMany` not working | Missing pivot table or wrong naming | Create `post_tag` table (alphabetical, singular) with `post_id` and `tag_id` |
| `$post->category` returns null | `category_id` is null or invalid | Check foreign key value; use `belongsTo` not `hasOne` |
| `update()` not saving | Missing `$fillable` or passing non-fillable fields | Check `$fillable` matches the fields you're updating |

## See Also

- [[laravel-migrations]] - creating tables and columns for models
- [[laravel-routing]] - CRUD routes calling Eloquent operations
- [[laravel-validation]] - validating data before Eloquent operations
- https://laravel.com/docs/11.x/eloquent
- https://laravel.com/docs/11.x/eloquent-relationships
- https://laravel.com/docs/11.x/eloquent-collections
