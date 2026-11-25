---
title: "Tests gRPC avec Python"
category: tools
tags: [grpc, protobuf, api-testing, code-generation, interceptors, wiremock, mocking]
level: 3
source_sha256: 6f887d72ea9ce97c14a3eb48055ee9445098a09b2c89b945cc5fb10005a58e70
translation: machine
translated_at: '2026-10-24'
---
# Tests gRPC avec Python {#grpc-testing-with-python}

Tests de services gRPC : compilation protobuf, génération de clients, intercepteurs pour la journalisation, intégration Allure et mocking avec WireMock.

## Du protobuf vers Python {#protobuf-to-python}

```protobuf
// user.proto
syntax = "proto3";
package userservice;

service UserService {
  rpc GetUser (GetUserRequest) returns (UserResponse);
  rpc CreateUser (CreateUserRequest) returns (UserResponse);
  rpc ListUsers (Empty) returns (stream UserResponse);
}

message GetUserRequest {
  string user_id = 1;
}

message UserResponse {
  string id = 1;
  string name = 2;
  string email = 3;
}
```

Compilation :

```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  --pyi_out=./generated \
  proto/user.proto
```

Résultat : `user_pb2.py` (messages), `user_pb2_grpc.py` (stubs), `user_pb2.pyi` (indications de types).

## Test gRPC de base {#basic-grpc-test}

```python
import grpc
from generated import user_pb2, user_pb2_grpc

@pytest.fixture(scope="session")
def grpc_channel(config):
    channel = grpc.insecure_channel(config.grpc_host)
    yield channel
    channel.close()

@pytest.fixture
def user_stub(grpc_channel):
    return user_pb2_grpc.UserServiceStub(grpc_channel)

def test_get_user(user_stub):
    request = user_pb2.GetUserRequest(user_id="123")
    response = user_stub.GetUser(request)
    assert response.name != ""
    assert "@" in response.email
```

## Intercepteurs pour la journalisation {#interceptors-for-logging}

```python
class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        method = client_call_details.method
        print(f"gRPC Request: {method}")
        print(f"Payload: {request}")

        response = continuation(client_call_details, request)

        print(f"gRPC Response: {response.result()}")
        return response

# Apply interceptor
channel = grpc.insecure_channel(host)
channel = grpc.intercept_channel(channel, LoggingInterceptor())
```

## Intégration Allure {#allure-integration}

```python
import allure

class AllureInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        method = client_call_details.method
        with allure.step(f"gRPC: {method}"):
            allure.attach(str(request), "Request", allure.attachment_type.TEXT)
            response = continuation(client_call_details, request)
            allure.attach(str(response.result()), "Response", allure.attachment_type.TEXT)
        return response
```

## Mocking avec WireMock {#mocking-with-wiremock}

WireMock prend en charge le mocking gRPC via une extension :

```json
{
  "request": {
    "method": "POST",
    "urlPathPattern": "/userservice.UserService/GetUser"
  },
  "response": {
    "status": 200,
    "headers": {
      "Content-Type": "application/grpc"
    },
    "body": "base64-encoded-protobuf"
  }
}
```

Basculer entre le service réel et le mock :

```python
@pytest.fixture
def grpc_channel(config):
    if config.use_mock:
        host = config.wiremock_host
    else:
        host = config.grpc_host
    return grpc.insecure_channel(host)
```

## Gestion des fichiers proto avec pbreflect {#proto-file-management-with-pbreflect}

```bash
pip install grpc-reflection
```

Télécharger les fichiers `.proto` depuis un serveur en cours d'exécution :

```python
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc

def get_service_protos(channel):
    stub = reflection_pb2_grpc.ServerReflectionStub(channel)
    # list services, then get file descriptors
```

Utile lorsque les fichiers proto ne sont pas partagés directement.

## RPC en flux {#streaming-rpcs}

```python
def test_list_users_stream(user_stub):
    """Server streaming: one request, multiple responses."""
    request = user_pb2.Empty()
    users = list(user_stub.ListUsers(request))
    assert len(users) > 0
    for user in users:
        assert user.id != ""
```

## Pièges courants {#gotchas}

- **Problème :** `grpc._channel._InactiveRpcError` avec le statut `UNAVAILABLE` : le serveur est injoignable. **Solution :** Vérifier la connectivité du canal avant les tests : `grpc.channel_ready_future(channel).result(timeout=5)`. Ajouter une logique de nouvelle tentative ou une attente du port dans la CI.

- **Problème :** Les modifications des fichiers proto cassent silencieusement le code généré : les anciens stubs restent importables mais les champs sont incorrects. **Solution :** Régénérer les stubs dans la CI à chaque build. Épingler les versions des fichiers proto. Ajouter une étape de compilation proto dans votre Makefile.

- **Problème :** Les intercepteurs avalent les exceptions : le test réussit alors que l'appel gRPC a échoué. **Solution :** Toujours appeler `.result()` sur le future de la réponse et vérifier la présence de `grpc.RpcError`.

## Voir aussi {#see-also}

- [[api-testing-requests]]
- [[allure-reporting]]
- [[docker-test-environments]]
