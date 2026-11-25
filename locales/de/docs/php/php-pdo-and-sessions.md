---
title: "PDO, Sitzungen und Authentifizierung"
category: fundamentals
tags: [php, pdo, database, sessions, authentication, prepared-statements, password-hashing, file-upload]
level: 3
source_sha256: b36d5922679c74b7c501128090e84932065f6b8dbd5aee8e66ba0210f7ca45a1
translation: machine
translated_at: '2026-10-24'
---
# PDO, Sitzungen und Authentifizierung {#pdo-sessions-and-authentication}

PDO (PHP Data Objects) bietet eine einheitliche Schnittstelle für den Datenbankzugriff mit Prepared Statements, die SQL-Injection verhindern. Sitzungen speichern den Benutzerstatus über Requests hinweg mithilfe von Cookies. Die Authentifizierung kombiniert Passwort-Hashing (`password_hash`/`password_verify`), Sitzungsverwaltung und CSRF-Schutz. Datei-Uploads verwenden `move_uploaded_file` mit Validierung.

## Key Facts {#key-facts}

- PDO unterstützt MySQL, PostgreSQL, SQLite usw. - gleiche API, unterschiedlicher DSN
- **Immer Prepared Statements verwenden** - `$stmt->execute([$param])` verhindert SQL-Injection
- `password_hash($pass, PASSWORD_DEFAULT)` erzeugt einen bcrypt-Hash (automatisch gesalzen)
- `password_verify($input, $hash)` prüft die Eingabe gegen den gespeicherten Hash
- `$_SESSION` bleibt nach `session_start()` über Requests hinweg erhalten; Flash-Messages = setzen + nach der Anzeige entfernen
- `move_uploaded_file()` validiert den temporären Pfad; Typ und Größe immer vor der Annahme prüfen

## Patterns {#patterns}

### PDO Database Wrapper {#pdo-database-wrapper}

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

### Session and Flash Messages {#session-and-flash-messages}

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

### Authentication {#authentication}

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

### File Upload {#file-upload}

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

## Gotchas {#gotchas}

- Niemals Klartext-Passwörter speichern - immer `password_hash()` mit `PASSWORD_DEFAULT` verwenden
- `PDO::ERRMODE_EXCEPTION` ist unverzichtbar - ohne diesen Modus liefern fehlgeschlagene Abfragen stillschweigend `false`
- `session_start()` muss vor jeglicher Ausgabe aufgerufen werden (auch vor Leerzeichen)
- PHPMailers `addAttachment()` benötigt einen Dateisystempfad, keine URL

## See Also {#see-also}

- [[php-type-system]] - Typsicherheit bei Datenbankoperationen
- [[mvc-framework]] - Model-/Database-Klassen, die PDO verwenden
- [[laravel-authentication]] - Laravels Auth-Grundgerüst (basiert auf denselben Prinzipien)
