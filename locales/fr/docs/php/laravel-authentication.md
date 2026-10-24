---
title: "Authentification Laravel"
category: framework
tags: [laravel, auth, login, password, hashing, guards, throttle]
level: 3
source_sha256: 62f0cbfcb1f19cc3dabc93bc6008f720c5e09d49fe5a11feec631631011155e5
translation: machine
translated_at: '2026-10-24'
---
# Authentification Laravel {#laravel-authentication}

Laravel fournit une authentification intégrée via la façade/fonction d'aide `Auth`, prenant en charge la connexion manuelle, l'authentification basée sur la session, les jetons « se souvenir de moi » et le hachage des mots de passe. L'authentification vérifie l'identité de l'utilisateur ; l'autorisation (policies/gates) vérifie les permissions. Protégée par [[laravel-middleware]] et utilisant le modèle User de [[laravel-eloquent-orm]].

## Points clés {#key-facts}

- La façade `Auth` et la fonction d'aide `auth()` offrent des fonctionnalités identiques
- `Auth::attempt(['email' => $e, 'password' => $p])` - vérifie les identifiants et connecte l'utilisateur (renvoie un booléen)
- `Auth::check()` - renvoie true si l'utilisateur est authentifié
- `Auth::user()` - renvoie l'instance du modèle User authentifié (ou null)
- `Auth::logout()` - déconnecte l'utilisateur courant
- Les mots de passe sont automatiquement hachés avec bcrypt via `Hash::make()` ou la fonction d'aide `bcrypt()`
- `Auth::attempt()` compare automatiquement le mot de passe haché - ne comparez jamais de texte en clair
- Des conditions supplémentaires peuvent être passées à `attempt()` : `['email' => $e, 'password' => $p, 'active' => 1]`
- Se souvenir de moi : `Auth::attempt($credentials, $remember)` - le second paramètre est un booléen
- La régénération de la session après connexion prévient les attaques par fixation de session
- La limitation de débit (middleware throttle) protège contre les attaques par force brute
- Laravel propose des starter kits (Breeze, Jetstream, Fortify), mais l'authentification manuelle est plus claire pour l'apprentissage

## Modèles {#patterns}

### Flux d'authentification manuelle {#manual-authentication-flow}

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

### Routes d'authentification {#routes-for-auth}

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

### Formulaire de connexion (Blade) {#login-form-blade}

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

### Création d'utilisateurs par programmation {#creating-users-programmatically}

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

### Vérification du rôle administrateur avec un middleware personnalisé {#admin-role-check-with-custom-middleware}

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

## Pièges {#gotchas}

| Symptôme | Cause | Solution |
|---------|-------|-----|
| `Route [login] not defined` | Aucune route nommée `login` n'existe | Créer la route avec `->name('login')` |
| La vérification du mot de passe échoue toujours | Mot de passe stocké en clair, non haché | Utiliser `Hash::make()` lors de la création de l'utilisateur |
| L'utilisateur connecté peut accéder à la page de connexion | Les routes de connexion n'ont pas le middleware `guest` | Ajouter `->middleware('guest')` aux routes de connexion |
| Vulnérabilité par fixation de session | Session non régénérée après connexion | Appeler `$request->session()->regenerate()` après `attempt()` |
| Attaques par force brute | Pas de limitation de débit sur la connexion | Appliquer le middleware `throttle` à la route de connexion |
| Ne pas valider la longueur/les règles du mot de passe à la connexion | Révèle la politique de mots de passe aux attaquants | Valider uniquement `required` à la connexion ; règles complètes à l'inscription |
| `Auth::user()` renvoie null dans le constructeur | Le constructeur du contrôleur s'exécute avant le middleware | Utiliser `$this->middleware()` ou accéder à `auth()` dans les méthodes |

## Voir aussi {#see-also}

- [[laravel-middleware]] - middleware auth et guest
- [[laravel-routing]] - schémas de protection des routes
- [[laravel-validation]] - validation des formulaires de connexion et d'inscription
- https://laravel.com/docs/11.x/authentication
- https://laravel.com/docs/11.x/hashing
