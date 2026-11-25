---
title: "Architecture de Laravel"
category: framework
tags: [laravel, architecture, service-container, service-providers, facades, artisan, directory-structure]
level: 3
source_sha256: 1ca84c63aa78291b4ac57706e367d1e003a713e771cae26c0aa052955862558b
translation: machine
translated_at: '2026-10-24'
---
# Architecture de Laravel {#laravel-architecture}

Laravel 11 est un framework PHP suivant le patron MVC, avec un conteneur de services (IoC), des fournisseurs de services, des façades et l'interface en ligne de commande Artisan. Comprendre l'architecture est indispensable pour travailler avec [[laravel-routing]], [[laravel-eloquent-orm]], [[laravel-middleware]] et tous les autres composants du framework.

## Points clés {#key-facts}

- Laravel utilise le **conteneur de services** (conteneur IoC) pour l'injection de dépendances et la résolution de classes
- Les **fournisseurs de services** initialisent les composants du framework ; ils sont enregistrés dans `bootstrap/providers.php` (Laravel 11)
- Les **façades** offrent un accès de type statique aux liaisons du conteneur (`Auth::check()`, `Route::get()`)
- **Artisan** est l'interface en ligne de commande pour générer du code, exécuter les migrations, vider le cache et créer des commandes personnalisées
- Le fichier `.env` stocke la configuration propre à l'environnement (identifiants de base de données, clé de l'application, mode debug)
- Le répertoire `config/` contient les fichiers de configuration qui lisent `.env` via la fonction utilitaire `env()`
- Laravel 11 a simplifié le squelette : moins de fichiers par défaut, `bootstrap/app.php` comme point central de configuration
- Cycle de vie d'une requête : requête HTTP -> `public/index.php` -> conteneur de services -> middleware -> routeur -> contrôleur -> réponse

## Modèles {#patterns}

### Structure des répertoires (Laravel 11) {#directory-structure-laravel-11}

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

### Configuration de l'environnement {#environment-configuration}

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

### Artisan CLI {#artisan-cli}

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

### Bases du conteneur de services {#service-container-basics}

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

### Façades ou fonctions utilitaires {#facades-vs-helper-functions}

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

## Pièges courants {#gotchas}

| Symptôme | Cause | Correctif |
|----------|-------|-----------|
| Les modifications de configuration ne sont pas prises en compte | La configuration est mise en cache | Exécuter `php artisan config:clear` |
| `env()` renvoie null en production | Cache de configuration actif, `env()` ne fonctionne que dans les fichiers de configuration | Utiliser partout la fonction `config()`, sauf dans `config/*.php` |
| Classe introuvable après sa création | L'autoload de Composer n'a pas été rafraîchi | Exécuter `composer dump-autoload` |
| `Route [name] not defined` | Nom de route mal orthographié ou route non enregistrée | Vérifier avec `php artisan route:list` |
| Les modifications de `.env` ne sont pas appliquées | `.env` n'est pas rechargé automatiquement | Redémarrer le serveur ou vider le cache de configuration |
| Erreur de jeton CSRF (token mismatch) | `@csrf` absent du formulaire ou session expirée | Ajouter la directive Blade `@csrf` à tous les formulaires POST |

## Voir aussi {#see-also}

- [[laravel-routing]] - correspondance entre URL et contrôleur
- [[laravel-middleware]] - pipeline de requêtes et de réponses
- https://laravel.com/docs/11.x/structure
- https://laravel.com/docs/11.x/container
- https://laravel.com/docs/11.x/artisan
