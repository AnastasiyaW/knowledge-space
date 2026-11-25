---
title: "Tests d'API"
category: technique
tags: [api, rest, grpc, requests, httpx, json-schema, pydantic, protobuf, response-validation]
level: 3
source_sha256: 5431cebda4198dd339822dbe7544fedef28af088c52b5e5b644d22b6403ee1d2
translation: machine
translated_at: '2026-10-24'
---
# Tests d'API {#api-testing}

Les tests d'API valident les services backend via HTTP (REST) ou gRPC. La bibliothèque `requests` de Python associée à Pydantic pour la validation des réponses constitue la pile standard. Pour gRPC, protobuf définit les contrats et la génération de code crée des stubs typés. Les clients HTTP basés sur des sessions, avec journalisation automatique, réduisent le code répétitif.

## Points clés {#key-facts}

- `requests.Session()` conserve les en-têtes et les cookies entre les appels ; les hooks ajoutent automatiquement la journalisation
- Les modèles Pydantic valident la structure des réponses au moment de l'analyse : les erreurs de type sont détectées immédiatement
- Validation JSON Schema pour les tests de contrat : `jsonschema.validate(response, schema)`
- gRPC utilise des fichiers `.proto` pour la définition des services ; `grpcio-tools` génère les stubs Python
- Motif de client HTTP : une classe par service, les fixtures gèrent le cycle de vie
- Le flux OAuth 2.0 + PKCE peut être automatisé dans les fixtures de session pour les API protégées par authentification

## Motifs {#patterns}

### Client HTTP basé sur une session {#session-based-http-client}

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

### Validation des réponses avec Pydantic {#response-validation-with-pydantic}

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

### Tests gRPC {#grpc-testing}

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

### OAuth 2.0 dans les fixtures de test {#oauth-20-in-test-fixtures}

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

## Pièges {#gotchas}

- Les hooks de réponse peuvent journaliser des secrets (en-têtes d'authentification, jetons) : ajoutez des filtres de données sensibles
- `raise_for_status()` après chaque requête : les erreurs 4xx/5xx silencieuses sont la première cause de temps perdu au débogage
- Les codes d'erreur gRPC diffèrent des codes de statut HTTP (UNAVAILABLE, NOT_FOUND, etc.)
- Pydantic v2 utilise `model_validate()` à la place de `parse_obj()` de la v1 : vérifiez votre version

## Voir aussi {#see-also}

- [[pytest-fundamentals]] - fixtures pour le cycle de vie du client
- [[allure-reporting]] - ajout automatique des journaux HTTP
- [[test-architecture]] - organisation des clients HTTP dans les projets de test
