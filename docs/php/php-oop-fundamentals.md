---
title: PHP OOP Fundamentals
category: concepts
tags: [php, oop, classes, inheritance, interfaces, traits, namespaces, autoloading, psr-4, abstract]
---

# PHP OOP Fundamentals

PHP 8.x OOP covers classes, inheritance, interfaces, abstract classes, traits, namespaces, and PSR-4 autoloading. Everything is private by default in modern PHP. Constructor promotion (PHP 8) eliminates boilerplate. Namespaces prevent naming conflicts; Composer's PSR-4 autoloader maps namespaces to directories.

## Key Facts

- Constructor promotion (PHP 8): `public function __construct(private string $name)` - declares + assigns
- `readonly` properties (PHP 8.1): set once in constructor, immutable after
- Visibility: `public`, `protected`, `private` - default is implicit public for methods
- `abstract class` cannot be instantiated; `interface` defines contract with no implementation
- `trait` provides horizontal code reuse (multiple traits per class, resolves conflicts)
- PSR-4 autoloading: namespace `App\Controllers` maps to `app/Controllers/` directory

## Patterns

### Class with Constructor Promotion

```php
class User {
    public function __construct(
        private readonly string $name,
        private string $email,
        private string $role = 'user',
    ) {}

    public function getName(): string { return $this->name; }
    public function getRole(): string { return $this->role; }
}
```

### Inheritance and Abstract Classes

```php
abstract class Shape {
    abstract public function area(): float;

    public function describe(): string {
        return static::class . ": area = " . $this->area();
    }
}

class Circle extends Shape {
    public function __construct(private float $radius) {}
    public function area(): float { return M_PI * $this->radius ** 2; }
}
```

### Interfaces

```php
interface Renderable {
    public function render(): string;
}

interface Cacheable {
    public function getCacheKey(): string;
    public function getCacheTtl(): int;
}

class Widget implements Renderable, Cacheable {
    public function render(): string { return '<div>Widget</div>'; }
    public function getCacheKey(): string { return 'widget_' . $this->id; }
    public function getCacheTtl(): int { return 3600; }
}
```

### Traits

```php
trait Timestampable {
    public ?string $created_at = null;
    public ?string $updated_at = null;

    public function touch(): void {
        $this->updated_at = date('Y-m-d H:i:s');
    }
}

class Post {
    use Timestampable;
}
```

### Namespaces and Autoloading

```php
// src/Controllers/UserController.php
namespace App\Controllers;

use App\Models\User;

class UserController {
    public function index(): array {
        return User::all();
    }
}
```

```json
// composer.json
{
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    }
}
```

## Gotchas

- `static::method()` uses late static binding (resolves at runtime); `self::method()` resolves at definition time
- Traits with conflicting method names need explicit resolution: `use A, B { A::method insteadof B; }`
- Constructor in child must call `parent::__construct()` if parent defines one
- `readonly` properties cannot be modified after initial assignment - even by the object itself

## See Also

- [[php-type-system]] - type hints in class properties and methods
- [[mvc-framework]] - OOP applied to MVC architecture
- [[laravel-architecture]] - Laravel's use of interfaces, service container, providers
