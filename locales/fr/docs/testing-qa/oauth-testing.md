---
title: "Tests OAuth et authentification"
category: patterns
tags: [oauth, oauth2, oidc, pkce, jwt, bearer-token, session, authentication, requests]
level: 3
source_sha256: d53a154e5efb43deb0ddb16a843bb75243437d3ca799728ed6b93a697c75cf6b
translation: machine
translated_at: '2026-10-24'
---
# Tests OAuth et authentification {#oauth-and-authentication-testing}

Tests d'API nécessitant une authentification OAuth 2.0, OIDC, JWT ou basée sur des sessions. Sessions de requêtes personnalisées, gestion des tokens et flux PKCE.

## Vue d'ensemble des flux OAuth 2.0 {#oauth-20-flows-overview}

| Flux | Quand | Approche de test |
|------|-------|------------------|
| Client Credentials | Service à service | Demande directe de token |
| Authorization Code | Connexion utilisateur (web) | Échange de token programmatique |
| Authorization Code + PKCE | SPA, mobile | Code verifier + challenge |
| Resource Owner Password | Héritage/tests uniquement | Nom d'utilisateur/mot de passe directs |

## Flux Client Credentials {#client-credentials-flow}

```python
import requests

@pytest.fixture(scope="session")
def access_token(config):
    resp = requests.post(config.token_url, data={
        "grant_type": "client_credentials",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "scope": "read write",
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

@pytest.fixture
def auth_client(access_token):
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {access_token}"
    return session
```

## Session d'authentification personnalisée avec renouvellement automatique {#custom-auth-session-with-auto-refresh}

```python
class AuthSession(requests.Session):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self._token = None
        self._expires_at = 0

    def _get_token(self):
        if time.time() >= self._expires_at:
            resp = requests.post(self.config.token_url, data={
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            })
            data = resp.json()
            self._token = data["access_token"]
            self._expires_at = time.time() + data["expires_in"] - 60
        return self._token

    def request(self, method, url, **kwargs):
        self.headers["Authorization"] = f"Bearer {self._get_token()}"
        return super().request(method, url, **kwargs)
```

## Flux PKCE (Authorization Code avec Proof Key) {#pkce-flow-authorization-code-with-proof-key}

```python
import hashlib
import base64
import secrets

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return code_verifier, code_challenge

def test_pkce_flow(config):
    verifier, challenge = generate_pkce_pair()

    # Step 1: Authorization request (normally in browser)
    auth_params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "scope": "openid profile",
    }

    # Step 2: Exchange code for token
    token_resp = requests.post(config.token_url, data={
        "grant_type": "authorization_code",
        "code": auth_code,  # obtained from redirect
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "code_verifier": verifier,
    })
    assert token_resp.status_code == 200
    assert "access_token" in token_resp.json()
```

## Validation des tokens JWT {#jwt-token-validation}

```python
import jwt

def test_token_claims(access_token):
    # Decode without verification (for inspection only)
    claims = jwt.decode(access_token, options={"verify_signature": False})
    assert claims["iss"] == "https://auth.example.com"
    assert claims["aud"] == "my-api"
    assert claims["exp"] > time.time()
    assert "read" in claims.get("scope", "").split()
```

## Authentification basée sur les sessions {#session-based-auth}

```python
@pytest.fixture
def logged_in_client(config):
    session = requests.Session()
    resp = session.post(f"{config.base_url}/login", data={
        "username": config.test_user,
        "password": config.test_password,
    })
    assert resp.status_code == 200
    # Session cookies are automatically stored
    return session
```

## Tests d'autorisation (permissions) {#testing-authorization-permissions}

```python
@pytest.mark.parametrize("role,endpoint,expected", [
    ("admin", "/api/users", 200),
    ("user", "/api/users", 403),
    ("admin", "/api/settings", 200),
    ("user", "/api/settings", 403),
    ("anonymous", "/api/users", 401)])
def test_role_permissions(make_auth_client, role, endpoint, expected):
    client = make_auth_client(role=role)
    resp = client.get(endpoint)
    assert resp.status_code == expected
```

## Journalisation Allure pour les requêtes d'authentification {#allure-logging-for-auth-requests}

```python
import allure

class AllureAuthSession(AuthSession):
    def request(self, method, url, **kwargs):
        with allure.step(f"{method.upper()} {url}"):
            resp = super().request(method, url, **kwargs)
            allure.attach(str(resp.status_code), "Status")
            allure.attach(resp.text[:1000], "Response Body")
            return resp
```

## Pièges courants {#gotchas}

- **Problème :** Le token expire en cours de suite de tests, provoquant une cascade d'échecs 401. **Solution :** Utiliser la session à renouvellement automatique (ci-dessus). Définir la portée de la fixture de token à « session » et renouveler proactivement avant l'expiration.

- **Problème :** Le endpoint de token OAuth renvoie 200 avec une erreur dans le corps (`{"error": "invalid_grant"}`) au lieu d'un code d'erreur HTTP. **Solution :** Toujours vérifier le champ d'erreur dans le corps de la réponse, et pas seulement le code de statut.

- **Problème :** Les tests utilisent un vrai serveur OAuth, peu fiable et lent. **Solution :** Pour les tests unitaires, simuler (mocker) le endpoint de token. Pour les tests d'intégration, utiliser un serveur OAuth local (Keycloak dans Docker). Réserver le vrai OAuth aux tests E2E uniquement.

## Voir aussi {#see-also}

- [[api-testing-requests]]
- [[test-data-management]]
- [[allure-reporting]]
