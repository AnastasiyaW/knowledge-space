---
title: "Routage Laravel"
category: framework
tags: [laravel, routing, controllers, resource-routes, named-routes, route-groups]
level: 3
source_sha256: be23616c9db8b2530739b19862343cbed152b0765810fb4fdadba1a9aed5a7ad
translation: machine
translated_at: '2026-10-24'
---
# Routage Laravel {#laravel-routing}

Les routes associent les requêtes HTTP aux actions des contrôleurs. Elles sont définies dans `routes/web.php` (session/CSRF) et `routes/api.php` (sans état). Les routes prennent en charge les paramètres, les références nommées, le regroupement et les conventions CRUD des ressources. Les contrôleurs organisent les gestionnaires de routes par domaine. Étroitement liées à [[laravel-middleware]] pour le contrôle d'accès et à [[laravel-blade-templates]] pour le rendu des vues.

## Points clés {#key-facts}

- `routes/web.php` - routes web avec session, protection CSRF, middleware de cookies
- `routes/api.php` - routes API, sans état, préfixe `/api` par défaut
- Méthodes de route : `Route::get()`, `::post()`, `::put()`, `::patch()`, `::delete()`, `::any()`, `::match()`
- Routes nommées : `->name('posts.index')` - utilisées dans le helper `route('posts.index')` pour générer des URL
- Paramètres de route : `{id}` obligatoire, `{id?}` optionnel
- Route model binding : typer un modèle Eloquent dans le contrôleur pour le résoudre automatiquement par ID
- Routes de ressources : `Route::resource('posts', PostController::class)` génère 7 routes CRUD
- Groupes de routes : partagent middleware, préfixe et namespace entre plusieurs routes
- `php artisan route:list` affiche toutes les routes enregistrées

## Modèles {#patterns}

### Routes de base {#basic-routes}

```php
<?php
use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

// Closure route (simple pages)
Route::get('/', function () {
    return view('welcome');
});

// Controller route
Route::get('/posts', [PostController::class, 'index'])->name('posts.index');
Route::get('/posts/{post}', [PostController::class, 'show'])->name('posts.show');
Route::post('/posts', [PostController::class, 'store'])->name('posts.store');
Route::put('/posts/{post}', [PostController::class, 'update'])->name('posts.update');
Route::delete('/posts/{post}', [PostController::class, 'destroy'])->name('posts.destroy');
```

### Routes de ressources (CRUD) {#resource-routes-crud}

```php
<?php
// Generates all 7 RESTful routes
Route::resource('posts', PostController::class);

// Equivalent to:
// GET    /posts              -> index    posts.index
// GET    /posts/create       -> create   posts.create
// POST   /posts              -> store    posts.store
// GET    /posts/{post}       -> show     posts.show
// GET    /posts/{post}/edit  -> edit     posts.edit
// PUT    /posts/{post}       -> update   posts.update
// DELETE /posts/{post}       -> destroy  posts.destroy

// Partial resource
Route::resource('posts', PostController::class)->only(['index', 'show']);
Route::resource('posts', PostController::class)->except(['destroy']);

// API resource (no create/edit - those are form views)
Route::apiResource('posts', PostController::class);
```

### Groupes de routes {#route-groups}

```php
<?php
// Admin routes with prefix, middleware, and controller namespace
Route::prefix('admin')
    ->middleware(['auth', 'admin'])
    ->name('admin.')
    ->group(function () {
        Route::get('/', [Admin\MainController::class, 'index'])->name('main.index');
        Route::resource('posts', Admin\PostController::class);
        Route::resource('categories', Admin\CategoryController::class);
    });
// Generates: admin/posts, admin/categories, etc.
// Names: admin.posts.index, admin.categories.index, etc.
```

### Route model binding {#route-model-binding}

```php
<?php
// Implicit binding - Laravel resolves {post} to Post model by ID
Route::get('/posts/{post}', function (Post $post) {
    return view('posts.show', compact('post'));
});
// Automatically returns 404 if post not found

// Custom column binding
Route::get('/posts/{post:slug}', function (Post $post) {
    return $post; // resolved by slug column
});
```

### Contrôleurs {#controllers}

```php
<?php
namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::latest()->paginate(15);
        return view('posts.index', compact('posts'));
    }

    public function show(Post $post)
    {
        return view('posts.show', compact('post'));
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'body'  => 'required']);

        Post::create($validated);
        return redirect()->route('posts.index')
            ->with('success', 'Post created.');
    }

    public function destroy(Post $post)
    {
        $post->delete();
        return redirect()->route('posts.index')
            ->with('success', 'Post deleted.');
    }
}
```

### Génération d'URL {#url-generation}

```php
<?php
// In Blade templates
<a href="{{ route('posts.show', $post) }}">View</a>
<a href="{{ route('posts.edit', ['post' => $post->id]) }}">Edit</a>

// In controllers
return redirect()->route('admin.main.index');
return redirect()->back()->with('error', 'Not found');

// Asset URLs
<link href="{{ asset('assets/admin/css/adminlte.css') }}" rel="stylesheet">
```

## Pièges {#gotchas}

| Symptôme | Cause | Correctif |
|----------|-------|-----------|
| `Route [name] not defined` | Faute de frappe dans le nom de la route ou route non enregistrée | Exécuter `php artisan route:list` pour vérifier |
| Mauvaise route correspondante (ex. `posts/create` atteint `posts/{post}`) | L'ordre des routes compte - les routes spécifiques doivent précéder les routes paramétrées | Placer `posts/create` avant `posts/{post}` |
| 405 Method Not Allowed | Le formulaire utilise GET alors que la route attend POST, ou `@method('PUT')` est absent | Ajouter `@method('PUT')` ou `@method('DELETE')` au formulaire |
| Le route model binding renvoie 404 | Modèle introuvable par ID (ou supprimé logiquement) | Vérifier la base de données ou utiliser `withTrashed()` dans la liaison de route |
| Erreur de jeton CSRF sur POST | Directive `@csrf` absente du formulaire | Ajouter `@csrf` à l'intérieur de la balise `<form>` |
| Cache de routes obsolète après modifications | Le cache de routes a été généré avant l'ajout de nouvelles routes | Exécuter `php artisan route:clear` |

## Voir aussi {#see-also}

- [[laravel-middleware]] - protection des routes par authentification et vérifications admin
- [[laravel-blade-templates]] - rendu des vues depuis les contrôleurs
- [[laravel-validation]] - validation des données de requête
- https://laravel.com/docs/11.x/routing
- https://laravel.com/docs/11.x/controllers
