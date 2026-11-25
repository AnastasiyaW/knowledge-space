---
title: "FastAPI-Authentifizierung und Sicherheit"
category: frameworks
tags: [python, fastapi, jwt, bcrypt, authentication, authorization, security]
level: 3
source_sha256: 45621fd514c2965d0e1c2a4686fe52c30b392997c72164f50382fdc6ad080a06
translation: machine
translated_at: '2026-10-24'
---
# FastAPI-Authentifizierung und Sicherheit {#fastapi-authentication-and-security}

FastAPI-Authentifizierung verwendet typischerweise JWT-Tokens, die in HTTP-only-Cookies gespeichert werden, zusammen mit bcrypt-Passwort-Hashing. Authentifizierung prüft die Identität (wer du bist); Autorisierung prüft Berechtigungen (was du tun darfst).

## Key Facts {#key-facts}

- Authentifizierung = Prüfung der Anmeldedaten; Autorisierung = Prüfung der Berechtigungen (aufeinanderfolgende Schritte)
- Passwörter werden mit bcrypt (passlib) gehasht - niemals im Klartext speichern
- JWT (JSON Web Token) kodiert die Benutzeridentität zusammen mit einer Ablaufzeit
- HTTP-only-Cookies verhindern den JavaScript-Zugriff auf Tokens (XSS-Schutz)
- Abhängigkeitskette: Endpoint -> `get_current_user` -> `get_token_from_cookie` -> JWT verifizieren

## Patterns {#patterns}

### Passwort-Hashing {#password-hashing}
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### Erstellung von JWT-Tokens {#jwt-token-creation}
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

### Login-Endpoint {#login-endpoint}
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

### Abhängigkeit für den aktuellen Benutzer {#current-user-dependency}
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

### Registrierung {#registration}
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

### Benutzerdefinierte Exceptions {#custom-exceptions}
```python
class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

class IncorrectCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Incorrect email or password")
```

## Gotchas {#gotchas}

- Passwörter niemals im Klartext speichern - immer mit bcrypt hashen
- Der `exp`-Claim eines JWT verwendet UTC-Zeit - `datetime.utcnow()` verwenden
- HTTP-only-Cookies sind aus JavaScript nicht zugänglich - das verhindert den Diebstahl von Tokens durch XSS
- Der Ablauf eines Tokens macht bereits ausgestellte Tokens nicht ungültig - daher kurze Gültigkeitsdauern und Refresh-Tokens verwenden
- Signatur und Ablaufzeit des Tokens bei jeder Anfrage immer validieren

## Siehe auch {#see-also}

- [[fastapi-fundamentals]] - Dependency Injection
- [[fastapi-deployment]] - SSL/TLS-Einrichtung
- [[security/index]] - allgemeinere Sicherheitskonzepte
