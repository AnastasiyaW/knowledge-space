---
title: PDO, Sessions, and Authentication
category: fundamentals
tags: [php, pdo, database, sessions, authentication, prepared-statements, password-hashing, file-upload]
---

# PDO, Sessions, and Authentication

PDO (PHP Data Objects) provides a consistent interface for database access with prepared statements to prevent SQL injection. Sessions store user state across requests via cookies. Authentication combines password hashing (`password_hash`/`password_verify`), session management, and CSRF protection. File uploads use `move_uploaded_file` with validation.

## Key Facts

- PDO supports MySQL, PostgreSQL, SQLite, etc. - same API, different DSN
- **Always use prepared statements** - `$stmt->execute([$param])` prevents SQL injection
- `password_hash($pass, PASSWORD_DEFAULT)` generates bcrypt hash (auto-salted)
- `password_verify($input, $hash)` checks against stored hash
- `$_SESSION` persists across requests after `session_start()`; flash messages = set + unset after display
- `move_uploaded_file()` validates temp path; always validate type/size before accepting

## Patterns

### PDO Database Wrapper

```php
class Database {
    private \PDO $pdo;

    public function __construct(string $host, string $db, string $user, string $pass) {
        $dsn = "mysql:host=$host;dbname=$db;charset=utf8mb4";
        $this->pdo = new \PDO($dsn, $user, $pass, [
            \PDO::ATTR_ERRMODE => \PDO::ERRMODE_EXCEPTION,
            \PDO::ATTR_DEFAULT_FETCH_MODE => \PDO::FETCH_ASSOC]);
    }

    public function query(string $sql, array $params = []): \PDOStatement {
        $stmt = $this->pdo->prepare($sql);
        $stmt->execute($params);
        return $stmt;
    }

    public function findOne(string $table, int $id): array|false {
        return $this->query("SELECT * FROM `$table` WHERE id = ?", [$id])->fetch();
    }

    public function lastInsertId(): string {
        return $this->pdo->lastInsertId();
    }
}
```

### Session and Flash Messages

```php
session_start();

// Flash messages (set in controller, display in view, auto-clear)
class Session {
    public function setFlash(string $key, string $message): void {
        $_SESSION['flash'][$key] = $message;
    }

    public function getFlash(string $key): ?string {
        $msg = $_SESSION['flash'][$key] ?? null;
        unset($_SESSION['flash'][$key]);
        return $msg;
    }
}
```

### Authentication

```php
// Registration
$hash = password_hash($password, PASSWORD_DEFAULT);
$db->query("INSERT INTO users (email, password) VALUES (?, ?)", [$email, $hash]);

// Login
$user = $db->query("SELECT * FROM users WHERE email = ?", [$email])->fetch();
if ($user && password_verify($password, $user['password'])) {
    $_SESSION['user_id'] = $user['id'];
    header('Location: /dashboard');
}

// Auth check helper
function isAuth(): bool { return isset($_SESSION['user_id']); }
function isAdmin(): bool { return ($_SESSION['role'] ?? '') === 'admin'; }
```

### File Upload

```php
function uploadFile(array $file): string {
    $ext = pathinfo($file['name'], PATHINFO_EXTENSION);
    $filename = uniqid() . '.' . $ext;
    $dir = 'uploads/' . date('Y/m/d');
    if (!is_dir($dir)) mkdir($dir, 0755, true);
    move_uploaded_file($file['tmp_name'], "$dir/$filename");
    return "/$dir/$filename";
}
```

## Gotchas

- Never store plain text passwords - always `password_hash()` with `PASSWORD_DEFAULT`
- `PDO::ERRMODE_EXCEPTION` is essential - without it, query failures return false silently
- `session_start()` must be called before any output (even whitespace)
- PHPMailer's `addAttachment()` needs filesystem path, not URL

## See Also

- [[php-type-system]] - type safety in database operations
- [[mvc-framework]] - Model/Database classes using PDO
- [[laravel-authentication]] - Laravel's auth scaffolding (built on same principles)
