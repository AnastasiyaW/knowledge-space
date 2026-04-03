---
title: FastAPI Authentication and Security
category: frameworks
tags: [python, fastapi, jwt, bcrypt, authentication, authorization, security]
---

# FastAPI Authentication and Security

FastAPI authentication typically uses JWT tokens stored in HTTP-only cookies, with bcrypt password hashing. Authentication verifies identity (who you are); authorization verifies permissions (what you can do).

## Key Facts

- Authentication = credential validation; Authorization = permission checking (sequential steps)
- Passwords hashed with bcrypt (passlib) - never store plaintext
- JWT (JSON Web Token) encodes user identity with expiration time
- HTTP-only cookies prevent JavaScript access to tokens (XSS protection)
- Dependency chain: endpoint -> `get_current_user` -> `get_token_from_cookie` -> verify JWT

## Patterns

### Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### JWT Token Creation
```python
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### Login Endpoint
```python
@router.post("/login")
async def login(response: Response, user_data: UserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", token, httponly=True)
    return {"access_token": token}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "logged out"}
```

### Current User Dependency
```python
async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.JWTError:
        raise HTTPException(status_code=401)
    user_id = payload.get("sub")
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401)
    return user

@app.get("/bookings")
async def get_bookings(user: User = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)
```

### Registration
```python
@router.post("/register")
async def register(user_data: UserRegister):
    existing = await UserDAO.find_one_or_none(email=user_data.email)
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")
    hashed = hash_password(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed)
    return {"status": "registered"}
```

### Custom Exceptions
```python
class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

class IncorrectCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Incorrect email or password")
```

## Gotchas

- Never store plaintext passwords - always bcrypt hash
- JWT `exp` claim uses UTC time - use `datetime.utcnow()`
- HTTP-only cookies not accessible from JavaScript - prevents XSS token theft
- Token expiration doesn't invalidate tokens already issued - use short expiry + refresh tokens
- Always validate token signature and expiration on every request

## See Also

- [[fastapi-fundamentals]] - dependency injection
- [[fastapi-deployment]] - SSL/TLS setup
- [[security/index]] - broader security concepts
