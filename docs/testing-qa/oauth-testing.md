---
title: OAuth and Authentication Testing
category: patterns
tags: [oauth, oauth2, oidc, pkce, jwt, bearer-token, session, authentication, requests]
---

# OAuth and Authentication Testing

Testing APIs that require OAuth 2.0, OIDC, JWT, or session-based authentication. Custom requests sessions, token management, and PKCE flows.

## OAuth 2.0 Flows Overview

| Flow | When | Test approach |
|------|------|---------------|
| Client Credentials | Service-to-service | Direct token request |
| Authorization Code | User login (web) | Programmatic token exchange |
| Authorization Code + PKCE | SPAs, mobile | Code verifier + challenge |
| Resource Owner Password | Legacy/testing only | Direct username/password |

## Client Credentials Flow

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

## Custom Auth Session with Auto-Refresh

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

## PKCE Flow (Authorization Code with Proof Key)

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

## JWT Token Validation

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

## Session-Based Auth

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

## Testing Authorization (Permissions)

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

## Allure Logging for Auth Requests

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

## Gotchas

- **Issue:** Token expires mid-test-suite, causing cascading 401 failures. **Fix:** Use auto-refresh session (above). Set token fixture scope to "session" and refresh proactively before expiry.

- **Issue:** OAuth token endpoint returns 200 with error in body (`{"error": "invalid_grant"}`) instead of HTTP error status. **Fix:** Always check response body for error field, not just status code.

- **Issue:** Tests use real OAuth server which is flaky/slow. **Fix:** For unit tests, mock the token endpoint. For integration tests, use a local OAuth server (Keycloak in Docker). Keep real OAuth for E2E only.

## See Also

- [[api-testing-requests]]
- [[test-data-management]]
- [[allure-reporting]]
