---
title: gRPC Testing with Python
category: tools
tags: [grpc, protobuf, api-testing, code-generation, interceptors, wiremock, mocking]
---

# gRPC Testing with Python

Testing gRPC services: protobuf compilation, client generation, interceptors for logging, Allure integration, and mocking with WireMock.

## Protobuf to Python

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

Compile:

```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  --pyi_out=./generated \
  proto/user.proto
```

Output: `user_pb2.py` (messages), `user_pb2_grpc.py` (stubs), `user_pb2.pyi` (type hints).

## Basic gRPC Test

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

## Interceptors for Logging

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

## Allure Integration

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

## Mocking with WireMock

WireMock supports gRPC mocking via extension:

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

Switching between real and mock:

```python
@pytest.fixture
def grpc_channel(config):
    if config.use_mock:
        host = config.wiremock_host
    else:
        host = config.grpc_host
    return grpc.insecure_channel(host)
```

## Proto File Management with pbreflect

```bash
pip install grpc-reflection
```

Download `.proto` files from a running server:

```python
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc

def get_service_protos(channel):
    stub = reflection_pb2_grpc.ServerReflectionStub(channel)
    # list services, then get file descriptors
```

Useful when proto files are not shared directly.

## Streaming RPCs

```python
def test_list_users_stream(user_stub):
    """Server streaming: one request, multiple responses."""
    request = user_pb2.Empty()
    users = list(user_stub.ListUsers(request))
    assert len(users) > 0
    for user in users:
        assert user.id != ""
```

## Gotchas

- **Issue:** `grpc._channel._InactiveRpcError` with `UNAVAILABLE` status - server not reachable. **Fix:** Check channel connectivity before tests: `grpc.channel_ready_future(channel).result(timeout=5)`. Add retry logic or wait-for-port in CI.

- **Issue:** Proto file changes break generated code silently - old stubs still importable but fields wrong. **Fix:** Regenerate stubs in CI on every build. Pin proto file versions. Add a proto compilation step to your Makefile.

- **Issue:** Interceptors swallow exceptions - test passes but gRPC call actually failed. **Fix:** Always call `.result()` on the response future and check for `grpc.RpcError`.

## See Also

- [[api-testing-requests]]
- [[allure-reporting]]
- [[docker-test-environments]]
