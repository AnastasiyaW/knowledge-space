---
title: "Laravel-Middleware"
category: framework
tags: [laravel, middleware, auth, authorization, request-pipeline, guards]
level: 3
source_sha256: 1a7a2c2d66950ea2c958eccef1a6cb2738e2b25694fa0a124f9c170d42f667f9
translation: machine
translated_at: '2026-10-24'
---
# Laravel-Middleware {#laravel-middleware}

Middleware filtert HTTP-Requests, bevor sie die Controller erreichen. Sie bilden eine Pipeline, in der jede Middleware den Request prüft, verändert oder ablehnt. Laravel nutzt Middleware für Authentifizierung (`auth`), Gastprüfung (`guest`), CSRF-Schutz, Rate Limiting (throttle) und eigene Autorisierungslogik. Middleware ist zentral für den Schutz von [[laravel-routing]] und die Abläufe in [[laravel-authentication]].

## Key Facts {#key-facts}

- Middleware sind Klassen, die einen Request entgegennehmen, verarbeiten und über `$next($request)` an den nächsten Handler weitergeben
- Eingebaute Middleware: `auth` (Anmeldung erforderlich), `guest` (Abmeldung erforderlich), `verified` (E-Mail-Adresse verifiziert), `throttle` (Rate Limiting)
- Die CSRF-Token-Prüfung ist eine globale Middleware und wird automatisch auf alle Web-Routen angewendet
- Middleware kann **vor** (Request prüfen) oder **nach** (Response verändern) dem Controller ausgeführt werden
- Eigene Middleware wird mit `php artisan make:middleware MiddlewareName` erstellt
- Middleware wird in `bootstrap/app.php` (Laravel 11) oder über die Routendefinition registriert
- Middleware kann angewendet werden auf: einzelne Routen, Routengruppen oder global
- Mehrere Middleware lassen sich kombinieren: `->middleware(['auth', 'admin'])`

## Patterns {#patterns}

### Eingebaute Middleware anwenden {#applying-built-in-middleware}

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

### Eigene Middleware erstellen {#creating-custom-middleware}

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

### Middleware registrieren (Laravel 11) {#registering-middleware-laravel-11}

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

### Vor vs. nach Middleware {#before-vs-after-middleware}

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

### Middleware mit Parametern {#middleware-with-parameters}

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

### Visualisierung der Request-Pipeline {#request-pipeline-visualization}

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

## Gotchas {#gotchas}

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| `Route login not defined` | Die `auth`-Middleware leitet auf die benannte Route `login` weiter, die nicht existiert | Eine Route mit `->name('login')` anlegen |
| Middleware wird nicht ausgeführt | Middleware nicht registriert oder Alias nicht definiert | In `bootstrap/app.php` registrieren oder FQCN verwenden |
| Endlose Weiterleitungsschleife | Middleware leitet auf eine Route weiter, die dieselbe Middleware ebenfalls verwendet | `guest`-Middleware auf der Login-Seite, `auth` auf geschützten Seiten verwenden |
| CSRF-Token-Mismatch | Formular ohne `@csrf` oder Session abgelaufen | `@csrf` in Formulare aufnehmen; bei AJAX das Token in den Headern übergeben |
| Alias `auth` middleware nicht gefunden | Der Klassenname der eigenen Middleware kollidiert mit einem eingebauten Alias | Einen eindeutigen Alias verwenden (z. B. `is_admin` statt `admin`) |
| Gast kann Admin-Seite aufrufen | Middleware wurde einzelnen Routen zugewiesen, einige wurden aber übersehen | Routengruppe mit Middleware verwenden, um Konsistenz sicherzustellen |

## See Also {#see-also}

- [[laravel-authentication]] - Authentifizierungsablauf, den Middleware schützt
- [[laravel-routing]] - Anwenden von Middleware auf Routen
- [[laravel-architecture]] - Middleware im Request-Lebenszyklus
- https://laravel.com/docs/11.x/middleware
