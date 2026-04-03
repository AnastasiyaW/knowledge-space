---
title: API Authentication and Security
category: api
tags: [architecture, security, authentication, oauth, jwt, tls, encryption]
---

# API Authentication and Security

Comprehensive guide to API security covering cryptographic fundamentals, authentication methods, authorization frameworks, and transport security for production REST APIs.

## Cryptography Fundamentals

### Symmetric Encryption
One shared secret key for both encryption and decryption. Fast but risky - key must be transmitted securely.
- **Pro**: Fast, suitable for large data volumes
- **Con**: Key transmission is the vulnerability

### Asymmetric Encryption
Two keys: public (encrypts) and private (decrypts). Receiver generates public key from private key and distributes it freely.
- **Pro**: High security, no key transmission risk, enables digital signatures
- **Con**: Slower (orders of magnitude), not suitable for large data

### Hybrid Encryption (HTTPS)
Combines both: asymmetric encryption to exchange a symmetric key, then symmetric encryption for data. Best of both worlds.

### Hashing
One-way transformation producing fixed-length output. Any single-character change produces completely different hash. Used for: password storage, data integrity verification, digital signatures.

### Digital Signatures
1. Sender creates hash of document
2. Hash encrypted with sender's **private key** = digital signature
3. Receiver decrypts signature using sender's **public key** to get hash
4. Receiver independently hashes received document
5. If hashes match: document is authentic and unmodified

**Certificate Authority (CA)**: sender registers, receives certificate (public key + identity info). CA maintains registry of valid/revoked certificates.

### Diffie-Hellman Key Exchange
Both parties agree on public numbers, each has a secret, and through mathematical operations they arrive at the same shared secret without ever transmitting it.

## Authentication vs Authorization

- **Identification**: Who are you? (username/login)
- **Authentication**: Prove it (password, token, biometrics)
- **Authorization**: What can you access? (permissions, roles)

## Authentication Methods

### 1. API Key
Simple key in header: `X-API-Key: abc123`. Easy to implement. Typically for server-to-server, not user-level auth.

### 2. Basic Auth
Base64-encoded `username:password` in `Authorization` header. Must use HTTPS. Simple but sends credentials with every request.

### 3. Session-Based (Cookies)
Server creates session on login, stores session ID in cookie (`Set-Cookie: PHPSESSID=...`). Browser sends cookie automatically.
- Cookie attributes: `Secure` (HTTPS only), `HttpOnly` (no JS access), `SameSite` (CSRF protection)

### 4. Token-Based (JWT)
JSON Web Token: self-contained token with claims, signed by server.
- Structure: `header.payload.signature` (Base64-encoded)
- Header: algorithm + type
- Payload: claims (user ID, roles, expiration)
- Signature: HMAC or RSA of header+payload
- **Stateless**: server doesn't store sessions
- **Expiration**: access token (15-30 min) + refresh token (long-lived)

### 5. OAuth 2.0
Delegated authorization framework. Four roles: Resource Owner, Client, Authorization Server, Resource Server.

**Grant types:**
- **Authorization Code** (most secure, for server apps)
- **Client Credentials** (machine-to-machine)
- **PKCE** (for mobile/SPA apps)

**Authorization Code flow:**
1. Client redirects user to authorization server
2. User authenticates and grants permission
3. Authorization server returns authorization code
4. Client exchanges code for access token (server-side)
5. Client uses access token to access resources

### 6. mTLS (Mutual TLS)
Both client and server present certificates. Used for high-security scenarios: financial APIs, inter-service communication.

## TLS Handshake

1. Client sends supported cipher suites
2. Server selects cipher suite, sends certificate with public key
3. Client verifies certificate against CA
4. Key exchange (Diffie-Hellman or RSA)
5. Symmetric key established for session
6. All subsequent data encrypted symmetrically

## Method Selection Guide

| Method | Best For | Complexity |
|--------|----------|------------|
| API Key | Server-to-server, internal APIs | Low |
| Basic Auth | Simple internal tools (over HTTPS) | Low |
| Session/Cookie | Traditional web apps | Medium |
| JWT | Stateless APIs, microservices | Medium |
| OAuth 2.0 | Third-party access, delegated auth | High |
| mTLS | Financial, high-security inter-service | High |

## Gotchas

- Never send credentials over plain HTTP - always HTTPS
- JWT tokens cannot be invalidated before expiration without a blacklist (defeats statelessness)
- OAuth 2.0 is an authorization framework, not authentication - use OpenID Connect for auth
- API keys in query parameters get logged in server access logs - use headers instead
- Session-based auth complicates horizontal scaling - use external session store (Redis)

## See Also

- [[rest-api-design]] - REST API fundamentals
- [[security-architecture]] - comprehensive security architecture
- [[distributed-systems]] - mTLS in service mesh context
