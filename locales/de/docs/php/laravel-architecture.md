---
title: "Laravel-Architektur"
category: framework
tags: [laravel, architecture, service-container, service-providers, facades, artisan, directory-structure]
level: 3
source_sha256: 1ca84c63aa78291b4ac57706e367d1e003a713e771cae26c0aa052955862558b
translation: machine
translated_at: '2026-10-24'
---
# Laravel-Architektur {#laravel-architecture}

Laravel 11 ist ein PHP-Framework nach dem MVC-Muster mit Service Container (IoC), Service Providern, Facades und der Artisan-CLI. Das Verständnis der Architektur ist unerlässlich für die Arbeit mit [[laravel-routing]], [[laravel-eloquent-orm]], [[laravel-middleware]] und allen anderen Framework-Komponenten.

## Wichtige Fakten {#key-facts}

- Laravel verwendet den **Service Container** (IoC-Container) für Dependency Injection und Klassenauflösung
- **Service Provider** initialisieren Framework-Komponenten; sie werden in `bootstrap/providers.php` registriert (Laravel 11)
- **Facades** bieten statisch anmutenden Zugriff auf Container-Bindings (`Auth::check()`, `Route::get()`)
- **Artisan** ist die CLI für Scaffolding, Migrationen, Cache-Leerung und eigene Befehle
- Die Datei `.env` speichert umgebungsspezifische Konfiguration (DB-Zugangsdaten, App-Key, Debug-Modus)
- Das Verzeichnis `config/` enthält Konfigurationsdateien, die über den Helper `env()` Werte aus `.env` lesen
- Laravel 11 hat das Grundgerüst vereinfacht: weniger Standarddateien, `bootstrap/app.php` als zentraler Konfigurationspunkt
- Request-Lebenszyklus: HTTP-Request -> `public/index.php` -> Service Container -> Middleware -> Router -> Controller -> Response

## Muster {#patterns}

### Verzeichnisstruktur (Laravel 11) {#directory-structure-laravel-11}

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

### Umgebungskonfiguration {#environment-configuration}

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

### Artisan-CLI {#artisan-cli}

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

### Grundlagen des Service Containers {#service-container-basics}

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

### Facades vs. Hilfsfunktionen {#facades-vs-helper-functions}

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

## Fallstricke {#gotchas}

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| Konfigurationsänderungen werden nicht übernommen | Konfiguration ist gecacht | `php artisan config:clear` ausführen |
| `env()` gibt in Produktion null zurück | Config-Cache aktiv, `env()` funktioniert nur in Konfigurationsdateien | Überall außer in `config/*.php` den Helper `config()` verwenden |
| Klasse nach dem Erstellen nicht gefunden | Composer-Autoload nicht aktualisiert | `composer dump-autoload` ausführen |
| `Route [name] not defined` | Routenname falsch geschrieben oder Route nicht registriert | `php artisan route:list` prüfen |
| Änderungen an `.env` werden nicht übernommen | `.env` wird nicht automatisch neu geladen | Server neu starten / Config-Cache leeren |
| CSRF token mismatch | `@csrf` im Formular fehlt oder Sitzung abgelaufen | Blade-Direktive `@csrf` zu allen POST-Formularen hinzufügen |

## Siehe auch {#see-also}

- [[laravel-routing]] - URL-zu-Controller-Zuordnung
- [[laravel-middleware]] - Request-/Response-Pipeline
- https://laravel.com/docs/11.x/structure
- https://laravel.com/docs/11.x/container
- https://laravel.com/docs/11.x/artisan
