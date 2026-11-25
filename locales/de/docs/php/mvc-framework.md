---
title: "Eigenes MVC-Framework"
category: patterns
tags: [php, mvc, router, controller, model, view, middleware, validation, pagination, framework]
level: 3
source_sha256: 3c679d40e7eaadbfed90c2b0fa349bd026f9f7073e9a69eefbd60393f6eb7e1c
translation: machine
translated_at: '2026-10-24'
---
# Eigenes MVC-Framework {#custom-mvc-framework}

Der Aufbau eines MVC-Frameworks in PHP von Grund auf vermittelt grundlegende Web-Architektur: Der Router leitet URLs an Controller-Aktionen weiter, Models übernehmen CRUD-Operationen mit Validierung für die Datenbank, und Views rendern Templates mit Layouts. Middleware (Auth-Guards), Pagination, Caching und Admin-Panels zeigen reale Framework-Muster, wie sie Laravel und Symfony im großen Maßstab umsetzen.

## Key Facts {#key-facts}

- **Router**: ordnet URL-Muster Controller#Aktion zu; unterstützt benannte Routen und Regex-Parameter (`{slug}`)
- **Controller**: nimmt die Anfrage entgegen, delegiert an das Model und gibt eine View zurück; die Eigenschaft `$layout` legt das Template fest
- **Model**: kapselt eine Datenbanktabelle, validiert Attribute und stellt CRUD-Operationen bereit (find, save, update, delete)
- **View**: rendert PHP-Templates mit Layout-Umschluss; `renderPartial` für AJAX/Fragmente
- **Middleware**: die Methoden `only()` / `except()` beschränken Aktionen auf authentifizierte Benutzer
- **Helpers**: globale Funktionen (`app()`, `view()`, `session()`, `old()`, `redirect()`)

## Patterns {#patterns}

### Router {#router}

```php
class Router {
    protected array $routes = [];

    public function get(string $path, array|callable $callback): self {
        $this->routes['GET'][$path] = ['callback' => $callback];
        return $this;
    }

    public function post(string $path, array|callable $callback): self {
        $this->routes['POST'][$path] = ['callback' => $callback];
        return $this;
    }

    protected function dispatch(): void {
        $uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
        $method = $_SERVER['REQUEST_METHOD'];
        $route = $this->matchRoute($uri, $method);

        [$class, $action] = $route['callback'];
        $controller = new $class();
        app()->layout = $controller->layout ?? LAYOUT_DEFAULT;
        echo $controller->$action();
    }
}
```

### Controller with Layout {#controller-with-layout}

```php
abstract class Controller {
    public string $layout = LAYOUT_DEFAULT;

    protected function render(string $view, array $data = []): string {
        return app()->view->render($view, $data, $this->layout);
    }
}

// Admin controllers override layout
class AdminBaseController extends Controller {
    public string $layout = 'admin';

    public function __construct() {
        if (!isAdmin()) { abort('Forbidden', 403); }
    }
}
```

### Model with Validation {#model-with-validation}

```php
abstract class Model {
    public string $table;
    public array $attributes = [];
    public array $errors = [];
    public array $rules = [];

    public function validate(): bool {
        foreach ($this->rules as $field => $fieldRules) {
            foreach ($fieldRules as $rule) {
                // Rules: required, min:3, max:255, email, unique:users, match:password
                $this->applyRule($field, $rule);
            }
        }
        return empty($this->errors);
    }

    public function save(): int|false {
        $fields = implode(', ', array_keys($this->attributes));
        $placeholders = implode(', ', array_fill(0, count($this->attributes), '?'));
        db()->query(
            "INSERT INTO {$this->table} ($fields) VALUES ($placeholders)",
            array_values($this->attributes)
        );
        return db()->lastInsertId();
    }

    public function update(int $id): bool {
        $set = implode(', ', array_map(fn($k) => "$k = ?", array_keys($this->attributes)));
        return db()->query(
            "UPDATE {$this->table} SET $set WHERE id = ?",
            [...array_values($this->attributes), $id]
        );
    }
}
```

### View with Layouts {#view-with-layouts}

```php
class View {
    public function render(string $view, array $data = [], string $layout = ''): string {
        extract($data);
        ob_start();
        require "views/$view.php";
        $content = ob_get_clean();

        if ($layout) {
            ob_start();
            require "views/layouts/$layout.php";  // uses $content
            return ob_get_clean();
        }
        return $content;
    }
}
```

### Pagination {#pagination}

```php
class Pagination {
    public int $page;
    public int $perPage;
    public int $total;

    public function __construct(int $page, int $perPage, int $total) {
        $this->page = max(1, $page);
        $this->perPage = $perPage;
        $this->total = $total;
    }

    public function getOffset(): int { return ($this->page - 1) * $this->perPage; }
    public function getTotalPages(): int { return (int)ceil($this->total / $this->perPage); }
}
```

### Middleware (Auth Guard) {#middleware-auth-guard}

```php
trait AuthMiddleware {
    protected array $onlyAuth = [];
    protected array $exceptAuth = [];

    protected function checkAuth(string $action): void {
        if (!empty($this->onlyAuth) && in_array($action, $this->onlyAuth) && !isAuth()) {
            redirect('/login');
        }
    }
}
```

## Gotchas {#gotchas}

- Der Helper `old()` muss sessionbasiert arbeiten (PRG-Muster): Formulardaten vor dem Redirect in der Session speichern und danach auslesen
- Der Validator `unique` muss beim UPDATE den aktuellen Datensatz ausschließen: `WHERE field = ? AND id != ?`
- Priorität der Layout-Auflösung: expliziter Parameter > Controller-`$layout` > Standard
- Slug-basiertes Routing benötigt Regex im Router, um `/post/{slug}` von `/post/create` zu unterscheiden

## See Also {#see-also}

- [[php-oop-fundamentals]] - Klassen, Namespaces, Traits, die durchgehend verwendet werden
- [[php-pdo-and-sessions]] - Database- und Session-Klassen
- [[laravel-architecture]] - wie Laravel diese Muster im großen Maßstab umsetzt
