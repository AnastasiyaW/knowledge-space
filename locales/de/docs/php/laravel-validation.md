---
title: "Laravel-Validierung"
category: framework
tags: [laravel, validation, form-requests, rules, error-messages]
level: 3
source_sha256: 223a25f3de082d523e0b0d9b8256f50deb0d1afb616924676f0a61580e409abf
translation: machine
translated_at: '2026-10-24'
---
# Laravel-Validierung {#laravel-validation}

Laravel bietet eine integrierte Request-Validierung mit über 90 Regeln, automatische Weiterleitung zurück bei Fehlern und Flash-Fehlermeldungen. Die Validierung kann inline in Controllern erfolgen oder in Form-Request-Klassen ausgelagert werden. Validierte Daten sind sicher für Operationen mit [[laravel-eloquent-orm]]. Fehler werden in [[laravel-blade-templates]] über `$errors` und `@error` angezeigt.

## Wichtige Fakten {#key-facts}

- `$request->validate([...])` gibt ein Array mit validierten Daten zurück; bei Fehlern erfolgt automatisch eine Weiterleitung zurück mit den Fehlern
- Validierungsregeln als String (`'required|email|max:255'`) oder als Array (`['required', 'email', 'max:255']`)
- Die Variable `$errors` ist in Blade-Templates immer verfügbar (auch wenn sie leer ist)
- `old('field')` ruft die vorherige Eingabe nach einem Validierungsfehler ab
- Form-Request-Klassen: Validierungslogik in eine eigene `Request`-Unterklasse auslagern
- `php artisan make:request StorePostRequest` erzeugt eine Form-Request-Klasse
- Eigene Fehlermeldungen über den dritten Parameter oder die Methode `messages()` der Form-Request-Klasse
- Lokalisierung: Validierungsmeldungen in `lang/en/validation.php`
- `unique`-Regel: `'email' => 'unique:users,email'` prüft gegen die Datenbank
- `sometimes`-Regel: Validierung nur, wenn das Feld im Request vorhanden ist

## Muster {#patterns}

### Inline-Validierung im Controller {#inline-validation-in-controller}

```php
<?php
public function store(Request $request)
{
    $validated = $request->validate([
        'title'       => 'required|string|max:255',
        'slug'        => 'required|string|unique:posts,slug',
        'body'        => 'required|string',
        'category_id' => 'required|exists:categories,id',
        'image'       => 'nullable|image|mimes:jpg,png,webp|max:2048',
        'tags'        => 'nullable|array',
        'tags.*'      => 'exists:tags,id']);

    Post::create($validated);
    return redirect()->route('posts.index')->with('success', 'Post created.');
}

// On validation failure: auto redirect back with $errors and old input
```

### Form-Request-Klasse {#form-request-class}

```bash
php artisan make:request StorePostRequest
```

```php
<?php
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // or check user permissions
    }

    public function rules(): array
    {
        return [
            'title'       => 'required|string|max:255',
            'slug'        => 'required|string|unique:posts,slug',
            'body'        => 'required|string',
            'category_id' => 'required|exists:categories,id'];
    }

    public function messages(): array
    {
        return [
            'title.required'    => 'Post title is required.',
            'slug.unique'       => 'This URL slug is already taken.',
            'category_id.exists' => 'Selected category does not exist.'];
    }
}
```

```php
<?php
// Controller uses type-hinted Form Request
public function store(StorePostRequest $request)
{
    // Validation already passed at this point
    Post::create($request->validated());
    return redirect()->route('posts.index');
}
```

### Gängige Validierungsregeln {#common-validation-rules}

```php
<?php
$rules = [
    // String rules
    'name'     => 'required|string|min:2|max:100',
    'email'    => 'required|email',
    'slug'     => 'required|alpha_dash',      // letters, numbers, dashes, underscores
    'url'      => 'nullable|url',

    // Numeric rules
    'price'    => 'required|numeric|min:0',
    'quantity' => 'required|integer|between:1,100',

    // Date rules
    'start'    => 'required|date|after:today',
    'end'      => 'required|date|after:start',

    // File rules
    'avatar'   => 'nullable|image|mimes:jpg,png|max:2048',  // max 2MB
    'document' => 'nullable|file|mimes:pdf,doc|max:10240',

    // Database rules
    'email'    => 'required|unique:users,email',           // unique in table
    'email'    => 'required|unique:users,email,' . $user->id, // ignore current record
    'cat_id'   => 'required|exists:categories,id',         // must exist in table

    // Array rules
    'tags'     => 'nullable|array',
    'tags.*'   => 'integer|exists:tags,id',                // each element

    // Conditional rules
    'password' => 'required|confirmed|min:8',              // requires password_confirmation field
    'bio'      => 'sometimes|string|max:500',              // only validate if present
];
```

### Validierung beim Aktualisieren (unique, außer aktueller Datensatz) {#update-validation-unique-except-current}

```php
<?php
// When updating, exclude current record from unique check
public function update(Request $request, Post $post)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'slug'  => 'required|unique:posts,slug,' . $post->id,
        'body'  => 'required|string']);

    $post->update($validated);
    return redirect()->route('posts.index');
}
```

### Login-Validierung (Sicherheitsaspekte) {#login-validation-security-considerations}

```php
<?php
public function authenticate(Request $request)
{
    // For LOGIN: only validate format, NOT password strength
    // Revealing password requirements helps attackers
    $credentials = $request->validate([
        'email'    => ['required', 'email'],
        'password' => ['required'],  // NO min length, NO complexity rules
    ]);

    if (Auth::attempt($credentials)) {
        $request->session()->regenerate();
        return redirect()->intended('/admin');
    }

    // Generic error message - don't reveal which field was wrong
    return back()->with('error', 'Incorrect email or password.');
}
```

## Fallstricke {#gotchas}

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| `old()` zeigt nach einem Fehler nichts an | Eingabe hat kein `name`-Attribut | `name="field"` zum HTML-Input hinzufügen |
| Validierung besteht für leeres optionales Feld | Die Regel `nullable` erlaubt null/leer | Das ist korrektes Verhalten; `required` hinzufügen, falls das Feld Pflicht ist |
| Dateivalidierung akzeptiert falschen Typ | Regel `mimes` fehlt oder falscher MIME-Typ | `mimes:jpg,png,pdf` explizit hinzufügen |
| `unique` schlägt beim Aktualisieren des eigenen Datensatzes fehl | Aktuelle Datensatz-ID wird nicht ausgeschlossen | `unique:table,column,' . $model->id` verwenden |
| Passwortanforderungen werden beim Login offengelegt | Passwortregeln werden im Login-Formular validiert | Beim Login nur `required` verwenden; vollständige Regeln für die Registrierung |
| Form-Request-Methode `authorize()` gibt false zurück | Standardwert ist `false` | Auf `true` setzen oder Autorisierungslogik hinzufügen |
| Array-Validierung funktioniert nicht | Suffix `.*` für Array-Elemente fehlt | `'tags.*' => 'exists:tags,id'` verwenden |

## Siehe auch {#see-also}

- [[laravel-blade-templates]] - Anzeige von Fehlern mit @error und $errors
- [[laravel-authentication]] - Validierung von Login-Formularen
- [[laravel-eloquent-orm]] - Verwendung validierter Daten für CRUD
- https://laravel.com/docs/11.x/validation
- https://laravel.com/docs/11.x/validation#available-validation-rules
