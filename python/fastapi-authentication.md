---
title: FastAPI Authentication
category: concepts
tags: [python, fastapi, jwt, oauth2, authentication, security, bcrypt, cors]
---

# FastAPI Authentication

FastAPI provides built-in security utilities for OAuth2, JWT tokens, API keys, and HTTP Basic auth. The security module integrates with the OpenAPI spec, automatically adding authentication UI to the docs. JWT (JSON Web Tokens) with bearer scheme is the most common pattern for REST APIs.

## Key Facts

- `OAuth2PasswordBearer(tokenUrl="/auth/token")` creates a dependency that extracts the bearer token from the `Authorization` header
- JWT tokens are encoded with `python-jose` or `PyJWT`; contain claims (sub, exp, iss)
- Password hashing with `passlib` (bcrypt) or `argon2-cffi` -- never store plain passwords
- `HTTPBearer`, `HTTPBasic`, `APIKeyHeader` are alternative security schemes
- Scopes provide fine-grained permission control (e.g., `read:users`, `write:items`)
- `SecurityScopes` dependency provides scope checking in dependencies
- CORS middleware is essential for browser-based clients accessing the API
- See [[fastapi-dependency-injection]] for `Depends` patterns, [[fastapi-fundamentals]] for middleware

## Patterns

### JWT Authentication Flow

```python
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "your-secret-key"  # use env variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str | None = None

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
```

### Current User Dependency

```python
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DBSession,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/users/me")
async def read_current_user(user: CurrentUser):
    return user
```

### Login Endpoint

```python
@app.post("/auth/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession,
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")
```

### Role-Based Access Control

```python
from enum import Enum

class Role(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"

def require_role(*roles: Role):
    async def check_role(user: CurrentUser):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return check_role

AdminUser = Annotated[User, Depends(require_role(Role.admin))]

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, admin: AdminUser, db: DBSession):
    ...
```

### Refresh Token Pattern

```python
REFRESH_TOKEN_EXPIRE_DAYS = 7

@app.post("/auth/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: DBSession,
):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(400, "Invalid token type")
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    user = await db.get(User, int(user_id))
    if not user:
        raise HTTPException(401, "User not found")

    new_access = create_access_token({"sub": str(user.id)})
    return Token(access_token=new_access, token_type="bearer")
```

### API Key Authentication

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(
    api_key: Annotated[str, Depends(api_key_header)],
    db: DBSession,
) -> APIClient:
    client = await db.execute(
        select(APIClient).where(APIClient.key == api_key, APIClient.is_active == True)
    )
    client = client.scalar_one_or_none()
    if not client:
        raise HTTPException(403, "Invalid or inactive API key")
    return client
```

## Gotchas

- **JWT tokens cannot be invalidated**: once issued, a JWT is valid until expiry. For logout, use a token blacklist (Redis) or short-lived access tokens with refresh tokens
- **`SECRET_KEY` must be truly secret**: a leaked key allows forging any JWT. Use a random 256-bit key, store in environment variables, rotate periodically
- **`OAuth2PasswordRequestForm` uses form data**: the login endpoint receives `username` and `password` as form fields (`application/x-www-form-urlencoded`), not JSON. This is per OAuth2 spec
- **bcrypt version compatibility**: `passlib` with `bcrypt>=4.1` may raise warnings. Pin `passlib[bcrypt]` and `bcrypt<4.1` or migrate to `argon2-cffi`
- **CORS must be configured for browser access**: without `CORSMiddleware`, browsers block cross-origin requests. Include `allow_credentials=True` if sending cookies/auth headers

## See Also

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [python-jose](https://python-jose.readthedocs.io/)
- [[fastapi-dependency-injection]] - dependency patterns for auth
- [[fastapi-fundamentals]] - middleware and CORS setup
