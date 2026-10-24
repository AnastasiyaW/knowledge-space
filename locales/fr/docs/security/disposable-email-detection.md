---
title: "Détection des adresses e-mail jetables"
category: concepts
tags: [security, anti-fraud, email, disposable, multi-account, normalization]
level: 3
source_sha256: a77c7c4e4111eec988f792b0ef4ec9e459c2066123bf55d97f438b21ebca5827
translation: machine
translated_at: '2026-10-24'
---
# Détection des adresses e-mail jetables {#disposable-email-detection}

Référence backend pour la détection des adresses e-mail jetables et des abus par comptes multiples lors de l'inscription. Couvre les listes de blocage, les vérifications DNS, la normalisation des adresses et les signaux de liaison de comptes.

## Points clés {#key-facts}

- Les listes de blocage statiques détectent 60 à 80 % des inscriptions jetables évidentes sans coût ; la superposition de listes curées et de listes générées automatiquement porte la couverture à 85-90 % — voir [[anti-fraud-behavioral-analysis]] pour la manière dont les signaux e-mail se combinent aux signaux comportementaux
- L'astuce du point Gmail et l'adressage avec suffixe (plus addressing) ne figurent PAS dans les listes de domaines jetables ; ils nécessitent une normalisation au moment de l'écriture
- Les services d'alias de confidentialité (`*@privaterelay.appleid.com`, `*.mozmail.com`, `*.simplelogin.co`) sont des boîtes légitimes : les bloquer de façon stricte fait perdre des utilisateurs soucieux de leur vie privée à forte valeur client (LTV) ; ne appliquer qu'un blocage souple
- L'absence d'enregistrement MX est un signal d'échec fiable ; la présence d'un enregistrement MX n'est PAS un indicateur de réussite fiable (les domaines en catch-all acceptent n'importe quelle adresse)
- `disposable-email-domains/disposable-email-domains` (npm : `disposable-email-domains`) — curée par la communauté, environ 3 000 entrées, faible taux de faux positifs ; cadence de mise à jour : manuelle
- `disposable/disposable` (GitHub) — générée automatiquement chaque jour, plus de 100 000 domaines, taux de faux positifs plus élevé ; à utiliser comme superposition secondaire
- La prise d'empreinte numérique de l'appareil pour lier des comptes multiples exige un consentement RGPD au titre des lignes directrices 2/2023 de l'EDPB (art. 5(3) de la directive ePrivacy) — voir [[compliance-and-regulations]]
- Le hachage des e-mails (SHA-256 de la forme canonique) avant stockage respecte le principe de minimisation des données du RGPD ; MaxMind minFraud accepte nativement les e-mails pré-hachés

## Signaux de détection {#detection-signals}

### 1. Vérification par liste de blocage de domaines {#1-domain-blocklist-check}

Superposer la liste curée (blocage strict) à la liste générée automatiquement (blocage souple). Charger les deux listes en mémoire au démarrage ; actualiser la liste générée automatiquement toutes les 24 h via cron.

```python
import hashlib
import json
import re
from pathlib import Path
from typing import Literal

# Load curated list (npm package ships JSON; or use python equivalent)
# pip install disposable-email-domains  (Python port: pyIsEmail / disposable-email-domains)
# For the auto-generated list, fetch:
# https://raw.githubusercontent.com/disposable/disposable/master/domains.json

CURATED: set[str] = set()   # populated from disposable-email-domains
AUTO_GEN: set[str] = set()  # populated from disposable/disposable daily

def load_lists(curated_path: str, autogen_path: str) -> None:
    global CURATED, AUTO_GEN
    with open(curated_path) as f:
        CURATED = set(json.load(f))
    with open(autogen_path) as f:
        AUTO_GEN = set(json.load(f))

def check_domain(domain: str) -> Literal["block", "softblock", "pass"]:
    d = domain.lower()
    if d in CURATED:
        return "block"
    if d in AUTO_GEN:
        return "softblock"
    return "pass"
```

### 2. Normalisation des adresses (Gmail, googlemail) {#2-address-normalization-gmail-googlemail}

Normaliser au moment de l'écriture et stocker à la fois le hachage canonique et le hachage brut. Rechercher par hachage canonique à la connexion pour détecter les doublons appartenant à la même personne.

```python
def canonicalize_email(email: str) -> str:
    """
    Canonical form used ONLY for dedup lookups, never shown to user.
    Covers: gmail.com, googlemail.com (dots + plus-addressing).
    Other providers (Yahoo, Outlook) do NOT strip dots — do not generalize.
    """
    local, _, domain = email.lower().strip().partition("@")
    domain = domain.strip()

    # googlemail.com is an alias for gmail.com
    if domain == "googlemail.com":
        domain = "gmail.com"

    if domain == "gmail.com":
        # Strip plus-suffix: john+anything@gmail.com -> john@gmail.com
        local = local.split("+")[0]
        # Remove dots: j.o.h.n -> john
        local = local.replace(".", "")

    return f"{local}@{domain}"

def email_hashes(raw_email: str) -> dict[str, str]:
    canonical = canonicalize_email(raw_email)
    return {
        "raw_hash": hashlib.sha256(raw_email.lower().encode()).hexdigest(),
        "canonical_hash": hashlib.sha256(canonical.encode()).hexdigest(),
        "canonical": canonical,  # store temporarily for dedup query; discard after
    }
```

### 3. Validation des enregistrements MX {#3-mx-record-validation}

```python
import dns.asyncresolver  # dnspython >= 2.0

async def has_mx(domain: str) -> bool:
    """No MX -> hard-block. MX present -> not sufficient (catch-all passes). Cache 24 h."""
    try:
        answers = await dns.asyncresolver.resolve(domain, "MX")
        return len(answers) > 0
    except Exception:
        return False
# Node: dns.promises.resolveMx(domain) -> records.length > 0
```

### 4. API de réputation payante (MaxMind minFraud) {#4-paid-reputation-api-maxmind-minfraud}

Un seul appel couvre `email.is_disposable`, le risque lié à l'IP et la détection de proxy/VPN. N'appeler qu'après que les contrôles gratuits ont été franchis.

```python
# pip install minfraud
from minfraud import AsyncClient

async def minfraud_score(email_sha256: str, ip: str, fp: str | None, acct: int, key: str) -> dict:
    async with AsyncClient(account_id=acct, license_key=key) as c:
        req = {"device": {"ip_address": ip}, "email": {"address": email_sha256, "hash_address": True}}
        if fp:
            req["device"]["fingerprint"] = fp
        r = await c.score(req)
        return {
            "risk_score": r.risk_score,           # 0-100
            "is_disposable": r.email.is_disposable if r.email else None,
            "is_anonymous": r.ip_address.traits.is_anonymous if r.ip_address else None,
        }
```

## Liaison de comptes multiples {#multi-account-linking}

### Hachage des e-mails normalisés {#normalized-email-hashing}

```sql
-- Store at registration; look up on new signup
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    email_raw_hash       TEXT NOT NULL,       -- SHA-256(raw_input.lower())
    email_canonical_hash TEXT NOT NULL,       -- SHA-256(canonicalize(email))
    created_at  TIMESTAMPTZ DEFAULT now()
);
CREATE UNIQUE INDEX idx_users_canonical ON users(email_canonical_hash);

-- Signup dedup query (before INSERT):
-- SELECT id FROM users WHERE email_canonical_hash = $1 LIMIT 1;
-- Match -> same person or abuse -> block with "account already exists, try logging in"
```

### Vélocité des empreintes d'appareil {#device-fingerprint-velocity}

Bibliothèques de prise d'empreinte d'appareil : ThumbmarkJS (MIT, précision d'environ 80 % en mode OSS ; l'API Pro la porte à environ 99 %), FingerprintJS Pro (99,5 %, à partir de 99 $/mois). Voir [[browser-and-device-fingerprinting]] pour le fonctionnement interne des signaux.

```python
# Redis sorted-set velocity check (Python/redis-py)
import redis.asyncio as redis
import time

r = redis.Redis()

async def fingerprint_signup_count_30d(fp: str) -> int:
    key = f"fp_signups:{fp}"
    now = time.time()
    cutoff = now - 30 * 86400
    # Remove entries older than 30 days
    await r.zremrangebyscore(key, "-inf", cutoff)
    count = await r.zcard(key)
    # Record this signup attempt
    await r.zadd(key, {str(now): now})
    await r.expire(key, 31 * 86400)
    return count

# Thresholds (tune via shadow-mode data before enforcing):
# count > 3 in 30d -> soft-block (require phone verify)
# count > 10 in 30d -> hard-block
```

### Table du journal d'audit {#audit-log-table}

```sql
CREATE TABLE signup_audit_log (
    id                   BIGSERIAL PRIMARY KEY,
    ts                   TIMESTAMPTZ DEFAULT now(),
    email_canonical_hash TEXT NOT NULL,
    email_raw_hash       TEXT NOT NULL,
    ip                   INET NOT NULL,
    fingerprint          TEXT,
    action               TEXT NOT NULL,   -- allow | softblock | block
    reason               TEXT NOT NULL,
    score                INT,
    signals_json         JSONB            -- full minFraud response
);
CREATE INDEX idx_audit_canonical ON signup_audit_log(email_canonical_hash);
CREATE INDEX idx_audit_fp        ON signup_audit_log(fingerprint);
CREATE INDEX idx_audit_ip        ON signup_audit_log(ip);
CREATE INDEX idx_audit_ts        ON signup_audit_log(ts);
```

## Implémentation {#implementation}

Pipeline Python complet combinant actualisation des listes de blocage, normalisation et décision :

```python
import asyncio
import hashlib
import json
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Literal

import aiohttp
import dns.asyncresolver
import redis.asyncio as aioredis

CURATED_URL = "https://cdn.jsdelivr.net/npm/disposable-email-domains@latest/disposable_email_blocklist.conf"
AUTOGEN_URL = "https://raw.githubusercontent.com/disposable/disposable/master/domains.json"

_curated: set[str] = set()
_autogen: set[str] = set()
_redis: aioredis.Redis | None = None


async def refresh_lists(session: aiohttp.ClientSession) -> None:
    global _curated, _autogen
    async with session.get(CURATED_URL) as r:
        text = await r.text()
        _curated = {line.strip() for line in text.splitlines() if line.strip()}
    async with session.get(AUTOGEN_URL) as r:
        _autogen = set(await r.json())


def canonicalize(email: str) -> str:
    local, _, domain = email.lower().strip().partition("@")
    if domain == "googlemail.com":
        domain = "gmail.com"
    if domain == "gmail.com":
        local = local.split("+")[0].replace(".", "")
    return f"{local}@{domain}"


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


async def mx_ok(domain: str, r: aioredis.Redis) -> bool:
    cache_key = f"mx:{domain}"
    cached = await r.get(cache_key)
    if cached is not None:
        return cached == b"1"
    try:
        answers = await dns.asyncresolver.resolve(domain, "MX")
        result = len(answers) > 0
    except Exception:
        result = False
    await r.setex(cache_key, 86400, b"1" if result else b"0")
    return result


@dataclass
class Decision:
    action: Literal["allow", "softblock", "block"]
    reason: str
    score: int


async def evaluate(
    raw_email: str,
    ip: str,
    fingerprint: str | None,
    r: aioredis.Redis,
) -> Decision:
    domain = raw_email.lower().split("@")[-1]

    # Blocklist
    if domain in _curated:
        return Decision("block", "disposable_curated", 100)
    if domain in _autogen:
        return Decision("softblock", "disposable_autogen", 70)

    # MX
    if not await mx_ok(domain, r):
        return Decision("block", "no_mx", 100)

    # Canonical dedup (pseudo — implement with real DB)
    canonical = canonicalize(raw_email)
    # exists = await db.fetchval("SELECT 1 FROM users WHERE email_canonical_hash=$1", sha256(canonical))
    # if exists: return Decision("block", "canonical_duplicate", 100)

    # Fingerprint velocity
    if fingerprint:
        key = f"fp:{fingerprint}"
        now = time.time()
        await r.zremrangebyscore(key, "-inf", now - 30 * 86400)
        count = await r.zcard(key)
        await r.zadd(key, {str(now): now})
        await r.expire(key, 31 * 86400)
        if count > 10:
            return Decision("block", "fp_velocity", 90)
        if count > 3:
            return Decision("softblock", "fp_velocity_warn", 65)

    # IP velocity
    ip_key = f"ip_h:{ip}"
    ip_count = int(await r.incr(ip_key))
    if ip_count == 1:
        await r.expire(ip_key, 3600)
    if ip_count > 5:
        return Decision("softblock", "ip_velocity", 60)

    return Decision("allow", "clean", 0)


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        await refresh_lists(session)

    r = aioredis.Redis()
    result = await evaluate("john.doe+test@gmail.com", "1.2.3.4", "fp-abc123", r)
    print(result)  # Decision(action='allow', reason='clean', score=0)
    # canonical: johndoe@gmail.com — dots and suffix stripped


if __name__ == "__main__":
    asyncio.run(main())
```

Actualiser les listes de blocage chaque jour via cron (`curl -sS <AUTOGEN_URL> -o domains.json && systemctl reload app`) ou sous forme de tâche asyncio en arrière-plan au démarrage.

## Pièges courants {#gotchas}

- **Problème :** Les listes deviennent obsolètes — de nouveaux services jetables (clones de mailtm, variantes de temp-mail) apparaissent chaque semaine ; la liste curée peut accuser un retard de 3 à 7 jours, la liste générée automatiquement jusqu'à 24 h. -> **Correctif :** Superposer les deux listes ; s'abonner au flux des publications GitHub de `disposable/disposable` ; envisager un cron quotidien qui récupère le JSON et le recharge à chaud dans l'ensemble en mémoire de l'application, sans redémarrage. Signaler les domaines récents (enregistrés depuis moins de 30 jours) via WHOIS comme signal de blocage souple supplémentaire.

- **Problème :** Blocage excessif des alias de confidentialité légitimes. Firefox Relay (`*.mozmail.com`), Apple Hide My Email (`*@privaterelay.appleid.com`), SimpleLogin et Addy.io figurent dans certaines listes générées automatiquement ; un blocage strict rejette des utilisateurs à forte valeur client. Bleeping Computer a documenté la réaction négative de la communauté lorsque Firefox Relay a été ajouté à `disposable-email-domains` en 2022. -> **Correctif :** Maintenir une liste d'autorisation explicite des domaines de relais de confidentialité ; toujours appliquer un blocage souple (exiger une vérification par téléphone ou une confirmation supplémentaire) plutôt qu'un blocage strict ; ne jamais ajouter ces domaines à la liste curée de blocage strict.

- **Problème :** Normalisation de type Gmail (suppression des points, suffixes) appliquée aux fournisseurs autres que Gmail. Yahoo et Outlook ne suppriment PAS les points (`j.o.h.n@yahoo.com` et `john@yahoo.com` sont deux boîtes différentes). Appliquer la normalisation Gmail globalement génère de faux doublons pour les utilisateurs Yahoo et Outlook. -> **Correctif :** Limiter la suppression des points à `gmail.com` et `googlemail.com` uniquement ; pour l'adressage avec suffixe, Fastmail et d'autres le prennent en charge, mais ne le supprimer qu'après avoir vérifié le comportement du fournisseur — ou ne le supprimer que pour Gmail, où il s'agit d'un comportement documenté.

- **Problème :** Exposition au RGPD lors du stockage de hachages d'e-mails liés à des empreintes d'appareil. Au titre des lignes directrices 2/2023 de l'EDPB, la combinaison d'un e-mail haché, d'une empreinte d'appareil et d'une IP constitue un profilage à haut risque ; l'art. 35 du RGPD peut exiger une AIPD avant le déploiement. -> **Correctif :** Hacher tous les e-mails (SHA-256 de la forme canonique en minuscules) avant stockage ; purger les entrées de `fingerprint_aggregations` selon une fenêtre glissante de 30 jours ; ne conserver les IP brutes que 90 jours au maximum ; documenter la base de l'intérêt légitime (considérant 49 du RGPD) dans la politique de confidentialité et dans une évaluation de l'intérêt légitime — détails dans [[compliance-and-regulations]].

- **Problème :** La validation MX produit des faux négatifs pour les domaines d'entreprise en catch-all. `random123@small-startup.io` n'est peut-être pas une boîte réelle, mais le serveur SMTP du domaine en catch-all renverra un enregistrement MX valide et acceptera la connexion SMTP. -> **Correctif :** N'utiliser la vérification MX que comme signal d'échec strict (pas de MX = manifestement invalide) ; ne pas utiliser la présence d'un MX comme signal de réussite pour les adresses ambiguës ; compléter avec des API payantes de vérification d'e-mail (IPQualityScore, MaxMind `is_disposable`) pour confirmer la délivrabilité au niveau SMTP.

## Voir aussi {#see-also}

- [[anti-fraud-behavioral-analysis]] — signaux comportementaux (vélocité, durée de session) qui complètent les signaux au niveau de l'e-mail
- [[browser-and-device-fingerprinting]] — fonctionnement interne des empreintes d'appareil (canvas, WebGL, AudioContext) utilisées pour la liaison de comptes multiples
- [[authentication-and-authorization]] — architecture des jetons et des sessions qui détermine la propagation des données de liaison de comptes après l'inscription
- [[compliance-and-regulations]] — RGPD art. 5(3), directive ePrivacy, exigences d'AIPD pour la prise d'empreinte
- [[secure-backend-development]] — schémas de limitation de débit, vérifications de vélocité avec Redis, gestion des secrets pour les clés API (MaxMind, Turnstile)
- Sources de listes de blocage : [disposable-email-domains/disposable-email-domains](https://github.com/disposable-email-domains/disposable-email-domains), [disposable/disposable](https://github.com/disposable/disposable), [amieiro/disposable-email-domains](https://github.com/amieiro/disposable-email-domains)
- Référence sur la normalisation des e-mails : [UserCheck — How to Normalize Email Addresses](https://www.usercheck.com/guides/how-to-normalize-email-addresses)
- Lignes directrices 2/2023 de l'EDPB sur l'art. 5(3) de la directive ePrivacy : [edpb.europa.eu](https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202302_technical_scope_art_53_eprivacydirective_v2_en_0.pdf)
- Documentation de l'API MaxMind minFraud : [dev.maxmind.com/minfraud](https://dev.maxmind.com/minfraud/)
- Cloudflare Turnstile (filtre anti-bot, gratuit, conforme à l'UE) : [cloudflare.com/products/turnstile](https://www.cloudflare.com/application-services/products/turnstile/)
