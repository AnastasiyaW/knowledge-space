---
title: Laravel Architecture
category: framework
tags: [laravel, architecture, service-container, service-providers, facades, artisan, directory-structure]
---

# Laravel Architecture

Laravel 11 is a PHP framework following the MVC pattern with a service container (IoC), service providers, facades, and Artisan CLI. Understanding the architecture is essential for working with [[laravel-routing]], [[laravel-eloquent-orm]], [[laravel-middleware]], and all other framework components.

## Key Facts

- Laravel uses the **service container** (IoC container) for dependency injection and class resolution
- **Service providers** bootstrap framework components; registered in `bootstrap/providers.php` (Laravel 11)
- **Facades** provide static-like access to container bindings (`Auth::check()`, `Route::get()`)
- **Artisan** is the CLI for scaffolding, migrations, cache clearing, and custom commands
- `.env` file stores environment-specific configuration (DB credentials, app key, debug mode)
- `config/` directory holds configuration files that read from `.env` via `env()` helper
- Laravel 11 simplified the skeleton: fewer default files, `bootstrap/app.php` as the central config point
- Request lifecycle: HTTP request -> `public/index.php` -> service container -> middleware -> router -> controller -> response

## Patterns

### Directory structure (Laravel 11)

```hcl
project/
  app/
    Http/
      Controllers/          # request handlers
      Middleware/            # custom middleware
    Models/                  # Eloquent models
    Providers/               # service providers
  bootstrap/
    app.php                  # application bootstrap (middleware, routes, exceptions)
    providers.php            # registered service providers
  config/                    # configuration files
  database/
    migrations/              # database schema changes
    seeders/                 # test data seeders
  public/
    index.php                # entry point (all requests route here)
  resources/
    views/                   # Blade templates
  routes/
    web.php                  # web routes (session, CSRF)
    api.php                  # API routes (stateless)
  storage/                   # logs, cache, compiled views
  .env                       # environment variables
  composer.json              # dependencies
  artisan                    # CLI entry point
```

### Environment configuration

```bash
# .env file
APP_NAME=MyApp
APP_ENV=local
APP_DEBUG=true
APP_URL=http://myapp.test

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel_practice
DB_USERNAME=root
DB_PASSWORD=
```

```php
<?php
// Accessing config values
$debug = config('app.debug');           // reads config/app.php
$dbHost = config('database.connections.mysql.host');
$appName = env('APP_NAME', 'Laravel');  // with default fallback

// NEVER use env() outside config files - values are cached in production
```

### Artisan CLI

```bash
# Scaffolding
php artisan make:controller PostController
php artisan make:controller Admin/MainController  # subdirectory
php artisan make:model Post -m                     # model + migration
php artisan make:middleware AdminMiddleware
php artisan make:request StorePostRequest

# Database
php artisan migrate                    # run pending migrations
php artisan migrate:rollback           # undo last batch
php artisan migrate:fresh              # drop all tables + re-migrate
php artisan db:seed                    # run seeders

# Cache
php artisan config:cache               # cache config (production)
php artisan route:cache                # cache routes (production)
php artisan cache:clear                # clear application cache
php artisan view:clear                 # clear compiled views

# Maintenance
php artisan down                       # maintenance mode
php artisan up                         # exit maintenance mode

# Custom commands
php artisan make:command SendEmails
```

### Service container basics

```php
<?php
// Binding
app()->bind(PaymentGateway::class, StripeGateway::class);
app()->singleton(Logger::class, fn() => new FileLogger('/var/log'));

// Resolution
$gateway = app(PaymentGateway::class);
$gateway = resolve(PaymentGateway::class);

// Automatic injection in controllers
class OrderController extends Controller {
    public function store(Request $request, PaymentGateway $gateway) {
        // $gateway is automatically resolved from container
    }
}
```

### Facades vs helper functions

```php
<?php
// Facade
use Illuminate\Support\Facades\Auth;
Auth::check();           // is user authenticated?
Auth::user();            // get current user object
Auth::attempt($creds);   // try to log in

// Equivalent helper function
auth()->check();
auth()->user();
auth()->attempt($creds);

// Both resolve the same underlying class from the container
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| Config changes not reflected | Config is cached | Run `php artisan config:clear` |
| `env()` returns null in production | Config cache active, `env()` only works in config files | Use `config()` helper everywhere except `config/*.php` |
| Class not found after creating | Composer autoload not refreshed | Run `composer dump-autoload` |
| `Route [name] not defined` | Route name misspelled or route not registered | Check `php artisan route:list` |
| `.env` changes not applied | `.env` is not auto-reloaded | Restart server / clear config cache |
| CSRF token mismatch | Missing `@csrf` in form or session expired | Add `@csrf` blade directive to all POST forms |

## See Also

- [[laravel-routing]] - URL to controller mapping
- [[laravel-middleware]] - request/response pipeline
- https://laravel.com/docs/11.x/structure
- https://laravel.com/docs/11.x/container
- https://laravel.com/docs/11.x/artisan
