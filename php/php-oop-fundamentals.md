---
title: PHP OOP Fundamentals
category: concepts
tags: [php, oop, classes, inheritance, interfaces, traits, namespaces, abstract]
---

# PHP OOP Fundamentals

Object-oriented programming in PHP 8.x covers classes, inheritance, interfaces, traits, abstract classes, namespaces, and autoloading. PHP's OOP model is the foundation of every modern framework including [[laravel-architecture]] and is required for understanding [[laravel-eloquent-orm]] models, controllers, middleware, and service providers.

## Key Facts

- Classes define properties (attributes) and methods (functions)
- Visibility: `public` (anywhere), `protected` (class + children), `private` (class only)
- Constructor promotion (PHP 8.0+): `public function __construct(private string $name)` declares + assigns in one line
- `readonly` properties (PHP 8.1+): can only be assigned once (in constructor)
- Interfaces define method contracts; a class can implement multiple interfaces
- Abstract classes cannot be instantiated; mix of implemented and abstract methods
- Traits provide horizontal code reuse (methods injected into classes via `use`)
- Enums (PHP 8.1+): `enum Status: string { case Active = 'active'; }`
- Namespaces prevent name collisions; follow PSR-4 autoloading convention
- `$this` refers to current object; `self::` refers to defining class; `static::` uses late static binding
- `::class` constant returns fully qualified class name as string

## Patterns

### Class with constructor promotion

```php
<?php
class User {
    public function __construct(
        private readonly int $id,
        private string $name,
        private string $email,
        private string $role = 'user',
    ) {}

    public function isAdmin(): bool {
        return $this->role === 'admin';
    }

    public function getName(): string {
        return $this->name;
    }
}

$user = new User(id: 1, name: 'Admin', email: 'admin@mail.com', role: 'admin');
```

### Inheritance and abstract classes

```php
<?php
abstract class Model {
    protected string $table;

    abstract public function find(int $id): ?static;

    public function getTable(): string {
        return $this->table;
    }
}

class User extends Model {
    protected string $table = 'users';

    public function find(int $id): ?static {
        // query database
        return $this;
    }
}
```

### Interfaces

```php
<?php
interface Authenticatable {
    public function getAuthIdentifier(): int;
    public function getPassword(): string;
}

interface HasRoles {
    public function hasRole(string $role): bool;
}

// A class can implement multiple interfaces
class User implements Authenticatable, HasRoles {
    public function getAuthIdentifier(): int { return $this->id; }
    public function getPassword(): string { return $this->password; }
    public function hasRole(string $role): bool { return $this->role === $role; }
}
```

### Traits

```php
<?php
trait HasTimestamps {
    public ?string $createdAt = null;
    public ?string $updatedAt = null;

    public function setTimestamps(): void {
        $now = date('Y-m-d H:i:s');
        $this->createdAt ??= $now;
        $this->updatedAt = $now;
    }
}

trait SoftDeletes {
    public ?string $deletedAt = null;

    public function softDelete(): void {
        $this->deletedAt = date('Y-m-d H:i:s');
    }

    public function isDeleted(): bool {
        return $this->deletedAt !== null;
    }
}

class Post {
    use HasTimestamps, SoftDeletes;
}
```

### Namespaces and autoloading

```php
<?php
// File: app/Models/User.php
namespace App\Models;

use App\Contracts\Authenticatable;

class User implements Authenticatable {
    // ...
}

// Usage in another file
use App\Models\User;
$user = new User();

// PSR-4 autoloading in composer.json:
// "autoload": { "psr-4": { "App\\": "app/" } }
```

### Enums (PHP 8.1+)

```php
<?php
enum Status: string {
    case Draft     = 'draft';
    case Published = 'published';
    case Archived  = 'archived';

    public function label(): string {
        return match($this) {
            self::Draft     => 'Draft',
            self::Published => 'Published',
            self::Archived  => 'Archived',
        };
    }
}

// Usage
$status = Status::Published;
echo $status->value; // 'published'
$fromDb = Status::from('draft'); // Status::Draft
$maybe = Status::tryFrom('invalid'); // null (no exception)
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `self::method()` doesn't call child override | `self::` binds at compile time | Use `static::` for late static binding |
| Trait method conflict | Two traits define same method | Use `insteadof` and `as` to resolve: `A::method insteadof B` |
| `Cannot access private property` | Accessing parent's `private` from child | Change to `protected` for inheritance access |
| Namespace import not working | Missing `use` statement or wrong path | Check PSR-4 mapping in `composer.json`, run `composer dump-autoload` |
| `readonly` property cannot be reset | By design - assigned once in constructor | Remove `readonly` if property needs to change |
| Circular dependency in constructor | Class A needs B, B needs A | Refactor to use interface or setter injection |

## See Also

- [[laravel-architecture]] - how Laravel uses OOP patterns (service container, facades)
- [[composer-and-autoloading]] - PSR-4 autoloading, dependency management
- https://www.php.net/manual/en/language.oop5.php
- https://www.php.net/manual/en/language.namespaces.php
- https://www.php.net/manual/en/language.enumerations.php
