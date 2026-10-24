---
title: "Laravel Blade-Templates"
category: framework
tags: [laravel, blade, templates, views, layouts, components, directives]
level: 3
source_sha256: bbecc3dc2240b2687c82279c2a4bb758afd32ac3f54cd848388f65df6a5535b6
translation: machine
translated_at: '2026-10-24'
---
# Laravel Blade-Templates {#laravel-blade-templates}

Blade ist die Template-Engine von Laravel. Sie bietet Template-Vererbung, Sections, Komponenten und Steuerungsdirektiven. Templates liegen in `resources/views/` mit der Dateiendung `.blade.php`. Blade kompiliert zu reinem PHP und cacht das Ergebnis zur Performance-Optimierung. Wird in [[laravel-routing]]-Controllern verwendet, um HTML-Antworten zu rendern.

## Wichtige Fakten {#key-facts}

- Templates werden in `resources/views/` mit der Dateiendung `.blade.php` gespeichert
- `{{ $var }}` gibt escaptes HTML aus (XSS-sicher); `{!! $var !!}` gibt rohes HTML aus (gefährlich)
- Template-Vererbung über `@extends('layout')` und `@section`/`@yield`
- Blade-Direktiven: `@if`, `@foreach`, `@isset`, `@empty`, `@auth`, `@guest`, `@csrf`, `@method`
- `view('posts.index', compact('posts'))` rendert `resources/views/posts/index.blade.php`
- Daten werden über `compact()`, ein assoziatives Array oder `->with()` an Views übergeben
- `@include('partials.header')` bindet ein Sub-Template ein
- Blade-Komponenten (klassenbasiert und anonym) für wiederverwendbare UI-Elemente
- `old('field')` liefert die vorherige Eingabe nach einem Validierungsfehler (Flash-Daten)
- Die Variable `$errors` ist in Blade immer verfügbar (Validierungsfehler-Bag)

## Muster {#patterns}

### Layout und Sections {#layout-and-sections}

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

### Daten aus Controllern übergeben {#passing-data-from-controllers}

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

### Steuerungsdirektiven {#control-directives}

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

### Formulare mit CSRF und Method Spoofing {#forms-with-csrf-and-method-spoofing}

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

### Anzeige von Validierungsfehlern {#validation-errors-display}

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

### Admin- vs. öffentliche Layouts {#admin-vs-public-layouts}

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

## Stolpersteine {#gotchas}

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| XSS-Schwachstelle | `{!! !!}` mit Benutzereingaben verwendet | Für benutzerseitige Daten immer `{{ }}` verwenden |
| `@csrf` fehlt -> 419-Fehler | POST-Formular ohne CSRF-Token | `@csrf` in jedes POST/PUT/DELETE-Formular einfügen |
| `old()` liefert nichts | Formular verwendet kein `name`-Attribut | `name="field"` zu den Eingabeelementen hinzufügen |
| View nicht gefunden | Falsche Punkt-Notation oder Datei existiert nicht | Pfad prüfen: `view('admin.posts.index')` = `views/admin/posts/index.blade.php` |
| Layout-Änderungen werden nicht übernommen | Kompilierte Views sind gecacht | `php artisan view:clear` ausführen |
| `$loop` undefiniert | `$loop` außerhalb von `@foreach` verwendet | `$loop` ist nur innerhalb von `@foreach`/`@forelse` verfügbar |
| `@method('PUT')` funktioniert nicht | Platzierung außerhalb des `<form>`-Tags | Muss innerhalb des `<form>`-Elements stehen |

## Siehe auch {#see-also}

- [[laravel-routing]] - Controller, die Views zurückgeben
- [[laravel-validation]] - Fehleranzeige in Templates
- [[laravel-authentication]] - Auth/Guest-Direktiven
- https://laravel.com/docs/11.x/blade
- https://laravel.com/docs/11.x/views
