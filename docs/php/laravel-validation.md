---
title: Laravel Validation
category: framework
tags: [laravel, validation, form-requests, rules, error-messages]
---

# Laravel Validation

Laravel provides built-in request validation with 90+ rules, automatic redirect-back on failure, and flash error messages. Validation can be inline in controllers or extracted to Form Request classes. Validated data is safe for [[laravel-eloquent-orm]] operations. Errors are displayed in [[laravel-blade-templates]] via `$errors` and `@error`.

## Key Facts

- `$request->validate([...])` returns validated data array; auto-redirects back with errors on failure
- Validation rules as string (`'required|email|max:255'`) or array (`['required', 'email', 'max:255']`)
- `$errors` variable is always available in Blade templates (even when empty)
- `old('field')` retrieves previous input after validation failure
- Form Request classes: separate validation logic into dedicated `Request` subclass
- `php artisan make:request StorePostRequest` generates a Form Request class
- Custom error messages via third parameter or Form Request `messages()` method
- Localization: validation messages in `lang/en/validation.php`
- `unique` rule: `'email' => 'unique:users,email'` checks against database
- `sometimes` rule: only validate if field is present in request

## Patterns

### Inline validation in controller

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
        'tags.*'      => 'exists:tags,id',
    ]);

    Post::create($validated);
    return redirect()->route('posts.index')->with('success', 'Post created.');
}

// On validation failure: auto redirect back with $errors and old input
```

### Form Request class

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
            'category_id' => 'required|exists:categories,id',
        ];
    }

    public function messages(): array
    {
        return [
            'title.required'    => 'Post title is required.',
            'slug.unique'       => 'This URL slug is already taken.',
            'category_id.exists' => 'Selected category does not exist.',
        ];
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

### Common validation rules

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

### Update validation (unique except current)

```php
<?php
// When updating, exclude current record from unique check
public function update(Request $request, Post $post)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'slug'  => 'required|unique:posts,slug,' . $post->id,
        'body'  => 'required|string',
    ]);

    $post->update($validated);
    return redirect()->route('posts.index');
}
```

### Login validation (security considerations)

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

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| `old()` shows nothing after error | Input missing `name` attribute | Add `name="field"` to HTML input |
| Validation passes for empty optional field | `nullable` rule allows null/empty | This is correct behavior; add `required` if field is mandatory |
| File validation accepts wrong type | Missing `mimes` rule or wrong mime type | Add `mimes:jpg,png,pdf` explicitly |
| `unique` fails on update (own record) | Current record ID not excluded | Use `unique:table,column,' . $model->id` |
| Revealing password requirements on login | Validating password rules on login form | Only use `required` for login; full rules for registration |
| Form Request `authorize()` returns false | Default is `false` | Set to `true` or add authorization logic |
| Array validation not working | Missing `.*` suffix for array elements | Use `'tags.*' => 'exists:tags,id'` |

## See Also

- [[laravel-blade-templates]] - displaying errors with @error and $errors
- [[laravel-authentication]] - login form validation
- [[laravel-eloquent-orm]] - using validated data for CRUD
- https://laravel.com/docs/11.x/validation
- https://laravel.com/docs/11.x/validation#available-validation-rules
