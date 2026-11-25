---
title: "Templates Blade de Laravel"
category: framework
tags: [laravel, blade, templates, views, layouts, components, directives]
level: 3
source_sha256: bbecc3dc2240b2687c82279c2a4bb758afd32ac3f54cd848388f65df6a5535b6
translation: machine
translated_at: '2026-10-24'
---
# Templates Blade de Laravel {#laravel-blade-templates}

Blade est le moteur de templates de Laravel. Il fournit l'héritage de templates, les sections, les composants et les directives de contrôle. Les templates se trouvent dans `resources/views/` avec l'extension `.blade.php`. Blade compile les templates en PHP pur et met le résultat en cache pour les performances. Utilisé dans les contrôleurs de [[laravel-routing]] pour générer les réponses HTML.

## Points clés {#key-facts}

- Templates stockés dans `resources/views/` avec l'extension `.blade.php`
- `{{ $var }}` affiche du HTML échappé (protégé contre le XSS) ; `{!! $var !!}` affiche du HTML brut (dangereux)
- Héritage de templates via `@extends('layout')` et `@section`/`@yield`
- Directives Blade : `@if`, `@foreach`, `@isset`, `@empty`, `@auth`, `@guest`, `@csrf`, `@method`
- `view('posts.index', compact('posts'))` génère `resources/views/posts/index.blade.php`
- Données transmises aux vues via `compact()`, un tableau associatif ou `->with()`
- `@include('partials.header')` inclut un sous-template
- Composants Blade (basés sur une classe et anonymes) pour les éléments d'interface réutilisables
- `old('field')` récupère la saisie précédente après un échec de validation (flash data)
- La variable `$errors` est toujours disponible dans Blade (sac d'erreurs de validation)

## Motifs d'utilisation {#patterns}

### Mise en page et sections {#layout-and-sections}

```html
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    <title>@yield('title', 'My App')</title>
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
</head>
<body>
    @include('partials.navbar')

    <div class="container">
        @yield('content')
    </div>

    @stack('scripts')
</body>
</html>
```

```html
{{-- resources/views/posts/index.blade.php --}}
@extends('layouts.app')

@section('title', 'All Posts')

@section('content')
    <h1>Posts</h1>
    @foreach ($posts as $post)
        <article>
            <h2>{{ $post->title }}</h2>
            <p>{{ Str::limit($post->body, 200) }}</p>
            <a href="{{ route('posts.show', $post) }}">Read more</a>
        </article>
    @endforeach

    {{ $posts->links() }}  {{-- pagination --}}
@endsection

@push('scripts')
    <script src="{{ asset('js/posts.js') }}"></script>
@endpush
```

### Transmettre des données depuis les contrôleurs {#passing-data-from-controllers}

```php
<?php
// Method 1: compact()
public function index()
{
    $posts = Post::latest()->paginate(15);
    $categories = Category::all();
    return view('posts.index', compact('posts', 'categories'));
}

// Method 2: associative array
return view('posts.show', ['post' => $post, 'related' => $related]);

// Method 3: with()
return view('posts.show')->with('post', $post);
```

### Directives de contrôle {#control-directives}

```html
{{-- Conditionals --}}
@if ($posts->count() > 0)
    <p>{{ $posts->count() }} posts found.</p>
@elseif ($category)
    <p>No posts in {{ $category->name }}.</p>
@else
    <p>No posts yet.</p>
@endif

{{-- Auth check --}}
@auth
    <p>Welcome, {{ auth()->user()->name }}</p>
@endauth

@guest
    <a href="{{ route('login') }}">Log in</a>
@endguest

{{-- Isset / Empty --}}
@isset($post->image)
    <img src="{{ asset('storage/' . $post->image) }}" alt="">
@endisset

@empty($posts)
    <p>Nothing to display.</p>
@endempty

{{-- Loops --}}
@forelse ($posts as $post)
    <h2>{{ $post->title }}</h2>
@empty
    <p>No posts found.</p>
@endforelse

{{-- Loop variable --}}
@foreach ($items as $item)
    {{ $loop->index }}        {{-- 0-based index --}}
    {{ $loop->iteration }}    {{-- 1-based index --}}
    {{ $loop->first }}        {{-- true on first iteration --}}
    {{ $loop->last }}         {{-- true on last iteration --}}
    {{ $loop->count }}        {{-- total items --}}
@endforeach
```

### Formulaires avec CSRF et usurpation de méthode {#forms-with-csrf-and-method-spoofing}

```html
{{-- Create form --}}
<form method="POST" action="{{ route('posts.store') }}">
    @csrf
    <input type="text" name="title" value="{{ old('title') }}">
    @error('title')
        <span class="text-danger">{{ $message }}</span>
    @enderror
    <button type="submit">Create</button>
</form>

{{-- Update form (PUT method) --}}
<form method="POST" action="{{ route('posts.update', $post) }}">
    @csrf
    @method('PUT')
    <input type="text" name="title" value="{{ old('title', $post->title) }}">
    <button type="submit">Update</button>
</form>

{{-- Delete form --}}
<form method="POST" action="{{ route('posts.destroy', $post) }}"
      onsubmit="return confirm('Are you sure?')">
    @csrf
    @method('DELETE')
    <button type="submit">Delete</button>
</form>
```

### Affichage des erreurs de validation {#validation-errors-display}

```html
{{-- Show all errors --}}
@if ($errors->any())
    <div class="alert alert-danger">
        <ul class="list-unstyled mb-0">
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

{{-- Show error for specific field --}}
@error('email')
    <div class="text-danger">{{ $message }}</div>
@enderror

{{-- Flash messages --}}
@if (session('success'))
    <div class="alert alert-success">{{ session('success') }}</div>
@endif
```

### Layouts admin et public {#admin-vs-public-layouts}

```text
resources/views/
  admin/
    layouts/
      default.blade.php     # admin layout (sidebar, AdminLTE)
    posts/
      index.blade.php       # admin post list
      create.blade.php
  layouts/
    app.blade.php            # public layout
  posts/
    index.blade.php          # public post list
    show.blade.php
  user/
    login.blade.php          # standalone layout (no extends)
```

## Pièges {#gotchas}

| Symptôme | Cause | Solution |
|---------|-------|-----|
| Vulnérabilité XSS | Utilisation de `{!! !!}` avec des données utilisateur | Toujours utiliser `{{ }}` pour les données fournies par l'utilisateur |
| `@csrf` absent -> erreur 419 | Formulaire POST sans jeton CSRF | Ajouter `@csrf` dans chaque formulaire POST/PUT/DELETE |
| `old()` ne retourne rien | Formulaire sans attribut `name` | Ajouter `name="field"` aux éléments input |
| Vue introuvable | Notation par points incorrecte ou fichier inexistant | Vérifier le chemin : `view('admin.posts.index')` = `views/admin/posts/index.blade.php` |
| Modifications du layout non prises en compte | Vues compilées mises en cache | Exécuter `php artisan view:clear` |
| `$loop` non défini | Utilisation de `$loop` en dehors de `@foreach` | `$loop` n'est disponible qu'à l'intérieur de `@foreach`/`@forelse` |
| `@method('PUT')` sans effet | Placé en dehors de la balise `<form>` | Doit être placé à l'intérieur de l'élément `<form>` |

## Voir aussi {#see-also}

- [[laravel-routing]] - contrôleurs qui retournent des vues
- [[laravel-validation]] - affichage des erreurs dans les templates
- [[laravel-authentication]] - directives auth/guest
- https://laravel.com/docs/11.x/blade
- https://laravel.com/docs/11.x/views
