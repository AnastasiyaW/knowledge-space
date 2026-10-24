---
title: "PHP-OOP-Grundlagen"
category: concepts
tags: [php, oop, classes, inheritance, interfaces, traits, namespaces, autoloading, psr-4, abstract]
level: 2
source_sha256: 97abee949c45d687eca02cb41a6c18506dd81f2b1dbf8b4122417ec8c2b677cb
translation: machine
translated_at: '2026-10-24'
---
Wait, I need to output the translation, not this. Let me produce it.

---
title: PHP-OOP-Grundlagen
category: concepts
tags: [php, oop, classes, inheritance, interfaces, traits, namespaces, autoloading, psr-4, abstract]
---

# PHP-OOP-Grundlagen {#php-oop-fundamentals}

PHP 8.x-OOP umfasst Klassen, Vererbung, Interfaces, abstrakte Klassen, Traits, Namespaces und PSR-4-Autoloading. In modernem PHP sind alle Elemente standardmäßig private. Constructor Promotion (PHP 8) eliminiert Boilerplate-Code. Namespaces verhindern Namenskonflikte; der PSR-4-Autoloader von Composer ordnet Namespaces Verzeichnissen zu.

## Key Facts {#key-facts}

- Constructor Promotion (PHP 8): `public function __construct(private string $name)` - deklariert und weist zu
- `readonly`-Properties (PHP 8.1): werden einmal im Konstruktor gesetzt und sind danach unveränderlich
- Sichtbarkeit: `public`, `protected`, `private` - Standard ist bei Methoden implizit public
- `abstract class` kann nicht instanziiert werden; ein `interface` definiert einen Vertrag ohne Implementierung
- `trait` ermöglicht horizontale Code-Wiederverwendung (mehrere Traits pro Klasse, löst Konflikte auf)
- PSR-4-Autoloading: der Namespace `App\Controllers` entspricht dem Verzeichnis `app/Controllers/`

## Patterns {#patterns}

### Class with Constructor Promotion {#class-with-constructor-promotion}

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

### Inheritance and Abstract Classes {#inheritance-and-abstract-classes}

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

### Interfaces {#interfaces}

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

### Traits {#traits}

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

### Namespaces and Autoloading {#namespaces-and-autoloading}

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

## Gotchas {#gotchas}

- `static::method()` verwendet Late Static Binding (wird zur Laufzeit aufgelöst); `self::method()` wird zur Definitionszeit aufgelöst
- Traits mit kollidierenden Methodennamen benötigen eine explizite Auflösung: `use A, B { A::method insteadof B; }`
- Der Konstruktor einer Kindklasse muss `parent::__construct()` aufrufen, wenn die Elternklasse einen Konstruktor definiert
- `readonly`-Properties können nach der initialen Zuweisung nicht mehr verändert werden - auch nicht vom Objekt selbst

## See Also {#see-also}

- [[php-type-system]] - Typhinweise in Klassen-Properties und Methoden
- [[mvc-framework]] - OOP angewendet auf die MVC-Architektur
- [[laravel-architecture]] - Laravels Einsatz von Interfaces, Service Container und Providern
