---
title: "Fondamentaux de la POO en PHP"
category: concepts
tags: [php, oop, classes, inheritance, interfaces, traits, namespaces, autoloading, psr-4, abstract]
level: 2
source_sha256: 97abee949c45d687eca02cb41a6c18506dd81f2b1dbf8b4122417ec8c2b677cb
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux de la POO en PHP {#php-oop-fundamentals}

La POO en PHP 8.x couvre les classes, l'héritage, les interfaces, les classes abstraites, les traits, les espaces de noms et l'autoloading PSR-4. Tout est privé par défaut en PHP moderne. La promotion de constructeur (PHP 8) élimine le code répétitif. Les espaces de noms évitent les conflits de noms ; l'autoloader PSR-4 de Composer associe les espaces de noms à des répertoires.

## Points clés {#key-facts}

- Promotion de constructeur (PHP 8) : `public function __construct(private string $name)` - déclare et assigne
- Propriétés `readonly` (PHP 8.1) : définies une seule fois dans le constructeur, immuables ensuite
- Visibilité : `public`, `protected`, `private` - la valeur par défaut est `public` implicite pour les méthodes
- Une `abstract class` ne peut pas être instanciée ; une `interface` définit un contrat sans implémentation
- Un `trait` fournit une réutilisation horizontale de code (plusieurs traits par classe, résolution des conflits)
- Autoloading PSR-4 : l'espace de noms `App\Controllers` correspond au répertoire `app/Controllers/`

## Modèles {#patterns}

### Classe avec promotion de constructeur {#class-with-constructor-promotion}

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

### Héritage et classes abstraites {#inheritance-and-abstract-classes}

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

### Espaces de noms et autoloading {#namespaces-and-autoloading}

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

## Pièges {#gotchas}

- `static::method()` utilise le late static binding (résolu à l'exécution) ; `self::method()` est résolu à la définition
- Les traits dont les noms de méthodes entrent en conflit nécessitent une résolution explicite : `use A, B { A::method insteadof B; }`
- Le constructeur d'une classe enfant doit appeler `parent::__construct()` si le parent en définit un
- Les propriétés `readonly` ne peuvent pas être modifiées après leur affectation initiale, même par l'objet lui-même

## Voir aussi {#see-also}

- [[php-type-system]] - indications de type dans les propriétés et méthodes de classe
- [[mvc-framework]] - la POO appliquée à l'architecture MVC
- [[laravel-architecture]] - l'utilisation par Laravel des interfaces, du conteneur de services et des providers
