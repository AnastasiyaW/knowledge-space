---
title: "API-Testing"
category: technique
tags: [api, rest, grpc, requests, httpx, json-schema, pydantic, protobuf, response-validation]
level: 3
source_sha256: 5431cebda4198dd339822dbe7544fedef28af088c52b5e5b644d22b6403ee1d2
translation: machine
translated_at: '2026-10-24'
---
# API-Testing {#api-testing}

API-Tests validieren Backend-Services über HTTP (REST) oder gRPC. Python-`requests` in Kombination mit Pydantic zur Response-Validierung ist der Standard-Stack. Für gRPC definieren Protobuf-Dateien die Verträge, und Code-Generierung erzeugt typisierte Stubs. Session-basierte HTTP-Clients mit automatischem Logging reduzieren Boilerplate.

## Wichtige Fakten {#key-facts}

- `requests.Session()` speichert Header und Cookies über mehrere Aufrufe hinweg; Hooks hängen Logging automatisch an
- Pydantic-Modelle validieren die Struktur der Response beim Parsen - Typfehler werden sofort erkannt
- JSON-Schema-Validierung für Contract-Tests: `jsonschema.validate(response, schema)`
- gRPC verwendet `.proto`-Dateien zur Service-Definition; `grpcio-tools` generiert Python-Stubs
- HTTP-Client-Klassenmuster: eine Klasse pro Service, Fixtures verwalten den Lebenszyklus
- OAuth 2.0 + PKCE-Flow lässt sich in Session-Fixtures für auth-geschützte APIs automatisieren

## Muster {#patterns}

### Session-basierter HTTP-Client {#session-based-http-client}

```python
class SpendHttpClient:
    def __init__(self, base_url: str, token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })
        self.session.hooks["response"].append(self._log_response)
        self.base_url = base_url

    @staticmethod
    def _log_response(response, *args, **kwargs):
        allure.attach(
            body=response.text,
            name=f"{response.request.method} {response.url} [{response.status_code}]",
            attachment_type=allure.attachment_type.TEXT,
        )

    def get_categories(self):
        resp = self.session.get(f"{self.base_url}/api/categories/all")
        resp.raise_for_status()
        return resp.json()
```

### Response-Validierung mit Pydantic {#response-validation-with-pydantic}

```python
from pydantic import BaseModel

class Category(BaseModel):
    id: str
    category: str
    username: str

class CategoryList(BaseModel):
    items: list[Category]

# In test
response = client.get_categories()
categories = [Category(**item) for item in response]
# Pydantic raises ValidationError if structure doesn't match
```

### gRPC-Tests {#grpc-testing}

```protobuf
// service.proto
service CurrencyService {
    rpc GetAllCurrencies (google.protobuf.Empty) returns (CurrencyResponse) {}
    rpc CalculateRate (CalculateRequest) returns (CalculateResponse) {}
}
```

```python
import grpc
from generated import currency_pb2, currency_pb2_grpc

channel = grpc.insecure_channel("localhost:50051")
stub = currency_pb2_grpc.CurrencyServiceStub(channel)

response = stub.GetAllCurrencies(currency_pb2.Empty())
assert len(response.allCurrencies) > 0
```

### OAuth 2.0 in Test-Fixtures {#oauth-20-in-test-fixtures}

```python
@pytest.fixture(scope="session")
def auth_session(auth_url, client_id, username, password):
    session = requests.Session()
    # Step 1: get authorization code
    auth_resp = session.post(f"{auth_url}/authorize", data={
        "client_id": client_id, "response_type": "code",
        "username": username, "password": password,
    }, allow_redirects=False)
    code = parse_qs(urlparse(auth_resp.headers["Location"]).query)["code"][0]
    # Step 2: exchange for token
    token_resp = session.post(f"{auth_url}/token", data={
        "grant_type": "authorization_code", "code": code,
    })
    session.headers["Authorization"] = f"Bearer {token_resp.json()['access_token']}"
    return session
```

## Fallstricke {#gotchas}

- Response-Hooks können Secrets protokollieren (Auth-Header, Tokens) - füge Filter für sensible Daten hinzu
- `raise_for_status()` nach jedem Request aufrufen - stille 4xx/5xx-Fehler sind die größte Zeitfalle beim Debugging
- gRPC-Fehlercodes unterscheiden sich von HTTP-Statuscodes (UNAVAILABLE, NOT_FOUND usw.)
- Pydantic v2 verwendet `model_validate()` statt `parse_obj()` aus v1 - prüfe deine Version

## Siehe auch {#see-also}

- [[pytest-fundamentals]] - Fixtures für den Client-Lebenszyklus
- [[allure-reporting]] - automatisches Anhängen von HTTP-Logs
- [[test-architecture]] - Organisation von HTTP-Clients in Testprojekten
