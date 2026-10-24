---
title: "Validation Laravel"
category: framework
tags: [laravel, validation, form-requests, rules, error-messages]
level: 3
source_sha256: 223a25f3de082d523e0b0d9b8256f50deb0d1afb616924676f0a61580e409abf
translation: machine
translated_at: '2026-10-24'
---
# Validation Laravel {#laravel-validation}

Laravel fournit une validation de requêtes intégrée avec plus de 90 règles, une redirection automatique vers la page précédente en cas d'échec et des messages d'erreur flash. La validation peut être directement intégrée dans les contrôleurs ou extraite dans des classes Form Request. Les données validées peuvent être utilisées sans risque avec les opérations de [[laravel-eloquent-orm]]. Les erreurs sont affichées dans [[laravel-blade-templates]] via `$errors` et `@error`.

## Points clés {#key-facts}

- `$request->validate([...])` retourne un tableau de données validées ; en cas d'échec, redirige automatiquement vers la page précédente avec les erreurs
- Règles de validation sous forme de chaîne (`'required|email|max:255'`) ou de tableau (`['required', 'email', 'max:255']`)
- La variable `$errors` est toujours disponible dans les templates Blade (même vide)
- `old('field')` récupère la saisie précédente après un échec de validation
- Classes Form Request : séparent la logique de validation dans une sous-classe `Request` dédiée
- `php artisan make:request StorePostRequest` génère une classe Form Request
- Messages d'erreur personnalisés via le troisième paramètre ou la méthode `messages()` de Form Request
- Localisation : les messages de validation se trouvent dans `lang/en/validation.php`
- Règle `unique` : `'email' => 'unique:users,email'` vérifie l'existence en base de données
- Règle `sometimes` : ne valide le champ que s'il est présent dans la requête

## Modèles {#patterns}

### Validation en ligne dans le contrôleur {#inline-validation-in-controller}

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

### Classe Form Request {#form-request-class}

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

### Règles de validation courantes {#common-validation-rules}

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

### Validation lors d'une mise à jour (unique sauf l'enregistrement courant) {#update-validation-unique-except-current}

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

### Validation de la connexion (considérations de sécurité) {#login-validation-security-considerations}

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

## Pièges {#gotchas}

| Symptôme | Cause | Correction |
|---------|-------|-----|
| `old()` ne renvoie rien après une erreur | L'attribut `name` manque sur le champ | Ajouter `name="field"` à l'input HTML |
| La validation réussit pour un champ optionnel vide | La règle `nullable` accepte null ou vide | Comportement normal ; ajouter `required` si le champ est obligatoire |
| La validation de fichier accepte un mauvais type | Règle `mimes` absente ou mauvais type MIME | Ajouter explicitement `mimes:jpg,png,pdf` |
| `unique` échoue lors d'une mise à jour (son propre enregistrement) | L'ID de l'enregistrement courant n'est pas exclu | Utiliser `unique:table,column,' . $model->id` |
| Révélation des exigences de mot de passe à la connexion | Règles de mot de passe appliquées au formulaire de connexion | Utiliser uniquement `required` pour la connexion ; les règles complètes pour l'inscription |
| `authorize()` de Form Request retourne `false` | La valeur par défaut est `false` | Passer à `true` ou ajouter une logique d'autorisation |
| Validation de tableau ne fonctionne pas | Suffixe `.*` manquant pour les éléments du tableau | Utiliser `'tags.*' => 'exists:tags,id'` |

## Voir aussi {#see-also}

- [[laravel-blade-templates]] - affichage des erreurs avec @error et $errors
- [[laravel-authentication]] - validation du formulaire de connexion
- [[laravel-eloquent-orm]] - utilisation des données validées pour le CRUD
- https://laravel.com/docs/11.x/validation
- https://laravel.com/docs/11.x/validation#available-validation-rules
