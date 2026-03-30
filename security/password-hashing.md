---
title: Password Hashing and Storage
category: cryptography
tags: [password, hashing, bcrypt, argon2, salt, credential-storage]
---

# Password Hashing and Storage

## Key Facts

- Passwords must NEVER be stored in plaintext - always use slow, salted hash functions designed for passwords
- Recommended algorithms (in order): Argon2id (winner of Password Hashing Competition 2015), bcrypt, scrypt
- Salt: random value unique per password that prevents rainbow table attacks and ensures identical passwords produce different hashes
- Work factor / cost: intentionally slow computation (bcrypt cost 10-12, Argon2 memory 64MB+) to make brute-force impractical
- MD5, SHA-1, SHA-256 are NOT suitable for passwords - they are too fast (billions of hashes/second on GPU)
- [[jwt-authentication]] issues tokens only after successful password verification
- [[linux-user-security]] stores password hashes in `/etc/shadow` with restricted read access

## Patterns

```javascript
// Node.js bcrypt usage
const bcrypt = require('bcryptjs');

// Registration - hash password
const SALT_ROUNDS = 10;
const hashedPassword = await bcrypt.hash(plainPassword, SALT_ROUNDS);
// Store hashedPassword in database

// Login - verify password
const isValid = await bcrypt.compare(submittedPassword, storedHash);
if (!isValid) throw new UnauthorizedException('Invalid credentials');
```

```python
# Python password hashing with passlib (supports multiple algorithms)
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    default="argon2",
    argon2__memory_cost=65536,  # 64MB
    argon2__time_cost=3,
    argon2__parallelism=4,
    bcrypt__rounds=12,
)

# Hash
hashed = pwd_context.hash("user_password")
# "$argon2id$v=19$m=65536,t=3,p=4$..."

# Verify
is_valid = pwd_context.verify("submitted_password", hashed)

# Check if rehash needed (algorithm upgrade)
needs_update = pwd_context.needs_update(hashed)
```

```bash
# Linux password hash format in /etc/shadow
# $id$salt$hash
# $1$ = MD5 (deprecated)
# $5$ = SHA-256
# $6$ = SHA-512
# $2b$ = bcrypt
# $argon2id$ = Argon2id

# Generate bcrypt hash from command line
python3 -c "import bcrypt; print(bcrypt.hashpw(b'password', bcrypt.gensalt(12)))"
```

## Gotchas

- bcrypt truncates passwords at 72 bytes - for longer passwords, pre-hash with SHA-256 then bcrypt the result
- Cost factor should be calibrated to take ~250ms on your hardware - too fast enables brute force, too slow causes login latency
- NEVER implement custom password hashing - use well-tested libraries (bcrypt, argon2-cffi, passlib)
- Password comparison must be constant-time to prevent timing attacks - bcrypt.compare() handles this internally
- Pepper (server-side secret added to password before hashing) adds defense-in-depth if hash database is stolen
- When upgrading hash algorithm (e.g., bcrypt to argon2), rehash on next successful login, don't force password reset

## See Also

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [CWE-916 Use of Password Hash With Insufficient Effort](https://cwe.mitre.org/data/definitions/916.html)
- [NIST SP 800-63B Section 5.1.1.2 - Memorized Secret Verifiers](https://pages.nist.gov/800-63-3/sp800-63b.html)
