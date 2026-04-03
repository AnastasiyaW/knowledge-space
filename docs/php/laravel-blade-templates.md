---
title: Laravel Blade Templates
category: framework
tags: [laravel, blade, templates, views, layouts, components, directives]
---

# Laravel Blade Templates

Blade is Laravel's templating engine that provides template inheritance, sections, components, and control directives. Templates live in `resources/views/` with `.blade.php` extension. Blade compiles to plain PHP and caches the result for performance. Used in [[laravel-routing]] controllers to render HTML responses.

## Key Facts

- Templates stored in `resources/views/` with `.blade.php` extension
- `{{ $var }}` outputs escaped HTML (XSS safe); `{!! $var !!}` outputs raw HTML (dangerous)
- Template inheritance via `@extends('layout')` and `@section`/`@yield`
- Blade directives: `@if`, `@foreach`, `@isset`, `@empty`, `@auth`, `@guest`, `@csrf`, `@method`
- `view('posts.index', compact('posts'))` renders `resources/views/posts/index.blade.php`
- Data passed to views via `compact()`, associative array, or `->with()`
- `@include('partials.header')` includes a sub-template
- Blade components (class-based and anonymous) for reusable UI elements
- `old('field')` retrieves previous input after validation failure (flash data)
- `$errors` variable is always available in Blade (validation error bag)

## Patterns

### Layout and sections

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

### Passing data from controllers

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

### Control directives

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

### Forms with CSRF and method spoofing

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

### Validation errors display

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

### Admin vs Public layouts

```
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

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| XSS vulnerability | Using `{!! !!}` with user input | Always use `{{ }}` for user-provided data |
| `@csrf` missing -> 419 error | POST form without CSRF token | Add `@csrf` inside every POST/PUT/DELETE form |
| `old()` returns nothing | Form not using `name` attribute | Add `name="field"` to input elements |
| View not found | Wrong dot notation or file doesn't exist | Check path: `view('admin.posts.index')` = `views/admin/posts/index.blade.php` |
| Layout changes not reflected | Compiled views cached | Run `php artisan view:clear` |
| `$loop` undefined | Using `$loop` outside `@foreach` | `$loop` is only available inside `@foreach`/`@forelse` |
| `@method('PUT')` not working | Placed outside `<form>` tag | Must be inside the `<form>` element |

## See Also

- [[laravel-routing]] - controllers that return views
- [[laravel-validation]] - error display in templates
- [[laravel-authentication]] - auth/guest directives
- https://laravel.com/docs/11.x/blade
- https://laravel.com/docs/11.x/views
