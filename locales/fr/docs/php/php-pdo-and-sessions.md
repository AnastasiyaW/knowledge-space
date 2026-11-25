---
title: "PDO, sessions et authentification"
category: fundamentals
tags: [php, pdo, database, sessions, authentication, prepared-statements, password-hashing, file-upload]
level: 3
source_sha256: b36d5922679c74b7c501128090e84932065f6b8dbd5aee8e66ba0210f7ca45a1
translation: machine
translated_at: '2026-10-24'
---
# PDO, sessions et authentification {#pdo-sessions-and-authentication}

PDO (PHP Data Objects) fournit une interface cohérente pour l'accès aux bases de données, avec des requêtes préparées pour prévenir les injections SQL. Les sessions conservent l'état de l'utilisateur d'une requête à l'autre grâce à des cookies. L'authentification combine le hachage de mots de passe (`password_hash`/`password_verify`), la gestion des sessions et la protection CSRF. Les envois de fichiers utilisent `move_uploaded_file` avec validation.

## Points clés {#key-facts}

- PDO prend en charge MySQL, PostgreSQL, SQLite, etc. - même API, DSN différent
- **Toujours utiliser des requêtes préparées** - `$stmt->execute([$param])` prévient les injections SQL
- `password_hash($pass, PASSWORD_DEFAULT)` génère un hash bcrypt (salé automatiquement)
- `password_verify($input, $hash)` vérifie la valeur saisie par rapport au hash stocké
- `$_SESSION` persiste d'une requête à l'autre après `session_start()` ; les messages flash = affectation puis suppression après affichage
- `move_uploaded_file()` valide le chemin temporaire ; toujours valider le type et la taille avant d'accepter un fichier

## Modèles {#patterns}

### Wrapper de base de données PDO {#pdo-database-wrapper}

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

### Session et messages flash {#session-and-flash-messages}

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

### Authentification {#authentication}

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

### Envoi de fichier {#file-upload}

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

## Pièges {#gotchas}

- Ne jamais stocker les mots de passe en clair - toujours utiliser `password_hash()` avec `PASSWORD_DEFAULT`
- `PDO::ERRMODE_EXCEPTION` est indispensable : sans lui, les échecs de requête renvoient silencieusement false
- `session_start()` doit être appelé avant toute sortie (même un simple espace blanc)
- `addAttachment()` de PHPMailer attend un chemin système de fichiers, et non une URL

## Voir aussi {#see-also}

- [[php-type-system]] - sûreté de typage dans les opérations de base de données
- [[mvc-framework]] - classes Model/Database utilisant PDO
- [[laravel-authentication]] - le socle d'authentification de Laravel (construit sur les mêmes principes)
