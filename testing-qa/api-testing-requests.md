---
title: API Testing with Python
category: technique
tags: [api, rest, requests, httpx, json-schema, http-methods, status-codes]
---
# API Testing with Python

Automated testing of REST APIs using Python HTTP clients - requests, httpx, response validation.

## Key Facts

- `requests` library - synchronous HTTP client, most common for API testing
- `httpx` - modern alternative with async support, HTTP/2, similar API to `requests`
- HTTP methods: GET (read), POST (create), PUT (replace), PATCH (update), DELETE (remove)
- Status codes: 2xx success, 4xx client error, 5xx server error
- Response validation: status code, JSON body fields, JSON schema, response time
- API client class pattern: encapsulates base URL, auth, headers, and endpoint methods
- `jsonschema` library for structural validation of API responses
- Environment-based configuration: base URL, credentials via `.env` files
- [[pydantic-test-validation]] for response model validation with type safety
- [[allure-reporting]] for documenting API test steps and attaching request/response data

## Patterns

```python
import requests
import pytest
from jsonschema import validate

BASE_URL = "https://api.example.com/v1"

# Basic API test
def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "id" in data[0]
    assert "email" in data[0]

# POST with JSON body
def test_create_user():
    payload = {"name": "John", "email": "john@example.com"}
    response = requests.post(
        f"{BASE_URL}/users",
        json=payload,
        headers={"Authorization": "Bearer TOKEN"}
    )
    assert response.status_code == 201
    user = response.json()
    assert user["name"] == "John"

# JSON Schema validation
USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
    }
}

def test_user_schema():
    response = requests.get(f"{BASE_URL}/users/1")
    validate(instance=response.json(), schema=USER_SCHEMA)

# API Client class pattern
class UsersClient:
    def __init__(self, base_url: str, token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        self.base_url = f"{base_url}/users"

    def get_all(self):
        return self.session.get(self.base_url)

    def get_by_id(self, user_id: int):
        return self.session.get(f"{self.base_url}/{user_id}")

    def create(self, name: str, email: str):
        return self.session.post(
            self.base_url,
            json={"name": name, "email": email}
        )

    def delete(self, user_id: int):
        return self.session.delete(f"{self.base_url}/{user_id}")

# Fixture providing API client
@pytest.fixture(scope="session")
def users_client(base_url, auth_token):
    return UsersClient(base_url, auth_token)

def test_crud_flow(users_client):
    # Create
    resp = users_client.create("Test", "test@example.com")
    assert resp.status_code == 201
    user_id = resp.json()["id"]

    # Read
    resp = users_client.get_by_id(user_id)
    assert resp.json()["name"] == "Test"

    # Delete
    resp = users_client.delete(user_id)
    assert resp.status_code == 204

# Using httpx (modern alternative)
import httpx

def test_with_httpx():
    with httpx.Client(base_url=BASE_URL) as client:
        resp = client.get("/users")
        assert resp.status_code == 200

# Enum for API endpoints
from enum import Enum

class Endpoints(str, Enum):
    USERS = "/api/v1/users"
    COURSES = "/api/v1/courses"
    FILES = "/api/v1/files"
```

## Gotchas

- **Symptom**: 401 Unauthorized in tests - **Cause**: expired or missing auth token - **Fix**: refresh token in session-scoped fixture, use env vars for credentials
- **Symptom**: test data conflicts in parallel runs - **Cause**: tests modify shared resources - **Fix**: create unique test data per test, clean up in teardown
- **Symptom**: `requests.post()` sends form data, not JSON - **Cause**: using `data=` instead of `json=` - **Fix**: use `json=payload` parameter for JSON content type
- Never hardcode URLs, tokens, or credentials - use config files or env vars
- Check response time: `assert response.elapsed.total_seconds() < 2`
- Use `requests.Session()` for persistent connections and shared headers

## See Also

- [[pydantic-test-validation]] - Pydantic models for response validation
- [[allure-reporting]] - attaching request/response to reports
- [[test-data-management]] - generating test data with Faker
- [[pytest-fixtures]] - API client fixtures
- [requests docs](https://requests.readthedocs.io/)
- [httpx docs](https://www.python-httpx.org/)
- [jsonschema docs](https://python-jsonschema.readthedocs.io/)
