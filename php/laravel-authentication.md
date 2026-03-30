---
title: Laravel Authentication
category: framework
tags: [laravel, auth, login, password, hashing, guards, throttle]
---

# Laravel Authentication

Laravel provides built-in authentication via the `Auth` facade/helper, supporting manual login, session-based auth, remember-me tokens, and password hashing. Authentication verifies user identity; authorization (policies/gates) verifies permissions. Protected by [[laravel-middleware]] and working with [[laravel-eloquent-orm]] User model.

## Key Facts

- `Auth` facade and `auth()` helper provide identical functionality
- `Auth::attempt(['email' => $e, 'password' => $p])` - checks credentials and logs in (returns bool)
- `Auth::check()` - returns true if user is authenticated
- `Auth::user()` - returns authenticated User model instance (or null)
- `Auth::logout()` - logs out the current user
- Passwords are automatically hashed with bcrypt via `Hash::make()` or `bcrypt()` helper
- `Auth::attempt()` automatically compares hashed password - never compare plain text
- Extra conditions can be passed to `attempt()`: `['email' => $e, 'password' => $p, 'active' => 1]`
- Remember-me: `Auth::attempt($credentials, $remember)` - second param is boolean
- Session regeneration after login prevents session fixation attacks
- Rate limiting (throttle middleware) protects against brute force attacks
- Laravel offers starter kits (Breeze, Jetstream, Fortify) but manual auth is cleaner for learning

## Patterns

### Manual authentication flow

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
            'password' => ['required'],
        ]);

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

### Routes for auth

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

### Login form (Blade)

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

### Creating users programmatically

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
    'password' => bcrypt('securePassword123'),
]);
```

### Admin role check with custom middleware

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

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Route [login] not defined` | No route named `login` exists | Create route with `->name('login')` |
| Password check always fails | Password stored as plain text, not hashed | Use `Hash::make()` when creating user |
| Logged-in user can access login page | Login route missing `guest` middleware | Add `->middleware('guest')` to login routes |
| Session fixation vulnerability | Not regenerating session after login | Call `$request->session()->regenerate()` after `attempt()` |
| Brute force attacks | No rate limiting on login | Apply `throttle` middleware to login route |
| Don't validate password length/rules on login | Reveals password policy to attackers | Only validate `required` on login; full rules on registration |
| `Auth::user()` returns null in constructor | Controller constructor runs before middleware | Use `$this->middleware()` or access `auth()` in methods |

## See Also

- [[laravel-middleware]] - auth and guest middleware
- [[laravel-routing]] - route protection patterns
- [[laravel-validation]] - form validation for login/registration
- https://laravel.com/docs/11.x/authentication
- https://laravel.com/docs/11.x/hashing
