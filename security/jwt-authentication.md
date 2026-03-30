---
title: JWT Authentication
category: web-security
tags: [jwt, authentication, tokens, access-token, refresh-token, authorization]
---

# JWT Authentication

## Key Facts

- JWT (JSON Web Token) is a compact, URL-safe token format for securely transmitting claims between parties (RFC 7519)
- Structure: `header.payload.signature` - three Base64URL-encoded parts separated by dots
- Access token: short-lived (15-60 min), sent with each API request in `Authorization: Bearer <token>` header
- Refresh token: long-lived (7-30 days), used to obtain new access/refresh token pair without re-authentication
- Two-token pattern improves security: stolen access token has limited window; refresh token stored more securely
- [[cors-and-origin-security]] must be configured to restrict which origins can send authentication headers
- [[password-hashing]] secures stored credentials before tokens are ever issued

## Patterns

```javascript
// NestJS JWT authentication setup
// Install: npm install @nestjs/jwt @nestjs/passport passport-jwt bcryptjs

// auth.module.ts
@Module({
  imports: [
    JwtModule.registerAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get('JWT_SECRET'),
        signOptions: { expiresIn: '15m' },
      }),
    }),
  ],
})
export class AuthModule {}

// Generate token pair
async generateTokens(userId: string) {
  const accessToken = this.jwtService.sign(
    { sub: userId, type: 'access' },
    { expiresIn: '15m' }
  );
  const refreshToken = this.jwtService.sign(
    { sub: userId, type: 'refresh' },
    { expiresIn: '7d' }
  );
  return { accessToken, refreshToken };
}

// Refresh endpoint - exchange refresh token for new pair
@Post('auth/refresh')
async refresh(@Body('refreshToken') refreshToken: string) {
  const payload = this.jwtService.verify(refreshToken);
  if (payload.type !== 'refresh') throw new UnauthorizedException();
  return this.generateTokens(payload.sub);
}
```

```python
# Python JWT with PyJWT
import jwt
from datetime import datetime, timedelta

SECRET = 'your-secret-key'

def create_access_token(user_id: str) -> str:
    payload = {
        'sub': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')
```

```
# Token refresh flow:
1. Client sends request with expired access token
2. Server returns 401 Unauthorized
3. Client sends refresh token to /auth/refresh endpoint
4. Server validates refresh token, generates new access + refresh tokens
5. Client retries original request with new access token
6. Old refresh token is invalidated (rotation)
```

## Gotchas

- NEVER store JWT secret in code - use environment variables or secret manager (CWE-798)
- JWTs are NOT encrypted by default - payload is Base64-encoded and readable by anyone; never put sensitive data in payload
- Refresh token rotation: invalidate old refresh token when issuing new pair - prevents reuse of stolen refresh tokens
- localStorage is vulnerable to XSS; httpOnly cookies are safer for token storage but require CSRF protection
- `none` algorithm attack: always validate the `alg` header and reject tokens with `alg: none` (CWE-327)
- Clock skew between servers can cause valid tokens to be rejected - use `leeway` parameter in verification

## See Also

- [RFC 7519 - JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [CWE-287 Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
