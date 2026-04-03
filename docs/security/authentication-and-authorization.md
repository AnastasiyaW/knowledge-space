---
title: Authentication and Authorization
category: concepts
tags: [security, authentication, authorization, jwt, oauth, kerberos, mfa, rbac]
---

# Authentication and Authorization

Authentication (proving identity) and authorization (granting access) mechanisms: password policies, MFA, JWT tokens, OAuth 2.0/OIDC, Kerberos, RBAC, and PAM. Covers both conceptual patterns and implementation.

## Key Facts
- Authentication = who you are; Authorization = what you can do
- MFA factors: something you know + something you have + something you are
- SMS-based 2FA is the weakest MFA option (SIM swapping, SS7 attacks)
- FIDO2/WebAuthn hardware keys are the strongest consumer MFA
- OAuth 2.0 is for authorization (access tokens); OIDC adds authentication (ID tokens) on top
- NIST 800-63B recommends against forced password rotation - it leads to weaker passwords

## Password Security

### Password Policies (Modern)
- Minimum 12+ characters
- Complexity encouraged but not required (length > complexity per NIST)
- Check against breach databases (Have I Been Pwned API)
- No forced periodic rotation (NIST 800-63B)
- Account lockout after failed attempts (5 attempts, 15-30 min lockout)

### Password Hashing
```python
# bcrypt (recommended)
import bcrypt
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password.encode(), salt)
# Verify
bcrypt.checkpw(input_password.encode(), hashed)
```

```javascript
// Node.js with bcryptjs
const bcrypt = require('bcryptjs');
const salt = await bcrypt.genSalt(10);
const hashed = await bcrypt.hash(password, salt);
const isMatch = await bcrypt.compare(inputPassword, hashed);
```

## Multi-Factor Authentication (MFA)

| Method | Security | UX | Notes |
|--------|----------|-----|-------|
| FIDO2/WebAuthn | Highest | Good | Hardware keys (YubiKey), phishing-resistant |
| TOTP | High | OK | Google Authenticator, Authy - time-based codes |
| Push notifications | High | Good | Mobile app approval |
| SMS codes | Low | Easy | SIM swapping, SS7 interception attacks |

## JWT (JSON Web Tokens)

### Structure
Three Base64-encoded parts separated by dots: `header.payload.signature`

### Implementation (Node.js)
```javascript
const jwt = require('jsonwebtoken');

// Generate
const token = jwt.sign(
  { userId: user.id, email: user.email },
  process.env.JWT_SECRET,
  { expiresIn: '24h' }
);

// Verify middleware
const auth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (e) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

### NestJS JWT Strategy
```typescript
@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.JWT_SECRET,
    });
  }
  async validate(payload: any) {
    return { userId: payload.sub, email: payload.email };
  }
}
```

## OAuth 2.0 / OIDC

- **OAuth 2.0** - authorization framework (grants access tokens)
- **OIDC** (OpenID Connect) - authentication layer on top of OAuth 2.0 (ID tokens)
- Flows: Authorization Code (server apps, most secure), Client Credentials (service-to-service), Implicit (deprecated)

## Kerberos (Active Directory)

Ticket-based authentication - no passwords sent over network:
1. Client authenticates to KDC (Key Distribution Center)
2. KDC issues TGT (Ticket Granting Ticket)
3. Client uses TGT to request service tickets for specific services
4. Service validates ticket without contacting KDC

Kerberos attacks: Kerberoasting, AS-REP Roasting, Golden/Silver Tickets (see [[active-directory-attacks]]).

## LDAP
Directory service protocol for querying/modifying user databases. Used with Active Directory. Port 389 (plaintext), 636 (LDAPS).

## SSO (Single Sign-On)
One authentication grants access to multiple services. Reduces password fatigue, centralizes access control. Risk: SSO compromise = access to everything.

## Patterns

### RBAC (Role-Based Access Control)
```typescript
// NestJS Guard implementation
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}
  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!requiredRoles) return true;
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}
```

### PAM (Privileged Access Management)
- Password vaulting - encrypted credential storage
- Session recording - audit admin sessions
- Just-in-time access - temporary privilege elevation with approval
- Credential rotation - automatic password changes
- Break-glass procedures - emergency access with full audit trail

## Gotchas
- JWT tokens cannot be revoked once issued - use short expiration + refresh tokens
- Storing JWT in localStorage is XSS-vulnerable; HttpOnly cookies are safer but need CSRF protection
- OAuth implicit flow is deprecated - always use Authorization Code + PKCE
- Kerberos clock skew > 5 minutes causes authentication failures
- "Remember me" cookies must still be invalidated on password change

## See Also
- [[cryptography-and-pki]] - underlying crypto mechanisms
- [[web-application-security-fundamentals]] - session management, CSRF
- [[active-directory-attacks]] - Kerberoasting, Golden Ticket
- [[windows-security-and-powershell]] - Windows auth internals, SAM, LSASS
