---
title: "Sichere Backend-Entwicklung"
category: techniques
tags: [security, backend, nestjs, express, nodejs, prisma, validation, guards]
level: 3
source_sha256: 6d846016ec488988aead757b8fb4df101740e57df6092c7d2c03c66d100ceacf
translation: machine
translated_at: '2026-10-24'
---
# Sichere Backend-Entwicklung {#secure-backend-development}

Sicherheitsmuster für die Backend-Entwicklung mit Node.js/NestJS/Express: Eingabevalidierung, Authentifizierungs-Guards, RBAC-Middleware, sichere ORM-Nutzung mit Prisma/Mongoose, Fehlerbehandlung, die keine internen Details preisgibt, sowie sichere Deployment-Praktiken.

## Wichtige Fakten {#key-facts}
- `ValidationPipe` mit `whitelist: true` entfernt unbekannte Eigenschaften; `forbidNonWhitelisted: true` weist sie zurück
- NestJS-Guards werden vor den Controllern ausgeführt – sie dienen der Authentifizierung und Autorisierung
- Prisma/Mongoose verwenden standardmäßig parametrisierte Abfragen – rohe Abfragen umgehen diesen Schutz
- Datenbankfehler niemals an Benutzer ausgeben – sie verraten Informationen über das Schema
- Geheimnisse über Umgebungsvariablen bereitstellen (DATABASE_URL, JWT_SECRET) – niemals in Git committen
- HttpOnly-Cookies für Session-Tokens verhindern Session-Diebstahl über XSS

## Eingabevalidierung {#input-validation}

### NestJS Validation Pipe {#nestjs-validation-pipe}
```typescript
// Global pipe
app.useGlobalPipes(new ValidationPipe({
    whitelist: true,           // Strip unknown properties
    forbidNonWhitelisted: true // Reject unknown properties
}));
```

### DTOs mit class-validator {#dtos-with-class-validator}
```typescript
export class CreateMovieDto {
    @IsString()
    @IsNotEmpty()
    title: string;

    @IsString()
    @IsOptional()
    description?: string;

    @IsArray()
    @IsString({ each: true })
    genres: string[];
}
```

### Express-Validierung {#express-validation}
```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/register', [
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 6 }),
    body('name').trim().notEmpty()
], async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
    }
});
```

## Authentifizierungs-Guards {#authentication-guards}

### NestJS JWT Guard {#nestjs-jwt-guard}
```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}

// Usage on controller
@Get('profile')
@UseGuards(JwtAuthGuard)
getProfile(@CurrentUser() user: User) { ... }
```

### Express-Auth-Middleware {#express-auth-middleware}
```javascript
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

## RBAC (Rollenbasierte Zugriffskontrolle) {#rbac-role-based-access-control}
```typescript
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

// Custom decorator
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

// Usage
@Post()
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles('admin')
create(@Body() dto: CreateDto) { ... }
```

## Fehlerbehandlung {#error-handling}
```typescript
// NestJS Exception Filter - safe error responses
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
    catch(exception: HttpException, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const status = exception.getStatus();
        response.status(status).json({
            statusCode: status,
            message: exception.message,    // Safe message only
            timestamp: new Date().toISOString(),
        });
        // Log full error internally, never send to client
    }
}
```

## Sichere ORM-Nutzung {#secure-orm-usage}

### Prisma {#prisma}
```typescript
// Safe - parameterized
const user = await prisma.user.findUnique({ where: { id: userId } });

// Safe - nested creates
const log = await prisma.log.create({
    data: {
        userId: req.userId,
        exercises: { create: [{ name: "Bench Press" }] }
    },
    include: { exercises: true }
});

// DANGEROUS - raw query with interpolation
await prisma.$queryRaw`SELECT * FROM users WHERE id = ${unsafeInput}`;
```

### Mongoose (MongoDB) {#mongoose-mongodb}
```javascript
// Prevent NoSQL injection
const mongoSanitize = require('express-mongo-sanitize');
app.use(mongoSanitize());  // Strips $ operators from user input
```

## NestJS-Architekturmuster {#nestjs-architecture-patterns}

### Middleware (Logging) {#middleware-logging}
```typescript
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
    use(req: Request, res: Response, next: NextFunction) {
        console.log(`${req.method} ${req.url} - ${new Date().toISOString()}`);
        next();
    }
}
```

### Interceptors (Antwort-Transformation) {#interceptors-response-transform}
```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
    intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
        return next.handle().pipe(map(data => ({ data, statusCode: 200 })));
    }
}
```

### Eigene Decorators {#custom-decorators}
```typescript
export const CurrentUser = createParamDecorator(
    (data: unknown, ctx: ExecutionContext) => {
        return ctx.switchToHttp().getRequest().user;
    },
);
```

## Deployment-Sicherheit {#deployment-security}
- Umgebungsvariablen für alle Geheimnisse
- HTTPS über einen Reverse Proxy (Nginx)
- Process Manager (PM2) für Node.js
- `helmet`-Middleware für Sicherheits-Header
- Rate Limiting (`express-rate-limit`)
- CORS-Konfiguration (restriktive Whitelist)
- Den `X-Powered-By`-Header deaktivieren

### Sicherheit von Serverless-Backends {#serverless-backend-security}

```typescript
// Lambda/Cloud Function: validate event source
export async function handler(event: APIGatewayProxyEvent) {
    // Always validate event structure - it could come from any trigger
    if (!event.body || typeof event.body !== 'string') {
        return { statusCode: 400, body: 'Invalid request' };
    }

    // Parse with schema validation
    const parsed = JSON.parse(event.body);
    const validated = schema.safeParse(parsed); // zod
    if (!validated.success) {
        return { statusCode: 400, body: 'Validation failed' };
    }
}
```

### Verwaltung von Geheimnissen {#secrets-management}

```typescript
// Never hardcode secrets - use environment + secrets manager
// BAD
const API_KEY = "sk-1234567890";

// GOOD - from env (set by deployment, not committed)
const API_KEY = process.env.API_KEY;

// BETTER - from secrets manager with caching
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

let cachedSecret: string | null = null;
async function getSecret(name: string): Promise<string> {
    if (cachedSecret) return cachedSecret;
    const client = new SecretsManagerClient({});
    const response = await client.send(new GetSecretValueCommand({ SecretId: name }));
    cachedSecret = response.SecretString!;
    return cachedSecret;
}
```

### Muster für Rate Limiting {#rate-limiting-patterns}

```typescript
// Express with sliding window
import rateLimit from 'express-rate-limit';

// Global rate limit
app.use(rateLimit({
    windowMs: 15 * 60 * 1000,  // 15 minutes
    max: 100,                   // 100 requests per window
    standardHeaders: true,
    legacyHeaders: false,
}));

// Per-endpoint stricter limit for auth
app.use('/api/auth', rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,                     // 5 login attempts per 15 min
    skipSuccessfulRequests: true,
}));
```

## Stolperfallen {#gotchas}
- `whitelist: true` allein weist zusätzliche Felder NICHT zurück – sie werden stillschweigend entfernt. Füge `forbidNonWhitelisted: true` hinzu, um sie abzulehnen
- `$queryRaw` von Prisma mit Template-Literalen ist sicher (tagged template), String-Verkettung hingegen NICHT
- `@Body()` in NestJS ohne `ValidationPipe` führt überhaupt keine Validierung durch – die Pipe muss angewendet werden
- Der MongoDB-Operator `$where` erlaubt die Ausführung von JavaScript – niemals mit Benutzereingaben verwenden
- `express-mongo-sanitize` muss VOR den Route-Handlern angewendet werden, um wirksam zu sein
- Rate Limiting allein nach IP-Adresse ist unzureichend – Angreifer nutzen IP-Rotation. Kombiniere es mit Benutzer-ID, API-Schlüssel oder Fingerprint
- `helmet()` setzt gute Standardwerte, aber `Content-Security-Policy` muss je Anwendung manuell angepasst werden – teste zuerst im Report-Only-Modus
- Geheimnisse in Lambda-Umgebungsvariablen sind über `console.log(process.env)` sichtbar – die vollständige Umgebung niemals in Produktion protokollieren

## Siehe auch {#see-also}
- [[authentication-and-authorization]] – JWT, OAuth, RBAC-Konzepte
- [[sql-injection-deep-dive]] – was parametrisierte Abfragen verhindern
- [[web-application-security-fundamentals]] – XSS, CSRF, IDOR
- [Datenbanksicherheit](database-security.md) – Sicherheitskontrollen auf Datenbankebene
