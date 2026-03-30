---
title: Composer and Autoloading
category: tooling
tags: [php, composer, autoloading, psr-4, dependencies, packages]
---

# Composer and Autoloading

Composer is PHP's dependency manager and autoloader. It resolves packages from Packagist, manages version constraints, and generates PSR-4 autoload maps. Every modern PHP project - including [[laravel-architecture]] - relies on Composer for dependency resolution and class autoloading.

## Key Facts

- `composer.json` defines project metadata, dependencies, and autoloading rules
- `composer.lock` pins exact versions for reproducible installs (commit this file)
- `vendor/` directory contains all installed packages (do not commit)
- `vendor/autoload.php` is the single entry point for autoloading all classes
- PSR-4: maps namespace prefixes to directory paths (`App\` -> `app/`)
- `composer install` reads `.lock` file; `composer update` resolves new versions and updates `.lock`
- `composer require package/name` adds a dependency
- `composer dump-autoload` regenerates autoload maps without installing packages
- Laravel is installed via `composer create-project laravel/laravel project-name`

## Patterns

### composer.json structure

```json
{
    "name": "vendor/project",
    "description": "My PHP project",
    "type": "project",
    "require": {
        "php": "^8.1",
        "laravel/framework": "^11.0",
        "guzzlehttp/guzzle": "^7.0"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "laravel/pint": "^1.0"
    },
    "autoload": {
        "psr-4": {
            "App\\": "app/",
            "Database\\": "database/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    },
    "scripts": {
        "post-autoload-dump": [
            "@php artisan package:discover --ansi"
        ]
    }
}
```

### Common Composer commands

```bash
# Create new Laravel project
composer create-project laravel/laravel my-app

# Install from lock file (CI/production)
composer install --no-dev --optimize-autoloader

# Add a package
composer require guzzlehttp/guzzle

# Add dev dependency
composer require --dev phpunit/phpunit

# Update dependencies
composer update                    # all packages
composer update vendor/package     # specific package

# Regenerate autoload (after adding new class/namespace)
composer dump-autoload

# Show installed packages
composer show
composer show --tree               # dependency tree

# Check for outdated packages
composer outdated

# Version constraints
# ^1.2   = >=1.2.0 <2.0.0  (caret - recommended)
# ~1.2   = >=1.2.0 <1.3.0  (tilde)
# 1.2.*  = >=1.2.0 <1.3.0  (wildcard)
# >=1.0  = any version >= 1.0
```

### PSR-4 autoloading

```php
<?php
// composer.json: "App\\": "app/"
// File location: app/Services/PaymentService.php

namespace App\Services;

class PaymentService {
    // Composer autoloader resolves this class automatically
}

// Usage anywhere:
use App\Services\PaymentService;
$service = new PaymentService();
```

### Global installation (CLI tools)

```bash
# Install Laravel installer globally
composer global require laravel/installer

# Create project with installer
laravel new my-app

# Global bin must be in PATH:
# Linux/Mac: ~/.composer/vendor/bin
# Windows: %APPDATA%/Composer/vendor/bin
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Class not found` after adding new class | Autoload map not updated | Run `composer dump-autoload` |
| Different behavior on dev vs prod | `composer.lock` not committed | Always commit `composer.lock` |
| `Your requirements could not be resolved` | Version conflict between packages | Check constraints with `composer why-not vendor/package version` |
| `require` uses dev dependency in production | Wrong section in `composer.json` | Move to `require-dev` and install with `--no-dev` in prod |
| Global tool conflicts with project | Different PHP version requirements | Use project-local tools via `vendor/bin/` |
| Slow autoloading in production | Class map not optimized | Use `composer install --optimize-autoloader` or `--classmap-authoritative` |

## See Also

- [[php-oop-fundamentals]] - namespaces and PSR-4 naming
- [[laravel-architecture]] - Laravel's Composer-based structure
- https://getcomposer.org/doc/
- https://www.php-fig.org/psr/psr-4/
- https://packagist.org/
