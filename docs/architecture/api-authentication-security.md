---
title: API Authentication and Security
category: reference
tags: [security, authentication, authorization, oauth, jwt, tls, encryption]
---

# API Authentication and Security

Authentication proves identity, authorization determines access. Security architecture spans cryptography, protocols, and organizational practices. The architect identifies weak spots and communicates them to the right people.

## Authentication vs Authorization

| Concept | Question | Example |
|---------|----------|---------|
| **Identification** | Who are you? | Username/login |
| **Authentication** | Prove it | Password, token, biometrics |
| **Authorization** | What can you access? | Permissions, roles |

## Authentication Methods

### 1. API Key
Simple key in header: `X-API-Key: abc123`. Easy but limited - typically for server-to-server, not user-level auth.

### 2. Basic Auth
Base64-encoded `username:password` in `Authorization` header. Must use HTTPS. Sends credentials with every request.

### 3. Session-Based (Cookies)
Server creates session on login, stores session ID in cookie. Browser sends cookie automatically.
- Cookie attributes: `Secure` (HTTPS only), `HttpOnly` (no JS access), `SameSite` (CSRF protection)
- Requires session storage (Keycloak, Redis)

### 4. JWT (JSON Web Token)
Self-contained token: `header.payload.signature` (Base64-encoded).

```
Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"user_id": 123, "roles": ["admin"], "exp": 1700000000}
Signature: HMAC-SHA256(base64(header) + "." + base64(payload), secret)
```

- **Stateless** - server doesn't store sessions
- **Token pair** - access token (short-lived, 15-30 min) + refresh token (long-lived)

### 5. OAuth 2.0
Delegated authorization framework. Four roles: Resource Owner, Client, Authorization Server, Resource Server.

**Grant types:**

| Type | Use Case |
|------|----------|
| Authorization Code | Server apps (most secure) |
| Client Credentials | Machine-to-machine |
| PKCE | Mobile/SPA apps |

**Authorization Code Flow:**
```
1. Client redirects user to authorization server
2. User authenticates and grants permission
3. Auth server returns authorization code
4. Client exchanges code for access token (server-side)
5. Client uses access token to access resources
```

### 6. mTLS (Mutual TLS)
Both client and server present certificates. Used for high-security scenarios: financial APIs, inter-service communication.

## Cryptography Fundamentals

### Symmetric Encryption
One shared secret key for both encryption and decryption. Fast but key must be transmitted securely.
- Pro: fast, suitable for large data volumes
- Con: key transmission is the vulnerability

### Asymmetric Encryption
Two keys: public (encrypts) and private (decrypts). Receiver distributes public key freely.
- Pro: high security, no key transmission risk, enables digital signatures
- Con: slower by orders of magnitude, higher compute cost

### Hybrid Encryption (HTTPS)
Asymmetric to securely exchange symmetric key, then symmetric for actual data transfer. Best of both worlds.

### TLS Handshake
```
1. Client sends supported cipher suites
2. Server selects cipher, sends certificate with public key
3. Client verifies certificate against CA
4. Key exchange (Diffie-Hellman or RSA)
5. Symmetric key established for session
6. All subsequent data encrypted symmetrically
```

## Digital Signatures

1. Sender creates hash of document
2. Hash encrypted with sender's **private key** = digital signature
3. Receiver decrypts signature with sender's **public key** to get hash
4. Receiver independently hashes the document
5. If hashes match: document is authentic and unmodified

**Certificate Authority (CA)** system verifies identity. CA maintains registry of valid/revoked certificates.

## Hashing

One-way transformation producing fixed-length output. Any single-character change produces completely different hash. Used for: password storage, data integrity verification, digital signatures.

## Application Security Checklist

| Area | Threats | Mitigations |
|------|---------|-------------|
| Input validation | SQL injection, XSS | Parameterized queries, sanitization |
| Session management | Session hijacking | Unique IDs, Secure/HttpOnly cookies |
| Data encryption | Interception | AES at rest, TLS in transit |
| API security | Code injection | API Gateway, input validation |
| Logging | Undetected attacks | ELK Stack, Grafana, audit trail |
| Code scanning | Vulnerabilities | OWASP ZAP, SonarQube |
| Error handling | Information leakage | Custom error pages, internal-only details |
| Rate limiting | DoS/DDoS | Per-user/IP limits |

## Data-Level Security

- **At-rest encryption** - AES, TDE. Regular key rotation
- **In-transit encryption** - TLS/SSL for all transmission
- **Data masking** - masked values for non-production environments
- **Access control** - RBAC, principle of least privilege
- **DLP** - monitor/block unauthorized data transfer
- **Immutable backups (WORM)** - Write Once, Read Many
- **Zero Trust** - verify every request regardless of source

## Gotchas

- **JWT in local storage** - vulnerable to XSS. Prefer HttpOnly cookies for web apps
- **API keys in URLs** - visible in logs and browser history. Use headers
- **OAuth implicit flow** - deprecated. Use Authorization Code + PKCE instead
- **Self-signed certificates** - disable SSL verification in dev only, never in production
- **Error messages** - "Invalid username" vs "Invalid password" reveals which is correct. Use generic "Invalid credentials"

## See Also

- [[http-rest-fundamentals]] - HTTP protocol basics, CORS
- [[security-architecture]] - Architect's security workflow
- [[authentication-and-authorization]] - SSO patterns, SAML, OpenID Connect
