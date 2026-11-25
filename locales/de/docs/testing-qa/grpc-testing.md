---
title: "gRPC-Tests mit Python"
category: tools
tags: [grpc, protobuf, api-testing, code-generation, interceptors, wiremock, mocking]
level: 3
source_sha256: 6f887d72ea9ce97c14a3eb48055ee9445098a09b2c89b945cc5fb10005a58e70
translation: machine
translated_at: '2026-10-24'
---
# gRPC-Tests mit Python {#grpc-testing-with-python}

Testen von gRPC-Services: Protobuf-Kompilierung, Client-Generierung, Interceptors für Logging, Allure-Integration und Mocking mit WireMock.

## Protobuf nach Python {#protobuf-to-python}

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

Kompilieren:

```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  --pyi_out=./generated \
  proto/user.proto
```

Ausgabe: `user_pb2.py` (Nachrichten), `user_pb2_grpc.py` (Stubs), `user_pb2.pyi` (Typhinweise).

## Einfacher gRPC-Test {#basic-grpc-test}

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

## Interceptors für Logging {#interceptors-for-logging}

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

## Allure-Integration {#allure-integration}

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

## Mocking mit WireMock {#mocking-with-wiremock}

WireMock unterstützt gRPC-Mocking über eine Erweiterung:

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

Wechsel zwischen echtem Service und Mock:

```python
@pytest.fixture
def grpc_channel(config):
    if config.use_mock:
        host = config.wiremock_host
    else:
        host = config.grpc_host
    return grpc.insecure_channel(host)
```

## Verwaltung von Proto-Dateien mit pbreflect {#proto-file-management-with-pbreflect}

```bash
pip install grpc-reflection
```

`.proto`-Dateien von einem laufenden Server herunterladen:

```python
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc

def get_service_protos(channel):
    stub = reflection_pb2_grpc.ServerReflectionStub(channel)
    # list services, then get file descriptors
```

Nützlich, wenn Proto-Dateien nicht direkt weitergegeben werden.

## Streaming-RPCs {#streaming-rpcs}

```python
def test_list_users_stream(user_stub):
    """Server streaming: one request, multiple responses."""
    request = user_pb2.Empty()
    users = list(user_stub.ListUsers(request))
    assert len(users) > 0
    for user in users:
        assert user.id != ""
```

## Fallstricke {#gotchas}

- **Problem:** `grpc._channel._InactiveRpcError` mit `UNAVAILABLE`-Status – Server nicht erreichbar. **Lösung:** Vor den Tests die Channel-Verbindung prüfen: `grpc.channel_ready_future(channel).result(timeout=5)`. In der CI Retry-Logik oder Warten auf den Port ergänzen.

- **Problem:** Änderungen an Proto-Dateien machen den generierten Code stillschweigend fehlerhaft – alte Stubs sind weiterhin importierbar, aber die Felder stimmen nicht. **Lösung:** Stubs bei jedem Build in der CI neu generieren. Proto-Dateiversionen fixieren. Einen Proto-Kompilierungsschritt in das Makefile aufnehmen.

- **Problem:** Interceptors verschlucken Exceptions – der Test ist grün, obwohl der gRPC-Aufruf tatsächlich fehlgeschlagen ist. **Lösung:** Immer `.result()` auf dem Response-Future aufrufen und auf `grpc.RpcError` prüfen.

## Siehe auch {#see-also}

- [[api-testing-requests]]
- [[allure-reporting]]
- [[docker-test-environments]]
