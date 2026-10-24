---
title: "Développement backend sécurisé"
category: techniques
tags: [security, backend, nestjs, express, nodejs, prisma, validation, guards]
level: 3
source_sha256: 6d846016ec488988aead757b8fb4df101740e57df6092c7d2c03c66d100ceacf
translation: machine
translated_at: '2026-10-24'
---
# Développement backend sécurisé {#secure-backend-development}

Patrons de sécurité pour le développement backend avec Node.js, NestJS et Express : validation des entrées, guards d'authentification, middleware RBAC, usage sécurisé des ORM Prisma et Mongoose, gestion des erreurs qui ne divulgue pas les détails internes, et pratiques de déploiement sécurisé.

## Points clés {#key-facts}
- `ValidationPipe` avec `whitelist: true` supprime les propriétés inconnues ; `forbidNonWhitelisted: true` les rejette
- Les Guards NestJS s'exécutent avant les contrôleurs : à utiliser pour l'authentification et l'autorisation
- Prisma et Mongoose utilisent des requêtes paramétrées par défaut : les requêtes brutes contournent cette protection
- Ne jamais exposer les erreurs de base de données aux utilisateurs : elles révèlent des informations sur le schéma
- Variables d'environnement pour les secrets (DATABASE_URL, JWT_SECRET) : ne jamais les committer dans git
- Les cookies HttpOnly pour les jetons de session empêchent le vol de session par XSS

## Validation des entrées {#input-validation}

### ValidationPipe NestJS {#nestjs-validation-pipe}
```typescript
// Global pipe
app.useGlobalPipes(new ValidationPipe({
    whitelist: true,           // Strip unknown properties
    forbidNonWhitelisted: true // Reject unknown properties
}));
```

### DTOs avec class-validator {#dtos-with-class-validator}
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

### Validation avec Express {#express-validation}
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

## Guards d'authentification {#authentication-guards}

### Guard JWT NestJS {#nestjs-jwt-guard}
```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}

// Usage on controller
@Get('profile')
@UseGuards(JwtAuthGuard)
getProfile(@CurrentUser() user: User) { ... }
```

### Middleware d'authentification Express {#express-auth-middleware}
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

## RBAC (contrôle d'accès basé sur les rôles) {#rbac-role-based-access-control}
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

## Gestion des erreurs {#error-handling}
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

## Usage sécurisé des ORM {#secure-orm-usage}

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

## Patrons d'architecture NestJS {#nestjs-architecture-patterns}

### Middleware (journalisation) {#middleware-logging}
```typescript
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
    use(req: Request, res: Response, next: NextFunction) {
        console.log(`${req.method} ${req.url} - ${new Date().toISOString()}`);
        next();
    }
}
```

### Interceptors (transformation des réponses) {#interceptors-response-transform}
```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
    intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
        return next.handle().pipe(map(data => ({ data, statusCode: 200 })));
    }
}
```

### Décorateurs personnalisés {#custom-decorators}
```typescript
export const CurrentUser = createParamDecorator(
    (data: unknown, ctx: ExecutionContext) => {
        return ctx.switchToHttp().getRequest().user;
    },
);
```

## Sécurité du déploiement {#deployment-security}
- Variables d'environnement pour tous les secrets
- HTTPS via un reverse proxy (Nginx)
- Gestionnaire de processus (PM2) pour Node.js
- Middleware `helmet` pour les en-têtes de sécurité
- Limitation de débit (`express-rate-limit`)
- Configuration CORS restrictive (liste blanche)
- Désactiver l'en-tête `X-Powered-By`

### Sécurité des backends serverless {#serverless-backend-security}

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

### Gestion des secrets {#secrets-management}

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

### Patrons de limitation de débit {#rate-limiting-patterns}

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

## Pièges courants {#gotchas}
- `whitelist: true` seul ne rejette PAS les champs en trop : il les supprime silencieusement. Ajouter `forbidNonWhitelisted: true` pour les rejeter
- Les `$queryRaw` de Prisma avec des template literals SONT sûrs (tagged template), mais la concaténation de chaînes ne l'est PAS
- Un `@Body()` NestJS sans `ValidationPipe` ne effectue aucune validation : le pipe doit être appliqué
- L'opérateur `$where` de MongoDB permet l'exécution de JavaScript : ne jamais l'utiliser avec des entrées utilisateur
- `express-mongo-sanitize` doit être appliqué AVANT les gestionnaires de routes pour être efficace
- La limitation de débit par adresse IP seule est insuffisante : les attaquants changent d'IP. La combiner avec l'identifiant utilisateur, une clé d'API ou une empreinte
- `helmet()` fournit de bonnes valeurs par défaut, mais `Content-Security-Policy` doit être ajustée manuellement pour chaque application : tester d'abord en mode report-only
- Les secrets dans les variables d'environnement Lambda sont visibles via `console.log(process.env)` : ne jamais journaliser l'environnement complet en production

## Voir aussi {#see-also}
- [[authentication-and-authorization]] - concepts JWT, OAuth, RBAC
- [[sql-injection-deep-dive]] - ce que les requêtes paramétrées empêchent
- [[web-application-security-fundamentals]] - XSS, CSRF, IDOR
- [Sécurité des bases de données](database-security.md) - contrôles de sécurité au niveau de la base de données
