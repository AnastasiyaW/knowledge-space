---
title: File Upload Security
category: web-security
tags: [file-upload, validation, web-shell, mime-type, owasp, injection]
---

# File Upload Security

## Key Facts

- Unrestricted file upload is a critical vulnerability allowing remote code execution (CWE-434)
- Validation must happen on both client AND server side - client-side validation is trivially bypassed
- Check file type by magic bytes (file signature), NOT by extension or Content-Type header - both are user-controlled
- Store uploaded files outside the web root or in object storage (S3) - never serve uploads from the application directory
- Rename uploaded files with random UUID - original filename may contain path traversal (`../../etc/passwd`)
- [[cors-and-origin-security]] must restrict upload endpoints to authorized origins
- [[jwt-authentication]] should protect upload endpoints from anonymous access

## Patterns

```javascript
// NestJS file upload with validation
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { v4 as uuid } from 'uuid';
import * as path from 'path';

@Post('upload')
@UseInterceptors(FileInterceptor('file', {
  storage: diskStorage({
    destination: './uploads',  // Outside web root
    filename: (req, file, cb) => {
      // Random filename, preserve extension
      const ext = path.extname(file.originalname);
      cb(null, `${uuid()}${ext}`);
    },
  }),
  limits: {
    fileSize: 10 * 1024 * 1024,  // 10MB max
  },
  fileFilter: (req, file, cb) => {
    // Whitelist MIME types
    const allowed = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowed.includes(file.mimetype)) {
      cb(new BadRequestException('Invalid file type'), false);
    }
    cb(null, true);
  },
}))
async uploadFile(@UploadedFile() file: Express.Multer.File) {
  return { path: file.filename };
}
```

```python
# Magic bytes validation (server-side)
import magic  # python-magic library

ALLOWED_MIMES = {'image/jpeg', 'image/png', 'image/webp', 'application/pdf'}

def validate_upload(file_bytes: bytes, claimed_type: str) -> bool:
    """Validate file by actual content, not claimed type"""
    actual_type = magic.from_buffer(file_bytes[:2048], mime=True)
    return actual_type in ALLOWED_MIMES

# Magic bytes reference:
# JPEG: FF D8 FF
# PNG:  89 50 4E 47
# PDF:  25 50 44 46
# GIF:  47 49 46 38
# ZIP:  50 4B 03 04
```

```nginx
# Nginx - serve uploads as static with restricted types
location /uploads/ {
    alias /var/data/uploads/;

    # Disable script execution
    location ~* \.(php|jsp|py|sh|cgi|pl)$ {
        deny all;
    }

    # Force download for non-image types
    add_header Content-Disposition "attachment";

    # Only allow specific types inline
    location ~* \.(jpg|jpeg|png|gif|webp)$ {
        add_header Content-Disposition "inline";
    }
}
```

## Gotchas

- Double extension bypass: `shell.php.jpg` - some servers execute `.php` ignoring `.jpg` suffix
- Content-Type header is set by the client and MUST NOT be trusted for validation
- SVG files can contain embedded JavaScript - treat SVG as potentially dangerous even though it is an "image"
- Image processing libraries (ImageMagick, Pillow) have had RCE vulnerabilities - keep them updated and use policy files
- EXIF metadata in images can contain malicious content - strip metadata from uploaded images
- Polyglot files: a file that is simultaneously valid JPEG and valid PHP - magic bytes check is necessary but not sufficient

## See Also

- [CWE-434 Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
