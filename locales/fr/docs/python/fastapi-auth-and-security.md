---
title: "FastAPI Authentication and Security"
category: frameworks
tags: [python, fastapi, jwt, bcrypt, authentication, authorization, security]
level: 3
source_sha256: 45621fd514c2965d0e1c2a4686fe52c30b392997c72164f50382fdc6ad080a06
translation: machine
translated_at: '2026-10-24'
---
# Authentification et sécurité avec FastAPI {#fastapi-authentication-and-security}

L'authentification dans FastAPI utilise généralement des jetons JWT stockés dans des cookies HTTP-only, avec un hachage des mots de passe via bcrypt. L'authentification vérifie l'identité (qui vous êtes) ; l'autorisation vérifie les permissions (ce que vous pouvez faire).

## Points clés {#key-facts}

- Authentification = validation des identifiants ; autorisation = vérification des permissions (étapes séquentielles)
- Mots de passe hachés avec bcrypt (passlib) - ne jamais stocker de mot de passe en clair
- JWT (JSON Web Token) encode l'identité de l'utilisateur avec une date d'expiration
- Les cookies HTTP-only empêchent JavaScript d'accéder aux jetons (protection contre XSS)
- Chaîne de dépendances : endpoint -> `get_current_user` -> `get_token_from_cookie` -> vérification du JWT

## Modèles {#patterns}

### Hachage des mots de passe {#password-hashing}
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### Création du jeton JWT {#jwt-token-creation}
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

### Endpoint de connexion {#login-endpoint}
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

### Dépendance de l'utilisateur courant {#current-user-dependency}
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

### Inscription {#registration}
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

### Exceptions personnalisées {#custom-exceptions}
```python
class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

class IncorrectCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Incorrect email or password")
```

## Pièges {#gotchas}

- Ne jamais stocker de mots de passe en clair - toujours les hacher avec bcrypt
- La claim `exp` du JWT utilise l'heure UTC - utiliser `datetime.utcnow()`
- Les cookies HTTP-only ne sont pas accessibles depuis JavaScript - cela empêche le vol de jetons par XSS
- L'expiration d'un jeton n'invalide pas les jetons déjà émis - utiliser une durée de vie courte et des jetons de rafraîchissement
- Toujours valider la signature et l'expiration du jeton à chaque requête

## Voir aussi {#see-also}

- [[fastapi-fundamentals]] - injection de dépendances
- [[fastapi-deployment]] - configuration SSL/TLS
- [[security/index]] - concepts de sécurité plus généraux
