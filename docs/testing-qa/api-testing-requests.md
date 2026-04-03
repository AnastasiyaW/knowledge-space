---
title: API Testing
category: technique
tags: [api, rest, grpc, requests, httpx, json-schema, pydantic, protobuf, response-validation]
---

# API Testing

API testing validates backend services via HTTP (REST) or gRPC. Python's `requests` library + Pydantic for response validation is the standard stack. For gRPC, protobuf defines contracts and code-generation creates typed stubs. Session-based HTTP clients with automatic logging reduce boilerplate.

## Key Facts

- `requests.Session()` persists headers/cookies across calls; hooks auto-attach logging
- Pydantic models validate response structure at parse time - type errors caught immediately
- JSON Schema validation for contract testing: `jsonschema.validate(response, schema)`
- gRPC uses `.proto` files for service definition; `grpcio-tools` generates Python stubs
- HTTP client class pattern: one class per service, fixtures manage lifecycle
- OAuth 2.0 + PKCE flow can be automated in session fixtures for auth-protected APIs

## Patterns

### Session-Based HTTP Client

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

### Response Validation with Pydantic

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

### gRPC Testing

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

### OAuth 2.0 in Test Fixtures

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

## Gotchas

- Response hooks may log secrets (auth headers, tokens) - add sensitive data filters
- `raise_for_status()` after every request - silent 4xx/5xx errors are the #1 debugging time sink
- gRPC error codes differ from HTTP status codes (UNAVAILABLE, NOT_FOUND, etc.)
- Pydantic v2 uses `model_validate()` instead of v1's `parse_obj()` - check your version

## See Also

- [[pytest-fundamentals]] - fixtures for client lifecycle
- [[allure-reporting]] - auto-attaching HTTP logs
- [[test-architecture]] - HTTP client organization in test projects
