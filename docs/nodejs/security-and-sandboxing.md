---
title: Security and Sandboxing
category: operations
tags: [nodejs, security, crypto, vm, sandbox, password-hashing, macaroons, jwt]
---

# Security and Sandboxing

Node.js security encompasses password hashing with salt, token-based authentication, sandboxed code execution via the `vm` module, and context isolation for multi-tenant applications. Understanding both cryptographic primitives and runtime isolation is essential for server-side security.

## Key Facts

- UUID v4: 128 bits total, 122 random bits, ~10 billion years to find a collision
- Use UUID for: session tokens, request context IDs, file identifiers, database keys
- **Macaroons** (Google's token format) are better than JWT: more honest security model, support attenuation (adding restrictions to existing tokens)
- Macaroons have poor JavaScript library support - low adoption because JWT is overhyped
- TypeScript 5 introduced standard decorators (replacing experimental) with `reflect-metadata` for runtime reflection

## Patterns

### Password Hashing with Salt

```js
const crypto = require('node:crypto');

const hashPassword = (password) => {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.scryptSync(password, salt, 64).toString('hex');
  return `${salt}:${hash}`;
};

const verifyPassword = (password, stored) => {
  const [salt, hash] = stored.split(':');
  const derived = crypto.scryptSync(password, salt, 64).toString('hex');
  return hash === derived;
};
```

**Why salt:** Without salt, identical passwords produce identical hashes. Rainbow tables can reverse common passwords. Salt makes every hash unique.

### Sandboxed Code Execution

```js
const vm = require('vm');

class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

const context = vm.createContext({
  AppError,
  // Only expose safe APIs to untrusted code
});

const result = vm.runInContext(userCode, context, { timeout: 5000 });
// instanceof AppError distinguishes app errors from system errors
// Never expose system error details to untrusted code
```

### Multi-Framework Security Comparison

Same security layer across Pure Node.js, Fastify, NestJS, Metarhia:
- User registration and authentication
- Session management with TTL
- Context isolation per connection
- Different DB permissions per user session

## NPM Security

- `npm test` - run tests from package.json scripts
- `npm audit` - check for known vulnerabilities
- Always read npm docs for available flags - 3-5 minutes of reading saves hours of guessing
- Review dependencies before adding - quality of npm packages directly impacts security

## Gotchas

- `vm` module is NOT a security sandbox - determined attacker can escape it. Use isolated processes or containers for true isolation
- Timing attacks on string comparison: use `crypto.timingSafeEqual()` for password verification
- Macaroons offer superior security model but ecosystem support in JS is limited

## See Also

- [[application-architecture]] - context isolation levels (call, connection, session, application)
- [[error-handling]] - AppError vs system errors, safe error propagation
- [[modules-and-packages]] - npm security and dependency management
