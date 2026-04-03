---
title: Secure Backend Development
category: techniques
tags: [security, backend, nestjs, express, nodejs, prisma, validation, guards]
---

# Secure Backend Development

Security patterns for backend development with Node.js/NestJS/Express: input validation, authentication guards, RBAC middleware, secure ORM usage with Prisma/Mongoose, error handling that does not leak internals, and secure deployment practices.

## Key Facts
- `ValidationPipe` with `whitelist: true` strips unknown properties; `forbidNonWhitelisted: true` rejects them
- NestJS Guards execute before controllers - use for authentication and authorization
- Prisma/Mongoose use parameterized queries by default - raw queries bypass protection
- Never expose database errors to users - they reveal schema information
- Environment variables for secrets (DATABASE_URL, JWT_SECRET) - never commit to git
- HttpOnly cookies for session tokens prevent XSS-based session theft

## Input Validation

### NestJS Validation Pipe
```typescript
// Global pipe
app.useGlobalPipes(new ValidationPipe({
    whitelist: true,           // Strip unknown properties
    forbidNonWhitelisted: true // Reject unknown properties
}));
```

### DTOs with class-validator
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

### Express Validation
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

## Authentication Guards

### NestJS JWT Guard
```typescript
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}

// Usage on controller
@Get('profile')
@UseGuards(JwtAuthGuard)
getProfile(@CurrentUser() user: User) { ... }
```

### Express Auth Middleware
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

## RBAC (Role-Based Access Control)
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

## Error Handling
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

## Secure ORM Usage

### Prisma
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

### Mongoose (MongoDB)
```javascript
// Prevent NoSQL injection
const mongoSanitize = require('express-mongo-sanitize');
app.use(mongoSanitize());  // Strips $ operators from user input
```

## NestJS Architecture Patterns

### Middleware (Logging)
```typescript
@Injectable()
export class LoggerMiddleware implements NestMiddleware {
    use(req: Request, res: Response, next: NextFunction) {
        console.log(`${req.method} ${req.url} - ${new Date().toISOString()}`);
        next();
    }
}
```

### Interceptors (Response Transform)
```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
    intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
        return next.handle().pipe(map(data => ({ data, statusCode: 200 })));
    }
}
```

### Custom Decorators
```typescript
export const CurrentUser = createParamDecorator(
    (data: unknown, ctx: ExecutionContext) => {
        return ctx.switchToHttp().getRequest().user;
    },
);
```

## Deployment Security
- Environment variables for all secrets
- HTTPS via reverse proxy (Nginx)
- Process manager (PM2) for Node.js
- `helmet` middleware for security headers
- Rate limiting (`express-rate-limit`)
- CORS configuration (restrictive whitelist)
- Disable `X-Powered-By` header

## Gotchas
- `whitelist: true` alone does NOT reject extra fields - it silently strips them. Add `forbidNonWhitelisted: true` to reject
- Prisma `$queryRaw` with template literals IS safe (tagged template), but string concatenation is NOT
- NestJS `@Body()` without `ValidationPipe` does no validation at all - pipe must be applied
- MongoDB `$where` operator allows JavaScript execution - never use with user input
- `express-mongo-sanitize` must be applied BEFORE route handlers to be effective

## See Also
- [[authentication-and-authorization]] - JWT, OAuth, RBAC concepts
- [[sql-injection-deep-dive]] - what parameterized queries prevent
- [[web-application-security-fundamentals]] - XSS, CSRF, IDOR
- [[database-security]] - database-level security controls
