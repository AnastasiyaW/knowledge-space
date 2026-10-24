---
title: "Laravel-Dateispeicherung"
category: framework
tags: [laravel, storage, file-upload, images, disk, filesystem]
level: 3
source_sha256: 888d450744b97765c63d99a3cb8440846e5891584e81e2c577dccbb6956cce14
translation: machine
translated_at: '2026-10-24'
---
# Laravel-Dateispeicherung {#laravel-file-storage}

Laravels Dateisystem-Abstraktion (Flysystem) bietet eine einheitliche API für lokale Datenträger, S3 und weitere Speicher-Backends. Datei-Uploads aus Formularen werden über `$request->file()` verarbeitet, mit der Storage-Facade gespeichert und über symbolische Links oder signierte URLs ausgeliefert. Verwendet in [[laravel-validation]] für Datei-Regeln und in [[laravel-eloquent-orm]]-Modellen, um Dateipfade zu speichern.

## Wichtige Fakten {#key-facts}

- Konfiguration in `config/filesystems.php`; der Standard-Datenträger wird über `FILESYSTEM_DISK` in `.env` gesetzt
- Der `public`-Datenträger speichert Dateien in `storage/app/public/` und ist über den Symlink `public/storage` erreichbar
- `php artisan storage:link` erstellt den Symlink `public/storage -> storage/app/public`
- `$request->file('image')` gibt eine `UploadedFile`-Instanz zurück
- `$request->file('image')->store('uploads')` speichert nach `storage/app/uploads/` mit zufälligem Namen
- `$request->file('image')->storeAs('uploads', 'custom-name.jpg')` speichert mit einem bestimmten Namen
- `Storage::disk('public')->url($path)` erzeugt die öffentliche URL einer gespeicherten Datei
- `asset('storage/' . $path)` erzeugt die URL bei Verwendung des public-Datenträgers mit Symlink
- Die maximale Upload-Größe wird über `upload_max_filesize` und `post_max_size` in der php.ini gesteuert
- Dateien validieren mit `image|mimes:jpg,png|max:2048` (max in KB)

## Muster {#patterns}

### Datei-Upload im Controller {#file-upload-in-controller}

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

### Datei aktualisieren (alte löschen, neue speichern) {#updating-file-delete-old-store-new}

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

### Dateien löschen {#deleting-files}

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

### Bilder in Blade anzeigen {#displaying-images-in-blade}

```html
{{-- Display uploaded image --}}
@if ($post->image)
    <img src="{{ asset('storage/' . $post->image) }}" alt="{{ $post->title }}">
@else
    <img src="{{ asset('images/default-post.jpg') }}" alt="Default">
@endif
```

### Upload-Formular {#upload-form}

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

### Storage-Facade-Operationen {#storage-facade-operations}

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

## Stolperfallen {#gotchas}

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| Bilder zeigen einen defekten Link | `storage:link` wurde nicht ausgeführt | `php artisan storage:link` ausführen |
| `enctype` fehlt -> Datei wird nicht empfangen | Formular hat kein `multipart/form-data` | `enctype="multipart/form-data"` zum `<form>` hinzufügen |
| Upload schlägt stillschweigend fehl | Datei überschreitet die php.ini-Limits | `upload_max_filesize` und `post_max_size` erhöhen |
| Alte Datei wird beim Aktualisieren nicht gelöscht | Lösch-Logik nicht implementiert | `Storage::delete()` aufrufen, bevor die neue Datei gespeichert wird |
| Datei-URL liefert nach Deployment 404 | Symlink defekt oder auf dem Server nicht erstellt | `storage:link` auf dem Server ausführen; manche Hoster unterstützen keine Symlinks |
| Verwaiste Dateien sammeln sich an | Dateien werden beim Löschen des Modells nicht entfernt | Dateien im `deleting`-Event des Modells oder im Controller löschen |

## Siehe auch {#see-also}

- [[laravel-validation]] - Datei-Validierungsregeln (image, mimes, max)
- [[laravel-blade-templates]] - Anzeige hochgeladener Bilder
- [[laravel-eloquent-orm]] - Speichern von Dateipfaden in Modellspalten
- https://laravel.com/docs/11.x/filesystem
- https://laravel.com/docs/11.x/requests#files
