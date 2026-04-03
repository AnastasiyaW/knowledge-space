---
title: Custom MVC Framework
category: patterns
tags: [php, mvc, router, controller, model, view, middleware, validation, pagination, framework]
---

# Custom MVC Framework

Building an MVC framework from scratch in PHP teaches core web architecture: Router dispatches URLs to Controller actions, Models handle database CRUD with validation, Views render templates with layouts. Adding middleware (auth guards), pagination, cache, and admin panels demonstrates real-world framework patterns that Laravel/Symfony implement at scale.

## Key Facts

- **Router**: maps URL patterns to controller#action; supports named routes, regex params (`{slug}`)
- **Controller**: receives request, delegates to Model, returns View; `$layout` property sets template
- **Model**: wraps database table, validates attributes, provides CRUD (find, save, update, delete)
- **View**: renders PHP templates with layout wrapping; `renderPartial` for AJAX/fragments
- **Middleware**: `only()` / `except()` methods restrict actions to authenticated users
- **Helpers**: global functions (`app()`, `view()`, `session()`, `old()`, `redirect()`)

## Patterns

### Router

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

### Controller with Layout

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

### Model with Validation

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

### View with Layouts

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

### Pagination

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

### Middleware (Auth Guard)

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

## Gotchas

- `old()` helper must be session-based (PRG pattern): store form data in session before redirect, read after
- `unique` validator on UPDATE must exclude current record: `WHERE field = ? AND id != ?`
- Layout resolution priority: explicit param > controller `$layout` > default
- Slug-based routing needs regex in Router to distinguish `/post/{slug}` from `/post/create`

## See Also

- [[php-oop-fundamentals]] - classes, namespaces, traits used throughout
- [[php-pdo-and-sessions]] - Database and Session classes
- [[laravel-architecture]] - how Laravel implements these patterns at scale
