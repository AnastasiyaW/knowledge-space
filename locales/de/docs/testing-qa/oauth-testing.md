---
title: "OAuth- und Authentifizierungstests"
category: patterns
tags: [oauth, oauth2, oidc, pkce, jwt, bearer-token, session, authentication, requests]
level: 3
source_sha256: d53a154e5efb43deb0ddb16a843bb75243437d3ca799728ed6b93a697c75cf6b
translation: machine
translated_at: '2026-10-24'
---
# OAuth- und Authentifizierungstests {#oauth-and-authentication-testing}

Tests für APIs, die OAuth 2.0, OIDC, JWT oder sitzungsbasierte Authentifizierung erfordern. Benutzerdefinierte Requests-Sessions, Token-Verwaltung und PKCE-Flows.

## Überblick über die OAuth-2.0-Flows {#oauth-20-flows-overview}

| Flow | Wann | Testansatz |
|------|------|---------------|
| Client Credentials | Service-to-Service | Direkte Token-Anfrage |
| Authorization Code | Benutzer-Login (Web) | Programmatischer Token-Austausch |
| Authorization Code + PKCE | SPAs, Mobile | Code Verifier + Challenge |
| Resource Owner Password | Nur Legacy/Testing | Direkter Benutzername/Passwort |

## Client-Credentials-Flow {#client-credentials-flow}

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

## Benutzerdefinierte Auth-Session mit automatischer Aktualisierung {#custom-auth-session-with-auto-refresh}

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

## PKCE-Flow (Authorization Code with Proof Key) {#pkce-flow-authorization-code-with-proof-key}

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

## Validierung von JWT-Tokens {#jwt-token-validation}

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

## Sitzungsbasierte Authentifizierung {#session-based-auth}

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

## Testen der Autorisierung (Berechtigungen) {#testing-authorization-permissions}

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

## Allure-Logging für Auth-Requests {#allure-logging-for-auth-requests}

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

## Stolperfallen {#gotchas}

- **Problem:** Token läuft während der Testsuite ab und verursacht kaskadierende 401-Fehler. **Lösung:** Auto-Refresh-Session verwenden (siehe oben). Den Token-Fixture-Scope auf "session" setzen und vor Ablauf proaktiv aktualisieren.

- **Problem:** Der OAuth-Token-Endpunkt liefert 200 mit einem Fehler im Body (`{"error": "invalid_grant"}`) statt eines HTTP-Fehlerstatus. **Lösung:** Immer den Antwort-Body auf das Feld `error` prüfen, nicht nur den Statuscode.

- **Problem:** Tests verwenden einen echten OAuth-Server, der instabil oder langsam ist. **Lösung:** Für Unit-Tests den Token-Endpunkt mocken. Für Integrationstests einen lokalen OAuth-Server verwenden (Keycloak in Docker). Echtes OAuth nur für E2E-Tests einsetzen.

## Siehe auch {#see-also}

- [[api-testing-requests]]
- [[test-data-management]]
- [[allure-reporting]]
