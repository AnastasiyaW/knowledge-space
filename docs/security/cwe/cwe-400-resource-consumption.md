---
description: "CWE-400: Attacker triggers uncontrolled CPU, memory, disk, or fd consumption via regex DoS, hash collision, zip bombs, XML entity expansion, or unbounded collections."
date: 2026-04-16
tags: [security, cwe, dos, redos, regex, zip-bomb, xml-bomb, algorithmic-complexity, resource-exhaustion]
level: Advanced
---

# CWE-400: Uncontrolled Resource Consumption

**CWE-400** | CWE Pillar: Resource Management | CVSS Base Score range: 5.3-7.5 (DoS) | Rank 24 in CWE Top 25

## Functional Semantics

The vulnerability class covers inputs that cause asymmetric resource consumption: attacker sends O(n) bytes, server expends O(n²) or O(2^n) CPU/memory. The application lacks an upper bound on the work performed for any single request. Exploitation does not require authentication or code injection; a single well-crafted request can consume all available resources of one type, degrading or denying service for all users.

Resource types attacked: CPU time, heap memory, stack frames (recursion), disk I/O, file descriptors, thread pool slots, database connection pool, outbound network bandwidth.

## Attack Surface Taxonomy

| Attack Class | Resource | Complexity | Examples |
|---|---|---|---|
| ReDoS — catastrophic backtracking | CPU | O(2^n) worst case | Evil regex on user-supplied string |
| Hash collision (HashDoS) | CPU | O(n²) per-bucket | Crafted HTTP POST params fill one hash bucket |
| Decompression bomb | Memory + Disk | O(compression_ratio) | 42.zip (4.5PB from 42KB), gzip bomb |
| XML entity expansion (Billion Laughs) | Memory | O(10^9) | Nested XML entity references |
| Quadratic algorithm | CPU | O(n²) | Regex with poor engine, naive string concat in loop |
| Unbounded collection growth | Memory | O(n) unbounded | Append to list without size cap |
| Connection pool exhaustion | File descriptors | O(open_conns) | Slow-read / Slowloris HTTP attack |
| Log flooding | Disk I/O | O(log_entries) | Request that triggers unbounded log output |
| GraphQL query depth | CPU + DB | O(depth^branching) | `{ user { friends { friends { friends ... } } } }` |
| gRPC stream flood | Memory + CPU | O(messages) | Unbounded streaming RPC with no backpressure |

## ReDoS — Catastrophic Backtracking

A regex engine using backtracking can exhibit exponential time complexity when a pattern contains nested quantifiers or alternation on overlapping character sets.

**Pattern anatomy of catastrophic regex:**
- `(a+)+` — nested quantifiers, the same `a` characters can be matched in exponentially many ways
- `(a|a)+` — alternation with identical branches
- `([a-zA-Z]+)*` — unbounded group with quantifier applied to group
- `(.*a){n}` — repeated match to a rare character with greedy `.*`

```python
# VULNERABLE: user-supplied string tested against catastrophic regex
import re
from flask import request

@app.route("/validate-email")
def validate_email():
    email = request.args.get("email", "")
    # Catastrophic: (a+)+ pattern equivalent — overlapping quantifiers
    # Input "aaaaaaaaaaaaaaaaaaa@" causes exponential backtracking
    pattern = r"^([a-zA-Z0-9_\-\.]+)+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email):  # hangs on crafted input
        return "valid"
    return "invalid"
```

```python
# FIXED: use re with timeout wrapper, or switch to possessive quantifiers / atomic groups
import re
import signal

def regex_with_timeout(pattern, string, timeout_sec=0.1):
    def handler(signum, frame):
        raise TimeoutError("Regex timeout")
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, timeout_sec)
    try:
        result = re.match(pattern, string)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    return result

# Better: use a non-backtracking regex engine
# pip install google-re2
import re2  # Google RE2 — linear time guarantee, no catastrophic backtracking
pattern = re2.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
if pattern.match(email):
    return "valid"
```

**Catastrophic patterns to flag in code review:**

| Pattern | Why catastrophic |
|---|---|
| `(a+)+` | Each `a` can participate in inner or outer group |
| `(\w+\s?)+` | Same character matches both groups ambiguously |
| `(.*,)*` | `.` matches `,`, creating exponential ambiguity |
| `([a-z]+)*` | Nested unbounded repetition |
| `^(([a-z])+.)+[A-Z]([a-z])+$` | Multiple overlapping groups |

## Decompression Bombs

```python
# VULNERABLE: no size limit on decompression
import zipfile, io
from flask import request

@app.route("/upload-zip")
def upload_zip():
    data = request.data  # attacker sends 42.zip (42KB → 4.5PB decompressed)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for name in zf.namelist():
            content = zf.read(name)  # reads entire decompressed content into memory
            process(content)
```

```python
# FIXED: enforce decompressed size limit
import zipfile, io

MAX_COMPRESSED_SIZE = 10 * 1024 * 1024    # 10 MB input
MAX_DECOMPRESSED_SIZE = 100 * 1024 * 1024  # 100 MB output
MAX_FILES = 100
MAX_COMPRESSION_RATIO = 10

@app.route("/upload-zip")
def upload_zip():
    if len(request.data) > MAX_COMPRESSED_SIZE:
        return "File too large", 413

    total_decompressed = 0
    with zipfile.ZipFile(io.BytesIO(request.data)) as zf:
        if len(zf.namelist()) > MAX_FILES:
            return "Too many files", 400
        for name in zf.namelist():
            info = zf.getinfo(name)
            total_decompressed += info.file_size
            if total_decompressed > MAX_DECOMPRESSED_SIZE:
                return "Decompressed size limit exceeded", 400
            # Check per-file compression ratio
            if info.compress_size > 0 and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
                return "Suspicious compression ratio", 400
            content = zf.read(name, pwd=None)
            process(content)
```

## XML Entity Expansion (Billion Laughs)

```xml
<!-- Billion Laughs attack: 9 entity levels, each expanding 10x → 10^9 entities -->
<?xml version="1.0"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
  ...
  <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<root>&lol9;</root>
```

```python
# VULNERABLE: default lxml/ElementTree settings allow entity expansion
from lxml import etree

def parse_xml(xml_bytes):
    return etree.fromstring(xml_bytes)  # processes entity expansion

# FIXED: disable entity expansion and DTD processing
from lxml import etree

def parse_xml_safe(xml_bytes):
    parser = etree.XMLParser(
        resolve_entities=False,  # do not expand &entities;
        no_network=True,         # no external entity fetches (also prevents XXE/SSRF)
        dtd_validation=False,
        load_dtd=False
    )
    return etree.fromstring(xml_bytes, parser=parser)
```

```java
// FIXED: Java SAX/DOM with entity expansion disabled
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setExpandEntityReferences(false);
DocumentBuilder db = dbf.newDocumentBuilder();
Document doc = db.parse(inputStream);
```

## Hash Collision / HashDoS

Attacker crafts POST parameters with keys that all hash to the same bucket, turning O(1) lookups into O(n) chain traversal. For n=100,000 parameters: O(n²) = 10^10 operations.

```python
# VULNERABLE: default dict/form parsing with no key count limit
from flask import request

@app.route("/process", methods=["POST"])
def process():
    # Flask/Werkzeug by default limits form keys but older versions did not
    data = request.form  # attacker posts 100,000 keys with hash collisions
    for key, value in data.items():  # O(n²) in a poor hash implementation
        store(key, value)
```

```python
# FIXED: limit form field count
from werkzeug.formparser import MultiPartParser

app.config['MAX_FORM_PARTS'] = 1000     # Werkzeug 2.3+
app.config['MAX_FORM_MEMORY_SIZE'] = 500_000  # 500KB

# Or explicit check:
@app.route("/process", methods=["POST"])
def process():
    if len(request.form) > 100:
        return "Too many form fields", 400
    data = request.form
```

Python 3.2+ uses hash randomization (`PYTHONHASHSEED`) by default, mitigating HashDoS for Python dicts. Java `HashMap` uses a tree structure for large buckets (Java 8+). PHP historically was the most affected platform.

## Unbounded Collection Growth

```javascript
// VULNERABLE: SSE/WebSocket with no client limit
const activeConnections = new Map(); // grows without bound

io.on("connection", (socket) => {
    activeConnections.set(socket.id, socket); // never cleaned up on error
    socket.on("subscribe", (topic) => {
        if (!subscriptions[topic]) subscriptions[topic] = [];
        subscriptions[topic].push(socket.id); // attacker subscribes 10M times
    });
});

// FIXED: per-client limits and cleanup
const MAX_CONNECTIONS = 10_000;
const MAX_SUBSCRIPTIONS_PER_CLIENT = 100;

io.on("connection", (socket) => {
    if (activeConnections.size >= MAX_CONNECTIONS) {
        socket.disconnect(true);
        return;
    }
    activeConnections.set(socket.id, socket);
    let clientSubCount = 0;

    socket.on("subscribe", (topic) => {
        if (++clientSubCount > MAX_SUBSCRIPTIONS_PER_CLIENT) {
            socket.disconnect(true);
            return;
        }
        subscriptions[topic] = subscriptions[topic] || [];
        subscriptions[topic].push(socket.id);
    });

    socket.on("disconnect", () => {
        activeConnections.delete(socket.id);
        // cleanup subscriptions...
    });
});
```

## GraphQL Query Depth / Complexity

```graphql
# ATTACK: exponential DB queries through unbounded nesting
query {
    user(id: 1) {
        friends {           # N users
            friends {       # N² users
                friends {   # N³ users
                    name
                }
            }
        }
    }
}
```

```javascript
// FIXED: depth limiting with graphql-depth-limit
const depthLimit = require("graphql-depth-limit");
const { createComplexityLimitRule } = require("graphql-validation-complexity");

const schema = makeExecutableSchema({ typeDefs, resolvers });
const server = new ApolloServer({
    schema,
    validationRules: [
        depthLimit(5),                    // max nesting depth
        createComplexityLimitRule(1000),  // total complexity score
    ]
});
```

## Detection Heuristics

**Static analysis triggers:**
- Regex with nested quantifiers applied to user-controlled string: `re.match(pattern, user_input)` where pattern contains `(X+)+`, `(X*Y*)+`, `(\w+\s?)+`
- `zipfile.ZipFile.read()`, `tarfile.extractall()`, `gzip.decompress()` without size check
- XML parsing: `lxml.etree.fromstring()` without `XMLParser(resolve_entities=False)`, `DocumentBuilderFactory.newDocumentBuilder()` without feature flags
- `list.append(item)` inside a request handler with no size cap on the list
- `dict` or `map` built from user-supplied keys with no count limit
- Recursive function where recursion depth is user-controlled (tree traversal depth = user JSON nesting level)
- `json.loads(user_data)` in Python — safe from injection but Python's json module has a max recursion depth for nested structures; deeply nested JSON causes RecursionError

**Configuration triggers:**
- `MAX_CONTENT_LENGTH` not set in Flask (unlimited request body)
- No `client_max_body_size` in Nginx config
- GraphQL server with no depth/complexity limits
- Elasticsearch with no index.mapping.total_fields.limit
- Redis with no `maxmemory` policy

**False positive indicators:**
- Regex with nested quantifiers where the input string is bounded by a previous check (`if len(s) > 100: reject`) — the bound eliminates catastrophic backtracking if it is tight enough. Flag for review but note the mitigation.
- Decompression of files from the application's own static assets (not user-supplied) — no attacker control.
- XML parsing of responses from trusted internal APIs (not user-supplied XML) — lower risk, but external API compromise could introduce malicious XML.
- `list.append()` inside a request handler where the list is ephemeral (local variable, not shared state) and request body size is limited upstream (Nginx `client_max_body_size`).

## Gotchas

- **re2 is not a drop-in replacement for Python re.** `re2` does not support backreferences (`\1`), lookahead/lookbehind assertions, or some Unicode features. Evaluate regex features needed before switching engines.
- **Regex compilation is also a DoS vector.** Some regex engines exhibit polynomial time during *compilation* of pathological patterns, not just matching. If user supplies the pattern (rare but occurs in filter/search features), the engine selection matters.
- **ZIP path traversal vs. ZIP bomb are separate issues.** Checking decompressed size does not prevent `../../../etc/cron.d/evil` path traversal. Both checks are needed for ZIP processing.
- **JSON depth limits differ by library.** Python `json.loads` raises `RecursionError` at ~1000 nesting levels (CPython default recursion limit). Node.js `JSON.parse` is iterative and does not recursion-bomb but a deeply nested structure still consumes O(n) memory. Set `sys.setrecursionlimit` or use `json.loads` with depth-limited pre-check for deeply nested untrusted JSON.
- **HTTP/2 stream multiplexing enables connection-level DoS.** A single TCP connection carries multiple streams; a client opening the maximum concurrent streams and then sending RST_STREAM forces the server to allocate and immediately tear down stream state. Limit `http2_max_concurrent_streams` in server config.
- **Rate limiting does not prevent single-request DoS.** A 42.zip bomb, a billion-laughs XML, or a catastrophic regex can exhaust resources from a single request before rate limiting triggers. Content-based defenses (size checks, entity limits, RE2) are required alongside rate limiting.

## See Also

- CWE-190: Integer Overflow — overflow in size calculations can lead to allocation that undercounts, with a related DoS when the correct size is later needed
- CWE-611: XML External Entities — XXE shares XML parser configuration fixes with billion laughs
- CWE-020: Input Validation — upstream validation: limit size, depth, and count before processing
- CWE-770: Allocation Without Limits — related: allocation without checking available resources
