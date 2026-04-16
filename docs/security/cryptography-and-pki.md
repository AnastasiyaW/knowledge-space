---
title: Cryptography and PKI
category: concepts
tags: [security, cryptography, encryption, tls, pki, hashing]
---

# Cryptography and PKI

Symmetric and asymmetric encryption, hashing algorithms, digital signatures, TLS/SSL protocol mechanics, and Public Key Infrastructure. Essential building blocks for secure communications and data protection.

## Key Facts
- Symmetric encryption (AES) is fast for bulk data but has the key distribution problem
- Asymmetric encryption (RSA, ECC) solves key exchange but is slow - used for key exchange and signatures, not bulk data
- ECC 256-bit provides equivalent security to RSA 3072-bit with shorter keys
- TLS 1.3 reduced handshake to 1-RTT (from 2-RTT in 1.2), removed weak ciphers, mandates PFS
- Perfect Forward Secrecy (PFS) means compromising the server's private key does not decrypt past sessions
- MD5 and SHA-1 are broken - never use for security purposes

## Symmetric Encryption
Same key for encryption and decryption:
- **AES** - current standard, 128/192/256-bit keys
- **ChaCha20** - stream cipher, used in TLS, mobile-friendly (faster without AES-NI)
- **DES/3DES** - legacy, broken/deprecated
- Key distribution problem: how to securely share the key between parties

## Asymmetric Encryption
Public key + private key pair:
- **RSA** - based on factoring large primes, 2048+ bit keys minimum
- **ECC** (Elliptic Curve) - shorter keys for equivalent security
- **Diffie-Hellman** - key exchange protocol (not encryption itself)
- Used for key exchange and digital signatures, not bulk data

## Hashing
One-way function producing fixed-size output:

| Algorithm | Status | Use Case |
|-----------|--------|----------|
| SHA-256/SHA-3 | Current standard | Integrity verification |
| MD5 | Broken (collisions) | Never for security |
| SHA-1 | Deprecated (SHAttered 2017) | Legacy only |
| bcrypt/scrypt/Argon2 | Current standard | Password hashing (deliberately slow, salted) |

Properties: deterministic, avalanche effect, pre-image resistance, collision resistance.

## Digital Signatures
1. Sender hashes the message
2. Sender encrypts hash with **private key** = signature
3. Recipient decrypts signature with sender's **public key**
4. Recipient hashes the message independently
5. Hashes match = authentic and unmodified

## PKI (Public Key Infrastructure)

### Trust Hierarchy
- **Root CA** - self-signed, trusted by OS/browser
- **Intermediate CA** - signed by Root CA, signs end-entity certificates
- **End-entity certificate** - server/client certificates
- **CRL/OCSP** - certificate revocation checking

Certificate contains: public key, subject (domain), issuer, validity period, signature.

### Certificate Transparency
Public logs of all issued certificates. Tools: crt.sh, censys.io. Used for:
- Detecting mis-issued certificates
- Subdomain enumeration during reconnaissance

## TLS/SSL

### Protocol Versions
- SSL - all versions deprecated (SSLv3 broken by POODLE attack)
- TLS 1.0/1.1 - deprecated
- TLS 1.2 - current widely supported minimum
- TLS 1.3 - 1-RTT handshake, removed weak ciphers, mandatory PFS

### TLS Handshake (1.2)
```yaml
Client → Server: ClientHello (supported ciphers, random)
Server → Client: ServerHello (chosen cipher, random) + Certificate
Server → Client: Key Exchange parameters
Client → Server: Key Exchange + ChangeCipherSpec
Both: Encrypted application data
```

### TLS Configuration (Nginx)
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
```

### Let's Encrypt
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d example.com -d www.example.com
# Auto-renew via systemd timer: certbot renew
```

## Gotchas
- Encryption at rest without proper key management is security theater - keys stored next to encrypted data provide no protection
- TLS termination at a load balancer means traffic between LB and backend is unencrypted unless re-encrypted
- Certificate pinning prevents MITM but makes certificate rotation painful - use with caution
- `bcrypt` has a 72-byte password limit - longer passwords are silently truncated
- Self-signed certificates encrypt traffic but do not authenticate identity

## See Also
- [[authentication-and-authorization]] - JWT, OAuth, Kerberos use crypto
- [[tls-fingerprinting-and-network-identifiers]] - TCP/IP stack fingerprinting
- [[web-application-security-fundamentals]] - HTTPS, CSP headers
- [[database-security]] - encryption at rest and in transit
