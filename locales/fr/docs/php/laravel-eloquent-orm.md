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

Eloquent est l'ORM Active Record de Laravel. Chaque table de base de données possède une classe Model correspondante, utilisée pour interroger et manipuler les données. Les modèles définissent des relations (hasMany, belongsTo, belongsToMany), des scopes, des accesseurs/mutateurs, et prennent en charge les suppressions logiques (soft deletes). Socle de toutes les opérations CRUD dans les contrôleurs de [[laravel-routing]].

## Points clés {#key-facts}

- Chaque modèle correspond à une table : modèle `Post` -> table `posts` (convention : classe au singulier, table au pluriel)
- La clé primaire est `id` par défaut ; la propriété `$primaryKey` permet de la modifier
- Les horodatages (`created_at`, `updated_at`) sont gérés automatiquement ; à désactiver avec `$timestamps = false`
- Protection contre l'assignation de masse via le tableau `$fillable` (liste blanche) ou `$guarded` (liste noire)
- Suppressions logiques : le trait `use SoftDeletes` ajoute la colonne `deleted_at` — les enregistrements sont masqués sans être supprimés
- Relations : `hasOne`, `hasMany`, `belongsTo`, `belongsToMany`, `hasManyThrough`, `morphMany`
- Les méthodes du query builder sont chaînables : `Post::where()->orderBy()->paginate()`
- `findOrFail($id)` renvoie le modèle ou lève une erreur 404 ; `firstOrFail()` pour les résultats de requête
- Chargement anticipé (eager loading) : `Post::with('category', 'tags')->get()` évite le problème des requêtes N+1
- Collections : Eloquent renvoie des objets `Collection` dotés des méthodes `map`, `filter`, `pluck`, `groupBy`

## Modèles {#patterns}

### Définition d'un modèle {#model-definition}

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

### Opérations CRUD {#crud-operations}

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

### Relations en pratique {#relationships-in-practice}

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

### Scopes de requête {#query-scopes}

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

### Suppressions logiques {#soft-deletes}

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

## Pièges courants {#gotchas}

| Symptôme | Cause | Correction |
|---------|-------|-----|
| `MassAssignmentException` | Propriété absente de `$fillable` | Ajouter la colonne au tableau `$fillable` du modèle |
| Problème de requêtes N+1 | Accès à une relation dans une boucle sans chargement anticipé | Utiliser `::with('relation')` pour le chargement anticipé |
| Enregistrements supprimés encore affichés | Trait `SoftDeletes` non utilisé | Ajouter `use SoftDeletes` au modèle + à la migration |
| Erreur de contrainte de clé étrangère lors de la suppression | Des enregistrements enfants référencent le parent | Supprimer d'abord les enfants ou utiliser `onDelete('cascade')` dans la migration |
| `belongsToMany` ne fonctionne pas | Table pivot manquante ou nommage incorrect | Créer la table `post_tag` (ordre alphabétique, singulier) avec `post_id` et `tag_id` |
| `$post->category` renvoie null | `category_id` est null ou invalide | Vérifier la valeur de la clé étrangère ; utiliser `belongsTo` et non `hasOne` |
| `update()` ne sauvegarde pas | `$fillable` manquant ou champs non autorisés transmis | Vérifier que `$fillable` contient les champs mis à jour |

## Voir aussi {#see-also}

- [[laravel-migrations]] - création des tables et colonnes des modèles
- [[laravel-routing]] - routes CRUD appelant les opérations Eloquent
- [[laravel-validation]] - validation des données avant les opérations Eloquent
- https://laravel.com/docs/11.x/eloquent
- https://laravel.com/docs/11.x/eloquent-relationships
- https://laravel.com/docs/11.x/eloquent-collections
