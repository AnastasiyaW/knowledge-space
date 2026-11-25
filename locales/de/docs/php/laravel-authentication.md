---
title: "Laravel-Authentifizierung"
category: framework
tags: [laravel, auth, login, password, hashing, guards, throttle]
level: 3
source_sha256: 62f0cbfcb1f19cc3dabc93bc6008f720c5e09d49fe5a11feec631631011155e5
translation: machine
translated_at: '2026-10-24'
---
# Laravel-Authentifizierung {#laravel-authentication}

Laravel bietet eine integrierte Authentifizierung über die `Auth`-Facade bzw. den `auth()`-Helper. Sie unterstützt manuellen Login, sessionbasierte Authentifizierung, Remember-me-Tokens und Passwort-Hashing. Authentifizierung prüft die Identität eines Benutzers, Autorisierung (Policies/Gates) prüft Berechtigungen. Geschützt wird über [[laravel-middleware]], und die Authentifizierung arbeitet mit dem User-Modell aus [[laravel-eloquent-orm]].

## Key Facts {#key-facts}

- `Auth`-Facade und `auth()`-Helper bieten identische Funktionalität
- `Auth::attempt(['email' => $e, 'password' => $p])` - prüft die Zugangsdaten und meldet an (gibt bool zurück)
- `Auth::check()` - gibt true zurück, wenn der Benutzer authentifiziert ist
- `Auth::user()` - gibt die Instanz des authentifizierten User-Modells zurück (oder null)
- `Auth::logout()` - meldet den aktuellen Benutzer ab
- Passwörter werden automatisch mit bcrypt gehasht, über `Hash::make()` oder den `bcrypt()`-Helper
- `Auth::attempt()` vergleicht das gehashte Passwort automatisch - niemals Klartext vergleichen
- Zusätzliche Bedingungen können an `attempt()` übergeben werden: `['email' => $e, 'password' => $p, 'active' => 1]`
- Remember-me: `Auth::attempt($credentials, $remember)` - der zweite Parameter ist ein Boolean
- Die Regenerierung der Session nach dem Login verhindert Session-Fixation-Angriffe
- Rate Limiting (Throttle-Middleware) schützt vor Brute-Force-Angriffen
- Laravel bietet Starter-Kits (Breeze, Jetstream, Fortify), manuelle Authentifizierung ist für das Lernen aber übersichtlicher

## Patterns {#patterns}

### Manueller Authentifizierungsablauf {#manual-authentication-flow}

```php
<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class UserController extends Controller
{
    // Show login form
    public function loginForm()
    {
        return view('user.login');
    }

    // Handle login attempt
    public function authenticate(Request $request)
    {
        $credentials = $request->validate([
            'email'    => ['required', 'email'],
            'password' => ['required']]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate(); // prevent session fixation
            return redirect()->intended('admin'); // go to intended URL or fallback
        }

        return back()->with('error', 'Incorrect email or password.');
    }

    // Logout
    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/');
    }
}
```

### Routen für die Authentifizierung {#routes-for-auth}

```php
<?php
use App\Http\Controllers\UserController;

// Login routes - guest middleware (only for non-authenticated users)
Route::middleware('guest')->group(function () {
    Route::get('/login', [UserController::class, 'loginForm'])->name('login');
    Route::post('/login', [UserController::class, 'authenticate'])->name('login.authenticate');
});

// Logout - auth middleware (only for authenticated users)
Route::post('/logout', [UserController::class, 'logout'])
    ->middleware('auth')
    ->name('logout');

// Protected admin routes
Route::middleware(['auth', 'admin'])->prefix('admin')->group(function () {
    Route::get('/', [AdminController::class, 'index'])->name('admin.main.index');
});
```

### Login-Formular (Blade) {#login-form-blade}

```html
<form method="POST" action="{{ route('login.authenticate') }}">
    @csrf

    {{-- Validation errors --}}
    @if ($errors->any())
        <div class="alert alert-danger">
            <ul class="list-unstyled mb-0">
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    {{-- Flash error message (from Auth::attempt failure) --}}
    @if (session('error'))
        <div class="alert alert-danger">{{ session('error') }}</div>
    @endif

    <input type="email" name="email" value="{{ old('email') }}" required>
    <input type="password" name="password" required>
    <button type="submit">Sign In</button>
</form>
```

### Benutzer programmatisch anlegen {#creating-users-programmatically}

```php
<?php
use App\Models\User;
use Illuminate\Support\Facades\Hash;

// Create a user (e.g., in a seeder or controller)
User::create([
    'name'     => 'Admin',
    'email'    => 'admin@mail.com',
    'password' => Hash::make('securePassword123'), // auto-hashed
]);

// Or using bcrypt helper
User::create([
    'name'     => 'Admin',
    'email'    => 'admin@mail.com',
    'password' => bcrypt('securePassword123')]);
```

### Admin-Rollenprüfung mit eigener Middleware {#admin-role-check-with-custom-middleware}

```php
<?php
// Add 'role' column to users table migration
Schema::table('users', function (Blueprint $table) {
    $table->tinyInteger('role')->default(0); // 0 = user, 1 = admin
});

// Model method
class User extends Authenticatable
{
    public function isAdmin(): bool
    {
        return $this->role === 1;
    }
}

// AdminMiddleware
class AdminMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        if (!auth()->user()?->isAdmin()) {
            abort(403);
        }
        return $next($request);
    }
}
```

## Gotchas {#gotchas}

| Symptom | Ursache | Lösung |
|---------|-------|-----|
| `Route [login] not defined` | Keine Route mit dem Namen `login` vorhanden | Route mit `->name('login')` anlegen |
| Passwortprüfung schlägt immer fehl | Passwort als Klartext gespeichert, nicht gehasht | `Hash::make()` beim Anlegen des Benutzers verwenden |
| Angemeldeter Benutzer kann die Login-Seite aufrufen | Login-Routen ohne `guest`-Middleware | `->middleware('guest')` zu den Login-Routen hinzufügen |
| Session-Fixation-Schwachstelle | Session wird nach dem Login nicht regeneriert | `$request->session()->regenerate()` nach `attempt()` aufrufen |
| Brute-Force-Angriffe | Kein Rate Limiting beim Login | `throttle`-Middleware auf die Login-Route anwenden |
| Passwortlänge/-regeln beim Login nicht validieren | Verrät Angreifern die Passwortrichtlinie | Beim Login nur `required` validieren, vollständige Regeln bei der Registrierung |
| `Auth::user()` gibt im Konstruktor `null` zurück | Der Controller-Konstruktor läuft vor der Middleware | `$this->middleware()` verwenden oder `auth()` in Methoden aufrufen |

## See Also {#see-also}

- [[laravel-middleware]] - Auth- und Guest-Middleware
- [[laravel-routing]] - Muster für den Routenschutz
- [[laravel-validation]] - Formularvalidierung für Login und Registrierung
- https://laravel.com/docs/11.x/authentication
- https://laravel.com/docs/11.x/hashing
