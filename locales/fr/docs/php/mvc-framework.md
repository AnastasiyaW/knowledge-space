---
title: "Framework MVC personnalisé"
category: patterns
tags: [php, mvc, router, controller, model, view, middleware, validation, pagination, framework]
level: 3
source_sha256: 3c679d40e7eaadbfed90c2b0fa349bd026f9f7073e9a69eefbd60393f6eb7e1c
translation: machine
translated_at: '2026-10-24'
---
# Framework MVC personnalisé {#custom-mvc-framework}

Construire un framework MVC à partir de zéro en PHP permet de comprendre l'architecture web de base : le Router dirige les URL vers les actions du Controller, les Models gèrent le CRUD en base de données avec validation, et les Views rendent des templates avec des layouts. L'ajout de middleware (gardes d'authentification), de pagination, de cache et de panneaux d'administration illustre les patterns de framework du monde réel que Laravel et Symfony implémentent à grande échelle.

## Points clés {#key-facts}

- **Router** : associe des patterns d'URL à controller#action ; prend en charge les routes nommées et les paramètres par expression régulière (`{slug}`)
- **Controller** : reçoit la requête, délègue au Model, retourne une View ; la propriété `$layout` définit le template
- **Model** : encapsule une table de base de données, valide les attributs, fournit le CRUD (find, save, update, delete)
- **View** : rend des templates PHP avec encapsulation dans un layout ; `renderPartial` pour les requêtes AJAX et les fragments
- **Middleware** : les méthodes `only()` / `except()` restreignent les actions aux utilisateurs authentifiés
- **Helpers** : fonctions globales (`app()`, `view()`, `session()`, `old()`, `redirect()`)

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

### Controller avec Layout {#controller-with-layout}

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

### Model avec validation {#model-with-validation}

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

### View avec Layouts {#view-with-layouts}

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

### Middleware (garde d'authentification) {#middleware-auth-guard}

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

## Pièges à éviter {#gotchas}

- Le helper `old()` doit reposer sur la session (pattern PRG) : stocker les données du formulaire en session avant la redirection, puis les lire après
- Le validateur `unique` lors d'un UPDATE doit exclure l'enregistrement courant : `WHERE field = ? AND id != ?`
- Ordre de résolution du layout : paramètre explicite > `$layout` du controller > valeur par défaut
- Le routage basé sur un slug nécessite une expression régulière dans le Router pour distinguer `/post/{slug}` de `/post/create`

## Voir aussi {#see-also}

- [[php-oop-fundamentals]] - classes, namespaces, traits utilisés partout
- [[php-pdo-and-sessions]] - classes Database et Session
- [[laravel-architecture]] - comment Laravel implémente ces patterns à grande échelle
