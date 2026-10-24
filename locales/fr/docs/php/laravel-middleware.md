---
title: "Middleware Laravel"
category: framework
tags: [laravel, middleware, auth, authorization, request-pipeline, guards]
level: 3
source_sha256: 1a7a2c2d66950ea2c958eccef1a6cb2738e2b25694fa0a124f9c170d42f667f9
translation: machine
translated_at: '2026-10-24'
---
# Middleware Laravel {#laravel-middleware}

Les middleware filtrent les requêtes HTTP avant qu'elles n'atteignent les contrôleurs. Ils forment un pipeline dans lequel chaque middleware inspecte, modifie ou rejette la requête. Laravel utilise les middleware pour l'authentification (`auth`), la vérification des invités (`guest`), la protection CSRF, la limitation de débit (throttle) et la logique d'autorisation personnalisée. Les middleware sont au cœur de la protection des [[laravel-routing]] et des flux d'[[laravel-authentication]].

## Points clés {#key-facts}

- Un middleware est une classe qui reçoit une requête, la traite et la transmet au gestionnaire suivant via `$next($request)`
- Middleware intégrés : `auth` (connexion requise), `guest` (non connecté requis), `verified` (e-mail vérifié), `throttle` (limitation de débit)
- La vérification du jeton CSRF est un middleware global, appliqué automatiquement à toutes les routes web
- Un middleware peut s'exécuter **avant** (inspection de la requête) ou **après** (modification de la réponse) le contrôleur
- Un middleware personnalisé se crée avec `php artisan make:middleware MiddlewareName`
- Enregistrez les middleware dans `bootstrap/app.php` (Laravel 11) ou via la définition de la route
- Un middleware peut être appliqué à une route individuelle, à un groupe de routes ou globalement
- Plusieurs middleware peuvent être combinés : `->middleware(['auth', 'admin'])`

## Modèles d'utilisation {#patterns}

### Application des middleware intégrés {#applying-built-in-middleware}

```php
<?php
use Illuminate\Support\Facades\Route;

// Single middleware
Route::get('/admin', [AdminController::class, 'index'])
    ->middleware('auth')
    ->name('admin.main.index');

// Multiple middleware
Route::get('/admin', [AdminController::class, 'index'])
    ->middleware(['auth', 'admin']);

// Route group with middleware
Route::middleware(['auth', 'admin'])->prefix('admin')->group(function () {
    Route::get('/', [AdminController::class, 'index']);
    Route::resource('posts', PostController::class);
});

// Excluding middleware
Route::withoutMiddleware(['csrf'])->group(function () {
    Route::post('/webhook', [WebhookController::class, 'handle']);
});
```

### Création d'un middleware personnalisé {#creating-custom-middleware}

```bash
php artisan make:middleware AdminMiddleware
```

```php
<?php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class AdminMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        // Check if user is authenticated AND has admin role
        if (!auth()->check() || !auth()->user()->isAdmin()) {
            abort(403, 'Access denied.');
        }

        return $next($request);  // pass request to next middleware/controller
    }
}
```

### Enregistrement d'un middleware (Laravel 11) {#registering-middleware-laravel-11}

```php
<?php
// bootstrap/app.php
use App\Http\Middleware\AdminMiddleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withMiddleware(function (Middleware $middleware) {
        // Register alias for route-level use
        $middleware->alias([
            'admin' => AdminMiddleware::class]);

        // Global middleware (runs on every request)
        $middleware->append(LogRequests::class);

        // Middleware groups
        $middleware->group('web', [
            // default web middleware...
        ]);
    })
    ->create();
```

### Middleware avant et après {#before-vs-after-middleware}

```php
<?php
// BEFORE middleware - runs before controller
class CheckAge
{
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->age < 18) {
            return redirect('home');
        }
        return $next($request);  // continue to controller
    }
}

// AFTER middleware - runs after controller
class AddHeaders
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);  // get controller response first
        $response->headers->set('X-Custom-Header', 'value');
        return $response;
    }
}
```

### Middleware avec paramètres {#middleware-with-parameters}

```php
<?php
class RoleMiddleware
{
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (!$request->user()?->hasRole($role)) {
            abort(403);
        }
        return $next($request);
    }
}

// Usage in routes
Route::get('/admin', [AdminController::class, 'index'])
    ->middleware('role:admin');

Route::get('/editor', [EditorController::class, 'index'])
    ->middleware('role:editor');
```

### Visualisation du pipeline de requête {#request-pipeline-visualization}

```text
HTTP Request
  |
  v
[CSRF Middleware]         -- rejects if token invalid
  |
  v
[Auth Middleware]         -- redirects to /login if not authenticated
  |
  v
[Admin Middleware]        -- returns 403 if not admin
  |
  v
[Controller::action()]   -- handles request, returns response
  |
  v
[After Middleware]        -- modifies response (headers, logging)
  |
  v
HTTP Response
```

## Pièges courants {#gotchas}

| Symptôme | Cause | Solution |
|---------|-------|-----|
| `Route login not defined` | Le middleware `auth` redirige vers la route nommée `login`, qui n'existe pas | Créer une route avec `->name('login')` |
| Le middleware ne s'exécute pas | Middleware non enregistré ou alias non défini | L'enregistrer dans `bootstrap/app.php` ou utiliser le FQCN |
| Boucle de redirection infinie | Le middleware redirige vers une route qui possède elle-même le même middleware | Utiliser le middleware `guest` sur la page de connexion, `auth` sur les pages protégées |
| CSRF token mismatch | Formulaire sans `@csrf` ou session expirée | Ajouter `@csrf` aux formulaires ; pour les requêtes AJAX, ajouter le jeton dans les en-têtes |
| Alias du middleware `auth` introuvable | Le nom de la classe du middleware personnalisé entre en conflit avec un alias intégré | Utiliser un nom d'alias unique (par exemple `is_admin` au lieu de `admin`) |
| Un invité peut accéder à la page d'administration | Middleware appliqué à certaines routes individuelles mais oublié sur d'autres | Utiliser un groupe de routes avec le middleware pour assurer la cohérence |

## Voir aussi {#see-also}

- [[laravel-authentication]] - flux d'authentification protégé par les middleware
- [[laravel-routing]] - application des middleware aux routes
- [[laravel-architecture]] - middleware dans le cycle de vie de la requête
- https://laravel.com/docs/11.x/middleware
