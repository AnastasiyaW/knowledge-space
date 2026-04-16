---
title: Laravel Middleware
category: framework
tags: [laravel, middleware, auth, authorization, request-pipeline, guards]
---

# Laravel Middleware

Middleware filters HTTP requests before they reach controllers. They form a pipeline where each middleware inspects, modifies, or rejects the request. Laravel uses middleware for authentication (`auth`), guest checking (`guest`), CSRF protection, rate limiting (throttle), and custom authorization logic. Middleware is central to [[laravel-routing]] protection and [[laravel-authentication]] flows.

## Key Facts

- Middleware are classes that receive a request, process it, and pass it to the next handler via `$next($request)`
- Built-in middleware: `auth` (require login), `guest` (require not logged in), `verified` (email verified), `throttle` (rate limit)
- CSRF token verification is a global middleware - applied to all web routes automatically
- Middleware can run **before** (inspect request) or **after** (modify response) the controller
- Custom middleware created via `php artisan make:middleware MiddlewareName`
- Register middleware in `bootstrap/app.php` (Laravel 11) or via route definition
- Middleware can be applied to: individual routes, route groups, or globally
- Multiple middleware can be combined: `->middleware(['auth', 'admin'])`

## Patterns

### Applying built-in middleware

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

### Creating custom middleware

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

### Registering middleware (Laravel 11)

```php
<?php
// bootstrap/app.php
use App\Http\Middleware\AdminMiddleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withMiddleware(function (Middleware $middleware) {
        // Register alias for route-level use
        $middleware->alias([
            'admin' => AdminMiddleware::class,
        ]);

        // Global middleware (runs on every request)
        $middleware->append(LogRequests::class);

        // Middleware groups
        $middleware->group('web', [
            // default web middleware...
        ]);
    })
    ->create();
```

### Before vs After middleware

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

### Middleware with parameters

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

### Request pipeline visualization

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

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Route login not defined` | `auth` middleware redirects to named route `login` which doesn't exist | Create a route with `->name('login')` |
| Middleware not running | Middleware not registered or alias not defined | Register in `bootstrap/app.php` or use FQCN |
| Infinite redirect loop | Middleware redirects to a route that also has the same middleware | Use `guest` middleware on login page, `auth` on protected pages |
| CSRF token mismatch | Form missing `@csrf` or session expired | Add `@csrf` to forms; for AJAX add token to headers |
| `auth` middleware alias not found | Custom middleware class name conflicts with built-in alias | Use a unique alias name (e.g., `is_admin` instead of `admin`) |
| Guest can access admin page | Middleware applied to individual routes but missed some | Use route group with middleware for consistency |

## See Also

- [[laravel-authentication]] - auth flow that middleware protects
- [[laravel-routing]] - applying middleware to routes
- [[laravel-architecture]] - middleware in the request lifecycle
- https://laravel.com/docs/11.x/middleware
