---
title: Role-Based Access Control (RBAC)
category: web-security
tags: [rbac, authorization, roles, permissions, access-control, guards]
---

# Role-Based Access Control (RBAC)

## Key Facts

- RBAC assigns permissions to roles, roles to users - users never get permissions directly
- Common roles in web apps: anonymous (unauthenticated), user (authenticated), admin (full access), moderator (partial admin)
- Authorization != Authentication: authentication verifies WHO you are, authorization determines WHAT you can do
- [[jwt-authentication]] tokens carry role claims in payload - decoded server-side to make authorization decisions
- Guards/middleware check role before executing controller logic - reject early with 403 Forbidden
- [[linux-user-security]] implements similar concepts at OS level with user/group/root model

## Patterns

```javascript
// NestJS RBAC implementation
// roles.decorator.ts
import { SetMetadata } from '@nestjs/common';
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

// roles.guard.ts
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>(
      'roles', [context.getHandler(), context.getClass()]
    );
    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}

// Usage in controller
@Get('admin/users')
@Roles('admin')
@UseGuards(JwtAuthGuard, RolesGuard)
async getUsers() { /* only admin can access */ }

@Get('profile')
@Roles('user', 'admin')  // Both roles can access
@UseGuards(JwtAuthGuard, RolesGuard)
async getProfile() { /* authenticated users */ }
```

```python
# Python/FastAPI RBAC pattern
from functools import wraps
from fastapi import HTTPException, Depends

def require_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=Depends(get_current_user), **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

@app.get("/admin/dashboard")
@require_role("admin")
async def admin_dashboard(current_user: User = Depends(get_current_user)):
    return {"message": "Admin only content"}
```

```
# RBAC authorization matrix example:
Resource        | anonymous | user  | moderator | admin
----------------|-----------|-------|-----------|------
GET /movies     | yes       | yes   | yes       | yes
POST /movies    | no        | no    | no        | yes
PUT /movies/:id | no        | no    | yes       | yes
DELETE /movies  | no        | no    | no        | yes
GET /profile    | no        | own   | own       | any
PUT /users/:id  | no        | own   | own       | any
```

## Gotchas

- Never trust role information from the client (cookies, localStorage) - always verify from the token or database server-side
- Role checks must happen on EVERY request, not just at login - roles can change while session is active
- Hierarchical roles (admin > moderator > user) should be explicit - don't assume higher roles inherit lower role permissions
- API endpoints without role guards default to public - adopt deny-by-default pattern
- Horizontal privilege escalation: user A accessing user B's data - RBAC alone doesn't prevent this; need resource-level ownership checks
- Frontend hiding UI elements is NOT authorization - it is UX; backend must enforce all access rules independently

## See Also

- [OWASP Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html)
- [CWE-285 Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)
- [NIST SP 800-162 Guide to ABAC](https://csrc.nist.gov/publications/detail/sp/800-162/final)
