---
title: Laravel File Storage
category: framework
tags: [laravel, storage, file-upload, images, disk, filesystem]
---

# Laravel File Storage

Laravel's filesystem abstraction (Flysystem) provides a unified API for local disk, S3, and other storage backends. File uploads from forms are handled via `$request->file()`, stored with the Storage facade, and served via symbolic links or signed URLs. Used in [[laravel-validation]] for file rules and [[laravel-eloquent-orm]] models to store file paths.

## Key Facts

- Configuration in `config/filesystems.php`; default disk set via `FILESYSTEM_DISK` in `.env`
- `public` disk stores files in `storage/app/public/`; accessible via `public/storage` symlink
- `php artisan storage:link` creates the symlink `public/storage -> storage/app/public`
- `$request->file('image')` returns `UploadedFile` instance
- `$request->file('image')->store('uploads')` saves to `storage/app/uploads/` with random name
- `$request->file('image')->storeAs('uploads', 'custom-name.jpg')` saves with specific name
- `Storage::disk('public')->url($path)` generates public URL for stored file
- `asset('storage/' . $path)` generates URL when using public disk with symlink
- Max upload size controlled by `upload_max_filesize` and `post_max_size` in php.ini
- Validate files with `image|mimes:jpg,png|max:2048` (max in KB)

## Patterns

### File upload in controller

```php
<?php
use Illuminate\Support\Facades\Storage;

public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'image' => 'nullable|image|mimes:jpg,jpeg,png,webp|max:2048']);

    // Store uploaded file
    if ($request->hasFile('image')) {
        $path = $request->file('image')->store('posts', 'public');
        // $path = "posts/randomname.jpg"
        $validated['image'] = $path;
    }

    Post::create($validated);
    return redirect()->route('posts.index');
}
```

### Updating file (delete old, store new)

```php
<?php
public function update(Request $request, Post $post)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'image' => 'nullable|image|mimes:jpg,png,webp|max:2048']);

    if ($request->hasFile('image')) {
        // Delete old file if exists
        if ($post->image) {
            Storage::disk('public')->delete($post->image);
        }
        $validated['image'] = $request->file('image')->store('posts', 'public');
    }

    $post->update($validated);
    return redirect()->route('posts.index');
}
```

### Deleting files

```php
<?php
public function destroy(Post $post)
{
    // Delete associated file
    if ($post->image) {
        Storage::disk('public')->delete($post->image);
    }

    $post->delete();
    return redirect()->route('posts.index');
}
```

### Displaying images in Blade

```html
{{-- Display uploaded image --}}
@if ($post->image)
    <img src="{{ asset('storage/' . $post->image) }}" alt="{{ $post->title }}">
@else
    <img src="{{ asset('images/default-post.jpg') }}" alt="Default">
@endif
```

### Upload form

```html
{{-- enctype is required for file uploads --}}
<form method="POST" action="{{ route('posts.store') }}" enctype="multipart/form-data">
    @csrf
    <input type="text" name="title" value="{{ old('title') }}">
    <input type="file" name="image" accept="image/*">
    @error('image')
        <span class="text-danger">{{ $message }}</span>
    @enderror
    <button type="submit">Upload</button>
</form>
```

### Storage facade operations

```php
<?php
use Illuminate\Support\Facades\Storage;

// Check if file exists
Storage::disk('public')->exists('posts/image.jpg');

// Get file contents
$contents = Storage::disk('public')->get('posts/image.jpg');

// Get file URL
$url = Storage::disk('public')->url('posts/image.jpg');

// Delete file
Storage::disk('public')->delete('posts/image.jpg');

// Delete directory
Storage::disk('public')->deleteDirectory('posts');

// List files in directory
$files = Storage::disk('public')->files('posts');

// Copy / Move
Storage::disk('public')->copy('old/file.jpg', 'new/file.jpg');
Storage::disk('public')->move('old/file.jpg', 'new/file.jpg');
```

## Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| Images show broken link | `storage:link` not run | Run `php artisan storage:link` |
| `enctype` missing -> file not received | Form missing `multipart/form-data` | Add `enctype="multipart/form-data"` to `<form>` |
| Upload fails silently | File exceeds php.ini limits | Increase `upload_max_filesize` and `post_max_size` |
| Old file not deleted on update | Delete logic not implemented | Call `Storage::delete()` before storing new file |
| File URL 404 after deploy | Symlink broken or not created on server | Run `storage:link` on server; some hosts don't support symlinks |
| Orphaned files accumulate | Files not deleted when model deleted | Delete files in model's `deleting` event or controller |

## See Also

- [[laravel-validation]] - file validation rules (image, mimes, max)
- [[laravel-blade-templates]] - displaying uploaded images
- [[laravel-eloquent-orm]] - storing file paths in model columns
- https://laravel.com/docs/11.x/filesystem
- https://laravel.com/docs/11.x/requests#files
