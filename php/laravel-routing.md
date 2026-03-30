---
title: Laravel Routing
category: framework
tags: [laravel, routing, controllers, resource-routes, named-routes, route-groups]
---

# Laravel Routing

Routes map HTTP requests to controller actions. Defined in `routes/web.php` (session/CSRF) and `routes/api.php` (stateless). Routes support parameters, named references, grouping, and resource CRUD conventions. Controllers organize route handlers by domain. Closely tied to [[laravel-middleware]] for access control and [[laravel-blade-templates]] for view rendering.

## Key Facts

- `routes/web.php` - web routes with session, CSRF protection, cookie middleware
- `routes/api.php` - API routes, stateless, `/api` prefix by default
- Route methods: `Route::get()`, `::post()`, `::put()`, `::patch()`, `::delete()`, `::any()`, `::match()`
- Named routes: `->name('posts.index')` - used in `route('posts.index')` helper for URL generation
- Route parameters: `{id}` required, `{id?}` optional
- Route model binding: type-hint Eloquent model in controller to auto-resolve by ID
- Resource routes: `Route::resource('posts', PostController::class)` generates 7 CRUD routes
- Route groups: share middleware, prefix, namespace across multiple routes
- `php artisan route:list` shows all registered routes

## Patterns

### Basic routes

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

### Resource routes (CRUD)

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

### Route groups

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

### Route model binding

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

### Controllers

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
            'body'  => 'required',
        ]);

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

### URL generation

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

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Route [name] not defined` | Typo in route name or route not registered | Run `php artisan route:list` to verify |
| Wrong route matches (e.g., `posts/create` hits `posts/{post}`) | Route order matters - specific routes before parameterized | Place `posts/create` before `posts/{post}` |
| 405 Method Not Allowed | Form uses GET but route expects POST, or missing `@method('PUT')` | Add `@method('PUT')` or `@method('DELETE')` to form |
| Route model binding returns 404 | Model not found by ID (or soft deleted) | Check database or use `withTrashed()` in route binding |
| CSRF token mismatch on POST | Missing `@csrf` directive in form | Add `@csrf` inside `<form>` tag |
| Route cache stale after changes | Route cache was generated before new routes | Run `php artisan route:clear` |

## See Also

- [[laravel-middleware]] - protecting routes with auth, admin checks
- [[laravel-blade-templates]] - rendering views from controllers
- [[laravel-validation]] - validating request data
- https://laravel.com/docs/11.x/routing
- https://laravel.com/docs/11.x/controllers
