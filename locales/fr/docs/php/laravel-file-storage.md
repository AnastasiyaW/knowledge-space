---
title: "Stockage de fichiers Laravel"
category: framework
tags: [laravel, storage, file-upload, images, disk, filesystem]
level: 3
source_sha256: 888d450744b97765c63d99a3cb8440846e5891584e81e2c577dccbb6956cce14
translation: machine
translated_at: '2026-10-24'
---
# Stockage de fichiers Laravel {#laravel-file-storage}

L'abstraction de système de fichiers de Laravel (Flysystem) fournit une API unifiée pour le disque local, S3 et d'autres backends de stockage. Les fichiers envoyés via les formulaires sont traités avec `$request->file()`, enregistrés avec la façade Storage, puis servis via des liens symboliques ou des URL signées. Utilisé avec [[laravel-validation]] pour les règles de fichiers et avec les modèles [[laravel-eloquent-orm]] pour stocker les chemins de fichiers.

## Faits clés {#key-facts}

- Configuration dans `config/filesystems.php` ; disque par défaut défini via `FILESYSTEM_DISK` dans `.env`
- Le disque `public` stocke les fichiers dans `storage/app/public/`, accessibles via le lien symbolique `public/storage`
- `php artisan storage:link` crée le lien symbolique `public/storage -> storage/app/public`
- `$request->file('image')` retourne une instance de `UploadedFile`
- `$request->file('image')->store('uploads')` enregistre dans `storage/app/uploads/` avec un nom aléatoire
- `$request->file('image')->storeAs('uploads', 'custom-name.jpg')` enregistre avec un nom spécifique
- `Storage::disk('public')->url($path)` génère l'URL publique du fichier stocké
- `asset('storage/' . $path)` génère l'URL lorsque le disque public est utilisé avec le lien symbolique
- La taille maximale d'envoi est contrôlée par `upload_max_filesize` et `post_max_size` dans php.ini
- Valider les fichiers avec `image|mimes:jpg,png|max:2048` (max en Ko)

## Modèles courants {#patterns}

### Envoi de fichier dans un contrôleur {#file-upload-in-controller}

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

### Mise à jour de fichier (suppression de l'ancien, stockage du nouveau) {#updating-file-delete-old-store-new}

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

### Suppression de fichiers {#deleting-files}

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

### Affichage d'images dans Blade {#displaying-images-in-blade}

```html
{{-- Display uploaded image --}}
@if ($post->image)
    <img src="{{ asset('storage/' . $post->image) }}" alt="{{ $post->title }}">
@else
    <img src="{{ asset('images/default-post.jpg') }}" alt="Default">
@endif
```

### Formulaire d'envoi {#upload-form}

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

### Opérations avec la façade Storage {#storage-facade-operations}

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

## Pièges courants {#gotchas}

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Images affichées avec un lien cassé | `storage:link` non exécuté | Exécuter `php artisan storage:link` |
| `enctype` absent -> fichier non reçu | Formulaire sans `multipart/form-data` | Ajouter `enctype="multipart/form-data"` à `<form>` |
| Échec silencieux de l'envoi | Fichier dépassant les limites de php.ini | Augmenter `upload_max_filesize` et `post_max_size` |
| Ancien fichier non supprimé lors de la mise à jour | Logique de suppression non implémentée | Appeler `Storage::delete()` avant de stocker le nouveau fichier |
| URL du fichier en 404 après déploiement | Lien symbolique cassé ou non créé sur le serveur | Exécuter `storage:link` sur le serveur ; certains hébergeurs ne supportent pas les liens symboliques |
| Accumulation de fichiers orphelins | Fichiers non supprimés lors de la suppression du modèle | Supprimer les fichiers dans l'événement `deleting` du modèle ou dans le contrôleur |

## Voir aussi {#see-also}

- [[laravel-validation]] - règles de validation de fichiers (image, mimes, max)
- [[laravel-blade-templates]] - affichage des images envoyées
- [[laravel-eloquent-orm]] - stockage des chemins de fichiers dans les colonnes de modèles
- https://laravel.com/docs/11.x/filesystem
- https://laravel.com/docs/11.x/requests#files
